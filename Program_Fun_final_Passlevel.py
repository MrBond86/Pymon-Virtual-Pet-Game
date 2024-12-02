'''
Everything is coverd in this level'''
import os
import sys
import random
import datetime

class Creature:
    def __init__(self, nickname, description, location=None):
        self.nickname = nickname
        self.description = description
        self.location = location

    def set_location(self, location):
        self.location = location

    def get_location(self):
        return self.location

class Pymon(Creature):
    def __init__(self, nickname="Kimimon", description="I am white and yellow with a square face.", energy=3):
        super().__init__(nickname, description)
        self.energy = energy
        self.current_location = None

    def move(self, direction):
        if self.current_location and direction in self.current_location.doors:
            new_location = self.current_location.doors[direction]
            if new_location:
                self.current_location.creatures.remove(self)
                new_location.add_creature(self)
                self.current_location = new_location
                print(f"\nYou traveled {direction} and arrived at {self.current_location.get_name()}.")
            else:
                print(f"\nThere is no door to the {direction}. Pymon remains at its current location.")
        else:
            print("\nInvalid direction. Please enter west, north, east, or south.")

    def spawn(self, loc):
        loc.add_creature(self)
        self.current_location = loc

    def inspect(self):
        return f"\nHi Player, my name is {self.nickname}. {self.description} My energy level is {self.energy}/3. What can I do to help you?"

class Location:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.doors = {"west": None, "north": None, "east": None, "south": None}
        self.creatures = []

    def add_creature(self, creature):
        self.creatures.append(creature)
        creature.set_location(self)

    def connect(self, direction, another_room):
        if another_room:
            self.doors[direction] = another_room
            opposite_directions = {"west": "east", "east": "west", "north": "south", "south": "north"}
            opposite_direction = opposite_directions[direction]
            another_room.doors[opposite_direction] = self

    def get_name(self):
        return self.name

    def inspect(self):
        creature_names = ', '.join([creature.nickname for creature in self.creatures]) or "None"
        return f"\nYou are at {self.name}, {self.description}.\nCreatures present: {creature_names}."

class Record:
    def __init__(self):
        self.locations = {}
        self.creatures = []
        self.create_initial_setup()

    def create_initial_setup(self):
        # Creating locations
        self.locations['Playground'] = Location("Playground", "An outdoor playground with slide and swing clearly visible.")
        self.locations['Beach'] = Location("Beach", "A sandy beach with waves gently crashing onto the shore.")
        self.locations['School'] = Location("School", "A small building with several classrooms and a large bell on top.")

        # Connecting locations
        self.locations['Playground'].connect('west', self.locations['School'])
        self.locations['Playground'].connect('north', self.locations['Beach'])
        self.locations['Beach'].connect('south', self.locations['Playground'])
        self.locations['School'].connect('east', self.locations['Playground'])

        # Adding creatures
        kitimon = Creature("Kitimon", "A friendly blue Pymon with tiny wings.", self.locations['Playground'])
        sheep = Creature("Sheep", "A small fluffy animal, not a Pymon but adorable.", self.locations['Beach'])
        marimon = Creature("Marimon", "A fierce looking red Pymon with sharp claws.", self.locations['School'])

        # Placing creatures in their locations
        self.locations['Playground'].add_creature(kitimon)
        self.locations['Beach'].add_creature(sheep)
        self.locations['School'].add_creature(marimon)

        self.creatures.extend([kitimon, sheep, marimon])

    def import_data(self, filename, type='location'):
        with open(filename, 'r') as file:
            headers = file.readline().strip().split(',')
            for line in file:
                data = line.strip().split(',')
                if type == 'location':
                    data_dict = dict(zip(headers, data))
                    name = data_dict['name'].strip()
                    description = data_dict['description'].strip()
                    location = Location(name, description)
                    self.locations[name] = location
                elif type == 'creature':
                    data_dict = dict(zip(headers, data))
                    nickname = data_dict['nickname'].strip()
                    description = data_dict['description'].strip()
                    location_name = data_dict['adoptable'].strip()
                    location = self.locations.get(location_name, None)
                    if location:
                        creature = Creature(nickname, description)
                        location.add_creature(creature)
                        self.creatures.append(creature)

    def establish_connections(self):
        for location in self.locations.values():
            with open('locations.csv', 'r') as file:
                headers = file.readline().strip().split(',')
                for line in file:
                    data = line.strip().split(',')
                    data_dict = dict(zip(headers, data))
                    if data_dict['name'].strip() == location.name:
                        for direction in ['west', 'north', 'east', 'south']:
                            neighbor_name = data_dict[direction].strip() if data_dict[direction] and data_dict[direction] != 'None' else None
                            if neighbor_name and neighbor_name in self.locations:
                                location.connect(direction, self.locations[neighbor_name])

    def get_locations(self):
        return list(self.locations.values())

class Operation:
    def __init__(self):
        self.record = Record()
        self.current_pymon = Pymon()
        initial_location = self.record.locations.get("Playground")
        if initial_location is None:
            raise Exception("Initial location 'Playground' not found in locations.")
        self.current_pymon.spawn(initial_location)

    def handle_menu(self):
        while True:
            print("\nPlease issue a command to your Pymon:")
            print("1) Inspect Pymon")
            print("2) Inspect current location")
            print("3) Move")
            print("4) Exit the program")
            choice = input("Your command: ")

            if choice == "1":
                print(self.current_pymon.inspect())
            elif choice == "2":
                print(self.current_pymon.current_location.inspect())
            elif choice == "3":
                direction = input("Moving to which direction?: ").strip().lower()
                self.current_pymon.move(direction)
            elif choice == "4":
                print("\nExiting game.")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def start_game(self):
        print("Welcome to Pymon World\n")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        print("You started at", self.current_pymon.current_location.get_name())
        self.handle_menu()

if __name__ == '__main__':
    ops = Operation()
    ops.start_game()
