import streamlit as st
import time
import qrcode
import io
import socket
import random
from collections import defaultdict

from state import BUZZ_STATE, TEAM_NAMES
from question_bank import question_bank

if __name__ == "__main__":
    st.set_page_config(page_title="Scripture Jeopardy - Teacher", layout="wide")
# v3.4 — Buttons visible during answering timer

# ---------------------------------------------------------
# AUTO-DETECT LOCAL IP FOR QR CODE
# ---------------------------------------------------------
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP

LOCAL_IP = get_local_ip()
BUZZER_URL = f"http://{LOCAL_IP}:8501/buzzer"

# ---------------------------------------------------------
# TEAM COLORS (4 TEAMS MAX)
# ---------------------------------------------------------
TEAM_COLORS = [
    "#3b82f6",  # Team 1 - Blue
    "#ef4444",  # Team 2 - Red
    "#22c55e",  # Team 3 - Green
    "#a855f7",  # Team 4 - Purple
]

# ---------------------------------------------------------
# DYNAMIC JEOPARDY BOARD (5 random categories x 5 questions each)
# ---------------------------------------------------------

category_map = defaultdict(list)
for q in question_bank:
    category_map[q["category"]].append(q)

def init_board():
    if "selected_categories" not in st.session_state:
        all_categories = list(category_map.keys())
        st.session_state.selected_categories = random.sample(all_categories, 5)

        board = {}
        for cat in st.session_state.selected_categories:
            questions = category_map[cat]

            if len(questions) < 5:
                chosen = random.choices(questions, k=5)
            else:
                chosen = random.sample(questions, 5)

            board[cat] = {}
            for i, q in enumerate(chosen):
                points = str((i + 1) * 100)
                board[cat][points] = {"q": q["q"], "a": q["a"]}

        st.session_state.jeopardy_board = board

    return st.session_state.jeopardy_board

# ---------------------------------------------------------
# TIMER HELPERS
# ---------------------------------------------------------
TIMER_READING = 15
TIMER_ANSWERING = 10
TIMER_DISCUSSION = 30

def get_current_duration():
    mode = st.session_state.get("timer_mode", "reading")
    if mode == "answering":
        return TIMER_ANSWERING
    elif mode == "discussion":
        return TIMER_DISCUSSION
    return TIMER_READING

def start_timer():
    st.session_state.timer_start = time.time()
    st.session_state.timer_running = True

def stop_timer():
    st.session_state.timer_running = False

def get_time_left():
    if not st.session_state.timer_running or st.session_state.timer_start is None:
        return get_current_duration()
    elapsed = time.time() - st.session_state.timer_start
    return max(0, get_current_duration() - int(elapsed))

def timer_color(seconds_left):
    total = get_current_duration()
    if seconds_left > total * 0.6:
        return "#22c55e"
    elif seconds_left > total * 0.3:
        return "#eab308"
    else:
        return "#ef4444"

# ---------------------------------------------------------
# TEAM BUTTONS (TOP OF SCREEN)
# ---------------------------------------------------------
def render_team_buttons():
    cols = st.columns(4)

    for i in range(4):
        color = TEAM_COLORS[i]
        name = TEAM_NAMES[i]
        score = st.session_state.team_scores[i]
        is_current = (i == st.session_state.current_team)

        if is_current:
            style = f"""
                padding: 1rem;
                text-align: center;
                border-radius: 10px;
                font-weight: bold;
                color: white;
                background-color: {color};
                margin: 0.25rem;
                font-size: 1.4rem;
                border: 4px solid white;
                transform: scale(1.05);
            """
        else:
            style = f"""
                padding: 1rem;
                text-align: center;
                border-radius: 10px;
                font-weight: bold;
                color: {color};
                background-color: transparent;
                margin: 0.25rem;
                font-size: 1.4rem;
                border: 3px solid {color};
            """

        with cols[i]:
            if st.button(name, key=f"team-btn-{i}"):
                st.session_state.current_team = i
                st.rerun()

            st.markdown(f"<div style='{style}'>{name}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div style='text-align: center; font-size: 1.2rem; font-weight: bold; color: {color};'>${score}</div>",
                unsafe_allow_html=True
            )

# ---------------------------------------------------------
# SIDEBAR: QR CODE + BUZZER LINK
# ---------------------------------------------------------

def app():
    st.sidebar.subheader("Buzzer Link")

    qr = qrcode.QRCode(box_size=4, border=2)
    qr.add_data(BUZZER_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    st.sidebar.image(buf.getvalue(), width=300)

    st.sidebar.code(BUZZER_URL, language="text")

    # ---------------------------------------------------------
    # SESSION STATE INIT
    # ---------------------------------------------------------
    if "team_scores" not in st.session_state:
        st.session_state.team_scores = {i: 0 for i in range(4)}

    if "current_team" not in st.session_state:
        st.session_state.current_team = 0

    if "current_question" not in st.session_state:
        st.session_state.current_question = None

    if "answered_questions" not in st.session_state:
        st.session_state.answered_questions = set()

    if "show_answer" not in st.session_state:
        st.session_state.show_answer = False

    if "timer_start" not in st.session_state:
        st.session_state.timer_start = None

    if "timer_running" not in st.session_state:
        st.session_state.timer_running = False

    if "timer_mode" not in st.session_state:
        st.session_state.timer_mode = "reading"

    categories = init_board()

    # ---------------------------------------------------------
    # MAIN UI
    # ---------------------------------------------------------
    st.title("📘 Scripture Jeopardy — Teacher Control")

    render_team_buttons()

    if st.button("🔄 Refresh Teams"):
        st.rerun()

    st.markdown("---")

    # ---------------------------------------------------------
    # JEOPARDY BOARD
    # ---------------------------------------------------------
    if st.session_state.current_question is None:
        cols = st.columns(len(categories))

        for idx, (cat, values) in enumerate(categories.items()):
            with cols[idx]:
                st.markdown(f"### {cat}")
                for points, qa in values.items():
                    points_int = int(points)
                    disabled = (cat, points_int) in st.session_state.answered_questions
                    if st.button(f"${points}", key=f"{cat}-{points}", disabled=disabled):
                        st.session_state.current_question = (cat, points_int)
                        st.session_state.show_answer = False
                        st.session_state.timer_mode = "reading"
                        BUZZ_STATE.clear()
                        start_timer()
                        st.rerun()

    # ---------------------------------------------------------
    # QUESTION + BUZZER DISPLAY
    # ---------------------------------------------------------
    if st.session_state.current_question:
        cat, points = st.session_state.current_question
        qdata = categories[cat][str(points)]

        st.markdown(f"## {cat} — ${points}")
        st.markdown(f"### {qdata['q']}")

        # Placeholders rendered first so they appear at the top
        timer_placeholder = st.empty()
        buzz_banner = st.empty()

        def render_timer(time_left=None):
            if time_left is None:
                time_left = get_time_left()
            color = timer_color(time_left)
            timer_placeholder.markdown(
                f"""
                <div style="
                    font-size:5rem;
                    font-weight:800;
                    text-align:center;
                    padding:0.5rem 1rem;
                    border-radius:1rem;
                    margin:1rem auto;
                    background-color:{color};
                    color:white;
                    width:60%;
                ">
                    {time_left}
                </div>
                """,
                unsafe_allow_html=True,
            )

        def render_buzz_banner(buzz_name=None):
            if buzz_name:
                buzz_banner.markdown(
                    f"""
                    <div style="
                        background:#22c55e;
                        color:white;
                        padding:1rem;
                        text-align:center;
                        font-size:2rem;
                        font-weight:700;
                        border-radius:10px;
                        margin-bottom:1rem;
                    ">
                        🔔 {buzz_name} BUZZED IN FIRST!
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                buzz_banner.info("No team has buzzed in yet.")

        # ---------------------------------------------------------
        # CONTROL BUTTONS — rendered BEFORE timer loops so they are
        # always visible while the countdown is running
        # ---------------------------------------------------------
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("▶️ Restart Timer"):
                start_timer()
                st.rerun()

        with col2:
            if st.button("⏹️ Stop Timer"):
                stop_timer()
                st.rerun()

        with col3:
            if st.button("🧹 Clear Buzzers"):
                BUZZ_STATE.clear()
                st.rerun()

        with col4:
            if st.button("👁️ Show Answer"):
                st.session_state.show_answer = True
                st.session_state.timer_running = False
                st.rerun()

        if st.session_state.show_answer:
            st.markdown(f"### ✅ Answer: {qdata['a']}")

            if st.button("⏳ Start Discussion Timer (30s)"):
                st.session_state.timer_mode = "discussion"
                start_timer()
                st.rerun()

            colA, colB, colC = st.columns(3)
            with colA:
                if st.button("✅ Correct"):
                    st.session_state.team_scores[st.session_state.current_team] += points
                    st.session_state.answered_questions.add((cat, points))
                    st.session_state.current_question = None
                    st.session_state.show_answer = False
                    st.rerun()

            with colB:
                if st.button("❌ Wrong"):
                    st.session_state.team_scores[st.session_state.current_team] -= points
                    st.session_state.answered_questions.add((cat, points))
                    st.session_state.current_question = None
                    st.session_state.show_answer = False
                    st.rerun()

            with colC:
                if st.button("➡️ Skip"):
                    st.session_state.answered_questions.add((cat, points))
                    st.session_state.current_question = None
                    st.session_state.show_answer = False
                    st.rerun()

        # ---------------------------------------------------------
        # TIMER LOOPS — run after buttons are already painted
        # ---------------------------------------------------------
        if st.session_state.timer_running:

            # READING MODE: Watch for a buzz, then hand off to answering
            if st.session_state.timer_mode == "reading":
                render_buzz_banner(None)

                while get_time_left() > 0:
                    render_timer()

                    if BUZZ_STATE.get():
                        buzz_name = BUZZ_STATE.get()["team"]

                        for i in range(4):
                            if TEAM_NAMES[i] == buzz_name:
                                st.session_state.current_team = i
                                break

                        render_buzz_banner(buzz_name)

                        current_val = get_time_left()
                        for t in range(current_val, -1, -1):
                            render_timer(t)
                            time.sleep(0.05)

                        st.session_state.timer_mode = "answering"
                        start_timer()
                        st.rerun()
                        break

                    time.sleep(0.1)

                if get_time_left() == 0:
                    st.session_state.timer_running = False
                    render_timer(0)

            # ANSWERING MODE: Team name stays visible above the 10-second countdown
            elif st.session_state.timer_mode == "answering":
                first_buzz = BUZZ_STATE.get()
                if first_buzz:
                    buzz_name = first_buzz["team"]
                    for i in range(4):
                        if TEAM_NAMES[i] == buzz_name:
                            st.session_state.current_team = i
                            break
                    render_buzz_banner(buzz_name)
                else:
                    render_buzz_banner(None)

                while get_time_left() > 0:
                    render_timer()
                    time.sleep(0.1)
                st.session_state.timer_running = False
                render_timer(0)

            # DISCUSSION MODE
            else:
                first_buzz = BUZZ_STATE.get()
                render_buzz_banner(first_buzz["team"] if first_buzz else None)

                while get_time_left() > 0:
                    render_timer()
                    time.sleep(0.1)
                st.session_state.timer_running = False
                render_timer(0)

        else:
            first_buzz = BUZZ_STATE.get()
            render_buzz_banner(first_buzz["team"] if first_buzz else None)
            render_timer()

if __name__ == "__main__":
    app()