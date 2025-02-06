# -------------------------------
# Database File Paths
# -------------------------------
# Paths to the main game database and specific data files for heroes, spells, and units.
DATABASE_PATH = "../database/hearthstone_database.json"
HEROES_DB_PATH = "./database/data/heroes.json"
SPELLS_DB_PATH = "./database/data/spells.json"
UNITS_DB_PATH = "./database/data/units.json"

# -------------------------------
# Database Table Names
# -------------------------------
# Names of the tables used in the TinyDB database.
PLAYERS_TABLE_NAME = "players"
DECKS_TABLE_NAME = "decks"
HEROES_TABLE_NAME = "heroes"
SPELLS_TABLE_NAME = "spells"
UNITS_TABLE_NAME = "units"

# -------------------------------
# Default Hero Stats
# -------------------------------
# These are the starting values for a hero at the beginning of the game.
HERO_STARTING_ATTACK = 0  # Heroes start with no attack power.
HERO_STARTING_HEALTH = 30  # Standard initial health for a hero.
HERO_STARTING_MANA = 1  # Heroes begin with 1 mana.
HERO_STARTING_ARMOR = 0  # No armor at the start.

# -------------------------------
# Maximum Hero Stats
# -------------------------------
# These define the upper limits for hero attributes during the game.
HERO_MAXIMUM_ATTACK = None  # No predefined attack limit.
HERO_MAXIMUM_HEALTH = 30  # Maximum hero health is 30.
HERO_MAXIMUM_MANA = 10  # A hero cannot exceed 10 mana.
HERO_MAXIMUM_ARMOR = None  # No predefined armor limit.

# -------------------------------
# Maximum Card Stats
# -------------------------------
# These define the upper limits for individual card attributes.
CARD_MAXIMUM_ATTACK = None  # No predefined maximum attack for a card.
CARD_MAXIMUM_HEALTH = 30  # Maximum health a card can have.
CARD_MAXIMUM_COST = 10  # No card can cost more than 10 mana.
CARD_MAXIMUM_ARMOR = None  # No predefined armor limit for cards.

# -------------------------------
# Deck Limits
# -------------------------------
# These values impose restrictions on the number of cards in hand and on the board.
HAND_LIMIT = 10  # Maximum number of cards a player can hold in their hand.
BOARD_LIMIT = 5  # Maximum number of cards a player can place on the board.
