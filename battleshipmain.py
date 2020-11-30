import os
from os import system,name #do i need to import separately?
from os import sleep
##############
"""Global Variables"""
all_ships_dict = {"Carrier": 5 , "Battleship" : 4 , "Cruiser" : 3, "Submarine" : 3 , "Destroyer" : 2}
shot_list = []
ls_all_ships_points = []
##############
"""Set up Pyrebase"""
from libdw import pyrebase
from time import sleep

#add Firebase to application
projectid = "toat-11cda"
dburl = "https://" + projectid + ".firebaseio.com"
authdomain = projectid + ".firebaseapp.com"
apikey = "AIzaSyB7GpY2DNqjiWQeKnTN4Cn-jUu5RTNJMcU"
email = "joshuantw@gmail.com"
password = "password"

#for use with only user based authentication
config = {
    "apiKey": apikey,
    "authDomain": authdomain,
    "databaseURL": dburl,
}
"""
Pyrebase app can use multiple Firebase services such as:
firebase.auth() - Authentication

firebase.database() - Database

firebase.storage() - Storage
"""

firebase = pyrebase.initialize_app(config) #kick things off
auth = firebase.auth() #authentication service
user = auth.sign_in_with_email_and_password(email, password) #creation of first token
db = firebase.database() #database service
user = auth.refresh(user['refreshToken']) #renewal of token as tokens expire hourly
##############
"""generate unique id for each player to differentiate them in database"""
import string
import random
def generate_unique_id():
    letters = string.ascii_lowercase
    id_str = ""
    for i in range(4):
        id_str.join(random.choice(letters))
    return id_str 
##############

#initialise board as a 8 x 8 matrix of 0s
import matplotlib.pyplot as plt
board = plt.figure(figsize=[8,8])
board.patch.set_facecolor((1,1,.8))
ax = board.add_subplot(111)

# draw the grid
for x in range(10):
    ax.plot([x, x], [0,9], 'k')
for y in range(10):
    ax.plot([0, 9], [y,y], 'k')

# scale the axis area to fill the whole figure
ax.set_position([0,0,1,1])

# get rid of axes and everything (the figure background will show through)
ax.set_axis_off()

# scale the plot area conveniently (the board is in 0,0..18,18)
ax.set_xlim(-1,10)
ax.set_ylim(-1,10)
plt.show()

##############
#Matching Phase
def ask_player_name():
    name = input("Please enter your name: ")
    print("Your name is: ", name )
    return name

def get_id(P1_name):
    pass

def create_dict_player_name(P1_name, ls_player_id):
    pass
##############
#Setup Phase
class Point:
    def __init__(self, initX, initY):
        self.x = initX
        self.y = initY

def check_valid_point(point_str, thing):
    #returns False if string is in invalid format, True if valid.
    if (len(point_str) != 2) or (point_str[0].upper() not in "ABCDEFGHJK") or (point_str[1] not in "0123456789"):
        print("Please enter valid coordinates! e.g. B1")
        return False
        #Check if thing is within the board using ASCII index
    elif (ord(point_str[0]) > 75 or ord(point_str[0]) < 65 or ord(point_str[1]) > 57 or ord(point_str[1]) < 48): 
        print(thing, " is out of board!")
        return False
    else:
        return True
        
def place_stern(ship_name):
    stern_bool = False
    
    while stern_bool == False :
        stern_str = input("Where would you like the stern of your {} to be? e.g. A0. 'I' is not valid.".format(ship_name))#A0
        stern_bool = check_valid_point(stern_str, "Stern") #check if string is garbage
        if stern_bool == True:
            return Point( stern_str[0].upper() , stern_str[1] )
            #returns stern coordinates as a Point object

def generate_ship_sections(stern, ship_name, size ):
    direction_bool = False
    ls_points = [stern]
    
    while direction_bool == False:
        #Generating ships points based on direction
        direction = input("Which direction would you like your {} to face? [N/S/E/W] ".format(ship_name))
        direction = direction.upper()
        if direction in "NSEW":
            for i in range(1, size):
                if direction == "N":
                    ls_points.append(Point(stern.x, chr(ord(stern.y) - i)))
                elif direction == "W":
                    ls_points.append(Point(chr(ord(stern.x) + i) , stern.y))
                elif direction == "S":
                    ls_points.append(Point(stern.x, chr(ord(stern.y) + i)))
                elif direction == "E":
                    ls_points.append(Point(chr(ord(stern.x) - i) , stern.y))
            direction_bool = True
        else:
            print("Please type [N/S/E/W]!")
            direction_bool = False
            
    return ls_points

def check_ship_sections(ship_name, ls_points):
    points_valid = True
    #use ASCII numbering to check
    for point in ls_points:
        #if point is out of board, break for loop
        point_str = point.x + point.y
        if not check_valid_point(point_str, ship_name):
            points_valid = False
            break
        #check if point conflicts with another ship's points
        elif point in ls_all_ships_points:
            print(ship_name, " overlaps an existing ship!")
            points_valid = False
            break
        else:
            continue
    return points_valid


def place_ship(ship_name):
    global all_ships_dict
    global ls_all_ships_points # necessary to check if current ship conflicts with previously placed ship
    size = all_ships_dict.get(ship_name) #get ship's size from dictionary
    stern = place_stern(ship_name) #ask player for stern position
    
    ship_placed = False      
    while ship_placed == False:
        #generate list of ship points based on known stern and requested direction
        ls_points = generate_ship_sections(stern, ship_name, size)
        
        #check if the ships points are valid based on the known board and known ships
        points_valid = check_ship_sections(ship_name, ls_points)
        #if any of the ship's points are invalid, points_valid = False and the for loop breaks, restarting the while loop
        #If the for loop doesn't break, all ship points are valid and we set direction_bool to True to break the while loop
        if points_valid:
            ship_placed = True

    print("Ship placed!") #tell the player the ship is placed
    
    for i in ls_points: #add the ship's points to list of known ships points
        ls_all_ships_points.append(i)
    #maybe I dont need to return anything cos i just write it to database
    return [ship_name, ls_points]

#ship is  Write list of points to database for key: ship type, value is a dictionary with key as player id and value as list of ship coordinates
def write_ship(ship):
    

##############        

##############        
def main():
    #initialise board
    board = get_zero_matrix(10,10)

    #Matching Phase
    #Ask for player name
    P1_name = ask_player_name()
    P1_id = generate_unique_id()

   
    sleep(2)



    #Setup Phase
    print("SETUP PHASE: BEGIN!")
    sleep(2)
    for ship_name in all_ships_dict:
        ship = place_ship(ship_name)
        write_ship(ship)
    while P2_ready == False:
        sleep(5)
        print("Waiting on Player 2...")

    #War Phase
    game_not_over = True
    while game_not_over:
        pass


"""
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


"""
