# pages/buzzer.py
import streamlit as st
import time

from state import BUZZ_STATE

st.set_page_config(page_title="Team Buzzer", layout="centered")

st.title("🔔 Team Buzzer")

st.write("Enter your **team name** and wait for the teacher to start a question.")

team_name = st.text_input("Team name", value="", max_chars=30)

if "last_buzz_result" not in st.session_state:
    st.session_state.last_buzz_result = None
if "last_buzz_time" not in st.session_state:
    st.session_state.last_buzz_time = None

buzz_button_disabled = team_name.strip() == ""

if st.button("🔴 BUZZ IN!", disabled=buzz_button_disabled, use_container_width=True):
    if not team_name.strip():
        st.warning("Please enter a team name first.")
    else:
        success, first = BUZZ_STATE.buzz(team_name.strip())
        st.session_state.last_buzz_result = success
        st.session_state.last_buzz_time = time.time()

if st.session_state.last_buzz_result is True:
    st.success("You buzzed in FIRST! Wait for the teacher.")
elif st.session_state.last_buzz_result is False:
    first = BUZZ_STATE.get()
    if first:
        st.error(f"Too late! **{first['team']}** buzzed in first.")
    else:
        st.info("No active question or buzzers have been cleared.")

st.markdown("---")
st.caption("Keep this page open. Tap the button as soon as you know the answer.")
