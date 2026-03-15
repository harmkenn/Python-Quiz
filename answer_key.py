import streamlit as st
import sys
import os

# Ensure we can find data.py in the same folder
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import data

def main():
    st.set_page_config(page_title="Feud Answers", page_icon="🗝️")
    st.title("🗝️ Answer Key")

    if hasattr(data, 'feud_data'):
        for i, round_data in enumerate(data.feud_data):
            # Use expanders to keep the list clean, but open by default or demand
            with st.expander(f"Round {i + 1}: {round_data['question']}", expanded=True):
                for j, (answer, points) in enumerate(round_data["answers"]):
                    st.write(f"**{j + 1}. {answer}** — {points}")
    else:
        st.error("Could not find 'feud_data' in data.py")

if __name__ == "__main__":
    main()