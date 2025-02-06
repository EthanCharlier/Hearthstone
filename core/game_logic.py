#!/usr/bin/python3

# Imports
import random
from rich.columns import Columns
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

# Modules Imports
from modules.player_mod import Player
from modules.unit_mod import Unit

# Class
class GameLogic:
    """
    Class responsible for handling the core game logic such as turn order, game-over conditions, 
    player and board state management, and printing of the game's visual elements.
    """

    def __init__(self, player_1: Player, player_2: Player = None):
        """
        Initializes the game logic with two players.

        Args:
            player_1 (Player): The first player.
            player_2 (Player, optional): The second player. Defaults to None.
        """
        if not isinstance(player_1, Player):
            raise TypeError(f"Expected 'player_1' to be a Player, got {type(player_1).__name__}")
        self.player_1: Player = player_1

        if player_2 is not None and not isinstance(player_2, Player):
            raise TypeError(f"Expected 'player_2' to be a Player or None, got {type(player_2).__name__}")
        self.player_2: Player | None = player_2

    def choose_who_starts(self) -> tuple[Player, Player]:
        """
        Randomly selects which player will start the game.

        Returns:
            tuple[Player, Player]: A tuple containing the first player and second player (or None if only one player).
        """
        if self.player_2 is None:
            return self.player_1, None
        return (self.player_1, self.player_2) if random.choice([True, False]) else (self.player_2, self.player_1)
    
    def check_game_over(self) -> bool:
        """
        Checks if the game is over by evaluating the health of both players.

        Returns:
            bool: True if either player has 0 health, indicating the game is over; False otherwise.
        """
        return ((self.player_1.health <= 0) or (self.player_2.health <= 0))

    def get_winner(self) -> Player:
        """
        Determines the winner of the game.

        Returns:
            Player: The player who has won the game (the one whose health is not 0).
        """
        if self.player_1.health <= 0:
            return self.player_2
        else:
            return self.player_1
        
    def print_winner(self, winner: Player) -> Columns:
        """
        Create and return a formatted panel displaying the winner's name.

        Args:
            winner (Player): The player who won the game.

        Returns:
            Columns: A Rich Columns object containing a panel with the winner's name.
        """
        winner_panel = Panel(
            Text(f"{winner.name}", style="bold yellow"),
            title="Winner",
            border_style="yellow",
            expand=False
        )

        return Columns([winner_panel])
        
    def print_player_infos(self, player: Player) -> Columns:
        """
        Creates and returns the visual representation of a player's information including their mana, 
        health, armor, attack, and remaining deck cards.

        Args:
            player (Player): The player whose information is to be displayed.

        Returns:
            Columns: A Rich Columns object containing panels for the player's stats.
        """
        mana_panel = Panel(
            Text(f"{player.mana}", style="bold cyan"),
            title="Mana",
            border_style="cyan",
            expand=False
        )

        health_panel = Panel(
            Text(f"{player.health}", style="bold green"),
            title="Health",
            border_style="green",
            expand=False
        )

        armor_panel = Panel(
            Text(f"{player.armor}", style="bold white"),
            title="Armor",
            border_style="white",
            expand=False
        )

        attack_panel = Panel(
            Text(f"{player.attack}", style="bold red"),
            title="Attack",
            border_style="red",
            expand=False
        )

        deck_panel = Panel(
            Text(f"{len(player.deck.cards)} cards", style="bold magenta"),
            title="Deck",
            border_style="magenta",
            expand=False
        )

        return Columns([mana_panel, attack_panel, health_panel, armor_panel, deck_panel])
    
    def print_player_in_hand_card(self, player: Player) -> Panel:
        """
        Creates and returns the visual representation of the player's hand, including the cards they are holding 
        with relevant details like cost, attack, health, and armor.

        Args:
            player (Player): The player whose hand is to be displayed.

        Returns:
            Panel: A Rich Panel object containing all the cards in the player's hand.
        """
        player_cards = []
        for card in player.deck.hand:
            mana_panel = Panel(
                Text(f"{card.cost}", style="bold cyan"),
                title="Mana",
                border_style="cyan",
                expand=False
            )

            health_panel = Panel(
                Text(f"{card.health}", style="bold green"),
                title="Health",
                border_style="green",
                expand=False
            )

            armor_panel = Panel(
                Text(f"{card.armor}", style="bold white"),
                title="Armor",
                border_style="white",
                expand=False
            )

            attack_panel = Panel(
                Text(f"{card.attack}", style="bold red"),
                title="Attack",
                border_style="red",
                expand=False
            )

            inner_panels = Columns([mana_panel, attack_panel, health_panel, armor_panel], expand=False, equal=True)

            card_panel = Panel(
                Align.center(inner_panels),
                title=f"{card.name}",
                border_style="white" if isinstance(card, Unit) else "yellow",
                expand=False,
                width=55
            )

            player_cards.append(card_panel)

        deck_hand_panel = Panel(
            Align.center(Columns(player_cards)),
            title=f"{player.name}'s hand",
            border_style="magenta",
        )
        return deck_hand_panel

    def print_board(self) -> Panel:
        """
        Creates and returns the visual representation of the game board, showing both players' units (cards) in play.

        Returns:
            Panel: A Rich Panel object containing both players' boards.
        """
        player_1_cards = []
        for card in self.player_1.deck.board:
            mana_panel = Panel(
                Text(f"{card.cost}", style="bold cyan"),
                title="Mana",
                border_style="cyan",
                expand=False
            )

            health_panel = Panel(
                Text(f"{card.health}", style="bold green"),
                title="Health",
                border_style="green",
                expand=False
            )

            attack_panel = Panel(
                Text(f"{card.attack}", style="bold red"),
                title="Attack",
                border_style="red",
                expand=False
            )

            inner_panels = Columns([mana_panel, attack_panel, health_panel], expand=False, equal=True)

            card_panel = Panel(
                Align.center(inner_panels),
                title=f"{card.name}",
                border_style="white",
                expand=False,
                width=45
            )

            player_1_cards.append(card_panel)

        player_1_board = Panel(
            Align.center(Columns(player_1_cards)),
            title=f"{self.player_1.name}'s board",
            border_style="white",
        )

        player_2_cards = []
        for card in self.player_2.deck.board:
            mana_panel = Panel(
                Text(f"{card.cost}", style="bold cyan"),
                title="Mana",
                border_style="cyan",
                expand=False
            )

            health_panel = Panel(
                Text(f"{card.health}", style="bold green"),
                title="Health",
                border_style="green",
                expand=False
            )

            attack_panel = Panel(
                Text(f"{card.attack}", style="bold red"),
                title="Attack",
                border_style="red",
                expand=False
            )

            inner_panels = Columns([mana_panel, attack_panel, health_panel], expand=False, equal=True)

            card_panel = Panel(
                Align.center(inner_panels),
                title=f"{card.name}",
                border_style="white",
                expand=False,
                width=45
            )

            player_2_cards.append(card_panel)

        player_2_board = Panel(
            Align.center(Columns(player_2_cards)),
            title=f"{self.player_2.name}'s board",
            border_style="white",
        )

        board_panel = Panel(
            Columns([player_1_board, player_2_board]),
            border_style="white",
        )
        return board_panel
