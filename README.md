# battleshiprep
 Repository for 1D game battleships

## Table of contents
* [General info](#general-info)
* [Description](#description)
* [References](#references)
* [Setup](#setup)
* [Documentation](#documentation)

## General info
This project is a Battleship game meant to be played by a single player versus CPU. A PDF of the rules can be found here: https://themindcafe.com.sg/wp-content/uploads/1970/01/Battleship.pdf

## Description
The objective of this game is to be the first to sink all of the opponent's ships. In this version of the game, there is Setup Phase and War Phase.

In Setup Phase, the ships are placed by first selecting the location of the ship's stern (the back of the ship), then selecting the direction the ship will face.

Once both the player and the CPU have set up their ships, War Phase begins. They take turns guessing the locations of the opponent's ships. 

The CPU has a simple targetting algorithm: when it has no targets, it will shoot a random target. When it hits a ship, it will target the North, South, East and West tiles of the target and exhaust the targets. If one of the targets results in a hit, the CPU will follow that direction until it misses, then return to random targets. If all of the targets miss, it will also return to random targets.
The CPU is not smart enough to aim for open areas, revisit a bombed area or stop bombing if a longer ship is already destroyed (e.g. if the Carrier is already destroyed and it has shot another ship 4 times, it will still try to shoot the same ship a 5th time.)

The description of the ships are as follows:

Carrier : 5 holes

Battleship: 4 holes

Cruiser: 3 holes

Submarine: 3 holes

Destroyer : 2 holes
	
## References
This project is created with the following technologies:
* Python 3.8.5
* random
* matplotlib.pyplot
* matplotlib.patches

draw rectangle

Starter code for board setup adapted from Stack Exchange answer for GO board setup:

https://stackoverflow.com/questions/24563513/drawing-a-go-board-with-matplotlib
	
## Setup
To run this project, run joanne_battleshipmain_vs_cpu.py alone. 

There are 2 phases: 
1. Setup Phase
2. War Phase

Setup Phase:
No overlap

Once all done, CPU will write ship positions to dict

Initialise the board and start War Phase

War Phase:
This is an infinite loop till a win or lose condition is fulfilled

Player 1 Attack:
Player 1 calls a shot e.g."A1"
CPU checks if miss or hit and updates the board. (clear all output)
If hit and not in list of known enemy ships:
    add to list of known enemy ships

CPU checks if Player 2 has any surviving ships.
If Player 2 has no remaining ships
    Player 1 wins
else
    Player 1 ends turn, Player 2 turn starts

CPU Attack:
CPU calls a random shot from list of available points.
CPU checks if miss or hit and updates the board. (clear all output)
CPU checks if Player 1 has any surviving ships.
If Player 1 has no remaining ships
    Player 2 wins
else
    Player 2 ends turn, Player 1 turn starts\
    
## Documentation
Note: Points in this code are strings where the first char is a single alphabet from "ABCDEFGHJK" and the second char is a single digit.

### Global Variables:

#### all_ships_dict 

Dictionary of the 5 ships as keys and their sizes as values

#### shot_list_P1

Empty list used to record the shots that Player 1 takes

#### shot_list_CPU

Empty list used to record the shots that CPU takes

#### ls_all_ships_points_P1

Empty list used to record the ship coordinates of Player 1. Used to check for overlap of ship coordinates. Never modified after creation.

#### ls_all_ships_points_CPU

Empty list used to record the ship coordinates of CPU Used to check for overlap of ship coordinates. Never modified after creation.

#### matplot lib here



#### draw_rectangle_setup(point)

Takes in a point variable and draws a black square on the board

#### draw_rectangle_war(point, colour)

Takes a point and colour. Draws either a grey or red square on the board

#### draw_rectangle_cpu(point)

Takes a point. Draws a red square over a black square (existing ship coordinates) to register a hit by CPU

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

Takes in point as parameter. Returns True if point is within the board, False if otherwise

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

#### War Phase: Player 1
