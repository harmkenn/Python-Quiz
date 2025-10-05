import streamlit as st
import random
import time

# --- Page Setup ---
st.set_page_config(page_title="Scripture Match", layout="wide")

st.markdown("""
<style>
.big-font { font-size: 24px !important; text-align: center; }
.stButton button { height: 100px; width: 100%; font-size: 20px; white-space: normal; word-wrap: break-word; }
.team-current { font-weight: 700; color: green; }
</style>
""", unsafe_allow_html=True)

# --- Scripture Data ---
scriptures = {
"Joseph Smith—History 1:15–20": "Joseph Smith “saw two Personages, whose brightness and glory defy all description.”",
"Doctrine and Covenants 1:30": "“The only true and living church.”",
"Doctrine and Covenants 1:37–38": "“Whether by mine own voice or by the voice of my servants, it is the same.”",
"Doctrine and Covenants 6:36": "“Look unto me in every thought; doubt not, fear not.”",
"Doctrine and Covenants 8:2–3": "“I will tell you in your mind and in your heart, by the Holy Ghost.”",
"Doctrine and Covenants 13:1": "The Aaronic Priesthood “holds the keys of the ministering of angels, and of the gospel of repentance, and of baptism.”",
"Doctrine and Covenants 18:10–11": "“The worth of souls is great in the sight of God.”",
"Doctrine and Covenants 18:15–16": "“How great will be your joy if you should bring many souls unto me!”",
"Doctrine and Covenants 19:16–19": "“I, [Jesus Christ], have suffered these things for all.”",
"Doctrine and Covenants 21:4–6": "The prophet’s “word ye shall receive, as if from mine own mouth.”",
"Doctrine and Covenants 29:10–11": "“I will reveal myself from heaven with power and great glory … and dwell in righteousness with men on earth a thousand years.”",
"Doctrine and Covenants 49:15–17": "“Marriage is ordained of God.”",
"Doctrine and Covenants 58:42–43": "“He who has repented of his sins, the same is forgiven.”",
"Doctrine and Covenants 64:9–11": "“Of you it is required to forgive all men.”",
"Doctrine and Covenants 76:22–24": "“By [Jesus Christ] the worlds are and were created.”",
"Doctrine and Covenants 82:10": "“I, the Lord, am bound when ye do what I say.”",
"Doctrine and Covenants 84:20–22": "“In the ordinances thereof, the power of godliness is manifest.”",
"Doctrine and Covenants 88:118": "“Seek learning, even by study and also by faith.”",
"Doctrine and Covenants 89:18–21": "The blessings of the Word of Wisdom",
"Doctrine and Covenants 107:8": "“The Melchizedek Priesthood … has power and authority … to administer in spiritual things.”",
"Doctrine and Covenants 121:36, 41–42": "“The rights of the priesthood … cannot be controlled nor handled only on the principles of righteousness.”",
"Doctrine and Covenants 130:22–23": "“The Father has a body of flesh and bones … ; the Son also; but the Holy Ghost … is a personage of Spirit.”",
"Doctrine and Covenants 131:1–4": "“The new and everlasting covenant of marriage.”",
"Doctrine and Covenants 135:3": " Joseph Smith “brought forth the Book of Mormon, which he translated by the gift and power of God.”",
}

# --- Sidebar: Game Setup ---
st.sidebar.header("🎮 Game Setup")
num_pairs = st.sidebar.slider("Number of scripture pairs:", 6, len(scriptures), 6, step=2)
num_teams = st.sidebar.slider("Number of teams:", 2, 4, 4, step=1)

# --- Initialize game ---
if "initialized" not in st.session_state or st.sidebar.button("🔁 Start New Game"):
    selected_refs = random.sample(list(scriptures.items()), num_pairs)
    pairs = []
    for ref, text in selected_refs:
        pairs.append((ref, "reference"))
        pairs.append((text, "phrase"))
    random.shuffle(pairs)

    st.session_state.cards = pairs
    st.session_state.revealed = []
    st.session_state.matched = []
    st.session_state.turns = 0
    st.session_state.team_scores = [0] * num_teams
    st.session_state.current_team = 0
    st.session_state.flip_timer = None  # store time when cards were flipped
    st.session_state.initialized = True
    st.rerun()

# --- Check if 3 seconds passed to hide non-matching cards ---
if st.session_state.flip_timer:
    if time.time() - st.session_state.flip_timer >= 3:
        # hide the two revealed cards
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

    if st.session_state.flip_timer:  # ignore clicks during flip delay
        return

    st.session_state.revealed.append(index)

    if len(st.session_state.revealed) == 2:
        idx1, idx2 = st.session_state.revealed
        st.session_state.turns += 1
        if is_matching_pair(idx1, idx2):
            st.session_state.matched.extend([idx1, idx2])
            st.session_state.team_scores[st.session_state.current_team] += 1
            st.session_state.revealed = []
        else:
            # start 3-second timer for non-matching pair
            st.session_state.flip_timer = time.time()

# --- Display game board with numbers ---
st.markdown(f"### Current turn: Team {st.session_state.current_team + 1}")
cols_per_row = 6
cols = st.columns(cols_per_row)

for i, (card, ctype) in enumerate(st.session_state.cards):
    col = cols[i % cols_per_row]
    with col:
        if i in st.session_state.matched or i in st.session_state.revealed:
            # Show scripture text
            st.markdown(f"<div class='big-font'>{card}</div>", unsafe_allow_html=True)
        else:
            # Show unique number for hidden cards
            if st.button(f"{i+1}", key=f"card-{i}"):
                flip_card(i)


# --- Scores ---
st.markdown("---")
score_cols = st.columns(len(st.session_state.team_scores))
for t in range(len(st.session_state.team_scores)):
    label = f"Team {t+1}: {st.session_state.team_scores[t]}"
    if t == st.session_state.current_team:
        score_cols[t].markdown(f"<span class='team-current'>{label} ⬅️</span>", unsafe_allow_html=True)
    else:
        score_cols[t].markdown(label)

st.markdown(f"**Turns taken:** {st.session_state.turns}")

# --- Restart ---
if st.button("🔁 Restart Game"):
    st.session_state.clear()
    st.rerun()
