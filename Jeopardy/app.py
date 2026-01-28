import streamlit as st
import time
import qrcode
import io
import socket
import random
from collections import defaultdict

from state import BUZZ_STATE, TEAM_NAMES
from question_bank import question_bank

st.set_page_config(page_title="Scripture Jeopardy - Teacher", layout="wide")
# v3.0 — Dynamic Question Bank Edition

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

# ---------------------------------------------------------
# DYNAMIC JEOPARDY BOARD (5 random categories × 5 questions each)
# ---------------------------------------------------------
import random
from collections import defaultdict

# Build a dictionary: category → list of questions
category_map = defaultdict(list)
for q in question_bank:
    category_map[q["category"]].append(q)

# Only run once per game
if "selected_categories" not in st.session_state:
    # 1. Pick 5 random categories
    all_categories = list(category_map.keys())
    st.session_state.selected_categories = random.sample(all_categories, 5)

    # 2. For each category, pick 5 random questions
    board = {}
    for cat in st.session_state.selected_categories:
        questions = category_map[cat]

        # Ensure at least 5 questions exist
        if len(questions) < 5:
            # If a category is too small, randomly repeat questions
            chosen = random.choices(questions, k=5)
        else:
            chosen = random.sample(questions, 5)

        # Assign Jeopardy point values
        board[cat] = {}
        for i, q in enumerate(chosen):
            points = str((i + 1) * 100)
            board[cat][points] = {"q": q["q"], "a": q["a"]}

    st.session_state.jeopardy_board = board

# Use the generated board
categories = st.session_state.jeopardy_board

# ---------------------------------------------------------
# TIMER HELPERS
# ---------------------------------------------------------
TIMER_DURATION = 15

def start_timer():
    st.session_state.timer_start = time.time()
    st.session_state.timer_running = True

def stop_timer():
    st.session_state.timer_running = False

def get_time_left():
    if not st.session_state.timer_running or st.session_state.timer_start is None:
        return TIMER_DURATION
    elapsed = time.time() - st.session_state.timer_start
    return max(0, TIMER_DURATION - int(elapsed))

def timer_color(seconds_left):
    if seconds_left > TIMER_DURATION * 0.6:
        return "#22c55e"
    elif seconds_left > TIMER_DURATION * 0.3:
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

    timer_placeholder = st.empty()

    def render_timer():
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

    if st.session_state.timer_running:
        for _ in range(200):
            render_timer()
            time.sleep(0.2)
            if get_time_left() == 0:
                st.session_state.timer_running = False
                break
    else:
        render_timer()

    first_buzz = BUZZ_STATE.get()
    if first_buzz:
        buzz_name = first_buzz["team"]

        for i in range(4):
            if TEAM_NAMES[i] == buzz_name:
                st.session_state.current_team = i
                break

        st.markdown(
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
        st.info("No team has buzzed in yet.")

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
            st.rerun()

    if st.session_state.show_answer:
        st.markdown(f"### ✅ Answer: {qdata['a']}")

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
