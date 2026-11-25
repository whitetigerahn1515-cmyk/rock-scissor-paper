import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="가위바위보 챌린지",
    page_icon="✊",
    layout="centered",
)

# 커스텀 CSS (고등학생 취향에 맞춘 깔끔하고 생동감 있는 UI)
st.markdown(
    """
    <style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        text-align: center;
        color: #666666;
        font-size: 1.05rem;
        margin-bottom: 2rem;
    }
    .choice-card {
        background-color: #f8f9fa;
        border: 2px solid #e9ecef;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    .choice-label {
        font-size: 1.1rem;
        font-weight: 700;
        color: #495057;
        margin-bottom: 8px;
    }
    .choice-emoji {
        font-size: 4.5rem;
        line-height: 1.2;
    }
    .choice-text {
        font-size: 1.3rem;
        font-weight: 700;
        margin-top: 8px;
        color: #212529;
    }
    div.stButton > button {
        width: 100%;
        height: 75px;
        font-size: 1.3rem;
        font-weight: 700;
        border-radius: 12px;
        border: 2px solid #dee2e6;
        transition: all 0.2s ease;
    }
    div.stButton > button:hover {
        border-color: #4dabf7;
        transform: translateY(-2px);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 세션 상태 초기화 (전적 및 마지막 게임 결과 저장)
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "draws" not in st.session_state:
    st.session_state.draws = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None

# 선택지 데이터 정의
CHOICES = {
    "가위": "✌️",
    "바위": "✊",
    "보": "🖐️",
}


def determine_winner(user_choice: str, comp_choice: str) -> str:
    """승패 판정 함수"""
    if user_choice == comp_choice:
        return "draw"
    elif (
        (user_choice == "가위" and comp_choice == "보")
        or (user_choice == "바위" and comp_choice == "가위")
        or (user_choice == "보" and comp_choice == "바위")
    ):
        return "win"
    else:
        return "lose"


def play_game(user_choice: str):
    """게임 실행 및 상태 업데이트"""
    comp_choice = random.choice(list(CHOICES.keys()))
    outcome = determine_winner(user_choice, comp_choice)

    if outcome == "win":
        st.session_state.wins += 1
        st.session_state.streak += 1
    elif outcome == "lose":
        st.session_state.losses += 1
        st.session_state.streak = 0
    else:
        st.session_state.draws += 1

    st.session_state.last_result = {
        "user": user_choice,
        "comp": comp_choice,
        "outcome": outcome,
    }


# 1) 화면 상단 제목
st.markdown('<div class="main-title">✊ 가위바위보 챌린지</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">컴퓨터와의 짜릿한 한 판 승부! 무엇을 낼지 선택해보세요.</div>',
    unsafe_allow_html=True,
)

# 전적 요약 대시보드
col_w, col_d, col_l, col_s = st.columns(4)
col_w.metric("🏆 승리", f"{st.session_state.wins}회")
col_d.metric("🤝 무승부", f"{st.session_state.draws}회")
col_l.metric("💀 패배", f"{st.session_state.losses}회")
col_s.metric("🔥 현재 연승", f"{st.session_state.streak}연승")

st.divider()

# 2) 사용자 선택 버튼 영역
st.subheader("👇 당신의 선택은?")
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    if st.button("✌️ 가위"):
        play_game("가위")
with btn_col2:
    if st.button("✊ 바위"):
        play_game("바위")
with btn_col3:
    if st.button("🖐️ 보"):
        play_game("보")

st.write("")

# 3~6) 대결 결과 및 이모지 표시 영역
if st.session_state.last_result is not None:
    res = st.session_state.last_result
    user_c = res["user"]
    comp_c = res["comp"]
    outcome = res["outcome"]

    # 사용자 vs 컴퓨터 선택 카드
    c1, c_vs, c2 = st.columns([4, 1, 4])

    with c1:
        st.markdown(
            f"""
            <div class="choice-card">
                <div class="choice-label">🙋‍♂️ 나 (Player)</div>
                <div class="choice-emoji">{CHOICES[user_c]}</div>
                <div class="choice-text">{user_c}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c_vs:
        st.markdown(
            "<div style='text-align:center; font-size:1.8rem; font-weight:900; padding-top:65px; color:#868e96;'>VS</div>",
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="choice-card">
                <div class="choice-label">🤖 컴퓨터 (AI)</div>
                <div class="choice-emoji">{CHOICES[comp_c]}</div>
                <div class="choice-text">{comp_c}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")

    # 승/무/패 결과 배너
    if outcome == "win":
        st.success(f"🎉 **승리했습니다!** ({user_c}가 {comp_c}를 이겼습니다!)")
        if st.session_state.streak >= 3:
            st.toast(f"🔥 대단해요! {st.session_state.streak}연승 달성 중!", icon="🔥")
    elif outcome == "lose":
        st.error(f"😭 **패배했습니다...** ({comp_c}에게 졌습니다. 다시 도전해보세요!)")
    else:
        st.info(f"😐 **무승부입니다!** (둘 다 {user_c}를 냈습니다!)")

else:
    st.info("👆 위에서 **가위, 바위, 보** 버튼 중 하나를 눌러 게임을 시작하세요!")

st.divider()

# 전적 초기화 버튼
_, reset_col, _ = st.columns([3, 2, 3])
with reset_col:
    if st.button("🔄 전적 초기화"):
        st.session_state.wins = 0
        st.session_state.losses = 0
        st.session_state.draws = 0
        st.session_state.streak = 0
        st.session_state.last_result = None
        st.rerun()
