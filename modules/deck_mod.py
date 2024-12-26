#!/usr/bin/python3

# Imports
import random

# Modules Imports
from modules.card_mod import Card

# Constants Imports
from utils.constants import HAND_LIMIT, BOARD_LIMIT

# Enum Imports
from enums.card_status_enum import CardStatus

# Class
class Deck:
    """
    Represents a deck of cards in the game.

    Attributes:
        cards (list[Card]): The list of cards in the deck.
        hand (list[Card]): Cards currently in the player's hand.
        board (list[Card]): Cards currently on the board.
        graveyard (list[Card]): Cards that have been played or destroyed.
    """

    def __init__(self, cards: list[Card], hand: list[Card] = None, board: list[Card] = None, graveyard: list[Card] = None) -> None:
        """
        Initialize the Deck.

        Args:
            cards (list[Card]): A list of cards to initialize the deck.
            hand (list[Card]): Cards currently in the player's hand.
            board (list[Card]): Cards currently on the board.
            graveyard (list[Card]): Cards that have been played or destroyed.

        Raises:
            ValueError: If the deck contains more than 30 cards.
        """
        if len(cards) > 30:
            raise ValueError("A deck cannot contain more than 30 cards.")
        self.cards = cards
        self.hand = hand or []
        self.board = board or []
        self.graveyard = graveyard or []

        for card in self.cards:
            card.status = CardStatus.IN_DECK

        for card in self.graveyard:
            card.status = CardStatus.IN_GRAVEYARD

    def shuffle(self) -> None:
        """
        Shuffle the deck randomly.
        """
        random.shuffle(self.cards)

    def draw(self) -> Card:
        """
        Draw the top card from the deck.

        Returns:
            Card: The top card of the deck.

        Raises:
            ValueError: If the deck is empty or hand limit is reached.
        """
        if not self.cards:
            raise ValueError("Cannot draw from an empty deck.")
        if len(self.hand) >= HAND_LIMIT:
            raise ValueError(f"Hand limit reached.")
        card = self.cards.pop(0)
        card.status = CardStatus.IN_HAND
        self.hand.append(card)
        return card

    def play_card(self, card: Card) -> None:
        """
        Play a card from the player's hand, moving it to the board.

        Args:
            card (Card): The card to play.

        Raises:
            ValueError: If the card is not in the player's hand or if the board is full.
        """
        if len(self.board) >= BOARD_LIMIT:
            raise ValueError(f"Cannot play {card.name}. The board is full ({BOARD_LIMIT} cards maximum).")
        if card.status != CardStatus.IN_HAND:
            raise ValueError("The card must be in hand to be played.")
        card.status = CardStatus.ON_BOARD
        self.hand.remove(card)
        self.board.append(card)

    def move_to_graveyard(self, card: Card) -> None:
        """
        Move a card to the graveyard.

        Args:
            card (Card): The card to move to the graveyard.

        Raises:
            ValueError: If the card is not on the board or in the hand.
        """
        if card.status not in [CardStatus.ON_BOARD, CardStatus.IN_HAND]:
            raise ValueError("The card must be on the board or in hand to move to the graveyard.")
        card.status = CardStatus.IN_GRAVEYARD
        if card in self.hand:
            self.hand.remove(card)
        elif card in self.board:
            self.board.remove(card)
        self.graveyard.append(card)

    def add_card(self, card: Card) -> None:
        """
        Add a card to the deck (at the bottom).

        Args:
            card (Card): The card to add.

        Raises:
            ValueError: If adding the card would exceed the deck limit.
        """
        if len(self.cards) >= 30:
            raise ValueError("Cannot add more cards to the deck; maximum is 30.")
        card.status = CardStatus.IN_DECK
        self.cards.append(card)

    def remove_card(self, card: Card) -> None:
        """
        Remove a card from the deck.

        Args:
            card (Card): The card to remove.

        Raises:
            ValueError: If the card is not in the deck.
        """
        if card not in self.cards:
            raise ValueError("The card is not in the deck.")
        self.cards.remove(card)

    def get_cards_by_status(self, status: CardStatus) -> list[Card]:
        """
        Get all cards with a specific status.

        Args:
            status (CardStatus): The status to filter cards by.

        Returns:
            list[Card]: A list of cards matching the given status.
        """
        if status == CardStatus.IN_HAND:
            return self.hand
        if status == CardStatus.ON_BOARD:
            return self.board
        return [card for card in self.cards + self.graveyard if card.status == status]
    
    def reset_deck(self) -> None:
        """
        Reset the deck by returning all cards from the graveyard to the deck.
        """
        self.cards.extend(self.graveyard)
        self.cards.extend(self.board)
        for card in self.cards:
            card.status = CardStatus.IN_DECK
        self.graveyard.clear()
        self.board.clear()
