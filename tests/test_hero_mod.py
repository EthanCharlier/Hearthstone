#!/usr/bin/python3

# Imports
import json
import unittest
from tests.models.hero_model import create_hero_by_model

# Modules Imports
from modules.hero_mod import Hero

# Constants Imports
from utils.constants import HERO_STARTING_HEALTH, HERO_STARTING_MANA, HERO_STARTING_ARMOR, HEROES_DB_PATH

# Enum Imports
from enums.card_class_enum import CardClass
from enums.hero_power_enum import HeroPower

# Class
class TestHero(unittest.TestCase):
    """
    Unit tests for the Hero class.
    """

    def setUp(self):
        """
        Sets up default values for testing.
        """
        self.default_id = 1
        self.default_name = "Jaina Proudmoore"
        self.default_description = "A powerful sorceress and master of the arcane arts."
        self.default_class = CardClass.MAGE
        self.default_power = HeroPower.FIREBLAST
        self.default_health = HERO_STARTING_HEALTH
        self.default_mana = HERO_STARTING_MANA
        self.default_armor = HERO_STARTING_ARMOR

    def test_hero_creation_valid(self):
        """
        Test that a Hero can be successfully created with valid attributes.
        """
        hero = Hero(
            id=self.default_id,
            name=self.default_name,
            description=self.default_description,
            hero_class=self.default_class,
            hero_power=self.default_power,
            health=self.default_health,
            mana=self.default_mana,
            armor=self.default_armor
        )
        self.assertEqual(hero.id, self.default_id)
        self.assertEqual(hero.name, self.default_name)
        self.assertEqual(hero.description, self.default_description)
        self.assertEqual(hero.hero_class, self.default_class)
        self.assertEqual(hero.hero_power, self.default_power)
        self.assertEqual(hero.health, self.default_health)
        self.assertEqual(hero.mana, self.default_mana)
        self.assertEqual(hero.armor, self.default_armor)

    def test_hero_creation_invalid_class(self):
        """
        Test that a ValueError is raised when an invalid hero class is provided.
        """
        with self.assertRaises(ValueError):
            Hero(
                id=self.default_id,
                name=self.default_name,
                description=self.default_description,
                hero_class="InvalidClass",  # Invalid class
                hero_power=self.default_power,
                health=self.default_health,
                mana=self.default_mana,
                armor=self.default_armor
            )

    def test_hero_creation_invalid_power(self):
        """
        Test that a ValueError is raised when the hero power does not match the hero class.
        """
        with self.assertRaises(ValueError):
            Hero(
                id=self.default_id,
                name=self.default_name,
                description=self.default_description,
                hero_class=CardClass.MAGE,
                hero_power=HeroPower.ARMOR_UP,  # Invalid power for Mage
                health=self.default_health,
                mana=self.default_mana,
                armor=self.default_armor
            )

    def test_hero_creation_negative_health(self):
        """
        Test that a ValueError is raised when health is negative.
        """
        with self.assertRaises(ValueError):
            Hero(
                id=self.default_id,
                name=self.default_name,
                description=self.default_description,
                hero_class=self.default_class,
                hero_power=self.default_power,
                health=-1,  # Invalid health
                mana=self.default_mana,
                armor=self.default_armor
            )

    def test_hero_creation_negative_mana(self):
        """
        Test that a ValueError is raised when mana is negative.
        """
        with self.assertRaises(ValueError):
            Hero(
                id=self.default_id,
                name=self.default_name,
                description=self.default_description,
                hero_class=self.default_class,
                hero_power=self.default_power,
                health=self.default_health,
                mana=-1,  # Invalid mana
                armor=self.default_armor
            )

    def test_hero_creation_negative_mana_2(self):
        """
        Test that a ValueError is raised when mana is negative.
        """
        with self.assertRaises(ValueError):
            Hero(
                id=self.default_id,
                name=self.default_name,
                description=self.default_description,
                hero_class=self.default_class,
                hero_power=self.default_power,
                health=self.default_health,
                mana=11,  # Invalid mana
                armor=self.default_armor
            )

    def test_hero_creation_negative_armor(self):
        """
        Test that a ValueError is raised when armor is negative.
        """
        with self.assertRaises(ValueError):
            Hero(
                id=self.default_id,
                name=self.default_name,
                description=self.default_description,
                hero_class=self.default_class,
                hero_power=self.default_power,
                health=self.default_health,
                mana=self.default_mana,
                armor=-1  # Invalid armor
            )

    def test_hero_to_dict(self):
        """
        Test the to_dict method to ensure it returns the correct dictionary representation.
        """
        hero = Hero(
            id=self.default_id,
            name=self.default_name,
            description=self.default_description,
            hero_class=self.default_class,
            hero_power=self.default_power,
            health=self.default_health,
            mana=self.default_mana,
            armor=self.default_armor
        )
        expected_dict = {
            "id": self.default_id,
            "name": self.default_name,
            "description": self.default_description,
            "hero_class": self.default_class.value,
            "hero_power": self.default_power.value,
            "health": self.default_health,
            "mana": self.default_mana,
            "armor": self.default_armor,
        }
        self.assertEqual(hero.to_dict(), expected_dict)

    def test_heroes_json(self):
        """
        Test the heroes.json file to ensure that all heroes a correctly define.
        """
        with open(HEROES_DB_PATH, "r") as file:
            heroes_json = json.load(file)

        for hero_class, heroes in heroes_json.items():
            for hero_data in heroes:
                with self.subTest(hero=hero_data["name"]):
                    try:
                        hero = create_hero_by_model(hero_data)
                        self.assertIsNotNone(hero)
                    except Exception as e:
                        self.fail(f"Hero creation failed for {hero_data['name']} with error: {e}")

if __name__ == "__main__":
    unittest.main()
