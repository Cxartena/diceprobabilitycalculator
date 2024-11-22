from collections import Counter
import itertools
import math

def calculate_dice_probability(targets):
    def verify_targets(targets):
        total_dice = sum(targets.values())
        if total_dice > 5:
            return False
        for num, count in targets.items():
            if num < 1 or num > 6 or count < 0:
                return False
        return True
    
    if not verify_targets(targets):
        return "Invalid targets. Cannot exceed 5 dice total and numbers must be between 1-6"
    
    def calculate_specific_path(current_state, needed_state, attempts_left):
        if attempts_left == 0:
            return 0
        
        success = all(current_state.get(num, 0) >= count 
                     for num, count in needed_state.items())
        if success:
            return 1
            
        remaining_dice = 5 - sum(current_state.values())
        if remaining_dice == 0:
            return 0
            
        total_prob = 0
        for roll_result in range(1, 7):
            new_state = current_state.copy()
            if roll_result in needed_state:
                if new_state.get(roll_result, 0) < needed_state[roll_result]:
                    new_state[roll_result] = new_state.get(roll_result, 0) + 1
                    prob = (1/6) * calculate_specific_path(new_state, needed_state, attempts_left - 1)
                    total_prob += prob
            else:
                new_state[roll_result] = new_state.get(roll_result, 0) + 1
                prob = (1/6) * calculate_specific_path(new_state, needed_state, attempts_left - 1)
                total_prob += prob
            
        return total_prob
    
    initial_state = Counter()
    probability = calculate_specific_path(initial_state, targets, 3)
    
    return probability

def run_probability_calculation():
    while True:
        print("\nDice Probability Calculator")
        print("Enter your target dice combinations.")
        print("Format: number count, number count, etc.")
        print("Examples:")
        print("- '3 3' for three 3s")
        print("- '6 5' for five 6s")
        print("- '6 2, 5 2' for two 6s and two 5s")
        
        try:
            input_str = input("\nEnter targets: ")
            targets = {}
            for part in input_str.split(','):
                num, count = map(int, part.strip().split())
                targets[num] = count
            
            prob = calculate_dice_probability(targets)
            if isinstance(prob, str):
                print(f"\n{prob}")
            else:
                # Prevent extremely low probabilities from showing as 1 in infinite
                if prob > 0:
                    percentage = prob * 100
                    rounded_prob = round(prob, 6)
                    rounded_percentage = round(percentage, 4)
                    
                    # Calculate attempts with rounding to prevent integer overflow
                    attempts = max(1, round(1 / prob))
                    
                    print(f"\nProbability: {rounded_prob}")
                    print(f"Percentage: {rounded_percentage}%")
                    print(f"Approximately 1 in {attempts} attempts")
                else:
                    print("\nProbability is effectively zero.")
        
        except ValueError:
            print("\nInvalid input format. Please use 'number count, number count' format.")
        
        again = input("\nCalculate another probability? (y/n): ").lower()
        if again != 'y':
            break

if __name__ == "__main__":
    run_probability_calculation()
