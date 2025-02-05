#!/usr/bin/python3

# Imports
import unittest

# Modules Imports
from modules.hero_mod import Hero

# Constants Imports
from utils.constants import HERO_STARTING_ATTACK, HERO_STARTING_HEALTH, HERO_STARTING_MANA, HERO_STARTING_ARMOR, HEROES_DB_PATH

# Enum Imports
from enums.card_class_enum import CardClass
from enums.hero_power_enum import HeroPower

# Class
class TestHero(unittest.TestCase):
    """
    Unit tests for the Hero class.
    """

    def setUp(self) -> None:
        """
        Sets up default values for testing.
        """
        self.default_id = 1
        self.default_name = "Jaina Proudmoore"
        self.default_description = "A powerful sorceress and master of the arcane arts."
        self.default_class = CardClass.MAGE
        self.default_power = HeroPower.FIREBLAST
        self.default_attack = HERO_STARTING_ATTACK
        self.default_health = HERO_STARTING_HEALTH
        self.default_mana = HERO_STARTING_MANA
        self.default_armor = HERO_STARTING_ARMOR

    def test_hero_creation_valid(self) -> None:
        """
        Test that a Hero can be successfully created with valid attributes.
        """
        hero = Hero(
            id=self.default_id,
            name=self.default_name,
            description=self.default_description,
            hero_class=self.default_class,
            hero_power=self.default_power,
            attack=self.default_attack,
            health=self.default_health,
            mana=self.default_mana,
            armor=self.default_armor
        )
        self.assertEqual(hero.id, self.default_id)
        self.assertEqual(hero.name, self.default_name)
        self.assertEqual(hero.description, self.default_description)
        self.assertEqual(hero.hero_class, self.default_class)
        self.assertEqual(hero.hero_power, self.default_power)
        self.assertEqual(hero.attack, self.default_attack)
        self.assertEqual(hero.health, self.default_health)
        self.assertEqual(hero.mana, self.default_mana)
        self.assertEqual(hero.armor, self.default_armor)

    def test_hero_creation_invalid_attack(self) -> None:
        """
        Test that a ValueError is raised when attack is negative.
        """
        with self.assertRaises(ValueError):
            Hero(
                id=self.default_id,
                name=self.default_name,
                description=self.default_description,
                hero_class=self.default_class,
                hero_power=self.default_power,
                attack=-1,  # Invalid attack
                health=self.default_health,
                mana=self.default_mana,
                armor=self.default_armor
            )

    def test_hero_creation_invalid_class(self) -> None:
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

    def test_hero_creation_invalid_power(self) -> None:
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

    def test_hero_creation_negative_health(self) -> None:
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

    def test_hero_creation_negative_mana(self) -> None:
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

    def test_hero_creation_invalid_mana_exceeding(self) -> None:
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

    def test_hero_creation_negative_armor(self) -> None:
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

    def test_hero_to_dict(self) -> None:
        """
        Test the to_dict method to ensure it returns the correct dictionary representation.
        """
        hero = Hero(
            id=self.default_id,
            name=self.default_name,
            description=self.default_description,
            hero_class=self.default_class,
            hero_power=self.default_power,
            attack=self.default_attack,
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
            "attack": self.default_attack,
            "health": self.default_health,
            "mana": self.default_mana,
            "armor": self.default_armor,
        }
        self.assertEqual(hero.to_dict(), expected_dict)

if __name__ == "__main__":
    unittest.main()
