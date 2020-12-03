"""Global Variables"""
all_ships_dict = {"Carrier": 5 , "Battleship" : 4 , "Cruiser" : 3, "Submarine" : 3 , "Destroyer" : 2}
shot_list = []
ls_all_ships_points_P1 = []
ls_all_ships_points_CPU = []

#Setup Phase
class Point:
    def __init__(self, initX, initY):
        self.x = initX
        self.y = initY

"""P1 Setup"""
def check_valid_point_P1(point_str, thing):
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
        
def place_stern_P1(ship_name):
    stern_bool = False
    
    while stern_bool == False :
        stern_str = input("Where would you like the stern of your {} to be? e.g. A0. 'I' is not valid.".format(ship_name))#A0
        stern_bool = check_valid_point_P1(stern_str, "Stern") #check if string is garbage
        if stern_bool == True:
            return Point( stern_str[0].upper() , stern_str[1] )
            #returns stern coordinates as a Point object

def generate_ship_sections_P1(stern, ship_name, size ):
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

def check_ship_sections_P1(ship_name, ls_points):
    points_valid = True
    #use ASCII numbering to check
    for point in ls_points:
        #if point is out of board, break for loop
        point_str = point.x + point.y
        if not check_valid_point_P1(point_str, ship_name):
            points_valid = False
            break
        #check if point conflicts with another ship's points
        elif point in ls_all_ships_points_P1:
            print(ship_name, " overlaps an existing ship!")
            points_valid = False
            break
        else:
            continue
    return points_valid


def place_ship_P1(ship_name):
    global all_ships_dict
    global ls_all_ships_points_P1 # necessary to check if current ship conflicts with previously placed ship
    size = all_ships_dict.get(ship_name) #get ship's size from dictionary
    stern = place_stern_P1(ship_name) #ask player for stern position
    
    ship_placed = False      
    while ship_placed == False:
        #generate list of ship points based on known stern and requested direction
        ls_points = generate_ship_sections_P1(stern, ship_name, size)
        
        #check if the ships points are valid based on the known board and known ships
        points_valid = check_ship_sections_P1(ship_name, ls_points)
        #if any of the ship's points are invalid, points_valid = False and the for loop breaks, restarting the while loop
        #If the for loop doesn't break, all ship points are valid and we set direction_bool to True to break the while loop
        if points_valid:
            ship_placed = True

    print("Ship placed!") #tell the player the ship is placed
    
    for i in ls_points: #add the ship's points to list of known ships points
        ls_all_ships_points_P1.append(i)
    return [ship_name, ls_points]

"""CPU setup"""

def check_valid_point_CPU(point_str):
    #Check if thing is within the board using ASCII index
    if (ord(point_str[0]) > 75 or ord(point_str[0]) < 65 or ord(point_str[1]) > 57 or ord(point_str[1]) < 48): 
        return False
    else:
        return True

###
import random
###
def generate_random_point_str():
    ls_valid_points = []
    for char in "ABCDEFGHJK":
        for num in "0123456789":
            ls_valid_points.append(char+num)
    return random.choice(ls_valid_points)

def place_stern_CPU(ship_name):
    stern_str = generate_random_point_str()
    return Point( stern_str[0] , stern_str[1] )  #returns stern coordinates as a Point object

           
def generate_ship_sections_CPU(stern, ship_name, size ):
    ls_points = [stern]
    #Generating ships points based on random direction
    valid_dir_ls = ["N", "S","E", "W"]
    direction = random.choice(valid_dir_ls)
    for i in range(1, size):
        if direction == "N":
            ls_points.append(Point(stern.x, chr(ord(stern.y) - i)))
        elif direction == "W":
            ls_points.append(Point(chr(ord(stern.x) + i) , stern.y))
        elif direction == "S":
            ls_points.append(Point(stern.x, chr(ord(stern.y) + i)))
        elif direction == "E":
            ls_points.append(Point(chr(ord(stern.x) - i) , stern.y))  
    return ls_points

def check_ship_sections_CPU(ship_name, ls_points):
    points_valid = True
    #use ASCII numbering to check
    for point in ls_points:
        #if point is out of board, break for loop
        point_str = point.x + point.y
        if not check_valid_point_CPU(point_str):
            points_valid = False
            break
        #check if point conflicts with another ship's points
        elif point in ls_all_ships_points_P1:
            points_valid = False
            break
        else:
            continue
    return points_valid


def place_ship_CPU(ship_name):
    global all_ships_dict
    global ls_all_ships_points_CPU # necessary to check if current ship conflicts with previously placed ship
    size = all_ships_dict.get(ship_name) #get ship's size from dictionary
    stern = place_stern_CPU(ship_name) #ask player for stern position
    
    ship_placed = False      
    while ship_placed == False:
        #generate list of ship points based on known stern and requested direction
        ls_points = generate_ship_sections_CPU(stern, ship_name, size)
        
        #check if the ships points are valid based on the known board and known ships
        points_valid = check_ship_sections_CPU(ship_name, ls_points)
        #if any of the ship's points are invalid, points_valid = False and the for loop breaks, restarting the while loop
        #If the for loop doesn't break, all ship points are valid and we set direction_bool to True to break the while loop
        if points_valid:
            ship_placed = True

    print("Ship placed!") #CPU placed ship
    
    for i in ls_points: #add the ship's points to list of known ships points
        ls_all_ships_points_CPU.append(i)
    return [ship_name, ls_points]


def main():
    #Setting player ships
    p1_ship_dict = {}
    CPU_ship_dict = {}
    for ship_name in all_ships_dict:
        some_ship = place_ship_P1(ship_name)
        some_ship_name = some_ship[0]
        some_ls_points = some_ship[1]
        p1_ship_dict[some_ship_name] = some_ls_points
        print("{} written to {}!".format(some_ls_points, some_ship_name))
    
    #Setting CPU ships
    for ship_name in all_ships_dict:
        some_ship_CPU = place_ship_CPU(ship_name)
        some_ls_points = some_ship_CPU[1]
        CPU_ship_dict[some_ship_name] = some_ls_points
    
    #War Phase
    
