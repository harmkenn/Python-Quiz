import streamlit as st
import random
import time
from puzzle_bank import PUZZLE_BANK  # Import the puzzle bank from the external file

st.set_page_config(page_title="Scripture Wheel", layout="wide")
# v3.5

# ---------------------------------------------------------
# CONFIGURATION & PUZZLE BANK
# ---------------------------------------------------------
TEAM_NAMES = ["Team 1", "Team 2", "Team 3", "Team 4"]
TEAM_COLORS = ["#3b82f6", "#ef4444", "#22c55e", "#a855f7"]

VOWEL_COST = 200  # Cost to buy a vowel
RANDOM_VALUES = [100, 200, 300, 400, 500, "Lose Turn"]  # Possible random point values

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

# ---------------------------------------------------------
# GAME LOGIC
# ---------------------------------------------------------
def start_new_round():
    puzzle_obj = random.choice(PUZZLE_BANK)
    st.session_state.w_puzzle = puzzle_obj
    st.session_state.w_guessed_letters = set()
    st.session_state.w_revealed = False
    st.session_state.w_random_value = None

TIMER_DURATION = 15

def start_timer():
    st.session_state.w_timer_start = time.time()
    st.session_state.w_timer_running = True

def stop_timer():
    st.session_state.w_timer_running = False
    st.session_state.w_timer_start = None

def get_time_left():
    if not st.session_state.get('w_timer_running', False) or st.session_state.get('w_timer_start') is None:
        return TIMER_DURATION
    elapsed = time.time() - st.session_state.w_timer_start
    return max(0, TIMER_DURATION - int(elapsed))

def timer_color(seconds_left):
    if seconds_left > TIMER_DURATION * 0.6:
        return "#22c55e"
    elif seconds_left > TIMER_DURATION * 0.3:
        return "#eab308"
    else:
        return "#ef4444"

def spin_random_value():
    st.session_state.w_random_value = random.choice(RANDOM_VALUES)

def guess_letter(letter):
    # Stop the timer as soon as a guess is made
    stop_timer()

    # Check if the random value has been spun
    if st.session_state.w_random_value is None:
        st.error("Error: No spin value. Please refresh the page.")
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
            
            # Check if the vowel exists in the puzzle
            phrase = st.session_state.w_puzzle["text"].upper()
            count = phrase.count(letter)
            
            if count == 0:
                # Vowel does not exist, lose turn
                st.warning(f"Vowel '{letter}' is not in the puzzle. Team {TEAM_NAMES[st.session_state.w_current_team]} loses their turn!")
                st.session_state.w_current_team = (st.session_state.w_current_team + 1) % len(TEAM_NAMES)
                st.session_state.w_random_value = None  # Let the main loop handle the new turn
                return # Exit
            else:
                # Vowel exists, reveal it
                st.session_state.w_guessed_letters.add(letter)
                st.info(f"Vowel '{letter}' guessed correctly!")
                st.session_state.w_random_value = None
                return  # Exit the function without adding points

    # Add the guessed letter to the set of guessed letters
    st.session_state.w_guessed_letters.add(letter)
    
    # Check occurrences of the letter in the puzzle
    phrase = st.session_state.w_puzzle["text"].upper()
    count = phrase.count(letter)
    
    if count > 0:
        # Ensure random value is numeric before calculating points
        if isinstance(st.session_state.w_random_value, int):
            points = count * st.session_state.w_random_value
            st.session_state.w_team_scores[st.session_state.w_current_team] += points
        else:
            st.error("Invalid random value! Please spin again.")
            return
        
        # Check if all letters have been guessed
        unique_chars = set(c for c in phrase if c.isalpha())
        if unique_chars.issubset(st.session_state.w_guessed_letters):
            st.session_state.w_revealed = True
            st.balloons()
        st.session_state.w_random_value = None
    else:
        # If the letter does not exist, cycle to the next team
        st.warning(f"Letter '{letter}' is not in the puzzle. Team {TEAM_NAMES[st.session_state.w_current_team]} loses their turn!")
        st.session_state.w_current_team = (st.session_state.w_current_team + 1) % len(TEAM_NAMES)
        st.session_state.w_random_value = None  # Let the main loop handle the new turn

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
        st.session_state.w_random_value = None
# ---------------------------------------------------------
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
        time.sleep(0.5) # Let toast appear before rerun
        st.rerun()

    c1, c2 = st.columns([2, 1])
    
    # --- Top: Timer ---
    timer_placeholder = st.empty()

    # Set a default static display for the timer
    timer_placeholder.markdown(
        f"""
        <div style="
            font-size:3rem; font-weight:800; text-align:center; padding:0.5rem 1rem;
            border-radius:1rem; margin:1rem auto; background-color:#334155; color:white;
        ">
            --
        </div>
        """,
        unsafe_allow_html=True,
    )

    with c1:
        st.title("🎡 Scripture Wheel")


        # --- Top Bar: Controls ---
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
             if st.button("🔄 New Puzzle"):
                start_new_round()
                st.rerun()

       

        # --- Top Bar: Controls ---
            st.rerun()

        if not st.session_state.w_puzzle:
            start_new_round()
            st.rerun()

    # --- New Turn Logic ---
    # If puzzle is active and there's no spin value, it's a new turn.
    if st.session_state.w_puzzle and st.session_state.w_random_value is None and not st.session_state.w_revealed:
        spin_random_value()
        # If spin is "Lose Turn", the user must click, so don't start timer.
        if st.session_state.w_random_value != "Lose Turn":
            start_timer()
        st.rerun()

    # --- Scoreboard ---
    with st.sidebar:
            unsafe_allow_html=True,
        )

        st.write("### Team Scores")
        for i in range(4):
            is_active = (i == st.session_state.w_current_team)
            border = "4px solid white" if is_active else f"2px solid {TEAM_COLORS[i]}"
            bg = TEAM_COLORS[i] if is_active else "transparent"
            text_color = "white" if is_active else TEAM_COLORS[i]
            
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
                    margin-bottom: 10px;
                ">
                    {TEAM_NAMES[i]}<br>
                    <span style="font-size: 1.5rem">${st.session_state.w_team_scores[i]}</span><br>
                    Day Total: ${st.session_state.w_day_totals[i]}
                </div>
                """, 
                unsafe_allow_html=True
            )
            if st.button(f"Select {TEAM_NAMES[i]}", key=f"sel_team_{i}"):
                st.session_state.w_current_team = i
                st.session_state.w_random_value = None
                st.rerun()

    # --- Random Value Spinner ---
    with c2:
        st.write("### Spin Result")
        if st.session_state.w_random_value == "Lose Turn":
            stop_timer() # Ensure timer is stopped
            st.warning("You landed on 'Lose Turn'! Click the button below to cycle to the next team.")
            if st.button("➡️ Next Team"):
                st.session_state.w_current_team = (st.session_state.w_current_team + 1) % len(TEAM_NAMES)
                st.session_state.w_random_value = None  # Reset spinner value
                st.rerun()
        elif st.session_state.w_random_value is not None:
            st.success(f"Current Spin Value: {st.session_state.w_random_value}")
        else:
            # This case should not be reached with auto-spin
            st.info("Spinning...")

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
                    disabled = (
                        (char in st.session_state.w_guessed_letters)
                        or st.session_state.w_revealed
                        or st.session_state.w_random_value == "Lose Turn"
                    )
                    
                    # Add a label for vowels to indicate cost
                    label = f"{char} ($200)" if char in "AEIOU" else char
                    
                    if st.button(label, key=f"btn_{char}", disabled=disabled):
                        guess_letter(char)
                        st.rerun()

    with col_right:
        st.write("### Solve the Puzzle")
        #st.info("Click 'Correct' if the team solved the puzzle correctly, or 'Incorrect' if they guessed wrong.")
        
        # Solve buttons
        if st.button("✅ Correct"):
            solve_puzzle(correct=True)
            st.rerun()
        if st.button("❌ Incorrect"):
            solve_puzzle(correct=False)
            st.rerun()

        #st.info("Scoring: Random value determines points per letter. 500 points bonus for solving.")

    # --- Confetti on Win ---
    if st.session_state.w_revealed:
        stop_timer()
        st.success(f"Puzzle Solved! The phrase was: {st.session_state.w_puzzle['text']} ({st.session_state.w_puzzle.get('reference', 'No reference')})")
        if st.button("Next Puzzle ➡️"):
            start_new_round()
            st.rerun()

    # --- Timer Update Loop ---
    if st.session_state.get('w_timer_running', False):
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
        time.sleep(1)
        st.rerun()


if __name__ == "__main__":
    app()
