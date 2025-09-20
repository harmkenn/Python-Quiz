import streamlit as st
import pandas as pd
import os
import time
from io import BytesIO

# --- Files ---
QUESTIONS_FILE = "questions.csv"
CSV_FILE = "answers.csv"
STATE_FILE = "state.csv"

# --- Helpers for CSV persistence ---
def read_questions():
    if os.path.exists(QUESTIONS_FILE) and os.path.getsize(QUESTIONS_FILE) > 0:
        return pd.read_csv(QUESTIONS_FILE)
    else:
        return pd.DataFrame(columns=["q", "type", "choices", "answer"])

def save_questions(df):
    df.to_csv(QUESTIONS_FILE, index=False)

def read_answers():
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=["Student", "Question", "Answer", "TimeTaken"])

def save_answers(df):
    df.to_csv(CSV_FILE, index=False)

def append_answer(student, question, answer, time_taken):
    df = read_answers()
    if not ((df["Student"] == student) & (df["Question"] == question)).any():
        df = pd.concat(
            [df, pd.DataFrame([{
                "Student": student,
                "Question": question,
                "Answer": answer,
                "TimeTaken": time_taken
            }])],
            ignore_index=True
        )
        save_answers(df)

def read_state():
    if os.path.exists(STATE_FILE) and os.path.getsize(STATE_FILE) > 0:
        return pd.read_csv(STATE_FILE).to_dict(orient="records")[0]
    else:
        return {"index": 0, "show_answer": False, "start_time": 0}

def save_state(state):
    pd.DataFrame([state]).to_csv(STATE_FILE, index=False)

def reset_all():
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

# --- Quiz flow helpers ---
def calculate_scores(df, quiz):
    scores = {}
    for student in df["Student"].unique():
        student_df = df[df["Student"] == student]
        correct_count = 0
        total_time = 0.0

        for _, row in student_df.iterrows():
            q_text = row["Question"]
            q_match = next((q for q in quiz if q["q"] == q_text), None)
            if q_match and q_match["type"] == "MC":
                if str(row["Answer"]).strip() == q_match["answer"]:
                    correct_count += 1
            total_time += float(row["TimeTaken"]) if "TimeTaken" in row else 0

        scores[student] = {"correct": correct_count, "time": round(total_time, 2)}
    return scores

def export_scores(scores):
    df = pd.DataFrame([
        {"Student": s, "Correct": d["correct"], "TotalTime": d["time"]}
        for s, d in scores.items()
    ])
    buffer = BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer

# --- Streamlit App ---
st.title("📊 Quiz App with Speed Scoring")

mode = st.sidebar.radio("Mode", ["Teacher", "Student"])

# ---------------- Teacher Mode ----------------
if mode == "Teacher":
    st.header("👩‍🏫 Teacher Dashboard")

    if st.button("Reset Quiz"):
        reset_all()
        st.success("Quiz reset!")

    # Manage quiz questions
    st.subheader("Manage Questions")
    questions_df = read_questions()

    with st.form("add_question"):
        q_text = st.text_input("Question")
        q_type = st.selectbox("Type", ["MC", "TF"])
        if q_type == "MC":
            q_choices = st.text_input("Choices (comma-separated)")
            q_answer = st.text_input("Correct Answer")
        else:
            q_choices = "True,False"
            q_answer = st.selectbox("Correct Answer", ["True", "False"])
        submitted = st.form_submit_button("Add Question")
        if submitted:
            new_row = {"q": q_text, "type": q_type, "choices": q_choices, "answer": q_answer}
            questions_df = pd.concat([questions_df, pd.DataFrame([new_row])], ignore_index=True)
            save_questions(questions_df)
            st.success("Question added!")

    st.dataframe(questions_df)

    # Quiz control
    st.subheader("Quiz Control")
    state = read_state()
    quiz = questions_df.to_dict(orient="records")

    if quiz:
        q_index = state["index"]
        if q_index < len(quiz):
            q = quiz[q_index]
            st.write(f"**Q{q_index+1}:** {q['q']}")

            if st.button("Next Question"):
                state["index"] += 1
                state["show_answer"] = False
                state["start_time"] = time.time()
                save_state(state)

            if st.button("Show Answer"):
                state["show_answer"] = True
                save_state(state)

            if state["show_answer"]:
                st.info(f"Answer: {q['answer']}")
        else:
            st.success("Quiz finished!")

    # Scores
    st.subheader("Scores")
    df = read_answers()
    scores = calculate_scores(df, quiz)
    for student, data in scores.items():
        st.write(f"- {student} ✅ {data['correct']} correct | ⏱ {data['time']} sec")

    if scores:
        csv_file = export_scores(scores)
        st.download_button("Download Scores CSV", data=csv_file, file_name="scores.csv", mime="text/csv")

# ---------------- Student Mode ----------------
else:
    st.header("🧑‍🎓 Student View")

    student_name = st.text_input("Your Name")
    state = read_state()
    quiz = read_questions().to_dict(orient="records")

    if student_name and quiz and state["index"] < len(quiz):
        q = quiz[state["index"]]
        st.write(f"**Q{state['index']+1}:** {q['q']}")

        if q["type"] == "MC":
            choices = q["choices"].split(",")
            ans = st.radio("Choose:", choices)
        else:
            ans = st.radio("Choose:", ["True", "False"])

        if st.button("Submit"):
            elapsed = round(time.time() - state.get("start_time", time.time()), 2)
            append_answer(student_name, q["q"], ans, elapsed)
            st.success(f"Answer submitted in {elapsed} sec!")

    elif student_name:
        st.success("Quiz finished! 🎉")
