import streamlit as st
import random
import time

# --- Page Setup ---
st.set_page_config(page_title="Scripture Match", layout="wide")

st.markdown("""
<style>
.big-font { font-size: 20px !important; text-align: center; }
.stButton button { height: 100px; width: 100%; font-size: 20px; white-space: normal; word-wrap: break-word; }
.team-current { font-weight: 700; color: green; }
.score-label { font-size: 24px; font-weight: bold; text-align: center; }
.row-space { margin-top: 25px; }  /* 👈 space between rows */
</style>
""", unsafe_allow_html=True)

# --- Scripture Data ---
scriptures = {
"Article of Faith 1": "We believe in God, the Eternal Father, and in His Son, Jesus Christ, and in the Holy Ghost.",
"Article of Faith 2": "We believe that men will be punished for their own sins, and not for Adam's transgression.",
"Article of Faith 3": "We believe that through the Atonement of Christ, all mankind may be saved, by obedience to the laws and ordinances of the Gospel.",
"Article of Faith 4": "We believe that the first principles and ordinances of the Gospel are: first, Faith in the Lord Jesus Christ; second, Repentance; third, Baptism by immersion for the remission of sins; fourth, Laying on of hands for the gift of the Holy Ghost.",
"Article of Faith 5": "We believe that a man must be called of God, by prophecy, and by the laying on of hands by those who are in authority, to preach the Gospel and administer in the ordinances thereof.",
"Article of Faith 6": "We believe in the same organization that existed in the Primitive Church, namely, apostles, prophets, pastors, teachers, evangelists, and so forth.",
"Article of Faith 7": "We believe in the gift of tongues, prophecy, revelation, visions, healing, interpretation of tongues, and so forth.",
"Article of Faith 8": "We believe the Bible to be the word of God as far as it is translated correctly; we also believe the Book of Mormon to be the word of God.",
"Article of Faith 9": "We believe all that God has revealed, all that He does now reveal, and we believe that He will yet reveal many great and important things pertaining to the Kingdom of God.",
"Article of Faith 10": "We believe in the literal gathering of Israel and in the restoration of the Ten Tribes; that Zion (the New Jerusalem) will be built upon the American continent; that Christ will reign personally upon the earth; and, that the earth will be renewed and receive its paradisiacal glory.",
"Article of Faith 11": "We claim the privilege of worshiping Almighty God according to the dictates of our own conscience, and allow all men the same privilege, let them worship how, where, or what they may.",
"Article of Faith 12": "We believe in being subject to kings, presidents, rulers, and magistrates, in obeying, honoring, and sustaining the law.",
"Article of Faith 13": "We believe in being honest, true, chaste, benevolent, virtuous, and in doing good to all men; indeed, we may say that we follow the admonition of Paul—We believe all things, we hope all things, we have endured many things, and hope to be able to endure all things. If there is anything virtuous, lovely, or of good report or praiseworthy, we seek after these things.",
}

# --- Helper function to convert index to letter ---
def index_to_letter(index):
    """Convert index to letter (A, B, C, ..., Z, AA, BB, etc.)"""
    if index < 26:
        return chr(65 + index)  # A-Z
    else:
        # For more than 26 cards, use AA, BB, CC, etc.
        return chr(65 + (index % 26)) * ((index // 26) + 1)

# --- Sidebar: Game Setup ---
st.sidebar.header("🎮 Game Setup")
num_pairs = st.sidebar.slider("Number of scripture pairs:", 6, len(scriptures), 6, step=1)
num_teams = st.sidebar.slider("Number of teams:", 2, 4, 4, step=1)

# Define team colors
team_colors = ["#FF4B4B", "#007BFF", "#2ECC71", "#F4B400"]
team_colors = team_colors[:num_teams]

# --- Initialize game (only shuffle when "Start New Game" pressed) ---
if "initialized" not in st.session_state:
    st.session_state.initialized = False

if st.sidebar.button("🔁 Start New Game") or not st.session_state.initialized:
    selected_refs = random.sample(list(scriptures.items()), num_pairs)
    pairs = []
    for ref, text in selected_refs:
        pairs.append((ref, "reference"))
        pairs.append((text, "phrase"))
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


# --- Check timer to flip back non-matching pair ---
if st.session_state.flip_timer:
    if time.time() - st.session_state.flip_timer >= 3:
        st.session_state.revealed = []
        st.session_state.current_team = (st.session_state.current_team + 1) % len(st.session_state.team_scores)
        st.session_state.flip_timer = None
        st.rerun()

# --- Helper functions ---
def is_matching_pair(idx1, idx2):
    card1, _ = st.session_state.cards[idx1]
    card2, _ = st.session_state.cards[idx2]
    return (card1 in scriptures and scriptures[card1] == card2) or \
           (card2 in scriptures and scriptures[card2] == card1)

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

# --- Reveal / Hide Buttons ---
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

# --- Display game board ---
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
                card_letter = index_to_letter(idx)
                if st.button(f"{card_letter}", key=f"card-{idx}"):
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