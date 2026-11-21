"""인사이트 나비(NAVI) 통합 컨설팅 솔루션 — 통합 대문 + 4종 체험판 + 내 위치 NAVI 연결.

- 로그인 없는 대문(허브): 5단계 입시 컨설팅 흐름을 한눈에 보고 눌러 볼 수 있다.
- 체험판 4종(진로·학습·수시·면접)은 100% 내장 샘플 데이터로 동작한다.
  OpenAI 호출 없음 · Supabase/DB 연결 없음 · 개인정보 0건.
- 내 위치 NAVI는 이미 공개된 실사용 앱으로 바로 연결한다.
"""

from __future__ import annotations

import altair as alt
import pandas as pd
import streamlit as st

import demo_data as D

APP_TITLE = D.BRAND_TITLE

PAGES = [
    "🏠 통합 대문",
    "🧭 진로NAVI 체험",
    "📚 학습NAVI 체험",
    "📋 수시NAVI 체험",
    "🎤 면접NAVI PRO 체험",
    "📊 내 위치 NAVI",
]

NAVY = "#17233B"
TEAL = "#12A3B4"
AMBER = "#E8A33D"
RED = "#D64545"
SLATE = "#5B6B84"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="auto",  # 모바일에서는 접힌 채로 시작
)

# ---------------------------------------------------------------------------
# 스타일
# ---------------------------------------------------------------------------
st.markdown(
    """
<style>
  .block-container { padding-top: 1.1rem; padding-bottom: 2.4rem; max-width: 1180px; }
  html, body, [class*="css"] { font-family: "Pretendard", "Apple SD Gothic Neo",
      "Malgun Gothic", "Noto Sans KR", sans-serif; }

  /* 상단 헤더 */
  .hub-hero {
    background: linear-gradient(135deg, #17233B 0%, #1E3A5F 55%, #12586B 100%);
    border-radius: 18px; padding: 22px 24px 20px; color: #FFFFFF;
    box-shadow: 0 10px 26px rgba(23,35,59,.18);
  }
  .hub-badge {
    display: inline-block; font-size: 11px; letter-spacing: .12em; font-weight: 800;
    color: #9EE7F1; background: rgba(158,231,241,.12); border: 1px solid rgba(158,231,241,.35);
    border-radius: 999px; padding: 3px 10px; margin-bottom: 10px;
  }
  .hub-hero h1 { font-size: 25px; line-height: 1.3; margin: 0 0 6px; font-weight: 800; letter-spacing: -.02em; }
  .hub-hero .hub-sub { font-size: 13.5px; color: #C7D6E6; margin: 0 0 14px; }
  .hub-tags { display: flex; flex-wrap: wrap; gap: 6px; }
  .hub-tags span {
    font-size: 11.5px; font-weight: 700; color: #E7F3F7;
    background: rgba(255,255,255,.10); border: 1px solid rgba(255,255,255,.18);
    border-radius: 999px; padding: 4px 10px; white-space: nowrap;
  }

  /* 데모 안내 배너 */
  .demo-banner {
    margin: 12px 0 4px; padding: 10px 14px; border-radius: 12px; font-size: 12.8px;
    color: #7A4A05; background: #FFF6E3; border: 1px solid #F3D79A; font-weight: 700;
  }

  /* 섹션 제목 */
  .sec-title { font-size: 16px; font-weight: 800; color: #17233B; margin: 6px 0 2px; }
  .sec-sub { font-size: 12.5px; color: #5B6B84; margin: 0 0 10px; }

  /* 카드 공통 */
  .card-title { font-size: 15.5px; font-weight: 800; color: #17233B; margin: 0 0 2px; }
  .card-tag { font-size: 11.5px; font-weight: 700; color: #12A3B4; margin: 0 0 8px; }
  .card-desc { font-size: 12.8px; color: #4A5A72; line-height: 1.55; margin: 0; }
  .chip {
    display: inline-block; font-size: 11px; font-weight: 700; border-radius: 999px;
    padding: 3px 9px; margin: 2px 4px 2px 0; white-space: nowrap;
  }
  .chip-teal { color: #0B7181; background: #E4F6F8; border: 1px solid #BEE7EC; }
  .chip-navy { color: #1E3557; background: #EAF0F8; border: 1px solid #CBD9EA; }
  .chip-amber { color: #8A5A05; background: #FFF4DC; border: 1px solid #F0D9A6; }
  .chip-red { color: #9B2C2C; background: #FDECEC; border: 1px solid #F3C4C4; }
  .chip-grey { color: #4A5A72; background: #F1F4F9; border: 1px solid #DCE3EC; }

  /* 5단계 로드맵 */
  .step-card {
    background: #FFFFFF; border: 1px solid #E2E9F2; border-radius: 14px;
    padding: 13px 14px; height: 100%;
  }
  .step-no {
    display: inline-flex; align-items: center; justify-content: center;
    width: 24px; height: 24px; border-radius: 8px; font-size: 12px; font-weight: 800;
    color: #FFFFFF; background: linear-gradient(135deg, #17233B, #12A3B4); margin-bottom: 8px;
  }
  .step-name { font-size: 13.5px; font-weight: 800; color: #17233B; }
  .step-app { font-size: 11px; font-weight: 700; color: #12A3B4; margin: 1px 0 5px; }
  .step-desc { font-size: 11.5px; color: #5B6B84; line-height: 1.5; }

  /* KPI 카드 */
  .kpi {
    background: #FFFFFF; border: 1px solid #E2E9F2; border-radius: 14px; padding: 13px 15px;
  }
  .kpi-label { font-size: 11.5px; font-weight: 700; color: #5B6B84; }
  .kpi-value { font-size: 24px; font-weight: 800; color: #17233B; line-height: 1.25; }
  .kpi-delta-up { font-size: 11.5px; font-weight: 700; color: #0E8A6B; }
  .kpi-delta-down { font-size: 11.5px; font-weight: 700; color: #C0392B; }
  .kpi-note { font-size: 11px; color: #7A8798; }

  /* 근거 문장 */
  .quote {
    background: #F7FAFC; border-left: 4px solid #12A3B4; border-radius: 10px;
    padding: 11px 13px; font-size: 13px; color: #23324A; line-height: 1.6;
  }
  .quote .q-sub { display: block; font-size: 11px; color: #12A3B4; font-weight: 800; margin-bottom: 4px; }

  /* 질문 카드 */
  .q-stage {
    display: inline-block; font-size: 11px; font-weight: 800; border-radius: 8px;
    padding: 2px 8px; margin-bottom: 6px;
  }
  .q-stage-1 { color: #0B7181; background: #E4F6F8; }
  .q-stage-2 { color: #1E3557; background: #E7EEF9; }
  .q-stage-3 { color: #8A3A05; background: #FFF1E2; }
  .q-text { font-size: 14px; font-weight: 700; color: #17233B; line-height: 1.55; }
  .q-point { font-size: 11.5px; color: #5B6B84; margin-top: 4px; }

  .student-box {
    background: linear-gradient(135deg, #F3F8FC, #EAF4F7);
    border: 1px solid #D8E7EF; border-radius: 14px; padding: 13px 16px;
  }
  .student-name { font-size: 16.5px; font-weight: 800; color: #17233B; margin: 0; }
  .student-meta { font-size: 12px; color: #4A5A72; margin: 3px 0 0; }
  .student-sum { font-size: 12.5px; color: #33445C; line-height: 1.6; margin: 8px 0 0; }

  .adm { border: 1px solid #E2E9F2; border-radius: 12px; padding: 10px 12px;
         margin-bottom: 8px; background: #FFFFFF; }
  .adm-head { display: flex; justify-content: space-between; font-size: 12.5px;
              font-weight: 800; color: #17233B; }
  .adm-head span:last-child { color: #12A3B4; }
  .adm-bar { height: 6px; background: #EEF3F9; border-radius: 999px; overflow: hidden; margin: 7px 0; }
  .adm-bar i { display: block; height: 100%; border-radius: 999px;
               background: linear-gradient(90deg, #12A3B4, #17233B); }
  .adm-note { font-size: 11.5px; color: #5B6B84; line-height: 1.5; }

  .footer {
    margin-top: 26px; padding-top: 12px; border-top: 1px solid #E2E9F2;
    font-size: 11.5px; color: #7A8798; line-height: 1.7;
  }
  .note-line { font-size: 12px; color: #5B6B84; line-height: 1.65; }

  div[data-testid="stMetricValue"] { font-size: 22px; }
  section[data-testid="stSidebar"] { background: #F7F9FC; border-right: 1px solid #E4EAF2; }
  .stMarkdown ol li, .stMarkdown ul li { margin-bottom: 2px; line-height: 1.75; }
  .stMarkdown ol, .stMarkdown ul { padding-left: 1.1rem; }
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------------------
# 네비게이션 도우미
# ---------------------------------------------------------------------------
def goto(page: str) -> None:
    """카드 버튼에서 다른 화면으로 이동한다."""
    st.session_state["_goto"] = page


def _apply_goto() -> None:
    if "_goto" in st.session_state:
        target = st.session_state.pop("_goto")
        if target in PAGES:
            st.session_state["page"] = target


if "page" not in st.session_state:
    st.session_state["page"] = PAGES[0]
_apply_goto()

# 블로그·문자로 특정 체험판을 바로 열 수 있는 딥링크: ?p=career / learning / susi / interview / ranking
PAGE_SLUGS = {
    "home": PAGES[0],
    "career": PAGES[1],
    "learning": PAGES[2],
    "susi": PAGES[3],
    "interview": PAGES[4],
    "ranking": PAGES[5],
}
if not st.session_state.get("_deep_link_applied"):
    st.session_state["_deep_link_applied"] = True
    _slug = st.query_params.get("p")
    if _slug in PAGE_SLUGS:
        st.session_state["page"] = PAGE_SLUGS[_slug]


# ---------------------------------------------------------------------------
# 공통 UI 조각
# ---------------------------------------------------------------------------
def hero() -> None:
    tags = "".join(f"<span>{s['no']} {s['title']}</span>" for s in D.ROADMAP)
    st.markdown(
        f"""
        <div class="hub-hero">
          <div class="hub-badge">INSIGHT NAVI · CHOICE 1000</div>
          <h1>{D.BRAND_TITLE}</h1>
          <div class="hub-sub">{D.BRAND_SUB}</div>
          <div class="hub-tags">{tags}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="demo-banner">🔔 {D.BANNER}</div>', unsafe_allow_html=True)


def section(title: str, sub: str = "") -> None:
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)
    if sub:
        st.markdown(f'<div class="sec-sub">{sub}</div>', unsafe_allow_html=True)


def kpi_card(label: str, value: str, delta: str = "", up: bool = True, note: str = "") -> str:
    cls = "kpi-delta-up" if up else "kpi-delta-down"
    arrow = "▲" if up else "▼"
    delta_html = f'<div class="{cls}">{arrow} {delta}</div>' if delta else ""
    note_html = f'<div class="kpi-note">{note}</div>' if note else ""
    return (
        f'<div class="kpi"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div>{delta_html}{note_html}</div>'
    )


def student_selector(prefix: str) -> dict:
    labels = D.student_labels()
    picked = st.radio(
        "샘플 학생 선택",
        labels,
        index=0,
        horizontal=True,
        key=f"{prefix}_student",
        help="가명(창작) 학생입니다. 실제 학생 정보는 쓰지 않습니다.",
    )
    student = D.student_by_label(picked)
    st.markdown(
        f"""
        <div class="student-box">
          <p class="student-name">{student['name']} <span class="chip chip-teal">{student['grade']}</span>
             <span class="chip chip-navy">{student['track']}</span></p>
          <p class="student-meta">{student['interest']} · {student['record']}</p>
          <p class="student-sum">{student['summary']}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    return student


def footer() -> None:
    st.markdown(
        f"""
        <div class="footer">
          천명의선택 입시전문연구소 · 인사이트 나비(NAVI) 통합 컨설팅 솔루션<br>
          이 화면은 체험용 데모입니다. {D.FICTIONAL_NOTICE}<br>
          상담·도입 문의: <a href="{D.BLOG_URL}" target="_blank">천명의선택 블로그</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# 🏠 통합 대문
# ---------------------------------------------------------------------------
def page_home() -> None:
    section(
        "5단계 입시 컨설팅 로드맵",
        "진로에서 정시까지 한 줄로 이어지는 흐름입니다. 지금 단계의 카드를 눌러 바로 체험해 보세요.",
    )
    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    cols = st.columns(5, gap="small")
    for col, step in zip(cols, D.ROADMAP):
        with col:
            st.markdown(
                f"""
                <div class="step-card">
                  <div class="step-no">{step['no']}</div>
                  <div class="step-name">{step['title']}</div>
                  <div class="step-app">{step['app']}</div>
                  <div class="step-desc">{step['desc']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    section("앱 바로가기", "체험판 4종은 로그인 없이 누르면 바로 동작하고, 5단계 내 위치 NAVI는 실사용 앱으로 열립니다.")

    row1 = st.columns(3, gap="medium")
    row2 = st.columns(2, gap="medium")
    slots = [(row1[0], D.APP_CARDS[0]), (row1[1], D.APP_CARDS[1]), (row1[2], D.APP_CARDS[2]),
             (row2[0], D.APP_CARDS[3]), (row2[1], D.APP_CARDS[4])]
    for col, card in slots:
        with col:
            with st.container(border=True):
                chip_cls = "chip-teal" if card["status"] == "체험판" else "chip-amber"
                st.markdown(
                    f"""
                    <div class="card-tag">{card['tag']}</div>
                    <div class="card-title">{card['icon']} {card['name']}
                      <span class="chip {chip_cls}">{card['status']}</span></div>
                    <p class="card-desc">{card['desc']}</p>
                    """,
                    unsafe_allow_html=True,
                )
                st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
                if card["name"] == "내 위치 NAVI":
                    st.link_button(
                        "🚀 내 위치 NAVI 바로 실행",
                        D.MYRANKING_URL,
                        width="stretch",
                        type="primary",
                    )
                st.button(
                    card["cta"] + " →",
                    key=f"home_btn_{card['name']}",
                    width="stretch",
                    on_click=goto,
                    args=(card["page"],),
                )

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(
            '<div class="card-title">💬 상담·도입 문의</div>'
            '<p class="card-desc">학원·학교·지자체 단위 도입, 학생 개별 컨설팅 문의는 '
            '천명의선택 블로그로 연락 주십시오. 28년 입시 현장 경력의 진단 기준을 그대로 쓰고 있습니다.</p>',
            unsafe_allow_html=True,
        )
        st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
        st.link_button("천명의선택 블로그 열기 (상담 문의)", D.BLOG_URL, width="content")

    with st.expander("🔒 원장님 실전용(암호) — 실사용 앱 4종 바로가기"):
        st.markdown(
            '<p class="note-line">아래 앱은 실제 학생 데이터를 다루므로 각 앱의 접속 암호가 필요합니다. '
            '이 대문의 체험판은 암호 없이 열리지만 <b>실제 데이터·저장 기능은 없습니다.</b></p>',
            unsafe_allow_html=True,
        )
        pcols = st.columns(2, gap="small")
        for i, (name, url, desc) in enumerate(D.PRIVATE_APPS):
            with pcols[i % 2]:
                st.link_button(f"🔐 {name}", url, width="stretch")
                st.caption(f"{desc} · {url}")

    st.markdown(
        '<p class="note-line" style="margin-top:14px">'
        '· 체험판 수치는 설명을 위한 예시이고, 2027 등급컷만 기관 발표 자료를 옮겨 적었습니다.<br>'
        '· 입력한 값은 서버·DB에 저장되지 않습니다(저장 기능 자체가 없음).</p>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# 🧭 진로NAVI 체험
# ---------------------------------------------------------------------------
def page_career() -> None:
    section("🧭 진로NAVI 체험", "계열 적합도 → 추천 학과 → 도서·탐구 주제까지 한 번에 확인합니다.")
    student = student_selector("career")
    data = D.CAREER[student["id"]]

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.05, 1], gap="large")

    with left:
        section("목표 계열 적합도", f"세특·이수 교과·활동을 계열 기준으로 대조한 결과입니다. 최종 목표: {data['target_track']}")
        for item in data["track_fit"]:
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;font-size:12.5px;'
                f'font-weight:700;color:#17233B;margin:6px 0 2px">'
                f'<span>{item["track"]}</span><span>{item["score"]}점</span></div>',
                unsafe_allow_html=True,
            )
            st.progress(item["score"] / 100)
            st.caption(item["reason"])

        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
        section("권장 선택과목", "이수 여부가 세특 평가의 출발점이 됩니다.")
        chips = "".join(f'<span class="chip chip-teal">{c}</span>' for c in data["recommended_courses"]["core"])
        chips += "".join(f'<span class="chip chip-grey">{c}</span>' for c in data["recommended_courses"]["related"])
        st.markdown(f"<div>핵심 · {chips}</div>", unsafe_allow_html=True)

    with right:
        section("추천 학과 3개", "적합도 순입니다. '왜'를 함께 읽으면 세특 연결 문장을 바로 만들 수 있습니다.")
        for m in data["majors"]:
            with st.container(border=True):
                st.markdown(
                    f'<div class="card-title">{m["name"]} <span class="chip chip-navy">적합도 {m["fit"]}%</span></div>'
                    f'<p class="card-desc">{m["why"]}<br><b>이수 권장</b> · {m["courses"]}</p>',
                    unsafe_allow_html=True,
                )

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    section("추천 도서 · 세특 연계 질문", "책을 읽고 끝내지 않고, 세특·탐구 질문으로 넘기는 것이 목적입니다.")
    bcols = st.columns(3, gap="medium")
    for col, book in zip(bcols, data["books"]):
        with col:
            with st.container(border=True):
                chips = "".join(f'<span class="chip chip-amber">{k}</span>' for k in book["keywords"])
                st.markdown(
                    f'<div class="card-title">📖 {book["title"]}</div>'
                    f'<div class="card-tag">{book["author"]}</div>'
                    f'<div>{chips}</div>'
                    f'<p class="card-desc" style="margin-top:8px"><b>탐구 질문</b><br>{book["question"]}</p>'
                    f'<p class="card-desc" style="margin-top:8px;color:#12A3B4"><b>연계</b> · {book["link"]}</p>',
                    unsafe_allow_html=True,
                )

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    with st.expander("🔍 탐구 주제 예시 3개 펼치기"):
        for i, topic in enumerate(data["research_topics"], 1):
            st.markdown(f"**{i}.** {topic}")
        st.caption("탐구 주제는 '측정 가능한 질문'으로 좁히는 것이 핵심입니다. 데이터를 어떤 단위로 모을지까지 정해 두세요.")


# ---------------------------------------------------------------------------
# 📚 학습NAVI 체험
# ---------------------------------------------------------------------------
def page_learning() -> None:
    section("📚 학습NAVI 체험", "교재·회독·진도율을 KPI로 보고, 시험일이 가까운 위험교재를 먼저 잡습니다.")
    student = student_selector("learning")
    plan = D.LEARNING[student["id"]]
    rows = D.learning_rows(student["id"])
    kpi = D.learning_kpis(student["id"])

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="note-line"><b>{plan["exam_name"]}</b> · 시험일 {plan["exam_date"].isoformat()} · '
        f'이번 주 기준일 {D.DEMO_TODAY.isoformat()} ({plan["week_label"]})</p>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4, gap="small")
    with k1:
        st.markdown(kpi_card("주간 평균 완료율", f"{kpi['completion']}%", note="교재별 진도율 평균"),
                    unsafe_allow_html=True)
    with k2:
        st.markdown(
            kpi_card("D-7 위험교재", f"{kpi['danger_count']}종",
                     note=f"전체 {kpi['material_count']}종 중 · 점검일 7일 이내 + 진도 80% 미만"),
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            kpi_card("전주 대비", f"{kpi['delta']:+.1f}p", delta=f"{plan['prev_week_label']} {kpi['prev_completion']}% → "
                     f"{plan['week_label']} {kpi['completion']}%", up=kpi["delta"] >= 0),
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            kpi_card("점검일 임박", f"{min(r['dday'] for r in rows)}일 전",
                     note="가장 가까운 교재 점검일까지"),
            unsafe_allow_html=True,
        )

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)

    st.markdown("##### 교재별 진도 · 회독")
    table = pd.DataFrame(
        [
            {
                "과목": r["subject"],
                "교재": r["title"],
                "회독": r["rounds_text"],
                "진도율": r["progress"],
                "전주": r["prev_progress"],
                "단원": f"{r['units_done']}/{r['units_total']}",
                "점검일": r["dday_text"],
                "상태": r["status"],
            }
            for r in rows
        ]
    )
    st.dataframe(
        table,
        hide_index=True,
        column_config={
            "진도율": st.column_config.ProgressColumn("진도율", min_value=0, max_value=100, format="%d"),
            "전주": st.column_config.NumberColumn("전주 %", format="%d"),
        },
    )

    danger_rows = [r for r in rows if r["danger"]]
    if danger_rows:
        chips = "".join(f'<span class="chip chip-red">🚨 {r["title"]} · {r["dday_text"]} · {r["progress"]}%</span>'
                        for r in danger_rows)
        st.markdown(f'<div style="margin-top:6px">{chips}</div>', unsafe_allow_html=True)
        st.caption("D-7 위험교재: 점검일까지 7일 이내인데 진도율이 80% 미만인 교재입니다.")
    else:
        st.success("D-7 위험교재가 없습니다.")

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    section("과목별 진도 비교", "이번 주와 전주를 겹쳐 보면 '멈춘 교재'가 바로 보입니다.")
    chart_df = pd.DataFrame(
        [
            {"과목": r["subject"], "구분": plan["prev_week_label"], "진도율": r["prev_progress"]} for r in rows
        ]
        + [{"과목": r["subject"], "구분": plan["week_label"], "진도율": r["progress"]} for r in rows]
    )
    chart = (
        alt.Chart(chart_df)
        .mark_bar(cornerRadiusTopLeft=4, cornerRadiusTopRight=4)
        .encode(
            x=alt.X("과목:N", title=None, sort=[r["subject"] for r in rows],
                    axis=alt.Axis(labelAngle=0, labelFontSize=11)),
            xOffset=alt.XOffset("구분:N", sort=[plan["prev_week_label"], plan["week_label"]]),
            y=alt.Y("진도율:Q", title="진도율(%)", scale=alt.Scale(domain=[0, 100])),
            color=alt.Color(
                "구분:N",
                scale=alt.Scale(domain=[plan["prev_week_label"], plan["week_label"]], range=["#CBD9EA", TEAL]),
                legend=alt.Legend(title=None, orient="top"),
            ),
            tooltip=["과목", "구분", "진도율"],
        )
        .properties(height=280)
    )
    st.altair_chart(chart, width="stretch")

    with st.container(border=True):
        st.markdown(
            f'<div class="card-title">🧑‍🏫 컨설턴트 코멘트</div>'
            f'<p class="card-desc">{plan["consult_note"]}</p>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# 📋 수시NAVI 체험
# ---------------------------------------------------------------------------
def page_susi() -> None:
    section("📋 수시NAVI 체험", "학생부를 학업·진로·공동체 역량으로 나눠 점수화하고, 세특 코칭을 붙입니다.")
    student = student_selector("susi")
    data = D.SUSI[student["id"]]
    scores = data["scores"]
    prev = data["prev_scores"]

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    cols = st.columns(3, gap="small")
    for col, (name, score) in zip(cols, scores.items()):
        diff = score - prev[name]
        with col:
            st.markdown(
                kpi_card(f"{name}", f"{score}점 / 100", delta=f"전월 대비 {diff:+.0f}p", up=diff >= 0),
                unsafe_allow_html=True,
            )
            st.progress(score / 100)

    total = round(sum(scores.values()) / len(scores))
    prev_total = round(sum(prev.values()) / len(prev))
    st.markdown(
        f'<p class="note-line" style="margin-top:8px">종합 지수 <b>{total}점</b> · '
        f'전월 {prev_total}점 대비 <b>{total - prev_total:+d}p</b> · '
        f'3개 역량 단순 평균이며 실제 전형 반영비율과는 다릅니다.</p>',
        unsafe_allow_html=True,
    )

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.15, 1], gap="large")

    with left:
        section("역량 시각화", "항목별 배점 합계가 위 점수와 같습니다.")
        chart_df = pd.DataFrame(
            [{"역량": k, "점수": v, "구분": "이번 달"} for k, v in scores.items()]
            + [{"역량": k, "점수": v, "구분": "전월"} for k, v in prev.items()]
        )
        order = list(scores.keys())
        base = alt.Chart(chart_df).encode(
            y=alt.Y("역량:N", sort=order, title=None, axis=alt.Axis(labelFontSize=12)),
        )
        prev_bars = (
            base.transform_filter(alt.datum.구분 == "전월")
            .mark_bar(size=26, cornerRadiusTopRight=4, color="#DCE6F1")
            .encode(
                x=alt.X("점수:Q", scale=alt.Scale(domain=[0, 100]), title="점수(100점)"),
                tooltip=["역량", "구분", "점수"],
            )
        )
        now_bars = (
            base.transform_filter(alt.datum.구분 == "이번 달")
            .mark_bar(size=11, cornerRadiusTopRight=4, color=NAVY)
            .encode(x="점수:Q", tooltip=["역량", "구분", "점수"])
        )
        st.altair_chart((prev_bars + now_bars).properties(height=200), width="stretch")
        st.caption("굵은 연회색 = 전월, 가는 진남색 = 이번 달 — 항목별 배점 합계가 위 점수와 같습니다.")

        with st.expander("항목별 배점 자세히 보기"):
            for comp, items in data["detail"].items():
                st.markdown(f"**{comp}** · {scores[comp]}/100")
                st.dataframe(
                    pd.DataFrame(items, columns=["평가 항목", "획득", "배점"]),
                    width="stretch",
                    hide_index=True,
                )
                st.caption(f"합계 {sum(i[1] for i in items)}/{sum(i[2] for i in items)}")

        st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
        section("지원 가능 전형 요약", "현재 학생부 기준의 상대 평가입니다.")
        for a in data["admissions"]:
            st.markdown(
                f'<div class="adm"><div class="adm-head"><span>{a["type"]}</span>'
                f'<span>적합도 {a["fit"]}</span></div>'
                f'<div class="adm-bar"><i style="width:{a["fit"]}%"></i></div>'
                f'<div class="adm-note">{a["note"]}</div></div>',
                unsafe_allow_html=True,
            )
        st.caption("대학·전형별 실제 반영 방식과 다를 수 있습니다.")

    with right:
        section("세특 강점 3", "그대로 자소서·면접 답변의 재료가 됩니다.")
        for s in data["strengths"]:
            st.markdown(
                f'<div class="quote"><span class="q-sub">강점</span><b>{s["title"]}</b><br>{s["evidence"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
        section("보완 코칭 3", "지금 남은 기간에 실제로 바꿀 수 있는 것만 담았습니다.")
        for s in data["improvements"]:
            st.markdown(
                f'<div class="quote" style="border-left-color:{AMBER}">'
                f'<span class="q-sub" style="color:{AMBER}">보완</span><b>{s["title"]}</b><br>{s["how"]}</div>',
                unsafe_allow_html=True,
            )
            st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)




# ---------------------------------------------------------------------------
# 🎤 면접NAVI PRO 체험
# ---------------------------------------------------------------------------
def page_interview() -> None:
    section("🎤 면접NAVI PRO 체험", "생활기록부 세특 문장에서 근거를 뽑고, 3단계 질문으로 진위를 확인합니다.")
    student = student_selector("interview")
    data = D.INTERVIEW[student["id"]]

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    section("추출된 세특 근거 문장", "질문은 이 문장들에서만 만들어집니다. 없는 활동은 질문하지 않습니다.")
    ecols = st.columns(3, gap="medium")
    for col, ev in zip(ecols, data["evidence"]):
        with col:
            st.markdown(
                f'<div class="quote"><span class="q-sub">{ev["subject"]} · {ev["tag"]}</span>'
                f'{ev["quote"]}</div>',
                unsafe_allow_html=True,
            )

    st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
    stage_meta = {1: ("1단계 · 기본", "q-stage-1", "기록을 본인이 썼는지 확인합니다."),
                  2: ("2단계 · 심화", "q-stage-2", "전공 지식으로 확장해 사고의 깊이를 봅니다."),
                  3: ("3단계 · 진실성 검증", "q-stage-3", "구체적 수치·역할로 실제 수행을 확인합니다.")}
    for stage in (1, 2, 3):
        label, cls, desc = stage_meta[stage]
        section(f"{label}", desc)
        qs = [q for q in data["questions"] if q["stage"] == stage]
        for i, q in enumerate(qs):
            key_base = f"iv_{student['id']}_{stage}_{i}"
            with st.container(border=True):
                st.markdown(
                    f'<div class="q-stage {cls}">{label}</div>'
                    f'<div class="q-text">Q. {q["q"]}</div>'
                    f'<div class="q-point">평가 포인트 · {q["point"]}</div>',
                    unsafe_allow_html=True,
                )
                show = st.toggle("답변 체크포인트 보기", key=f"{key_base}_toggle")
                if show:
                    for j, cp in enumerate(q["checkpoints"]):
                        st.checkbox(cp, key=f"{key_base}_cp{j}")
        st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)

    with st.container(border=True):
        st.markdown(
            '<div class="card-title">📝 면접 준비 메모</div>'
            '<p class="card-desc">답변이  막히면 대개 <b>수치·역할·이유</b>가 비어 있기 때문입니다. '
            '각 질문마다 숫자 하나와 내가 한 일 하나를 미리 정해 두세요. '
            '체크포인트는 이 화면 안에서만 표시되고 저장되지 않습니다.</p>',
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------------------------
# 📊 내 위치 NAVI
# ---------------------------------------------------------------------------
def page_ranking() -> None:
    section("📊 내 위치 NAVI", "모의고사 성적을 전국 모집단위에 그대로 놓아 보는 정시 위치 진단입니다.")
    meta = D.RANKING_META

    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4, gap="small")
    with c1:
        st.markdown(kpi_card("반영 모집단위", f"{meta['units']:,}개", note="2027 지원참고표 기준"),
                    unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("등급컷 과목", f"{meta['subjects']}개", note="국·수 선택과목 + 탐구 17과목"),
                    unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("등급컷 기준일", meta["as_of"], note="2027 가채점 추정"),
                    unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card("판정 구간", "4단계", note="안정 · 적정 · 소신 · 도전"),
                    unsafe_allow_html=True)

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.link_button("🚀 내 위치 NAVI 바로 실행 (실사용 · 암호 없음)", D.MYRANKING_URL,
                   type="primary", width="content")
    st.caption(f"{D.MYRANKING_URL} — 성적을 입력하면 전국 위치·예상 석차·지원권을 계산합니다. 입력값은 저장되지 않습니다.")

    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    left, right = st.columns([1.15, 1], gap="large")

    with left:
        section("2027학년도 가채점 등급컷(원점수)", f"{meta['source']}")
        cuts = pd.DataFrame(D.GRADE_CUTS).rename(
            columns={"group": "영역", "select": "선택과목", "g1": "1등급", "g2": "2등급",
                     "g3": "3등급", "std1": "표준점수(1등급)"}
        )
        st.dataframe(cuts, hide_index=True)
        st.caption(f"백분위 · {D.GRADE_CUT_PERCENTILE} / {meta['note']}")

    with right:
        section("모집단위별 반영비율(예시 4건)", "같은 점수라도 대학이 정한 가중치에 따라 위치가 달라집니다.")
        ratios = pd.DataFrame(D.RATIO_EXAMPLES).rename(
            columns={"university": "대학", "major": "모집단위", "kor": "국어%", "math": "수학%",
                     "eng": "영어%", "inq": "탐구%", "hist": "한국사%",
                     "inq_count": "탐구 과목수", "combo": "응시 조합"}
        )
        st.dataframe(ratios, hide_index=True)

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown('<div class="card-title">계산 방식</div>', unsafe_allow_html=True)
        for i, step in enumerate(D.RANKING_STEPS, 1):
            st.markdown(f"{i}. {step}")
        chips = "".join(
            f'<span class="chip {"chip-teal" if t == "안정" else "chip-navy" if t == "적정" else "chip-amber" if t == "소신" else "chip-red"}">'
            f'{t} · {cond}</span>'
            for t, cond in meta["tiers"]
        )
        st.markdown(f'<div style="margin-top:6px">{chips}</div>', unsafe_allow_html=True)
        st.caption("판정은 백분위 평균 차이(+표준점수 합 차이 30% 혼합)를 기준으로 계산합니다.")

    st.markdown(
        '<p class="note-line" style="margin-top:10px">'
        '이 화면은 소개용입니다. 실제 계산·리포트 발급은 위의 <b>내 위치 NAVI</b> 앱에서 하십시오. '
        '2027학년도 값은 가채점 등급컷으로 만든 추정치입니다.</p>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# 라우터
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div style="font-size:13px;font-weight:800;color:#17233B;letter-spacing:-.01em">'
        '인사이트 나비(NAVI)<br><span style="font-size:11px;color:#5B6B84;font-weight:700">'
        '천명의선택 입시전문연구소</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div style="height:6px"></div>', unsafe_allow_html=True)
    nav = st.radio("화면 이동", PAGES, key="page", label_visibility="collapsed")
    st.markdown('<div style="height:8px"></div>', unsafe_allow_html=True)
    st.link_button("📊 내 위치 NAVI", D.MYRANKING_URL, width="stretch")
    st.link_button("✉️ 상담·도입 문의", D.BLOG_URL, width="stretch")
    st.markdown(
        '<p style="font-size:10.5px;color:#7A8798;line-height:1.6;margin-top:10px">'
        '체험판 4종은 가명 학생의 예시 데이터입니다.<br>'
        '입력·저장·외부 전송 없음 · OpenAI/DB 미연결</p>',
        unsafe_allow_html=True,
    )

hero()

if nav == "🏠 통합 대문":
    page_home()
elif nav == "🧭 진로NAVI 체험":
    page_career()
elif nav == "📚 학습NAVI 체험":
    page_learning()
elif nav == "📋 수시NAVI 체험":
    page_susi()
elif nav == "🎤 면접NAVI PRO 체험":
    page_interview()
elif nav == "📊 내 위치 NAVI":
    page_ranking()

footer()
