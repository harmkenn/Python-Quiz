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
HINT_REVEAL_INTERVAL = 15 # seconds between auto-revealing hints
GUESS_TIME_LIMIT = 15 # seconds for a buzzed-in team to guess

def clean_character_name(name):
    """Removes parenthetical parts from character names."""
    return re.sub(r"\(.*\)", "", name).strip()

def build_character_options(correct_character, all_characters, num_options=10):
    """Return a list of character options including the correct character."""
    cleaned_correct_character = clean_character_name(correct_character)
    available = [
        char for char in all_characters
        if clean_character_name(char) != cleaned_correct_character
    ]
    num_distractors = min(num_options - 1, len(available))
    distractors = random.sample(available, num_distractors) if num_distractors > 0 else []
    
    options = distractors + [correct_character]
    random.shuffle(options)
    return options

def initialize_game_state(num_teams):
    selected_characters = random.sample(character_data, len(character_data))
    st.session_state.character_questions = selected_characters
    st.session_state.current_character_question = 0
    st.session_state.team_scores = [0] * num_teams
    st.session_state.current_team = 0
    st.session_state.game_phase = PHASE_WAITING_FOR_HINT_REVEAL
    st.session_state.character_game_history = []
    st.session_state.character_game_over = False
    st.session_state.buzzed_team_index = None
    st.session_state.has_guessed_this_round = [False] * num_teams
    st.session_state.guess_timer_start = None
    st.session_state.question_answered = False
    st.session_state.selected_option = None
    
    # --- Timer & Hint State ---
    st.session_state.question_start_time = time.time()
    st.session_state.timer_stopped = False
    st.session_state.shuffled_hint_indices = []
    st.session_state.initialized = True

def setup_question():
    """Sets up state specifically for the active question."""
    current_char = st.session_state.character_questions[st.session_state.current_character_question]
    all_character_names = [char['character_name'] for char in character_data]
    
    # Pre-generate multiple-choice options immediately at question start
    st.session_state.character_options_for_current_question = build_character_options(
        current_char['character_name'],
        all_character_names,
        num_options=10
    )
    
    num_hints = len(current_char['hints'])
    indices = list(range(num_hints))
    random.shuffle(indices)
    st.session_state.shuffled_hint_indices = indices
    st.session_state.question_start_time = time.time()
    st.session_state.timer_stopped = False
    st.session_state.selected_option = None

def app():
    """Main Guess Who Game Application"""

    st.set_page_config(layout="wide")
    
    # --- Custom CSS for Large Options & Fonts ---
    st.markdown("""
    <style>
    html, body, [class*="css"] {
        font-size: 1.5rem;
    }
    .stButton>button {
        font-size: 2.2rem !important;
        padding: 15px 25px !important;
        width: 100%;
        margin-bottom: 10px;
        white-space: normal;
        overflow-wrap: anywhere;
    }
    .stRadio label {
        font-size: 2.2rem !important;
    }
    h1 {
        font-size: 4.5rem !important;
    }
    h3 {
        font-size: 3.5rem !important;
    }
    h5 {
        font-size: 2.5rem !important;
    }
    .options-box {
        background-color: #1E293B;
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 25px;
        color: white;
    }
    .options-title {
        font-size: 2.8rem !important;
        font-weight: bold;
        text-align: center;
        margin-bottom: 15px;
        color: #F3F4F6;
    }
    .character-hints {
        font-size: 2.5rem !important;
        line-height: 1.6;
        padding: 20px;
        background-color: #f0f2f6;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .hint-item {
        margin-bottom: 20px;
        color: #111;
    }
    .hint-item strong {
        color: #111 !important;
    }
    .answer-guess {
        font-size: 2.5rem !important;
        padding: 20px;
        margin: 15px 0;
        border-radius: 12px;
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
        font-size: 2.5rem !important;
        font-weight: bold;
        text-align: center;
        padding: 18px;
        border-radius: 12px;
        color: white;
    }
    .character-name-display {
        font-size: 3.0rem !important;
        font-weight: bold;
        text-align: center;
    }
    .timer-display {
        font-size: 3.0rem !important;
        font-weight: bold;
        color: #D97706;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar Setup ---
    st.sidebar.header("🎮 Game Setup")
    num_teams_setting = st.sidebar.slider("Number of teams:", 2, 4, 2, step=1)

    if "initialized" not in st.session_state or not st.session_state.initialized:
        initialize_game_state(num_teams_setting)
        setup_question()
        st.rerun()
    
    if st.session_state.initialized and len(st.session_state.team_scores) != num_teams_setting:
        initialize_game_state(num_teams_setting)
        setup_question()
        st.rerun()

    if st.sidebar.button("🔁 Start New Game"):
        initialize_game_state(num_teams_setting)
        setup_question()
        st.rerun()

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

    # --- Current Question Info ---
    current_char_data = st.session_state.character_questions[st.session_state.current_character_question]
    question_num = st.session_state.current_character_question + 1
    total_questions = len(st.session_state.character_questions)

    st.markdown(f"### Question {question_num} of {total_questions}")

    # =========================================================
    # 📌 TOP SECTION: Multiple Choice Answers Available Immediately
    # =========================================================
    st.markdown("<div class='options-box'><div class='options-title'>📋 Character Choice Board</div></div>", unsafe_allow_html=True)
    
    options = st.session_state.character_options_for_current_question
    # Display choices in five columns so they fill the board in multiple rows.
    option_columns = st.columns(5)
    
    for idx, opt in enumerate(options):
        with option_columns[idx % 5]:
            # Highlight option button if currently selected
            is_selected = (st.session_state.selected_option == opt)
            label = f"⭐ {opt}" if is_selected else opt
            
            if st.button(label, key=f"opt_btn_{question_num}_{idx}"):
                st.session_state.selected_option = opt
                st.rerun()

    st.markdown("---")

    # --- Calculate elapsed time & active hints ---
    total_hints = len(current_char_data['hints'])
    if not st.session_state.timer_stopped and st.session_state.game_phase == PHASE_WAITING_FOR_HINT_REVEAL:
        elapsed = time.time() - st.session_state.question_start_time
    else:
        elapsed = getattr(st.session_state, 'frozen_elapsed', 0)

    hints_to_show_count = min(total_hints, max(1, int(elapsed // HINT_REVEAL_INTERVAL) + 1))
    points_possible = max(100, 500 - (hints_to_show_count * 100))

    # --- Timer & Control Header ---
    col_timer, col_stop = st.columns([3, 1])
    with col_timer:
        st.markdown(f"<div class='timer-display'>⏱️ Time: {int(elapsed)}s | Value: {points_possible} pts</div>", unsafe_allow_html=True)
    with col_stop:
        if st.session_state.game_phase == PHASE_WAITING_FOR_HINT_REVEAL:
            if not st.session_state.timer_stopped:
                if st.button("🛑 STOP CLOCK", key="stop_clock_btn"):
                    st.session_state.timer_stopped = True
                    st.session_state.frozen_elapsed = elapsed
                    st.rerun()
            else:
                if st.button("▶ RESUME CLOCK", key="resume_clock_btn"):
                    st.session_state.timer_stopped = False
                    st.session_state.question_start_time = time.time() - st.session_state.frozen_elapsed
                    st.rerun()

    # --- Game Logic: Hint Reveal Phase ---
    if st.session_state.game_phase == PHASE_WAITING_FOR_HINT_REVEAL:
        if st.session_state.character_game_history:
            hist = st.session_state.character_game_history[-1]
            if hist['question_num'] == question_num and not hist['is_correct']:
                st.warning(
                    f"Team {hist['team']} guessed '{hist['guess']}' and lost {abs(hist['points'])} points."
                )

        # Active Hints Block
        st.markdown("<div class='character-hints'>", unsafe_allow_html=True)
        active_indices = st.session_state.shuffled_hint_indices[:hints_to_show_count]
        for display_idx, hint_idx in enumerate(active_indices):
            st.markdown(f"<div class='hint-item'>**Hint {display_idx + 1}:** {current_char_data['hints'][hint_idx]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if hints_to_show_count >= total_hints and not st.session_state.question_answered:
            st.info("All hints revealed!")
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
                        st.session_state.frozen_elapsed = elapsed
                        st.rerun()
                else:
                    st.write(f"Team {t+1} has guessed.")

    # --- Game Logic: Buzzed-In Guess Phase ---
    elif st.session_state.game_phase == PHASE_BUZZED_IN_GUESS:
        buzzed_team = st.session_state.buzzed_team_index
        st.markdown(f"##### 🔔 Team {buzzed_team + 1} Buzzed In! You have {GUESS_TIME_LIMIT} seconds.")

        elapsed_guess_time = time.time() - st.session_state.guess_timer_start
        remaining_guess_time = GUESS_TIME_LIMIT - elapsed_guess_time

        if remaining_guess_time <= 0:
            st.warning(f"Time's up for Team {buzzed_team + 1}! -100 points.")
            st.session_state.team_scores[buzzed_team] -= 100
            st.session_state.has_guessed_this_round[buzzed_team] = True
            st.session_state.buzzed_team_index = None
            
            if all(st.session_state.has_guessed_this_round):
                st.session_state.game_phase = PHASE_ANSWER_REVEALED
                st.session_state.question_answered = True
            else:
                st.session_state.game_phase = PHASE_WAITING_FOR_HINT_REVEAL
            st.rerun()

        st.markdown(f"**Time remaining:** {int(max(0, remaining_guess_time))} seconds")

        # Hints display
        st.markdown("<div class='character-hints'>", unsafe_allow_html=True)
        active_indices = st.session_state.shuffled_hint_indices[:hints_to_show_count]
        for display_idx, hint_idx in enumerate(active_indices):
            st.markdown(f"<div class='hint-item'>**Hint {display_idx + 1}:** {current_char_data['hints'][hint_idx]}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        # Radio selection synced with top button grid
        options = st.session_state.character_options_for_current_question
        selected_idx = options.index(st.session_state.selected_option) if st.session_state.selected_option in options else 0

        selected_character = st.radio(
            "Confirm or change choice:",
            options,
            index=selected_idx,
            key=f"char_guess_{question_num}_{buzzed_team}"
        )
        
        if st.button("Submit Guess", key=f"submit_char_{question_num}_{buzzed_team}"):
            is_correct = (clean_character_name(selected_character) == clean_character_name(current_char_data['character_name']))
            points_earned = points_possible if is_correct else -100

            st.session_state.character_game_history.append({
                'question_num': question_num,
                'character_name': current_char_data['character_name'],
                'guess': selected_character,
                'is_correct': is_correct,
                'points': points_earned,
                'team': buzzed_team + 1,
            })
            
            st.session_state.team_scores[buzzed_team] += points_earned
            if is_correct:
                st.session_state.game_phase = PHASE_ANSWER_REVEALED
                st.session_state.question_answered = True
            else:
                st.session_state.has_guessed_this_round[buzzed_team] = True
                st.session_state.buzzed_team_index = None

                if all(st.session_state.has_guessed_this_round):
                    st.session_state.game_phase = PHASE_ANSWER_REVEALED
                    st.session_state.question_answered = True
                else:
                    st.session_state.game_phase = PHASE_WAITING_FOR_HINT_REVEAL
            
            st.rerun()

    # --- Show Answer Result Phase ---
    if st.session_state.question_answered or st.session_state.game_phase == PHASE_ANSWER_REVEALED:
        if st.session_state.character_game_history:
            hist = st.session_state.character_game_history[-1]

            if hist['is_correct']:
                st.markdown(
                    f"<div class='answer-guess answer-correct'>✅ Correct! Team {hist['team']} earned {hist['points']} points!</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='answer-guess answer-wrong'>❌ Incorrect guess! Team {hist['team']} guessed '{hist['guess']}'. -100 points.</div>",
                    unsafe_allow_html=True
                )

            st.markdown(
                f"<div class='character-name-display'>The character was: {hist['character_name']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                "<div class='answer-guess answer-wrong'>ℹ️ Answer revealed without a correct guess.</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div class='character-name-display'>The character was: {current_char_data['character_name']}</div>",
                unsafe_allow_html=True
            )

        if st.button("➡️ Next Character", key=f"next_char_{question_num}"):
            st.session_state.current_character_question += 1
            st.session_state.question_answered = False
            st.session_state.buzzed_team_index = None
            st.session_state.has_guessed_this_round = [False] * len(st.session_state.team_scores)
            st.session_state.game_phase = PHASE_WAITING_FOR_HINT_REVEAL
            setup_question()
            st.rerun()

    # --- Score Display ---
    st.markdown("---")
    st.markdown("### 📊 Current Scores")
    
    num_teams = len(st.session_state.team_scores)
    team_cols = st.columns(num_teams)
    for t in range(num_teams):
        color = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400"][t]
        label = f"Team {t+1}: {st.session_state.team_scores[t]}"
        with team_cols[t]:
            st.markdown(
                f"<div class='score-label' style='background-color:{color}'>{label}</div>",
                unsafe_allow_html=True
            )

    # --- Auto-rerun loop to drive ticking timer ---
    if st.session_state.game_phase == PHASE_WAITING_FOR_HINT_REVEAL and not st.session_state.timer_stopped and not st.session_state.question_answered:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    app()
