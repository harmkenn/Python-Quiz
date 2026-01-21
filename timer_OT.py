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

# Teacher PIN
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
    }

# =========================
# PAGE CONFIG
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
.option-button button { 
    width: 100%; 
    height: 80px; 
    white-space: normal; 
    font-size: 20px;
    margin: 5px 0;
    font-weight: 600;
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
}
.correct-answer {
    background-color: #d4edda !important;
    border: 3px solid #28a745 !important;
}
.incorrect-answer {
    background-color: #f8d7da !important;
    border: 3px solid #dc3545 !important;
}
.stButton button:hover {
    transform: scale(1.02);
    transition: transform 0.2s;
}
</style>
""", unsafe_allow_html=True)

# Initialize local session state for UI
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

# =========================
# HELPER FUNCTIONS
# =========================
def get_local_ip():
    """Detect local IP address for QR code."""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def start_new_question(game_state):
    """Teacher starts a new question: pick phrase, build options, reset answers."""
    refs = list(SCRIPTURES.keys())
    recent_refs = [q["ref"] for q in game_state["question_history"][-5:]]
    available_refs = [r for r in refs if r not in recent_refs]
    if not available_refs:
        available_refs = refs
    
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
    
    return game_state

def compute_points(elapsed_seconds: float) -> int:
    return max(0, 10 - int(elapsed_seconds // 2))

def record_student_answer(game_state, name: str, answer_ref: str):
    """Record a student's answer if answers are open and they haven't answered yet."""
    if not game_state["answers_open"]:
        return game_state
    if name in game_state["student_answers"]:
        return game_state
    if game_state["question_start_time"] is None:
        return game_state
    
    elapsed = time.time() - game_state["question_start_time"]
    if elapsed < 0:
        elapsed = 0
    
    correct = (answer_ref == game_state["correct_ref"])
    points = compute_points(elapsed) if correct and elapsed <= 10 else 0
    
    game_state["student_answers"][name] = {
        "answer": answer_ref,
        "elapsed": elapsed,
        "points": points,
        "correct": correct,
    }
    
    if name not in game_state["student_scores"]:
        game_state["student_scores"][name] = 0
    game_state["student_scores"][name] += points
    
    return game_state

def lock_answers(game_state):
    """Lock answers and save to history."""
    game_state["answers_open"] = False
    if game_state["correct_ref"]:
        game_state["question_history"].append({
            "number": game_state["question_number"],
            "ref": game_state["correct_ref"],
            "phrase": game_state["current_phrase"],
            "total_answers": len(game_state["student_answers"]),
            "correct_answers": sum(1 for a in game_state["student_answers"].values() if a["correct"])
        })
    return game_state

def get_leaderboard(game_state):
    """Return sorted leaderboard."""
    return sorted(game_state["student_scores"].items(), key=lambda x: x[1], reverse=True)

# =========================
# MAIN APP
# =========================

# Load shared game state
game_state = get_game_state()

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚡ Scripture Speed Quiz")

ip = get_local_ip()
port = 8501
url = f"http://{ip}:{port}"

qr = qrcode.make(url)
buf = BytesIO()
qr.save(buf, format="PNG")
st.sidebar.image(buf.getvalue(), caption="Scan to join", width="stretch")
st.sidebar.code(url, language=None)

st.sidebar.markdown("---")

mode = st.sidebar.radio("Who are you?", ["Student", "Teacher"], label_visibility="collapsed")

is_teacher = False
student_name = None

if mode == "Teacher":
    pin = st.sidebar.text_input("Enter teacher PIN:", type="password")
    if pin == TEACHER_PIN:
        is_teacher = True
        st.sidebar.success("✅ Teacher mode")
    elif pin:
        st.sidebar.error("❌ Incorrect PIN")
else:
    student_name = st.sidebar.text_input("Your name:", max_chars=30)
    if student_name:
        st.sidebar.success(f"Welcome, {student_name}! 👋")
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
            st.rerun()
    
    with col2:
        if st.button("🔒 Lock Answers", use_container_width=True):
            lock_answers(game_state)
            st.rerun()
    
    with col3:
        if st.button("🔁 Reset Game", use_container_width=True):
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
            })
            st.rerun()
    
    with col4:
        if st.button("⏭️ Next Question", use_container_width=True):
            lock_answers(game_state)
            time.sleep(0.5)
            start_new_question(game_state)
            st.rerun()
    
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Questions Asked", game_state["question_number"])
    with col_b:
        st.metric("Active Players", len(game_state["student_scores"]))
    with col_c:
        if game_state["student_answers"]:
            avg_time = sum(a["elapsed"] for a in game_state["student_answers"].values()) / len(game_state["student_answers"])
            st.metric("Avg Response Time", f"{avg_time:.1f}s")
        else:
            st.metric("Avg Response Time", "—")
    
    st.markdown("---")
    
    if game_state["current_phrase"] is None:
        st.info("🎮 No active question. Click **Start New Question** to begin.")
    else:
        st.subheader(f"📖 Question {game_state['question_number']}")
        st.markdown(f"<div class='big-text'>{game_state['current_phrase']}</div>", unsafe_allow_html=True)
        
        if game_state["question_start_time"]:
            elapsed = time.time() - game_state["question_start_time"]
            remaining = max(0, 20 - elapsed)
            
            timer_col1, timer_col2 = st.columns(2)
            with timer_col1:
                st.metric("Time Elapsed", f"{elapsed:.1f}s")
            with timer_col2:
                st.metric(
                    "Time for Points",
                    f"{remaining:.1f}s", 
                    delta="Time up!" if remaining == 0 else None,
                    delta_color="off" if remaining == 0 else "normal"
                )
    
    st.markdown("---")
    st.subheader("🏆 Leaderboard")
    
    if not game_state["student_scores"]:
        st.write("No scores yet.")
    else:
        leaderboard = get_leaderboard(game_state)
        
        for rank, (name, score) in enumerate(leaderboard[:10], 1):
            medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
            st.markdown(f"""
            <div class='leaderboard-card'>
                <strong>{medal} {name}</strong> — {score} points
            </div>
            """, unsafe_allow_html=True)

# =========================
# STUDENT VIEW
# =========================
if not is_teacher:
    st.title("⚡ Scripture Speed Quiz")
    
    if not student_name:
        st.info("👈 Enter your name in the sidebar to play!")
        st.stop()
    
    # Add refresh button
    col_refresh1, col_refresh2 = st.columns([4, 1])
    with col_refresh2:
        if st.button("🔄 Refresh", use_container_width=True, key="top_refresh"):
            st.rerun()
    
    if game_state["current_phrase"] is None:
        st.info("⏳ Waiting for the teacher to start a question...")
        st.caption("Click 🔄 Refresh to check for new questions")
        
        if game_state["student_scores"]:
            st.subheader("🏆 Current Leaderboard")
            leaderboard = get_leaderboard(game_state)
            for rank, (name, score) in enumerate(leaderboard[:5], 1):
                medal = "🥇" if rank == 1 else "🥈" if rank == 2 else "🥉" if rank == 3 else f"{rank}."
                highlight = "background-color: #fff3cd;" if name == student_name else ""
                st.markdown(f"""
                <div style='padding: 10px; margin: 5px 0; border-radius: 5px; {highlight}'>
                    <strong>{medal} {name}</strong> — {score} points
                </div>
                """, unsafe_allow_html=True)
        st.stop()
    
    st.subheader(f"📖 Question {game_state['question_number']}")
    st.markdown(f"<div class='big-text'>{game_state['current_phrase']}</div>", unsafe_allow_html=True)
    
    st.write("")
    
    if game_state["question_start_time"]:
        elapsed = time.time() - game_state["question_start_time"]
        remaining = max(0, 10 - elapsed)
    else:
        elapsed = 0
        remaining = 0
    
    already_answered = student_name in game_state["student_answers"]
    
    # Create countdown timer display
    timer_placeholder = st.empty()
    
    if game_state["answers_open"] and not already_answered:
        if remaining > 0:
            # Color coding based on time remaining
            if remaining > 7:
                color = "#28a745"  # Green
            elif remaining > 4:
                color = "#ffc107"  # Yellow
            else:
                color = "#dc3545"  # Red
            
            timer_placeholder.markdown(f"""
            <div style='font-size: 72px; font-weight: bold; color: {color}; 
                        text-align: center; animation: pulse 1s infinite;'>
                ⏱️ {int(remaining)}
            </div>
            <div style='text-align: center; font-size: 20px; color: #666; margin-top: -10px;'>
                Points available: {compute_points(elapsed)}
            </div>
            """, unsafe_allow_html=True)
        else:
            timer_placeholder.markdown("<div class='timer-text'>⏱️ 0 (No points)</div>", unsafe_allow_html=True)
    elif already_answered:
        timer_placeholder.markdown("<div class='timer-text'>✅ Answer Submitted</div>", unsafe_allow_html=True)
    else:
        timer_placeholder.markdown("<div class='timer-text'>🔒 Answers Locked</div>", unsafe_allow_html=True)
    
    st.write("")
    st.write("### Choose the correct reference:")
    
    option_cols = st.columns(2)
    for i, opt in enumerate(game_state["options"]):
        col = option_cols[i % 2]
        with col:
            disabled = (not game_state["answers_open"]) or already_answered or (remaining <= 0)
            
            button_class = ""
            if already_answered:
                student_answer = game_state["student_answers"][student_name]["answer"]
                if opt == game_state["correct_ref"]:
                    button_class = "correct-answer"
                elif opt == student_answer and not game_state["student_answers"][student_name]["correct"]:
                    button_class = "incorrect-answer"
            
            if st.button(opt, key=f"opt-{opt}-{student_name}", disabled=disabled, use_container_width=True):
                record_student_answer(game_state, student_name, opt)
                st.rerun()
    
    st.write("---")
    
    if already_answered:
        info = game_state["student_answers"][student_name]
        if info['correct']:
            st.success(
                f"✅ Correct! You answered **{info['answer']}** "
                f"in {info['elapsed']:.1f}s and earned **{info['points']} points**!"
            )
        else:
            st.error(
                f"❌ Incorrect. You answered **{info['answer']}**. "
                f"The correct answer was **{game_state['correct_ref']}**."
            )
    else:
        if not game_state["answers_open"] or remaining <= 0:
            st.warning("⚠️ You did not answer in time or answers are locked.")
    
    total_score = game_state["student_scores"].get(student_name, 0)
    st.markdown(f"""
    <div class='score-card'>
        🎯 Your Total Score: <strong>{total_score}</strong> points
    </div>
    """, unsafe_allow_html=True)
    
    if game_state["answers_open"] and not already_answered and remaining > 0:
        st.caption("💡 Answer quickly for more points!")
        time.sleep(0.1)  # Faster refresh for smoother countdown
        st.rerun()
