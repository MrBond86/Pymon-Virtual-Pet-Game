# Pymon-Virtual-Pet-Game
Pymon is a virtual pet game where players navigate a map, interact with creatures, and complete challenges using their pet Pymon. The game is designed with an Object-Oriented Programming (OOP) paradigm, focusing on modularity, extensibility, and user interaction.

Players start the game with one Pymon and aim to capture all other Pymons on the map while managing resources like energy and items. The game ends when the player captures all creatures or loses their Pymon.

Features
Core Functionality (PASS Level)
Map Exploration: Navigate interconnected locations using cardinal directions.
Pymon Management: View Pymon's stats (energy, description) and interact with other creatures.
Basic Actions: Move between locations and inspect surroundings.
Enhanced Gameplay (CREDIT Level)
Item Interaction: Pick up items like apples, magic potions, and binoculars, and manage inventory.
Creature Challenges: Engage in "rock, paper, scissors" battles with creatures to capture them.
Advanced Features (DI Level)
Energy Management: Pymon loses energy after multiple moves or battles but can replenish it using items.
Inventory Usability: Use items strategically to aid in battles or explore the map.
Premium Features (HD Level)
Statistics Tracking: Track battle outcomes and save game progress for later continuation.
Admin Features: Add custom locations, creatures, and items to extend gameplay.
Save and Load Game: Maintain game state using external files.
How to Play
Clone or download this repository.
Ensure you have the required files (locations.csv, creatures.csv, items.csv) in the working directory.
Run the game using Python:
bash
Copy code
python pymon_game.py  
Follow the menu prompts to navigate the map, manage Pymon, and complete challenges.
Menu Options
Inspect Pymon: View stats or switch to another Pymon.
Inspect Current Location: Explore surroundings and view connected locations.
Move: Navigate to adjacent locations using cardinal directions.
Pick an Item: Collect useful items from the current location.
View Inventory: Manage and use collected items.
Challenge a Creature: Engage in battles to capture other Pymons.
Generate Stats: View game statistics, including battle outcomes.
Exit: Save progress and quit the game.
File Format Requirements
Locations File (locations.csv)
Format:

Copy code
LocationName, Description, West, North, East, South  
Creatures File (creatures.csv)
Format:

bash
Copy code
CreatureName, Description, Adoptable (yes/no)  
Items File (items.csv)
Format:

bash
Copy code
ItemName, Description, Usability (yes/no)  
Key Technologies
Python: Core programming language.
OOP Principles: Classes, inheritance, encapsulation, and polymorphism.
Data Handling: CSV-based input and output for dynamic game content.
