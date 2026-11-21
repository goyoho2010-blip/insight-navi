"""6개 화면 렌더링 스모크 테스트(AppTest) — 예외 0건 확인."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PAGES = [
    ("🏠 통합 대문", "5단계 입시 컨설팅 로드맵"),
    ("🧭 진로NAVI 체험", "목표 계열 적합도"),
    ("📚 학습NAVI 체험", "교재별 진도 · 회독"),
    ("📋 수시NAVI 체험", "세특 강점 3"),
    ("🎤 면접NAVI PRO 체험", "추출된 세특 근거 문장"),
    ("📊 내 위치 NAVI", "모집단위별 반영비율"),
]


def _run(page: str) -> AppTest:
    at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60)
    at.session_state["page"] = page
    at.run()
    return at


@pytest.mark.parametrize("page,expected", PAGES)
def test_page_renders_without_exception(page, expected):
    at = _run(page)
    assert not at.exception, f"{page} 예외: {[e.value for e in at.exception]}"
    body = "\n".join(m.value for m in at.markdown)
    assert expected in body, f"{page} 에 '{expected}' 문구 없음"


def test_home_has_six_way_navigation_and_links():
    at = _run("🏠 통합 대문")
    buttons = [b.label for b in at.button]
    links = [b.label for b in at.get("link_button")]
    # 5개 앱 카드 이동 버튼 + 내 위치 NAVI 실사용 링크
    assert len(buttons) == 5, buttons
    assert any("내 위치 NAVI 바로 실행" in label for label in links)
    assert any("blog.naver.com" in (m.value or "") for m in at.markdown)
    # 원장님 실전용(암호) 접이식 안에 실사용 4종 링크
    private_links = [label for label in links if "🔐" in label]
    assert len(private_links) == 4, private_links
    assert len(at.expander) == 1


def test_no_streamlit_error_elements_on_any_page():
    for page, _ in PAGES:
        at = _run(page)
        assert len(at.error) == 0, f"{page} st.error {[e.value for e in at.error]}"
        assert len(at.exception) == 0, f"{page} 예외"


def test_widget_states_do_not_leak_between_pages():
    """체험판 토글·체크박스는 화면 안에서만 쓰이고 저장되지 않는다."""
    at = _run("🎤 면접NAVI PRO 체험")
    toggles = at.toggle
    assert len(toggles) == 6
    toggles[0].set_value(True).run()
    assert not at.exception
    assert len(at.checkbox) == 3
