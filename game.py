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
            offense_choice = int(input(f"{offense_player}, pick your number (1-4): "))

        if is_computer and defense_player == 'Computer':
            defense_choice = computer_defense_strategy()
        else:
            defense_choice = int(input(f"{defense_player}, pick your number (1-4): "))

        result = get_play_result(offense_choice, defense_choice)
        print(f"Offense picked {offense_choice}, Defense picked {defense_choice}. Result: {result}")

        if result == 'Intercept':
            result_log.append('p' + '\\' * (3 - tries))
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
                print(f"Touchdown completed at {yards} yards!")
                result_log.append('1' + '\\' * (3 - tries))
                print(f"Current Scoreboard: {offense_player}: {' '.join(result_log)}")
                break
        else:
            if tries == 3:
                result_log.append('-')
                print(f"Current Scoreboard: {offense_player}: {' '.join(result_log)}")

    return result_log


def computer_strategy(current_yards):
    # Basic strategy: Pick the smallest number to avoid overshooting if close to 4
    if current_yards >= 4:
        return 1
    elif current_yards == 3:
        return 1
    else:
        return random.randint(1, 4)


def computer_defense_strategy():
    return random.randint(1, 4)

def calculate_final_score(results):
    touchdowns = sum(1 for result in results if '1' in result)  # Count touchdowns
    marks = sum(result.count('\'') for result in results if 'p' not in result)  # Count marks, excluding interceptions
    return f"{touchdowns}" + "'" * marks

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
        player1_results += play_round(player1, player2, is_computer)

        print(f"\n{player2}'s turn as offense (Round {i+1})")
        player2_results += play_round(player2, player1, is_computer)

    final_score_p1 = calculate_final_score(player1_results)
    final_score_p2 = calculate_final_score(player2_results)
    
    print(f"\nFinal Scores:")
    print(f"{player1}: {' '.join(player1_results)} → Final Score: {final_score_p1}")
    print(f"{player2}: {' '.join(player2_results)} → Final Score: {final_score_p2}")


if __name__ == "__main__":
    main()
