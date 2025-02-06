#!/usr/bin/python3

# Imports
from tinydb import TinyDB
import json
import os
from rich.panel import Panel
from tinydb import TinyDB
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

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
    Represents the main game logic, including setting up the players, handling turns, and the flow of the game.
    This class coordinates all interactions between the game state, players, actions, and database.
    """

    def __init__(self) -> None:
        """
        Initializes the game, sets up the database, and prepares the players.
        It connects to the database, loads the card data, sets up the players, and starts the game.
        """
        self.console = Console()  # Create an instance of Console to display messages in the terminal.

        # Initialize the database with the provided path and setup the tables for heroes, spells, and units.
        self.hearthstone_db = Database.initialize_database(DATABASE_PATH)
        self.init_database(self.hearthstone_db, HEROES_TABLE_NAME, HEROES_DB_PATH)
        self.init_database(self.hearthstone_db, SPELLS_TABLE_NAME, SPELLS_DB_PATH)
        self.init_database(self.hearthstone_db, UNITS_TABLE_NAME, UNITS_DB_PATH)
    
        # Set up the interface for player choices and initialize both players.
        interface = PlayerChoiceInterface(self.hearthstone_db)
        player_1, player_2 = interface.setup_players()
        self.logic = GameLogic(player_1, player_2)  # Initialize game logic with two players.
        self.start()  # Start the game loop.

    def init_database(self, hearthstone_db: TinyDB, table_name: str, table_path: str) -> None:
        """
        Initializes a database table by loading data from a JSON file.
        
        Args:
            hearthstone_db (TinyDB): The TinyDB instance where the table resides.
            table_name (str): The name of the table to initialize.
            table_path (str): The path to the JSON file containing the data.
        
        Raises:
            TypeError: If the database or table name is not the expected type.
            ValueError: If the table path does not exist.
        """
        # Check for the correct types of inputs.
        if not isinstance(hearthstone_db, TinyDB):
            raise TypeError(f"Expected 'hearthstone_db' to be a TinyDB, got {type(hearthstone_db).__name__}")
        if not isinstance(table_name, str):
            raise TypeError(f"Expected 'table_name' to be a string, got {type(table_name).__name__}")
        if isinstance(table_path, str):
            if not os.path.exists(table_path):  # Check if the file exists at the given path.
                raise ValueError(f"Invalid table path: {table_path}. No such file or directory.")
        else:
            raise TypeError(f"Expected 'table_path' to be a string, got {type(table_path).__name__}")
        
        # Load the data from the JSON file.
        with open(table_path, "r") as file:
            table_data = json.load(file)

        # If the table exists, clear it and insert the new data; otherwise, just insert the data.
        if Database.fetch_all_from_table(hearthstone_db, table_name):
            Database.clear_table(hearthstone_db, table_name)
            Database.insert_data_to_table(hearthstone_db, table_name, table_data)
        else:
            Database.insert_data_to_table(hearthstone_db, table_name, table_data)

    def start(self) -> Player:
        """
        Starts the game loop where players alternate turns until the game ends.
        The game alternates between players, checking for game over conditions after each turn.
        Once the game ends, the winner is displayed.
        """
        turn_order = self.logic.choose_who_starts()  # Choose who starts the game.
        
        # Continue the game until there is a winner.
        while not self.logic.check_game_over():
            self.play_turn(turn_order[0], turn_order[1])  # Player 1's turn.

            if self.logic.check_game_over():
                break

            self.play_turn(turn_order[1], turn_order[0])  # Player 2's turn.

            if self.logic.check_game_over():
                break

        # Once the game is over, display the winner.
        self.console.clear()
        winner = self.logic.get_winner()
        self.stop(winner)

    def stop(self, winner: Player) -> None:
        """
        Ends the game and displays the winner.
        """
        self.console.clear()
        self.console.print(self.logic.print_winner(winner))  # Print the winner's message.

    def print_game(self, player: Player) -> None:
        """
        Prints the current game state including player stats, hand, board, and the active player's turn.
        
        Args:
            player (Player): The player whose turn is being printed.
        """
        self.console.clear()  # Clear the console.
        
        # Display the information for Player 1.
        self.console.print(Panel(f"[bold cyan]{self.logic.player_1.name}[/bold cyan]", border_style="blue", expand=False))
        self.console.print(self.logic.print_player_infos(self.logic.player_1))
        self.console.print(self.logic.print_player_in_hand_card(self.logic.player_1))

        # Display the game board.
        self.console.print(self.logic.print_board())

        # Display the information for Player 2.
        self.console.print(self.logic.print_player_in_hand_card(self.logic.player_2))
        self.console.print(self.logic.print_player_infos(self.logic.player_2))
        self.console.print(Panel(f"[bold cyan]{self.logic.player_2.name}[/bold cyan]", border_style="blue", expand=False))

        self.console.print()  # Add a blank line.
        self.console.print(Panel(f"[bold cyan]{player.name}'s turn[/bold cyan]", border_style="yellow", expand=False))

    def play_turn(self, player: Player, opponent: Player) -> None:
        """
        Executes the actions for one player's turn, including drawing cards, playing units/spells, using hero power, and attacking.
        
        Args:
            player (Player): The player whose turn it is.
            opponent (Player): The opponent player.
        """
        self.console.clear()  # Clear the console for the new turn.

        self.add_mana(player)  # Add mana for the player.
        self.draw_card(player)  # Draw a card for the player.
        played_card: bool = self.play_cards(player)  # Prompt player to play a card if possible.
        played_hero_power: bool = self.ask_hero_power(player)  # Ask if the player wants to use hero power.

        if not played_card:
            self.use_cards(player, opponent)  # Use the cards on the board if no card was played.

        if not played_hero_power:
            self.use_hero_power(player, opponent)  # Use hero power if it hasn't been used yet.

    def add_mana(self, player: Player) -> None:
        """
        Increase the player's mana by 1 if it is below the maximum limit.
        
        Args:
            player (Player): The player whose mana will be increased.
        """
        try:
            if player.mana < HERO_MAXIMUM_MANA:  # Check if mana is less than the maximum allowed.
                player.mana += 1  # Increase the player's mana by 1.
        except ValueError:
            raise

    def draw_card(self, player: Player) -> None:
        """
        Draw a card from the player's deck if they have space in their hand.
        
        Args:
            player (Player): The player drawing a card.
        """
        try:
            if len(player.deck.hand) < HAND_LIMIT and len(player.deck.cards) >= 1:  # Check hand space.
                player.deck.draw()  # Draw a card from the deck.
        except ValueError:
            raise

    def play_cards(self, player: Player) -> bool:
        """
        Allows the player to play a card from their hand if they have enough mana.
        Displays available cards and prompts the player for their choice.
        
        Args:
            player (Player): The player attempting to play a card.

        Returns:
            bool: True if a card was successfully played, False otherwise.
        """
        try:
            self.print_game(player)  # Display the game state.
            
            playable_cards = [card for card in player.deck.hand if card.cost <= player.mana]  # Filter playable cards.
            if not playable_cards or len(player.deck.board) == BOARD_LIMIT:  # No playable cards or board limit reached.
                return False

            # Display the playable cards in a table format.
            playable_card_table = Table(title="\n[bold cyan]Playable cards[/bold cyan]")
            playable_card_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
            playable_card_table.add_column("Name", justify="left", style="yellow")

            for i, card in enumerate(playable_cards):
                playable_card_table.add_row(str(i + 1), card.name)
            self.console.print(playable_card_table)

            card_choices = ["0"] + [str(i + 1) for i in range(len(playable_cards))]  # Choices for card selection.
            card_choice = Prompt.ask("[yellow]Enter the number of the playing card (or '0' to skip): [/yellow]", choices=card_choices, default="0")

            if card_choice == '0':  # If the player skips.
                return False

            try:
                index = int(card_choice) - 1
                card_to_play = playable_cards[index]

                if isinstance(card_to_play, Unit):  # If the card is a unit, reduce mana and play the card.
                    player.mana -= card_to_play.cost
                    player.deck.play_card(card_to_play)
                    return True
                elif isinstance(card_to_play, Spell):  # If the card is a spell, reduce mana and play the card.
                    player.mana -= card_to_play.cost
                    player.deck.play_card(card_to_play)
                    
                    # Display choosable cards (those to apply the spell effect to).
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

                    card_choices = ["0"] + [str(i + 1) for i in range(len(list(filter(lambda card: card != card_to_play, player.deck.board))))]  # Choices for choosing a card.
                    card_choice = Prompt.ask("[yellow]Enter the number of the playing card: [/yellow]", choices=card_choices, default="0")

                    if card_choice == '0':
                        selected_card = player
                    else:
                        index = int(card_choice) - 1
                        selected_card = player.deck.board[index]
                    try:
                        selected_card.apply_effects(card_to_play)  # Apply the spell effects.
                        player.deck.move_to_graveyard(card_to_play)  # Move the played card to the graveyard.
                        return True
                    except Exception as e:
                        raise
            except ValueError:
                raise
        except ValueError:
            raise

    def ask_hero_power(self, player: Player) -> bool:
        """
        Prompts the player to use their hero power if they have enough mana.

        Args:
            player (Player): The player considering using their hero power.

        Returns:
            None
        """
        try:
            # Check if the player has enough mana (4 or more)
            if player.mana >= 4:
                # Display the current game state
                self.print_game(player)

                # Define the possible choices (yes/no)
                answer_choices = ["o", "n"]
                
                # Ask the player if they want to use their hero power
                answer_choice = Prompt.ask(f"[yellow]Do you want to use {player.hero.name}'s hero power? [/yellow]", choices=answer_choices, default="n")

                # If the player answers 'yes'
                if answer_choice == "o":
                    try:
                        # Increase the player's attack by 2 and decrease their mana by 4
                        player.attack += 2
                        player.mana -= 4
                        
                        # Print the updated game state
                        self.print_game(player)
                        
                        # Return True indicating the hero power was used
                        return True
                    except Exception as e:
                        # Raise any exception that occurs (should handle specific exceptions in production)
                        raise
                else:
                    # If the player answers 'no', return False
                    return False
            else:
                # If the player doesn't have enough mana, return False
                return False
        except ValueError:
            # Catch any value errors that occur and raise them
            raise

    def use_cards(self, player: Player, opponent: Player) -> None:
        """
        Prompts the player to use their hero power if they have enough mana.

        Args:
            player (Player): The player considering using their hero power.

        Returns:
            bool: True if the hero power was used, False otherwise.
        """
        try:
            # Continuously prompt the player until they decide to stop
            while True:
                # Print the current game state
                self.print_game(player)
                
                # If the player has no cards on their board, break the loop
                if not player.deck.board:
                    break

                # Prepare a table displaying the player's cards
                choosable_card_table = Table(title="\n[bold cyan]Choosable cards[/bold cyan]")
                choosable_card_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
                choosable_card_table.add_column("Name", justify="left", style="yellow")
                choosable_card_table.add_column("Attack", justify="left", style="red")
                choosable_card_table.add_column("Health", justify="left", style="green")

                # Add each card from the player's board to the table
                for i, card in enumerate(player.deck.board):
                    choosable_card_table.add_row(str(i + 1), card.name, str(card.attack), str(card.health))
                
                # Display the table
                self.console.print(choosable_card_table)

                # Define possible choices for the player (select card or skip)
                card_choices = ["0"] + [str(i + 1) for i in range(len(player.deck.board))]
                
                # Ask the player which card they want to play
                card_choice = Prompt.ask("[yellow]Enter the number of the playing card (or '0' to skip): [/yellow]", choices=card_choices, default="0")

                # If the player chooses to skip, break the loop
                if card_choice == '0':
                    break

                try:
                    # Convert the player's choice into an integer index
                    index = int(card_choice) - 1
                    attacker = player.deck.board[index]

                    # Prepare a table displaying the opponent's targetable cards
                    targetable_card_table = Table(title="\n[bold cyan]Targetable cards[/bold cyan]")
                    targetable_card_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
                    targetable_card_table.add_column("Name", justify="left", style="yellow")
                    targetable_card_table.add_column("Health", justify="left", style="green")

                    # Add the opponent's name and health to the table
                    targetable_card_table.add_row(str(0), opponent.name, str(opponent.health))
                    
                    # Add the opponent's cards to the table
                    for i, card in enumerate(opponent.deck.board):
                        targetable_card_table.add_row(str(i + 1), card.name, str(card.health))
                    
                    # Display the table
                    self.console.print(targetable_card_table)

                    # Define possible choices for the target (select target or skip)
                    card_choices = ["0"] + [str(i + 1) for i in range(len(opponent.deck.board))]
                    
                    # Ask the player which target they want to attack
                    card_choice = Prompt.ask("[yellow]Enter the target card number: [/yellow]", choices=card_choices, default="0")

                    try:
                        # Convert the player's choice into an integer index for the target
                        target_index = int(card_choice) - 1
                        
                        # If the player chooses to attack the opponent directly
                        if target_index == -1:
                            target = opponent
                            attacker.attack_player_or_unit(target)
                            player.deck.move_to_graveyard(attacker)
                        
                        # If the player chooses to attack a specific card of the opponent
                        elif 0 <= target_index < len(opponent.deck.board):
                            target = opponent.deck.board[target_index]
                            attacker.attack_player_or_unit(target)
                            player.deck.move_to_graveyard(attacker)
                            
                            # If the target card is dead, move it to the graveyard
                            if target.health <= 0:
                                opponent.deck.move_to_graveyard(target)
                        
                        # Print the updated game state
                        self.print_game(player)
                    except ValueError:
                        # If there's an error with the player's input, raise the error
                        raise
                except ValueError:
                    # If there's an error with the player's card selection, raise the error
                    raise
        except ValueError:
            # Catch any value errors that occur and raise them
            raise

    def use_hero_power(self, player: Player, opponent: Player) -> None:
        """
        Allows the player to use their hero power to attack an opponent or their units, if they have attack points.

        Args:
            player (Player): The player using their hero power.
            opponent (Player): The opponent who may be attacked.

        Returns:
            None
        """
        try:
            # Check if the player has attack points
            if player.attack > 0:
                # Print the current game state
                self.print_game(player)

                # Define possible choices for the player (yes/no)
                answer_choices = ["o", "n"]
                
                # Ask the player if they want to attack with their hero power
                answer_choice = Prompt.ask(f"[yellow]Do you want to attack with {player.hero.name}? [/yellow]", choices=answer_choices, default="n")

                # If the player answers 'yes'
                if answer_choice == "o":
                    # Prepare a table displaying the opponent's targetable cards
                    target_card_table = Table(title="\n[bold cyan]Targetable cards[/bold cyan]")
                    target_card_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
                    target_card_table.add_column("Name", justify="left", style="yellow")
                    target_card_table.add_column("Health", justify="left", style="green")

                    # Add the opponent's name and health to the table
                    target_card_table.add_row(str(0), opponent.name, str(opponent.health))
                    
                    # Add the opponent's cards to the table
                    for i, card in enumerate(opponent.deck.board):
                        target_card_table.add_row(str(i + 1), card.name, str(card.health))
                    
                    # Display the table
                    self.console.print(target_card_table)

                    # Define possible choices for the target (select target or skip)
                    card_choices = ["0"] + [str(i + 1) for i in range(len(opponent.deck.board))]
                    
                    # Ask the player which target they want to attack
                    card_choice = Prompt.ask("[yellow]Enter the target card number: [/yellow]", choices=card_choices, default="0")

                    try:
                        # Convert the player's choice into an integer index for the target
                        target_index = int(card_choice) - 1
                        
                        # If the player chooses to attack the opponent directly
                        if target_index == -1:
                            target = opponent
                            player.attack_player_or_unit(target)
                        
                        # If the player chooses to attack a specific card of the opponent
                        elif 0 <= target_index < len(opponent.deck.board):
                            target = opponent.deck.board[target_index]
                            player.attack_player_or_unit(target)
                            
                            # If the target card is dead, move it to the graveyard
                            if target.health <= 0:
                                opponent.deck.move_to_graveyard(target)

                        # Reset the player's attack points after using hero power
                        player.attack = 0

                        # Print the updated game state
                        self.print_game(player)
                    except ValueError:
                        # If there's an error with the player's input, raise the error
                        raise
        except ValueError:
            # Catch any value errors that occur and raise them
            raise
