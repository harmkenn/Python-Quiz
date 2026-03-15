import streamlit as st
import data

def app():
    # --- CSS Styling for the Board ---
    st.markdown("""
    <style>
    .feud-question {
        font-size: 32px;
        font-weight: bold;
        text-align: center;
        color: #1E3A8A;
        margin-bottom: 20px;
        padding: 20px;
        background-color: #DBEAFE;
        border-radius: 10px;
        border: 2px solid #1E3A8A;
    }
    .answer-card {
        background-color: #1E40AF; /* Blue hidden */
        color: white;
        font-size: 24px;
        font-weight: bold;
        padding: 15px;
        margin: 5px 0;
        border-radius: 8px;
        border: 2px solid white;
        text-align: center;
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 3px 3px 5px rgba(0,0,0,0.3);
    }
    .answer-card-revealed {
        background-color: #FEF3C7; /* Yellowish revealed */
        color: #1E3A8A;
        border: 2px solid #1E3A8A;
        justify-content: space-between;
        padding: 0 20px;
    }
    .strike-x {
        color: #DC2626;
        font-size: 80px;
        font-weight: 900;
        text-align: center;
        line-height: 1;
    }
    .score-box {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        padding: 10px;
        border-radius: 10px;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Session State Initialization ---
    if "feud_round_index" not in st.session_state:
        st.session_state.feud_round_index = 0
    if "feud_scores" not in st.session_state:
        st.session_state.feud_scores = [0, 0] # Team 1, Team 2
    if "feud_revealed" not in st.session_state:
        st.session_state.feud_revealed = [] # List of indices revealed
    if "feud_strikes" not in st.session_state:
        st.session_state.feud_strikes = 0
    if "feud_round_points" not in st.session_state:
        st.session_state.feud_round_points = 0

    # --- Game Logic Functions ---
    def next_round():
        if st.session_state.feud_round_index < len(data.feud_data) - 1:
            st.session_state.feud_round_index += 1
            st.session_state.feud_revealed = []
            st.session_state.feud_strikes = 0
            st.session_state.feud_round_points = 0
    
    def prev_round():
        if st.session_state.feud_round_index > 0:
            st.session_state.feud_round_index -= 1
            st.session_state.feud_revealed = []
            st.session_state.feud_strikes = 0
            st.session_state.feud_round_points = 0

    def reveal_answer(idx, points):
        if idx not in st.session_state.feud_revealed:
            st.session_state.feud_revealed.append(idx)
            st.session_state.feud_round_points += points

    def add_strike():
        if st.session_state.feud_strikes < 3:
            st.session_state.feud_strikes += 1

    def clear_strikes():
        st.session_state.feud_strikes = 0

    def award_points(team_idx):
        st.session_state.feud_scores[team_idx] += st.session_state.feud_round_points
        # Optional: Auto advance or just clear points? 
        # Family Feud usually plays to end of round, then awards.
        # We will just clear the bank after awarding to prevent double awarding.
        st.session_state.feud_round_points = 0

    # --- Data for Current Round ---
    current_data = data.feud_data[st.session_state.feud_round_index]
    question = current_data["question"]
    answers = current_data["answers"] # List of (text, points)

    # --- Layout: Header & Scores ---
    st.title("👨‍👩‍👧‍👦 Family Feud")
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        st.markdown(f"<div class='score-box' style='background-color:#3b82f6;'>Team 1<br>{st.session_state.feud_scores[0]}</div>", unsafe_allow_html=True)
        if st.button("Award Bank to Team 1", use_container_width=True):
            award_points(0)
    with c2:
        st.markdown(f"<div style='text-align:center; font-size:40px; font-weight:bold;'>BANK: {st.session_state.feud_round_points}</div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='score-box' style='background-color:#ef4444;'>Team 2<br>{st.session_state.feud_scores[1]}</div>", unsafe_allow_html=True)
        if st.button("Award Bank to Team 2", use_container_width=True):
            award_points(1)

    st.markdown("---")

    # --- Question Board ---
    st.markdown(f"<div class='feud-question'>{question}</div>", unsafe_allow_html=True)

    # Display Answers (Host controls + Visuals)
    # We'll use columns to mimic the board, but for simple layout a vertical stack is fine.
    # Let's do 2 columns if more than 5 answers, else 1 column.
    
    total_ans = len(answers)
    col_a, col_b = st.columns(2)
    
    for i, (ans_text, pts) in enumerate(answers):
        is_revealed = i in st.session_state.feud_revealed
        
        # Determine which column to place this answer in
        target_col = col_a if i < (total_ans + 1) // 2 else col_b
        
        with target_col:
            # Visual Card
            if is_revealed:
                st.markdown(
                    f"<div class='answer-card answer-card-revealed'><span>{i+1}. {ans_text}</span> <span>{pts}</span></div>", 
                    unsafe_allow_html=True
                )
            else:
                # Hidden Card
                st.markdown(
                    f"<div class='answer-card'>{i+1}</div>", 
                    unsafe_allow_html=True
                )
            
            # Control Button (Host only essentially)
            if not is_revealed:
                if st.button(f"Reveal {i+1}", key=f"rev_{i}"):
                    reveal_answer(i, pts)
                    st.rerun()
            else:
                # Invisible placeholder to keep alignment? Or just nothing.
                st.write("") 

    st.markdown("---")

    # --- Strikes & Controls ---
    sc1, sc2, sc3 = st.columns([1, 2, 1])
    
    with sc1:
        st.write("### Strikes")
        s_cols = st.columns(3)
        with s_cols[0]:
            if st.button("❌"): add_strike()
        with s_cols[1]:
            if st.button("Clear"): clear_strikes()
            
    with sc2:
        # Display Big X's
        x_str = " X " * st.session_state.feud_strikes
        st.markdown(f"<div class='strike-x'>{x_str}</div>", unsafe_allow_html=True)

    with sc3:
        st.write("### Controls")
        nav_c1, nav_c2 = st.columns(2)
        with nav_c1:
            if st.button("⬅️ Prev"):
                prev_round()
                st.rerun()
        with nav_c2:
            if st.button("Next ➡️"):
                next_round()
                st.rerun()