import streamlit as st
import random
import re
from who_data import character_data


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


def app():
    """Main Guess Who Game Application"""
    
    # --- CSS Styling ---
    st.markdown("""
    <style>
    .character-hints {
        font-size: 20px;
        text-align: left;
        color: #1E3A8A;
        margin: 20px 0;
        padding: 20px;
        background-color: #DBEAFE;
        border-radius: 10px;
        border: 3px solid #1E3A8A;
        line-height: 1.6;
    }
    .hint-item {
        margin-bottom: 10px;
    }
    .answer-guess {
        font-size: 20px;
        padding: 15px;
        margin: 10px 0;
        background-color: #DDD;
        border-radius: 8px;
        text-align: center;
        font-weight: bold;
    }
    .answer-correct {
        background-color: #10B981 !important;
        color: white;
    }
    .answer-wrong {
        background-color: #EF4444 !important;
        color: white;
    }
    .score-label {
        font-size: 22px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        color: white;
    }
    .team-current {
        font-weight: 700;
        border: 3px solid #000;
    }
    .character-name-display {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background-color: #E0E7FF;
        border-radius: 10px;
        border: 2px solid #4F46E5;
        color: #1E3A8A;
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Initialize game state ---
    if "guess_who_game_initialized" not in st.session_state:
        st.session_state.guess_who_game_initialized = False

    if st.sidebar.button("🔁 Start New Game") or not st.session_state.guess_who_game_initialized:
        selected_characters = random.sample(character_data, len(character_data)) # Use all 50 characters
        
        st.session_state.character_questions = selected_characters
        st.session_state.current_character_question = 0
        st.session_state.team_scores = [0] * 2 # Default to 2 teams
        st.session_state.current_team = 0
        st.session_state.question_answered = False
        st.session_state.hints_revealed_count = 0
        st.session_state.character_game_history = []
        st.session_state.character_game_over = False
        st.session_state.character_options_for_current_question = []
        st.session_state.guess_who_game_initialized = True
        st.rerun()

    if not st.session_state.guess_who_game_initialized:
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
            st.write(f"Team {t+1}: {st.session_state.team_scores[t]} points")
        if st.button("🔁 Play Again"):
            st.session_state.clear()
            st.rerun()
        return

    # --- Current Question ---
    current_char_data = st.session_state.character_questions[st.session_state.current_character_question]
    question_num = st.session_state.current_character_question + 1
    total_questions = len(st.session_state.character_questions)

    st.markdown(f"### Question {question_num} of {total_questions}")
    st.markdown(f"##### 🎯 Team {st.session_state.current_team + 1}'s Turn")

    st.markdown("<div class='character-hints'>", unsafe_allow_html=True)
    for i in range(st.session_state.hints_revealed_count):
        if i < len(current_char_data['hints']):
            st.markdown(f"<div class='hint-item'>**Hint {i+1}:** {current_char_data['hints'][i]}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.hints_revealed_count < len(current_char_data['hints']) and not st.session_state.question_answered:
        if st.button(f"Reveal Hint {st.session_state.hints_revealed_count + 1}"):
            st.session_state.hints_revealed_count += 1
            st.rerun()
    
    # Prepare options for the current question if not already done
    if not st.session_state.character_options_for_current_question:
        st.session_state.character_options_for_current_question = build_character_options(
            current_char_data['character_name'],
            all_character_names
        )

    # --- Answer Input ---
    if not st.session_state.question_answered:
        selected_character = st.radio(
            "Who is this character?",
            st.session_state.character_options_for_current_question,
            key=f"char_guess_{question_num}"
        )
        
        if st.button("Submit Guess", key=f"submit_char_{question_num}"):
            st.session_state.question_answered = True
            
            is_correct = (clean_character_name(selected_character) == clean_character_name(current_char_data['character_name']))
            
            # Scoring: 400 points for first hint, 300 for second, 200 for third, 100 for fourth.
            # If no hints used, 500 points.
            points_possible = 500
            if st.session_state.hints_revealed_count > 0:
                points_possible = 500 - (st.session_state.hints_revealed_count * 100)
            
            points_earned = points_possible if is_correct else 0

            st.session_state.character_game_history.append({
                'question_num': question_num,
                'character_name': current_char_data['character_name'],
                'guess': selected_character,
                'is_correct': is_correct,
                'points': points_earned,
                'team': st.session_state.current_team + 1,
                'hints_used': st.session_state.hints_revealed_count
            })
            
            if is_correct:
                st.session_state.team_scores[st.session_state.current_team] += points_earned
            
            st.rerun()

    # --- Show Result ---
    if st.session_state.question_answered:
        hist = st.session_state.character_game_history[-1]
        
        if hist['is_correct']:
            st.markdown(
                f"<div class='answer-guess answer-correct'>✅ Correct! Team {hist['team']} earned {hist['points']} points!</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='answer-guess answer-wrong'>❌ Incorrect! You guessed: {hist['guess']}</div>",
                unsafe_allow_html=True
            )
        
        st.markdown(
            f"<div class='character-name-display'>The character was: {hist['character_name']}</div>",
            unsafe_allow_html=True
        )
        
        if st.button("➡️ Next Character", key=f"next_char_{question_num}"):
            st.session_state.current_character_question += 1
            st.session_state.question_answered = False
            st.session_state.hints_revealed_count = 0
            st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)
            st.session_state.character_options_for_current_question = [] # Clear options for next question
            st.rerun()

    # --- Score Display ---
    st.markdown("---")
    st.markdown("### 📊 Current Scores")
    
    num_teams = len(st.session_state.team_scores)
    team_cols = st.columns(num_teams)
    for t in range(num_teams):
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