import streamlit as st
import random
import re

# --- Page Setup ---
if __name__ == "__main__":
    st.set_page_config(page_title="Italian Sentence", layout="wide")

# --- Load Italian Data ---
from italian_set import italian_set

def categorize_dataset():
    """Categorize words from italian_set by linguistic type"""
    categories = {
        "greeting": [],
        "food": [],
        "adjective": [],
        "person": [],
        "place": [],
        "object": [],
        "verb": [],
        "emotion": [],
        "other": []
    }
    
    # Manual categorization based on key patterns and keywords
    for english, italian in italian_set.items():
        english_lower = english.lower()
        
        if any(word in english_lower for word in ["hello", "hi", "good", "goodbye", "welcome", "thank", "sorry", "please", "excuse"]):
            categories["greeting"].append((english, italian))
        elif any(word in english_lower for word in ["water", "coffee", "tea", "milk", "bread", "cheese", "meat", "fish", "fruit", "apple", "banana", "orange", "rice", "pasta", "pizza", "salad", "soup", "dessert"]):
            categories["food"].append((english, italian))
        elif any(word in english_lower for word in ["big", "small", "beautiful", "ugly", "new", "old", "hot", "cold", "easy", "difficult", "fast", "slow", "happy", "sad", "angry", "tired", "hungry", "thirsty", "clean", "dirty", "expensive", "cheap", "happy", "excited", "bored", "worried", "scared", "confident", "calm", "nervous", "surprised", "proud", "ashamed", "embarrassed", "grateful", "jealous", "curious", "brave"]):
            categories["adjective"].append((english, italian))
        elif any(word in english_lower for word in ["man", "woman", "child", "boy", "girl", "friend", "family", "mother", "father", "brother", "sister", "son", "daughter", "husband", "wife", "teacher", "student", "doctor", "nurse", "police"]):
            categories["person"].append((english, italian))
        elif any(word in english_lower for word in ["house", "apartment", "hotel", "room", "restaurant", "bar", "store", "supermarket", "market", "school", "church", "hospital", "pharmacy", "airport", "station", "city", "town", "street", "square", "park", "bank", "beach", "mountain"]):
            categories["place"].append((english, italian))
        elif any(word in english_lower for word in ["car", "bus", "train", "bicycle", "phone", "computer", "table", "chair", "bed", "door", "window", "bag", "wallet", "ticket", "key", "book", "pen", "paper", "money", "card", "luggage", "map"]):
            categories["object"].append((english, italian))
        elif any(word in english_lower for word in ["to ", "be", "have", "go", "come", "do", "make", "eat", "drink", "see", "hear", "speak", "read", "write", "sleep", "work", "study", "buy", "pay", "help", "wait", "start", "finish", "walk", "run", "drive", "live", "love", "think", "believe", "feel", "find", "give", "take", "call", "ask", "answer", "open", "close", "bring", "use", "try", "learn", "remember", "forget", "cook", "clean", "wash", "shower", "shave", "dressed", "wake", "sit", "stand", "leave", "return", "stay", "visit", "travel", "plan", "organize", "iron"]):
            categories["verb"].append((english, italian))
        elif any(word in english_lower for word in ["fine", "hungry", "thirsty", "tired", "cold", "hot", "sick", "good", "bad"]):
            categories["emotion"].append((english, italian))
        else:
            categories["other"].append((english, italian))
    
    return categories

def generate_sentence_pair():
    """Generate an English sentence from dataset words, then translate to Italian"""
    categories = categorize_dataset()
    
    # Define sentence patterns
    patterns = [
        # Pattern: "[verb] the [object]"
        lambda: {
            "parts": [random.choice(categories["verb"])[0], "the", random.choice(categories["object"])[0]],
        } if categories["verb"] and categories["object"] else None,
        
        # Pattern: "I [verb] [food/object]"
        lambda: {
            "parts": ["I", random.choice(categories["verb"])[0], random.choice(categories["food"] + categories["object"])[0]],
        } if categories["verb"] and (categories["food"] or categories["object"]) else None,
        
        # Pattern: "The [person] [verb] the [object]"
        lambda: {
            "parts": ["The", random.choice(categories["person"])[0], random.choice(categories["verb"])[0], "the", random.choice(categories["object"])[0]],
        } if categories["person"] and categories["verb"] and categories["object"] else None,
        
        # Pattern: "The [adjective] [person]"
        lambda: {
            "parts": ["The", random.choice(categories["adjective"])[0], random.choice(categories["person"])[0]],
        } if categories["adjective"] and categories["person"] else None,
        
        # Pattern: "I like [food]"
        lambda: {
            "parts": ["I", "like", random.choice(categories["food"])[0]],
        } if categories["food"] else None,
        
        # Pattern: "[greeting]"
        lambda: {
            "parts": [random.choice(categories["greeting"])[0]],
        } if categories["greeting"] else None,
    ]
    
    # Get a valid pattern
    valid_patterns = [p for p in patterns if p() is not None]
    if not valid_patterns:
        # Fallback: just pick two random dictionary items
        items = random.sample(list(italian_set.items()), min(3, len(italian_set)))
        english_parts = [item[0] for item in items]
    else:
        result = random.choice(valid_patterns)()
        english_parts = result["parts"]
    
    # Create English sentence
    english_sentence = " ".join(english_parts)
    
    # Translate to Italian
    italian_parts = []
    for part in english_parts:
        italian_parts.append(italian_set.get(part, part))
    italian_sentence = " ".join(italian_parts)
    
    return {
        "english_sentence": english_sentence,
        "english_parts": english_parts,
        "italian_sentence": italian_sentence,
    }

def app():
    st.markdown("""
    <style>
    .big-font { font-size: 24px !important; text-align: center; font-weight: bold; }
    .stButton button { height: 60px; width: 100%; font-size: 16px; white-space: normal; word-wrap: break-word; padding: 0.25rem 0.5rem !important; }
    .team-current { font-weight: 700; color: green; }
    .score-label { font-size: 24px; font-weight: bold; text-align: center; }
    .word-space { margin-top: 8px; }
    .word-selected { border: 3px solid yellow !important; background-color: #ffffcc !important; }
    .word-correct { border: 3px solid green !important; background-color: #ccffcc !important; }
    .sentence-box { font-size: 20px; padding: 15px; background-color: #2a2a2a; border-radius: 5px; text-align: center; margin-bottom: 20px; color: #ffffff; }
    .selected-words { font-size: 18px; padding: 10px; background-color: #2a2a2a; border-radius: 5px; text-align: center; margin-bottom: 15px; min-height: 40px; color: #ffffff; }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar: Game Setup ---
    st.sidebar.header("🎮 Game Setup")
    difficulty = st.sidebar.radio("Difficulty:", ["Easy (3-4 words)", "Medium (4-5 words)", "Hard (6+ words)"])
    num_extra_words = {"Easy (3-4 words)": 3, "Medium (4-5 words)": 5, "Hard (6+ words)": 7}[difficulty]

    # --- Initialize game ---
    if "sentence_initialized" not in st.session_state:
        st.session_state.sentence_initialized = False
    if "just_correct" not in st.session_state:
        st.session_state.just_correct = False
    if "just_wrong" not in st.session_state:
        st.session_state.just_wrong = False

    if st.sidebar.button("🔁 Start New Game") or not st.session_state.sentence_initialized:
        sentence_pair = generate_sentence_pair()
        
        # Create word pool with correct English words and extra distractor words
        correct_words = sentence_pair["english_parts"].copy()
        all_words = correct_words.copy()
        
        # Add extra distractor words from italian_set
        all_english_words = list(italian_set.keys())
        available_words = [w for w in all_english_words if w not in correct_words]
        extra_words = random.sample(available_words, min(num_extra_words, len(available_words)))
        all_words.extend(extra_words)
        random.shuffle(all_words)
        
        st.session_state.current_sentence = sentence_pair
        st.session_state.word_pool = all_words
        st.session_state.selected_words = []
        st.session_state.score = 0
        st.session_state.total_attempts = 0
        st.session_state.sentence_initialized = True
        st.session_state.just_correct = False
        st.session_state.just_wrong = False
        st.rerun()

    # --- Helper functions ---
    def check_answer():
        correct_words = st.session_state.current_sentence["english_parts"]
        if st.session_state.selected_words == correct_words:
            st.session_state.score += 1
            return True
        return False

    def select_word(word):
        if word not in st.session_state.selected_words:
            st.session_state.selected_words.append(word)

    def unselect_word(word_idx):
        if 0 <= word_idx < len(st.session_state.selected_words):
            st.session_state.selected_words.pop(word_idx)

    # --- Display Italian Sentence ---
    st.markdown(f"<div class='sentence-box'>Translate to English:<br><strong>{st.session_state.current_sentence['italian_sentence']}</strong></div>", unsafe_allow_html=True)

    # --- Display Previously Selected Words ---
    if st.session_state.selected_words:
        selected_text = " → ".join(st.session_state.selected_words)
        st.markdown(f"<div class='selected-words'><strong>Your Selection:</strong><br>{selected_text}</div>", unsafe_allow_html=True)
        
        # Option to remove the last selected word
        col1, col2 = st.columns(2)
        with col1:
            if st.button("↶ Remove Last Word"):
                unselect_word(-1)
                st.rerun()
        with col2:
            if st.button("🗑️ Clear All"):
                st.session_state.selected_words = []
                st.rerun()
    else:
        st.markdown("<div class='selected-words'><em>Click words below to build the sentence...</em></div>", unsafe_allow_html=True)

    st.markdown("---")

    # --- Display Word Pool ---
    st.markdown("### Choose Words:")
    cols_per_row = 4
    num_words = len(st.session_state.word_pool)

    for start in range(0, num_words, cols_per_row):
        cols = st.columns(cols_per_row)
        for i, col in enumerate(cols):
            word_idx = start + i
            if word_idx >= num_words:
                continue
            word = st.session_state.word_pool[word_idx]
            with col:
                if st.button(f"{word}", key=f"word-{word_idx}"):
                    select_word(word)
                    st.rerun()

    st.markdown("---")

    # --- Check Answer ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Check Answer") and st.session_state.selected_words:
            st.session_state.total_attempts += 1
            if check_answer():
                st.session_state.just_correct = True
                st.session_state.just_wrong = False
                st.rerun()
            else:
                st.session_state.just_correct = False
                st.session_state.just_wrong = True
                st.rerun()

    # --- Show Results ---
    if st.session_state.just_correct:
        st.success("🎉 Correct! Great job!")
        st.balloons()
        if st.button("📝 Next Sentence"):
            st.session_state.sentence_initialized = False
            st.session_state.just_correct = False
            st.session_state.selected_words = []
            st.rerun()
    
    if st.session_state.just_wrong:
        correct_text = " ".join(st.session_state.current_sentence["english_parts"])
        st.error(f"❌ Not quite right. The correct answer is:\n\n**{correct_text}**")
        if st.button("🔄 Try Again"):
            st.session_state.selected_words = []
            st.session_state.just_wrong = False
            st.rerun()

    # --- Score ---
    st.markdown("---")
    st.markdown(f"**Score:** {st.session_state.score} correct")
    if st.session_state.total_attempts > 0:
        accuracy = (st.session_state.score / st.session_state.total_attempts) * 100
        st.markdown(f"**Accuracy:** {accuracy:.1f}% ({st.session_state.score}/{st.session_state.total_attempts})")

if __name__ == "__main__":
    app()
