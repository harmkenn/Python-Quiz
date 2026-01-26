import streamlit as st
import time
import qrcode
import io
import socket

from state import BUZZ_STATE

st.set_page_config(page_title="Scripture Jeopardy - Teacher", layout="wide")
#v2.1
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
# JEOPARDY QUESTIONS
# ---------------------------------------------------------
categories = {
    "Old Testament": {
        100: {"q": "This man built an ark to save his family and animals from the flood.", "a": "Who is Noah?"},
        200: {"q": "This prophet parted the Red Sea to help the Israelites escape Egypt.", "a": "Who is Moses?"},
        300: {"q": "This young shepherd boy defeated the giant Goliath with a sling and stone.", "a": "Who is David?"},
        400: {"q": "This prophet was taken up to heaven in a whirlwind without dying.", "a": "Who is Elijah?"},
        500: {"q": "This book contains the Ten Commandments given to Moses.", "a": "What is Exodus?"}
    },
    "New Testament": {
        100: {"q": "This is where Jesus was born.", "a": "What is Bethlehem?"},
        200: {"q": "This apostle denied knowing Jesus three times before the crucifixion.", "a": "Who is Peter?"},
        300: {"q": "This is the number of apostles Jesus originally called.", "a": "What is twelve?"},
        400: {"q": "This apostle was known as 'doubting' because he needed to see Jesus's wounds.", "a": "Who is Thomas?"},
        500: {"q": "This is the mountain where Jesus gave the Sermon on the Mount.", "a": "What is the Mount of Beatitudes (or Mount of Olives)?"}
    },
    "Book of Mormon": {
        100: {"q": "This prophet wrote the first book in the Book of Mormon.", "a": "Who is Nephi?"},
        200: {"q": "This is the name of Lehi's rebellious son.", "a": "Who is Laman?"},
        300: {"q": "This prophet buried the golden plates in the Hill Cumorah.", "a": "Who is Moroni?"},
        400: {"q": "This king gave up his throne to serve God and became a great missionary.", "a": "Who is King Mosiah (or Alma)?"},
        500: {"q": "This is the city where Jesus appeared to the Nephites.", "a": "What is Bountiful?"}
    },
    "Doctrine & Covenants": {
        100: {"q": "This section contains the Word of Wisdom.", "a": "What is Section 89?"},
        200: {"q": "This is the age when young men can receive the Aaronic Priesthood.", "a": "What is 12?"},
        300: {"q": "This section describes the three degrees of glory.", "a": "What is Section 76?"},
        400: {"q": "This section contains the law of tithing.", "a": "What is Section 119?"},
        500: {"q": "This section describes the organization of the First Presidency and Twelve Apostles.", "a": "What is Section 107?"}
    },
    "Church History": {
        100: {"q": "This is the year the Church was organized.", "a": "What is 1830?"},
        200: {"q": "This is where Joseph Smith received the First Vision.", "a": "What is the Sacred Grove?"},
        300: {"q": "This angel appeared to Joseph Smith to tell him about the golden plates.", "a": "Who is Moroni?"},
        400: {"q": "This is the first temple built in this dispensation.", "a": "What is the Kirtland Temple?"},
        500: {"q": "This prophet led the saints to Utah after Joseph Smith's death.", "a": "Who is Brigham Young?"}
    },
    "Gospel Principles": {
        100: {"q": "This is the first principle of the gospel.", "a": "What is faith?"},
        200: {"q": "This ordinance is required for entrance into the celestial kingdom.", "a": "What is baptism?"},
        300: {"q": "This is the gift received after baptism and confirmation.", "a": "What is the gift of the Holy Ghost?"},
        400: {"q": "This principle allows us to be forgiven of our sins.", "a": "What is repentance?"},
        500: {"q": "This is the highest degree of glory in the celestial kingdom.", "a": "What is exaltation?"}
    }
}

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
# TIMER HELPERS
# ---------------------------------------------------------
TIMER_DURATION = 20

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
        is_current = (i == st.session_state.current_team)

        if is_current:
            # ACTIVE TEAM — filled button
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
            # NON-ACTIVE TEAM — outline only
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
            if st.button(f"Team {i+1}", key=f"team-btn-{i}"):
                st.session_state.current_team = i
                st.rerun()

            st.markdown(f"<div style='{style}'>Team {i+1}</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# SIDEBAR: QR CODE + SCORES
# ---------------------------------------------------------
st.sidebar.header("Team Scores")

for i in range(4):
    st.sidebar.write(f"Team {i+1}: {st.session_state.team_scores[i]}")

st.sidebar.markdown("---")
st.sidebar.subheader("Buzzer Link")

qr = qrcode.QRCode(box_size=4, border=2)
qr.add_data(BUZZER_URL)
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
buf = io.BytesIO()
img.save(buf, format="PNG")
st.sidebar.image(buf.getvalue(), use_column_width=True)

st.sidebar.code(BUZZER_URL, language="text")

# ---------------------------------------------------------
# MAIN UI
# ---------------------------------------------------------
st.title("📘 Scripture Jeopardy — Teacher Control")

render_team_buttons()
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
                disabled = (cat, points) in st.session_state.answered_questions
                if st.button(f"${points}", key=f"{cat}-{points}", disabled=disabled):
                    st.session_state.current_question = (cat, points)
                    st.session_state.show_answer = False
                    BUZZ_STATE.clear()
                    start_timer()
                    st.rerun()

# ---------------------------------------------------------
# QUESTION + BUZZER DISPLAY
# ---------------------------------------------------------
if st.session_state.current_question:
    cat, points = st.session_state.current_question
    qdata = categories[cat][points]

    st.markdown(f"## {cat} — ${points}")
    st.markdown(f"### {qdata['q']}")

    # Timer
    time_left = get_time_left()
    color = timer_color(time_left)
    st.markdown(
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

    if time_left == 0 and st.session_state.timer_running:
        stop_timer()

    # Buzzer status
    first_buzz = BUZZ_STATE.get()
    if first_buzz:
        try:
            team_num = int(first_buzz["team"].split()[-1]) - 1
            st.session_state.current_team = team_num
        except:
            pass

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
                🔔 {first_buzz['team']} BUZZED IN FIRST!
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

    if st.session_state.timer_running:
        st.rerun()
