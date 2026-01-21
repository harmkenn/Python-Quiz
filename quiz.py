import streamlit as st
import qrcode
from io import BytesIO
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh

# --- Files ---
QUESTIONS_FILE = "questions.csv"
ANSWERS_FILE = "answers.csv"
STATE_FILE = "state.csv"

# --- Helpers ---
def make_qr_image(url):
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

def load_quiz_from_csv(file):
    if os.path.exists(file) and os.path.getsize(file) > 0:
        df = pd.read_csv(file, quotechar='"', keep_default_na=False)
        quiz_list = []
        for _, row in df.iterrows():
            options = [row[f"Option{i}"] for i in range(1, 5) if row.get(f"Option{i}", "").strip()]
            quiz_list.append({
                "q": row["Question"],
                "type": row["Type"],
                "options": options,
                "answer": row.get("Answer", "").strip()
            })
        return quiz_list
    return []

def read_answers():
    if os.path.exists(ANSWERS_FILE) and os.path.getsize(ANSWERS_FILE) > 0:
        df = pd.read_csv(ANSWERS_FILE)
        if "Score" not in df.columns:
            df["Score"] = 0
        return df
    return pd.DataFrame(columns=["Student", "Question", "Answer", "Score"])

def append_answer(student, question, answer):
    df = read_answers()
    # Add only if not already answered
    if df[(df["Student"] == student) & (df["Question"] == question)].empty:
        df = pd.concat([df, pd.DataFrame([{
            "Student": student,
            "Question": question,
            "Answer": answer,
            "Score": 0
        }])], ignore_index=True)
        df.to_csv(ANSWERS_FILE, index=False)

def score_question(question_text, q_type, correct_answer):
    df = read_answers()
    mask = (df["Question"] == question_text) & (df["Score"] == 0)
    for idx in df[mask].index:
        ans = df.at[idx, "Answer"]
        if q_type == "MC":
            df.at[idx, "Score"] = 1 if ans == correct_answer else 0
        else:
            df.at[idx, "Score"] = 1 if len(ans.strip().split()) > 3 else 0
    df.to_csv(ANSWERS_FILE, index=False)

def read_state():
    default_state = {"current_question": -1, "quiz_started": False}
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        try:
            df = pd.read_csv(STATE_FILE)
            if not df.empty:
                state = df.iloc[0].to_dict()
                state["quiz_started"] = bool(state.get("quiz_started", False))
                state["current_question"] = int(state.get("current_question", -1))
                return state
        except Exception:
            return default_state
    return default_state

def write_state(state):
    pd.DataFrame([state]).to_csv(STATE_FILE, index=False)

def reset_quiz():
    if os.path.exists(ANSWERS_FILE):
        os.remove(ANSWERS_FILE)
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)
    write_state({"current_question": -1, "quiz_started": False})
    st.session_state.clear()

# --- Streamlit App ---
st.set_page_config(page_title="Classroom Quiz", layout="wide")

# --- IP Detection ---
def get_local_ip():
    # Try multiple strategies to find a LAN IP address usable by student devices
    try:
        # hostname -I is common on Linux
        ips = os.popen("hostname -I").read().split()
        for ip in ips:
            if ip and not ip.startswith("127.") and not ip.startswith("169.254"):
                return ip
    except Exception:
        pass

    try:
        # UDP socket trick (doesn't send packets)
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        if ip and not ip.startswith("127."):
            return ip
    except Exception:
        pass

    try:
        ip = socket.gethostbyname(socket.gethostname())
        if ip and not ip.startswith("127."):
            return ip
    except Exception:
        pass

    return "127.0.0.1"

detected_ip = get_local_ip()
# Allow manual override if auto-detection doesn't pick the correct interface
override_ip = st.sidebar.text_input("Optional: Network IP to show in QR (leave blank to auto-detect)", value="")
if override_ip.strip():
    detected_ip = override_ip.strip()

app_url = f"http://{detected_ip}:8501"
st.sidebar.title("Offline Quiz v1.3")
st.sidebar.markdown("## 🔗 Connection Info")
st.sidebar.write("Connect to teacher hotspot and open:")
st.sidebar.code(app_url)
st.sidebar.image(make_qr_image(app_url), caption="📱 Scan to join", use_container_width=True)
if detected_ip.startswith("127."):
    st.sidebar.warning("App is bound to localhost. To allow student devices to connect, run Streamlit with --server.address 0.0.0.0 or enter the device IP above.")

mode = st.sidebar.radio("Mode:", ["Student", "Teacher"])
quiz = load_quiz_from_csv(QUESTIONS_FILE)
state = read_state()

# --- Student Waiting Room with Scores ---
df_answers = read_answers()
student_scores = df_answers.groupby("Student")["Score"].sum().reset_index()
student_scores = student_scores.sort_values(by="Score", ascending=False)
st.sidebar.subheader("👥 Students Logged (by score)")
if student_scores.empty:
    st.sidebar.write("No students yet")
else:
    for _, row in student_scores.iterrows():
        st.sidebar.write(f"- {row['Student']}: {row['Score']}")

# ---------------- Teacher Password ----------------
if mode == "Teacher":
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if not st.session_state["password_correct"]:
        password = st.sidebar.text_input("🔑 Enter teacher password:", type="password")
        if password == "secret123":
            st.session_state["password_correct"] = True
            st.sidebar.success("Password accepted!")
            st_autorefresh(interval=1000, limit=None, key="teacher_refresh")
        elif password:
            st.sidebar.error("❌ Incorrect password")

# ---------------- Student View ----------------
if mode == "Student":
    st.title("📚 Classroom Quiz")
    st_autorefresh(interval=2000, limit=None, key="student_refresh")

    # Lock student name after entry
    if "student_name" not in st.session_state:
        student_name_input = st.text_input("✏️ Enter your name to start:")
        if student_name_input:
            st.session_state["student_name"] = student_name_input
    student_name = st.session_state.get("student_name")

    if student_name:
        # Log student immediately if not already in answers.csv
        df_answers = read_answers()
        if student_name not in df_answers["Student"].values:
            df_answers = pd.concat([df_answers, pd.DataFrame([{
                "Student": student_name,
                "Question": "__login__",
                "Answer": "",
                "Score": 0
            }])], ignore_index=True)
            df_answers.to_csv(ANSWERS_FILE, index=False)

        if not state["quiz_started"]:
            st.info("⌛ Waiting for teacher to start the quiz...")
        else:
            q_index = state["current_question"]
            if q_index >= 0 and q_index < len(quiz):
                q = quiz[q_index]
                st.subheader(f"📝 Question {q_index + 1}")
                st.markdown(q["q"].replace("\n", "  \n"))

                # --- Check if already answered ---
                already_answered = not df_answers[
                    (df_answers["Student"] == student_name) &
                    (df_answers["Question"] == q["q"])
                ].empty

                if already_answered:
                    st.success("✅ You have already submitted your answer for this question.")
                else:
                    key = f"{student_name}_q{q_index}"
                    if q["type"] == "MC":
                        selected = st.radio("Choose your answer:", q["options"], key=key)
                    else:
                        selected = st.text_area("Your answer:", key=key)

                    if st.button("✅ Submit Answer", key=f"submit_{key}"):
                        append_answer(student_name, q["q"], selected)
                        st.success("Answer submitted! You cannot change it afterwards.")

# ---------------- Teacher View ----------------
elif mode == "Teacher" and st.session_state.get("password_correct"):
    st.header("👩‍🏫 Teacher Dashboard")

    # Top buttons
    col_top1, col_top2, col_top3 = st.columns([1,1,1])
    with col_top1:
        if st.button("🧹 Reset Quiz"):
            reset_quiz()
            st.success("Quiz reset to waiting room.")
    with col_top2:
        if st.button("▶️ Start Quiz") and not state["quiz_started"]:
            state["quiz_started"] = True
            state["current_question"] = 0
            write_state(state)
            st.success("Quiz started!")
    with col_top3:
        st_autorefresh(interval=5000, limit=None, key="teacher_autorefresh")

    # ---------------- Quiz Display ----------------
    if state["quiz_started"] and state["current_question"] >= 0 and quiz:
        q_index = state["current_question"]
        if q_index < len(quiz):
            q = quiz[q_index]
            col_mid, col_right = st.columns([1, 1])

            # --- Question Display & Navigation ---
            with col_mid:
                st.subheader(f"👩‍🏫 Question {q_index + 1}")
                st.markdown(q["q"].replace("\n", "  \n"))
                b_left, b_right = st.columns(2)
                with b_left:
                    if st.button("⏮ Previous") and q_index > 0:
                        state["current_question"] -= 1
                        write_state(state)
                with b_right:
                    if st.button("⏭ Next") and q_index < len(quiz)-1:
                        score_question(q["q"], q["type"], q.get("answer", ""))
                        state["current_question"] += 1
                        write_state(state)

            # --- Student Responses for current question only ---
            with col_right:
                df_answers = read_answers()
                df_q = df_answers[df_answers["Question"] == q["q"]]

                st.subheader(f"📨 Student Responses ({len(df_q)}/{len(df_answers['Student'].unique())} submitted)")
                with st.expander("Show all responses"):
                    if not df_q.empty:
                        for ans in df_q["Answer"]:
                            st.write(f"- {ans}")
                    else:
                        st.write("No answers submitted yet.")

                # Show possible MC answers
                if q["type"] == "MC":
                    st.subheader("✅ Possible Answers")
                    show_key = f"show_answer_{q_index}"
                    if st.button("👀 Show Correct Answer"):
                        st.session_state[show_key] = True
                    for option in q["options"]:
                        if st.session_state.get(show_key) and option == q["answer"]:
                            st.markdown(f"**✅ {option}**")
                        else:
                            st.write(f"- {option}")
