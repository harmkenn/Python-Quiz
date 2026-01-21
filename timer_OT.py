import streamlit as st
import time
import random
import socket
import qrcode
from io import BytesIO

# =========================
# SHARED SCRIPTURE DATA v1.9
# =========================
SCRIPTURES = {
    "Moses 1:39": "This is my work and my glory—to bring to pass the immortality and eternal life of man.",
    "Moses 7:18": "The Lord called his people Zion, because they were of one heart and one mind.",
    "Abraham 2:9–11": "The Lord promised Abraham that his seed would bear this ministry and Priesthood unto all nations.",
    "Abraham 3:22–23": "As spirits we were organized before the world was.",
    "Genesis 1:26–27": "God created man in his own image.",
    "Genesis 2:24": "A man shall cleave unto his wife: and they shall be one.",
    "Genesis 39:9": "How then can I do this great wickedness, and sin against God?",
    "Exodus 20:3–17": "The Ten Commandments.",
    "Joshua 24:15": "Choose you this day whom ye will serve.",
    "Psalm 24:3–4": "Who shall stand in his holy place? He that hath clean hands, and a pure heart.",
    "Proverbs 3:5–6": "Trust in the Lord with all thine heart … and he shall direct thy paths.",
    "Isaiah 1:18": "Though your sins be as scarlet, they shall be as white as snow.",
    "Isaiah 5:20": "Woe unto them that call evil good, and good evil.",
    "Isaiah 29:13–14": "The restoration of the gospel is a marvellous work and a wonder.",
    "Isaiah 53:3–5": "Surely Jesus Christ hath borne our griefs, and carried our sorrows.",
    "Isaiah 58:6–7": "The blessings of a proper fast.",
    "Isaiah 58:13–14": "Turn away from doing thy pleasure on my holy day; and call the sabbath a delight.",
    "Jeremiah 1:4–5": "Before I formed thee in the belly I ordained thee a prophet unto the nations.",
    "Ezekiel 3:16–17": "The prophet is a watchman unto the house of Israel.",
    "Ezekiel 37:15–17": "The Bible and the Book of Mormon shall become one in thine hand.",
    "Daniel 2:44–45": "God shall set up a kingdom, which shall never be destroyed.",
    "Amos 3:7": "The Lord God revealeth his secret unto his servants the prophets.",
    "Malachi 3:8–10": "The blessings of paying tithing.",
    "Malachi 4:5–6": "Elijah shall turn the heart of the children to their fathers.",
}

TEACHER_PIN = "1234"

# =========================
# SHARED GAME STATE
# =========================
@st.cache_resource
def get_game_state():
    return {
        "current_phrase": None,
        "correct_ref": None,
        "options": [],
        "question_start_time": None,
        "answers_open": False,
        "student_scores": {},
        "student_answers": {},
        "question_number": 0,
        "question_history": [],
        "version": 0,  # used to trigger student refresh
    }

# =========================
# PAGE CONFIG & STYLES
# =========================
st.set_page_config(page_title="Scripture Speed Quiz", layout="wide")

st.markdown("""
<style>
.big-text { 
    font-size: 26px; 
    padding: 20px; 
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 10px;
    margin: 10px 0;
    text-align: center;
}
.timer-text { 
    font-size: 48px; 
    font-weight: bold; 
    color: #FF4B4B; 
    text-align: center;
    animation: pulse 1s infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}
.score-card {
    padding: 15px;
    border-radius: 10px;
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    text-align: center;
    font-size: 24px;
    margin: 10px 0;
}
.leaderboard-card {
    padding: 10px;
    margin: 5px 0;
    border-radius: 8px;
    background: #f8f9fa;
    border-left: 5px solid #667eea;
    color: #000;
}
.stButton button:hover {
    transform: scale(1.02);
    transition: transform 0.2s;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HELPER FUNCTIONS
# =========================
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def start_new_question(game_state):
    refs = list(SCRIPTURES.keys())
    recent_refs = [q["ref"] for q in game_state["question_history"][-5:]]
    available_refs = [r for r in refs if r not in recent_refs] or refs

    correct_ref = random.choice(available_refs)
    phrase = SCRIPTURES[correct_ref]

    wrong_refs = [r for r in refs if r != correct_ref]
    wrong_choices = random.sample(wrong_refs, k=min(5, len(wrong_refs)))
    options = wrong_choices + [correct_ref]
    random.shuffle(options)

    game_state["current_phrase"] = phrase
    game_state["correct_ref"] = correct_ref
    game_state["options"] = options
    game_state["question_start_time"] = time.time()
    game_state["answers_open"] = True
    game_state["student_answers"] = {}
    game_state["question_number"] += 1

def compute_points(elapsed):
    return max(0, 10 - int(elapsed // 2))

def record_student_answer(game_state, name, answer_ref):
    if not game_state["answers_open"]:
        return
    if name in game_state["student_answers"]:
        return
    if game_state["question_start_time"] is None:
        return

    elapsed = time.time() - game_state["question_start_time"]
    correct = (answer_ref == game_state["correct_ref"])
    points = compute_points(elapsed) if correct and elapsed <= 20 else 0

    game_state["student_answers"][name] = {
        "answer": answer_ref,
        "elapsed": elapsed,
        "points": points,
        "correct": correct,
    }

    game_state["student_scores"][name] = game_state["student_scores"].get(name, 0) + points

def lock_answers(game_state):
    game_state["answers_open"] = False

def get_leaderboard(game_state):
    return sorted(game_state["student_scores"].items(), key=lambda x: x[1], reverse=True)

# =========================
# MAIN APP
# =========================
game_state = get_game_state()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚡ Scripture Speed Quiz")

ip = get_local_ip()
url = f"http://{ip}:8501"

qr = qrcode.make(url)
buf = BytesIO()
qr.save(buf, format="PNG")
st.sidebar.image(buf.getvalue(), caption="Scan to join", width="stretch")
st.sidebar.code(url)

mode = st.sidebar.radio("Who are you?", ["Student", "Teacher"], label_visibility="collapsed")

is_teacher = False
student_name = None

if mode == "Teacher":
    pin = st.sidebar.text_input("Enter teacher PIN:", type="password")
    if pin == TEACHER_PIN:
        is_teacher = True
        st.sidebar.success("Teacher mode")
    elif pin:
        st.sidebar.error("Incorrect PIN")
else:
    student_name = st.sidebar.text_input("Your name:", max_chars=30)
    if student_name:
        st.sidebar.success(f"Welcome, {student_name}!")
        if student_name in game_state["student_scores"]:
            st.sidebar.metric("Your Score", game_state["student_scores"][student_name])

# =========================
# TEACHER VIEW
# =========================
if is_teacher:
    st.title("📋 Teacher Control Panel")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("▶️ Start New Question", use_container_width=True):
            start_new_question(game_state)
            game_state["version"] += 1  # trigger student refresh
            st.rerun()
    with col2:
        if st.button("🔒 Lock Answers", use_container_width=True):
            lock_answers(game_state)
    with col3:
        if st.button("🔁 Reset Game", use_container_width=True):
            base = get_game_state()
            game_state.clear()
            game_state.update({
                "current_phrase": None,
                "correct_ref": None,
                "options": [],
                "question_start_time": None,
                "answers_open": False,
                "student_scores": {},
                "student_answers": {},
                "question_number": 0,
                "question_history": [],
                "version": 0,
            })
            st.rerun()
    with col4:
        if st.button("⏭️ Next Question", use_container_width=True):
            lock_answers(game_state)
            time.sleep(0.3)
            start_new_question(game_state)
            game_state["version"] += 1
            st.rerun()

    st.markdown("---")

    if game_state["current_phrase"] is None:
        st.info("Click Start New Question to begin.")
    else:
        st.subheader(f"📖 Question {game_state['question_number']}")
        st.markdown(f"<div class='big-text'>{game_state['current_phrase']}</div>", unsafe_allow_html=True)

        elapsed = time.time() - game_state["question_start_time"]
        remaining = max(0, 20 - elapsed)

        colA, colB = st.columns(2)
        with colA:
            st.metric("Elapsed", f"{elapsed:.1f}s")
        with colB:
            st.metric("Remaining", f"{remaining:.1f}s")

        leaderboard_placeholder = st.empty()

        def render_leaderboard():
            leaderboard = get_leaderboard(game_state)
            with leaderboard_placeholder.container():
                st.subheader("🏆 Leaderboard")
                if not leaderboard:
                    st.write("No scores yet.")
                else:
                    for rank, (name, score) in enumerate(leaderboard, 1):
                        medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
                        st.markdown(
                            f"<div class='leaderboard-card'><strong>{medal} {name}</strong> — {score} points</div>",
                            unsafe_allow_html=True
                        )

        render_leaderboard()

        if remaining == 0:
            render_leaderboard()

# =========================
# STUDENT VIEW
# =========================
if not is_teacher:
    st.title("⚡ Scripture Speed Quiz")

    if not student_name:
        st.info("Enter your name to play.")
        st.stop()

    # 🔄 Auto-refresh when teacher starts a new question
    if "last_version" not in st.session_state:
        st.session_state.last_version = game_state["version"]

    if st.session_state.last_version != game_state["version"]:
        st.session_state.last_version = game_state["version"]
        st.rerun()

    if game_state["current_phrase"] is None:
        st.info("Waiting for teacher to start a question.")
        st.stop()

    st.subheader(f"📖 Question {game_state['question_number']}")
    st.markdown(f"<div class='big-text'>{game_state['current_phrase']}</div>", unsafe_allow_html=True)

    elapsed = time.time() - game_state["question_start_time"]
    remaining = max(0, 20 - elapsed)
    already_answered = student_name in game_state["student_answers"]

    timer_placeholder = st.empty()

    if game_state["answers_open"] and not already_answered and remaining > 0:
        if remaining > 14:
            color = "#28a745"
        elif remaining > 7:
            color = "#ffc107"
        else:
            color = "#dc3545"
        timer_placeholder.markdown(
            f"""
            <div style='font-size: 72px; font-weight: bold; color: {color};
                        text-align: center; animation: pulse 1s infinite;'>
                ⏱️ {int(remaining)}
            </div>
            <div style='text-align: center; font-size: 20px; color: #666; margin-top: -10px;'>
                Points available: {compute_points(elapsed)}
            </div>
            """,
            unsafe_allow_html=True
        )
    elif already_answered:
        timer_placeholder.markdown("<div class='timer-text'>Answer Submitted</div>", unsafe_allow_html=True)
    else:
        timer_placeholder.markdown("<div class='timer-text'>Locked</div>", unsafe_allow_html=True)

    st.write("")
    st.write("### Choose the correct reference:")

    option_cols = st.columns(2)
    for i, opt in enumerate(game_state["options"]):
        with option_cols[i % 2]:
            disabled = (not game_state["answers_open"]) or already_answered or (remaining <= 0)
            if st.button(opt, key=f"opt-{opt}-{student_name}", disabled=disabled, use_container_width=True):
                record_student_answer(game_state, student_name, opt)
                st.rerun()

    st.write("---")

    if already_answered:
        info = game_state["student_answers"][student_name]
        if info["correct"]:
            st.success(
                f"Correct! You answered {info['answer']} in {info['elapsed']:.1f}s "
                f"and earned {info['points']} points."
            )
        else:
            st.error(f"Incorrect. You answered {info['answer']}.")
    else:
        if remaining <= 0:
            st.warning("Time is up.")

    total_score = game_state["student_scores"].get(student_name, 0)
    st.markdown(
        f"<div class='score-card'>Your Score: {total_score}</div>",
        unsafe_allow_html=True
    )

    if game_state["answers_open"] and not already_answered and remaining > 0:
        time.sleep(0.1)
        st.rerun()
