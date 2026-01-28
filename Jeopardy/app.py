import streamlit as st
import random
from question_bank import question_bank
from collections import defaultdict

st.set_page_config(layout="wide")
#v 3.1
# ---------------------------------------------------------
# 1. Select 25 random questions once per game
# ---------------------------------------------------------
if "game_questions" not in st.session_state:
    st.session_state.game_questions = random.sample(question_bank, 25)

selected_questions = st.session_state.game_questions

# ---------------------------------------------------------
# 2. Group questions by category
# ---------------------------------------------------------
def group_by_category(questions):
    grouped = defaultdict(list)
    for q in questions:
        grouped[q["category"]].append(q)
    return grouped

grouped = group_by_category(selected_questions)

# ---------------------------------------------------------
# 3. Ensure exactly 5 categories (take first 5 if more)
# ---------------------------------------------------------
# If your question bank is well-balanced, this will always be 5.
final_categories = dict(list(grouped.items())[:5])

# ---------------------------------------------------------
# 4. Convert grouped questions into Jeopardy board format
# ---------------------------------------------------------
def format_for_board(categories):
    board = {}
    for cat, qs in categories.items():
        board[cat] = {}
        # Take first 5 questions for this category
        for i, q in enumerate(qs[:5]):
            points = str((i + 1) * 100)
            board[cat][points] = {
                "q": q["q"],
                "a": q["a"]
            }
    return board

categories = format_for_board(final_categories)

# ---------------------------------------------------------
# 5. Display the Jeopardy board
# ---------------------------------------------------------
st.title("Scripture Mastery Jeopardy")

cols = st.columns(5)

for col_index, (cat_name, questions) in enumerate(categories.items()):
    with cols[col_index]:
        st.header(cat_name)
        for value, qa in questions.items():
            button_key = f"{cat_name}-{value}"

            if st.button(value, key=button_key):
                st.session_state["current_question"] = qa["q"]
                st.session_state["current_answer"] = qa["a"]
                st.session_state["current_value"] = value
                st.session_state["current_category"] = cat_name

# ---------------------------------------------------------
# 6. Show selected question + answer reveal
# ---------------------------------------------------------
if "current_question" in st.session_state:
    st.subheader(f"Question for {st.session_state['current_value']} points")
    st.write(st.session_state["current_question"])

    if st.button("Show Answer"):
        st.success(st.session_state["current_answer"])

# ---------------------------------------------------------
# 7. Reset game button
# ---------------------------------------------------------
if st.button("New Game"):
    st.session_state.clear()
    st.rerun()
