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

# --- Streamlit App ---
st.set_page_config(page_title="Classroom Quiz", layout="wide")
st.title("📚 Classroom Quiz")

# --- Sidebar: QR code + info ---
app_url = "http://192.168.1.159:8501"  # Change to your hotspot IP
st.sidebar.markdown("## 🔗 Connection Info")
st.sidebar.write("Students: connect to your teacher's Wi-Fi hotspot, then open:")
st.sidebar.code(app_url)

qr_buf = make_qr_image(app_url)
st.sidebar.image(qr_buf, caption="📱 Scan to join", use_container_width=True)

# --- Mode selection ---
mode = st.sidebar.radio("Select mode:", ["Student", "Teacher"])

# --- Helper functions for CSV ---
def read_answers():
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Student", "Question", "Answer"])

def append_answer(student, question, answer):
    df = read_answers()
    df = pd.concat([df, pd.DataFrame([{"Student": student, "Question": question, "Answer": answer}])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# --- Student View ---
if mode == "Student":
    student_name = st.text_input("✏️ Enter your name to start:")

    if student_name:
        q_index = st.sidebar.number_input("Question number", min_value=0, max_value=len(quiz)-1, value=0, step=1)
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

    if password == "secret123":  # <<< Change this password
        # --- Auto-refresh every 5 seconds ---
        st_autorefresh(interval=5000, limit=None, key="teacher_refresh")

        q_index = st.session_state.get("current_question", 0)
        col_left, col_right = st.columns([1, 2])

        # --- Left column: student list ---
        with col_left:
            st.subheader("👥 Students Logged In")
            df = read_answers()
            students = df["Student"].unique()
            if len(students) > 0:
                for s in students:
                    st.write(f"- {s}")
            else:
                st.write("No students yet")

        # --- Right column: Question + responses ---
        with col_right:
            if q_index < len(quiz):
                q = quiz[q_index]
                st.subheader(f"👩‍🏫 Question {q_index + 1}")
                st.write(f"**{q['q']}**")
                st.write("Options:", q["options"])

                if not df.empty:
                    answers = df[df["Question"] == q["q"]].set_index("Student")
                    st.write("### Responses so far")
                    st.dataframe(answers)
                else:
                    st.info("No responses yet.")

                col1, col2 = st.columns(2)
                if col1.button("⏮ Previous") and q_index > 0:
                    st.session_state["current_question"] = q_index - 1
                if col2.button("⏭ Next") and q_index < len(quiz) - 1:
                    st.session_state["current_question"] = q_index + 1
            else:
                st.subheader("✅ Quiz complete!")
                if not df.empty:
                    st.dataframe(df)
                    csv = df.to_csv().encode("utf-8")
                    st.download_button("📥 Download all results as CSV", csv, "quiz_results.csv", "text/csv")

    elif password:
        st.error("❌ Incorrect password")
