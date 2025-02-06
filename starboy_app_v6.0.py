import streamlit as st
import random
import time

# Apply custom styles
st.markdown("""
<style>
.stApp { background-color: #87CEEB; }
div.stButton > button:first-child {
    background-color: blue; color: white; font-size: 18px; font-weight: bold;
    border-radius: 10px; padding: 10px; border: 2px solid black;
    transition: all 0.3s ease-in-out;
}
div.stButton > button:first-child:hover {
    background-color: navy; color: gold; transform: scale(1.2);
    border: 2px solid white;
}
</style>
""", unsafe_allow_html=True)

# Probability matrix
probabilities = {
    (1, 1): {'complete': 40, 'intercept': 0}, (1, 2): {'complete': 75, 'intercept': 0},
    (1, 3): {'complete': 85, 'intercept': 0}, (1, 4): {'complete': 95, 'intercept': 0},
    (2, 1): {'complete': 50, 'intercept': 0}, (2, 2): {'complete': 25, 'intercept': 10},
    (2, 3): {'complete': 60, 'intercept': 0}, (2, 4): {'complete': 70, 'intercept': 0},
    (3, 1): {'complete': 60, 'intercept': 0}, (3, 2): {'complete': 40, 'intercept': 0},
    (3, 3): {'complete': 15, 'intercept': 15}, (3, 4): {'complete': 50, 'intercept': 0},
    (4, 1): {'complete': 60, 'intercept': 0}, (4, 2): {'complete': 50, 'intercept': 0},
    (4, 3): {'complete': 30, 'intercept': 0}, (4, 4): {'complete': 5, 'intercept': 20}
}

# Game Logic
def get_play_result(offense_choice, defense_choice):
    prob = probabilities[(offense_choice, defense_choice)]
    rand_num = random.randint(1, 100)
    
    # Show completion chance and random number
    st.write(f"📊 **Completion Chance:** {prob['complete']}%")
    st.write(f"🎲 **Random Number Generated:** {rand_num}")

    if offense_choice == defense_choice and prob['intercept'] > 0:
        intercept_range_start = 100 - prob['intercept'] + 1
        if rand_num >= intercept_range_start:
            return 'Intercept'

    if rand_num <= prob['complete']:
        return 'Complete'
    return 'Incomplete'

# Initialize session state
if "game_state" not in st.session_state:
    st.session_state.game_state = {
        "player1_results": [],
        "player2_results": [],
        "current_turn": "Player 1",
        "yards": 0,
        "attempts": 0,
        "rounds_played": 0,
        "game_over": False
    }

def switch_turn():
    if st.session_state.game_state["current_turn"] == st.session_state["player1_name"]:
        st.session_state.game_state["current_turn"] = st.session_state["player2_name"]
    else:
        st.session_state.game_state["current_turn"] = st.session_state["player1_name"]

    st.session_state.game_state["yards"] = 0
    st.session_state.game_state["attempts"] = 0
    st.session_state.game_state["rounds_played"] += 1

# Reset the game
def reset_game():
    st.session_state.game_state = {
        "player1_results": [],
        "player2_results": [],
        "current_turn": st.session_state["player1_name"],
        "yards": 0,
        "attempts": 0,
        "rounds_played": 0,
        "game_over": False
    }

# Game Setup
st.title("🌟🏈 Starboy Football Game")
game_mode = st.radio("Choose your mode:", ("Play Against Computer", "Play with a Friend"))

st.session_state["player1_name"] = st.text_input("Enter Player 1's name:", value="Player 1")
if game_mode == "Play with a Friend":
    st.session_state["player2_name"] = st.text_input("Enter Player 2's name:", value="Player 2")
else:
    st.session_state["player2_name"] = "Computer"

st.write(f"**{st.session_state.game_state['current_turn']}'s turn to play offense!**")
st.write(f"**{3 - st.session_state.game_state['attempts']} attempts left**")

# Player choices
if st.session_state.game_state["current_turn"] == st.session_state["player1_name"]:
    offense_choice = st.number_input(f"{st.session_state['player1_name']}, pick your offense number (1-4):", min_value=1, max_value=4, step=1)
    
    if game_mode == "Play Against Computer":
        defense_choice = random.randint(1, 4)
    else:
        defense_choice = st.number_input(f"{st.session_state['player2_name']}, pick your defense number (1-4):", min_value=1, max_value=4, step=1)
else:
    if game_mode == "Play with a Friend":
        offense_choice = st.number_input(f"{st.session_state['player2_name']}, pick your offense number (1-4):", min_value=1, max_value=4, step=1)
        defense_choice = st.number_input(f"{st.session_state['player1_name']}, pick your defense number (1-4):", min_value=1, max_value=4, step=1)
    else:
        offense_choice = random.randint(1, 4)
        defense_choice = st.number_input(f"{st.session_state['player1_name']}, pick your defense number (1-4):", min_value=1, max_value=4, step=1)

# Play Button
if st.button("Play!"):
    result = get_play_result(offense_choice, defense_choice)
    st.write(f"🏈 **Offense picked:** {offense_choice}")
    st.write(f"🛡️ **Defense picked:** {defense_choice}")

    st.session_state.game_state["attempts"] += 1

    if result == "Complete":
        st.session_state.game_state["yards"] += offense_choice
        if st.session_state.game_state["yards"] >= 4:
            st.balloons()
            st.image("https://media.giphy.com/media/3oriOaneEKyhAViU5G/giphy.gif")
            st.write(f"🏆 **TOUCHDOWN! {st.session_state.game_state['current_turn']} scored!**")
            result = "Touchdown"
            switch_turn()
    elif result == "Intercept":
        st.image("https://media.giphy.com/media/l2JhsXfROlxQOryZG/giphy.gif")
        st.write(f"🚨 **Intercepted! {st.session_state['player2_name']} takes over.**")
        switch_turn()
    elif st.session_state.game_state["attempts"] == 3:
        st.image("https://media.giphy.com/media/l2JhsXfROlxQOryZG/giphy.gif")
        st.write("❌ **No more attempts left. Switching turns!**")
        switch_turn()

