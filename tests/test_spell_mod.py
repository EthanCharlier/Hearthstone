#!/usr/bin/python3

# Imports
import unittest

# Modules Imports
from models.spell_mod import Spell

# Enum Imports
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity

# Class
class TestSpell(unittest.TestCase):
    """
    Unit tests for the Spell class.
    """

    def setUp(self):
        """
        Sets up default values for testing.
        """
        self.default_id = 1
        self.default_name = "Fireball"
        self.default_cost = 4
        self.default_description = "Deal 6 damage."
        self.default_card_type = CardType.SPELL
        self.default_rarity = Rarity.COMMON
        self.default_effects = ["Deal 6 damage"]

    def test_spell_creation_valid(self):
        """
        Test that a Spell can be successfully created with valid attributes.
        """
        spell = Spell(
            id=self.default_id,
            name=self.default_name,
            cost=self.default_cost,
            description=self.default_description,
            card_type=self.default_card_type,
            card_rarity=self.default_rarity,
            effects=self.default_effects
        )
        self.assertEqual(spell.id, self.default_id)
        self.assertEqual(spell.name, self.default_name)
        self.assertEqual(spell.cost, self.default_cost)
        self.assertEqual(spell.description, self.default_description)
        self.assertEqual(spell.card_type, self.default_card_type)
        self.assertEqual(spell.card_rarity, self.default_rarity)
        self.assertEqual(spell.effects, self.default_effects)

    def test_spell_creation_invalid_card_type(self):
        """
        Test that a ValueError is raised when an invalid card type is provided.
        """
        with self.assertRaises(ValueError):
            Spell(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_type=CardType.UNIT,  # Invalid card type
                card_rarity=self.default_rarity,
                effects=self.default_effects
            )

    def test_spell_creation_negative_cost(self):
        """
        Test that a ValueError is raised when the cost is negative.
        """
        with self.assertRaises(ValueError):
            Spell(
                id=self.default_id,
                name=self.default_name,
                cost=-1,  # Invalid cost
                description=self.default_description,
                card_type=self.default_card_type,
                card_rarity=self.default_rarity,
                effects=self.default_effects
            )

    def test_spell_creation_negative_cost_2(self):
        """
        Test that a ValueError is raised when the cost is negative.
        """
        with self.assertRaises(ValueError):
            Spell(
                id=self.default_id,
                name=self.default_name,
                cost=11,  # Invalid cost
                description=self.default_description,
                card_type=self.default_card_type,
                card_rarity=self.default_rarity,
                effects=self.default_effects
            )

    def test_spell_to_dict(self):
        """
        Test the to_dict method to ensure it returns the correct dictionary representation.
        """
        spell = Spell(
            id=self.default_id,
            name=self.default_name,
            cost=self.default_cost,
            description=self.default_description,
            card_type=self.default_card_type,
            card_rarity=self.default_rarity,
            effects=self.default_effects
        )
        expected_dict = {
            "id": self.default_id,
            "name": self.default_name,
            "cost": self.default_cost,
            "description": self.default_description,
            "card_type": self.default_card_type.value,
            "card_rarity": self.default_rarity.value,
            "effects": self.default_effects,
        }
        self.assertEqual(spell.to_dict(), expected_dict)


if __name__ == "__main__":
    unittest.main()
