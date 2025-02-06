#!/usr/bin/python3

# Modules Imports
from utils.database_utils import Database
from enums.hero_power_enum import HeroPower, HERO_CLASS_TO_POWER

# Constants Imports
from utils.constants import (
    DATABASE_PATH,
    HERO_STARTING_ATTACK,
    HERO_STARTING_HEALTH,
    HERO_STARTING_MANA,
    HERO_STARTING_ARMOR,
    HERO_MAXIMUM_ATTACK,
    HERO_MAXIMUM_HEALTH,
    HERO_MAXIMUM_ARMOR,
    HERO_MAXIMUM_MANA
)

# Enum Imports
from enums.card_class_enum import CardClass

# Class
class Hero():
    """
    Represents a hero in a card game. Each hero has a specific class, power, and starting attributes 
    (health, mana, attack, and armor), and can be saved to a database.

    Attributes:
        id (int): Unique identifier for the hero.
        name (str): Name of the hero.
        description (str): A short description or lore about the hero.
        hero_class (CardClass): The class of the hero (e.g., Mage, Warrior).
        hero_power (HeroPower): The power associated with the hero class.
        attack (int): The starting attack value for the hero (default is `HERO_STARTING_ATTACK`).
        health (int): The starting health value for the hero (default is `HERO_STARTING_HEALTH`).
        mana (int): The starting mana value for the hero (default is `HERO_STARTING_MANA`).
        armor (int): The starting armor value for the hero (default is `HERO_STARTING_ARMOR`).

    Methods:
        __init__: Initializes a new hero object with the specified attributes.
        save_to_table: Saves the hero object to a database.
        get_maximum_attack: Returns the maximum allowable attack for the hero.
        get_maximum_health: Returns the maximum allowable health for the hero.
        get_maximum_mana: Returns the maximum allowable mana for the hero.
        get_maximum_armor: Returns the maximum allowable armor for the hero.
        to_dict: Converts the hero object to a dictionary format for serialization or storage.
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
        Initializes a Hero object with the provided attributes.

        Args:
            id (int): The unique identifier for the hero.
            name (str): The name of the hero.
            description (str): A description or lore of the hero.
            hero_class (CardClass): The hero's class (must be a valid `CardClass`).
            hero_power (HeroPower): The hero's power (must be a valid `HeroPower`).
            attack (int): The hero's starting attack (default: `HERO_STARTING_ATTACK`).
            health (int): The hero's starting health (default: `HERO_STARTING_HEALTH`).
            mana (int): The hero's starting mana (default: `HERO_STARTING_MANA`).
            armor (int): The hero's starting armor (default: `HERO_STARTING_ARMOR`).

        Raises:
            ValueError: If `hero_class` is not a valid `CardClass`.
            ValueError: If `hero_power` is not a valid `HeroPower`.
            ValueError: If `hero_power` does not match the expected value for `hero_class`.
            ValueError: If `attack`, `health`, `mana`, or `armor` are negative or exceed their maximum limits.
        """
        self.id = id  # Set unique hero identifier
        self.name = name  # Set hero name
        self.description = description  # Set hero's description

        # Check if the provided hero class is valid
        if not isinstance(hero_class, CardClass):
            raise ValueError(f"Invalid hero class: {hero_class}. Must be a CardClass enum.")
        self.hero_class = hero_class

        # Check if the provided hero power is valid
        if not isinstance(hero_power, HeroPower):
            raise ValueError(f"Invalid hero power: {hero_power}. Must be a HeroPower enum.")
        
        # Ensure the hero power matches the class
        if HERO_CLASS_TO_POWER.get(hero_class) != hero_power:
            raise ValueError(
                f"Invalid hero power: {hero_power} for class {hero_class}. "
                f"Expected power: {HERO_CLASS_TO_POWER[hero_class]}."
            )
        self.hero_power = hero_power  # Set the hero power

        # Validate and set attack, ensuring it does not exceed the maximum allowed
        if attack < 0:
            raise ValueError(f"Invalid attack: {attack}. Attack cannot be negative.")
        elif HERO_MAXIMUM_ATTACK is not None and attack > HERO_MAXIMUM_ATTACK:
            raise ValueError(f"Invalid attack: {attack}. Attack cannot be greater than {HERO_MAXIMUM_ATTACK}.")
        
        # Validate and set health, ensuring it does not exceed the maximum allowed
        if health < 0:
            raise ValueError(f"Invalid health: {health}. Health cannot be negative.")
        elif HERO_MAXIMUM_HEALTH is not None and health > HERO_MAXIMUM_HEALTH:
            raise ValueError(f"Invalid health: {health}. Health cannot be greater than {HERO_MAXIMUM_HEALTH}.")
        
        # Validate and set mana, ensuring it does not exceed the maximum allowed
        if mana < 0:
            raise ValueError(f"Invalid mana: {mana}. Mana cannot be negative.")
        elif HERO_MAXIMUM_MANA is not None and mana > HERO_MAXIMUM_MANA:
            raise ValueError(f"Invalid mana: {mana}. Mana cannot be greater than {HERO_MAXIMUM_MANA}.")
        
        # Validate and set armor, ensuring it does not exceed the maximum allowed
        if armor < 0:
            raise ValueError(f"Invalid armor: {armor}. Armor cannot be negative.")
        elif HERO_MAXIMUM_ARMOR is not None and armor > HERO_MAXIMUM_ARMOR:
            raise ValueError(f"Invalid armor: {armor}. Armor cannot be greater than {HERO_MAXIMUM_ARMOR}.")

        self.attack = attack  # Set the attack value
        self.health = health  # Set the health value
        self.mana = mana  # Set the mana value
        self.armor = armor  # Set the armor value

        # Save the hero's information to the database
        self.save_to_table()

    def save_to_table(self) -> None:
        """
        Saves the current hero instance to a database.

        This method stores the hero in the `Heroes` table of the database defined by `DATABASE_PATH`.
        """
        heroes_db = Database.initialize_database(DATABASE_PATH)  # Initialize the database
        Database.insert_data_to_table(heroes_db, "Heroes", [self.to_dict()])  # Insert hero data into the database
        heroes_db.close()  # Close the database connection

    @property
    def get_maximum_attack(self) -> int:
        """
        Returns the maximum attack value allowed for the hero.

        Returns:
            int: The maximum attack value (from `HERO_MAXIMUM_ATTACK`).
        """
        return HERO_MAXIMUM_ATTACK  # Return the maximum attack value

    @property
    def get_maximum_health(self) -> int:
        """
        Returns the maximum health value allowed for the hero.

        Returns:
            int: The maximum health value (from `HERO_MAXIMUM_HEALTH`).
        """
        return HERO_MAXIMUM_HEALTH  # Return the maximum health value
    
    @property
    def get_maximum_mana(self) -> int:
        """
        Returns the maximum mana value allowed for the hero.

        Returns:
            int: The maximum mana value (from `HERO_MAXIMUM_MANA`).
        """
        return HERO_MAXIMUM_MANA  # Return the maximum mana value
    
    @property
    def get_maximum_armor(self) -> int:
        """
        Returns the maximum armor value allowed for the hero.

        Returns:
            int: The maximum armor value (from `HERO_MAXIMUM_ARMOR`).
        """
        return HERO_MAXIMUM_ARMOR  # Return the maximum armor value

    def to_dict(self) -> dict:
        """
        Converts the hero object into a dictionary representation.

        This method is useful for serializing or storing the hero data in a database.

        Returns:
            dict: A dictionary containing the hero's attributes such as ID, name, description, class, power, attack, health, mana, and armor.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "hero_class": self.hero_class.value,  # Convert hero class to its string value
            "hero_power": self.hero_power.value,  # Convert hero power to its string value
            "attack": self.attack,
            "health": self.health,
            "mana": self.mana,
            "armor": self.armor,
        }
