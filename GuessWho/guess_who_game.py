import streamlit as st
import random
import re
import time
from who_data import character_data

# --- Constants for game phases ---
PHASE_WAITING_FOR_HINT_REVEAL = "waiting_for_hint_reveal"
PHASE_BUZZED_IN_GUESS = "buzzed_in_guess"
PHASE_ANSWER_REVEALED = "answer_revealed"

# --- Game Configuration ---
HINT_REVEAL_INTERVAL = 20 # seconds between hints
GUESS_TIME_LIMIT = 15 # seconds for a buzzed-in team to guess

def clean_character_name(name):
    """Removes parenthetical parts from character names."""
    return re.sub(r"\(.*\)", "", name).strip()


def build_character_options(correct_character, all_characters, num_options=6):
    """Return a list of character options including the correct character."""
    cleaned_correct_character = clean_character_name(correct_character)
    # Ensure we don't have duplicates after cleaning and exclude the correct one
    available = [
        char for char in all_characters
        if clean_character_name(char) != cleaned_correct_character
    ]
    
    # If there aren't enough unique characters, just use what's available
    num_distractors = min(num_options - 1, len(available))
    distractors = random.sample(available, num_distractors) if num_distractors > 0 else []
    
    options = distractors + [correct_character]
    random.shuffle(options)
    return options

def initialize_game_state(num_teams):
    selected_characters = random.sample(character_data, len(character_data)) # Use all 50 characters
    st.session_state.character_questions = selected_characters
    st.session_state.current_character_question = 0
    st.session_state.team_scores = [0] * num_teams
    st.session_state.current_team = 0 # Team 0 starts
    st.session_state.game_phase = PHASE_WAITING_FOR_HINT_REVEAL
    st.session_state.hints_revealed_count = 1 # Start with the first hint revealed
    st.session_state.character_game_history = []
    st.session_state.character_game_over = False
    st.session_state.character_options_for_current_question = []
    st.session_state.last_action_time = time.time()
    st.session_state.buzzed_team_index = None
    st.session_state.has_guessed_this_round = [False] * num_teams # Track who has guessed for current question
    st.session_state.guess_timer_start = None
    st.session_state.question_answered = False
    st.session_state.initialized = True


def app():
    """Main Guess Who Game Application"""

    # --- CSS Styling ---
    st.set_page_config(layout="wide")
    st.markdown("""
    <style>
    /* General font size increase for radio buttons and buttons */
    .stRadio, .stButton>button {
        font-size: 1.2rem;
    }
    h3 {
        font-size: 2.5rem;
    }
    h5 {
        font-size: 1.7rem;
    }
    .character-hints {
        font-size: 1.6rem; /* Larger font for hints */
        line-height: 1.6;
        padding: 10px;
    }
    .hint-item {
        margin-bottom: 12px;
    }
    .answer-guess {
        font-size: 1.7rem; /* Larger font for results */
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    }
    .answer-correct {
        background-color: #10B981;
        color: white;
    }
    .answer-wrong {
        background-color: #EF4444;
        color: white;
    }
    .score-label {
        font-size: 1.8rem; /* Larger font for scores */
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        color: white;
    }
    .team-current {
        border: 3px solid #000;
    }
    .character-name-display {
        font-size: 2.0rem; /* Larger font for correct character name */
        font-weight: bold;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Initialize game state ---
    st.sidebar.header("🎮 Game Setup")
    num_teams_setting = st.sidebar.slider("Number of teams:", 2, 4, 2, step=1) # Allow up to 4 teams

    if "initialized" not in st.session_state or not st.session_state.initialized:
        initialize_game_state(num_teams_setting)
        st.rerun()
    
    # If number of teams changed in sidebar, re-initialize
    if st.session_state.initialized and len(st.session_state.team_scores) != num_teams_setting:
        initialize_game_state(num_teams_setting)
        st.rerun()

    if st.sidebar.button("🔁 Start New Game (Resets Scores)"):
        initialize_game_state(num_teams_setting)
        st.rerun()

    if not st.session_state.initialized:
        st.info("👈 Click 'Start New Game' in the sidebar to begin!")
        return

    all_character_names = [char['character_name'] for char in character_data]

    # --- Game Over Check ---
    if st.session_state.current_character_question >= len(st.session_state.character_questions):
        st.session_state.character_game_over = True

    if st.session_state.character_game_over:
        st.success("🎉 Game Complete!")
        st.markdown("### 📊 Final Scores")
        for t in range(len(st.session_state.team_scores)):
            color = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400"][t]
            st.markdown(f"<div class='score-label' style='background-color:{color}'>Team {t+1}: {st.session_state.team_scores[t]} points</div>", unsafe_allow_html=True)
        if st.button("🔁 Play Again"):
            st.session_state.clear()
            st.rerun()
        return

    # --- Current Question ---
    current_char_data = st.session_state.character_questions[st.session_state.current_character_question]
    question_num = st.session_state.current_character_question + 1
    total_questions = len(st.session_state.character_questions)

    st.markdown(f"### Question {question_num} of {total_questions}")
    
    # --- Game Logic based on Phase ---
    if st.session_state.game_phase == PHASE_WAITING_FOR_HINT_REVEAL:
        if st.session_state.character_game_history:
            hist = st.session_state.character_game_history[-1]
            if hist['question_num'] == question_num and not hist['is_correct']:
                st.warning(
                    f"Team {hist['team']} guessed '{hist['guess']}' and lost {abs(hist['points'])} points."
                )

        # Display hints
        st.markdown("<div class='character-hints'>", unsafe_allow_html=True)
        for i in range(st.session_state.hints_revealed_count):
            if i < len(current_char_data['hints']):
                st.markdown(f"<div class='hint-item'>**Hint {i+1}:** {current_char_data['hints'][i]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # "Next Hint" button
        if st.session_state.hints_revealed_count < len(current_char_data['hints']):
            if st.button("Reveal Next Hint"):
                st.session_state.hints_revealed_count += 1
                st.rerun()
        else:
            st.info("All hints have been revealed!")
            if st.button("Show Answer"):
                st.session_state.game_phase = PHASE_ANSWER_REVEALED
                st.session_state.question_answered = True
                st.rerun()

        st.markdown("---")
        st.markdown("##### Who's buzzing in?")
        buzz_cols = st.columns(len(st.session_state.team_scores))
        for t in range(len(st.session_state.team_scores)):
            with buzz_cols[t]:
                if not st.session_state.has_guessed_this_round[t]:
                    if st.button(f"Team {t+1} Buzz!", key=f"buzz_{t}"):
                        st.session_state.buzzed_team_index = t
                        st.session_state.game_phase = PHASE_BUZZED_IN_GUESS
                        st.session_state.guess_timer_start = time.time()
                        st.rerun()
                else:
                    st.write(f"Team {t+1} has guessed.")



    elif st.session_state.game_phase == PHASE_BUZZED_IN_GUESS:
        buzzed_team = st.session_state.buzzed_team_index
        st.markdown(f"##### Team {buzzed_team + 1} has buzzed in! You have {GUESS_TIME_LIMIT} seconds to guess.")

        elapsed_guess_time = time.time() - st.session_state.guess_timer_start
        remaining_guess_time = GUESS_TIME_LIMIT - elapsed_guess_time

        if remaining_guess_time <= 0:
            st.warning(f"Time's up for Team {buzzed_team + 1}! -100 points.")
            st.session_state.team_scores[buzzed_team] -= 100 # Penalty for not guessing in time
            st.session_state.has_guessed_this_round[buzzed_team] = True
            st.session_state.buzzed_team_index = None
            
            # Check if other teams can still guess
            if all(st.session_state.has_guessed_this_round):
                st.session_state.game_phase = PHASE_ANSWER_REVEALED
                st.session_state.question_answered = True
            else:
                st.session_state.game_phase = PHASE_WAITING_FOR_HINT_REVEAL
                st.session_state.last_action_time = time.time() # Restart hint timer for next team/hint
                # Move to the next team that hasn't guessed yet
                st.session_state.current_team = (buzzed_team + 1) % len(st.session_state.team_scores)
                while st.session_state.has_guessed_this_round[st.session_state.current_team] and not all(st.session_state.has_guessed_this_round):
                    st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)
            st.rerun()

        st.markdown(f"**Time remaining:** {int(max(0, remaining_guess_time))} seconds")

        # Display hints revealed so far
        st.markdown("<div class='character-hints'>", unsafe_allow_html=True)
        for i in range(st.session_state.hints_revealed_count):
            if i < len(current_char_data['hints']):
                st.markdown(f"<div class='hint-item'>**Hint {i+1}:** {current_char_data['hints'][i]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Prepare options for the current question if not already done
        if not st.session_state.character_options_for_current_question:
            st.session_state.character_options_for_current_question = build_character_options(
                current_char_data['character_name'],
                all_character_names, num_options=10
            )

        selected_character = st.radio(
            "Who is this character?",
            st.session_state.character_options_for_current_question,
            key=f"char_guess_{question_num}_{buzzed_team}"
        )
        
        if st.button("Submit Guess", key=f"submit_char_{question_num}_{buzzed_team}"):
            is_correct = (clean_character_name(selected_character) == clean_character_name(current_char_data['character_name']))
            
            points_possible = 500 - (st.session_state.hints_revealed_count * 100)
            points_earned = points_possible if is_correct else -100 # Incorrect guess penalty

            st.session_state.character_game_history.append({
                'question_num': question_num,
                'character_name': current_char_data['character_name'],
                'guess': selected_character,
                'is_correct': is_correct,
                'points': points_earned,
                'team': buzzed_team + 1,
                'hints_used': st.session_state.hints_revealed_count
            })
            
            if is_correct:
                st.session_state.team_scores[buzzed_team] += points_earned
                st.session_state.game_phase = PHASE_ANSWER_REVEALED
                st.session_state.question_answered = True
            else:
                st.session_state.team_scores[buzzed_team] += points_earned
                st.session_state.has_guessed_this_round[buzzed_team] = True
                st.session_state.buzzed_team_index = None

                if all(st.session_state.has_guessed_this_round):
                    st.session_state.game_phase = PHASE_ANSWER_REVEALED
                    st.session_state.question_answered = True
                else:
                    st.session_state.game_phase = PHASE_WAITING_FOR_HINT_REVEAL
                    st.session_state.last_action_time = time.time()
                    st.session_state.current_team = (buzzed_team + 1) % len(st.session_state.team_scores)
                    while st.session_state.has_guessed_this_round[st.session_state.current_team]:
                        st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)
            
            st.rerun()

    # --- Show Result ---
    if st.session_state.question_answered:
        if st.session_state.character_game_history:
            hist = st.session_state.character_game_history[-1]

            if hist['is_correct']:
                st.markdown(
                    f"<div class='answer-guess answer-correct'>✅ Correct! Team {hist['team']} earned {hist['points']} points!</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='answer-guess answer-wrong'>❌ Incorrect guess! Team {hist['team']} guessed '{hist['guess']}'. That is not the correct character. -100 points.</div>",
                    unsafe_allow_html=True
                )

            st.markdown(
                f"<div class='character-name-display'>The character was: {hist['character_name']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='answer-guess answer-wrong'>ℹ️ Answer revealed without a submitted guess.</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div class='character-name-display'>The character was: {current_char_data['character_name']}</div>",
                unsafe_allow_html=True
            )

        if st.button("➡️ Next Character", key=f"next_char_{question_num}"):
            st.session_state.current_character_question += 1
            st.session_state.question_answered = False
            st.session_state.hints_revealed_count = 1 # Start next question with first hint revealed
            st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)
            st.session_state.buzzed_team_index = None
            st.session_state.has_guessed_this_round = [False] * len(st.session_state.team_scores)
            st.session_state.character_options_for_current_question = [] # Clear options for next question
            st.session_state.game_phase = PHASE_WAITING_FOR_HINT_REVEAL
            st.rerun()

    # --- Score Display ---
    st.markdown("---")
    st.markdown("### 📊 Current Scores")
    
    num_teams = len(st.session_state.team_scores)
    team_cols = st.columns(num_teams)
    for t in range(num_teams): # Iterate through all teams
        color = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400"][t] # Re-define for local scope
        label = f"Team {t+1}: {st.session_state.team_scores[t]}"
        with team_cols[t]:
            if t == st.session_state.current_team and not st.session_state.question_answered:
                st.markdown(
                    f"<div class='score-label team-current' style='background-color:{color}'>{label} ⬅️</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='score-label' style='background-color:{color}'>{label}</div>",
                    unsafe_allow_html=True
                )

    # --- Restart Game ---
    if st.button("🔄 Restart Game"):
        st.session_state.clear()
        st.rerun()


if __name__ == "__main__":
    app()