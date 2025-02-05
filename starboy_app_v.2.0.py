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

# Function to get play result
def get_play_result(offense_choice, defense_choice):
    prob = probabilities[(offense_choice, defense_choice)]
    rand_num = random.randint(1, 100)

    # Display probabilities and random number
    st.write(f"Completion percentage: **{prob['complete']}%**")
    st.write(f"Random number generated: **{rand_num}**")

    # Check for interception
    if offense_choice == defense_choice and prob['intercept'] > 0:
        if rand_num >= (100 - prob['intercept'] + 1):
            return 'Intercept'

    # Check for pass completion
    if rand_num <= prob['complete']:
        return 'Complete'
    
    return 'Incomplete'

# Function to calculate final score
def calculate_final_score(results, opponent_results):
    if 'k' in results:
        return 'k'
    touchdowns = sum(1 for result in results if '1' in result)
    marks = sum(result.count("'") for result in results if 'p' not in result)
    opponent_interception_marks = sum(result.count("'") for result in opponent_results if result.startswith('p'))
    total_marks = marks + opponent_interception_marks
    return f"{touchdowns}" + "'" * total_marks

# Function to determine if player should kneel
def should_kneel(player_results, opponent_results):
    player_score = calculate_final_score(player_results, opponent_results)
    opponent_score = calculate_final_score(opponent_results, player_results)

    player_touchdowns = int(player_score[0]) if player_score[0] != 'k' else 0
    player_marks = player_score.count("'")

    opponent_touchdowns = int(opponent_score[0]) if opponent_score[0] != 'k' else 0
    opponent_marks = opponent_score.count("'")

    potential_touchdowns = player_touchdowns + 1
    potential_marks = player_marks + 2

    if potential_touchdowns < opponent_touchdowns:
        return True
    elif potential_touchdowns == opponent_touchdowns and potential_marks < opponent_marks:
        return True
    return False

# Computer offensive strategy
def computer_strategy(current_yards):
    possible_moves = [i for i in range(1, 5) if current_yards + i <= 5]
    move_success_probabilities = [(move, sum(probabilities[(move, d)]['complete'] for d in range(1, 4)) / 4) for move in possible_moves]
    best_move = max(move_success_probabilities, key=lambda x: x[1])[0]
    return best_move

# Computer defensive strategy
def computer_defense_strategy(opponent_yards):
    if opponent_yards >= 4:
        predicted_choices = [1, 2]
    elif opponent_yards == 3:
        predicted_choices = [1, 2]
    else:
        predicted_choices = [3, 4]
    return random.choice(predicted_choices)

# Streamlit UI Starts Here
st.title("🏈 Football Probability Game")

# Game Setup
game_mode = st.radio("Choose your mode:", ("Play Against Computer", "Play with a Friend"))

# Initialize session state
if 'player1_results' not in st.session_state:
    st.session_state['player1_results'] = []
if 'player2_results' not in st.session_state:
    st.session_state['player2_results'] = []
if 'round' not in st.session_state:
    st.session_state['round'] = 1
if 'yards' not in st.session_state:
    st.session_state['yards'] = 0

# Playing Against Computer
if game_mode == "Play Against Computer":
    player_name = st.text_input("Enter your name:", value="Player 1")
    offense_choice = st.number_input(f"{player_name}, pick your number (1-4):", min_value=1, max_value=4, step=1)
    defense_choice = computer_defense_strategy(st.session_state['yards'])

    if st.button("Play!"):
        result = get_play_result(offense_choice, defense_choice)
        st.session_state['yards'] += offense_choice if result == 'Complete' else 0
        st.session_state['player1_results'].append(result)

        st.write(f"Offense picked **{offense_choice}**, Defense (Computer) picked **{defense_choice}**.")
        st.write(f"Result: **{result}**")

        # Display current score
        current_score = calculate_final_score(st.session_state['player1_results'], [])
        st.write(f"**Current Score:** {player_name}: {current_score}")

# Playing with a Friend
elif game_mode == "Play with a Friend":
    st.write("Share this link with your friend and take turns making your picks!")

    player_role = st.radio("Are you Player 1 or Player 2?", ("Player 1", "Player 2"))

    if player_role == "Player 1":
        offense_choice = st.number_input("Player 1, pick your number (1-4):", min_value=1, max_value=4, step=1)
        defense_choice = None
    else:
        defense_choice = st.number_input("Player 2, pick your number (1-4):", min_value=1, max_value=4, step=1)
        offense_choice = None

    if st.button("Submit Choices"):
        if offense_choice and defense_choice:
            result = get_play_result(offense_choice, defense_choice)
            st.session_state['player1_results'].append(result)

            st.write(f"Player 1 picked **{offense_choice}**, Player 2 picked **{defense_choice}**.")
            st.write(f"Result: **{result}**")

            # Display current score
            current_score_p1 = calculate_final_score(st.session_state['player1_results'], st.session_state['player2_results'])
            st.write(f"**Current Score:** Player 1: {current_score_p1}")

        else:
            st.warning("Both players need to make a choice!")

# Display Final Scores After Game Ends
if len(st.session_state['player1_results']) == 3 and len(st.session_state['player2_results']) == 3:
    final_score_p1 = calculate_final_score(st.session_state['player1_results'], st.session_state['player2_results'])
    final_score_p2 = calculate_final_score(st.session_state['player2_results'], st.session_state['player1_results'])

    st.write(f"### Final Scores:")
    st.write(f"Player 1: {final_score_p1}")
    st.write(f"Player 2: {final_score_p2}")

    # Determine Winner
    if final_score_p1 == 'k':
        st.write("**Player 2 wins! Player 1 had to kneel.**")
    elif final_score_p2 == 'k':
        st.write("**Player 1 wins! Player 2 had to kneel.**")
    else:
        player1_touchdowns = int(final_score_p1[0])
        player2_touchdowns = int(final_score_p2[0])

        if player1_touchdowns > player2_touchdowns:
            st.write("**Player 1 wins! Boohoo Player 2, go cry about it!**")
        elif player2_touchdowns > player1_touchdowns:
            st.write("**Player 2 wins! Boohoo Player 1, go cry about it!**")
        else:
            player1_marks = final_score_p1.count("'")
            player2_marks = final_score_p2.count("'")

            if player1_marks > player2_marks:
                st.write("**Player 1 wins! It was a close one!**")
            elif player2_marks > player1_marks:
                st.write("**Player 2 wins! It was a close one!**")
            else:
                st.write("**It's a tie!**")
