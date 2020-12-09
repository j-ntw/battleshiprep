# battleshiprep
 Repository for 1D game battleships. Note: the main branch is unfinished. Play a simpler, finished version in player_vs_cpu branch!

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a Battleship game meant to be played on 2 computers connected via the internet.
	
## Technologies
Project is created with:
* Python 3.8.5
* Pyrebase
* matplotlib
	
## Setup
To run this project, run battleshipmain.py along with the corresponding modules in the same folder.

There are 3 phases: 
1. Matching Phase
2. Setup Phase
3. War Phase

Matching Phase:
Player enter
Players will enter their names -done
CPU generate unique id, check if another player has joined the game and capture their id
CPU will read Player 2 name using P2_id -done

Setup Phase:

Place their ships(
    Horizontal or Vertical only, 
    no overlap
    no change in position once War Phase starts) -done

Once all done, CPU will write ship positions to database under their unique id

Initialise the board and start War Phase

War Phase:
This is an infinite loop till a win or lose condition is fulfilled

Player 1 Attack:
Player 1 calls a shot "A1"
CPU checks if miss or hit and updates the board. (clear all output)
If hit and not in list of known enemy ships:
    add to list of known enemy ships

CPU checks if Player 2 has any surviving ships.
If Player 2 has no remaining ships
    Player 1 wins
else
    Player 1 ends turn, Player 2 turn starts

Player 2 Attack:
Player 1 calls a shot "B5"
CPU checks if miss or hit and updates the board. (clear all output)
CPU checks if Player 1 has any surviving ships.
If Player 1 has no remaining ships
    Player 2 wins
else
    Player 2 ends turn, Player 1 turn starts


CPU checks:
Setup Phase:
    ships are in one piece not separate (may be difficult),
    Horizontal or Vertical only, 
    no overlap of ships,
    all ships within the board (length check),
    no change in position once War Phase starts
War Phase:
    If Hit
        change state of that ship section from 1 to dead
    else
        (miss) change state of tile from -

Each time the board changes state or the CPU makes a check, the Realtime Database is referenced.
Database Read/Writes:

Player identity: maybe use a random identity generator at the start of the game to differentiate players?
Ship positions for individual ships
shot_list
hit_list
destroyed ship list for each player

ability to replay the game
SALVO game type
