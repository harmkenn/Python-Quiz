import streamlit as st
import time
import qrcode
import io
import socket

from state import BUZZ_STATE, TEAM_NAMES

st.set_page_config(page_title="Scripture Jeopardy - Teacher", layout="wide")
#v2.9
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
  "Pearl of Great Price": {
    "100": {
      "q": "This verse teaches that God’s work and glory is to bring to pass the immortality and eternal life of man.",
      "a": "Moses 1:39"
    },
    "200": {
      "q": "This scripture describes Zion as a people of 'one heart and one mind.'",
      "a": "Moses 7:18"
    },
    "300": {
      "q": "These verses contain the Lord’s promise that Abraham’s seed would 'bear this ministry and Priesthood unto all nations.'",
      "a": "Abraham 2:9–11"
    },
    "400": {
      "q": "These verses teach that spirits 'were organized before the world was.'",
      "a": "Abraham 3:22–23"
    },
    "500": {
      "q": "This Article of Faith declares belief in God the Eternal Father, His Son Jesus Christ, and the Holy Ghost.",
      "a": "Article of Faith 1"
    }
  },

  "Old Testament": {
    "100": {
      "q": "This scripture teaches that God created man in His own image.",
      "a": "Genesis 1:26–27"
    },
    "200": {
      "q": "This verse teaches that a man shall 'cleave unto his wife: and they shall be one.'",
      "a": "Genesis 2:24"
    },
    "300": {
      "q": "Joseph asks, 'How then can I do this great wickedness, and sin against God?' in this verse.",
      "a": "Genesis 39:9"
    },
    "400": {
      "q": "This passage contains the Ten Commandments.",
      "a": "Exodus 20:3–17"
    },
    "500": {
      "q": "This verse includes the declaration, 'Choose you this day whom ye will serve.'",
      "a": "Joshua 24:15"
    }
  },

  "Wisdom & Prophets": {
    "100": {
      "q": "These verses teach that those with clean hands and a pure heart may stand in the Lord’s holy place.",
      "a": "Psalm 24:3–4"
    },
    "200": {
      "q": "This scripture teaches us to trust in the Lord with all our heart and promises He will direct our paths.",
      "a": "Proverbs 3:5–6"
    },
    "300": {
      "q": "This verse teaches that though sins be as scarlet, they can become white as snow.",
      "a": "Isaiah 1:18"
    },
    "400": {
      "q": "This Article of Faith teaches that men will be punished for their own sins, not for Adam’s transgression.",
      "a": "Article of Faith 2"
    },
    "500": {
      "q": "This Article of Faith teaches that all mankind may be saved through the Atonement of Christ by obedience to the laws and ordinances of the gospel.",
      "a": "Article of Faith 3"
    }
  },

  "Gospel Principles": {
    "100": {
      "q": "This Article of Faith lists the first principles and ordinances of the gospel: faith, repentance, baptism, and the gift of the Holy Ghost.",
      "a": "Article of Faith 4"
    },
    "200": {
      "q": "This Article of Faith teaches that a man must be called of God by prophecy and by the laying on of hands to preach the gospel.",
      "a": "Article of Faith 5"
    },
    "300": {
      "q": "This Article of Faith affirms belief in the same organization that existed in the Primitive Church, including apostles and prophets.",
      "a": "Article of Faith 6"
    },
    "400": {
      "q": "This Article of Faith declares belief in spiritual gifts such as tongues, prophecy, revelation, visions, and healing.",
      "a": "Article of Faith 7"
    },
    "500": {
      "q": "This Article of Faith states belief in the Bible as far as it is translated correctly and also in the Book of Mormon as the word of God.",
      "a": "Article of Faith 8"
    }
  },

  "Restoration & Latter-day Beliefs": {
    "100": {
      "q": "This Article of Faith teaches that God has revealed, does now reveal, and will yet reveal many great and important things.",
      "a": "Article of Faith 9"
    },
    "200": {
      "q": "This Article of Faith teaches about the literal gathering of Israel, the restoration of the Ten Tribes, and the building of Zion on the American continent.",
      "a": "Article of Faith 10"
    },
    "300": {
      "q": "This Article of Faith claims the privilege of worshiping God according to the dictates of one’s own conscience and allowing all men the same privilege.",
      "a": "Article of Faith 11"
    },
    "400": {
      "q": "This Article of Faith teaches obedience, honor, and sustaining the law, including being subject to rulers and magistrates.",
      "a": "Article of Faith 12"
    },
    "500": {
      "q": "This Article of Faith teaches that we seek after anything virtuous, lovely, of good report, or praiseworthy.",
      "a": "Article of Faith 13"
    }
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
        name = TEAM_NAMES[i]
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

# ---------------------------------------------------------
# SIDEBAR: QR CODE + SCORES
# ---------------------------------------------------------
st.sidebar.header("Team Scores")

for i in range(4):
    st.sidebar.write(f"{TEAM_NAMES[i]}: {st.session_state.team_scores[i]}")

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

# NEW: Refresh button
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

    # Smooth timer container
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

    # Live countdown loop
    if st.session_state.timer_running:
        for _ in range(200):  # enough iterations for 20 seconds
            render_timer()
            time.sleep(0.2)
            if get_time_left() == 0:
                st.session_state.timer_running = False
                break
    else:
        render_timer()

    # ---------------------------------------------------------
    # AUTO-HIGHLIGHT TEAM THAT BUZZED FIRST
    # ---------------------------------------------------------
    first_buzz = BUZZ_STATE.get()
    if first_buzz:
        buzz_name = first_buzz["team"]

        # Find which team slot matches this name
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
