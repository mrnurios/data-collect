import json

# Data dictionary for cubes and their probabilities
def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)  # Load JSON data into a Python dictionary
    return data

def get_top_colors_by_probability(cube_data, positions):
    """
    Computes the top 3 colors by their probabilities based on total frequencies.
    Args:
        cube_data (dict): The dataset with probabilities for cubes and positions.
        positions (dict): Mapping of cubes to their specified positions.
    Returns:
        list: Top 3 colors with their probabilities.
    """
    # Initialize total frequencies for all colors
    total_frequencies = {'R': 0, 'G': 0, 'Y': 0, 'P': 0, 'B': 0, 'W': 0}

    # Sum the probabilities across all specified positions
    for cube, position in positions.items():
        cube_frequencies = cube_data.get(cube, {}).get(position, {})
        for color, frequency in cube_frequencies.items():
            total_frequencies[color] += frequency

    # Compute the grand total for normalization
    grand_total = sum(total_frequencies.values())
    if grand_total == 0:
        return []  # Avoid division by zero; no data available

    # Calculate probabilities and sort by descending probability
    probabilities = {color: freq / grand_total for color, freq in total_frequencies.items()}
    top_colors = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:3]
    return top_colors

def update_bet(total_loss):
    """
    Updates the bet amount based on the total loss.
    Args:
        total_loss (int): The total loss amount.
    Returns:
        int: The updated bet amount.
    """
    # Thresholds for changing the bet
    bet_thresholds = [30, 90, 210]  # 15, 45, and 105 losses
    bet_amounts = [10, 20, 40]  # Bet amounts corresponding to the thresholds

    # If total_loss crosses a threshold, increase the bet
    if total_loss >= bet_thresholds[2]:
        return 80  # If total loss is 105 or more, bet is 40
    elif total_loss >= bet_thresholds[1]:
        return 40  # If total loss is 45 or more, bet is 20
    elif total_loss >= bet_thresholds[0]:
        return 20  # If total loss is 15 or more, bet is 10
    else:
        return 10  # Default bet is 5

def main():
    # print("testing",data[0,1])
    """
    Main function to interact with the user and compute results.
    """
    initial_capital = 1000
    capital = initial_capital
    bet = 10
    total_loss = 0

    file_path = "data.json"
    data = load_data(file_path)

    while True:
        print(f"\nCurrent capital: {capital}, Total loss: {total_loss}, Current bet: {bet}")

        action = input("Enter your action ('lose <amount>' or 'gain <amount>', 'config' for cube probabilities, 'exit' to stop): ").strip().lower()

        if action == 'exit':
            print("Exiting the program. Goodbye!")
            break
        elif action.startswith('lose'):
            try:
                amount = int(action.split()[1])
                capital -= amount
                total_loss += amount
                bet = update_bet(total_loss)
            except (IndexError, ValueError):
                print("Invalid input. Please use 'lose <amount>'.")
        elif action.startswith('gain'):
            try:
                amount = int(action.split()[1])
                capital += amount
                total_loss = max(0, total_loss - amount)
                bet = update_bet(total_loss)
            except (IndexError, ValueError):
                print("Invalid input. Please use 'gain <amount>'.")
        elif action == 'config':
            print("\n--Enter the cube configurations--")

            left_cube = input("Enter the cube for the Left position (e.g., 'BG'): ")                
            middle_cube = input("Enter the cube for the Middle position (e.g., 'WP'): ")
            right_cube = input("Enter the cube for the Right position (e.g., 'YR'): ")

            # Define the positions
            positions = {
                left_cube: 'L',
                middle_cube: 'M',
                right_cube: 'R'
            }
	
            # Get the top 3 colors by probabilities from the provided configurations
            top_colors = get_top_colors_by_probability(data, positions)

            # Display the results
            if top_colors:
                print("\nTop 3 colors by probabilities:")
                for color, probability in top_colors:
                    print(f"{color}: {probability:.2%}")
            else:
                print("\nNo data available for the given configurations.")
        else:
            print("Invalid action. Please enter 'lose <amount>', 'gain <amount>', 'config', or 'exit'.")

if __name__ == "__main__":
    main()