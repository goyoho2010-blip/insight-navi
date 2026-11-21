"""demo_data 무결성 · 가명/PII 없음 · 외부 의존 없음 검증."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import demo_data as D  # noqa: E402

FICTIONAL_NAMES = {"김서연", "이준호"}

PHONE_RE = re.compile(r"0\d{1,2}[-.\s]?\d{3,4}[-.\s]?\d{4}")
RRN_RE = re.compile(r"\d{6}\s?-\s?\d{7}")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
SCHOOL_RE = re.compile(r"(초등학교|중학교|고등학교|여자고|남자고)")
FORBIDDEN_IMPORTS = ("openai", "supabase", "sqlalchemy", "psycopg", "pymysql", "requests", "httpx")


# ---------------------------------------------------------------- 기본 무결성
def test_students_are_two_named_sample_students():
    students = D.students()
    assert len(students) == 2
    assert {s["name"] for s in students} == FICTIONAL_NAMES
    for s in students:
        for key in ("id", "name", "label", "grade", "track", "interest", "record", "summary",
                    "strength_keywords"):
            assert s.get(key), f"{s.get('id')} 에 {key} 없음"
        assert s["name"] in s["label"]


def test_every_student_has_all_four_demo_blocks():
    for s in D.students():
        sid = s["id"]
        assert D.CAREER[sid]["majors"] and len(D.CAREER[sid]["majors"]) == 3
        assert len(D.CAREER[sid]["books"]) == 3
        assert len(D.CAREER[sid]["track_fit"]) == 3
        assert D.LEARNING[sid]["materials"]
        assert set(D.SUSI[sid]["scores"]) == {"학업역량", "진로역량", "공동체역량"}
        assert D.INTERVIEW[sid]["evidence"] and D.INTERVIEW[sid]["questions"]


def test_career_book_fields_complete():
    for sid, block in D.CAREER.items():
        for book in block["books"]:
            assert book["title"] and book["author"]
            assert len(book["keywords"]) >= 2
            assert book["question"].rstrip().endswith(("?", "라.", "가?")) or "?" in book["question"]
            assert book["link"]
        for major in block["majors"]:
            assert 0 < major["fit"] <= 100
            assert major["why"] and major["courses"]


def test_nav_targets_exist_in_pages():
    """대문 카드·로드맵의 이동 대상이 실제 화면 목록과 맞는지."""
    app_source = (ROOT / "app.py").read_text(encoding="utf-8")
    pages_block = app_source.split("PAGES = [", 1)[1].split("]", 1)[0]
    pages = set(re.findall(r'"([^"]+)"', pages_block))
    for step in D.ROADMAP:
        assert step["page"] in pages, step["page"]
    for card in D.APP_CARDS:
        assert card["page"] in pages, card["page"]
    assert len(pages) == 6


def test_home_page_copy_matches_brief():
    assert "5단계 통합 컨설팅 허브" in D.BRAND_SUB
    assert D.BRAND_TITLE == "인사이트 나비(NAVI) 통합 컨설팅 솔루션"
    assert "입력·저장 없음" in D.BANNER
    assert D.MYRANKING_URL == "https://myranking-navi.streamlit.app"
    assert D.BLOG_URL == "https://blog.naver.com/goyoho"
    assert len(D.PRIVATE_APPS) == 4


# ---------------------------------------------------------------- 수치 정합성
def test_learning_kpi_math():
    kpi = D.learning_kpis("seoyeon")
    rows = D.learning_rows("seoyeon")
    assert kpi["completion"] == round(sum(r["progress"] for r in rows) / len(rows))
    assert kpi["delta"] == kpi["completion"] - kpi["prev_completion"]
    # 점검일 7일 이내 + 진도 80% 미만 = 위험교재
    expect = sum(1 for r in rows if r["dday"] <= D.DANGER_DAYS and r["progress"] < D.DANGER_PROGRESS)
    assert kpi["danger_count"] == expect == 2
    for r in rows:
        assert 0 <= r["progress"] <= 100
        assert r["current_rounds"] <= r["target_rounds"]
        assert r["dday"] == (r["check_date"] - D.DEMO_TODAY).days


def test_susi_score_equals_detail_sum():
    for sid, block in D.SUSI.items():
        for comp, items in block["detail"].items():
            got = sum(score for _, score, _ in items)
            total = sum(max_score for _, _, max_score in items)
            assert total == 100, (sid, comp, total)
            assert got == block["scores"][comp], (sid, comp, got, block["scores"][comp])
            assert all(0 <= score <= max_score for _, score, max_score in items)


def test_interview_question_stages():
    for sid, block in D.INTERVIEW.items():
        stages = sorted({q["stage"] for q in block["questions"]})
        assert stages == [1, 2, 3], (sid, stages)
        for q in block["questions"]:
            assert q["q"].strip()
            assert q["point"].strip()
            assert len(q["checkpoints"]) >= 3
        stage3 = [q for q in block["questions"] if q["stage"] == 3]
        assert all("진실성" in q["stage_name"] for q in stage3)


def test_ranking_numbers_match_source_data():
    assert D.RANKING_META["units"] == 4165
    assert D.RANKING_META["subjects"] == 22
    assert len(D.GRADE_CUTS) == 7
    for row in D.GRADE_CUTS:
        assert row["g1"] > row["g2"] > row["g3"]
        assert 0 < row["g1"] <= 100
    for row in D.RATIO_EXAMPLES:
        assert row["kor"] + row["math"] + row["eng"] + row["inq"] + row["hist"] > 0


# ---------------------------------------------------------------- 가명 · PII
@pytest.mark.parametrize("filename", ["demo_data.py", "app.py"])
def test_no_pii_patterns(filename):
    text = (ROOT / filename).read_text(encoding="utf-8")
    assert not PHONE_RE.search(text), "전화번호 형태 발견"
    assert not RRN_RE.search(text), "주민등록번호 형태 발견"
    assert not EMAIL_RE.search(text), "이메일 형태 발견"
    assert not SCHOOL_RE.search(text), "학교명 형태 발견"


def test_no_real_student_profile_claims():
    """실제 학생처럼 읽히는 고유 식별 정보(생년월일·학번·반)가 없는지."""
    text = (ROOT / "demo_data.py").read_text(encoding="utf-8")
    assert not re.search(r"\b\d{4}[-년]\s?\d{1,2}[-월]\s?\d{1,2}일?\s?생", text)
    assert "학번" not in text


def test_fictional_notice_present():
    assert "가명" in D.FICTIONAL_NOTICE
    assert "가명" in D.LEARNING["seoyeon"]["consult_note"] or "가명" in D.FICTIONAL_NOTICE


# ---------------------------------------------------------------- 외부 의존 없음
@pytest.mark.parametrize("filename", ["demo_data.py", "app.py"])
def test_no_external_service_imports(filename):
    text = (ROOT / filename).read_text(encoding="utf-8")
    for bad in FORBIDDEN_IMPORTS:
        assert f"import {bad}" not in text, f"{filename} 이 {bad} 를 import"
    for bad_word in ("api_key", "API_KEY", "OPENAI", "SUPABASE_URL", "service_role"):
        assert bad_word not in text, f"{filename} 에 {bad_word} 흔적"


def test_only_expected_imports():
    text = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "import demo_data as D" in text
    assert "altair" in text and "pandas" in text
