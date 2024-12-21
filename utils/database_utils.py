#!/usr/bin/python3

# Imports
import os
from tinydb import TinyDB

# Class
class DatabaseUtils():
    """
    A utility class for managing database initialization and interactions with TinyDB.
    """

    @staticmethod
    def ensure_directory_exists(path: str) -> None:
        """
        Ensures that the directory for the given path exists. Creates it if it doesn't.

        Args:
            path (str): The file path whose directory should be checked/created.
        """
        directory = os.path.dirname(path)
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)

    @staticmethod
    def initialize_database(file_path: str) -> TinyDB:
        """
        Ensures the database file exists and returns a TinyDB instance.

        Args:
            file_path (str): Path to the TinyDB JSON file.

        Returns:
            TinyDB: An instance of the TinyDB database.
        """
        DatabaseUtils.ensure_directory_exists(file_path)
        
        if not os.path.exists(file_path):
            with open(file_path, 'w') as db_file:
                db_file.write('{}')

        return TinyDB(file_path)
