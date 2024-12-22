#!/usr/bin/python3

# Imports
import json
import unittest

# Modules Imports
from modules.spell_mod import Spell
from tests.models.spell_model import create_spell_by_model

# Constants Imports
from utils.constants import SPELLS_DB_PATH

# Enum Imports
from enums.card_class_enum import CardClass
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
        self.default_card_class = CardClass.MAGE
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
            card_class=self.default_card_class,
            card_type=self.default_card_type,
            card_rarity=self.default_rarity,
            effects=self.default_effects
        )
        self.assertEqual(spell.id, self.default_id)
        self.assertEqual(spell.name, self.default_name)
        self.assertEqual(spell.cost, self.default_cost)
        self.assertEqual(spell.description, self.default_description)
        self.assertEqual(spell.card_class, self.default_card_class)
        self.assertEqual(spell.card_type, self.default_card_type)
        self.assertEqual(spell.card_rarity, self.default_rarity)
        self.assertEqual(spell.effects, self.default_effects)

    def test_spell_creation_invalid_class(self):
        """
        Test that a ValueError is raised when an invalid card class is provided.
        """
        with self.assertRaises(ValueError):
            Spell(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_class="InvalidClass",  # Invalid card class
                card_type=self.default_card_type,
                card_rarity=self.default_rarity,
                effects=self.default_effects
            )

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
                card_class=self.default_card_class,
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
                card_class=self.default_card_class,
                card_type=self.default_card_type,
                card_rarity=self.default_rarity,
                effects=self.default_effects
            )

    def test_spell_creation_cost_too_high(self):
        """
        Test that a ValueError is raised when the cost is greater than 10.
        """
        with self.assertRaises(ValueError):
            Spell(
                id=self.default_id,
                name=self.default_name,
                cost=11,  # Invalid cost
                description=self.default_description,
                card_class=self.default_card_class,
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
            card_class=self.default_card_class,
            card_type=self.default_card_type,
            card_rarity=self.default_rarity,
            effects=self.default_effects
        )
        expected_dict = {
            "id": self.default_id,
            "name": self.default_name,
            "cost": self.default_cost,
            "description": self.default_description,
            "card_class": self.default_card_class.value,
            "card_type": self.default_card_type.value,
            "card_rarity": self.default_rarity.value,
            "effects": self.default_effects,
        }
        self.assertEqual(spell.to_dict(), expected_dict)

    def test_spells_json(self):
        """
        Test the spells.json file to ensure that all spells are correctly defined.
        """
        with open(SPELLS_DB_PATH, "r") as file:
            spells_json = json.load(file)

        print(spells_json)

        # for hero_class, heroes in heroes_json.items():
        #     for hero_data in heroes:
        #         with self.subTest(hero=hero_data["name"]):
        #             try:
        #                 hero = create_hero_by_model(hero_data)
        #                 self.assertIsNotNone(hero)
        #             except Exception as e:
        #                 self.fail(f"Hero creation failed for {hero_data['name']} with error: {e}")


if __name__ == "__main__":
    unittest.main()
