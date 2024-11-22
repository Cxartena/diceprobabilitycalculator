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
    
    # Generate all possible 3-roll combinations
    all_rolls = list(product(range(1, 7), repeat=3))
    
    # Track successful rolls
    successful_rolls = 0
    total_rolls = len(all_rolls)
    
    for roll_combination in all_rolls:
        # Track the current state of dice after each roll
        current_dice = []
        current_targets = targets.copy()
        
        for roll in roll_combination:
            # If we've already met all targets, stop rolling
            if all(current_targets.get(num, 0) <= 0 for num in current_targets):
                break
            
            # Add the current roll to our dice
            current_dice.append(roll)
            
            # Update targets
            if roll in current_targets and current_targets[roll] > 0:
                current_targets[roll] -= 1
        
        # Check if we've met all targets
        if all(count <= 0 for count in current_targets.values()):
            successful_rolls += 1
    
    # Calculate probability
    probability = successful_rolls / total_rolls
    
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
                
                # Calculate attempts with rounding to prevent integer overflow
                attempts = max(1, round(1 / prob)) if prob > 0 else float('inf')
                
                print(f"\nProbability: {rounded_prob}")
                print(f"Percentage: {rounded_percentage}%")
                print(f"Approximately 1 in {attempts} attempts")
        
        except ValueError:
            print("\nInvalid input format. Please use 'number count, number count' format.")
        
        again = input("\nCalculate another probability? (y/n): ").lower()
        if again != 'y':
            break

if __name__ == "__main__":
    run_probability_calculation()
