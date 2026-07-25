import streamlit as st
import pandas as pd
from pathlib import Path
import random


@st.cache_data
def load_words(csv_path: Path) -> pd.DataFrame:
    return pd.read_csv(csv_path)


def main():
    st.set_page_config(page_title="Italian 1000 Words", layout="wide")
    st.title("Italian — 1000 Words")

    csv_path = Path(__file__).parent / "1000 Words.csv"
    if not csv_path.exists():
        st.error(f"CSV not found at {csv_path}")
        return

    df = load_words(csv_path)

    st.sidebar.header("Filters")
    q = st.sidebar.text_input("Search (Italian or English)")
    parts = ["All"] + sorted(df['Part'].dropna().unique().tolist())
    part_choice = st.sidebar.selectbox("Part", parts)
    shuffle = st.sidebar.checkbox("Shuffle table rows", value=False)

    mask = pd.Series(True, index=df.index)
    if q:
        mask &= df['Italiano'].str.contains(q, case=False, na=False) | df['English'].str.contains(q, case=False, na=False)
    if part_choice != "All":
        mask &= df['Part'] == part_choice

    filtered = df[mask]
    if shuffle:
        filtered = filtered.sample(frac=1).reset_index(drop=True)

    st.markdown(f"**Total words:** {len(df)} — **Showing:** {len(filtered)}")

    st.dataframe(filtered, use_container_width=True)

    csv_bytes = filtered.to_csv(index=False).encode('utf-8')
    st.download_button("Download filtered CSV", data=csv_bytes, file_name="1000_words_filtered.csv", mime="text/csv")

    st.markdown("---")
    st.header("Flashcards")
    if 'card_idx' not in st.session_state:
        st.session_state.card_idx = None
        st.session_state.revealed = False

    cols = st.columns([2, 1])
    with cols[0]:
        if st.button("Next card") or st.session_state.card_idx is None:
            if len(filtered) == 0:
                st.info("No words to review with current filters.")
            else:
                st.session_state.card_idx = random.randint(0, len(filtered) - 1)
                st.session_state.revealed = False

        if st.session_state.card_idx is not None and len(filtered) > 0:
            row = filtered.iloc[st.session_state.card_idx]
            st.subheader(row['Italiano'])
            if st.button("Reveal"):
                st.session_state.revealed = True
            if st.session_state.revealed:
                st.write(f"**English:** {row['English']}")
                st.write(f"**Part:** {row['Part']}")

    with cols[1]:
        st.write("\n")
        st.write("Use the filters to narrow the set used for flashcards.")


if __name__ == '__main__':
    main()
