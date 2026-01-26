import streamlit as st
import time

st.set_page_config(page_title="Scripture Jeopardy", layout="wide")

# ---------------------------------------------------------
# YOUR QUESTIONS (EXACTLY AS PROVIDED)
# ---------------------------------------------------------
categories = {
    "Old Testament": {
        100: {"q": "This man built an ark to save his family and animals from the flood.", "a": "Who is Noah?"},
        200: {"q": "This prophet parted the Red Sea to help the Israelites escape Egypt.", "a": "Who is Moses?"},
        300: {"q": "This young shepherd boy defeated the giant Goliath with a sling and stone.", "a": "Who is David?"},
        400: {"q": "This prophet was taken up to heaven in a whirlwind without dying.", "a": "Who is Elijah?"},
        500: {"q": "This book contains the Ten Commandments given to Moses.", "a": "What is Exodus?"}
    },
    "New Testament": {
        100: {"q": "This is where Jesus was born.", "a": "What is Bethlehem?"},
        200: {"q": "This apostle denied knowing Jesus three times before the crucifixion.", "a": "Who is Peter?"},
        300: {"q": "This is the number of apostles Jesus originally called.", "a": "What is twelve?"},
        400: {"q": "This apostle was known as 'doubting' because he needed to see Jesus's wounds.", "a": "Who is Thomas?"},
        500: {"q": "This is the mountain where Jesus gave the Sermon on the Mount.", "a": "What is the Mount of Beatitudes (or Mount of Olives)?"}
    },
    "Book of Mormon": {
        100: {"q": "This prophet wrote the first book in the Book of Mormon.", "a": "Who is Nephi?"},
        200: {"q": "This is the name of Lehi's rebellious son.", "a": "Who is Laman?"},
        300: {"q": "This prophet buried the golden plates in the Hill Cumorah.", "a": "Who is Moroni?"},
        400: {"q": "This king gave up his throne to serve God and became a great missionary.", "a": "Who is King Mosiah (or Alma)?"},
        500: {"q": "This is the city where Jesus appeared to the Nephites.", "a": "What is Bountiful?"}
    },
    "Doctrine & Covenants": {
        100: {"q": "This section contains the Word of Wisdom.", "a": "What is Section 89?"},
        200: {"q": "This is the age when young men can receive the Aaronic Priesthood.", "a": "What is 12?"},
        300: {"q": "This section describes the three degrees of glory.", "a": "What is Section 76?"},
        400: {"q": "This section contains the law of tithing.", "a": "What is Section 119?"},
        500: {"q": "This section describes the organization of the First Presidency and Twelve Apostles.", "a": "What is Section 107?"}
    },
    "Church History": {
        100: {"q": "This is the year the Church was organized.", "a": "What is 1830?"},
        200: {"q": "This is where Joseph Smith received the First Vision.", "a": "What is the Sacred Grove?"},
        300: {"q": "This angel appeared to Joseph Smith to tell him about the golden plates.", "a": "Who is Moroni?"},
        400: {"q": "This is the first temple built in this dispensation.", "a": "What is the Kirtland Temple?"},
        500: {"q": "This prophet led the saints to Utah after Joseph Smith's death.", "a": "Who is Brigham Young?"}
    },
    "Gospel Principles": {
        100: {"q": "This is the first principle of the gospel.", "a": "What is faith?"},
        200: {"q": "This ordinance is required for entrance into the celestial kingdom.", "a": "What is baptism?"},
        300: {"q": "This is the gift received after baptism and confirmation.", "a": "What is the gift of the Holy Ghost?"},
        400: {"q": "This principle allows us to be forgiven of our sins.", "a": "What is repentance?"},
        500: {"q": "This is the highest degree of glory in the celestial kingdom.", "a": "What is exaltation?"}
    }
}

# ---------------------------------------------------------
# SESSION STATE INIT
# ---------------------------------------------------------
if "team_scores" not in st.session_state:
    st.session_state.team_scores = {}

if "num_teams" not in st.session_state:
    st.session_state.num_teams = 2

if "current_team" not in st.session_state:
    st.session_state.current_team = 0

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "answered_questions" not in st.session_state:
    st.session_state.answered_questions = set()

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

if "timer_start" not in st.session_state:
    st.session_state.timer_start = None

if "timer_running" not in st.session_state:
    st.session_state.timer_running = False

TIMER_DURATION = 20


# ---------------------------------------------------------
# TIMER FUNCTIONS
# ---------------------------------------------------------
def start_timer():
    st.session_state.timer_start = time.time()
    st.session_state.timer_running = True


def stop_timer():
    st.session_state.timer_running = False


def get_time_left():
    if not st.session_state.timer_running or st.session_state.timer_start is None:
        return TIMER_DURATION
    elapsed = time.time() - st.session_state.timer_start
    return max(0, TIMER_DURATION - int(elapsed))


# ---------------------------------------------------------
# TEAM SETUP
# ---------------------------------------------------------
st.sidebar.header("Team Setup")
st.session_state.num_teams = st.sidebar.number_input("Number of Teams", 1, 10, st.session_state.num_teams)

for i in range(st.session_state.num_teams):
    if i not in st.session_state.team_scores:
        st.session_state.team_scores[i] = 0

st.sidebar.write("Scores:")
for team, score in st.session_state.team_scores.items():
    st.sidebar.write(f"Team {team + 1}: {score}")


# ---------------------------------------------------------
# GAME BOARD (JEOPARDY GRID)
# ---------------------------------------------------------
st.title("📘 Scripture Jeopardy — Teacher Control")

if st.session_state.current_question is None:
    cols = st.columns(len(categories))

    for idx, (cat, values) in enumerate(categories.items()):
        with cols[idx]:
            st.markdown(f"### {cat}")
            for points, qa in values.items():
                disabled = (cat, points) in st.session_state.answered_questions
                if st.button(f"${points}", key=f"{cat}-{points}", disabled=disabled):
                    st.session_state.current_question = (cat, points)
                    st.session_state.show_answer = False
                    start_timer()
                    st.rerun()


# ---------------------------------------------------------
# QUESTION DISPLAY
# ---------------------------------------------------------
if st.session_state.current_question:
    cat, points = st.session_state.current_question
    qdata = categories[cat][points]

    st.markdown(f"## {cat} — ${points}")
    st.markdown(f"### {qdata['q']}")

    # Timer
    time_left = get_time_left()
    st.markdown(f"# ⏱️ {time_left}")

    if time_left == 0:
        stop_timer()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("✅ Correct"):
            st.session_state.team_scores[st.session_state.current_team] += points
            st.session_state.answered_questions.add((cat, points))
            st.session_state.show_answer = True
            st.rerun()

    with col2:
        if st.button("❌ Wrong"):
            st.session_state.team_scores[st.session_state.current_team] -= points
            st.session_state.current_team = (st.session_state.current_team + 1) % st.session_state.num_teams
            st.session_state.show_answer = True
            st.rerun()

    with col3:
        if st.button("👁️ Show Answer"):
            st.session_state.show_answer = True
            st.rerun()

    if st.session_state.show_answer:
        st.markdown(f"### ✅ Answer: {qdata['a']}")

        if st.button("➡️ Next Question"):
            st.session_state.current_question = None
            st.session_state.show_answer = False
            st.session_state.current_team = (st.session_state.current_team + 1) % st.session_state.num_teams
            st.rerun()

    if st.session_state.timer_running:
        st.rerun()
