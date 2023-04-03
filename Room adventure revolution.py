#Name: Grant
#date: 3/29/2023
#Desc: Room adventure reloaded

from tkinter import *

class Room:
    """ a room that has a name and filepath that points to a .gif image """
    def __init__(self, name: str, filepath: str) -> None:
        self.name = name
        self.filepath = filepath
        self.exits = {}
        self.items = {}
        self.grabs = {}
        self.talkables = {}

    def add_exit(self, label: str, room: 'Room'):
        self.exits[label] = room

    def add_item(self, label: str, desc: str):
        self.items[label] = desc

    def add_grabs(self, label: str):
        self.grabs.append(label)

    def del_grabs(self, label: str):
        self.grabs.remove(label)

    def __str__(self) -> str:
        result = f"You are in {self.name}\n"

        result += "You see:\n"

        for item in self.items.keys():
            result += item + " "
        result += "\n"

        result += "Exits:"
        for exit in self.exits.keys():
            result += exit + " "
        result += "\n"

        return result
class Game:
    pass