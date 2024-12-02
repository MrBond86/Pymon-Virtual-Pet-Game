

import random

# Random generator function
def generate_random_number(max_number=1):
    return random.randint(0, max_number)

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
        self.pet_list = []
        self.current_location = None

    def move(self, direction):
        if self.current_location and direction in self.current_location.doors:
            new_location = self.current_location.doors[direction]
            if new_location:
                # Remove this Pymon from the current location's creature list
                if self in self.current_location.creatures:
                    self.current_location.creatures.remove(self)
                # Add this Pymon to the new location's creature list
                new_location.creatures.append(self)
                # Update the Pymon's current location
                self.current_location = new_location
                print(f"\nYou traveled {direction} and arrived at {new_location.get_name()}.")
            else:
                print(f"\nThere is no door to the {direction}. Pymon remains at its current location.")
        else:
            print("\nInvalid direction. Please enter west, north, east, or south.")

    def spawn(self, location):
        location.add_creature(self)
        self.current_location = location

    def inspect(self):
        return f"\nHi Player, my name is {self.nickname}. {self.description} My energy level is {self.energy}/3."

    def pick_item(self, item_name):
        item = next((item for item in self.current_location.items if item.name.lower() == item_name.lower()), None)
        if item and item.can_pick_up:
            self.inventory.append(item)
            self.current_location.items.remove(item)
            print(f"Picked up {item.name}.")
        else:
            print("Item cannot be picked up or does not exist here.")

    def view_inventory(self):
        if self.inventory:
            print("Items in inventory:")
            for item in self.inventory:
                print(f"- {item.name} ({item.description})")
        else:
            print("No items in inventory.")

    def challenge(self, creature_name):
        opponent = next((c for c in self.current_location.creatures if c.nickname == creature_name and isinstance(c, Pymon)), None)
        if not opponent:
            print("\nNo valid opponent here.")
            return

        print(f"\nChallenging {opponent.nickname} in rock, paper, scissors!")
        self.engage_battle(opponent)

    def engage_battle(self, opponent):
        moves = ['rock', 'paper', 'scissors']
        player_wins = 0
        opponent_wins = 0

        while player_wins < 2 and opponent_wins < 2:
            player_move = input("Choose rock, paper, or scissors: ").lower()
            if player_move not in moves:
                print("Invalid choice, please choose 'rock', 'paper', or 'scissors'.")
                continue

            opponent_move = random.choice(moves)
            print(f"Your opponent chose {opponent_move}")

            if player_move == opponent_move:
                print("It's a draw. Repeat the round.")
                continue  # Repeat the round in case of a draw
            elif self.determine_winner(player_move, opponent_move) == 'win':
                player_wins += 1
                print("You win this round.")
            else:
                opponent_wins += 1
                self.energy -= 1
                print("You lose this round.")

            if self.energy <= 0 or opponent_wins == 2:
                print("\nYou have no energy left or you lost two rounds.")
                self.handle_loss(opponent)
                break

            if player_wins == 2:
                print("\nYou won the battle!")
                self.capture_opponent(opponent)
                break

    def determine_winner(self, player, opponent):
        winning_combos = {'rock': 'scissors', 'paper': 'rock', 'scissors': 'paper'}
        return 'win' if winning_combos[player] == opponent else 'lose'

    def capture_opponent(self, opponent):
        print(f"{opponent.nickname} has been captured and added to your pet list.")
        opponent.current_location.creatures.remove(opponent)
        self.pet_list.append(opponent)
        opponent.current_location = None

    def handle_loss(self, opponent):
        print(f"{self.nickname} lost and must retreat.")
        available_locations = [loc for loc in self.current_location.doors.values() if loc]
        if available_locations:
            new_location = random.choice(available_locations)
            self.current_location.creatures.remove(self)
            new_location.add_creature(self)
            self.current_location = new_location
            print(f"{self.nickname} has moved to {self.current_location.get_name()} to recover.")
        if len(self.pet_list) > 0:
            self.current_pymon = self.pet_list.pop(0)  # Assuming the first Pymon in the list becomes the new active Pymon
            print(f"{self.current_pymon.nickname} is now active.")
        else:
            print("Game over. You have no Pymons left.")

    def relinquish_pymon(self):
        # Move to random location logic
        available_doors = [loc for loc in self.current_location.doors.values() if loc]
        if available_doors:
            random_location = random.choice(available_doors)
            print(f"{self.nickname} has been released into the wild and moved to {random_location.get_name()}.")
            self.spawn(random_location)  # Move to new location

class Item:
    def __init__(self, name, description, can_pick_up):
        self.name = name
        self.description = description
        self.can_pick_up = can_pick_up

class Location:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.doors = {}
        self.creatures = []
        self.items = []

    def add_creature(self, creature):
        if creature not in self.creatures:
            self.creatures.append(creature)
            creature.current_location = self   

    def add_item(self, item):
        self.items.append(item)

    def connect(self, direction, room):
        self.doors[direction] = room
        opposite = {'north': 'south', 'south': 'north', 'east': 'west', 'west': 'east'}
        room.doors[opposite[direction]] = self

    def get_name(self):
        return self.name

    def inspect(self):
        creature_names = ', '.join(creature.nickname for creature in self.creatures if creature is not None) or "None"
        item_names = ', '.join(item.name for item in self.items if item is not None) or "None"
        return f"\nYou are at {self.name}, {self.description}.\nCreatures present: {creature_names}.\nItems available: {item_names}."


class Record:
    def __init__(self):
        self.locations = {
            "Playground": Location("Playground", "An outdoor playground with slides and swings."),
            "Beach": Location("Beach", "A sandy beach with a beautiful ocean view."),
            "School": Location("School", "An educational institution with classrooms.")
        }
        self.creatures = []

    def setup_creatures(self):
        # Manually place creatures at specific locations
        kitimon = Pymon("Kitimon", "A large blue and white Pymon with yellow fangs")
        marimon = Pymon("Marimon", "A medium red and yellow Pymon with a cute round face")
        sheep = Creature("Sheep", "A small fluffy animal with interesting curly white fur")

        self.locations["Playground"].add_creature(kitimon)
        self.locations["Beach"].add_creature(sheep)
        self.locations["School"].add_creature(marimon)

        self.creatures.extend([kitimon, sheep, marimon])

        
    def import_creatures(self, filename):
        with open(filename, 'r') as file:
            headers = file.readline().strip().split(',')
            for line in file:
                data = dict(zip(headers, line.strip().split(',')))
                if data['type'].lower() == 'pymon':  # Assuming there is a 'type' column in CSV
                    creature = Pymon(data['nickname'].strip(), data['description'].strip())
                    location = self.locations.get(data['location'].strip())
                    if location:
                        location.add_creature(creature)
                        self.creatures.append(creature)
                else:
                    creature = Creature(data['nickname'].strip(), data['description'].strip())
                    location = self.locations.get(data['location'].strip())
                    if location:
                        location.add_creature(creature)

    def import_data(self, filename, type='location'):
        with open(filename, 'r') as file:
            headers = file.readline().strip().split(',')
            for line in file:
                data = dict(zip(headers, line.strip().split(',')))
                if type == 'location':
                    self.process_location_data(data)
                elif type == 'creature':
                    self.process_creature_data(data)

    def process_location_data(self, data):
        name = data['name'].strip()
        description = data.get('description', 'No description provided').strip()
        location = Location(name, description)
        self.locations[name] = location
        # Setting up connections based on the CSV input (requires locations to be predefined)
        for direction in ['west', 'north', 'east', 'south']:
            neighbor_name = data.get(direction, '').strip()
            if neighbor_name and neighbor_name in self.locations:
                location.connect(direction, self.locations[neighbor_name])

    def process_creature_data(self, data):
        nickname = data['nickname'].strip()
        description = data['description'].strip()
        adoptable = data['adoptable'].strip().lower() == 'yes'

        # Assuming a default location for simplicity; you'd set this based on another column in your CSV if available
        location_name = "Playground"  # Default to Playground if not specified in CSV
        location = self.locations.get(location_name, None)

        if adoptable:
            creature = Pymon(nickname, description)
        else:
            creature = Creature(nickname, description)

        if location:
            location.add_creature(creature)
            self.creatures.append(creature)
        else:
            print(f"Location {location_name} not found for creature {nickname}")



class Operation:
    def __init__(self):
        self.record = Record()
        self.record.import_data('locations.csv', 'location')
        self.record.import_data('creatures.csv', 'creature')
        
        self.setup_game_items()
        self.current_pymon = None
        self.initialize_game_state()  # Ensure this method is properly defined.

    def setup_game_items(self):
        # Example setup of items, hardcoded for simplicity
        apple = Item("Apple", "A delicious red apple that replenishes energy.", True)
        magic_potion = Item("Magic Potion", "Grants immunity during battle.", True)
        binoculars = Item("Binoculars", "Allows Pymon to see far away places.", True)
        tree = Item("Tree", "Just a decorative item.", False)

        # Assuming locations are stored in the record
        playground = self.record.locations.get("Playground")
        beach = self.record.locations.get("Beach")
        school = self.record.locations.get("School")

        playground.add_item(tree)
        playground.add_item(magic_potion)
        beach.add_item(apple)
        school.add_item(binoculars)

    def initialize_game_state(self):
        """
        Initializes the game state by setting the starting location for the first Pymon found in the record.
        """
        try:
            # Attempt to find the first Pymon in the list of creatures
            self.current_pymon = next(creature for creature in self.record.creatures if isinstance(creature, Pymon))
        except StopIteration:
            # Handle the case where no Pymons are available
            raise ValueError("No Pymon available in the creatures data.")

        # Get the starting location for the Pymon, defaulting to 'Playground' if not specified
        start_location = self.record.locations.get("Playground")
        if start_location:
            # If the location exists, spawn the Pymon there
            self.current_pymon.spawn(start_location)
            print(f"Game initialized: {self.current_pymon.nickname} has spawned at {start_location.name}.")
        else:
            # Fallback scenario if 'Playground' is not found
            print("Error: Starting location 'Playground' not set or not found.")
            # You could set a default location if none is found
            self.handle_no_start_location
            
    def handle_no_start_location(self):
        """
        Handles scenarios where no valid starting location is found by creating a default location.
        """
        print("Creating a default start location.")
        default_location = Location("Default Area", "An automatically created safe area.")
        self.record.locations['Default Area'] = default_location
        self.current_pymon.spawn(default_location)
        print(f"Game initialized in default location: {self.current_pymon.nickname} is at {default_location.name}.")

    def handle_menu(self):
        # Game interaction loop
        while True:
            print("\nPlease issue a command to your Pymon:")
            print("1) Inspect Pymon")
            print("2) Inspect current location")
            print("3) Move")
            print("4) Pick an item")
            print("5) View inventory")
            print("6) Challenge a creature")
            print("7) Exit the program")
            choice = input("Your command: ")

            if choice == "1":
                print(self.current_pymon.inspect())
            elif choice == "2":
                if self.current_pymon.current_location is not None:
                    print(self.current_pymon.current_location.inspect())
                else:
                    print("Your Pymon is not in a valid location.")
                    continue
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
                print("\nExiting game.")
                break
            else:
                print("\nInvalid choice. Please try again.")

    def start_game(self):
        print("Welcome to Pymon World\n")
        self.handle_menu()

if __name__ == '__main__':
    ops = Operation()
    ops.start_game()