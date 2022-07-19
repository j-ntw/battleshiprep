# battleshiprep
 Repository for 1D game battleships. Note: the main branch is unfinished. Play a simpler, finished version in player_vs_cpu branch!

## Table of contents
* [General info](#general-info)
* [Description](#description)
* [References](#references)
* [Setup](#setup)
* [Documentation](#documentation)

## General info
This project is a Battleship game meant to be played by a single player versus CPU.

A PDF of the rules can be found here: https://themindcafe.com.sg/wp-content/uploads/1970/01/Battleship.pdf

### Authors:

Joshua Ng (1005285)

Joanne Ng (1005639)

Lau Wuarn Hong (1005313)

Irvine Novian (1005491)


Class 20F02, Team 08 

## Description
The objective of this game is to be the first to sink all of the opponent's ships. In this version of the game, there is Setup Phase and War Phase.

In Setup Phase, the ships are placed by first selecting the location of the ship's stern (the back of the ship), then selecting the direction the ship will face.

Once both the player and the CPU have set up their ships, War Phase begins. They take turns guessing the locations of the opponent's ships. 

The description of the ships are as follows:

Carrier : 5 holes

Battleship: 4 holes

Cruiser: 3 holes

Submarine: 3 holes

Destroyer : 2 holes

### Feature(s)

#### Targetting Algorithm 
The CPU has a simple targetting algorithm: when it has no targets, it will shoot a random target. When it hits a ship, it will target the North, South, East and West tiles of the target and exhaust the targets. If one of the targets results in a hit, the CPU will follow that direction until it misses, then return to random targets. If all of the targets miss, it will also return to random targets.
The CPU is not smart enough to aim for open areas, revisit a bombed area or stop bombing if a longer ship is already destroyed (e.g. if the Carrier is already destroyed and it has shot another ship 4 times, it will still try to shoot the same ship a 5th time.)

## References
This project is created with the following technologies:
* Python 3.8.5
* random
* matplotlib.pyplot
* matplotlib.patches

Starter code for board setup adapted from Stack Exchange answer for GO board setup:

https://stackoverflow.com/questions/24563513/drawing-a-go-board-with-matplotlib
	
## Setup
To run this project, run battleship_game.py alone. 

## Documentation
Note: Points in this code are strings where the first char is a single alphabet from "ABCDEFGHJK" and the second char is a single digit.

### Global Variables:

#### all_ships_dict 

Dictionary of the 5 ships as keys and their sizes as values.

#### shot_list_P1

Empty list used to record the shots that the Player takes.

#### shot_list_CPU

Empty list used to record the shots that the CPU takes.

#### ls_all_ships_points_P1

Empty list used to record the ship coordinates of the Player. Used to check for overlap of ship coordinates. Never modified after creation.

#### ls_all_ships_points_CPU

Empty list used to record the ship coordinates of the CPU. Used to check for overlap of ship coordinates. Never modified after creation.

#### drawing_order

Variable used in draw_rectangle_setup and remove_rectangle_setup to determine zorder of matplotlib patches. 

### Board Setup

The board is created as a figure in matplotlib and has two subplots, ax_setup and ax_war, which are displayed at all times and vertically stacked.
ax_setup, labelled 'Your Board', displays the ships on the Player's board. ax_war, labelled 'CPU's Board', displays the Player's hits and misses on the CPU's board.
The subplots are displayed as grids with x-axis of range 'A' to 'K' (excluding 'I') and y-axis of range 0 to 9.

### Drawing Patches

#### draw_rectangle_setup(point)

Takes in a point. Draws a black square on the board. Used during P1 Setup to first display the stern, then the whole ship, at the point as decided by the Player's input.

#### remove_rectangle_setup(point)

Takes in a point. Draws a square the colour of the board's background over any existing squares at the specified point. Used during P1 Setup to visually indicate that the Player has removed a ship's stern from the specified point.

#### draw_rectangle_war(point, colour)

Takes in a point and colour. Draws either a grey or red square on the board. Used during War Phase to display the Player's hits (red) and misses (grey) on the CPU's board, at the points as decided by the Player's input.

#### draw_rectangle_cpu(point)

Takes in a point. Draws a red square over the existing black square at the specified point. Used during War Phase to display the CPU's hits on the Player's board.

### P1 Setup

#### check_valid_point_P1(point, thing)

Returns a Boolean. False if point is in invalid format or point is out of the board's boundaries, True if valid

#### place_stern_P1(ship_name, ship_length)

Takes ship name and size parameters. Asks for input point from Player using the parameters and draws a black square if point is valid.

#### generate_ship_sections_P1(stern, ship_name, size)

Takes a stern point, ship name and size parameters. Generates a list of ship points based on a direction input by the player. If the player types 'X', the function returns 'X'.

If an 'I' tile is generated, the function removes it and adds an additional tile in the chosen direction using a try exception loop. The function returns the list of ship points.

#### check_ship_sections_P1(ship_name, ls_points)

Takes ship name and list of ship points parameters. Each point in the list of ship points is checked so that it is within the board's boundaries and doesn't overlap with the points of a ship already placed on the board.

Returns True if it fulfils the stated conditions, False if otherwise.

#### place_ship_P1(ship_name)

Takes ship name as a parameter. References the global variables all_ships_dict to get the ship's size and ls_all__ships_points_P1 to check and update it. 

This function integrates place_stern_P1, generate_ships_sections_P1 and check_ship_sections_P1 in a while loop, such that the Player is asked for the stern location, direction of the ship and is informed if the direction picked is illegal.

The Player has the option to re-select the stern location by typing 'X' instead of a direction. This is useful in the event the Player picks a stern location blocked by other ships and the board boundaries.

If check_ship_sections_P1 returns True, the ships points are stored in ls_all_ships_points_P1 and black squares are drawn on the board for each of the ship's points. 

Returns a list of the ship's name and a nested list of the ship's points.

### CPU setup

#### check_valid_point_CPU(point)

Takes in point as parameter. Returns True if point is within the board, False if otherwise.

#### generate_random_point()

Takes in no parameters. random library is required for this function. Returns a random point on the board in the form "A0".

#### generate_ship_sections_CPU(stern, ship_name, size, valid_dir_ls)

Takes in stern as a point, ship name, ship size and a list of valid directions. From the stern, this function generates the more ship sections according to a direction randomly picked from the list of valid directions. 

Different lists of valid directions can be passed to the function to represent fewer choices as the CPU removes invalid directions from the list.

Returns a list with a list of ship points in the zeroth index and selected direction in the first index.

#### check_ship_sections_CPU(ship_name, ls_points)

Takes ship name and list of ship points as parameters. Iterates through each point. If any point is out of board (checked via check_valid_point_CPU) or any point exists in the 

#### place_ship_CPU(ship_name)

Takes ship name as a parameter. References the global variables all_ships_dict to get the ship's size and ls_all_ships_points_CPU to check and update it. valid_dir_ls is also created internally as an empty list.

This function integrates generate_random_point(), generate_ships_sections_CPU() and check_ship_sections_CPU() in a while loop, such that in the first iteration, the CPU randomly generates a stern and a direction \[N/S/E/W\], generates the ship points and checks if they are valid. If they are not, the selected direction is removed from the valid_dir_ls. This continues until valid ship points are found or the valid_dir_ls is exhausted, whichever is first. 

If the valid_dir_ls becomes an empty list again, the CPU picks a new random stern location as the previous stern location is not viable.

Once valid ship points are generated, they are appended to ls_all_ships_points_CPU and black squares are drawn on the board for each of the ship's points. 

Returns a list of the ship's name and a nested list of the ship's points.


### War Phase: Player 1

#### check_score(enemy_ship_dict)

Takes in an enemy ship's dictionary. For example, Player score is computed using CPU dictionary and vice versa. 

score is intialised as 0. For every empty list in the dictionary, 1 is added to the score. Returns score.

#### attack()

Takes in no parameters. References the global variable shot_list_P1.

This function asks the Player for attack coordinates. If the shot is invalid or if the shot has been taken before, the function prints a statement to inform the player and prompts them for new coordinates.

Once a valid shot is captured, it is appended to shot_list_P1. Returns shot.

#### check_hit(shot, enemy_ship_dict, enemy_ls_all_ships_points)

Takes in shot, an enemy's ship dictionary and an enemy's list of all ship points. 

If the shot is not within the enemy's list of all ship points, the Player is informed they missed the CPU's ships along with a visual indicator. A grey rectangle is drawn over the shot coordinates on the CPU board.

Otherwise, the Player is informed they successfully hit a ship and a red rectangle is drawn over the shot coordinates on the CPU board. By looping through enemy_ship_dict, the point is removed from the relevant list of ship points.

Returns nothing.

### War Phase: CPU

#### attack_CPU_random()

Takes no parameters. Generates a random shot. If the shot is previously shot, it generates a random shot. Returns shot.

#### generate_add_shot()

Takes a shot and a list of valid directions. This function generates additional strike locations as a dictionary with shot and direction as key and value respectively.

add_shot_dict is initialised as an empty dictionary and ls_to_del as an empty list. For each direction in the list of valid directions, the corresponding point is generated, offset 1 tile from the given shot.

For each generated point, if it is invalid (as checked by check_valid_point_CPU() )or already in shot_list_CPU, it is deleted from add_shot_dict. 

Returns add_shot_dict

#### check_hit_CPU(shot, enemy_ship_dict, enemy_ls_all_ships_points, target_dict)

Takes a shot, an enemy's ship dictionary, an enemy's list of all ship points and a target dictionary.

This is the CPU's attack decision tree. 

If there are targets in the target dictionary, the if loop is activated.

If the CPU misses, it will remove the point from the target_dict and pick another random point. It will do so until the target_dict is empty, after which the CPU will take a random shot.

If the target dictionary is empty the else loop activates. 

If shot is not in the enemy's list of ship points, it will inform the player of the miss.

If it is a hit, a red rectangle is drawn over the shot coordinates on the CPU board. By looping through enemy_ship_dict, the point is removed from the relevant list of ship points.

### Main Function

The main function takes no parameters and returns nothing. plt.draw() is called to draw the board. P1_ship_dict and CPU_ship_dict are initialised as empty dictionaries, ready to be filled up in the Setup Phase. game_not_over is set to True to start the while loop in War Phase and round_num is initialised as 0.

In Setup Phase, main() iterates through all_ships_dict to generate ships for the player and the CPU using place_ship_P1() and place_ship_CPU respectively.

In War Phase, the starting player is randomly chosen. While the game is not over, if it is the Player's turn , he will be prompted to attack. His shot is checked and the boards are updated accordingly. His turn ends as player_turn is set to False.

If it is the CPU's turn the CPU runs through its decision tree and updates the target_dict accordingly. the board is updated and the CPU_shot_list is updated here to avoid repetition in the decision tree. At the end of CPU's turn, player_turn is set to True.

At the end of either the CPU or Player's turn, main() checks the CPU_score with check_score(). If the CPU_score is 5, it has destroyed all the player's ships and game_not_over is set to False, breaking the while loop and ending the game. If P1_score is 5, the player has destroyed all the CPU's ships and game_not_over is set to False, breaking the while loop and ending the game. Otherwise, the game continues until a win/lose condition is fufilled.
