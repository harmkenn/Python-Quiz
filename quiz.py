import streamlit as st
import qrcode
from io import BytesIO
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh

# --- Files ---
QUESTIONS_FILE = "questions.csv"
CSV_FILE = "answers.csv"
STATE_FILE = "state.csv"

# --- Functions ---
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
        try:
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
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
            return []
    else:
        st.error("Questions CSV file is missing or empty!")
        return []

def read_answers():
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Student", "Question", "Answer"])

def append_answer(student, question, answer):
    df = read_answers()
    if not ((df["Student"] == student) & (df["Question"] == question)).any():
        df = pd.concat([df, pd.DataFrame([{"Student": student, "Question": question, "Answer": answer}])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

def read_current_question():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        df = pd.read_csv(STATE_FILE)
        if "current_question" in df.columns and not df.empty:
            return int(df.loc[0, "current_question"])
    # default if missing or empty
    return -1  # -1 indicates quiz hasn't started (waiting room)

def write_current_question(q_index):
    pd.DataFrame([{"current_question": q_index}]).to_csv(STATE_FILE, index=False)

def reset_quiz():
    pd.DataFrame(columns=["Student", "Question", "Answer"]).to_csv(CSV_FILE, index=False)
    write_current_question(-1)  # reset to waiting room
    keys_to_clear = [key for key in st.session_state.keys() if key.startswith("show_answer_") or key in ["current_question"]]
    for key in keys_to_clear:
        del st.session_state[key]

def calculate_scores(df, quiz):
    scores = {}
    for student in df["Student"].unique():
        student_df = df[df["Student"] == student]
        correct_count = 0
        for _, row in student_df.iterrows():
            q_text = row["Question"]
            q_match = next((q for q in quiz if q["q"] == q_text), None)
            if q_match and q_match["type"] == "MC":
                if str(row["Answer"]).strip() == q_match["answer"]:
                    correct_count += 1
        scores[student] = correct_count
    return scores

# --- Load quiz ---
quiz = load_quiz_from_csv(QUESTIONS_FILE)

# --- Streamlit config ---
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
    except Exception:
        return "127.0.0.1"

# --- Sidebar ---
app_url = f"http://{get_local_ip()}:8501"
st.sidebar.markdown("## 🔗 Connection Info")
st.sidebar.write("Students: connect to your teacher's Wi-Fi hotspot, then open:")
st.sidebar.code(app_url)
qr_buf = make_qr_image(app_url)
st.sidebar.image(qr_buf, caption="📱 Scan to join", use_container_width=True)

mode = st.sidebar.radio("Select mode:", ["Student", "Teacher"])

# --- Student View ---
if mode == "Student":
    st_autorefresh(interval=2000, limit=None, key="student_refresh")
    student_name = st.text_input("✏️ Enter your name to start:")

    if student_name and quiz:
        q_index = read_current_question()
        if q_index == -1:
            st.info("⏳ Waiting for teacher to start the quiz...")
        elif q_index < len(quiz):
            q = quiz[q_index]
            st.subheader(f"📝 Question {q_index + 1}")
            st.markdown(q["q"].replace("\n", "  \n"))

            key = f"{student_name}_q{q_index}"
            if q["type"] == "MC":
                selected = st.radio("Choose your answer:", q["options"], index=0, key=key)
            elif q["type"] == "OR":
                selected = st.text_area("Your answer:", key=key)

            if st.button("✅ Submit Answer", key=f"submit_{key}"):
                append_answer(student_name, q["q"], selected)
                st.success("Answer submitted!")
        else:
            st.success("🎉 Quiz finished!")

# --- Teacher View ---
elif mode == "Teacher":
    password = st.text_input("🔑 Enter teacher password:", type="password")
    if password == "secret123":  # change as needed
        st_autorefresh(interval=5000, limit=None, key="teacher_refresh")

        col_top1, col_top2 = st.columns([1, 1])
        with col_top1:
            if st.button("🧹 Reset Quiz"):
                reset_quiz()
                st.success("Quiz has been reset. Students can start fresh.")
        with col_top2:
            if st.button("🔄 Refresh Now"):
                st.rerun()

        if "current_question" not in st.session_state:
            st.session_state["current_question"] = read_current_question()
        q_index = st.session_state["current_question"]

        col_left, col_mid, col_right = st.columns([1, 2, 1])
        df = read_answers()

        # --- Waiting Room ---
        if q_index == -1:
            with col_mid:
                st.subheader("⏳ Waiting Room")
                st.write("Students logged in:")
                if not df.empty:
                    for student in df["Student"].unique():
                        st.write(f"- {student}")
                else:
                    st.write("No students yet")

                if st.button("▶️ Start Quiz"):
                    st.session_state["current_question"] = 0
                    write_current_question(0)
                    st.success("Quiz started!")
        else:
            # --- Left: Students logged in (+ scores only if show_answer pressed for that question) ---
            with col_left:
                st.subheader("👥 Students Logged In")
                if not df.empty:
                    show_key = f"show_answer_{q_index}"
                    if st.session_state.get(show_key):
                        scores = calculate_scores(df, quiz)
                        for student, score in scores.items():
                            st.write(f"- {student} ({score} correct)")
                    else:
                        for student in df["Student"].unique():
                            st.write(f"- {student}")
                else:
                    st.write("No students yet")

            # --- Middle: Current question + responses ---
            with col_mid:
                if quiz and q_index < len(quiz):
                    q = quiz[q_index]
                    st.subheader(f"👩‍🏫 Question {q_index + 1}")
                    st.markdown(q["q"].replace("\n", "  \n"))
                    df_q = df[df["Question"] == q["q"]]
                    total_responses = len(df_q)
                    st.write(f"📝 Total responses: {total_responses}")

                    if q["type"] == "MC" and total_responses > 0:
                        counts = df_q['Answer'].value_counts()
                        percentages = counts / total_responses * 100
                        with st.expander("📊 Show Answer Percentages", expanded=False):
                            for option in q["options"]:
                                pct = percentages.get(option, 0)
                                st.write(f"{option}: {pct:.1f}%")
                                st.progress(min(int(pct), 100))
                    elif q["type"] == "OR":
                        with st.expander("📝 Open Responses", expanded=False):
                            for idx, row in df_q.iterrows():
                                st.write(f"- {row['Student']}: {row['Answer']}")

                    # --- Navigation ---
                    col1, col2 = st.columns(2)
                    if col1.button("⏮ Previous") and q_index > 0:
                        st.session_state["current_question"] = q_index - 1
                        write_current_question(st.session_state["current_question"])
                    if col2.button("⏭ Next") and q_index < len(quiz) - 1:
                        st.session_state["current_question"] = q_index + 1
                        write_current_question(st.session_state["current_question"])

            # --- Right: Possible answers + show answer button ---
            with col_right:
                if quiz and q_index < len(quiz):
                    q = quiz[q_index]
                    st.subheader("✅ Possible Answers")
                    if st.button("👀 Show Correct Answer"):
                        st.session_state[f"show_answer_{q_index}"] = True

                    show_key = f"show_answer_{q_index}"
                    if q["type"] == "MC":
                        for option in q["options"]:
                            if st.session_state.get(show_key) and option == q["answer"]:
                                st.markdown(f"**✅ {option}**")
                            else:
                                st.write(f"- {option}")
                    elif q["type"] == "OR":
                        st.subheader("📝 Open Response")
                        st.write("Students type their own answers here.")
    elif password:
        st.error("❌ Incorrect password")
