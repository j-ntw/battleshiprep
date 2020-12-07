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
Starter code for board setup adapted from Stack Exchange answer for GO board setup: https://stackoverflow.com/questions/24563513/drawing-a-go-board-with-matplotlib
	
## Setup
To run this project, run battleshipmain_vs_cpu.py alone. 

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

