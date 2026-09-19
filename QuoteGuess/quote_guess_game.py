import streamlit as st
import random
from quotes_data import quotes_data
import re


def clean_speaker_name(speaker):
    """Removes parenthetical parts from speaker names."""
    return re.sub(r"\(.*\)", "", speaker).strip()


def build_speaker_options(correct_speaker, all_speakers, num_options=6):
    """Return a list of speaker options including the correct speaker."""
    cleaned_correct_speaker = clean_speaker_name(correct_speaker)
    # Ensure we don't have duplicates after cleaning
    cleaned_all_speakers = sorted(list(set(clean_speaker_name(s) for s in all_speakers if s)))
    available = [speaker for speaker in cleaned_all_speakers if speaker != cleaned_correct_speaker]
    num_distractors = min(num_options - 1, len(available))
    distractors = random.sample(available, num_distractors) if num_distractors > 0 else []
    options = distractors + [correct_speaker]
    random.shuffle(options)
    return options


def app():
    """Main Quote Guess Game Application"""
    
    # --- CSS Styling ---
    st.markdown("""
    <style>
    .quote-display {
        font-size: 26px;
        font-style: italic;
        text-align: center;
        color: #1E3A8A;
        margin: 30px 0;
        padding: 30px;
        background-color: #DBEAFE;
        border-radius: 10px;
        border: 3px solid #1E3A8A;
        line-height: 1.6;
    }
    .hint-box {
        font-size: 18px;
        padding: 15px;
        margin: 15px 0;
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        border-radius: 5px;
        color: #78350F;
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
    .big-quote {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin: 20px 0;
    }
    .speaker-box {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 20px;
        background-color: #E0E7FF;
        border-radius: 10px;
        border: 2px solid #4F46E5;
        color: #1E3A8A; /* Dark blue text for better contrast */
        margin: 20px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar: Game Setup ---
    st.sidebar.header("🎮 Game Setup")
    num_teams = st.sidebar.slider("Number of teams:", 2, 4, 2, step=1)
    num_questions = st.sidebar.slider("Number of questions:", 5, len(quotes_data), 10, step=1)

    if "current_team" not in st.session_state:
        st.session_state.current_team = 0

    team_options = [f"Team {t + 1}" for t in range(num_teams)]

    st.markdown("### 🎯 Select Guessing Team")
    team_cols = st.columns(num_teams)
    for t, team_name in enumerate(team_options):
        with team_cols[t]:
            is_active = t == st.session_state.current_team
            button_label = f"{team_name} {'● Active' if is_active else ''}".strip()
            if st.button(button_label, key=f"quote_team_{t}", use_container_width=True):
                st.session_state.current_team = t
                st.rerun()

    # Define team colors
    team_colors = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400"]
    team_colors = team_colors[:num_teams]

    # --- Initialize game state ---
    if "quote_game_initialized" not in st.session_state:
        st.session_state.quote_game_initialized = False

    if st.sidebar.button("🔁 Start New Game") or not st.session_state.quote_game_initialized:
        selected_quotes = random.sample(quotes_data, min(num_questions, len(quotes_data)))
        
        st.session_state.quote_questions = selected_quotes
        st.session_state.current_question = 0
        st.session_state.team_scores = [0] * num_teams
        st.session_state.current_team = 0
        st.session_state.question_answered = False
        st.session_state.hints_shown = []
        st.session_state.question_history = []
        st.session_state.game_over = False
        st.session_state.speaker_options = {}
        st.session_state.quote_game_initialized = True
        st.rerun()

    if not st.session_state.quote_game_initialized:
        st.info("👈 Click 'Start New Game' in the sidebar to begin!")
        return

    all_speaker_names = sorted({q['speaker'] for q in quotes_data if q.get('speaker')})

    # --- Game Over Check ---
    if st.session_state.current_question >= len(st.session_state.quote_questions):
        st.session_state.game_over = True

    if st.session_state.game_over:
        st.success("🎉 Game Complete!")
        
        # Display Final Scores
        st.markdown("### 📊 Final Scores")
        score_cols = st.columns(num_teams)
        for t in range(num_teams):
            color = team_colors[t]
            with score_cols[t]:
                st.markdown(
                    f"<div class='score-label' style='background-color:{color}'>"
                    f"Team {t+1}: {st.session_state.team_scores[t]}</div>",
                    unsafe_allow_html=True
                )
        
        # Determine winner
        max_score = max(st.session_state.team_scores)
        winners = [i+1 for i, score in enumerate(st.session_state.team_scores) if score == max_score]
        
        if len(winners) == 1:
            st.info(f"🏆 Team {winners[0]} wins with {max_score} points!")
        else:
            st.info(f"🏆 Teams {', '.join(map(str, winners))} tie with {max_score} points!")
        
        if st.button("🔁 Play Again"):
            st.session_state.clear()
            st.rerun()
        return

    # --- Current Question ---
    current_quote_data = st.session_state.quote_questions[st.session_state.current_question]
    question_num = st.session_state.current_question + 1
    total_questions = len(st.session_state.quote_questions)

    st.markdown(f"### Question {question_num} of {total_questions}")
    st.markdown(f"##### 🎯 Team {st.session_state.current_team + 1}'s Turn")

    # --- Display Quote ---
    st.markdown(
        f"<div class='quote-display'>\"{current_quote_data['quote']}\"</div>",
        unsafe_allow_html=True
    )

    st.markdown("#### Who said this quote?")

    # --- Display Hints ---
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("**Available Hints:**")
        for i, hint in enumerate(current_quote_data['hints']):
            hint_num = i + 1
            hint_type = hint.split(':')[0]
            is_revealed = i in st.session_state.hints_shown
            
            if is_revealed:
                st.markdown(
                    f"<div class='hint-box'>💡 **{hint_type}:** {hint.split(':', 1)[1].strip()}</div>",
                    unsafe_allow_html=True
                )
            else:
                button_label = f"💡 Show {hint_type} Hint"
                if st.button(button_label, key=f"hint-{question_num}-{hint_num}"):
                    if i not in st.session_state.hints_shown:
                        st.session_state.hints_shown.append(i)
                        st.rerun()

    with col2:
        st.write("**Points Available:**")
        base_points = 300
        hints_used = len(st.session_state.hints_shown)
        points_remaining = max(base_points - (hints_used * 100), 0)
        
        st.markdown(
            f"<div style='font-size: 24px; font-weight: bold; text-align: center; "
            f"color: #059669; background-color: #D1FAE5; padding: 15px; border-radius: 8px;'>"
            f"{points_remaining} pts</div>",
            unsafe_allow_html=True
        )

    # --- Answer Input ---
    st.markdown("---")
    
    if not st.session_state.question_answered:
        correct_speaker = current_quote_data['speaker']
        if st.session_state.current_question not in st.session_state.speaker_options:
            st.session_state.speaker_options[st.session_state.current_question] = build_speaker_options(
                correct_speaker,
                all_speaker_names,
                num_options=10
            )
        options = st.session_state.speaker_options[st.session_state.current_question]

        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_speaker = st.radio(
                "Pick the speaker from the list:",
                options,
                key=f"guess-{question_num}"
            )
        
        with col2:
            st.write("")  # Spacing
            submit = st.button("✓ Submit Answer", key=f"submit-{question_num}")
        
        if submit and selected_speaker:
            st.session_state.question_answered = True
            
            # Check answer
            correct_speaker_lower = correct_speaker.lower()
            guess_lower = selected_speaker.lower()
            
            # Calculate base points
            base_points = 300
            hints_used = len(st.session_state.hints_shown)
            points_earned = max(base_points - (hints_used * 100), 0)
            
            # Store in history
            is_correct = guess_lower == correct_speaker_lower
            st.session_state.question_history.append({
                'question_num': question_num,
                'quote': current_quote_data['quote'],
                'correct_speaker': correct_speaker,
                'guess': selected_speaker,
                'is_correct': is_correct,
                'points': points_earned if is_correct else 0,
                'team': st.session_state.current_team + 1,
                'hints_used': hints_used
            })
            
            # Update score if correct
            if is_correct:
                st.session_state.team_scores[st.session_state.current_team] += points_earned
            
            st.rerun()
    
    # --- Show Result ---
    if st.session_state.question_answered:
        hist = st.session_state.question_history[-1]
        
        if hist['is_correct']:
            st.markdown(
                f"<div class='answer-guess answer-correct'>✓ CORRECT! "
                f"Team {hist['team']} earned {hist['points']} points!</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='answer-guess answer-wrong'>✗ Incorrect! "
                f"You guessed: {hist['guess']}</div>",
                unsafe_allow_html=True
            )
        
        st.markdown(
            f"<div class='speaker-box'>The answer was: {hist['correct_speaker']}</div>",
            unsafe_allow_html=True
        )
        
        st.write(f"**Reference:** {current_quote_data['book']} {current_quote_data['chapter']}")
        
        if st.button("➡️ Next Question", key=f"next_quote_{question_num}"):
            st.session_state.current_question += 1
            st.session_state.question_answered = False
            st.session_state.hints_shown = []
            st.session_state.current_team = (st.session_state.current_team + 1) % num_teams
            st.rerun()


    # --- Score Display ---
    st.markdown("---")
    st.markdown("### 📊 Current Scores")
    
    score_cols = st.columns(num_teams)
    for t in range(num_teams):
        color = team_colors[t]
        label = f"Team {t+1}\n{st.session_state.team_scores[t]}"
        
        with score_cols[t]:
            if t == st.session_state.current_team and not st.session_state.question_answered:
                st.markdown(
                    f"<div class='score-label team-current' style='background-color:{color}'>"
                    f"{label} ⬅️ Current</div>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div class='score-label' style='background-color:{color}'>{label}</div>",
                    unsafe_allow_html=True
                )

    # --- Restart Game ---
    if st.button("🔁 Restart Game"):
        st.session_state.clear()
        st.rerun()


if __name__ == "__main__":
    app()
