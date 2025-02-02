#!/usr/bin/python3

# Imports
import random

# Modules Imports
from modules.player_mod import Player

# Class
class GameLogic:
    """
    """

    def __init__(self, player_1: Player, player_2: Player = None):
        """
        """
        if not isinstance(player_1, Player):
            raise TypeError(f"Expected 'player_1' to be a Player, got {type(player_1).__name__}")
        self.player_1: Player = player_1

        if player_2 is not None and not isinstance(player_2, Player):
            raise TypeError(f"Expected 'player_2' to be a Player or None, got {type(player_2).__name__}")
        self.player_2: Player | None = player_2

    def choose_who_starts(self) -> tuple[Player, Player]:
        """
        """
        if self.player_2 is None:
            return self.player_1, None
        return (self.player_1, self.player_2) if random.choice([True, False]) else (self.player_2, self.player_1)
    
    def check_game_over(self) -> bool:
        """
        """
        return ((self.player_1.health == 0) or (self.player_2.health == 0))

    def get_winner(self) -> Player:
        """
        """
        if self.player_1.health == 0:
            return self.player_2
        else:
            return self.player_1

