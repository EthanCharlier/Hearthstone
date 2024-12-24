#!/usr/bin/python3

# Imports
import unittest

# Modules Imports
from modules.card_mod import Card

# Enum Imports
from enums.card_class_enum import CardClass
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity

# Class
class TestCard(unittest.TestCase):
    """
    Unit tests for the Card class.
    """

    def setUp(self) -> None:
        """
        Sets up default values for testing.
        """
        self.default_id = 1
        self.default_name = "Fireball"
        self.default_cost = 4
        self.default_card_classes = [CardClass.MAGE]
        self.default_description = "Deal 6 damage."
        self.default_card_type = CardType.SPELL
        self.default_rarity = Rarity.COMMON

    def test_card_creation_valid(self) -> None:
        """
        Test that a Card can be successfully created with valid attributes.
        """
        card = Card(
            id=self.default_id,
            name=self.default_name,
            cost=self.default_cost,
            description=self.default_description,
            card_classes=self.default_card_classes,
            card_type=self.default_card_type,
            card_rarity=self.default_rarity
        )
        self.assertEqual(card.id, self.default_id)
        self.assertEqual(card.name, self.default_name)
        self.assertEqual(card.cost, self.default_cost)
        self.assertEqual(card.description, self.default_description)
        self.assertEqual(card.card_classes, self.default_card_classes)
        self.assertEqual(card.card_type, self.default_card_type)
        self.assertEqual(card.card_rarity, self.default_rarity)

    def test_card_creation_invalid_classes(self) -> None:
        """
        Test that a ValueError is raised when any invalid card class is provided.
        """
        with self.assertRaises(ValueError):
            Card(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_classes=["InvalidClass"],  # Invalid class
                card_type=self.default_card_type,
                card_rarity=self.default_rarity
            )

    def test_card_creation_invalid_type(self) -> None:
        """
        Test that a ValueError is raised when an invalid card type is provided.
        """
        with self.assertRaises(ValueError):
            Card(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_classes=self.default_card_classes,
                card_type="InvalidType",  # Invalid type
                card_rarity=self.default_rarity
            )

    def test_card_creation_invalid_rarity(self) -> None:
        """
        Test that a ValueError is raised when an invalid card rarity is provided.
        """
        with self.assertRaises(ValueError):
            Card(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_classes=self.default_card_classes,
                card_type=self.default_card_type,
                card_rarity="InvalidRarity"  # Invalid rarity
            )

    def test_card_creation_negative_cost(self) -> None:
        """
        Test that a ValueError is raised when the cost is negative.
        """
        with self.assertRaises(ValueError):
            Card(
                id=self.default_id,
                name=self.default_name,
                cost=-1,  # Invalid cost
                description=self.default_description,
                card_classes=self.default_card_classes,
                card_type=self.default_card_type,
                card_rarity=self.default_rarity
            )

    def test_card_creation_cost_too_high(self) -> None:
        """
        Test that a ValueError is raised when the cost is greater than 10.
        """
        with self.assertRaises(ValueError):
            Card(
                id=self.default_id,
                name=self.default_name,
                cost=11,  # Invalid cost
                description=self.default_description,
                card_classes=self.default_card_classes,
                card_type=self.default_card_type,
                card_rarity=self.default_rarity
            )

    def test_card_to_dict(self) -> None:
        """
        Test the to_dict method to ensure it returns the correct dictionary representation.
        """
        card = Card(
            id=self.default_id,
            name=self.default_name,
            cost=self.default_cost,
            description=self.default_description,
            card_classes=self.default_card_classes,
            card_type=self.default_card_type,
            card_rarity=self.default_rarity
        )
        expected_dict = {
            "id": self.default_id,
            "name": self.default_name,
            "cost": self.default_cost,
            "description": self.default_description,
            "card_classes": [cls.value for cls in self.default_card_classes],
            "card_type": self.default_card_type.value,
            "card_rarity": self.default_rarity.value,
        }
        self.assertEqual(card.to_dict(), expected_dict)

if __name__ == "__main__":
    unittest.main()
