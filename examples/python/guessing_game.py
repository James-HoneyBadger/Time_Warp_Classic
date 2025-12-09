#!/usr/bin/env python3
"""
Python Number Guessing Game
An interactive game demonstrating input/output and control flow
"""
# pylint: disable=C0116,R1705

import random


def play_game():
    print("Python Number Guessing Game")
    print("=" * 30)
    print()

    # Generate random number between 1 and 100
    secret_number = random.randint(1, 100)
    attempts = 0
    max_attempts = 7

    print("I'm thinking of a number between 1 and 100.")
    print(f"You have {max_attempts} attempts to guess it!")
    print()

    while attempts < max_attempts:
        try:
            guess = int(input("Enter your guess: "))
            attempts += 1

            if guess == secret_number:
                print(f"🎉 Congratulations! You guessed it in {attempts} attempts!")
                return True
            elif guess < secret_number:
                print("Too low! Try a higher number.")
            else:
                print("Too high! Try a lower number.")

            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Attempts remaining: {remaining}")
            print()

        except ValueError:
            print("Please enter a valid number!")
            print()

    print(f"❌ Game over! The number was {secret_number}.")
    return False


# Main program
if __name__ == "__main__":
    play_game()

    while True:
        play_again = input("Play again? (y/n): ").lower()
        if play_again == "y":
            print()
            play_game()
        elif play_again == "n":
            print("Thanks for playing!")
            break
        else:
            print("Please enter 'y' or 'n'.")
