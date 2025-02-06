#!/usr/bin/python3

# Imports
import time
from rich import print
from rich.panel import Panel
from tinydb import TinyDB
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.progress import Progress

# Modules Imports
from modules.hero_mod import Hero
from modules.unit_mod import Unit
from modules.spell_mod import Spell
from modules.deck_mod import Deck
from modules.player_mod import Player

# Utils Imports
from utils.constants import HEROES_TABLE_NAME, SPELLS_TABLE_NAME, UNITS_TABLE_NAME
from utils.database_utils import Database

# Enum Imports
from enums.card_class_enum import CardClass
from enums.hero_power_enum import HeroPower
from enums.race_enum import Race
from enums.rarity_enum import Rarity
from enums.card_status_enum import CardStatus

# Class
class PlayerChoiceInterface():
    """
    Handles the player's choice interface, allowing them to select a game mode, 
    choose a hero, and set up their deck.
    """

    def __init__(self, hearthstone_db: TinyDB):
        """
        Initializes the PlayerChoiceInterface.

        Args:
            hearthstone_db (TinyDB): The database containing the game data.
        """
        self.hearthstone_db = hearthstone_db  # Store the database reference
        self.console = Console()  # Initialize the Console object for styled output

        # Fetch and organize all hero data from the database
        self.heroes_table = Database.fetch_all_from_table(self.hearthstone_db, HEROES_TABLE_NAME)
        self.heroes = {hero_class: [hero["name"] for hero in heroes] for item in self.heroes_table for hero_class, heroes in item.items()}
        self.heroes_class = {str(idx + 1): hero_class for idx, hero_class in enumerate(self.heroes.keys())}  # Mapping class indexes to hero classes

        # Fetch and organize all unit data from the database
        self.units_table = Database.fetch_all_from_table(self.hearthstone_db, UNITS_TABLE_NAME)
        self.units = {unit_class: [unit for unit in units] for item in self.units_table for unit_class, units in item.items()}

        # Fetch and organize all spell data from the database
        self.spells_table = Database.fetch_all_from_table(self.hearthstone_db, SPELLS_TABLE_NAME)
        self.spells = {spell_class: [spell for spell in spells] for item in self.spells_table for spell_class, spells in item.items()}

    def choose_game_mode(self) -> str:
        """
        Displays an enhanced interface for selecting the game mode.

        Returns:
            str: The selected game mode ("PVP" or "PVAI").
        """
        self.console.clear()  # Clear the console screen
        time.sleep(1)  # Pause for a brief moment
        self.console.print(Panel("[bold cyan]Choose Your Game Mode[/bold cyan]", border_style="blue", expand=False))  # Display a panel with the title
        # Prompt the user to select a game mode with a list of options
        game_mode = Prompt.ask(
            "[yellow]Select Game Mode[/yellow]",
            choices=["PVP"],  # Only allowing "PVP" for now
            default="PVP"  # Default to "PVP"
        )
        self.console.clear()  # Clear the console screen
        self.console.print(f"\n[green]✔ You selected:[/green] [bold cyan]{game_mode}[/bold cyan]")  # Show the selected game mode
        time.sleep(1)  # Pause for a brief moment
        self.console.clear()  # Clear the console again

        return game_mode  # Return the selected game mode

    def setup_player(self, player_number: int) -> Player:
        """
        Sets up a player by asking for their name, selecting a hero, 
        and creating their deck.

        Args:
            player_number (int): The number of the player (1 or 2).

        Returns:
            Player: The initialized Player object.
        """
        self.console.clear()  # Clear the console screen

        # Display setup header for the player
        self.console.print(Panel(f"[bold cyan]Setting up player {player_number}[/bold cyan]", border_style="blue", expand=False))
        # Ask for the player's name
        player_name = Prompt.ask("\n[yellow]What's your name?[/yellow]", default=f"Player{player_number}")
        self.console.clear()  # Clear the console screen again

        # Display available classes
        self.console.print(Panel(f"[bold cyan]Setting up player {player_number}[/bold cyan]", border_style="blue", expand=False))
        class_table = Table(title="\n[bold cyan]Available classes[/bold cyan]")  # Initialize a table to display classes
        class_table.add_column("Index", justify="center", style="magenta", no_wrap=True)  # Add columns for index and class name
        class_table.add_column("Classes", justify="left", style="yellow")

        # Populate the table with class options
        for hero_class_index, hero_class in self.heroes_class.items():
            class_table.add_row(hero_class_index, hero_class)
        self.console.print(class_table)  # Display the table of available classes

        # Prompt the user to select a class
        class_choice = Prompt.ask("[yellow]Enter your class number[/yellow]", choices=list(self.heroes_class.keys()), default=list(self.heroes_class.keys())[0])
        # Get available hero names based on the selected class
        hero_names = {str(index + 1): hero_name for index, hero_name in enumerate(self.heroes[self.heroes_class[class_choice]])}
        self.console.clear()  # Clear the console screen again

        # Display available heroes for the selected class
        self.console.print(Panel(f"[bold cyan]Setting up player {player_number}[/bold cyan]", border_style="blue", expand=False))
        hero_table = Table(title="\n[bold cyan]Available heroes[/bold cyan]")  # Initialize a table for heroes
        hero_table.add_column("Index", justify="center", style="magenta", no_wrap=True)  # Add columns for hero index and name
        hero_table.add_column("Heroes", justify="left", style="yellow")

        # Populate the hero table with available heroes
        for hero_name_index, hero_name in hero_names.items():
            hero_table.add_row(hero_name_index, hero_name)
        self.console.print(hero_table)  # Display the table of available heroes

        # Prompt the user to select a hero
        hero_choice = IntPrompt.ask("[yellow]Enter your hero number[/yellow]", choices=list(hero_names.keys()), default=list(hero_names.keys())[0])
        selected_hero_name = hero_names[hero_choice]  # Get the selected hero's name
        hero_data = None  # Initialize hero_data to store hero information
        self.console.clear()  # Clear the console screen again

        # Display loading progress
        self.console.print(Panel(f"[bold cyan]Setting up player {player_number}[/bold cyan]", border_style="blue", expand=False))
        with Progress() as progress:  # Use the Progress context manager to display a loading progress bar
            level_bar = progress.add_task("[green]Loading data...[/green]", total=33)  # Create a new progress bar for loading
            # Find the hero's data from the fetched hero table
            for item in self.heroes_table:
                if self.heroes_class[class_choice] in item:
                    for hero in item[self.heroes_class[class_choice]]:
                        if hero["name"] == selected_hero_name:
                            hero_data = hero  # Store the selected hero's data
                            break
            progress.update(level_bar, advance=1)  # Update the progress bar after checking hero data

            if hero_data:
                # Create a Hero object using the fetched data
                selected_hero = Hero(
                    id=hero_data["id"],
                    name=hero_data["name"],
                    description=hero_data["description"],
                    hero_class=CardClass[hero_data["hero_class"].upper()],
                    hero_power=HeroPower[hero_data["hero_power"].upper()],
                    attack=hero_data["attack"],
                    health=hero_data["health"],
                    mana=hero_data["mana"],
                    armor=hero_data["armor"]
                )
            else:
                print("[red]Error: Hero data not found![/red]")  # Print error if no hero data is found
                return None  # Return None if no hero data was found
            progress.update(level_bar, advance=1)  # Update the progress bar

            # Set up the deck for the selected hero class
            hero_class = self.heroes_class[class_choice]
            class_units = self.units.get(hero_class, [])  # Get units related to the selected class
            class_spells = self.spells.get(hero_class, [])  # Get spells related to the selected class

            if not class_units and not class_spells:
                print("[red]Warning: No cards found for this hero class![/red]")  # Show warning if no units or spells found

            deck_cards = []  # Initialize a list to store the deck cards

            # Add units to the deck
            for unit in class_units:
                deck_cards.append(Unit(
                    id=len(deck_cards) + 1,
                    name=unit.get("name", ""),
                    cost=unit.get("cost", 0),
                    description=unit.get("description", ""),
                    attack=unit.get("attack", 0),
                    health=unit.get("health", 0),
                    armor=unit.get("armor", 0),
                    unit_race=Race[unit.get("race", "ALL").upper()],
                    card_classes=[CardClass[hero_class.upper()]],
                    card_rarity=Rarity.COMMON,
                    status=CardStatus.IN_DECK
                ))
                progress.update(level_bar, advance=1)  # Update the progress bar after adding each unit to the deck

            # Add spells to the deck
            for spell in class_spells:
                deck_cards.append(Spell(
                    id=len(deck_cards) + 1,
                    name=spell.get("name", ""),
                    cost=spell.get("cost", 0),
                    description=spell.get("description", ""),
                    attack=spell.get("attack", 0),
                    health=spell.get("health", 0),
                    armor=spell.get("armor", 0),
                    card_classes=[CardClass[hero_class.upper()]],
                    card_rarity=Rarity.COMMON,
                    status=CardStatus.IN_DECK
                ))
                progress.update(level_bar, advance=1)  # Update the progress bar after adding each spell to the deck

            # Create and shuffle the deck
            deck = Deck(cards=deck_cards)
            deck.shuffle()
            progress.update(level_bar, advance=1)  # Final progress bar update

        print(f"[green]Deck created with {len(deck_cards)} cards for {player_name}.[/green]")  # Show deck creation message
        time.sleep(2)  # Pause for a brief moment

        return Player(name=player_name, hero=selected_hero, deck=deck)  # Return the initialized Player object

    def setup_players(self) -> tuple[Player, Player | None]:
        """
        Initializes both players based on the selected game mode.

        Returns:
            tuple[Player, Player | None]: The two players (or one if AI is chosen).
        """
        game_mode = self.choose_game_mode()  # Get the selected game mode

        if game_mode == "PVP":  # Check if the game mode is PVP
            player_1 = self.setup_player(player_number=1)  # Set up player 1
            player_2 = self.setup_player(player_number=2)  # Set up player 2
        else:
            raise ValueError("Invalid game mode")  # Raise an error for invalid game mode
        return player_1, player_2  # Return both players
