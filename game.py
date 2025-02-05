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

def get_play_result(offense_choice, defense_choice):
    play_key = (offense_choice, defense_choice)
    if play_key not in probabilities:
        return 'Invalid play'

    prob = probabilities[play_key]
    print(f"Completion percentage for this play: {prob['complete']}%")
    rand_num = random.randint(1, 100)
    print(f"Random number generated: {rand_num}")

    # Check for interception if numbers match
    if offense_choice == defense_choice and prob['intercept'] > 0:
        if rand_num >= (100 - prob['intercept'] + 1):
            return 'Intercept'

    # Check for pass completion
    if rand_num <= prob['complete']:
        return 'Complete'

    return 'Incomplete'


def play_round(offense_player, defense_player, is_computer=False):
    yards = 0
    tries = 0
    result_log = []

    while tries < 3:
        tries += 1

        if is_computer and offense_player == 'Computer':
            offense_choice = computer_strategy(yards)
        else:
            while True:
                try:
                    offense_choice = int(input(f"{offense_player}, pick your number (1-4): "))
                    if 1 <= offense_choice <= 4:
                        break
                    else:
                        print("Invalid choice. Please pick a number between 1 and 4.")
                except ValueError:
                    print("Invalid input. Please enter a number.")


        if is_computer and defense_player == 'Computer':
            defense_choice = computer_defense_strategy(yards)
        else:
                while True:
                    try:
                        defense_choice = int(input(f"{defense_player}, pick your number (1-4): "))
                        if 1 <= defense_choice <= 4:
                            break
                        else:
                            print("Invalid choice. Please pick a number between 1 and 4.")
                    except ValueError:
                        print("Invalid input. Please enter a number.")

        result = get_play_result(offense_choice, defense_choice)
        print(f"Offense picked {offense_choice}, Defense picked {defense_choice}. Result: {result}")

        if result == 'Intercept':
            result_log.append('p' + "'" * (3 - tries))
            print(f"Current Scoreboard: {offense_player}: {' '.join(result_log)}")
            break
        elif result == 'Complete':
            yards += offense_choice
            if yards >= 6:
                print("Offense went past 5 yards. Turn over.")
                result_log.append('-')
                print(f"Current Scoreboard: {offense_player}: {' '.join(result_log)}")
                break
            elif yards >= 4:
                print(f"Touchdown completed at {yards} yards in {tries} tries!")
                result_log.append('1' + "'" * (3 - tries))
                print(f"Current Scoreboard: {offense_player}: {' '.join(result_log)}")
                break
        else:
            if tries == 3:
                print("Player failed to score a touchdown :(")
                result_log.append('-')
                print(f"Current Scoreboard: {offense_player}: {' '.join(result_log)}")

    return result_log

def computer_strategy(current_yards):
    # Define possible moves based on current yardage to avoid going over 5 yards
    possible_moves = [i for i in range(1, 5) if current_yards + i <= 5]
    
    # Evaluate the expected success for each possible move
    move_success_probabilities = []
    for move in possible_moves:
        # Assume the player randomly picks defense moves 1 to 4
        avg_success_rate = sum(probabilities[(move, d)]['complete'] for d in range(1, 5)) / 4
        move_success_probabilities.append((move, avg_success_rate))
    
    # Choose the move with the highest average success rate
    best_move = max(move_success_probabilities, key=lambda x: x[1])[0]
    
    return best_move

def computer_defense_strategy(opponent_yards):
    # Predict opponent's behavior: likely to pick smaller numbers if close to touchdown
    if opponent_yards >= 4:
        predicted_offense_choices = [1, 2]  # Opponent will avoid going over
    elif opponent_yards == 3:
        predicted_offense_choices = [1, 2]  # Safer plays to avoid overshooting
    else:
        predicted_offense_choices = [3, 4]  # Riskier plays when there's more yardage to cover
    
    # Defense mirrors the most probable offense choice to maximize interception
    defense_choice = random.choice(predicted_offense_choices)
    
    return defense_choice

def calculate_final_score(results, opponent_results):
    if 'k' in results:
        return 'k'
    touchdowns = sum(1 for result in results if '1' in result)
    marks = sum(result.count("'") for result in results if 'p' not in result)
    opponent_interception_marks = sum(result.count("'") for result in opponent_results if result.startswith('p'))
    total_marks = marks + opponent_interception_marks
    return f"{touchdowns}" + "'" * total_marks

def should_kneel(player_results, opponent_results):
    player_score = calculate_final_score(player_results, opponent_results)
    opponent_score = calculate_final_score(opponent_results, player_results)

    # Split the score into touchdowns and marks
    player_touchdowns = int(player_score[0])
    player_marks = player_score.count("'")

    opponent_touchdowns = int(opponent_score[0])
    opponent_marks = opponent_score.count("'")

    # Even if the player gets a touchdown with maximum apostrophes, can they win?
    # Maximum score for one round is 1 with two apostrophes: 1''
    potential_touchdowns = player_touchdowns + 1
    potential_marks = player_marks + 2  # Max apostrophes possible in one round

    if potential_touchdowns < opponent_touchdowns:
        return True  # Can't catch up in touchdowns
    elif potential_touchdowns == opponent_touchdowns and potential_marks < opponent_marks:
        return True  # Same touchdowns but can't surpass in apostrophes
    else:
        return False  # Still a chance to win


def main():
    print("Welcome to the Football Probability Game!")
    mode = input("Do you want to play against the Computer (yes/no)? ").lower()

    if mode == 'yes':
        player1 = input("Enter your name: ")
        player2 = 'Computer'
        is_computer = True
    else:
        player1 = input("Enter Player 1's name: ")
        player2 = input("Enter Player 2's name: ")
        is_computer = False

    player1_results = []
    player2_results = []

    # Each player plays three rounds as offense
    for i in range(3):
        print(f"\n{player1}'s turn as offense (Round {i+1})")
        if i == 2 and should_kneel(player1_results, player2_results):
            print(f"{player1} cannot win and kneels.")
            player1_results.append('k')
            # Player 2 wins immediately if Player 1 kneels
            break
        else:
            player1_results += play_round(player1, player2, is_computer)

        print(f"\n{player2}'s turn as offense (Round {i+1})")
        if i == 2 and should_kneel(player2_results, player1_results):
            print(f"{player2} cannot win and kneels.")
            player2_results.append('k')
            break  # Game ends if Player 2 kneels
        else:
            player2_results += play_round(player2, player1, is_computer)


    final_score_p1 = calculate_final_score(player1_results, player2_results)
    final_score_p2 = calculate_final_score(player2_results, player1_results)
    
    print(f"\nFinal Scores:")
    print(f"{player1}: {' '.join(player1_results)} → Final Score: {final_score_p1}")
    print(f"{player2}: {' '.join(player2_results)} → Final Score: {final_score_p2}")

    if final_score_p1 == 'k':
        print(f"\n{player2} wins! {player1} had to kneel :(")
    elif final_score_p2 == 'k':
        print(f"\n{player1} wins! {player2} had to kneel :(")
    else:
        # Compare touchdowns first
        player1_touchdowns = int(final_score_p1[0])
        player2_touchdowns = int(final_score_p2[0])

        if player1_touchdowns > player2_touchdowns:
            print(f"\n{player1} wins! Boohoo {player2}, go cry about it!")
        elif player2_touchdowns > player1_touchdowns:
            print(f"\n{player2} wins! Boohoo {player1}, go cry about it!")
        else:
            # If touchdowns are tied, compare apostrophes (marks)
            player1_marks = final_score_p1.count("'")
            player2_marks = final_score_p2.count("'")

            if player1_marks > player2_marks:
                print(f"\n{player1} wins! It was a close one!")
            elif player2_marks > player1_marks:
                print(f"\n{player2} wins! It was a close one!")
            else:
                print("\nIt's a tie!")


if __name__ == "__main__":
    main()


