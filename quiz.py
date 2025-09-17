import streamlit as st
import qrcode
from io import BytesIO
import pandas as pd
import os
from streamlit_autorefresh import st_autorefresh

# --- Function to make QR code ---
def make_qr_image(url):
    qr = qrcode.QRCode(box_size=6, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf

# --- Quiz data ---
quiz = [
    {"q": "What is 2 + 2?", "options": ["3", "4", "5"], "answer": "4"},
    {"q": "Capital of France?", "options": ["Paris", "Rome", "Berlin"], "answer": "Paris"},
    {"q": "Which planet is known as the Red Planet?", "options": ["Mars", "Venus", "Jupiter"], "answer": "Mars"},
]

CSV_FILE = "answers.csv"
STATE_FILE = "state.csv"  # store current question index for students

st.set_page_config(page_title="Classroom Quiz", layout="wide")
st.title("📚 Classroom Quiz")

# --- Sidebar: QR code + info ---
app_url = "http://192.168.1.159:8501"  # Change to your hotspot IP
st.sidebar.markdown("## 🔗 Connection Info")
st.sidebar.write("Students: connect to your teacher's Wi-Fi hotspot, then open:")
st.sidebar.code(app_url)
qr_buf = make_qr_image(app_url)
st.sidebar.image(qr_buf, caption="📱 Scan to join", use_container_width=True)

mode = st.sidebar.radio("Select mode:", ["Student", "Teacher"])

# --- Helper functions ---
def read_answers():
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Student", "Question", "Answer"])

def append_answer(student, question, answer):
    df = read_answers()
    # Prevent multiple submissions for same question
    if not ((df["Student"] == student) & (df["Question"] == question)).any():
        df = pd.concat([df, pd.DataFrame([{"Student": student, "Question": question, "Answer": answer}])], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

def read_current_question():
    if os.path.exists(STATE_FILE):
        df = pd.read_csv(STATE_FILE)
        if not df.empty:
            return int(df.loc[0, "current_question"])
    return 0

def write_current_question(q_index):
    pd.DataFrame([{"current_question": q_index}]).to_csv(STATE_FILE, index=False)

def reset_quiz():
    # Clear answers
    pd.DataFrame(columns=["Student", "Question", "Answer"]).to_csv(CSV_FILE, index=False)
    # Reset question index
    write_current_question(0)
    # Clear session state
    for key in ["current_question"]:
        if key in st.session_state:
            del st.session_state[key]

# --- Student View ---
if mode == "Student":
    st_autorefresh(interval=2000, limit=None, key="student_refresh")

    student_name = st.text_input("✏️ Enter your name to start:")

    if student_name:
        q_index = read_current_question()
        q = quiz[q_index]

        st.subheader(f"📝 Question {q_index + 1}")
        st.write(q["q"])

        key = f"{student_name}_q{q_index}"
        selected = st.radio("Choose your answer:", q["options"], index=0, key=key)

        if st.button("✅ Submit Answer", key=f"submit_{key}"):
            append_answer(student_name, q["q"], selected)
            st.success("Answer submitted!")

# --- Teacher View ---
elif mode == "Teacher":
    password = st.text_input("🔑 Enter teacher password:", type="password")

    if password == "secret123":  # Change password
        st_autorefresh(interval=5000, limit=None, key="teacher_refresh")

        # Reset button
        if st.button("🔄 Reset Quiz"):
            reset_quiz()
            st.success("Quiz has been reset. Students can start fresh.")

        if "current_question" not in st.session_state:
            st.session_state["current_question"] = read_current_question()
        q_index = st.session_state["current_question"]

        col_left, col_right = st.columns([1, 2])

        # --- Left column: students logged in ---
        with col_left:
            st.subheader("👥 Students Logged In")
            df = read_answers()
            students = df["Student"].unique()
            if len(students) > 0:
                for s in students:
                    st.write(f"- {s}")
            else:
                st.write("No students yet")

        # --- Right column: current question + aggregated responses ---
        with col_right:
            if q_index < len(quiz):
                q = quiz[q_index]
                st.subheader(f"👩‍🏫 Question {q_index + 1}")
                st.write(f"**{q['q']}**")
                st.write("Options:", q["options"])

                if not df.empty:
                    df_q = df[df["Question"] == q["q"]]
                    total_responses = len(df_q)
                    st.write(f"📝 Total responses: {total_responses}")

                    if total_responses > 0:
                        counts = df_q['Answer'].value_counts()
                        percentages = counts / total_responses * 100

                        # Collapsible container
                        with st.expander("📊 Show Answer Percentages", expanded=False):
                            st.write("### Percentages")
                            for option in q["options"]:
                                pct = percentages.get(option, 0)
                                st.write(f"- {option}: {pct:.1f}%")
                            st.bar_chart(percentages.reindex(q["options"]).fillna(0))
                    else:
                        st.info("No responses yet.")
                else:
                    st.info("No responses yet.")

                # Teacher navigation
                col1, col2 = st.columns(2)
                if col1.button("⏮ Previous") and q_index > 0:
                    st.session_state["current_question"] = q_index - 1
                    write_current_question(st.session_state["current_question"])
                if col2.button("⏭ Next") and q_index < len(quiz) - 1:
                    st.session_state["current_question"] = q_index + 1
                    write_current_question(st.session_state["current_question"])
            else:
                st.subheader("✅ Quiz complete!")
                if not df.empty:
                    st.dataframe(df)
                    csv = df.to_csv().encode("utf-8")
                    st.download_button("📥 Download all results as CSV", csv, "quiz_results.csv", "text/csv")

    elif password:
        st.error("❌ Incorrect password")
