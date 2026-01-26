import streamlit as st
import random
import time

# --- Page Setup ---
st.set_page_config(page_title="Scripture Jeopardy", layout="wide")

st.markdown("""
<style>
.jeopardy-board { 
    display: grid; 
    gap: 10px; 
    margin: 20px 0; 
}
.category-header { 
    background: #1f4e79; 
    color: white; 
    padding: 15px; 
    text-align: center; 
    font-weight: bold; 
    font-size: 18px;
    border-radius: 5px;
}
.point-button { 
    background: #2e5984; 
    color: white; 
    padding: 20px; 
    text-align: center; 
    font-size: 24px; 
    font-weight: bold; 
    border: none; 
    border-radius: 5px; 
    cursor: pointer;
    min-height: 80px;
}
.point-button:hover { background: #3d6fa3; }
.answered { 
    background: #666 !important; 
    color: #999 !important; 
    cursor: not-allowed !important;
}
.team-score { 
    font-size: 24px; 
    font-weight: bold; 
    text-align: center; 
    padding: 15px;
    border-radius: 10px;
    margin: 10px;
}
.current-team { 
    border: 3px solid #FFD700; 
    box-shadow: 0 0 15px rgba(255, 215, 0, 0.5);
}
.question-display {
    background: #f0f2f6;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    font-size: 20px;
    margin: 20px 0;
}
.answer-display {
    background: #e8f5e8;
    padding: 20px;
    border-radius: 10px;
    text-align: center;
    font-size: 18px;
    margin: 10px 0;
    border-left: 5px solid #28a745;
}
</style>
""", unsafe_allow_html=True)

# --- Game Data ---
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

# --- Initialize Game State ---
if "jeopardy_initialized" not in st.session_state:
    st.session_state.jeopardy_initialized = False

def initialize_game():
    st.session_state.answered_questions = set()
    st.session_state.current_question = None
    st.session_state.show_answer = False
    st.session_state.team_scores = [0] * st.session_state.num_teams
    st.session_state.current_team = 0
    st.session_state.question_value = 0
    st.session_state.jeopardy_initialized = True

# --- Sidebar Setup ---
st.sidebar.header("🎯 Game Setup")
st.session_state.num_teams = st.sidebar.slider("Number of teams:", 2, 6, 3, step=1)

# Team colors
team_colors = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400", "#9C27B0", "#FF9800"]

if st.sidebar.button("🔁 Start New Game") or not st.session_state.jeopardy_initialized:
    initialize_game()
    st.rerun()

# --- Main Game Display ---
st.title("📚 Scripture Jeopardy")

# Display team scores
st.markdown("### Team Scores")
score_cols = st.columns(st.session_state.num_teams)
for i in range(st.session_state.num_teams):
    with score_cols[i]:
        team_class = "current-team" if i == st.session_state.current_team else ""
        color = team_colors[i % len(team_colors)]
        st.markdown(f"""
        <div class='team-score {team_class}' style='background-color: {color}20; border: 2px solid {color}'>
            <div style='color: {color}'>Team {i+1}</div>
            <div style='color: {color}; font-size: 28px'>${st.session_state.team_scores[i]}</div>
        </div>
        """, unsafe_allow_html=True)

# Current team indicator
st.markdown(f"### 🎯 Current Team: **Team {st.session_state.current_team + 1}**")

# Display current question if one is selected
if st.session_state.current_question:
    category, points = st.session_state.current_question
    question_data = categories[category][points]
    
    st.markdown(f"### Category: {category} - ${points}")
    st.markdown(f"""
    <div class='question-display'>
        <strong>Question:</strong><br>
        {question_data['q']}
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("✅ Correct Answer", key="correct"):
            st.session_state.team_scores[st.session_state.current_team] += points
            st.session_state.answered_questions.add((category, points))
            st.session_state.show_answer = True
            st.rerun()
    
    with col2:
        if st.button("❌ Wrong Answer", key="wrong"):
            st.session_state.team_scores[st.session_state.current_team] -= points
            st.session_state.current_team = (st.session_state.current_team + 1) % st.session_state.num_teams
            st.session_state.show_answer = True
            st.rerun()
    
    with col3:
        if st.button("👁️ Show Answer", key="show_answer"):
            st.session_state.show_answer = True
            st.rerun()
    
    if st.session_state.show_answer:
        st.markdown(f"""
        <div class='answer-display'>
            <strong>Answer:</strong> {question_data['a']}
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("➡️ Next Question", key="next"):
            st.session_state.current_question = None
            st.session_state.show_answer = False
            st.session_state.current_team = (st.session_state.current_team + 1) % st.session_state.num_teams
            st.rerun()

else:
    # Display the Jeopardy board
    st.markdown("### Game Board")
    
    # Create the board layout
    board_cols = st.columns(len(categories))
    
    # Category headers
    for i, category in enumerate(categories.keys()):
        with board_cols[i]:
            st.markdown(f"<div class='category-header'>{category}</div>", unsafe_allow_html=True)
    
    # Point values and questions
    for points in [100, 200, 300, 400, 500]:
        point_cols = st.columns(len(categories))
        for i, category in enumerate(categories.keys()):
            with point_cols[i]:
                if (category, points) in st.session_state.answered_questions:
                    st.markdown(f"<div class='point-button answered'>${points}</div>", unsafe_allow_html=True)
                else:
                    if st.button(f"${points}", key=f"{category}_{points}"):
                        st.session_state.current_question = (category, points)
                        st.session_state.question_value = points
                        st.session_state.show_answer = False
                        st.rerun()

# Game completion check
total_questions = len(categories) * 5
answered_questions = len(st.session_state.answered_questions)

if answered_questions == total_questions:
    st.success("🎉 Game Complete!")
    winner_score = max(st.session_state.team_scores)
    winners = [i+1 for i, score in enumerate(st.session_state.team_scores) if score == winner_score]
    
    if len(winners) == 1:
        st.info(f"🏆 Winner: Team {winners[0]} with ${winner_score}!")
    else:
        st.info(f"🏆 Tie between Teams {', '.join(map(str, winners))} with ${winner_score} each!")

# Progress indicator
progress = answered_questions / total_questions
st.progress(progress)
st.caption(f"Questions answered: {answered_questions}/{total_questions}")

# Manual team switching (in case needed)
st.sidebar.markdown("---")
st.sidebar.markdown("### Manual Controls")
if st.sidebar.button("⏭️ Skip to Next Team"):
    st.session_state.current_team = (st.session_state.current_team + 1) % st.session_state.num_teams
    st.rerun()

# Reset current question
if st.sidebar.button("🔄 Clear Current Question"):
    st.session_state.current_question = None
    st.session_state.show_answer = False
    st.rerun()
