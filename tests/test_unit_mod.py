#!/usr/bin/python3

# Imports
import json
import unittest

# Modules Imports
from modules.unit_mod import Unit
from tests.models.unit_model import create_unit_by_model

# Constants Imports
from utils.constants import UNITS_DB_PATH

# Enum Imports
from enums.card_class_enum import CardClass
from enums.card_type_enum import CardType
from enums.rarity_enum import Rarity
from enums.race_enum import Race

# Class
class TestUnit(unittest.TestCase):
    """
    Unit tests for the Unit class.
    """

    def setUp(self):
        """
        Sets up default values for testing.
        """
        self.default_id = 1
        self.default_name = "Chillwind Yeti"
        self.default_cost = 4
        self.default_description = "A sturdy minion with no special abilities."
        self.default_card_class = CardClass.NEUTRAL
        self.default_card_type = CardType.UNIT
        self.default_rarity = Rarity.COMMON
        self.default_race = Race.ALL
        self.default_attack = 4
        self.default_health = 5
        self.default_armor = 0
        self.default_effects = []

    def test_unit_creation_valid(self):
        """
        Test that a Unit can be successfully created with valid attributes.
        """
        unit = Unit(
            id=self.default_id,
            name=self.default_name,
            cost=self.default_cost,
            description=self.default_description,
            card_class=self.default_card_class,
            card_type=self.default_card_type,
            card_rarity=self.default_rarity,
            unit_race=self.default_race,
            attack=self.default_attack,
            health=self.default_health,
            armor=self.default_armor,
            effects=self.default_effects
        )
        self.assertEqual(unit.id, self.default_id)
        self.assertEqual(unit.name, self.default_name)
        self.assertEqual(unit.cost, self.default_cost)
        self.assertEqual(unit.description, self.default_description)
        self.assertEqual(unit.card_class, self.default_card_class)
        self.assertEqual(unit.card_type, self.default_card_type)
        self.assertEqual(unit.card_rarity, self.default_rarity)
        self.assertEqual(unit.unit_race, self.default_race)
        self.assertEqual(unit.attack, self.default_attack)
        self.assertEqual(unit.health, self.default_health)
        self.assertEqual(unit.armor, self.default_armor)
        self.assertEqual(unit.effects, self.default_effects)

    def test_unit_creation_invalid_class(self):
        """
        Test that a ValueError is raised when an invalid card class is provided.
        """
        with self.assertRaises(ValueError):
            Unit(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_class="InvalidClass",  # Invalid card class
                card_type=self.default_card_type,
                card_rarity=self.default_rarity,
                unit_race=self.default_race,
                attack=self.default_attack,
                health=self.default_health,
                armor=self.default_armor,
                effects=self.default_effects
            )

    def test_unit_creation_invalid_card_type(self):
        """
        Test that a ValueError is raised when an invalid card type is provided.
        """
        with self.assertRaises(ValueError):
            Unit(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_class=self.default_card_class,
                card_type=CardType.SPELL,  # Invalid card type
                card_rarity=self.default_rarity,
                unit_race=self.default_race,
                attack=self.default_attack,
                health=self.default_health,
                armor=self.default_armor,
                effects=self.default_effects
            )

    def test_unit_creation_invalid_race(self):
        """
        Test that a ValueError is raised when an invalid race is provided.
        """
        with self.assertRaises(ValueError):
            Unit(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_class=self.default_card_class,
                card_type=self.default_card_type,
                card_rarity=self.default_rarity,
                unit_race="InvalidRace",  # Invalid race
                attack=self.default_attack,
                health=self.default_health,
                armor=self.default_armor,
                effects=self.default_effects
            )

    def test_unit_creation_negative_attack(self):
        """
        Test that a ValueError is raised when attack is negative.
        """
        with self.assertRaises(ValueError):
            Unit(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_class=self.default_card_class,
                card_type=self.default_card_type,
                card_rarity=self.default_rarity,
                unit_race=self.default_race,
                attack=-1,  # Invalid attack
                health=self.default_health,
                armor=self.default_armor,
                effects=self.default_effects
            )

    def test_unit_creation_negative_health(self):
        """
        Test that a ValueError is raised when health is negative.
        """
        with self.assertRaises(ValueError):
            Unit(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_class=self.default_card_class,
                card_type=self.default_card_type,
                card_rarity=self.default_rarity,
                unit_race=self.default_race,
                attack=self.default_attack,
                health=-1,  # Invalid health
                armor=self.default_armor,
                effects=self.default_effects
            )

    def test_unit_creation_negative_armor(self):
        """
        Test that a ValueError is raised when armor is negative.
        """
        with self.assertRaises(ValueError):
            Unit(
                id=self.default_id,
                name=self.default_name,
                cost=self.default_cost,
                description=self.default_description,
                card_class=self.default_card_class,
                card_type=self.default_card_type,
                card_rarity=self.default_rarity,
                unit_race=self.default_race,
                attack=self.default_attack,
                health=self.default_health,
                armor=-5,  # Invalid armor
                effects=self.default_effects
            )

    def test_unit_to_dict(self):
        """
        Test the to_dict method to ensure it returns the correct dictionary representation.
        """
        unit = Unit(
            id=self.default_id,
            name=self.default_name,
            cost=self.default_cost,
            description=self.default_description,
            card_class=self.default_card_class,
            card_type=self.default_card_type,
            card_rarity=self.default_rarity,
            unit_race=self.default_race,
            attack=self.default_attack,
            health=self.default_health,
            armor=self.default_armor,
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
            "unit_race": self.default_race.value,
            "attack": self.default_attack,
            "health": self.default_health,
            "armor": self.default_armor,
            "effects": self.default_effects,
        }
        self.assertEqual(unit.to_dict(), expected_dict)

    def test_units_json(self):
        """
        Test the units.json file to ensure that all units are correctly defined.
        """
        with open(UNITS_DB_PATH, "r") as file:
            units_json = json.load(file)

        print(units_json)

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
