import streamlit as st
import random
import time

st.set_page_config(page_title="Scripture Wheel", layout="wide")

# ---------------------------------------------------------
# CONFIGURATION & PUZZLE BANK
# ---------------------------------------------------------
TEAM_NAMES = ["Team 1", "Team 2", "Team 3", "Team 4"]
TEAM_COLORS = ["#3b82f6", "#ef4444", "#22c55e", "#a855f7"]

PUZZLE_BANK = [
    {"category": "Verse", "text": "IN THE BEGINNING GOD CREATED THE HEAVENS AND THE EARTH"},
    {"category": "Verse", "text": "I CAN DO ALL THINGS THROUGH CHRIST WHO STRENGTHENS ME"},
    {"category": "Person", "text": "JOHN THE BAPTIST"},
    {"category": "Place", "text": "GARDEN OF EDEN"},
    {"category": "Phrase", "text": "FRUIT OF THE SPIRIT"},
    {"category": "Miracle", "text": "WALKING ON WATER"},
    {"category": "Commandment", "text": "HONOR YOUR FATHER AND MOTHER"},
]

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
if "w_team_scores" not in st.session_state:
    st.session_state.w_team_scores = [0, 0, 0, 0]

if "w_current_team" not in st.session_state:
    st.session_state.w_current_team = 0

if "w_puzzle" not in st.session_state:
    st.session_state.w_puzzle = None

if "w_guessed_letters" not in st.session_state:
    st.session_state.w_guessed_letters = set()

if "w_revealed" not in st.session_state:
    st.session_state.w_revealed = False

# ---------------------------------------------------------
# GAME LOGIC
# ---------------------------------------------------------
def start_new_round():
    puzzle_obj = random.choice(PUZZLE_BANK)
    st.session_state.w_puzzle = puzzle_obj
    st.session_state.w_guessed_letters = set()
    st.session_state.w_revealed = False

def guess_letter(letter):
    st.session_state.w_guessed_letters.add(letter)
    
    phrase = st.session_state.w_puzzle["text"].upper()
    count = phrase.count(letter)
    
    if count > 0:
        points = count * 100
        st.session_state.w_team_scores[st.session_state.w_current_team] += points
        
        unique_chars = set(c for c in phrase if c.isalpha())
        if unique_chars.issubset(st.session_state.w_guessed_letters):
            st.session_state.w_revealed = True
            st.balloons()

def solve_puzzle(guess_text):
    target = st.session_state.w_puzzle["text"].upper()
    if guess_text.upper().strip() == target.strip():
        st.session_state.w_team_scores[st.session_state.w_current_team] += 500
        st.session_state.w_revealed = True
        for char in target:
            if char.isalpha():
                st.session_state.w_guessed_letters.add(char)
        st.balloons()
    else:
        st.error("Incorrect solve attempt!")

# ---------------------------------------------------------
# UI COMPONENTS
# ---------------------------------------------------------
st.title("🎡 Scripture Wheel")

# --- Top Bar: Controls ---
c1, c2 = st.columns([3, 1])
with c1:
    if st.button("🔄 New Puzzle"):
        start_new_round()
        st.rerun()
with c2:
    if st.button("👀 Reveal Answer"):
        st.session_state.w_revealed = True
        st.rerun()

if not st.session_state.w_puzzle:
    start_new_round()
    st.rerun()

st.markdown("---")

# --- Scoreboard ---
cols = st.columns(4)
for i in range(4):
    is_active = (i == st.session_state.w_current_team)
    border = "4px solid white" if is_active else f"2px solid {TEAM_COLORS[i]}"
    bg = TEAM_COLORS[i] if is_active else "transparent"
    text_color = "white" if is_active else TEAM_COLORS[i]
    
    with cols[i]:
        st.markdown(
            f"""
            <div style="
                border: {border};
                background-color: {bg};
                color: {text_color};
                border-radius: 10px;
                padding: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 1.2rem;
            ">
                {TEAM_NAMES[i]}<br>
                <span style="font-size: 1.5rem">${st.session_state.w_team_scores[i]}</span>
            </div>
            """, 
            unsafe_allow_html=True
        )
        if st.button(f"Select {TEAM_NAMES[i]}", key=f"sel_team_{i}"):
            st.session_state.w_current_team = i
            st.rerun()

st.markdown("---")

# --- The Puzzle Board ---
category = st.session_state.w_puzzle["category"]

# FIX: Normalize puzzle text to remove newlines, tabs, double spaces
raw_text = st.session_state.w_puzzle["text"].upper()
text = " ".join(raw_text.split())

st.subheader(f"Category: {category}")

board_html = """
<div style="
    display: flex; 
    flex-wrap: wrap; 
    gap: 10px; 
    justify-content: center; 
    margin: 20px 0;
">
"""

for char in text:
    if char == " ":
        board_html += '<div style="width: 40px;"></div>'
    elif not char.isalpha():
        board_html += f"""
            <div style="
                width: 50px; height: 60px; 
                display: flex; align-items: center; justify-content: center;
                font-size: 2rem; font-weight: bold; color: white;
            ">{char}</div>
        """
    else:
        is_visible = (char in st.session_state.w_guessed_letters) or st.session_state.w_revealed
        display_char = char if is_visible else ""
        bg_color = "#3b82f6" if is_visible else "#334155"
        
        board_html += f"""
            <div style="
                width: 50px; height: 60px; 
                background-color: {bg_color}; 
                border-radius: 5px;
                display: flex; align-items: center; justify-content: center;
                font-size: 2.5rem; font-weight: bold; color: white;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            ">{display_char}</div>
        """

board_html += "</div>"
st.markdown(board_html, unsafe_allow_html=True)

st.markdown("---")

# --- Keyboard & Controls ---
col_left, col_right = st.columns([2, 1])

with col_left:
    st.write("### Guess a Letter")
    rows = [
        "ABCDEFGHI",
        "JKLMNOPQR",
        "STUVWXYZ"
    ]
    
    for row_chars in rows:
        c_cols = st.columns(len(row_chars))
        for idx, char in enumerate(row_chars):
            with c_cols[idx]:
                disabled = (char in st.session_state.w_guessed_letters) or st.session_state.w_revealed
                if st.button(char, key=f"btn_{char}", disabled=disabled):
                    guess_letter(char)
                    st.rerun()

with col_right:
    st.write("### Solve the Puzzle")
    with st.form("solve_form"):
        solve_attempt = st.text_input("Enter the full phrase:")
        submitted = st.form_submit_button("SOLVE!")
        if submitted:
            solve_puzzle(solve_attempt)
            st.rerun()

    st.info("Scoring: 100 points per letter found. 500 points bonus for solving.")

# --- Confetti on Win ---
if st.session_state.w_revealed:
    st.success(f"Puzzle Solved! The phrase was: {st.session_state.w_puzzle['text']}")
    if st.button("Next Puzzle ➡️"):
        start_new_round()
        st.rerun()
