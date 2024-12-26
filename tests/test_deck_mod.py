#!/usr/bin/python3

# Imports
import unittest

# Modules Imports
from modules.unit_mod import Unit
from modules.spell_mod import Spell
from modules.deck_mod import Deck

# Constants Imports
from utils.constants import BOARD_LIMIT

# Enum Imports
from enums.card_class_enum import CardClass
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity
from enums.race_enum import Race
from enums.card_status_enum import CardStatus

# Class
class TestDeck(unittest.TestCase):
    """
    Unit tests for the Deck class.
    """

    def setUp(self) -> None:
        """
        Sets up default values for testing.
        """
        self.fireball = Spell(
            id = 1,
            name = "Fireball",
            cost = 4,
            description = "Deal 6 damage.",
            card_classes = [CardClass.MAGE],
            card_type = CardType.SPELL,
            card_rarity = Rarity.COMMON,
        )
        self.yeti = Unit(
            id = 2,
            name = "Chillwind Yeti",
            cost = 4,
            description = "A sturdy minion.",
            card_classes = [CardClass.NEUTRAL],
            card_type = CardType.UNIT,
            card_rarity = Rarity.COMMON,
            unit_race = Race.ALL,
            attack = 4,
            health = 5,
        )
        self.deck = Deck(cards = [self.fireball, self.yeti])

    def test_deck_initialization(self) -> None:
        """
        Test that the deck initializes with correct cards and statuses.
        """
        self.assertEqual(len(self.deck.cards), 2)
        self.assertEqual(len(self.deck.board), 0)
        self.assertEqual(self.fireball.status, CardStatus.IN_DECK)
        self.assertEqual(self.yeti.status, CardStatus.IN_DECK)

    def test_draw_card(self) -> None:
        """
        Test that drawing a card updates its status and removes it from the deck.
        """
        drawn_card = self.deck.draw()
        self.assertEqual(drawn_card.status, CardStatus.IN_HAND)
        self.assertEqual(len(self.deck.cards), 1)
        self.assertNotIn(drawn_card, self.deck.cards)

    def test_play_card(self) -> None:
        """
        Test that playing a card updates its status to ON_BOARD.
        """
        card = self.deck.draw()
        self.deck.play_card(card)
        self.assertEqual(card.status, CardStatus.ON_BOARD)

    def test_move_to_graveyard(self) -> None:
        """
        Test that moving a card to the graveyard updates its status and moves it to the graveyard list.
        """
        card = self.deck.draw()
        self.deck.move_to_graveyard(card)
        self.assertEqual(card.status, CardStatus.IN_GRAVEYARD)
        self.assertIn(card, self.deck.graveyard)
        self.assertNotIn(card, self.deck.board)

    def test_add_card(self) -> None:
        """
        Test that a card can be added to the deck and its status is updated.
        """
        new_card = Spell(
            id = 3,
            name = "Polymorph",
            cost = 4,
            description = "Transform a minion into a 1/1 Sheep.",
            card_classes = [CardClass.MAGE],
            card_type = CardType.SPELL,
            card_rarity = Rarity.COMMON,
        )
        self.deck.add_card(new_card)
        self.assertIn(new_card, self.deck.cards)
        self.assertEqual(new_card.status, CardStatus.IN_DECK)

    def test_remove_card(self) -> None:
        """
        Test that a card can be removed from the deck.
        """
        self.deck.remove_card(self.fireball)
        self.assertNotIn(self.fireball, self.deck.cards)
    
    def test_reset_deck(self) -> None:
        """
        Test that resetting the deck moves all cards from the graveyard back into the deck.
        """
        card = self.deck.draw()
        self.deck.move_to_graveyard(card)
        self.deck.reset_deck()
        self.assertEqual(len(self.deck.cards), 2)
        self.assertEqual(len(self.deck.graveyard), 0)
        for card in self.deck.cards:
            self.assertEqual(card.status, CardStatus.IN_DECK)

    def test_get_cards_by_status(self) -> None:
        """
        Test that getting cards by status returns the correct cards.
        """
        drawn_card = self.deck.draw()
        self.assertEqual(self.deck.get_cards_by_status(CardStatus.IN_HAND), [drawn_card])
        self.assertEqual(self.deck.get_cards_by_status(CardStatus.IN_DECK), [self.yeti])

    def test_play_card_with_full_board(self) -> None:
        """
        Test that playing a card fails if the board already has BOARD_LIMIT cards.
        """
        for _ in range(BOARD_LIMIT):
            card = Spell(
                id = 100 + _,
                name = f"Extra Spell {_}",
                cost = 1,
                description = "Extra card for testing.",
                card_classes = [CardClass.MAGE],
                card_type = CardType.SPELL,
                card_rarity = Rarity.COMMON,
            )
            self.deck.add_card(card)
            drawn_card = self.deck.draw()
            self.deck.play_card(drawn_card)

        card = self.deck.draw()
        with self.assertRaises(ValueError) as context:
            self.deck.play_card(card)
        self.assertEqual(
            str(context.exception),
            f"Cannot play {card.name}. The board is full ({BOARD_LIMIT} cards maximum)."
        )

    def test_deck_limit(self):
        """
        Test that adding a card beyond the deck limit raises an error.
        """
        for _ in range(28):
            self.deck.add_card(Spell(
                id = 100 + _,
                name = f"Extra Spell {_}",
                cost = 1,
                description = "Extra card for testing.",
                card_classes = [CardClass.MAGE],
                card_type = CardType.SPELL,
                card_rarity = Rarity.COMMON,
            ))
        with self.assertRaises(ValueError):
            self.deck.add_card(self.fireball)

if __name__ == "__main__":
    unittest.main()
