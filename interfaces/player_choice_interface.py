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
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity
from enums.card_status_enum import CardStatus

# Class
class PlayerChoiceInterface():
    """
    """

    def __init__(self, hearthstone_db: TinyDB):
        """
        """
        self.hearthstone_db = hearthstone_db
        self.console = Console()

        self.heroes_table = Database.fetch_all_from_table(self.hearthstone_db, HEROES_TABLE_NAME)
        self.heroes = {hero_class: [hero["name"] for hero in heroes] for item in self.heroes_table for hero_class, heroes in item.items()}
        self.heroes_class = {str(idx + 1): hero_class for idx, hero_class in enumerate(self.heroes.keys())}

        self.units_table = Database.fetch_all_from_table(self.hearthstone_db, UNITS_TABLE_NAME)
        self.units = {unit_class: [unit for unit in units] for item in self.units_table for unit_class, units in item.items()}

        self.spells_table = Database.fetch_all_from_table(self.hearthstone_db, SPELLS_TABLE_NAME)
        self.spells = {spell_class: [spell for spell in spells] for item in self.spells_table for spell_class, spells in item.items()}

    def choose_game_mode(self) -> str:
        """
        Affichage amélioré du choix du mode de jeu.
        """
        self.console.clear()
        time.sleep(1)
        self.console.print(Panel("[bold cyan]Choose Your Game Mode[/bold cyan]", border_style="blue", expand=False))
        game_mode = Prompt.ask(
            "[yellow]Select Game Mode[/yellow]",
            choices=["PVP", "PVAI"],
            default="PVP"
        )
        self.console.clear()
        self.console.print(f"\n[green]✔ You selected:[/green] [bold cyan]{game_mode}[/bold cyan]")
        time.sleep(1)
        self.console.clear()

        return game_mode

    def setup_player(self, player_number: int) -> Player:
        """
        """
        self.console.clear()

        self.console.print(Panel(f"[bold cyan]Setting up player {player_number}[/bold cyan]", border_style="blue", expand=False))
        player_name = Prompt.ask("\n[yellow]What's your name?[/yellow]", default=f"Player{player_number}")
        self.console.clear()

        self.console.print(Panel(f"[bold cyan]Setting up player {player_number}[/bold cyan]", border_style="blue", expand=False))
        class_table = Table(title="\n[bold cyan]Available classes[/bold cyan]")
        class_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
        class_table.add_column("Classes", justify="left", style="yellow")

        for hero_class_index, hero_class in self.heroes_class.items():
            class_table.add_row(hero_class_index, hero_class)
        self.console.print(class_table)

        class_choice = Prompt.ask("[yellow]Enter your class number[/yellow]", choices=list(self.heroes_class.keys()), default=list(self.heroes_class.keys())[0])
        hero_names = {str(index + 1): hero_name for index, hero_name in enumerate(self.heroes[self.heroes_class[class_choice]])}
        self.console.clear()

        self.console.print(Panel(f"[bold cyan]Setting up player {player_number}[/bold cyan]", border_style="blue", expand=False))
        hero_table = Table(title="\n[bold cyan]Available heroes[/bold cyan]")
        hero_table.add_column("Index", justify="center", style="magenta", no_wrap=True)
        hero_table.add_column("Heroes", justify="left", style="yellow")

        for hero_name_index, hero_name in hero_names.items():
            hero_table.add_row(hero_name_index, hero_name)
        self.console.print(hero_table)

        hero_choice = IntPrompt.ask("[yellow]Enter your hero number[/yellow]", choices=list(hero_names.keys()), default=list(hero_names.keys())[0])
        selected_hero_name = hero_names[hero_choice]
        hero_data = None
        self.console.clear()

        self.console.print(Panel(f"[bold cyan]Setting up player {player_number}[/bold cyan]", border_style="blue", expand=False))
        with Progress() as progress:
            level_bar = progress.add_task("[green]Loading data...[/green]", total=33)
        
            for item in self.heroes_table:
                if self.heroes_class[class_choice] in item:
                    for hero in item[self.heroes_class[class_choice]]:
                        if hero["name"] == selected_hero_name:
                            hero_data = hero
                            break
            progress.update(level_bar, advance=1)

            if hero_data:
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
                print("[red]Error: Hero data not found![/red]")
                return None
            progress.update(level_bar, advance=1)
        
            hero_class = self.heroes_class[class_choice]
            class_units = self.units.get(hero_class, [])
            class_spells = self.spells.get(hero_class, [])

            if not class_units and not class_spells:
                print("[red]Warning: No cards found for this hero class![/red]")

            deck_cards = []

            for unit in class_units:
                deck_cards.append(Unit(
                    id=len(deck_cards) + 1,
                    name=unit["name"],
                    cost=unit["cost"],
                    attack=unit["attack"],
                    health=unit["health"],
                    unit_race=Race[unit["race"].upper()],
                    card_classes=[CardClass[hero_class.upper()]],
                    card_type=CardType.UNIT,
                    card_rarity=Rarity.COMMON,
                    status=CardStatus.IN_DECK
                ))
                progress.update(level_bar, advance=1)

            for spell in class_spells:
                deck_cards.append(Spell(
                    id=len(deck_cards) + 1,
                    name=spell["name"],
                    cost=spell["cost"],
                    description=spell["description"],
                    card_classes=[CardClass[hero_class.upper()]],
                    card_type=CardType.SPELL,
                    card_rarity=Rarity.COMMON,
                    status=CardStatus.IN_DECK
                ))
                progress.update(level_bar, advance=1)

            deck = Deck(cards=deck_cards)
            progress.update(level_bar, advance=1)

        print(f"[green]Deck created with {len(deck_cards)} cards for {player_name}.[/green]")
        time.sleep(2)

        return Player(name=player_name, hero=selected_hero, deck=deck)
    
    def setup_players(self) -> tuple[Player, Player | None]:
        """
        """
        game_mode = self.choose_game_mode()

        if game_mode == "PVP":
            player_1 = self.setup_player(player_number=1)
            player_2 = self.setup_player(player_number=2)
        elif game_mode == "PVAI":
            print("[yellow]Work in progress.[/yellow]")
        else:
            raise ValueError("Invalid game mode")
        return player_1, player_2
