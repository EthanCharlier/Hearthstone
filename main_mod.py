#!/usr/bin/python3

# Import the game module
from core.game_mod import Game

# Define the main class
class Main:
    """
    Main class that initializes and starts the game.
    """

    def __init__(self):
        # Start the game
        Game()

# Run the script only if executed directly
if __name__ == "__main__":
    Main()
