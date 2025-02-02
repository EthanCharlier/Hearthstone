#!/usr/bin/python3

# Imports
import unittest

# Modules Imports
from modules.hero_mod import Hero
from modules.deck_mod import Deck
from modules.unit_mod import Unit
from modules.player_mod import Player

# Constants Imports
from utils.constants import HERO_STARTING_ATTACK, HERO_STARTING_HEALTH, HERO_STARTING_MANA, HERO_STARTING_ARMOR, HEROES_DB_PATH

# Enum Imports
from enums.card_class_enum import CardClass
from enums.hero_power_enum import HeroPower
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity
from enums.race_enum import Race
from enums.card_status_enum import CardStatus
# Class
class TestPlayer(unittest.TestCase):
    """
    Unit tests for the Player class.
    """

    def setUp(self) -> None:
        """
        Set up default values for the tests.
        """
        self.hero = Hero(
            id = 1,
            name = "Jaina Proudmoore",
            description = "A powerful sorceress and master of the arcane arts.",
            hero_class = CardClass.MAGE,
            hero_power = HeroPower.FIREBLAST,
            attack = HERO_STARTING_ATTACK,
            health = HERO_STARTING_HEALTH,
            mana = HERO_STARTING_MANA,
            armor = HERO_STARTING_ARMOR
        )
        self.deck = Deck(cards = [])
        self.player = Player(name = "Player 1", hero = self.hero, deck = self.deck)

    def test_initialization(self) -> None:
        """
        Test that the player initializes correctly.
        """
        self.assertEqual(self.player.name, "Player 1")
        self.assertEqual(self.player.attack, 0)
        self.assertEqual(self.player.health, 30)
        self.assertEqual(self.player.mana, 1)
        self.assertEqual(self.player.armor, 0)

    def test_attack_setter(self) -> None:  #TODO: Add thing
        """
        Test setting the player's attack value.
        """
        self.player.attack = 3
        self.assertEqual(self.player.attack, 3)

    def test_health_setter(self) -> None:  #TODO: Add thing
        """
        Test setting the player's health value.
        """
        self.player.health = 10
        self.assertEqual(self.player.health, 30)
        self.player.health = -20
        self.assertEqual(self.player.health, 10)

    def test_armor_setter(self) -> None:  #TODO: Add thing
        """
        Test setting the player's armor value.
        """
        self.player.armor = 3
        self.assertEqual(self.player.armor, 3)

    def test_mana_setter(self) -> None:  #TODO: Add thing
        """
        Test setting the player's mana value.
        """
        self.player.mana = 5
        self.assertEqual(self.player.mana, 6)

    def test_take_damage(self) -> None:
        """
        Test the player taking damage.
        """
        self.player.take_damage(3)
        self.assertEqual(self.player.armor, 0)
        self.assertEqual(self.player.health, 27)

        self.player.take_damage(5)
        self.assertEqual(self.player.armor, 0)
        self.assertEqual(self.player.health, 22)

    def test_draw_card(self) -> None:
        """
        Test drawing a card from the deck.
        """
        unit_card = Unit(
            id = 1,
            name = "Fireball",
            cost = 4,
            card_classes = [CardClass.MAGE],
            description = "Deal 6 damage.",
            card_type = CardType.UNIT,
            card_rarity = Rarity.COMMON,
            unit_race = Race.ALL,
            status = CardStatus.IN_DECK,
            attack = 4,
            health = 5,
            armor = 0,
            effects = [],
        )
        self.deck.add_card(unit_card)

        drawn_card = self.player.draw_card()
        self.assertEqual(drawn_card, unit_card)

        self.assertEqual(len(self.deck.cards), 0)

    def test_play_card(self) -> None:
        """
        Test playing a card.
        """
        unit_card = Unit(
            id = 1,
            name = "Fireball",
            cost = 4,
            card_classes = [CardClass.MAGE],
            description = "Deal 6 damage.",
            card_type = CardType.UNIT,
            card_rarity = Rarity.COMMON,
            unit_race = Race.ALL,
            status = CardStatus.IN_DECK,
            attack = 4,
            health = 5,
            armor = 0,
            effects = [],
        )
        self.deck.add_card(unit_card)
        self.player.draw_card()

        self.player.mana = 3
        self.assertEqual(self.player.mana, 4)
        self.player.play_card(unit_card)
        self.assertEqual(self.player.mana, 0)
        self.assertNotIn(unit_card, self.deck.hand)

if __name__ == "__main__":
    unittest.main()
