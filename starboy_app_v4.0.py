import streamlit as st
import random

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
    background-color: navy; color: gold; transform: scale(1.3);
    border: 2px solid white;
}
</style>
""", unsafe_allow_html=True)

# Define the probability matrix and interception chances
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

# Game functions
def get_play_result(offense_choice, defense_choice):
    prob = probabilities[(offense_choice, defense_choice)]
    rand_num = random.randint(1, 100)
    
    # Display completion percentage and random number before showing result
    st.write(f"📊 **Completion Chance:** {prob['complete']}%")
    st.write(f"🎲 **Random Number Generated:** {rand_num}")

    if offense_choice == defense_choice and prob['intercept'] > 0:
        if rand_num >= (100 - prob['intercept'] + 1):
            return 'Intercept'

    if rand_num <= prob['complete']:
        return 'Complete'
    return 'Incomplete'

def update_score(player_results):
    score_string = ''
    if 'Touchdown' in player_results:
        td_attempt = player_results.index('Touchdown') + 1
        score_string += "1" + "'" * (3 - td_attempt)
    elif 'Intercept' in player_results:
        intercept_attempt = player_results.index('Intercept') + 1
        score_string += "p" + "'" * (3 - intercept_attempt)
    elif len(player_results) == 3 and 'Touchdown' not in player_results:
        score_string += "-"
    return score_string

def calculate_final_score(player_results, opponent_results):
    touchdowns = sum(1 for res in player_results if '1' in res)
    marks = sum(res.count("'") for res in player_results if 'p' not in res)
    opponent_intercept_marks = sum(res.count("'") for res in opponent_results if res.startswith('p'))
    total_marks = marks + opponent_intercept_marks
    return f"{touchdowns}" + "'" * total_marks

def switch_turn():
    st.session_state['current_turn'] = st.session_state['player2_name'] if st.session_state['current_turn'] == st.session_state['player1_name'] else st.session_state['player1_name']
    st.session_state['yards'] = 0
    st.session_state['attempts'] = 0

def reset_game():
    st.session_state['player1_results'] = []
    st.session_state['player2_results'] = []
    st.session_state['current_turn'] = st.session_state['player1_name']
    st.session_state['yards'] = 0
    st.session_state['attempts'] = 0

# Initialize session state
if 'player1_results' not in st.session_state:
    reset_game()

# Game Setup
st.title("🌟🏈 Starboy Football Game")
game_mode = st.radio("Choose your mode:", ("Play Against Computer", "Play with a Friend"))

# Get player names based on mode
st.session_state['player1_name'] = st.text_input("Enter Player 1's name:", value="Player 1")
if game_mode == "Play with a Friend":
    st.session_state['player2_name'] = st.text_input("Enter Player 2's name:", value="Player 2")
else:
    st.session_state['player2_name'] = "Computer"

# Display current player turn
st.write(f"**It's {st.session_state['current_turn']}'s turn to play offense!**")

# Get offense and defense choices with names
if st.session_state['current_turn'] == st.session_state['player1_name'] or game_mode == "Play with a Friend":
    offense_choice = st.number_input(f"{st.session_state['current_turn']}, pick your offense number (1-4):", min_value=1, max_value=4, step=1)
else:
    offense_choice = random.randint(1, 4)

defense_choice = random.randint(1, 4) if st.session_state['current_turn'] == st.session_state['player1_name'] and game_mode == "Play Against Computer" else st.number_input(f"{st.session_state['player2_name']}, pick your defense number (1-4):", min_value=1, max_value=4, step=1)

# Play button logic
if st.button("Play!"):
    result = get_play_result(offense_choice, defense_choice)
    st.session_state['attempts'] += 1

    if result == 'Complete':
        st.session_state['yards'] += offense_choice
        if st.session_state['yards'] > 5:
            st.write("🚫 **You went out of bounds! Attempt failed.**")
            result = 'Incomplete'
            switch_turn()
        elif st.session_state['yards'] >= 4:
            st.balloons()
            st.image("https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExemdjNWNtbHF6YXhtbjlqcHk5NTZycTM1d2YwZjl2czJhem0zYWx4diZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3oriOaneEKyhAViU5G/giphy.gif", use_column_width=True)
            st.write(f"🏆 **TOUCHDOWN! {st.session_state['current_turn']} scored!**")
            result = 'Touchdown'
            switch_turn()
    elif result == 'Intercept':
        st.write(f"🚨 **Intercepted! {st.session_state['player2_name']} takes over.**")
        st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGEzcm4zbHp2ZzI4d3ByNzA0YnFnMm42d2swMHRjN3E1eTVneTVsbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2JhsXfROlxQOryZG/giphy.gif", use_column_width=True)
        switch_turn()
    elif st.session_state['attempts'] == 3:
        st.write(f"❌ **No more attempts left. Switching turns!**")
        st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbGEzcm4zbHp2ZzI4d3ByNzA0YnFnMm42d2swMHRjN3E1eTVneTVsbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l2JhsXfROlxQOryZG/giphy.gif", use_column_width=True)
        result = 'Incomplete'
        switch_turn()

    # Update results
    if st.session_state['current_turn'] == st.session_state['player1_name']:
        st.session_state['player2_results'].append(result)
    else:
        st.session_state['player1_results'].append(result)

# Display progress bar for yard progression
yard_progress = min(st.session_state['yards'] / 5, 1.0)
st.progress(yard_progress)

# Display scoreboard
st.write("### 🏆 Live Scoreboard")
st.metric(label=f"{st.session_state['player1_name']}'s Score", value=update_score(st.session_state['player1_results']))
st.metric(label=f"{st.session_state['player2_name']}'s Score", value=update_score(st.session_state['player2_results']))

# Final Scoring
if len(st.session_state['player1_results']) == 3 and len(st.session_state['player2_results']) == 3:
    final_score_p1 = calculate_final_score(st.session_state['player1_results'], st.session_state['player2_results'])
    final_score_p2 = calculate_final_score(st.session_state['player2_results'], st.session_state['player1_results'])

    p1_name = st.session_state['player1_name']
    p2_name = st.session_state['player2_name']

    st.write(f"### Final Scores:")
    st.write(f"**{p1_name}:** {final_score_p1}")
    st.write(f"**{p2_name}:** {final_score_p2}")

    # Determine Winner
    if final_score_p1 == 'k':
        st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXNrMHV2azUxcTl1NmQ4d3UwOW9hbHIyZjN6ajlzZGVkaGUzcjByaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bf6GQkB3wcow9OPw40/giphy.gif", use_column_width=True)
        st.error(f"😢 **{p1_name} had to kneel!** {p2_name} wins! 🏆")
    elif final_score_p2 == 'k':
        st.image("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExbXNrMHV2azUxcTl1NmQ4d3UwOW9hbHIyZjN6ajlzZGVkaGUzcjByaCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/bf6GQkB3wcow9OPw40/giphy.gif", use_column_width=True)
        st.error(f"😢 **{p2_name} had to kneel!** {p1_name} wins! 🏆")
    else:
        player1_touchdowns = int(final_score_p1[0]) if final_score_p1[0].isdigit() else 0
        player2_touchdowns = int(final_score_p2[0]) if final_score_p2[0].isdigit() else 0

        if player1_touchdowns > player2_touchdowns:
            st.image("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2NxOGk4YXN6NnBzYW0yM3FtMnp5Nm9wYmw5YmpsOGRuOWZ2dTFodCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0MYJwo89pS4sOHHW/giphy.gif", use_column_width=True)
            st.success(f"🎉 **{p1_name} WINS!** 🏆💪") 
            st.error(f"😭🤧😚 Boohoo {p2_name}, go cry about it!") 
        elif player2_touchdowns > player1_touchdowns: 
            st.image("https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2NxOGk4YXN6NnBzYW0yM3FtMnp5Nm9wYmw5YmpsOGRuOWZ2dTFodCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l0MYJwo89pS4sOHHW/giphy.gif", use_column_width=True) 
            st.success(f"🎉 {p2_name} WINS! 🏆💪") 
            st.error(f"😭🤧😚 Boohoo {p1_name}, go cry about it!")
        else: 
            player1_marks = final_score_p1.count("'") 
            player2_marks = final_score_p2.count("'") 
            if player1_marks > player2_marks: 
                st.success(f"🎉 {p1_name} WINS! 🏆💪 It was a close one!") 
            elif player2_marks > player1_marks: 
                st.success(f"🎉 {p2_name} WINS! 🏆💪 It was a close one!") 
            else: 
                st.warning("🤝 It's a tie! Stop being boring and play like pros next time!")
