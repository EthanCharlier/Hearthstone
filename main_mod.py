#!/usr/bin/python3

"""
"""

# Imports
from rich import print
from rich.panel import Panel

# Class
class Main():
    """
    """

    def __init__(self):
        pass

    def display_main_menu(self) -> None:
        print(Panel("Hello, [red]World!", title="M E N U", subtitle="Thank you"))

if __name__ == "__main__":
    Main().display_main_menu()
