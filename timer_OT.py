import streamlit as st
import time
import random
import socket
import qrcode
from io import BytesIO

# =========================
# SHARED SCRIPTURE DATA
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

# =========================
# GLOBAL GAME STATE (SERVER-SIDE)
# =========================

if "game" not in st.session_state:
    st.session_state.game = {
        "current_phrase": None,          # text of the phrase
        "correct_ref": None,             # correct reference
        "options": [],                   # list of 6 references
        "question_start_time": None,     # float timestamp
        "answers_open": False,           # can students answer?
        "student_scores": {},            # {name: score}
        "student_answers": {},           # {name: {"answer": ref, "elapsed": seconds, "points": int}}
        "question_number": 0,            # which question we are on
    }

GAME = st.session_state.game

# Teacher PIN (change this to whatever you want)
TEACHER_PIN = "1234"

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(page_title="Scripture Speed Quiz", layout="wide")

st.markdown("""
<style>
.big-text { font-size: 24px; }
.timer-text { font-size: 32px; font-weight: bold; color: #FF4B4B; }
.option-button button { width: 100%; height: 70px; white-space: normal; font-size: 18px; }
.score-table td, .score-table th { padding: 4px 8px; }
</style>
""", unsafe_allow_html=True)

# =========================
# HELPER FUNCTIONS
# =========================

def get_local_ip():
    """Detect local IP address for QR code."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # no data actually sent
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"


def start_new_question():
    """Teacher starts a new question: pick phrase, build options, reset answers."""
    refs = list(SCRIPTURES.keys())
    correct_ref = random.choice(refs)
    phrase = SCRIPTURES[correct_ref]

    # Build 5 incorrect options
    wrong_refs = [r for r in refs if r != correct_ref]
    wrong_choices = random.sample(wrong_refs, k=min(5, len(wrong_refs)))

    options = wrong_choices + [correct_ref]
    random.shuffle(options)

    GAME["current_phrase"] = phrase
    GAME["correct_ref"] = correct_ref
    GAME["options"] = options
    GAME["question_start_time"] = time.time()
    GAME["answers_open"] = True
    GAME["student_answers"] = {}
    GAME["question_number"] += 1


def compute_points(elapsed_seconds: float) -> int:
    """Points = max(0, 11 - int(seconds_elapsed))"""
    return max(0, 11 - int(elapsed_seconds))


def record_student_answer(name: str, answer_ref: str):
    """Record a student's answer if answers are open and they haven't answered yet."""
    if not GAME["answers_open"]:
        return

    if name in GAME["student_answers"]:
        return  # already answered this question

    if GAME["question_start_time"] is None:
        return

    elapsed = time.time() - GAME["question_start_time"]
    if elapsed < 0:
        elapsed = 0

    correct = (answer_ref == GAME["correct_ref"])
    points = compute_points(elapsed) if correct and elapsed <= 10 else 0

    GAME["student_answers"][name] = {
        "answer": answer_ref,
        "elapsed": elapsed,
        "points": points,
        "correct": correct,
    }

    if name not in GAME["student_scores"]:
        GAME["student_scores"][name] = 0
    GAME["student_scores"][name] += points


def lock_answers():
    GAME["answers_open"] = False


# =========================
# SIDEBAR: QR + LOGIN / TEACHER MODE
# =========================

st.sidebar.title("Scripture Speed Quiz")

# Auto-detect network URL and show QR code
ip = get_local_ip()
port = 8501  # default Streamlit port
url = f"http://{ip}:{port}"

qr = qrcode.make(url)
buf = BytesIO()
qr.save(buf, format="PNG")
st.sidebar.image(buf.getvalue(), caption="Scan to join the game")
st.sidebar.write(f"Or enter: {url}")

st.sidebar.markdown("---")

mode = st.sidebar.radio("Who are you?", ["Student", "Teacher"])

is_teacher = False
student_name = None

if mode == "Teacher":
    pin = st.sidebar.text_input("Enter teacher PIN:", type="password")
    if pin == TEACHER_PIN:
        is_teacher = True
        st.sidebar.success("Teacher mode unlocked.")
    else:
        if pin:
            st.sidebar.error("Incorrect PIN.")
else:
    student_name = st.sidebar.text_input("Your name:")
    if student_name:
        st.sidebar.success(f"Welcome, {student_name}!")

# =========================
# TEACHER VIEW
# =========================

if is_teacher:
    st.title("📋 Teacher Control Panel")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("▶️ Start New Question"):
            start_new_question()
            st.rerun()

    with col2:
        if st.button("🔒 Lock Answers"):
            lock_answers()
            st.rerun()

    with col3:
        if st.button("🔁 Reset Scores"):
            GAME["student_scores"] = {}
            GAME["student_answers"] = {}
            GAME["question_number"] = 0
            GAME["current_phrase"] = None
            GAME["correct_ref"] = None
            GAME["options"] = []
            GAME["question_start_time"] = None
            GAME["answers_open"] = False
            st.experimental_rerun()

    st.markdown("---")

    if GAME["current_phrase"] is None:
        st.info("No active question. Click **Start New Question** to begin.")
    else:
        st.subheader(f"Question {GAME['question_number']}")
        st.markdown(f"<div class='big-text'><b>Phrase:</b> {GAME['current_phrase']}</div>", unsafe_allow_html=True)
        st.write("")
        st.write("**Options:**")
        for opt in GAME["options"]:
            if opt == GAME["correct_ref"]:
                st.markdown(f"- ✅ **{opt}**")
            else:
                st.markdown(f"- {opt}")

        if GAME["question_start_time"]:
            elapsed = time.time() - GAME["question_start_time"]
            remaining = max(0, 10 - elapsed)
            st.markdown(
                f"**Time since start:** {elapsed:.1f} s &nbsp;&nbsp; | "
                f"&nbsp;&nbsp; **Time left (for scoring):** {remaining:.1f} s"
            )

        st.markdown("---")

        st.subheader("Student Answers (This Question)")
        if not GAME["student_answers"]:
            st.write("No answers yet.")
        else:
            rows = []
            for name, info in GAME["student_answers"].items():
                rows.append({
                    "Name": name,
                    "Answer": info["answer"],
                    "Correct?": "✅" if info["correct"] else "❌",
                    "Time (s)": f"{info['elapsed']:.1f}",
                    "Points": info["points"],
                })
            st.table(rows)

    st.markdown("---")
    st.subheader("🏆 Total Scores")
    if not GAME["student_scores"]:
        st.write("No scores yet.")
    else:
        sorted_scores = sorted(GAME["student_scores"].items(), key=lambda x: x[1], reverse=True)
        score_rows = [{"Name": name, "Score": score} for name, score in sorted_scores]
        st.table(score_rows)

# =========================
# STUDENT VIEW
# =========================

if not is_teacher:
    st.title("📱 Scripture Speed Quiz")

    if not student_name:
        st.info("Enter your name in the sidebar to play.")
        st.stop()

    if GAME["current_phrase"] is None:
        st.info("Waiting for the teacher to start a question...")
        st.stop()

    st.subheader(f"Question {GAME['question_number']}")
    st.markdown(f"<div class='big-text'><b>Phrase:</b> {GAME['current_phrase']}</div>", unsafe_allow_html=True)
    st.write("")

    if GAME["question_start_time"]:
        elapsed = time.time() - GAME["question_start_time"]
        remaining = max(0, 10 - elapsed)
    else:
        elapsed = 0
        remaining = 0

    if GAME["answers_open"]:
        st.markdown(f"<div class='timer-text'>⏱️ Time left: {remaining:.1f} s</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='timer-text'>⏱️ Answers locked</div>", unsafe_allow_html=True)

    st.write("")

    already_answered = student_name in GAME["student_answers"]

    st.write("### Choose the correct reference:")
    option_cols = st.columns(2)
    for i, opt in enumerate(GAME["options"]):
        col = option_cols[i % 2]
        with col:
            disabled = (not GAME["answers_open"]) or already_answered or (remaining <= 0)
            if st.button(opt, key=f"opt-{opt}", disabled=disabled):
                record_student_answer(student_name, opt)
                st.experimental_rerun()

    st.write("---")

    if already_answered:
        info = GAME["student_answers"][student_name]
        st.success(
            f"You answered: **{info['answer']}** "
            f"({'correct' if info['correct'] else 'incorrect'}) "
            f"in {info['elapsed']:.1f} s and earned {info['points']} points."
        )
    else:
        if not GAME["answers_open"] or remaining <= 0:
            st.warning("You did not answer in time or answers are locked for this question.")

    total_score = GAME["student_scores"].get(student_name, 0)
    st.markdown(f"### Your total score: **{total_score}**")

    st.caption("If the timer seems stuck, pull to refresh or tap anywhere to trigger an update.")
