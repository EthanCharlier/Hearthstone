#!/usr/bin/python3

# Imports
import os
from tinydb import TinyDB

# Class
class Database:
    """
    A generic utility class for managing database initialization and interactions with TinyDB.
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
        Database.ensure_directory_exists(file_path)

        if not os.path.exists(file_path):
            with open(file_path, 'w') as db_file:
                db_file.write('{}')

        return TinyDB(file_path)

    @staticmethod
    def initialize_table(db: TinyDB, table_name: str) -> TinyDB.Table:
        """
        Retrieves or creates a specific table within the TinyDB database.

        Args:
            db (TinyDB): An instance of the TinyDB database.
            table_name (str): The name of the table to initialize.

        Returns:
            Table: A TinyDB table instance.
        """
        return db.table(table_name)

    @staticmethod
    def insert_data_to_table(db: TinyDB, table_name: str, data: list) -> None:
        """
        Inserts data into a specific table.

        Args:
            db (TinyDB): An instance of the TinyDB database.
            table_name (str): The name of the table where data will be inserted.
            data (list): A list of dictionaries representing the data to be inserted.

        Raises:
            ValueError: If the data is not a list of dictionaries.
        """
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise ValueError("Data must be a list of dictionaries.")

        table = db.table(table_name)
        table.insert_multiple(data)

    @staticmethod
    def fetch_all_from_table(db: TinyDB, table_name: str) -> list:
        """
        Fetches all data from a specific table.

        Args:
            db (TinyDB): An instance of the TinyDB database.
            table_name (str): The name of the table to fetch data from.

        Returns:
            list: A list of all records in the table.
        """
        table = db.table(table_name)
        return table.all()

    @staticmethod
    def clear_table(db: TinyDB, table_name: str) -> None:
        """
        Clears all data from a specific table.

        Args:
            db (TinyDB): An instance of the TinyDB database.
            table_name (str): The name of the table to clear.
        """
        table = db.table(table_name)
        table.truncate()

    @staticmethod
    def delete_database(file_path: str) -> None:
        """
        Deletes the database file.

        Args:
            file_path (str): The path to the TinyDB JSON file to delete.
        """
        if os.path.exists(file_path):
            os.remove(file_path)