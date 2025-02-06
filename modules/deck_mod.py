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
    Represents a deck of cards in a card game, managing cards in the deck, hand, board, and graveyard.

    Attributes:
        cards (list[Card]): The list of cards in the deck.
        hand (list[Card]): The cards currently in the player's hand.
        board (list[Card]): The cards currently on the board.
        graveyard (list[Card]): The cards that have been played or destroyed.

    Methods:
        __init__: Initializes the deck with a given list of cards, and optional lists for hand, board, and graveyard.
        shuffle: Shuffles the deck randomly.
        draw: Draws the top card from the deck and adds it to the hand.
        play_card: Plays a card from the hand to the board.
        move_to_graveyard: Moves a card from the hand or board to the graveyard.
        add_card: Adds a card to the deck (bottom of the deck).
        remove_card: Removes a card from the deck.
        get_cards_by_status: Retrieves all cards with a specific status (e.g., in hand, on board, etc.).
        reset_deck: Resets the deck by moving all cards from the graveyard and board back into the deck.
    """

    def __init__(self, cards: list[Card], hand: list[Card] = None, board: list[Card] = None, graveyard: list[Card] = None) -> None:
        """
        Initializes the deck with the provided list of cards and optional hand, board, and graveyard.

        Args:
            cards (list[Card]): A list of cards to initialize the deck.
            hand (list[Card]): Cards currently in the player's hand (default is an empty list).
            board (list[Card]): Cards currently on the board (default is an empty list).
            graveyard (list[Card]): Cards that have been played or destroyed (default is an empty list).

        Raises:
            ValueError: If the deck contains more than 30 cards.
        """
        if len(cards) > 30:  # Check if the deck has more than 30 cards
            raise ValueError("A deck cannot contain more than 30 cards.")  # Raise an error if deck exceeds 30 cards
        self.cards = cards  # Assign the provided cards list to the deck
        self.hand = hand or []  # If no hand is provided, initialize as an empty list
        self.board = board or []  # If no board is provided, initialize as an empty list
        self.graveyard = graveyard or []  # If no graveyard is provided, initialize as an empty list

        # Initialize the status of cards in the deck
        for card in self.cards:  # Iterate through the cards in the deck
            card.status = CardStatus.IN_DECK  # Set the status of each card to IN_DECK

        # Initialize the status of cards in the graveyard
        for card in self.graveyard:  # Iterate through the cards in the graveyard
            card.status = CardStatus.IN_GRAVEYARD  # Set the status of each card to IN_GRAVEYARD

    def shuffle(self) -> None:
        """
        Shuffles the cards in the deck randomly.
        """
        random.shuffle(self.cards)  # Shuffle the cards in the deck using the random shuffle function

    def draw(self) -> Card:
        """
        Draws the top card from the deck and adds it to the player's hand.

        Returns:
            Card: The card drawn from the deck.

        Raises:
            ValueError: If the deck is empty or if the player has reached the hand limit.
        """
        if not self.cards:  # Check if the deck is empty
            raise ValueError("Cannot draw from an empty deck.")  # Raise an error if deck is empty
        if len(self.hand) >= HAND_LIMIT:  # Check if the player has reached the hand limit
            raise ValueError(f"Hand limit reached.")  # Raise an error if hand limit is reached
        card = self.cards.pop(0)  # Draw the top card from the deck
        card.status = CardStatus.IN_HAND  # Change the card's status to IN_HAND
        self.hand.append(card)  # Add the card to the player's hand
        return card  # Return the drawn card

    def play_card(self, card: Card) -> None:
        """
        Plays a card from the player's hand and moves it to the board.

        Args:
            card (Card): The card to be played from the hand to the board.

        Raises:
            ValueError: If the card is not in the player's hand or if the board is full.
        """
        if len(self.board) >= BOARD_LIMIT:  # Check if the board has reached the maximum number of cards
            raise ValueError(f"Cannot play {card.name}. The board is full ({BOARD_LIMIT} cards maximum).")  # Raise an error if board is full
        if card.status != CardStatus.IN_HAND:  # Check if the card is in the hand
            raise ValueError("The card must be in hand to be played.")  # Raise an error if the card is not in hand
        card.status = CardStatus.ON_BOARD  # Change the card's status to ON_BOARD
        self.hand.remove(card)  # Remove the card from the hand
        self.board.append(card)  # Add the card to the board

    def move_to_graveyard(self, card: Card) -> None:
        """
        Moves a card from the hand or board to the graveyard.

        Args:
            card (Card): The card to move to the graveyard.

        Raises:
            ValueError: If the card is not in the hand or on the board.
        """
        if card.status not in [CardStatus.ON_BOARD, CardStatus.IN_HAND]:  # Check if the card is on the board or in hand
            raise ValueError("The card must be on the board or in hand to move to the graveyard.")  # Raise an error if card is not in the valid states
        card.status = CardStatus.IN_GRAVEYARD  # Change the card's status to IN_GRAVEYARD
        if card in self.hand:  # If the card is in the hand
            self.hand.remove(card)  # Remove it from the hand
        elif card in self.board:  # If the card is on the board
            self.board.remove(card)  # Remove it from the board
        self.graveyard.append(card)  # Add the card to the graveyard

    def add_card(self, card: Card) -> None:
        """
        Adds a card to the deck (at the bottom).

        Args:
            card (Card): The card to add to the deck.

        Raises:
            ValueError: If adding the card would exceed the deck limit of 30 cards.
        """
        if len(self.cards) >= 30:  # Check if adding a card would exceed the deck limit
            raise ValueError("Cannot add more cards to the deck; maximum is 30.")  # Raise an error if deck exceeds limit
        card.status = CardStatus.IN_DECK  # Change the card's status to IN_DECK
        self.cards.append(card)  # Add the card to the bottom of the deck

    def remove_card(self, card: Card) -> None:
        """
        Removes a card from the deck.

        Args:
            card (Card): The card to remove from the deck.

        Raises:
            ValueError: If the card is not found in the deck.
        """
        if card not in self.cards:  # Check if the card is in the deck
            raise ValueError("The card is not in the deck.")  # Raise an error if card is not found in the deck
        self.cards.remove(card)  # Remove the card from the deck

    def get_cards_by_status(self, status: CardStatus) -> list[Card]:
        """
        Retrieves all cards that have a specific status (e.g., in hand, on board, etc.).

        Args:
            status (CardStatus): The status to filter cards by.

        Returns:
            list[Card]: A list of cards matching the specified status.
        """
        if status == CardStatus.IN_HAND:  # Check if the status is IN_HAND
            return self.hand  # Return the list of cards in hand
        if status == CardStatus.ON_BOARD:  # Check if the status is ON_BOARD
            return self.board  # Return the list of cards on the board
        return [card for card in self.cards + self.graveyard if card.status == status]  # Return all cards with the matching status from deck and graveyard
    
    def reset_deck(self) -> None:
        """
        Resets the deck by moving all cards from the graveyard and board back to the deck.

        This method will return all cards from the graveyard and board to the deck 
        and reset their status to "IN_DECK". It clears the graveyard and the board.
        """
        self.cards.extend(self.graveyard)  # Add all graveyard cards back to the deck
        self.cards.extend(self.board)  # Add all board cards back to the deck
        for card in self.cards:  # Iterate through all cards in the deck
            card.status = CardStatus.IN_DECK  # Reset their status to IN_DECK
        self.graveyard.clear()  # Clear the graveyard
        self.board.clear()  # Clear the board
