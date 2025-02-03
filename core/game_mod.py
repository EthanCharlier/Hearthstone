#!/usr/bin/python3

# Imports
from tinydb import TinyDB
import json
import os
import time
from rich import print
from rich.panel import Panel
from tinydb import TinyDB
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.progress import Progress

# Core Imports
from core.game_logic import GameLogic

# Modules Imports
from modules.player_mod import Player
from modules.unit_mod import Unit
from modules.spell_mod import Spell

# Utils Imports
from utils.constants import (
     DATABASE_PATH,
     HEROES_DB_PATH,
     HEROES_TABLE_NAME,
     SPELLS_TABLE_NAME,
     SPELLS_DB_PATH,
     UNITS_DB_PATH,
     UNITS_TABLE_NAME,
     HERO_MAXIMUM_MANA,
     HAND_LIMIT,
     BOARD_LIMIT
)
from utils.database_utils import Database

# Interfaces Imports
from interfaces.player_choice_interface import PlayerChoiceInterface

# Class
class Game:
    """
    """

    def __init__(self) -> None:
        """
        """
        self.console = Console()

        self.hearthstone_db = Database.initialize_database(DATABASE_PATH)
        self.init_database(self.hearthstone_db, HEROES_TABLE_NAME, HEROES_DB_PATH)
        self.init_database(self.hearthstone_db, SPELLS_TABLE_NAME, SPELLS_DB_PATH)
        self.init_database(self.hearthstone_db, UNITS_TABLE_NAME, UNITS_DB_PATH)
    
        interface = PlayerChoiceInterface(self.hearthstone_db)
        player_1, player_2 = interface.setup_players()
        self.logic = GameLogic(player_1, player_2)
        self.start()


    def init_database(self, hearthstone_db: TinyDB, table_name: str, table_path: str) -> None:
        """
        """
        if not isinstance(hearthstone_db, TinyDB):
            raise TypeError(f"Expected 'hearthstone_db' to be a TinyDB, got {type(hearthstone_db).__name__}")
        if not isinstance(table_name, str):
            raise TypeError(f"Expected 'table_name' to be a string, got {type(table_name).__name__}")
        if isinstance(table_path, str):
            if not os.path.exists(table_path):
                raise ValueError(f"Invalid table path: {table_path}. No such file or directory.")
        else:
            raise TypeError(f"Expected 'table_path' to be a string, got {type(table_path).__name__}")
        
        with open(table_path, "r") as file:
            table_data = json.load(file)

        if Database.fetch_all_from_table(hearthstone_db, table_name):
            Database.clear_table(hearthstone_db, table_name)
            Database.insert_data_to_table(hearthstone_db, table_name, table_data)
        else:
            Database.insert_data_to_table(hearthstone_db, table_name, table_data)

    def start(self) -> Player:
        """
        """
        turn_order = self.logic.choose_who_starts()
        
        while not self.logic.check_game_over():
            self.play_turn(turn_order[0], turn_order[1])

            if self.logic.check_game_over():
                break

            self.play_turn(turn_order[1], turn_order[0])

            if self.logic.check_game_over():
                break

        self.console.clear()
        winner = self.logic.get_winner()
        print(winner)

    def print_game(self, player: Player) -> None:
        self.console.clear()
        self.console.print(Panel(f"[bold cyan]{self.logic.player_1.name}[/bold cyan]", border_style="blue", expand=False))
        self.console.print(self.logic.print_player_infos(self.logic.player_1))
        self.console.print(self.logic.print_player_in_hand_card(self.logic.player_1))

        self.console.print(self.logic.print_board())

        self.console.print(self.logic.print_player_in_hand_card(self.logic.player_2))
        self.console.print(self.logic.print_player_infos(self.logic.player_2))
        self.console.print(Panel(f"[bold cyan]{self.logic.player_2.name}[/bold cyan]", border_style="blue", expand=False))

        self.console.print()
        self.console.print(Panel(f"[bold cyan]{player.name}'s turn[/bold cyan]", border_style="yellow", expand=False))

    def play_turn(self, player: Player, opponent: Player) -> None:
        """
        """
        self.console.clear()

        # Étape 1 : Gain de mana (max HERO_MAXIMUM_MANA)
        if player.mana < HERO_MAXIMUM_MANA:
            player.mana += 1

        # Étape 2 : Pioche d’une carte
        try:
            if len(player.deck.hand) < HAND_LIMIT and len(player.deck.cards) >= 1:
                player.deck.draw()
        except ValueError:
            raise

        # Étape 3 : Jouer des cartes (Serviteurs et Sorts)
        while True:
            self.print_game(player)
            
            playable_cards = [card for card in player.deck.hand if card.cost <= player.mana]
            if not playable_cards or len(player.deck.board) == BOARD_LIMIT:
                break

            playable_card_table = Table(title="\n[bold cyan]Playable cards[/bold cyan]")
            playable_card_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
            playable_card_table.add_column("Name", justify="left", style="yellow")

            for i, card in enumerate(playable_cards):
                playable_card_table.add_row(str(i + 1), card.name)
            self.console.print(playable_card_table)

            card_choices = ["0"] + [str(i + 1) for i in range(len(playable_cards))]
            card_choice = Prompt.ask("[yellow]Enter the number of the playing card (or '0' to skip): [/yellow]", choices=card_choices, default="0")

            if card_choice == '0':
                break

            try:
                index = int(card_choice) - 1
                card_to_play = playable_cards[index]

                if isinstance(card_to_play, Unit):
                    player.mana -= card_to_play.cost
                    player.deck.play_card(card_to_play)
                elif isinstance(card_to_play, Spell):
                    player.mana -= card_to_play.cost
                    player.deck.play_card(card_to_play)
                    
                    choosable_card_table = Table(title="\n[bold cyan]Choosable cards[/bold cyan]")
                    choosable_card_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
                    choosable_card_table.add_column("Name", justify="left", style="yellow")
                    choosable_card_table.add_column("Attack", justify="left", style="red")
                    choosable_card_table.add_column("Health", justify="left", style="green")
                    choosable_card_table.add_column("Armor", justify="left", style="white")

                    choosable_card_table.add_row(str(0), player.name, str(player.attack), str(player.health), str(player.armor))
                    for i, card in enumerate(list(filter(lambda card: card != card_to_play, player.deck.board))):
                        choosable_card_table.add_row(str(i + 1), card.name, str(card.attack), str(card.health), str(card.armor))
                    self.console.print(choosable_card_table)

                    card_choices = ["0"] + [str(i + 1) for i in range(len(list(filter(lambda card: card != card_to_play, player.deck.board))))]
                    card_choice = Prompt.ask("[yellow]Enter the number of the playing card: [/yellow]", choices=card_choices, default="0")

                    if card_choice == '0':
                        selected_card = player
                    else:
                        index = int(card_choice) - 1
                        selected_card = player.deck.board[index]

                    try:
                        print(selected_card, card_to_play)
                        selected_card.apply_effects(card_to_play)
                        player.deck.move_to_graveyard(card_to_play)
                    except Exception as e:
                        raise
            except ValueError:
                raise

        self.print_game(player)

        # Étape 4 : Pouvoir héroïque (coût : 2 mana)
        if player.mana >= 4:
            answer_choices = ["o", "n"]
            answer_choice = Prompt.ask(f"[yellow]Do you want to use {player.hero.name}'s hero power? [/yellow]", choices=answer_choices, default="n")

            if answer_choice == "o":
                try:
                    player.attack += 2
                    player.mana -= 4
                    self.print_game(player)
                except Exception as e:
                    raise

        # Étape 5 : Attaques (Serviteurs et Héros)
        while True:
            self.print_game(player)
            
            if not player.deck.board:
                break

            choosable_card_table = Table(title="\n[bold cyan]Choosable cards[/bold cyan]")
            choosable_card_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
            choosable_card_table.add_column("Name", justify="left", style="yellow")
            choosable_card_table.add_column("Attack", justify="left", style="red")
            choosable_card_table.add_column("Health", justify="left", style="green")

            for i, card in enumerate(player.deck.board):
                choosable_card_table.add_row(str(i + 1), card.name, str(card.attack), str(card.health))
            self.console.print(choosable_card_table)

            card_choices = ["0"] + [str(i + 1) for i in range(len(player.deck.board))]
            card_choice = Prompt.ask("[yellow]Enter the number of the playing card (or '0' to skip): [/yellow]", choices=card_choices, default="0")

            if card_choice == '0':
                break

            try:
                index = int(card_choice) - 1
                attacker = player.deck.board[index]

                targetable_card_table = Table(title="\n[bold cyan]Targetable cards[/bold cyan]")
                targetable_card_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
                targetable_card_table.add_column("Name", justify="left", style="yellow")
                targetable_card_table.add_column("Health", justify="left", style="green")

                targetable_card_table.add_row(str(0), opponent.name, str(opponent.health))
                for i, card in enumerate(opponent.deck.board):
                    targetable_card_table.add_row(str(i + 1), card.name, str(card.health))
                self.console.print(targetable_card_table)

                card_choices = ["0"] + [str(i + 1) for i in range(len(opponent.deck.board))]
                card_choice = Prompt.ask("[yellow]Enter the target card number: [/yellow]", choices=card_choices, default="0")

                try:
                    target_index = int(card_choice) - 1
                    if target_index == -1:
                        target = opponent
                        attacker.attack_player_or_unit(target)
                        player.deck.move_to_graveyard(attacker)
                    elif 0 <= target_index < len(opponent.deck.board):
                        target = opponent.deck.board[target_index]
                        attacker.attack_player_or_unit(target)
                        player.deck.move_to_graveyard(attacker)
                        if target.health <= 0:
                            opponent.deck.move_to_graveyard(target)
                except ValueError:
                    raise

            except ValueError:
                raise

        # Attaque du héros
        if player.attack > 0:
            answer_choices = ["o", "n"]
            answer_choice = Prompt.ask(f"[yellow]Do you want to attack with {player.hero.name}? [/yellow]", choices=answer_choices, default="n")

            if answer_choice == "o":
                target_card_table = Table(title="\n[bold cyan]Targetable cards[/bold cyan]")
                target_card_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
                target_card_table.add_column("Name", justify="left", style="yellow")
                target_card_table.add_column("Health", justify="left", style="green")

                target_card_table.add_row(str(0), opponent.name, str(opponent.health))
                for i, card in enumerate(opponent.deck.board):
                    target_card_table.add_row(str(i + 1), card.name, str(card.health))
                self.console.print(target_card_table)

                card_choices = ["0"] + [str(i + 1) for i in range(len(opponent.deck.board))]
                card_choice = Prompt.ask("[yellow]Enter the target card number: [/yellow]", choices=card_choices, default="0")

                try:
                    target_index = int(card_choice) - 1
                    if target_index == -1:
                        target = opponent
                        player.attack_player_or_unit(target)
                    elif 0 <= target_index < len(opponent.deck.board):
                        target = opponent.deck.board[target_index]
                        player.attack_player_or_unit(target)
                        if target.health <= 0:
                            opponent.deck.move_to_graveyard(target)

                    player.attack = 0
                except ValueError:
                    raise
