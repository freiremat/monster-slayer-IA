import random
import os

MAX_HEALTH = 100
STRONG_ATTACK_COOLDOWN = 3
HEAL_COOLDOWN = 5
HIGHSCORE_FILE = "highscores.txt"

def get_random_value(min_val, max_val):
    return random.randint(min_val, max_val)

def print_health(player_name, player_health, monster_health):
    print(f"\n{player_name} Health: {player_health} | Monster Health: {monster_health}\n")

def monster_attack(difficulty):
    base = (8, 15)
    if difficulty == "easy":
        return get_random_value(base[0] - 4, base[1] - 3)
    elif difficulty == "hard":
        return get_random_value(base[0] + 2, base[1] + 3)
    return get_random_value(*base)

def player_attack(strong, difficulty):
    base = (15, 25) if strong else (8, 13)
    if difficulty == "easy":
        return get_random_value(base[0] + 4, base[1] + 4)
    elif difficulty == "hard":
        return get_random_value(base[0] - 2, base[1] - 2)
    return get_random_value(*base)

def player_heal(difficulty):
    base = (10, 20)
    if difficulty == "easy":
        return get_random_value(base[0] + 8, base[1] + 10)
    elif difficulty == "hard":
        return get_random_value(base[0] - 5, base[1] - 3)
    return get_random_value(*base)

def choose_difficulty():
    print("\nChoose difficulty level:")
    print("1. Easy\n2. Normal\n3. Hard")
    while True:
        choice = input("Enter difficulty (1-3): ")
        if choice == "1":
            return "easy"
        elif choice == "2":
            return "normal"
        elif choice == "3":
            return "hard"
        else:
            print("Invalid choice. Please select 1, 2, or 3.")

def save_highscore(username, rounds):
    highscores = load_highscores()
    highscores.append((username, rounds))
    highscores.sort(key=lambda x: x[1])  # sort by rounds (ascending)

    with open(HIGHSCORE_FILE, "w") as f:
        for name, r in highscores:
            f.write(f"{name},{r}\n")

def load_highscores():
    highscores = []
    if not os.path.exists(HIGHSCORE_FILE):
        return highscores
    with open(HIGHSCORE_FILE, "r") as f:
        for line in f:
            if "," in line:
                name, r = line.strip().split(",")
                try:
                    highscores.append((name, int(r)))
                except ValueError:
                    continue
    return highscores

def print_highscores():
    print("\n📜 Highscores (Least Rounds to Win):")
    highscores = load_highscores()
    if not highscores:
        print("No highscores yet!")
    else:
        for i, (name, rounds) in enumerate(highscores[:10], 1):  # top 10
            print(f"{i}. {name} - {rounds} rounds")

def game_loop(player_name, difficulty):
    player_health = MAX_HEALTH
    monster_health = MAX_HEALTH
    turn_counter = 0

    print(f"\n🔥 {player_name} VS Monster 🔥 (Difficulty: {difficulty.capitalize()})")
    print_health(player_name, player_health, monster_health)

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
            dmg = player_attack(False, difficulty)
            monster_health -= dmg
            print(f"{player_name} hits the monster for {dmg} damage.")
        elif choice == "2" and turn_counter % STRONG_ATTACK_COOLDOWN == 0:
            dmg = player_attack(True, difficulty)
            monster_health -= dmg
            print(f"{player_name} performs a STRONG attack for {dmg} damage!")
        elif choice == "3" and turn_counter % HEAL_COOLDOWN == 0:
            heal = player_heal(difficulty)
            player_health = min(player_health + heal, MAX_HEALTH)
            print(f"{player_name} heals for {heal} HP.")
        elif choice == "4":
            print("You fled the battlefield. Game over.")
            return False
        else:
            print("Invalid or unavailable choice.")
            turn_counter -= 1
            continue

        if monster_health > 0:
            monster_dmg = monster_attack(difficulty)
            player_health -= monster_dmg
            print(f"Monster attacks {player_name} for {monster_dmg} damage.")

        print_health(player_name, player_health, monster_health)

    if player_health <= 0 and monster_health <= 0:
        print("It's a draw!")
    elif player_health <= 0:
        print(f"{player_name} lost! The monster defeated you.")
    else:
        print(f"🏆 Victory! {player_name} slayed the monster in {turn_counter} rounds!")
        save_highscore(player_name, turn_counter)
        print_highscores()

    return True

# Main Program
if __name__ == "__main__":
    player_name = input("Enter your player name: ")

    while True:
        difficulty = choose_difficulty()
        game_finished = game_loop(player_name, difficulty)
        if not game_finished:
            break
        again = input("Play again? (y/n): ").lower()
        if again != "y":
            break

    print(f"\n👋 Goodbye, {player_name}!")
