'''
All the requiement are met in  this level .
'''

import os
import random
import sys


# Random generator function
def generate_random_number(max_number=1):
    return random.randint(0, max_number)

class InvalidDirectionException(Exception):
    pass

class InvalidInputFileFormat(Exception):
    pass


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
    def __init__(self, nickname, description, energy=3):
        super().__init__(nickname, description)
        self.energy = energy
        self.inventory = []
        self.immunity = False
        self.pet_list = []
        self.current_location = None
        self.moves_count = 0
        self.battle_stats = []

    def move(self, direction):
        if self.current_location and direction in self.current_location.doors:
            new_location = self.current_location.doors[direction]
            if new_location:
                self.current_location.creatures.remove(self)
                new_location.add_creature(self)
                self.current_location = new_location
                print(f"\nYou traveled {direction} and arrived at {self.current_location.get_name()}.")
                
                self.moves_count += 1
                if self.moves_count % 2 == 0:
                    self.energy -= 1
                    if self.energy <= 0:
                        print("Energy depleted. Pymon has escaped to a random location!")
                        if not self.handle_energy_depletion():
                            return  # Stop further execution if game is over
                    else:
                        print(f"Energy decreased by 1, current energy: {self.energy}")
            else:
                raise InvalidDirectionException(f"No location in the '{direction}' direction from {self.current_location.get_name()}.")
        else:
            raise InvalidDirectionException("Invalid direction or missing current location.")

    def use_item(self, item_name):
        item = next((item for item in self.inventory if item.name == item_name), None)
        if item:
            if item.name == "Apple" and self.energy < 3:
                self.energy += 1
                print("Apple eaten. Energy increased to", self.energy)
            elif item.name == "Magic Potion":
                self.immunity = True
                print("Magic potion used. You have temporary immunity.")
                
            elif item.name == "Binoculars":
                print("Using binoculars to inspect surroundings...")
                direction = input("Which direction would you like to inspect? (current, west, north, east, south): ").lower()
                self.inspect_with_binoculars(direction)
            self.inventory.remove(item)
        else:
            print("Item not found or cannot be used.")

    def inspect_with_binoculars(self, direction):
        if direction == "current":
            # Provide details about the current location and visible items and creatures
            creatures = ', '.join([creature.nickname for creature in self.current_location.creatures])
            items = ', '.join([item.name for item in self.current_location.items])
            print(f"Current location: {self.current_location.name}, visible creatures: {creatures}, items: {items}")
        elif direction in ["west", "north", "east", "south"]:
            # Check if there is a location in the specified direction
            adjacent_location = self.current_location.doors.get(direction)
            if adjacent_location:
                # Provide details about the location in the specified direction
                creatures = ', '.join([creature.nickname for creature in adjacent_location.creatures])
                items = ', '.join([item.name for item in adjacent_location.items])
                if creatures or items:
                    print(f"In the {direction}, there is {adjacent_location.name} with creatures: {creatures} and items: {items}")
                else:
                    print(f"In the {direction}, there seems to be {adjacent_location.name} with no visible creatures or items.")
            else:
                print(f"This direction leads nowhere.")
        else:
            print("Invalid direction.")

    def spawn(self, loc):
        loc.add_creature(self)
        self.current_location = loc

    def inspect(self):
        return f"\nHi Player, my name is {self.nickname}. {self.description} My energy level is {self.energy}/3. What can I do to help you?"

    def pick_item(self, item_name):
        current_location = self.current_location
        if current_location:
            # Normalize input to handle case insensitivity
            item_name = item_name.strip().lower()
            item = next((item for item in current_location.items if item.name.lower() == item_name), None)
            if item and item.can_pick_up:
                self.inventory.append(item)
                current_location.items.remove(item)
                print(f"Picked up {item.name}.")
            else:
                # Provide feedback about what items are available if the desired item isn't found
                available_items = ', '.join([item.name for item in current_location.items if item.can_pick_up])
                print(f"Item '{item_name}' cannot be picked up or does not exist here. Available items: {available_items}")
        else:
            print("Pymon is not in a valid location to pick up items.")

    def view_inventory(self):
        if self.inventory:
            print("Items in inventory:")
            for item in self.inventory:
                print(item.name)
        else:
            print("No items in inventory.")

    def challenge(self, creature_name):
        opponent = next((c for c in self.current_location.creatures if c.nickname == creature_name), None)
        if not opponent:
            print("No suitable opponent found.")
            return

        print(f"Challenging {opponent.nickname} in rock, paper, scissors!")
        moves = ['rock', 'paper', 'scissors']
        player_wins = 0
        opponent_wins = 0

        while player_wins < 2 and opponent_wins < 2 and (self.energy > 0 or self.immunity):
            player_move = input("Choose rock, paper, or scissors: ").lower()
            opponent_move = random.choice(moves)
            print(f"Your opponent chose {opponent_move}")

            if player_move == opponent_move:
                print("It's a draw.")
            elif self.win_condition(player_move, opponent_move):
                print("You win this round.")
                player_wins += 1
            else:
                print("You lose this round.")
                opponent_wins += 1
                if not self.immunity:
                    self.energy -= 1

            if self.energy <= 0 and not self.immunity:
                print("No energy left, you lost the battle.")
                break

        if player_wins > opponent_wins:
            print("You won the battle!")
        else:
            print("You lost the battle.")
            if self.immunity:
                print("Your magic potion saved you from losing energy this battle.")
            self.immunity = False  # Reset immunity status after the battle

    def win_condition(self, player_move, opponent_move):
        return ((player_move == 'rock' and opponent_move == 'scissors') or
                (player_move == 'paper' and opponent_move == 'rock') or
                (player_move == 'scissors' and opponent_move == 'paper'))

    def capture_opponent(self, opponent):
        print(f"{opponent.nickname} has been added to your Pymon collection.")
        self.current_location.creatures.remove(opponent)  # Remove from current location
        self.pet_list.append(opponent)  # Add opponent to the player's collection
        opponent.set_location(None) 

    def handle_loss(self):
        # Move Pymon to random location if available locations exist
        self.relinquish_pymon()

    def relinquish_pymon(self):
        # Move to random location logic
        available_doors = [loc for loc in self.current_location.doors.values() if loc]
        if available_doors:
            random_location = random.choice(available_doors)
            print(f"{self.nickname} has been released into the wild and moved to {random_location.get_name()}.")
            self.spawn(random_location)  # Move to new location

    def handle_energy_depletion(self):
        if len(self.pet_list) > 0:
            # Switch to another Pymon if available
            self.current_pymon = self.pet_list.pop(0)
            print("Switched to another Pymon due to energy depletion.")
            return True
        else:
            # Game over scenario
            print("Game over. No more Pymons left to play.")
            return False


class Location:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.doors = {"west": None, "north": None, "east": None, "south": None}
        self.creatures = []
        self.items = []

    def add_creature(self, creature):
        self.creatures.append(creature)
        creature.set_location(self)

    def add_item(self, item):
        if item.can_pick_up:
            self.items.append(item)

    def connect(self, direction, another_room):
        self.doors[direction] = another_room
        opposite_directions = {"west": "east", "east": "west", "north": "south", "south": "north"}
        opposite_direction = opposite_directions[direction]
        another_room.doors[opposite_direction] = self

    def get_name(self):
        return self.name

    def inspect(self):
        creature_names = ', '.join({creature.nickname for creature in self.creatures}) or "None"
        item_names = ', '.join([item.name for item in self.items]) or "None"
        return f"\nYou are at {self.name}, {self.description}.\nCreatures present: {creature_names}.\nItems available: {item_names}."
    
class Record:
    def __init__(self, default_location="Playground"):
        self.locations = {}
        self.creatures = []
        self.pymons = []

    def load_data(self, filename, data_type):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"File not found: {filename}")

        data = []
        with open(filename, 'r') as file:
            headers = file.readline().strip().split(',')
            for line in file:
                data.append(line.strip().split(','))

        if data_type == 'location':
            self._process_location_data(data)
        elif data_type == 'creature':
            self._process_creature_data(data)
        elif data_type == 'item':
            self._process_item_data(data)

    def _process_location_data(self, data):
        for entry in data:
            if len(entry) >= 6:
                name, description, west, north, east, south = [part.strip() for part in entry[:6]]
                location = Location(name, description)
                self.locations[name] = location
                location.doors = {
                    'west': west if west != 'None' else None,
                    'north': north if north != 'None' else None,
                    'east': east if east != 'None' else None,
                    'south': south if south != 'None' else None
                }
        self._resolve_location_connections()

    def _resolve_location_connections(self):
        """
        Connect locations based on the directions provided.
        """
        for loc_name, location in self.locations.items():
            for direction, neighbor_name in location.doors.items():
                if neighbor_name in self.locations:
                    location.connect(direction, self.locations[neighbor_name])

    def _process_item_data(self, data):
        for entry in data:
            if len(entry) >= 4:
                name, description, can_pick_up, location_name = [part.strip() for part in entry[:4]]
                item = Item(name, description, can_pick_up.lower() == 'true')
                if location_name in self.locations:
                    self.locations[location_name].add_item(item)

    def _process_creature_data(self, data):
        for entry in data:
            nickname, description, adoptable = entry[:3]
            adoptable = entry[2].strip().lower() == 'yes'
            creature = Pymon(nickname, description) if adoptable else Creature(nickname, description)
            self.creatures.append(creature)

            if adoptable and "Playground" in self.locations:
                self.locations["Playground"].add_creature(creature)
            elif not adoptable and "Beach" in self.locations:
                self.locations["Beach"].add_creature(creature)


    def get_locations(self):
        return list(self.locations.values())

    def get_pymons(self):
        return [creature for creature in self.creatures if isinstance(creature, Pymon)]

    def get_creatures(self):
        return self.creatures

class Item:
    def __init__(self, name, description, can_pick_up):
        self.name = name
        self.description = description
        self.can_pick_up = can_pick_up

class Operation:
    def __init__(self):
        self.record = Record()
        
        # Loading data from default CSV files
        self.record.load_data('locations.csv', 'location')
        self.record.load_data('creatures.csv', 'creature')
        self.record.load_data('items.csv', 'item')
        
        self.current_pymon = next((creature for creature in self.record.creatures if isinstance(creature, Pymon)), None)

        if self.current_pymon:
            start_location = self.record.locations.get("Playground")
            if start_location:
                self.current_pymon.spawn(start_location)
            else:
                print("Error: Starting location not set.")
        else:
            raise ValueError("No Pymon available in the creatures data.")

        self.setup_game_items()

    def setup_game_items(self):
        apple = Item("Apple", "A delicious red apple that replenishes energy.", True)
        magic_potion = Item("Magic Potion", "Grants immunity during battle.", True)
        binoculars = Item("Binoculars", "Allows Pymon to see far away places.", True)

        playground = self.record.locations.get("Playground")
        beach = self.record.locations.get("Beach")
        school = self.record.locations.get("School")

        if playground:
            playground.add_item(apple)
            playground.add_item(magic_potion)
        if beach:
            beach.add_item(Item("Tree", "A decorative tree", False))
        if school:
            school.add_item(binoculars)
            
    def handle_menu(self):
        while True:
            print("\nPlease issue a command to your Pymon:")
            print("1) Inspect Pymon")
            print("2) Inspect current location")
            print("3) Move")
            print("4) Pick an item")
            print("5) View inventory (a) Select item to use")
            print("6) Challenge a creature")
            print("7) Generate stats")
            print("8) Exit the program")
            choice = input("Your command: ")

            try:
                if choice == "1":
                    print(self.current_pymon.inspect())
                elif choice == "2":
                    print(self.current_pymon.get_location().inspect())
                elif choice == "3":
                    direction = input("Moving to which direction? (north, south, east, west): ")
                    self.current_pymon.move(direction)
                elif choice == "4":
                    item_name = input("Enter the item name to pick: ")
                    self.current_pymon.pick_item(item_name)
                elif choice == "5":
                    self.current_pymon.view_inventory()
                    sub_choice = input("Would you like to use an item? (a) Select item to use, or press Enter to skip: ")
                    if sub_choice.lower() == "a":
                        item_name = input("Enter the item name to use: ")
                        self.current_pymon.use_item(item_name)
                elif choice == "6":
                    creature_name = input("Enter the creature name to challenge: ")
                    self.current_pymon.challenge(creature_name)
                elif choice == "7":
                    self.generate_stats()
                elif choice == "8":
                    print("\nExiting game.")
                    break
                else:
                    print("\nInvalid choice. Please try again.")
            except InvalidDirectionException as e:
                print(e)
            except Exception as e:
                print("An unexpected error occurred:", str(e))

    def start_game(self):
        print("Welcome to Pymon World\n")
        print("It's just you and your loyal Pymon roaming around to find more Pymons to capture and adopt.\n")
        starting_location = self.current_pymon.get_location()
        if starting_location:
            print(f"You started at {starting_location.get_name()}.")
        else:
            print("Error: Starting location not set.")
        self.handle_menu()
def main():
    record = Record()
    args = sys.argv[1:]  # Get command-line arguments

    # Attempt to load files, defaulting to `locations.csv`, `creatures.csv`, and `items.csv`
    if not args:
        print("No files specified. Attempting default files: locations.csv, creatures.csv, items.csv")
        record.load_data('locations.csv', 'location')
        record.load_data('creatures.csv', 'creature')
        record.load_data('items.csv', 'item')
    else:
        # Load files from provided arguments
        if len(args) >= 1:
            record.load_data(args[0], 'location')
        if len(args) >= 2:
            record.load_data(args[1], 'creature')
        if len(args) >= 3:
            record.load_data(args[2], 'item')

    if not record.get_pymons():
        raise ValueError("No Pymon data available after loading. Please check the creature data.")

    ops = Operation()
    ops.start_game()

if __name__ == '__main__':
    main()
