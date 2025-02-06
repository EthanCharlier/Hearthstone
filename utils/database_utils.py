#!/usr/bin/python3

# Imports
import os
from typing import Any
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
        directory = os.path.dirname(path)  # Extracts the directory from the file path
        if not os.path.exists(directory):  # Checks if the directory exists
            os.makedirs(directory, exist_ok=True)  # Creates the directory if it doesn't exist

    @staticmethod
    def initialize_database(file_path: str) -> TinyDB:
        """
        Ensures the database file exists and returns a TinyDB instance.

        Args:
            file_path (str): Path to the TinyDB JSON file.

        Returns:
            TinyDB: An instance of the TinyDB database.
        """
        Database.ensure_directory_exists(file_path)  # Ensure the directory exists before accessing the file

        if not os.path.exists(file_path):  # Checks if the file doesn't exist
            with open(file_path, 'w') as db_file:  # Creates an empty file if it doesn't exist
                db_file.write('{}')  # Initializes the file with an empty dictionary

        return TinyDB(file_path)  # Returns a TinyDB instance for the provided file path

    @staticmethod
    def initialize_table(db: TinyDB, table_name: str) -> Any:
        """
        Retrieves or creates a specific table within the TinyDB database.

        Args:
            db (TinyDB): An instance of the TinyDB database.
            table_name (str): The name of the table to initialize.

        Returns:
            Table: A TinyDB table instance.
        """
        return db.table(table_name)  # Returns the table instance with the given name

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
        # Check if the data is a list and that each item is a dictionary
        if not isinstance(data, list) or not all(isinstance(item, dict) for item in data):
            raise ValueError("Data must be a list of dictionaries.")  # Raise error if the validation fails

        table = db.table(table_name)  # Retrieve the table with the provided name
        table.insert_multiple(data)  # Insert multiple records into the table

        # db.storage.flush()  # Optionally, you can call flush to save changes to the storage immediately (commented out)

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
        table = db.table(table_name)  # Retrieve the table
        return table.all()  # Return all records from the table

    @staticmethod
    def clear_table(db: TinyDB, table_name: str) -> None:
        """
        Clears all data from a specific table.

        Args:
            db (TinyDB): An instance of the TinyDB database.
            table_name (str): The name of the table to clear.
        """
        table = db.table(table_name)  # Retrieve the table
        table.truncate()  # Clear all data in the table

    @staticmethod
    def delete_database(file_path: str) -> None:
        """
        Deletes the database file.

        Args:
            file_path (str): The path to the TinyDB JSON file to delete.
        """
        if os.path.exists(file_path):  # Check if the file exists
            os.remove(file_path)  # Delete the file
