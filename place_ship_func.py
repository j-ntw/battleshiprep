"""Global Variables"""
all_ships_dict = {"Carrier": 5 , "Battleship" : 4 , "Cruiser" : 3, "Submarine" : 3 , "Destroyer" : 2}
shot_list = []
ls_all_ships_points = []

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