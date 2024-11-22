from collections import Counter
from itertools import combinations_with_replacement
import math

def calculate_dice_probability(targets):
    # Validate input
    total_dice_needed = sum(targets.values())
    if total_dice_needed > 5 or any(num < 1 or num > 6 or count < 0 for num, count in targets.items()):
        return "Invalid targets. Cannot exceed 5 dice total and numbers must be between 1-6"

    def calculate_single_roll_probability(dice_to_roll, targets_needed):
        """Calculate probability of getting specific targets in a single roll of N dice"""
        # Get all possible combinations for rolling N dice
        possible_outcomes = list(combinations_with_replacement(range(1, 7), dice_to_roll))
        total_outcomes = len(possible_outcomes)
        success_count = 0
        
        # For each possible roll outcome
        for outcome in possible_outcomes:
            roll_counter = Counter(outcome)
            # Check if this roll satisfies our targets
            if all(roll_counter[num] >= count for num, count in targets_needed.items()):
                success_count += math.factorial(dice_to_roll)
                for count in roll_counter.values():
                    success_count //= math.factorial(count)
        
        # Account for permutations
        total_perms = math.factorial(dice_to_roll)
        total_outcomes = 6 ** dice_to_roll
        
        return success_count / total_outcomes

    def calculate_total_probability():
        remaining_targets = targets.copy()
        total_prob = 0
        dice_to_roll = min(5, total_dice_needed)  # Can't roll more than 5 dice at once
        
        # First roll
        first_roll_prob = calculate_single_roll_probability(dice_to_roll, remaining_targets)
        if first_roll_prob == 1:  # If we can get everything in first roll
            return first_roll_prob
            
        # Add probability of getting it in exactly 2 rolls
        second_roll_prob = first_roll_prob + \
            (1 - first_roll_prob) * calculate_single_roll_probability(dice_to_roll, remaining_targets)
            
        # Add probability of getting it in exactly 3 rolls
        total_prob = second_roll_prob + \
            (1 - second_roll_prob) * calculate_single_roll_probability(dice_to_roll, remaining_targets)
        
        return total_prob

    return calculate_total_probability()

def run_probability_calculation():
    while True:
        print("\nDice Probability Calculator")
        print("Enter your target dice combinations.")
        print("Format: number count, number count, etc.")
        print("Examples:")
        print("- '3 3' for three 3s")
        print("- '6 2' for two 6s")
        print("- '6 2, 5 2' for two 6s and two 5s")
        
        try:
            input_str = input("\nEnter targets: ").strip()
            if not input_str:
                continue
                
            targets = {}
            for part in input_str.split(','):
                num, count = map(int, part.strip().split())
                targets[num] = count
            
            prob = calculate_dice_probability(targets)
            if isinstance(prob, str):
                print(f"\n{prob}")
            else:
                percentage = prob * 100
                rounded_percentage = round(percentage, 4)
                if prob > 0:
                    attempts = max(1, round(1/prob))
                    print(f"\nPercentage: {rounded_percentage}%")
                    print(f"Approximately 1 in {attempts} attempts")
                else:
                    print("\nProbability is effectively zero.")
        
        except ValueError:
            print("\nInvalid input format. Please use 'number count, number count' format.")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
        
        again = input("\nCalculate another probability? (y/n): ").lower()
        if again != 'y':
            break

if __name__ == "__main__":
    run_probability_calculation()
