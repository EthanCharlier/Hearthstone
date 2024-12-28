#!/usr/bin/python3

# Core Imports
from core.game_logic import GameLogic

# Modules Imports
from modules.player_mod import Player

# Class
class Game:
    """
    """

    def __init__(self, player_1: Player, player_2: Player = None) -> None:
        """
        """
        self.player_1 = player_1
        self.player_2 = player_2
        self.logic = GameLogic(player_1, player_2)

        if player_2 is None:
            print(f"{player_1.name} vs AI")
        else:
            print(f"{player_1.name} vs {player_2.name}")

    def start(self) -> Player:
        """
        """
        turn_order = self.logic.choose_who_starts()

        while not self.logic.check_game_over():
            self.play_turn(turn_order[0])
            if self.logic.check_game_over():
                break
            self.play_turn(turn_order[1])

        winner = self.logic.get_winner()

    def play_turn(self, player: Player) -> None:
        """
        """
        if player is None:
            pass
