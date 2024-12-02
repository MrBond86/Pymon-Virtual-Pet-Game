'''
Name-Pramod Bhattarai
SID-S4109474
Level Attempted- HD level (ALL)
'''
'''
Everything is coverd in this level. Some changes was done is csv file so when checking it 
please consider that in location csv header was added as name	description	west	north	east	south
.Admin custom created can be added by csv file is not allowing to overwrite it.Except all the fucntion such as running in terminal
,saving gave and loading the saved game was done succesfully.

'''

import os
import random
import datetime
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
            if isinstance(new_location, Location):  # Check that new_location is a Location instance
                print(f"Moving to {new_location.get_name()} from {self.current_location.get_name()}")
                if self in self.current_location.creatures:
                    self.current_location.creatures.remove(self)
                new_location.add_creature(self)
                self.current_location = new_location
                print(f"Arrived at {self.current_location.get_name()}.")
                
                # Energy deduction logic
                self.moves_count += 1
                if self.moves_count % 2 == 0:
                    self.energy -= 1
                    if self.energy <= 0:
                        print("Energy depleted. Pymon has escaped to a random location!")
                        if not self.handle_energy_depletion():
                            return  # Stop further execution 
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
        if not opponent or not isinstance(opponent, Pymon):
            print("No such Pymon creature to challenge.")
            return

        print(f"\nChallenging {opponent.nickname} in rock, paper, scissors!")
        moves = ['rock', 'paper', 'scissors']
        player_wins = 0
        opponent_wins = 0
        draws = 0

        while player_wins < 2 and opponent_wins < 2 and self.energy > 0:
            player_move = input("Choose rock, paper, or scissors: ").lower()
            opponent_move = random.choice(moves)
            print(f"Your opponent chose {opponent_move}")

            if player_move == opponent_move:
                print("It's a draw.")
                draws += 1
            elif (player_move == 'rock' and opponent_move == 'scissors') or \
                (player_move == 'paper' and opponent_move == 'rock') or \
                (player_move == 'scissors' and opponent_move == 'paper'):
                print("You win this round.")
                player_wins += 1
            else:
                print("You lose this round.")
                opponent_wins += 1
                self.energy -= 1

        # Record the battle outcome
        timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.battle_stats.append({
            'timestamp': timestamp,
            'opponent': opponent.nickname,
            'wins': player_wins,
            'draws': draws,
            'losses': opponent_wins
        })

        if player_wins > opponent_wins:
            print("\nYou won the battle!")
            self.capture_opponent(opponent)
        else:
            print("\nYou lost the battle.")
            self.handle_loss()

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

    def generate_stats(self):
        print(f"\nPymon Nickname: “{self.nickname}”")
        total_wins = total_draws = total_losses = 0
        for i, stat in enumerate(self.battle_stats):
            print(f"Battle {i + 1}, {stat['timestamp']} Opponent: “{stat['opponent']}”, W: {stat['wins']} D: {stat['draws']} L:{stat['losses']}")
            total_wins += stat['wins']
            total_draws += stat['draws']
            total_losses += stat['losses']
        print(f"Total: W: {total_wins} D: {total_draws} L: {total_losses}")
    
    def get_location(self):
        return self.current_location

class Location:
    def __init__(self, name, description=""):
        self.name = name
        self.description = description
        self.doors = {"west": None, "north": None, "east": None, "south": None}
        self.creatures = []
        self.items = []
      

    def add_creature(self, creature):
        if creature not in self.creatures:
            self.creatures.append(creature)

    def add_item(self, item):
        if item not in self.items:
            self.items.append(item)

    def connect(self, direction, another_room):
        self.doors[direction] = another_room
        opposite_directions = {"west": "east", "east": "west", "north": "south", "south": "north"}
        opposite_direction = opposite_directions[direction]
        another_room.doors[opposite_direction] = self

    def get_name(self):
        return self.name

    def inspect(self):
        creature_names = ', '.join([creature.nickname for creature in self.creatures]) or "None"
        item_names = ', '.join([item.name for item in self.items]) or "None"
        return f"\nYou are at {self.name}, {self.description}.\nCreatures present: {creature_names}.\nItems available: {item_names}."


    
    def load_data(self, filepath, data_type):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"No file found at {filepath}")
        with open(filepath, 'r') as file:
            headers = file.readline().strip().split(',')
            for line in file:
                parts = line.strip().split(',')
                if data_type == 'location':
                    self.locations[parts[0]] = Location(*parts[:2])
                elif data_type == 'creature':
                    creature = Creature(parts[0], parts[1])
                    self.creatures.append(creature)
                    if len(parts) > 2 and parts[2].strip().lower() == 'yes' and parts[0] in self.locations:
                        self.locations[parts[0]].creatures.append(creature)
                elif data_type == 'item':
                    if len(parts) > 3 and parts[3].strip().lower() in self.locations:
                        self.locations[parts[3]].items.append(Item(*parts[:3]))


class Record:
    def __init__(self):
        self.locations = {}
        self.creatures = []
        self.pymons = []

    def load_data(self, filepath, data_type):
        if not os.path.exists(filepath):
            return  

        with open(filepath, 'r') as file:
            headers = file.readline().strip().split(',')  # Read headers to determine structure
            data = [line.strip().split(',') for line in file]
            
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
        for loc_name, location in self.locations.items():
            for direction, neighbor_name in location.doors.items():
                if neighbor_name in self.locations:
                    location.connect(direction, self.locations[neighbor_name])

    def _process_creature_data(self, data):
        for entry in data:
            if len(entry) >= 3:
                nickname, description, adoptable = [part.strip() for part in entry[:3]]
                if adoptable.lower() == 'yes':
                    creature = Pymon(nickname, description)
                    self.pymons.append(creature)
                else:
                    creature = Creature(nickname, description)
                self.creatures.append(creature)
                self._assign_creature_to_location(creature, entry[3] if len(entry) > 3 else None)

    def _assign_creature_to_location(self, creature, location_name):
        if location_name and location_name in self.locations:
            self.locations[location_name].add_creature(creature)

    def _process_item_data(self, data):
        for entry in data:
            if len(entry) >= 4:
                name, description, can_pick_up, location_name = [part.strip() for part in entry[:4]]
                item = Item(name, description, can_pick_up.lower() == 'true')
                if location_name in self.locations:
                    self.locations[location_name].add_item(item)

    def get_locations(self):
        return list(self.locations.values())

    def get_pymons(self):
        return self.pymons

    def get_creatures(self):
        return self.creatures




class Item:
    def __init__(self, name, description, can_pick_up):
        self.name = name
        self.description = description
        self.can_pick_up = bool(can_pick_up)

class Operation:
    def __init__(self, record):
        self.record = record
        
        # Ensure that a Pymon is available and set a starting location
        self.current_pymon = next((creature for creature in self.record.creatures if isinstance(creature, Pymon)), None)
        
        if self.current_pymon:
            start_location = self.record.locations.get("Playground")  # Assuming "Playground" is a known location
            if start_location:
                self.current_pymon.current_location = start_location
                print(f"Starting location set: {start_location.get_name()}")
            else:
                print("Error: Starting location not set.")
        else:
            raise ValueError("No Pymon available in the creatures data.")

        self.setup_game_items()

    def setup_game_items(self):
        # Initialize items
        apple = Item("Apple", "A delicious red apple that replenishes energy.", True)
        magic_potion = Item("Magic Potion", "Grants immunity during battle.", True)
        binoculars = Item("Binoculars", "Allows Pymon to see far away places.", True)
        tree = Item("Tree", "Just a decorative item.", False)

        # Place items in specific locations
        playground = self.record.locations.get("Playground")
        beach = self.record.locations.get("Beach")
        school = self.record.locations.get("School")

        if playground:
            playground.add_item(tree)
            playground.add_item(magic_potion)
        
        if beach:
            beach.add_item(apple)
           
        if school:
            school.add_item(binoculars)

    #adding saving games 
    def save_game(self, filename="save2024.csv"):
        """Save the current game state to a custom CSV-like file."""
        try:
            with open(filename, mode='w') as file:
                
                # Save current Pymon location and energy
                file.write(f"Pymon,{self.current_pymon.nickname},{self.current_pymon.get_location().get_name()},{self.current_pymon.energy}\n")
                
                # Save Pymon's inventory
                inventory_items = ','.join(item.name for item in self.current_pymon.inventory)
                file.write(f"Inventory,{inventory_items}\n")
                
                # Save each location and its items
                for loc_name, location in self.record.locations.items():
                    doors = ','.join(f"{k}:{v.name if v else 'None'}" for k, v in location.doors.items())
                    file.write(f"Location,{loc_name},{location.description},{doors}\n")
                    items = ','.join(item.name for item in location.items)
                    file.write(f"Items,{items}\n")
                    
                print("Game progress saved successfully.")
        except Exception as e:
            print(f"Error saving game: {e}")
    
    def load_game(self, filename="save2024.csv"):
        """Load the saved game state from a custom CSV-like file."""
        try:
            with open(filename, mode='r') as file:
                lines = file.readlines()
                
                for line in lines:
                    parts = line.strip().split(',')
                    if parts[0] == "Pymon":
                        nickname, loc_name, energy = parts[1], parts[2], int(parts[3])
                        self.current_pymon.nickname = nickname
                        self.current_pymon.energy = energy
                        self.current_pymon.spawn(self.record.locations[loc_name])
                    
                    elif parts[0] == "Inventory":
                        self.current_pymon.inventory = [Item(item, "", True) for item in parts[1:]]
                    
                    elif parts[0] == "Location":
                        loc_name, description, doors = parts[1], parts[2], parts[3]
                        location = self.record.locations.get(loc_name, Location(loc_name, description))
                        location.doors = {k: self.record.locations.get(v) for k, v in (d.split(':') for d in doors.split(','))}
                    
                    elif parts[0] == "Items":
                        location.items = [Item(item, "", True) for item in parts[1:]]
                        
                print("Game progress loaded successfully.")
        except FileNotFoundError:
            print(f"No saved game file found: {filename}")
        except Exception as e:
            print(f"Error loading game: {e}")
    
    def admin_add_location(self, name, description, west=None, north=None, east=None, south=None):
        """Add a new location as an admin and save to locations.csv."""
        new_location = Location(name, description)
        
        # Update doors for the new location
        new_location.doors = {
            'west': self.record.locations.get(west),
            'north': self.record.locations.get(north),
            'east': self.record.locations.get(east),
            'south': self.record.locations.get(south),
        }
        
        # Save to locations.csv file
        with open("locations.csv", mode="a") as file:
            file.write(f"{name},{description},{west or 'None'},{north or 'None'},{east or 'None'},{south or 'None'}\n")
        
        # Add to record's locations
        self.record.locations[name] = new_location
        print(f"Location '{name}' added successfully.")

    def admin_add_creature(self, nickname, description, adoptable):
        creature_type = Pymon if adoptable.lower() == 'yes' else Creature
        new_creature = creature_type(nickname, description)
        self.record.creatures.append(new_creature)
        # Append to file for persistence
        with open("creatures.csv", 'a') as file:
            file.write(f"{nickname},{description},{adoptable}\n")
        print(f"New creature '{nickname}' added to creatures.csv.")    

    def handle_menu(self):
        while True:
            print("\nPlease issue a command to your Pymon:")
            print("1) Inspect Pymon")
            print("2) Inspect current location")
            print("3) Move")
            print("4) Pick an item")
            print("5) View inventory")
            print("6) Challenge a creature")
            print("7) Generate stats")
            print("8) Save Game")
            print("9) Load Game")
            print("10) Admin: Add Custom Creature")
            print("11) Exit the program")
            choice = input("Your command: ")

            try:
                if choice == "1":
                    print(self.current_pymon.inspect())
                elif choice == "2":
                    location = self.current_pymon.get_location()
                    if location:
                        print(location.inspect())
                    else:
                        print("Your Pymon is not currently in a location.")
                elif choice == "3":
                    direction = input("Moving to which direction? (north, south, east, west): ")
                    self.current_pymon.move(direction)
                elif choice == "4":
                    item_name = input("Enter the item name to pick: ")
                    self.current_pymon.pick_item(item_name)
                elif choice == "5":
                    self.current_pymon.view_inventory()
                elif choice == "6":
                    creature_name = input("Enter the creature name to challenge: ")
                    self.current_pymon.challenge(creature_name)
                elif choice == "7":
                    if self.current_pymon:
                        self.current_pymon.generate_stats()
                    else:
                        print("No Pymon available to generate stats.")
                elif choice == "8":
                    filename = input("Enter filename to save game (default: save2024.csv): ")
                    self.save_game(filename or "save2024.csv")
                elif choice == "9":
                    filename = input("Enter filename to load game (default: save2024.csv): ")
                    self.load_game(filename or "save2024.csv")
                elif choice == "10":
                    nickname = input("Enter creature name: ")
                    description = input("Enter creature description: ")
                    adoptable = input("Is this a Pymon? (yes/no): ")
                    self.admin_add_creature(nickname, description, adoptable)
                elif choice == "11":
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
        '''if starting_location:
            print(f"You started at {starting_location.get_name()}.")
        else:
            print("Error: Starting location not set.")'''
        self.handle_menu()

def parse_line(line):
    return [element.strip() for element in line.split(',')]

def load_data(filepath, type):
    data = []
    try:
        with open(filepath, 'r') as file:
            headers = parse_line(file.readline())
            for line in file:
                data.append(parse_line(line))
    except FileNotFoundError:
        print(f"No file found at {filepath}")
    return data

def main():
    record = Record()
    args = sys.argv[1:]

    # Attempt to load files, defaulting to `creatures.csv` and `items.csv` if they are not provided
    if len(args) == 0:
        print("No files specified. Attempting default files: locations.csv, creatures.csv, items.csv")
        record.load_data('locations.csv', 'location')
        record.load_data('creatures.csv', 'creature')
        record.load_data('items.csv', 'item')
    else:
        # Load the provided files, with fallback to default names if only some are provided
        print(f"Loading location data from {args[0]}...")
        record.load_data(args[0], 'location')
        
        if len(args) >= 2:
            print(f"Loading creature data from {args[1]}...")
            record.load_data(args[1], 'creature')
        else:
            print("Creature file not specified, loading default creatures.csv...")
            record.load_data('creatures.csv', 'creature')
        
        if len(args) >= 3:
            print(f"Loading item data from {args[2]}...")
            record.load_data(args[2], 'item')
        else:
            print("Item file not specified, loading default items.csv...")
            record.load_data('items.csv', 'item')

    # Validate essential data
    if not record.get_locations():
        print("Error: Location data is missing or failed to load. Please provide a valid location file.")
        return
    if not record.get_pymons():
        print("Error: Pymon data is missing in the creatures file. Ensure that the creatures file contains Pymon data.")
        return
    if not record.get_creatures():
        print("Warning: No creatures found in the creature data. Ensure creatures are correctly loaded.")

    # Start the game if all essential data is available
    ops = Operation(record)
    ops.start_game()




if __name__ == '__main__':
    main()
