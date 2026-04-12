import streamlit as st
import random

# --- Page Setup ---
if __name__ == "__main__":
    st.set_page_config(page_title="Italian Match", layout="wide")

# --- Load Italian Data (1000 common words/phrases) ---
from italian_set import italian_set   # <-- You will create this file

def app():
    st.markdown("""
    <style>
    .big-font { font-size: 20px !important; text-align: center; }
    .stButton button { height: 60px; width: 100%; font-size: 16px; white-space: normal; word-wrap: break-word; padding: 0.25rem 0.5rem !important; }
    .team-current { font-weight: 700; color: green; }
    .score-label { font-size: 24px; font-weight: bold; text-align: center; }
    .row-space { margin-top: 8px; }
    .card-selected { border: 3px solid yellow !important; }
    .card-matched { opacity: 0.5; }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar: Game Setup ---
    st.sidebar.header("🎮 Game Setup")
    num_pairs = st.sidebar.slider("Number of word pairs:", 10, len(italian_set), 20, step=1)
    num_teams = st.sidebar.slider("Number of teams:", 2, 4, 4, step=1)

    team_colors = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400"][:num_teams]

    # --- Initialize game ---
    if "initialized" not in st.session_state:
        st.session_state.initialized = False

    if st.sidebar.button("🔁 Start New Game") or not st.session_state.initialized:
        selected = random.sample(list(italian_set.items()), num_pairs)
        pairs = []
        for eng, ita in selected:
            pairs.append((eng, "eng"))
            pairs.append((ita, "ita"))
        random.shuffle(pairs)

        st.session_state.cards = pairs
        st.session_state.selected = []
        st.session_state.matched = []
        st.session_state.matched_by_team = {}
        st.session_state.turns = 0
        st.session_state.team_scores = [0] * num_teams
        st.session_state.current_team = random.randint(0, num_teams - 1)
        st.session_state.initialized = True
        st.rerun()

    # --- Matching logic ---
    def is_matching_pair(idx1, idx2):
        card1, type1 = st.session_state.cards[idx1]
        card2, type2 = st.session_state.cards[idx2]
        if type1 == type2:
            return False
        if type1 == "eng":
            return italian_set[card1] == card2
        else:
            return italian_set[card2] == card1

    def flip_card(index):
        if index in st.session_state.matched or index in st.session_state.selected:
            return

        st.session_state.selected.append(index)

        if len(st.session_state.selected) == 2:
            idx1, idx2 = st.session_state.selected
            st.session_state.turns += 1
            if is_matching_pair(idx1, idx2):
                st.session_state.matched.extend([idx1, idx2])
                team = st.session_state.current_team
                st.session_state.matched_by_team[idx1] = team
                st.session_state.matched_by_team[idx2] = team
                st.session_state.team_scores[team] += 1
                st.session_state.selected = []
            else:
                st.session_state.selected = []
                st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)

    # --- Display Board ---
    st.markdown(f"### Current turn: Team {st.session_state.current_team + 1}")
    cols_per_row = 6
    num_cards = len(st.session_state.cards)

    for start in range(0, num_cards, cols_per_row):
        cols = st.columns(cols_per_row)
        for i, col in enumerate(cols):
            idx = start + i
            if idx >= num_cards:
                continue
            card, ctype = st.session_state.cards[idx]
            with col:
                if idx in st.session_state.matched:
                    team = st.session_state.matched_by_team.get(idx, 0)
                    color = team_colors[team]
                    st.markdown(f"<div class='big-font card-matched' style='color:{color}'>{card}</div>", unsafe_allow_html=True)
                else:
                    is_selected = idx in st.session_state.selected
                    button_style = " card-selected" if is_selected else ""
                    if st.button(f"{card}", key=f"card-{idx}"):
                        flip_card(idx)
        st.markdown("<div class='row-space'></div>", unsafe_allow_html=True)

    # --- Scores ---
    st.markdown("---")
    score_cols = st.columns(len(st.session_state.team_scores))
    for t in range(len(st.session_state.team_scores)):
        color = team_colors[t]
        label = f"Team {t+1}: {st.session_state.team_scores[t]}"
        if t == st.session_state.current_team:
            score_cols[t].markdown(f"<div class='score-label team-current' style='color:{color}'>{label} ⬅️</div>", unsafe_allow_html=True)
        else:
            score_cols[t].markdown(f"<div class='score-label' style='color:{color}'>{label}</div>", unsafe_allow_html=True)

    st.markdown(f"**Turns taken:** {st.session_state.turns}")

    # --- Game Over ---
    if len(st.session_state.matched) == len(st.session_state.cards):
        st.success("🎉 Game Over! All pairs matched!")
        winner = max(range(len(st.session_state.team_scores)), key=lambda i: st.session_state.team_scores[i])
        st.info(f"🏆 Winner: Team {winner + 1} with {st.session_state.team_scores[winner]} points!")

    # --- Restart ---
    if st.button("🔁 Restart Game"):
        st.session_state.clear()
        st.rerun()

if __name__ == "__main__":
    app()

