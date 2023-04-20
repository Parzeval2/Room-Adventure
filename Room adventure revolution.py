# Name: Gavin, Grant, Matthew, and Max
# date: 3/29/2023
# Desc: Room adventure reloaded

from tkinter import *
from random import choice
import CLines


class Room:
    """ a room that has a name and filepath that points to a .gif image """

    def __init__(self, name: str, filepath: str, number: int) -> None:
        self.name = name
        self.filepath = filepath
        self.exits = {}
        self.items = {}
        self.grabs = []
        self.talkables = {}
        self.locked = False
        self.key = None
        self.number = number

    def add_exit(self, label: str, room: 'Room'):
        self.exits[label] = room

    def add_item(self, label: str, desc: str):
        self.items[label] = desc

    def remove_item(self, label: str):
        del self.items[label]

    def add_grabs(self, label: str):
        self.grabs.append(label)

    def del_grabs(self, label: str):
        self.grabs.remove(label)

    # make room locked
    def lock(self):
        self.locked = True

    def required_key(self, key):
        self.key = key

    def unlock(self):
        self.locked = False

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

        result += "Corriell: " + voiceline

        return result


class Game(Frame):
    global voiceline
    voiceline = ''
    EXIT_ACTIONS = ["quit,""exit", "bye", "q"]

    # statuses
    STATUS_DEFAULT = "I don't understand. Try [verb] [noun]. Valid verbs are go, look, take"
    SATUS_DEAD = "You are dead."
    STATUS_BAD_EXIT = "Invalid exit."
    STATUS_ROOM_CHANGE = "Room Changed"
    STATUS_GRABBED = "Item Grabbed"
    STATUS_BAD_GRABBABLE = "I cant grab that"
    STATUS_BAD_ITEM = "I dont see that"
    STATUS_UNLOCKED = "Room Unlocked"
    STATUS_LOCKED = "Room Locked"
    STATUS_BAD_KEY = "This key isnt unlocking the door"

    STATUS_LET_GUESS = "You gaze upon the majestic stone bust of Lady Gaga, you notice the mouth seems to be loose. You open it to see a small key pad, perhaps theres a code? Maybe you can guess./n[Hint: guess with <solve> <guess>]"
    STATUS_BAD_GUESS = "That doesn't seem to be right"
    STATUS_EGG_GRAB = "The chest portion of the bust opens to reveal a mystical cosmic Egg, you take the egg in your hands.\nBeautiful. Despite it's small, frail size it feels as though you could go straight into the egg"
    STATUS_BAD_UNKNOWN = "okay... sure...?"
    STATUS_ENTER_EGG = "You enter the egg"
    STATUS_NO_SOLVE = "There is nothing to solve here"

    WIDTH = 800
    HEIGHT = 600

    def __init__(self, parent):
        self.inventory = []
        Frame.__init__(self, parent)
        self.pack(fill=BOTH, expand=1)

    def setup_game(self):
        # create rooms
        r1 = Room("Room 1", "room1.gif", 1)
        r2 = Room("Room 2", "room2.gif", 2)
        r3 = Room("Room 3", "room3.gif", 3)
        r4 = Room("Room 4", "room4.gif", 4)
        r5 = Room("Room 5", "cosmicEgg.gif", 5)

        # add exits
        r1.add_exit("south", r3)
        r1.add_exit("east", r2)
        r1.add_exit("secretTunnel", r5)

        r2.add_exit("west", r1)
        r2.add_exit("south", r4)
        r2.add_exit("secretTunnel", r5)

        r3.add_exit("north", r1)
        r3.add_exit("east", r4)
        r3.add_exit("secretTunnel", r5)

        r4.add_exit("north", r2)
        r4.add_exit("west", r3)
        r4.add_exit("south", None)
        r4.add_exit("secretTunnel", r5)

        r5.add_exit("none", r5)

        # add items
        r1.add_item("chair", ""
                             "The chair's sleek black alloy legs and shimmering, translucent backrest pulse with a soft blue light, powered by an unknown energy source. "
                             "The cushion is made of a high-tech, memory foam material that molds to your body as you sit, while the armrests are made of a flexible polymer that adjusts to your arms. "
                             "The small control panel embedded in the armrest allows for adjustable height, angle, and lumbar support. "
                             "This chair was clearly designed for long space voyages, combining futuristic style with ergonomic functionality.")
        r1.add_item("large_chair", "The massive skull throne before you is a formidable sight to behold. "
                                   "Crafted from dark, polished metal, it seems to radiate an aura of power and dominance. "
                                   "Its legs are thick and sturdy, each one ending in sharp, pointed tips that look like they could easily pierce through any surface. "
                                   "The backrest is tall and imposing, decorated with intricate, glowing circuitry that gives off a faint green light. "
                                   "The armrests are wide and adorned with sharp, jagged edges, evoking the image of a throne fit for a space lord or conqueror. "
                                   "As you take a closer look, you notice small details that speak to its craftsmanship, such as the precision sculpting of the metal and the flawless finish of the material. "
                                   "This throne-like chair is not just a piece of furniture, but a symbol of power and authority that commands attention and respect.")
        r1.add_item("key", "The key card in your hand is a futuristic marvel. "
                           "Made of a lightweight metallic alloy, it's smooth to the touch and adorned with glowing symbols and glyphs along its edge.")

        r2.add_item("fireplace", "The fireplace on the space station is a rare sight, burning specialized fuel pellets that create blue flames that dance around a sleek, heat-resistant alloy surround. "
                                 "The mantel is engraved with alien symbols, and above the fireplace, a holographic display simulates a cozy cabin setting. "
                                 "It's a vital psychological boost for astronauts, providing a moment of relaxation and respite from space travel.")
        r2.add_item("chair", "The chair before you is nothing short of comical. "
                             "It's so small that it looks like it was made for a child's dollhouse rather than a human being. "
                             "The seat is barely wide enough to accommodate your backside, and the backrest is so low that it doesn't even reach your shoulder blades. "
                             "The legs are short and stubby, and the entire chair is barely a foot off the ground. "
                             "Despite its diminutive size, the chair is surprisingly sturdy, made of a durable yet lightweight material that doesn't creak or wobble under your weight. "
                             "The chair's surface is smooth and shiny, and it's colored in a bright, cheerful hue that only adds to its whimsical charm. "
                             "While it's clearly not a practical seating option for most people, it's hard to resist the urge to sit on it and revel in its absurdity.")

        r3.add_item("desk", "The desk is a stunning combination of sleek metals and advanced polymers. "
                            "Its surface is touch-sensitive and scratch-resistant, and the drawers and compartments are hidden within the design. "
                            "The legs are angular, and a holographic display rises from the desk, providing virtual access to your computer or other devices.")
        r3.add_item("small_statue", "A small stone bust of Lady Gaga.")
        r3.add_item("dimsdale_dimadome", "owned by doug dimadome")
        r3.add_item("fancy_chair", "The chair is generously proportioned and upholstered in fine leather with intricate stitching and piping. "
                                   "The legs are made of polished wood, and the arms are gracefully curved and adorned with delicate carvings.")

        r4.add_item("croissant", "Moldy")

        r5.add_item("the_egg", "You look at the egg and are filled with great joy. You feel complete. It is done.")
        # add grabs
        r1.add_grabs("key")
        r2.add_grabs("fire")
        r3.add_grabs("doug")
        r4.add_grabs("butter")

        # locking
        r3.lock()
        r3.required_key("key")
        # set the current room to the starting room
        self.current_room = r1

    def setup_gui(self):
        self.player_input = Entry(self, bg="white", fg="black")
        self.player_input.bind("<Return>", self.process)
        self.player_input.pack(side=BOTTOM, fill=X)
        self.player_input.focus()

        # the image container and default image
        img = None  # represetns the actual image
        self.image_container = Label(self, width=Game.WIDTH // 2, height=Game.HEIGHT // 2)
        self.image_container.image = img
        self.pack(side=LEFT, fill=Y)
        self.image_container.pack_propagate(False)

        #Create button to go to minimap
        self.btn = Button(self, text = 'Minimap', command = self.minimap)
        self.btn.pack(side=RIGHT, fill=Y, expand=1)
        
        # container for the game text
        text_container = Frame(self, width=Game.WIDTH // 2)
        self.text = Text(text_container, bg="lightgrey", fg="black")
        self.text.pack(fill=Y, expand=1)
        text_container.pack(side=RIGHT, fill=Y)
        
    def minimap(self):
        mini.pack(anchor=CENTER)
        game.pack_forget()
        mini.here()

    def set_room_image(self):
        if self.current_room is None:
            img = PhotoImage(file="skull.gif")
        else:
            img = PhotoImage(file="")

        self.image_container.config(image=img)
        self.image_container.image = img

    def set_status(self, status):
        self.text.config(state=NORMAL)
        self.text.delete(1.0, END)

        if self.current_room is None:
            self.text.insert(END, self.STATUS_DEAD)
        else:
            content = f"{self.current_room}\n You are carrying: {self.inventory}\n\n{status}"
            self.text.insert(END, content)

        self.text.config(state=DISABLED)

    def clear_entry(self):
        self.player_input.delete(0, END)

    def handle_go(self, destination):
        status = Game.STATUS_BAD_EXIT
        global voiceline
        if (destination == "egg" and destination in self.inventory):
            destination = "secretTunnel"
            self.current_room = self.current_room.exits[destination]
            status = Game.STATUS_ROOM_CHANGE
        elif (destination in self.current_room.exits):
            if self.current_room.exits[destination].locked == True:
                voiceline = choice(CLines.VLLockedDoor)
                status = Game.STATUS_LOCKED
            else:
                self.current_room = self.current_room.exits[destination]
                voiceline = choice(CLines.VLNewRoom, CLines.VLGoRight)
                status = Game.STATUS_ROOM_CHANGE

        self.set_status(status)

    def handle_unlock(self, destination):
        status = Game.STATUS_BAD_KEY
        if destination in self.current_room.exits:
            for playerkey in self.inventory:
                if playerkey in self.inventory and playerkey == self.current_room.exits[destination].key:
                    self.current_room.exits[destination].unlock()
                    status = Game.STATUS_UNLOCKED
                else:
                    global voiceline
                    voiceline = choice(CLines.VLWrongKey)

        self.set_status(status)

    def handle_look(self, item):
        status = Game.STATUS_BAD_ITEM
        if item in self.current_room.items:
            if item == "small_statue":
                    status = Game.STATUS_LET_GUESS
            else:
                status = self.current_room.items[item]

        self.set_status(status)
    
    def handle_solve(self, guess):
        guess = guess.upper()
        code = "ERWY"
        status = Game.STATUS_BAD_GUESS
        if guess == code:
            self.inventory.append("egg")
            status = Game.STATUS_EGG_GRAB

        self.set_status(status)
        
    def handle_take(self, grabbable):
        status = Game.STATUS_BAD_GRABBABLE
        if grabbable in self.current_room.grabs:
            if grabbable == "key":
                self.current_room.remove_item("key")
            self.inventory.append(grabbable)
            self.current_room.del_grabs(grabbable)
            status = Game.STATUS_GRABBED
        self.set_status(status)

    def play(self):
        self.setup_game()
        self.setup_gui()
        self.set_room_image()
        self.set_status("")

    def process(self, event):
        action = self.player_input.get()
        action = action.lower()

        if action in Game.EXIT_ACTIONS:
            exit()

        if self.current_room is None:
            self.clear_entry()
            return

        words = action.split()

        if len(words) != 2:
            global voiceline
            voiceline = choice(CLines.VLBadSyntax) or choice(CLines.VLLost)
            self.set_status(Game.STATUS_DEFAULT)
            return

        self.clear_entry()
        verb = words[0]
        noun = words[1]

        match verb:
            case "go":
                self.handle_go(destination=noun)
            case "look":
                self.handle_look(item=noun)
            case "take":
                self.handle_take(grabbable=noun)

            ### CUSTOM VERBS
            case "unlock":  ## Implemented by Grant
                self.handle_unlock(destination=noun)
            case "solve":   ## Implemented by Gavin
                self.handle_solve(guess=noun)
            
            ### ALTERNATIVES FOR MAIN VERBS     ## Implemented by Gavin
            case "move":
                self.handle_go(destination=noun)
            case "see":
                self.handle_look(item=noun)
            case "get":
                self.handle_take(grabbable=noun)
                
class Minimap(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()
        self.config(width=WIDTH,height=HEIGHT)
        #will be used to find where to put the "I am here!" label
        self.position = {1:"0 5", 2:"0 7", 3:"2 5", 4:"2 7", 6:"0 3", 7:"0 1", 8:"2 1"}
        
    def setup_gui(self):
        #Sets all the rooms labels
        l1 = Label(self, text="Common Area", width=200//6, height=300//24, relief="solid", anchor=N,)
        l2 = Label(self, text="Dining Hall", width=200//6, height=300//24, relief="solid", anchor=N,)
        l3 = Label(self, text="Restricted Labratory", width=200//6, height=300//24, relief="solid", anchor=N,)
        l4 = Label(self, text="Sleeping Quarters", width=200//6, height=300//24, relief="solid", anchor=N,)
        l6 = Label(self, text="Corridor", width=200//6, height=300//24, relief="solid", anchor=N,)
        l7 = Label(self, text="Observation Deck", width=200//6, height=300//24, relief="solid", anchor=N,)
        l8 = Label(self, text="Labratory", width=200//6, height=300//24, relief="solid", anchor=N,)
        #Spaces labels
        l9 = Label(self, height=1, width=1)
        l10 = Label(self, height=1, width=1)
        l11 = Label(self, height=1, width=1)
        #Create button to go back to game
        self.btn = Button(self, text = 'Go Back', command = self.back, height=300//12)
        self.btn.grid(rowspan=3, column=0)
        
        #Positions all labels
        l1.grid(row=0, column=5)
        l2.grid(row=0,column=7)
        l3.grid(row=2,column=5)
        l4.grid(row=2,column=7)
        l6.grid(row=0,column=3)
        l7.grid(row=0,column=1)
        l8.grid(row=2,column=1)
        l9.grid(row=1, column=2)
        l10.grid(row=1, column=4)
        l11.grid(row=1, column=6)
        
    def here(self):
        self.hereLabel = Label(self, text="You are here!", anchor=CENTER)
        row, col = self.position[game.current_room.number].split()
        self.hereLabel.grid(row=row, column=col)
        
    def back(self):
        game.pack(anchor=CENTER)
        mini.pack_forget()
        self.hereLabel.destroy()

# main

window = Tk()
window.title("Room Adventure")
game = Game(window)
mini = Minimap(window)
game.pack(anchor=CENTER)
mini.pack_forget()
game.play()
mini.setup_gui()
window.mainloop()
