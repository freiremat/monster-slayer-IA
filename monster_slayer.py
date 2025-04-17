import random

# Constants
MAX_HEALTH = 100
STRONG_ATTACK_COOLDOWN = 3
HEAL_COOLDOWN = 5

def get_random_value(min_val, max_val):
    return random.randint(min_val, max_val)

def print_health(player_health, monster_health):
    print(f"\nPlayer Health: {player_health} | Monster Health: {monster_health}\n")

def monster_attack():
    return get_random_value(8, 15)

def player_attack(strong=False):
    if strong:
        return get_random_value(15, 25)
    else:
        return get_random_value(8, 13)

def player_heal():
    return get_random_value(10, 20)

def game_loop():
    player_health = MAX_HEALTH
    monster_health = MAX_HEALTH
    turn_counter = 0

    print("🔥 Welcome to Monster Slayer 🔥")
    print_health(player_health, monster_health)

    while player_health > 0 and monster_health > 0:
        turn_counter += 1
        print("Choose your action:")
        options = ["1. Regular Attack"]
        if turn_counter % STRONG_ATTACK_COOLDOWN == 0:
            options.append("2. Strong Attack")
        if turn_counter % HEAL_COOLDOWN == 0:
            options.append("3. Heal")
        options.append("4. Quit Game")
        print("\n".join(options))

        choice = input("Enter your choice: ")

        if choice == "1":
            dmg = player_attack()
            monster_health -= dmg
            print(f"You hit the monster for {dmg} damage.")
        elif choice == "2" and turn_counter % STRONG_ATTACK_COOLDOWN == 0:
            dmg = player_attack(strong=True)
            monster_health -= dmg
            print(f"You perform a STRONG attack for {dmg} damage!")
        elif choice == "3" and turn_counter % HEAL_COOLDOWN == 0:
            heal = player_heal()
            player_health = min(player_health + heal, MAX_HEALTH)
            print(f"You heal yourself for {heal} HP.")
        elif choice == "4":
            print("You fled the battlefield. Game over.")
            return
        else:
            print("Invalid or unavailable choice.")
            turn_counter -= 1  # No valid action taken, don't count this turn
            continue

        # Monster retaliates
        if monster_health > 0:
            monster_dmg = monster_attack()
            player_health -= monster_dmg
            print(f"Monster attacks you for {monster_dmg} damage.")

        print_health(player_health, monster_health)

    # Game over
    if player_health <= 0 and monster_health <= 0:
        print("It's a draw!")
    elif player_health <= 0:
        print("You lost! The monster defeated you.")
    else:
        print("Victory! You slayed the monster!")

    # Restart?
    again = input("Play again? (y/n): ").lower()
    if again == "y":
        game_loop()

# Start the game
if __name__ == "__main__":
    game_loop()
