import streamlit as st
import random
import time
from puzzle_bank import PUZZLE_BANK  # Import the puzzle bank from the external file

st.set_page_config(page_title="Scripture Wheel", layout="wide")
# v3.9

# ---------------------------------------------------------
# CONFIGURATION & PUZZLE BANK
# ---------------------------------------------------------
TEAM_NAMES = ["Team 1", "Team 2", "Team 3", "Team 4"]
TEAM_COLORS = ["#3b82f6", "#ef4444", "#22c55e", "#a855f7"]

VOWEL_COST = 200  # Cost to buy a vowel
RANDOM_VALUES = [100, 200, 300, 400, 500, "Lose Turn"]  # Possible random point values
TIMER_DURATION = 15  # Timer duration in seconds

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

if "w_day_totals" not in st.session_state:
    st.session_state.w_day_totals = [0, 0, 0, 0]

if "w_timer_start" not in st.session_state:
    st.session_state.w_timer_start = None

if "w_timer_running" not in st.session_state:
    st.session_state.w_timer_running = False

if "w_timer_paused" not in st.session_state:
    st.session_state.w_timer_paused = False

if "w_timer_elapsed" not in st.session_state:
    st.session_state.w_timer_elapsed = 0  # Time elapsed before pausing

# ---------------------------------------------------------
# TIMER LOGIC
# ---------------------------------------------------------
def start_timer():
    st.session_state.w_timer_start = time.time()
    st.session_state.w_timer_running = True
    st.session_state.w_timer_paused = False

def pause_timer():
    if st.session_state.w_timer_running:
        elapsed = time.time() - st.session_state.w_timer_start
        st.session_state.w_timer_elapsed += elapsed
        st.session_state.w_timer_running = False
        st.session_state.w_timer_paused = True

def resume_timer():
    if st.session_state.w_timer_paused:
        st.session_state.w_timer_start = time.time()
        st.session_state.w_timer_running = True
        st.session_state.w_timer_paused = False

def stop_timer():
    st.session_state.w_timer_running = False
    st.session_state.w_timer_paused = False
    st.session_state.w_timer_start = None
    st.session_state.w_timer_elapsed = 0

def get_time_left():
    if st.session_state.w_timer_running:
        elapsed = time.time() - st.session_state.w_timer_start + st.session_state.w_timer_elapsed
    elif st.session_state.w_timer_paused:
        elapsed = st.session_state.w_timer_elapsed
    else:
        elapsed = 0
    return max(0, TIMER_DURATION - int(elapsed))

def timer_color(seconds_left):
    if seconds_left > TIMER_DURATION * 0.6:
        return "#22c55e"
    elif seconds_left > TIMER_DURATION * 0.3:
        return "#eab308"
    else:
        return "#ef4444"

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

def solve_puzzle(correct):
    stop_timer()
    if correct:
        # Award 500 points to the current team
        st.session_state.w_team_scores[st.session_state.w_current_team] += 500
        
        # Add the team's score to their day total (initialize if not present)
        if "w_day_totals" not in st.session_state:
            st.session_state.w_day_totals = [0, 0, 0, 0]
        st.session_state.w_day_totals[st.session_state.w_current_team] += st.session_state.w_team_scores[st.session_state.w_current_team]
        
        # Reset all team scores to zero for the next puzzle
        st.session_state.w_team_scores = [0, 0, 0, 0]
        
        # Mark the puzzle as solved and prepare for the next round
        st.session_state.w_revealed = True
        st.success(f"Team {TEAM_NAMES[st.session_state.w_current_team]} solved the puzzle! Their score has been added to their day total.")
        
        # Display the scriptural reference
        reference = st.session_state.w_puzzle.get("reference", "No reference available")
        st.write(f"**Scriptural Reference:** {reference}")
    else:
        # Cycle to the next team
        st.warning(f"Team {TEAM_NAMES[st.session_state.w_current_team]} guessed incorrectly. Next team's turn!")
        st.session_state.w_current_team = (st.session_state.w_current_team + 1) % len(TEAM_NAMES)

# ---------------------------------------------------------
# UI COMPONENTS
# ---------------------------------------------------------
def app():
    # --- Timer Expiration Check ---
    if st.session_state.get('w_timer_running', False) and get_time_left() <= 0:
        stop_timer()
        st.toast("Time's up! Next team's turn.", icon="⏳")
        st.session_state.w_current_team = (st.session_state.w_current_team + 1) % len(TEAM_NAMES)
        st.session_state.w_random_value = None
        time.sleep(0.5)  # Let toast appear before rerun
        st.rerun()

    # --- Timer Display ---
    timer_placeholder = st.empty()
    time_left = get_time_left()
    color = timer_color(time_left)
    timer_placeholder.markdown(
        f"""
        <div style="
            font-size:3rem; font-weight:800; text-align:center; padding:0.5rem 1rem;
            border-radius:1rem; margin:1rem auto; background-color:{color}; color:white;
        ">
            {time_left}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # --- Timer Controls ---
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⏸️ Pause Timer", key="pause_timer", disabled=not st.session_state.w_timer_running):
            pause_timer()
            st.rerun()
    with col2:
        if st.button("▶️ Resume Timer", key="resume_timer", disabled=not st.session_state.w_timer_paused):
            resume_timer()
            st.rerun()
    with col3:
        if st.button("⏹️ Stop Timer", key="stop_timer", disabled=not (st.session_state.w_timer_running or st.session_state.w_timer_paused)):
            stop_timer()
            st.rerun()

    # --- Game Logic ---
    # Add your game logic here (e.g., puzzle board, guessing letters, solving puzzles)

app()
