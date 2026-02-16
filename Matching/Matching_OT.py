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
"Moses 1:39": "“This is my work and my glory—to bring to pass the immortality and eternal life of man.”",
"Moses 7:18": "“The Lord called his people Zion, because they were of one heart and one mind.”",
"Abraham 2:9–11": "The Lord promised Abraham that his seed would “bear this ministry and Priesthood unto all nations.”",
"Abraham 3:22–23": "As spirits we “were organized before the world was.”",
"Genesis 1:26–27": "“God created man in his own image.”",
"Genesis 2:24": "“A man … shall cleave unto his wife: and they shall be one.”",
"Genesis 39:9": "“How then can I do this great wickedness, and sin against God?”",
"Exodus 20:3–17": "The Ten Commandments",
"Joshua 24:15": "“Choose you this day whom ye will serve.”",
"Psalm 24:3–4": "“Who shall stand in his holy place? He that hath clean hands, and a pure heart.”",
"Proverbs 3:5–6": "“Trust in the Lord with all thine heart … and he shall direct thy paths.”",
"Isaiah 1:18": "“Though your sins be as scarlet, they shall be as white as snow.”",
"Isaiah 5:20": "“Woe unto them that call evil good, and good evil.”",
"Isaiah 29:13–14": "The restoration of the gospel is “a marvellous work and a wonder.”",
"Isaiah 53:3–5": "“Surely [Jesus Christ] hath borne our griefs, and carried our sorrows.”",
"Isaiah 58:6–7": "The blessings of a proper fast",
"Isaiah 58:13–14": "“Turn away … from doing thy pleasure on my holy day; and call the sabbath a delight.”",
"Jeremiah 1:4–5": "“Before I formed thee in the belly … I ordained thee a prophet unto the nations.”",
"Ezekiel 3:16–17": "The prophet is “a watchman unto the house of Israel.”",
"Ezekiel 37:15–17": "The Bible and the Book of Mormon “shall become one in thine hand.”",
"Daniel 2:44–45": "God shall “set up a kingdom, which shall never be destroyed.”",
"Amos 3:7": "“The Lord God … revealeth his secret unto his servants the prophets.”",
"Malachi 3:8–10": "The blessings of paying tithing",
"Malachi 4:5–6": "Elijah “shall turn … the heart of the children to their fathers.”",
}
extra = {
"Moses 1:39": "“This is my work and my glory—to bring to pass the immortality and eternal life of man.”",
"Moses 7:18": "“The Lord called his people Zion, because they were of one heart and one mind.”",
"Abraham 2:9–11": "The Lord promised Abraham that his seed would “bear this ministry and Priesthood unto all nations.”",
"Abraham 3:22–23": "As spirits we “were organized before the world was.”",
"Genesis 1:26–27": "“God created man in his own image.”",
"Genesis 2:24": "“A man … shall cleave unto his wife: and they shall be one.”",
"Genesis 39:9": "“How then can I do this great wickedness, and sin against God?”",
"Exodus 20:3–17": "The Ten Commandments",
"Joshua 24:15": "“Choose you this day whom ye will serve.”",
"Psalm 24:3–4": "“Who shall stand in his holy place? He that hath clean hands, and a pure heart.”",
"Proverbs 3:5–6": "“Trust in the Lord with all thine heart … and he shall direct thy paths.”",
"Isaiah 1:18": "“Though your sins be as scarlet, they shall be as white as snow.”",
"Isaiah 5:20": "“Woe unto them that call evil good, and good evil.”",
"Isaiah 29:13–14": "The restoration of the gospel is “a marvellous work and a wonder.”",
"Isaiah 53:3–5": "“Surely [Jesus Christ] hath borne our griefs, and carried our sorrows.”",
"Isaiah 58:6–7": "The blessings of a proper fast",
"Isaiah 58:13–14": "“Turn away … from doing thy pleasure on my holy day; and call the sabbath a delight.”",
"Jeremiah 1:4–5": "“Before I formed thee in the belly … I ordained thee a prophet unto the nations.”",
"Ezekiel 3:16–17": "The prophet is “a watchman unto the house of Israel.”",
"Ezekiel 37:15–17": "The Bible and the Book of Mormon “shall become one in thine hand.”",
"Daniel 2:44–45": "God shall “set up a kingdom, which shall never be destroyed.”",
"Amos 3:7": "“The Lord God … revealeth his secret unto his servants the prophets.”",
"Malachi 3:8–10": "The blessings of paying tithing",
"Malachi 4:5–6": "Elijah “shall turn … the heart of the children to their fathers.”",

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
