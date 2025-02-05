#!/usr/bin/python3

# Imports
import unittest

# Modules Imports
from modules.unit_mod import Unit

# Enum Imports
from enums.card_class_enum import CardClass
from enums.rarity_enum import Rarity
from enums.race_enum import Race
from enums.card_status_enum import CardStatus

# Class
class TestUnit(unittest.TestCase):
    """
    Unit tests for the Unit class.
    """

    def setUp(self) -> None:
        """
        Sets up default values for testing.
        """
        self.default_id = 1
        self.default_name = "Chillwind Yeti"
        self.default_cost = 4
        self.default_description = "A sturdy minion with no special abilities."
        self.default_card_classes = [CardClass.NEUTRAL]
        self.default_rarity = Rarity.COMMON
        self.default_race = Race.ALL
        self.default_status = CardStatus.IN_DECK
        self.default_attack = 4
        self.default_health = 5
        self.default_armor = 0

    def test_unit_creation_valid(self) -> None:
        """
        Test that a Unit can be successfully created with valid attributes.
        """
        unit = Unit(
            id = self.default_id,
            name = self.default_name,
            cost = self.default_cost,
            description = self.default_description,
            card_classes = self.default_card_classes,
            card_rarity = self.default_rarity,
            unit_race = self.default_race,
            status = self.default_status,
            attack = self.default_attack,
            health = self.default_health,
            armor = self.default_armor
        )
        self.assertEqual(unit.id, self.default_id)
        self.assertEqual(unit.name, self.default_name)
        self.assertEqual(unit.cost, self.default_cost)
        self.assertEqual(unit.description, self.default_description)
        self.assertEqual(unit.card_classes, self.default_card_classes)
        self.assertEqual(unit.card_rarity, self.default_rarity)
        self.assertEqual(unit.unit_race, self.default_race)
        self.assertEqual(unit.status, self.default_status)
        self.assertEqual(unit.attack, self.default_attack)
        self.assertEqual(unit.health, self.default_health)
        self.assertEqual(unit.armor, self.default_armor)

    def test_unit_creation_invalid_status(self) -> None:
        """
        Test that a ValueError is raised when invalid card classes are provided.
        """
        with self.assertRaises(ValueError):
            Unit(
                id = self.default_id,
                name = self.default_name,
                cost = self.default_cost,
                description = self.default_description,
                card_classes = self.default_card_classes,
                card_rarity = self.default_rarity,
                unit_race = self.default_race,
                status = "InvalidStatus",  # Invalid status
                attack = self.default_attack,
                health = self.default_health,
                armor = self.default_armor
            )

    def test_unit_creation_invalid_classes(self) -> None:
        """
        Test that a ValueError is raised when invalid card classes are provided.
        """
        with self.assertRaises(ValueError):
            Unit(
                id = self.default_id,
                name = self.default_name,
                cost = self.default_cost,
                description = self.default_description,
                card_classes = ["InvalidClass"],  # Invalid card class
                card_rarity = self.default_rarity,
                unit_race = self.default_race,
                status = self.default_status,
                attack = self.default_attack,
                health = self.default_health,
                armor = self.default_armor
            )

    def test_unit_creation_invalid_race(self) -> None:
        """
        Test that a ValueError is raised when an invalid race is provided.
        """
        with self.assertRaises(ValueError):
            Unit(
                id = self.default_id,
                name = self.default_name,
                cost = self.default_cost,
                description = self.default_description,
                card_classes = self.default_card_classes,
                card_rarity = self.default_rarity,
                unit_race = "InvalidRace",  # Invalid race
                status = self.default_status,
                attack = self.default_attack,
                health = self.default_health,
                armor = self.default_armor
            )

    def test_unit_creation_negative_attack(self) -> None:
        """
        Test that a ValueError is raised when attack is negative.
        """
        with self.assertRaises(ValueError):
            Unit(
                id = self.default_id,
                name = self.default_name,
                cost = self.default_cost,
                description = self.default_description,
                card_classes = self.default_card_classes,
                card_rarity = self.default_rarity,
                unit_race = self.default_race,
                status = self.default_status,
                attack = -1,  # Invalid attack
                health = self.default_health,
                armor = self.default_armor
            )

    def test_unit_creation_negative_health(self) -> None:
        """
        Test that a ValueError is raised when health is negative.
        """
        with self.assertRaises(ValueError):
            Unit(
                id = self.default_id,
                name = self.default_name,
                cost = self.default_cost,
                description = self.default_description,
                card_classes = self.default_card_classes,
                card_rarity = self.default_rarity,
                unit_race = self.default_race,
                status = self.default_status,
                attack = self.default_attack,
                health = -1,  # Invalid health
                armor = self.default_armor
            )

    def test_unit_creation_negative_armor(self) -> None:
        """
        Test that a ValueError is raised when armor is negative.
        """
        with self.assertRaises(ValueError):
            Unit(
                id = self.default_id,
                name = self.default_name,
                cost = self.default_cost,
                description = self.default_description,
                card_classes = self.default_card_classes,
                card_rarity = self.default_rarity,
                unit_race = self.default_race,
                status = self.default_status,
                attack = self.default_attack,
                health = self.default_health,
                armor = -5  # Invalid armor
            )

if __name__ == "__main__":
    unittest.main()
