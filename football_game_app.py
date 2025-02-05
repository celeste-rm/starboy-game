import streamlit as st
import random

# Define the probability matrix and interception chances
probabilities = {
    (1, 1): {'complete': 40, 'intercept': 0},
    (1, 2): {'complete': 75, 'intercept': 0},
    (1, 3): {'complete': 85, 'intercept': 0},
    (1, 4): {'complete': 95, 'intercept': 0},
    (2, 1): {'complete': 50, 'intercept': 0},
    (2, 2): {'complete': 25, 'intercept': 10},
    (2, 3): {'complete': 60, 'intercept': 0},
    (2, 4): {'complete': 70, 'intercept': 0},
    (3, 1): {'complete': 60, 'intercept': 0},
    (3, 2): {'complete': 40, 'intercept': 0},
    (3, 3): {'complete': 15, 'intercept': 15},
    (3, 4): {'complete': 50, 'intercept': 0},
    (4, 1): {'complete': 60, 'intercept': 0},
    (4, 2): {'complete': 50, 'intercept': 0},
    (4, 3): {'complete': 30, 'intercept': 0},
    (4, 4): {'complete': 5, 'intercept': 20}
}

st.title("🏈 Football Probability Game")

# Game Setup
game_mode = st.radio("Choose your mode:", ("Play Against Computer", "Play with a Friend"))

if game_mode == "Play Against Computer":
    player_name = st.text_input("Enter your name:", value="Player 1")
    if 'yards' not in st.session_state:
        st.session_state['yards'] = 0

    offense_choice = st.number_input(f"{player_name}, pick your number (1-4):", min_value=1, max_value=4, step=1)
    defense_choice = random.randint(1, 4)  # Computer randomly picks defense

    if st.button("Play!"):
        result = get_play_result(offense_choice, defense_choice)
        st.write(f"Offense picked {offense_choice}, Defense (Computer) picked {defense_choice}.")
        st.write(f"Result: **{result}**")

elif game_mode == "Play with a Friend":
    st.write("Share this link with your friend and take turns making your picks!")

    # Initialize session states for both players
    if 'player1_choice' not in st.session_state:
        st.session_state['player1_choice'] = None
    if 'player2_choice' not in st.session_state:
        st.session_state['player2_choice'] = None

    player_role = st.radio("Are you Player 1 or Player 2?", ("Player 1", "Player 2"))

    if player_role == "Player 1":
        st.session_state['player1_choice'] = st.number_input("Player 1, pick your number (1-4):", min_value=1, max_value=4, step=1)
    else:
        st.session_state['player2_choice'] = st.number_input("Player 2, pick your number (1-4):", min_value=1, max_value=4, step=1)

    if st.button("Submit Choices"):
        if st.session_state['player1_choice'] and st.session_state['player2_choice']:
            result = get_play_result(st.session_state['player1_choice'], st.session_state['player2_choice'])
            st.write(f"Player 1 picked {st.session_state['player1_choice']}, Player 2 picked {st.session_state['player2_choice']}.")
            st.write(f"Result: **{result}**")
        else:
            st.warning("Both players need to make a choice!")

