import streamlit as st
import random

# Set up styles
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

# Probability Matrix
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

# Initialize game state
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

# Get game mode
st.title("🏈 Starboy Football Game")
game_mode = st.radio("Select Game Mode:", ["Play Against Computer", "Play with a Friend"])

# Player names
st.session_state["player1_name"] = st.text_input("Enter Player 1's name:", "Player 1")
if game_mode == "Play with a Friend":
    st.session_state["player2_name"] = st.text_input("Enter Player 2's name:", "Player 2")
else:
    st.session_state["player2_name"] = "Computer"

# Track progress
progress = st.session_state.game_state["rounds_played"] / 6
st.progress(progress)

# Display current turn
st.write(f"🎯 **{st.session_state.game_state['current_turn']}'s Turn**")
st.write(f"🏆 **{3 - st.session_state.game_state['attempts']} Attempts Left**")

# Stop game after 6 rounds
if st.session_state.game_state["rounds_played"] >= 6:
    st.write("🏁 **Game Over! Click below to see results**")
    if st.button("See Results"):
        st.write("Final Scores Displayed Here")
    st.stop()

# Get offense & defense choices
offense_choice = st.number_input(f"{st.session_state.game_state['current_turn']} Pick your offense (1-4):", min_value=1, max_value=4, step=1)
defense_choice = random.randint(1, 4) if game_mode == "Play Against Computer" else st.number_input(f"Defense Pick your defense (1-4):", min_value=1, max_value=4, step=1)

# Function to get play result
def get_play_result(offense, defense):
    prob = probabilities[(offense, defense)]
    rand_num = random.randint(1, 100)
    
    st.write(f"📊 **Completion Chance:** {prob['complete']}%")
    st.write(f"🎲 **Random Number:** {rand_num}")

    if offense == defense and prob['intercept'] > 0 and rand_num >= 100 - prob['intercept']:
        return 'Intercept'

    if rand_num <= prob['complete']:
        return 'Complete'
    
    return 'Incomplete'

# Function to switch turns
def switch_turn():
    if st.session_state.game_state["current_turn"] == st.session_state["player1_name"]:
        st.session_state.game_state["current_turn"] = st.session_state["player2_name"]
    else:
        st.session_state.game_state["current_turn"] = st.session_state["player1_name"]

    st.session_state.game_state["yards"] = 0
    st.session_state.game_state["attempts"] = 0
    st.session_state.game_state["rounds_played"] += 1

# Play button
if st.button("Play!"):
    result = get_play_result(offense_choice, defense_choice)
    
    st.write(f"🏈 **Offense Picked:** {offense_choice}")
    st.write(f"🛡 **Defense Picked:** {defense_choice}")

    st.session_state.game_state["attempts"] += 1

    if result == "Complete":
        st.session_state.game_state["yards"] += offense_choice
        if st.session_state.game_state["yards"] >= 4:
            st.balloons()
            st.image("https://media.giphy.com/media/3oriOaneEKyhAViU5G/giphy.gif")
            st.write(f"🏆 **TOUCHDOWN! {st.session_state.game_state['current_turn']} Scored!**")
            result = "Touchdown"
            switch_turn()
    elif result == "Intercept":
        st.image("https://media.giphy.com/media/l2JhsXfROlxQOryZG/giphy.gif")
        st.write(f"🚨 **Intercepted! {st.session_state['player2_name']} Takes Over.**")
        switch_turn()
    elif st.session_state.game_state["attempts"] == 3:
        st.image("https://media.giphy.com/media/l2JhsXfROlxQOryZG/giphy.gif")
        st.write("❌ **No More Attempts Left. Switching Turns!**")
        switch_turn()

# Live scoreboard
st.write("### 📊 Live Scoreboard")
st.metric(label=f"{st.session_state['player1_name']}'s Score", value=len(st.session_state.game_state["player1_results"]))
st.metric(label=f"{st.session_state['player2_name']}'s Score", value=len(st.session_state.game_state["player2_results"]))

# Navigation buttons
if st.session_state.game_state["rounds_played"] < 6:
    st.button("Go to Next Play")
else:
    st.button("See Results")
