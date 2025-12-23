import streamlit as st
import random
import time

# --- Constants ---
TEAM_COLORS = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400"]
COLS_PER_ROW = 6
FLIP_DELAY = 3  # seconds

# --- Scripture Data ---
SCRIPTURES = {
    "Moses 1:39": "“This is my work and my glory—to bring to pass the immortality and eternal life of man.”",
    "Moses 7:18": "“The Lord called his people Zion, because they were of one heart and one mind.”",
    "Abraham 2:9–11": "The Lord promised Abraham that his seed would “bear this ministry and Priesthood unto all nations.”",
    # Add more scriptures here...
}

# --- Helper Functions ---
def initialize_game(num_pairs, num_teams):
    """Initialize game state."""
    selected_refs = random.sample(list(SCRIPTURES.items()), num_pairs)
    pairs = [(ref, "reference") for ref, text in selected_refs] + [(text, "phrase") for ref, text in selected_refs]
    random.shuffle(pairs)

    return {
        "cards": pairs,
        "revealed": [],
        "matched": [],
        "matched_by_team": {},
        "turns": 0,
        "team_scores": [0] * num_teams,
        "current_team": random.randint(0, num_teams - 1),
        "flip_timer": None,
        "all_revealed": False,
    }

def is_matching_pair(card1, card2):
    """Check if two cards form a matching pair."""
    return (card1 in SCRIPTURES and SCRIPTURES[card1] == card2) or \
           (card2 in SCRIPTURES and SCRIPTURES[card2] == card1)

def flip_card(index, state):
    """Handle card flip logic."""
    if index in state["matched"] or index in state["revealed"] or state["flip_timer"] or state["all_revealed"]:
        return

    state["revealed"].append(index)

    if len(state["revealed"]) == 2:
        idx1, idx2 = state["revealed"]
        state["turns"] += 1
        card1, _ = state["cards"][idx1]
        card2, _ = state["cards"][idx2]

        if is_matching_pair(card1, card2):
            state["matched"].extend([idx1, idx2])
            team = state["current_team"]
            state["matched_by_team"][idx1] = team
            state["matched_by_team"][idx2] = team
            state["team_scores"][team] += 1
            state["revealed"] = []
        else:
            state["flip_timer"] = time.time()

def render_card(index, state, team_colors):
    """Render a single card."""
    card, ctype = state["cards"][index]
    if index in state["matched"]:
        team = state["matched_by_team"].get(index, 0)
        color = team_colors[team]
        st.markdown(f"<div class='big-font' style='color:{color}'>{card}</div>", unsafe_allow_html=True)
    elif state["all_revealed"] or index in state["revealed"]:
        st.markdown(f"<div class='big-font'>{card}</div>", unsafe_allow_html=True)
    else:
        card_letter = index_to_letter(index)
        if st.button(f"{card_letter}", key=f"card-{index}"):
            flip_card(index, state)

def index_to_letter(index):
    """Convert index to letter (A, B, C, ..., Z, AA, BB, etc.)."""
    if index < 26:
        return chr(65 + index)  # A-Z
    else:
        return chr(65 + (index % 26)) * ((index // 26) + 1)

# --- Streamlit App ---
st.set_page_config(page_title="Scripture Match", layout="wide")

# Sidebar: Game Setup
st.sidebar.header("🎮 Game Setup")
num_pairs = st.sidebar.slider("Number of scripture pairs:", 6, len(SCRIPTURES), 6, step=1)
num_teams = st.sidebar.slider("Number of teams:", 2, 4, 4, step=1)
team_colors = TEAM_COLORS[:num_teams]

# Initialize game state
if "game_state" not in st.session_state or st.sidebar.button("🔁 Start New Game"):
    st.session_state.game_state = initialize_game(num_pairs, num_teams)
    st.rerun()

state = st.session_state.game_state

# Check timer to flip back non-matching pair
if state["flip_timer"] and time.time() - state["flip_timer"] >= FLIP_DELAY:
    state["revealed"] = []
    state["current_team"] = (state["current_team"] + 1) % len(state["team_scores"])
    state["flip_timer"] = None
    st.rerun()

# Reveal / Hide Buttons
reveal_col, hide_col = st.columns(2)
with reveal_col:
    if st.sidebar.button("👁️ Reveal All"):
        state["all_revealed"] = True
        state["revealed"] = list(range(len(state["cards"])))
        st.rerun()

with hide_col:
    if st.sidebar.button("🙈 Hide All"):
        state["all_revealed"] = False
        state["revealed"] = []
        st.rerun()

# Display game board
st.markdown(f"### Current turn: Team {state['current_team'] + 1}")
num_cards = len(state["cards"])

for start in range(0, num_cards, COLS_PER_ROW):
    cols = st.columns(COLS_PER_ROW)
    for i, col in enumerate(cols):
        idx = start + i
        if idx >= num_cards:
            continue
        with col:
            render_card(idx, state, team_colors)

# Scores
st.markdown("---")
score_cols = st.columns(len(state["team_scores"]))
for t in range(len(state["team_scores"])):
    color = team_colors[t]
    label = f"Team {t+1}: {state['team_scores'][t]}"
    if t == state["current_team"]:
        score_cols[t].markdown(f"<div class='score-label team-current' style='color:{color}'>{label} ⬅️</div>", unsafe_allow_html=True)
    else:
        score_cols[t].markdown(f"<div class='score-label' style='color:{color}'>{label}</div>", unsafe_allow_html=True)

st.markdown(f"**Turns taken:** {state['turns']}")

# Game Over
if len(state["matched"]) == len(state["cards"]):
    st.success("🎉 Game Over! All pairs matched!")
    winner = max(range(len(state["team_scores"])), key=lambda i: state["team_scores"][i])
    st.info(f"🏆 Winner: Team {winner + 1} with {state['team_scores'][winner]} points!")

# Restart
if st.button("🔁 Restart Game"):
    st.session_state.clear()
    st.rerun()
