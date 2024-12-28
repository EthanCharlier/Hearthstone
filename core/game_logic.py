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
        self.player_1 = player_1
        self.player_2 = player_2

    def choose_who_starts(self) -> tuple[Player, Player]:
        """
        """
        if self.player_2 is None:
            return self.player_1, None
        return (self.player_1, self.player_2) if random.choice([True, False]) else (self.player_2, self.player_1)
    
    def check_game_over(self) -> bool:
        """
        """
        pass

    def get_winner(self) -> Player:
        """
        """
        pass
