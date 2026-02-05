import streamlit as st
import random
import time
from puzzle_bank import PUZZLE_BANK  # Import the puzzle bank from the external file

st.set_page_config(page_title="Scripture Wheel", layout="wide")
#V1.3
# ---------------------------------------------------------
# CONFIGURATION & PUZZLE BANK
# ---------------------------------------------------------
TEAM_NAMES = ["Team 1", "Team 2", "Team 3", "Team 4"]
TEAM_COLORS = ["#3b82f6", "#ef4444", "#22c55e", "#a855f7"]

VOWEL_COST = 200  # Cost to buy a vowel
RANDOM_VALUES = [100, 200, 300, 400, 500]  # Possible random point values

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

if "w_random_value" not in st.session_state:
    st.session_state.w_random_value = None

# ---------------------------------------------------------
# GAME LOGIC
# ---------------------------------------------------------
def start_new_round():
    puzzle_obj = random.choice(PUZZLE_BANK)
    st.session_state.w_puzzle = puzzle_obj
    st.session_state.w_guessed_letters = set()
    st.session_state.w_revealed = False
    st.session_state.w_random_value = None

def spin_random_value():
    st.session_state.w_random_value = random.choice(RANDOM_VALUES)

def guess_letter(letter):
    # Check if the random value has been spun
    if st.session_state.w_random_value is None:
        st.error("Spin for a random value first!")
        return

    # Check if the letter is a vowel
    if letter in "AEIOU":
        # Ensure the team has enough money to buy the vowel
        if st.session_state.w_team_scores[st.session_state.w_current_team] < VOWEL_COST:
            st.error("Not enough money to buy a vowel!")
            return
        else:
            # Deduct the cost of the vowel
            st.session_state.w_team_scores[st.session_state.w_current_team] -= VOWEL_COST

    # Add the guessed letter to the set of guessed letters
    st.session_state.w_guessed_letters.add(letter)
    
    # Check occurrences of the letter in the puzzle
    phrase = st.session_state.w_puzzle["text"].upper()
    count = phrase.count(letter)
    
    if count > 0:
        # Award points based on the random value
        points = count * st.session_state.w_random_value
        st.session_state.w_team_scores[st.session_state.w_current_team] += points
        
        # Check if all letters have been guessed
        unique_chars = set(c for c in phrase if c.isalpha())
        if unique_chars.issubset(st.session_state.w_guessed_letters):
            st.session_state.w_revealed = True
            st.balloons()
    else:
        # If the letter does not exist, cycle to the next team
        st.warning(f"Letter '{letter}' is not in the puzzle. Next team's turn!")
        st.session_state.w_current_team = (st.session_state.w_current_team + 1) % len(TEAM_NAMES)

    # Reset random value after guessing
    st.session_state.w_random_value = None

def solve_puzzle(guess_text):
    # Normalize both target and guess to handle whitespace consistently
    target = " ".join(st.session_state.w_puzzle["text"].upper().split())
    guess = " ".join(guess_text.upper().split())
    if guess == target:
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

# --- Random Value Spinner ---
st.write("### Spin for a Random Value")
if st.button("🎰 Spin Random Value"):
    spin_random_value()
    st.rerun()

if st.session_state.w_random_value is not None:
    st.success(f"Random Value: {st.session_state.w_random_value}")

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
    gap: 20px; 
    justify-content: center; 
    margin: 20px 0;
">
"""

# Split text into words to prevent line breaks inside words
words = text.split(" ")

for word in words:
    board_html += '<div style="display: flex; gap: 5px;">'
    for char in word:
        if not char.isalpha():
            board_html += f'<div style="width: 50px; height: 60px; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold; color: white;">{char}</div>'
        else:
            is_visible = (char in st.session_state.w_guessed_letters) or st.session_state.w_revealed
            display_char = char if is_visible else ""
            bg_color = "#3b82f6" if is_visible else "#334155"
            
            board_html += f'<div style="width: 50px; height: 60px; background-color: {bg_color}; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: bold; color: white; box-shadow: 2px 2px 5px rgba(0,0,0,0.3);">{display_char}</div>'
    board_html += '</div>'

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
                # Disable button if letter is already guessed or puzzle is revealed
                disabled = (char in st.session_state.w_guessed_letters) or st.session_state.w_revealed
                
                # Add a label for vowels to indicate cost
                label = f"{char} ($200)" if char in "AEIOU" else char
                
                if st.button(label, key=f"btn_{char}", disabled=disabled):
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

    st.info("Scoring: Random value determines points per letter. 500 points bonus for solving.")

# --- Confetti on Win ---
if st.session_state.w_revealed:
    st.success(f"Puzzle Solved! The phrase was: {st.session_state.w_puzzle['text']}")
    if st.button("Next Puzzle ➡️"):
        start_new_round()
        st.rerun()
