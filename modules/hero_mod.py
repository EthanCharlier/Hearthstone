#!/usr/bin/python3

# Imports

# Modules Imports
from utils.database_utils import Database
from enums.hero_power_enum import HeroPower, HERO_CLASS_TO_POWER

# Constants Imports
from utils.constants import DATABASE_PATH, HERO_STARTING_ATTACK, HERO_STARTING_HEALTH, HERO_STARTING_MANA, HERO_STARTING_ARMOR

# Enum Imports
from enums.card_class_enum import CardClass

# Class
class Hero():
    """
    Represents a hero in a card game. Each hero belongs to a specific class, 
    has a unique power, and starts with predefined values for health, mana, and armor.

    Attributes:
        id (int): Unique identifier for the hero.
        name (str): Name of the hero.
        description (str): A brief description or lore about the hero.
        hero_class (CardClass): The class of the hero (e.g., Mage, Warrior).
        hero_power (HeroPower): The power associated with the hero class.
        attack (int): The attack value of the unit (default: 0, cannot be negative).
        health (int): The starting health of the hero (default: `HERO_STARTING_HEALTH`, cannot be negative).
        mana (int): The starting mana of the hero (default: `HERO_STARTING_MANA`, cannot be negative, 10 is the maximum).
        armor (int): The starting armor of the hero (default: `HERO_STARTING_ARMOR`, cannot be negative).

    Raises:
        ValueError: If `hero_class` is not an instance of `CardClass`.
        ValueError: If `hero_power` is not an instance of `HeroPower`.
        ValueError: If the provided `hero_power` does not match the expected power 
                    for the given `hero_class` as defined in `HERO_CLASS_TO_POWER`.
        ValueError: If `attack`, `health`, `mana`, or `armor` is negative.
        ValueError: If `mana` is greater than 10.
    """

    def __init__(self, 
                id: int, 
                name: str, 
                description: str, 
                hero_class: CardClass, 
                hero_power: HeroPower, 
                attack: int = HERO_STARTING_ATTACK, 
                health: int = HERO_STARTING_HEALTH, 
                mana: int = HERO_STARTING_MANA, 
                armor: int = HERO_STARTING_ARMOR
                ) -> None:
        """
        Initializes a Hero object with its attributes.

        Args:
            id (int): A unique identifier for the hero.
            name (str): The name of the hero.
            description (str): A description or lore text for the hero.
            hero_class (CardClass): The class of the hero, which must be a valid `CardClass` enum.
            hero_power (HeroPower): The power associated with the hero class, which must be a valid `HeroPower` enum.
            attack (int): The attack value of the unit (default: 0, cannot be negative).
            health (int): The starting health of the hero (default: `HERO_STARTING_HEALTH`, cannot be negative).
            mana (int): The starting mana of the hero (default: `HERO_STARTING_MANA`, cannot be negative, 10 is the maximum).
            armor (int): The starting armor of the hero (default: `HERO_STARTING_ARMOR`, cannot be negative).

        Raises:
            ValueError: If `hero_class` is not a valid `CardClass` enum.
            ValueError: If `hero_power` is not a valid `HeroPower` enum.
            ValueError: If the provided `hero_power` does not match the expected 
                        power for the given `hero_class` as defined in `HERO_CLASS_TO_POWER`.
            ValueError: If `attack`, `health`, `mana`, or `armor` is negative.
            ValueError: If `mana` is greater than 10.
        """
        self.id = id
        self.name = name
        self.description = description

        if not isinstance(hero_class, CardClass):
            raise ValueError(f"Invalid hero class: {hero_class}. Must be a CardClass enum.")
        self.hero_class = hero_class

        if not isinstance(hero_power, HeroPower):
            raise ValueError(f"Invalid hero power: {hero_power}. Must be a HeroPower enum.")
        if HERO_CLASS_TO_POWER.get(hero_class) != hero_power:
            raise ValueError(
                f"Invalid hero power: {hero_power} for class {hero_class}. "
                f"Expected power: {HERO_CLASS_TO_POWER[hero_class]}."
            )
        self.hero_power = hero_power

        if attack < 0:
            raise ValueError(f"Invalid attack: {attack}. Attack cannot be negative.")
        if health < 0:
            raise ValueError(f"Invalid health: {health}. Health cannot be negative.")
        if mana < 0:
            raise ValueError(f"Invalid mana: {mana}. Mana cannot be negative.")
        elif mana > 10:
            raise ValueError(f"Invalid mana: {mana}. Mana cannot be greater than 10.")
        if armor < 0:
            raise ValueError(f"Invalid armor: {armor}. Armor cannot be negative.")

        self.attack = attack
        self.health = health
        self.mana = mana
        self.armor = armor

        self.save_to_table()

    def save_to_table(self) -> None:
        """
        Saves the current Hero instance to a single table within the hearthstone_database.json file.
        """
        heroes_db = Database.initialize_database(DATABASE_PATH)
        Database.insert_data_to_table(heroes_db, "Heroes", [self.to_dict()])
        heroes_db.close()

    def to_dict(self) -> dict:
        """
        Converts the Hero object into a dictionary for serialization or storage.

        Returns:
            dict: A dictionary representation of the hero, including:
                  - ID
                  - Name
                  - Description
                  - Hero class
                  - Hero power
                  - Attack
                  - Health
                  - Mana
                  - Armor
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "hero_class": self.hero_class.value,
            "hero_power": self.hero_power.value,
            "attack": self.attack,
            "health": self.health,
            "mana": self.mana,
            "armor": self.armor,
        }
