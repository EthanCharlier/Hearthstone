#!/usr/bin/python3

# Imports
import unittest

# Modules Imports
from modules.spell_mod import Spell

# Constants Imports
from utils.constants import SPELLS_DB_PATH

# Enum Imports
from enums.card_class_enum import CardClass
from enums.rarity_enum import Rarity
from enums.card_status_enum import CardStatus

# Class
class TestSpell(unittest.TestCase):
    """
    Unit tests for the Spell class.
    """

    def setUp(self) -> None:
        """
        Sets up default values for testing.
        """
        self.default_id = 1
        self.default_name = "Fireball"
        self.default_cost = 4
        self.default_description = "Deal 6 damage."
        self.default_card_classes = [CardClass.MAGE]
        self.default_rarity = Rarity.COMMON
        self.default_status = CardStatus.IN_DECK
        self.default_attack = 5
        self.default_health = 5
        self.default_armor = 5

    def test_spell_creation_valid(self) -> None:
        """
        Test that a Spell can be successfully created with valid attributes.
        """
        spell = Spell(
            id = self.default_id,
            name = self.default_name,
            cost = self.default_cost,
            description = self.default_description,
            card_classes = self.default_card_classes,
            card_rarity = self.default_rarity,
            status = self.default_status,
            armor = self.default_armor,
            health = self.default_health,
            attack = self.default_attack
        )
        self.assertEqual(spell.id, self.default_id)
        self.assertEqual(spell.name, self.default_name)
        self.assertEqual(spell.cost, self.default_cost)
        self.assertEqual(spell.description, self.default_description)
        self.assertEqual(spell.card_classes, self.default_card_classes)
        self.assertEqual(spell.card_rarity, self.default_rarity)
        self.assertEqual(spell.status, self.default_status)
        self.assertEqual(spell.armor, self.default_armor)
        self.assertEqual(spell.health, self.default_health)
        self.assertEqual(spell.attack, self.default_attack)

    def test_card_creation_invalid_status(self) -> None:
        """
        Test that a ValueError is raised when any invalid card status is provided.
        """
        with self.assertRaises(ValueError):
            Spell(
                id = self.default_id,
                name = self.default_name,
                cost = self.default_cost,
                description = self.default_description,
                card_classes = self.default_card_classes,
                card_rarity = self.default_rarity,
                status = "InvalidStatus",  # Invalid status
                armor = self.default_armor,
                health = self.default_health,
                attack = self.default_attack
            )

    def test_spell_creation_invalid_classes(self) -> None:
        """
        Test that a ValueError is raised when any invalid card class is provided.
        """
        with self.assertRaises(ValueError):
            Spell(
                id = self.default_id,
                name = self.default_name,
                cost = self.default_cost,
                description = self.default_description,
                card_classes = ["InvalidClass"],  # Invalid card class
                card_rarity = self.default_rarity,
                status = self.default_status,
                armor = self.default_armor,
                health = self.default_health,
                attack = self.default_attack
            )

    def test_spell_creation_negative_cost(self) -> None:
        """
        Test that a ValueError is raised when the cost is negative.
        """
        with self.assertRaises(ValueError):
            Spell(
                id = self.default_id,
                name = self.default_name,
                cost = -1,  # Invalid cost
                description = self.default_description,
                card_classes = self.default_card_classes,
                card_rarity = self.default_rarity,
                status = self.default_status,
                armor = self.default_armor,
                health = self.default_health,
                attack = self.default_attack
            )

if __name__ == "__main__":
    unittest.main()
