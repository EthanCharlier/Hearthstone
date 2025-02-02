#!/usr/bin/python3

# Imports
from tinydb import TinyDB
import json
import os

# Core Imports
from core.game_logic import GameLogic

# Modules Imports
from modules.player_mod import Player
from modules.unit_mod import Unit
from modules.spell_mod import Spell

# Utils Imports
from utils.constants import (
     DATABASE_PATH,
     HEROES_DB_PATH,
     HEROES_TABLE_NAME,
     SPELLS_TABLE_NAME,
     SPELLS_DB_PATH,
     UNITS_DB_PATH,
     UNITS_TABLE_NAME,
     HERO_MAXIMUM_MANA
)
from utils.database_utils import Database

# Interfaces Imports
from interfaces.player_choice_interface import PlayerChoiceInterface

# Class
class Game:
    """
    """

    def __init__(self) -> None:
        """
        """
        self.hearthstone_db = Database.initialize_database(DATABASE_PATH)
        self.init_database(self.hearthstone_db, HEROES_TABLE_NAME, HEROES_DB_PATH)
        self.init_database(self.hearthstone_db, SPELLS_TABLE_NAME, SPELLS_DB_PATH)
        self.init_database(self.hearthstone_db, UNITS_TABLE_NAME, UNITS_DB_PATH)
    
        interface = PlayerChoiceInterface(self.hearthstone_db)
        player_1, player_2 = interface.setup_players()
        self.logic = GameLogic(player_1, player_2)
        self.start()


    def init_database(self, hearthstone_db: TinyDB, table_name: str, table_path: str) -> None:
        """
        """
        if not isinstance(hearthstone_db, TinyDB):
            raise TypeError(f"Expected 'hearthstone_db' to be a TinyDB, got {type(hearthstone_db).__name__}")
        if not isinstance(table_name, str):
            raise TypeError(f"Expected 'table_name' to be a string, got {type(table_name).__name__}")
        if isinstance(table_path, str):
            if not os.path.exists(table_path):
                raise ValueError(f"Invalid table path: {table_path}. No such file or directory.")
        else:
            raise TypeError(f"Expected 'table_path' to be a string, got {type(table_path).__name__}")
        
        with open(table_path, "r") as file:
            table_data = json.load(file)

        if Database.fetch_all_from_table(hearthstone_db, table_name):
            Database.clear_table(hearthstone_db, table_name)
            Database.insert_data_to_table(hearthstone_db, table_name, table_data)
        else:
            Database.insert_data_to_table(hearthstone_db, table_name, table_data)

    def start(self) -> Player:
        """
        """
        turn_order = self.logic.choose_who_starts()
        
        while not self.logic.check_game_over():
            self.play_turn(turn_order[0], turn_order[1])

            if self.logic.check_game_over():
                break

            self.play_turn(turn_order[1], turn_order[0])

            if self.logic.check_game_over():
                break

        winner = self.logic.get_winner()
        print(winner)

    def play_turn(self, player: Player, opponent: Player) -> None:
        """
        """
        print(f"\n--- Tour de {player.name} ---")

        # Étape 1 : Gain de mana (max HERO_MAXIMUM_MANA)
        if player.mana < HERO_MAXIMUM_MANA:
            player.mana += 1
        print(f"{player.name} gagne un cristal de mana. Mana total : {player.mana}/{HERO_MAXIMUM_MANA}")

        # Étape 2 : Pioche d’une carte
        try:
            drawn_card = player.deck.draw()
            print(f"{player.name} a pioché : {drawn_card.name}")
        except ValueError:
            print(f"{player.name} n'a plus de cartes à piocher.")

        # Étape 3 : Jouer des cartes (Serviteurs et Sorts)
        while True:
            playable_cards = [card for card in player.deck.hand if card.cost <= player.mana]
            if not playable_cards:
                print("Aucune carte jouable.")
                break

            print("\nCartes disponibles :")
            for i, card in enumerate(playable_cards):
                print(f"{i + 1}. {card.name} - Coût: {card.cost} - Type: {'Serviteur' if isinstance(card, Unit) else 'Sort'}")

            choix = input("Entrez le numéro de la carte à jouer (ou '0' pour passer) : ")
            if choix == '0':
                break

            try:
                index = int(choix) - 1
                if index < 0 or index >= len(playable_cards):
                    print("Choix invalide.")
                    continue

                card_to_play = playable_cards[index]

                if isinstance(card_to_play, Unit):  # Si c'est un serviteur
                    player.mana -= card_to_play.cost
                    player.deck.play_card(card_to_play)  # Ajoute l'unité au plateau via deck
                    print(f"{player.name} a joué le serviteur : {card_to_play.name}")
                elif isinstance(card_to_play, Spell):  # Si c'est un sort
                    player.mana -= card_to_play.cost
                    player.deck.play_card(card_to_play)
                    card_to_play.cast(player, opponent)
                    print(f"{player.name} a lancé le sort : {card_to_play.name}")

            except ValueError:
                print("Entrée invalide, veuillez réessayer.")

        # Étape 4 : Pouvoir héroïque (coût : 2 mana)
        if player.mana >= 2:
            use_hero_power = input(f"Voulez-vous utiliser le pouvoir héroïque de {player.hero.name} ? (oui/non) : ").strip().lower()
            if use_hero_power == "oui":
                try:
                    player.attack += 2
                    player.mana -= 2
                    print(f"{player.name} utilise son pouvoir héroïque : {player.hero.hero_power}")
                except Exception as e:
                    print(f"Impossible d'utiliser le pouvoir héroïque : {e}")

        # Étape 5 : Attaques (Serviteurs et Héros)
        while True:
            if not player.deck.board:
                break

            print("\nServiteurs en jeu :")
            for i, unit in enumerate(player.deck.board):
                print(f"{i + 1}. {unit.name} (ATK: {unit.attack}, PV: {unit.health})")

            choix = input("Entrez le numéro du serviteur pour attaquer (ou '0' pour passer) : ")
            if choix == '0':
                break

            try:
                index = int(choix) - 1
                if index < 0 or index >= len(player.deck.board):
                    print("Choix invalide.")
                    continue

                attacker = player.deck.board[index]

                print("\nCibles possibles :")
                print(f"0. {opponent.name} (PV: {opponent.health})")
                for j, enemy_unit in enumerate(opponent.deck.board):
                    print(f"{j + 1}. {enemy_unit.name} (PV: {enemy_unit.health})")

                target_choix = input(f"Entrez le numéro de la cible : ")
                try:
                    target_index = int(target_choix) - 1
                    if target_index == -1:
                        target = opponent
                        attacker.attack_player_or_unit(target)
                        player.deck.move_to_graveyard(attacker)
                    elif 0 <= target_index < len(opponent.deck.board):
                        target = opponent.deck.board[target_index]
                        attacker.attack_player_or_unit(target)
                        player.deck.move_to_graveyard(attacker)
                    else:
                        print("Cible invalide.")
                        continue
                    
                    print(f"{attacker.name} attaque {target.name} et inflige {attacker.attack} dégâts !")
                    

                except ValueError:
                    print("Entrée invalide, veuillez réessayer.")

            except ValueError:
                print("Entrée invalide, veuillez réessayer.")

        # Attaque du héros
        if player.attack > 0:
            attack_choice = input(f"Voulez-vous attaquer avec votre héros ? (oui/non) : ").strip().lower()
            if attack_choice == "oui":
                print("\nCibles possibles :")
                print(f"0. {opponent.name} (PV: {opponent.health})")
                for j, enemy_unit in enumerate(opponent.deck.board):
                    print(f"{j + 1}. {enemy_unit.name} (PV: {enemy_unit.health})")

                target_choix = input(f"Entrez le numéro de la cible : ")
                try:
                    target_index = int(target_choix) - 1
                    if target_index == -1:
                        target = opponent
                        player.attack_player_or_unit(target)
                    elif 0 <= target_index < len(opponent.deck.board):
                        target = opponent.deck.board[target_index]
                        player.attack_player_or_unit(target)
                        if target.health <= 0:
                            opponent.deck.move_to_graveyard(target)
                    else:
                        print("Cible invalide.")
                        return

                    print(f"{player.name} attaque {target.name} et inflige {player.attack} dégâts !")
                    player.attack = 0
                except ValueError:
                    print("Entrée invalide, veuillez réessayer.")

        # Étape 6 : Fin du tour
        print(f"Fin du tour de {player.name}. Mana restant : {player.mana}")
