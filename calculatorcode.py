from itertools import product
from collections import Counter

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
    
    total_dice_needed = sum(targets.values())
    dice_per_roll = min(5, total_dice_needed)
    
    # Generate all possible combinations for each roll (5 dice at once)
    all_rolls = list(product(range(1, 7), repeat=dice_per_roll))
    total_combinations = len(all_rolls) ** 3  # Three attempts
    successful_combinations = 0
    
    # Try all possible combinations of three rolls
    for roll1 in all_rolls:
        counter1 = Counter(roll1)
        remaining_targets = targets.copy()
        
        # Update remaining targets after first roll
        for num, count in counter1.items():
            if num in remaining_targets:
                remaining_targets[num] = max(0, remaining_targets[num] - count)
        
        # If we've met all targets, count this as success
        if all(count == 0 for count in remaining_targets.values()):
            successful_combinations += len(all_rolls) * len(all_rolls)
            continue
            
        for roll2 in all_rolls:
            counter2 = Counter(roll2)
            remaining_targets2 = remaining_targets.copy()
            
            # Update remaining targets after second roll
            for num, count in counter2.items():
                if num in remaining_targets2:
                    remaining_targets2[num] = max(0, remaining_targets2[num] - count)
            
            # If we've met all targets, count this as success
            if all(count == 0 for count in remaining_targets2.values()):
                successful_combinations += len(all_rolls)
                continue
                
            for roll3 in all_rolls:
                counter3 = Counter(roll3)
                remaining_targets3 = remaining_targets2.copy()
                
                # Update remaining targets after third roll
                for num, count in counter3.items():
                    if num in remaining_targets3:
                        remaining_targets3[num] = max(0, remaining_targets3[num] - count)
                
                # If we've met all targets after three rolls, count this as success
                if all(count == 0 for count in remaining_targets3.values()):
                    successful_combinations += 1
    
    probability = successful_combinations / total_combinations
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
                percentage = prob * 100
                rounded_prob = round(prob, 6)
                rounded_percentage = round(percentage, 4)
                
                if prob > 0:
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
