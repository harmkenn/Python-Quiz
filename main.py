import streamlit as st
import sys
import os
import importlib.util

# --- Page Config (Must be first) ---
st.set_page_config(page_title="LDS Games Launcher", layout="wide")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Helper to Load Game Modules ---
def load_game_module(folder_name, file_name, unique_module_name):
    """Loads a python file from a folder as a module, handling sys.path for dependencies."""
    file_path = os.path.join(ROOT_DIR, folder_name, file_name)
    game_dir = os.path.join(ROOT_DIR, folder_name)

    # Add game folder to sys.path so internal imports (like 'import state') work
    if game_dir not in sys.path:
        sys.path.insert(0, game_dir)

    try:
        spec = importlib.util.spec_from_file_location(unique_module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[unique_module_name] = module
        spec.loader.exec_module(module)
        return module
    finally:
        # Clean up path to prevent conflicts between games
        if game_dir in sys.path:
            sys.path.remove(game_dir)

# --- Main Launcher ---
def main():
    if "current_game" not in st.session_state:
        st.session_state.current_game = "Home"

    # Store the current game choice to detect changes
    previous_game = st.session_state.current_game

    with st.sidebar:
        st.header("🚀 Game Launcher")
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_game = "Home"
        
        st.markdown("---")
        st.subheader("Select Game")
        
        if st.button("🧩 Matching", use_container_width=True):
            st.session_state.current_game = "Matching"
        if st.button("📘 Jeopardy", use_container_width=True):
            st.session_state.current_game = "Jeopardy"
        if st.button("🎡 Wheel", use_container_width=True):
            st.session_state.current_game = "Wheel"

    # If the game selection has changed, clear the old game's state and rerun.
    if st.session_state.current_game != previous_game:
        new_game = st.session_state.current_game
        # Clear all session state keys to reset the games
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        # Restore the new game choice
        st.session_state.current_game = new_game
        st.rerun()

    if st.session_state.current_game == "Home":
        st.title("🎮 LDS Games Arcade")
        st.info("Select a game from the sidebar to begin.")
    elif st.session_state.current_game == "Matching":
        mod = load_game_module("Matching", "both.py", "game_matching")
        mod.app()
    elif st.session_state.current_game == "Jeopardy":
        mod = load_game_module("Jeopardy", "app.py", "game_jeopardy")
        mod.app()
    elif st.session_state.current_game == "Wheel":
        mod = load_game_module("Wheel", "wheel_game.py", "game_wheel")
        mod.app()

if __name__ == "__main__":
    main()
