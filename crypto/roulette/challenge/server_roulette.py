from hashlib import sha256
import secrets


def get_color(number):
    """Determine roulette color for a given number"""
    if number == 0:
        return 'green'
    return 'red' if number % 2 == 1 else 'black'


def main():
    print("Welcome to Provably Fair Roulette!")

    with open('flag', 'rt') as f:
        FLAG = f.read()

    streak_13 = 0
    while True:
        # Generate server seed and its hash
        server_seed = sha256(bytes(secrets.randbits(17))).hexdigest()
        server_seed_hash = sha256(server_seed.encode()).hexdigest()

        print(f"Server seed hash (verify later): {server_seed_hash}")

        # Get client seed
        print("Enter your client seed (press enter to generate): ", end="")
        client_seed = input().strip()
        if not client_seed:
            client_seed = secrets.token_bytes(8).hex()
            print(f"Generated client seed: {client_seed}")

        # Generate game hash
        combined = f"{server_seed}:{client_seed}"
        game_hash = sha256(combined.encode()).hexdigest()
        hash_int = int(game_hash, 16)

        # Calculate roulette result
        roulette_number = hash_int % 37  # 0-36
        roulette_color = get_color(roulette_number)

        # Get user's bet
        while True:
            print("Place your bet (number 0-36 or color red/black/green): ", end="")
            bet = input().strip().lower()
            if bet in ['green', 'red', 'black']:
                break
            try:
                num = int(bet)
                if 0 <= num <= 36:
                    bet = str(num)  # Standardize to string for comparison
                    break
                print("Number must be between 0-36")
            except ValueError:
                print("Invalid bet. Enter number (0-36) or color (red/black/green)")

        # Determine result
        result_str = f"{roulette_number} ({roulette_color})"
        print(f"\nThe wheel lands on: {result_str}")

        # Check win conditions
        win = False
        if bet.isdigit():
            win = int(bet) == roulette_number
        else:
            win = bet == roulette_color

        if win:
            print("Congratulations! You win! ")
            if roulette_number == 13:
                print("...and you got 13, double congratulations!")
                streak_13 += 1
            else:
                print("But it's not 13, no streak for you")
                streak_13 = 0
        else:
            print("Sorry, you lose!")
            streak_13 = 0

        # Verification information
        print()
        print("Verification Details:")
        print(f"Server seed: {server_seed}")
        print(f"Client seed: {client_seed}")
        print(f"Combined string: {combined}")
        print(f"Game hash: {game_hash}")
        print(f"Calculated number: {roulette_number}")
        print(f"Resulting color: {roulette_color}")

        if streak_13 == 37:
            print("How? How is it possible? What was the chance?! "
                  f"Anyway, here's your flag, congratulations... {FLAG}")
            exit()


if __name__ == "__main__":
    main()
