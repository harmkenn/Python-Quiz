import streamlit as st
import random
import time

# --- Page Setup ---
if __name__ == "__main__":
    st.set_page_config(page_title="Italian Match", layout="wide")

# --- Load Italian Data (1000 common words/phrases) ---
from italian_1000_words import italian_words   # <-- You will create this file

# --- Helper function to convert index to letter ---
def index_to_letter(index):
    if index < 26:
        return chr(65 + index)
    else:
        return chr(65 + (index % 26)) * ((index // 26) + 1)

def app():
    st.markdown("""
    <style>
    .big-font { font-size: 20px !important; text-align: center; }
    .stButton button { height: 100px; width: 100%; font-size: 20px; white-space: normal; word-wrap: break-word; }
    .team-current { font-weight: 700; color: green; }
    .score-label { font-size: 24px; font-weight: bold; text-align: center; }
    .row-space { margin-top: 25px; }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar: Game Setup ---
    st.sidebar.header("🎮 Game Setup")
    num_pairs = st.sidebar.slider("Number of word pairs:", 10, len(italian_words), 20, step=1)
    num_teams = st.sidebar.slider("Number of teams:", 2, 4, 4, step=1)

    team_colors = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400"][:num_teams]

    # --- Initialize game ---
    if "initialized" not in st.session_state:
        st.session_state.initialized = False

    if st.sidebar.button("🔁 Start New Game") or not st.session_state.initialized:
        selected = random.sample(list(italian_words.items()), num_pairs)
        pairs = []
        for eng, ita in selected:
            pairs.append((eng, "eng"))
            pairs.append((ita, "ita"))
        random.shuffle(pairs)

        st.session_state.cards = pairs
        st.session_state.revealed = []
        st.session_state.matched = []
        st.session_state.matched_by_team = {}
        st.session_state.turns = 0
        st.session_state.team_scores = [0] * num_teams
        st.session_state.current_team = random.randint(0, num_teams - 1)
        st.session_state.flip_timer = None
        st.session_state.all_revealed = False
        st.session_state.initialized = True
        st.rerun()

    # --- Timer for flipping back ---
    if st.session_state.flip_timer:
        if time.time() - st.session_state.flip_timer >= 3:
            st.session_state.revealed = []
            st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)
            st.session_state.flip_timer = None
            st.rerun()

    # --- Matching logic ---
    def is_matching_pair(idx1, idx2):
        card1, type1 = st.session_state.cards[idx1]
        card2, type2 = st.session_state.cards[idx2]
        if type1 == type2:
            return False
        if type1 == "eng":
            return italian_words[card1] == card2
        else:
            return italian_words[card2] == card1

    def flip_card(index):
        if index in st.session_state.matched or index in st.session_state.revealed:
            return
        if st.session_state.flip_timer or st.session_state.all_revealed:
            return

        st.session_state.revealed.append(index)

        if len(st.session_state.revealed) == 2:
            idx1, idx2 = st.session_state.revealed
            st.session_state.turns += 1
            if is_matching_pair(idx1, idx2):
                st.session_state.matched.extend([idx1, idx2])
                team = st.session_state.current_team
                st.session_state.matched_by_team[idx1] = team
                st.session_state.matched_by_team[idx2] = team
                st.session_state.team_scores[team] += 1
                st.session_state.revealed = []
            else:
                st.session_state.flip_timer = time.time()

    # --- Reveal / Hide ---
    reveal_col, hide_col = st.columns(2)
    with reveal_col:
        if st.sidebar.button("👁️ Reveal All"):
            st.session_state.all_revealed = True
            st.session_state.revealed = list(range(len(st.session_state.cards)))
            st.rerun()

    with hide_col:
        if st.sidebar.button("🙈 Hide All"):
            st.session_state.all_revealed = False
            st.session_state.revealed = []
            st.rerun()

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
                    st.markdown(f"<div class='big-font' style='color:{color}'>{card}</div>", unsafe_allow_html=True)
                elif st.session_state.all_revealed or idx in st.session_state.revealed:
                    st.markdown(f"<div class='big-font'>{card}</div>", unsafe_allow_html=True)
                else:
                    letter = index_to_letter(idx)
                    if st.button(f"{letter}", key=f"card-{idx}"):
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

