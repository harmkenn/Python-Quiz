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
        return pd.read_csv(ANSWERS_FILE)
    return pd.DataFrame(columns=["Student", "Question", "Answer"])

def append_answer(student, question, answer):
    df = read_answers()
    df = pd.concat([df, pd.DataFrame([{"Student": student, "Question": question, "Answer": answer}])], ignore_index=True)
    df.to_csv(ANSWERS_FILE, index=False)

def read_state():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        df = pd.read_csv(STATE_FILE)
        if not df.empty:
            return df.iloc[0].to_dict()
    # Default state
    return {"current_question": -1, "quiz_started": False}

def write_state(state):
    pd.DataFrame([state]).to_csv(STATE_FILE, index=False)

def reset_quiz():
    if os.path.exists(ANSWERS_FILE):
        os.remove(ANSWERS_FILE)
    write_state({"current_question": -1, "quiz_started": False})
    st.session_state.clear()

def calculate_scores(df, quiz):
    scores = {}
    for student in df["Student"].unique():
        student_df = df[df["Student"] == student]
        correct_count = 0
        for _, row in student_df.iterrows():
            q_text = row["Question"]
            q_match = next((q for q in quiz if q["q"] == q_text), None)
            if q_match and q_match["type"] == "MC" and str(row["Answer"]).strip() == q_match["answer"]:
                correct_count += 1
        scores[student] = correct_count
    return scores

# --- Streamlit App ---
st.set_page_config(page_title="Classroom Quiz", layout="wide")
st.title("📚 Classroom Quiz")

# --- IP Detection ---
def get_local_ip():
    try:
        ips = os.popen("hostname -I").read().split()
        for ip in ips:
            if ip.startswith("10.") or ip.startswith("192."):
                return ip
        return "127.0.0.1"
    except:
        return "127.0.0.1"

app_url = f"http://{get_local_ip()}:8501"
st.sidebar.markdown("## 🔗 Connection Info")
st.sidebar.write("Connect to teacher hotspot and open:")
st.sidebar.code(app_url)
st.sidebar.image(make_qr_image(app_url), caption="📱 Scan to join", use_container_width=True)

mode = st.sidebar.radio("Mode:", ["Student", "Teacher"])
quiz = load_quiz_from_csv(QUESTIONS_FILE)
state = read_state()

# ---------------- Student View ----------------
if mode == "Student":
    st_autorefresh(interval=2000, limit=None, key="student_refresh")
    student_name = st.text_input("✏️ Enter your name to start:")

    if student_name:
        # Waiting room
        if not state["quiz_started"]:
            st.info("⌛ Waiting for teacher to start the quiz...")
        else:
            q_index = state["current_question"]
            if q_index >= 0 and q_index < len(quiz):
                q = quiz[q_index]
                st.subheader(f"📝 Question {q_index + 1}")
                st.markdown(q["q"].replace("\n", "  \n"))

                key = f"{student_name}_q{q_index}"
                if q["type"] == "MC":
                    selected = st.radio("Choose your answer:", q["options"], key=key)
                else:
                    selected = st.text_area("Your answer:", key=key)

                if st.button("✅ Submit Answer", key=f"submit_{key}"):
                    append_answer(student_name, q["q"], selected)
                    st.success("Answer submitted!")

# ---------------- Teacher View ----------------
elif mode == "Teacher":
    password = st.text_input("🔑 Enter teacher password:", type="password")
    if password == "secret123":
        st.header("👩‍🏫 Teacher Dashboard")

        col_top1, col_top2 = st.columns([1, 1])
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

        # Waiting Room: show logged-in students
        st.subheader("👥 Students in Waiting Room / Quiz")
        df = read_answers()
        students = df["Student"].unique().tolist()
        if not students:
            st.write("No students yet")
        else:
            for s in students:
                st.write(f"- {s}")

        # Quiz display
        if state["quiz_started"] and quiz:
            q_index = state["current_question"]
            if q_index < len(quiz):
                q = quiz[q_index]
                col_left, col_mid, col_right = st.columns([1, 2, 1])

                # Middle: question and navigation
                with col_mid:
                    st.subheader(f"👩‍🏫 Question {q_index + 1}")
                    st.markdown(q["q"].replace("\n", "  \n"))
                    if st.button("⏭ Next") and q_index < len(quiz)-1:
                        state["current_question"] += 1
                        write_state(state)
                        st.experimental_rerun()
                    if st.button("⏮ Previous") and q_index > 0:
                        state["current_question"] -= 1
                        write_state(state)
                        st.experimental_rerun()

                # Right: student responses / possible answers
                with col_right:
                    st.subheader("📨 Student Responses")
                    df_q = df[df["Question"] == q["q"]]
                    if not df_q.empty:
                        for ans in df_q['Answer']:
                            st.write(f"- {ans}")

                    # Only MC questions show possible answers
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
    elif password:
        st.error("❌ Incorrect password")
