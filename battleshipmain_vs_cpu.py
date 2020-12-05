"""Global Variables"""
all_ships_dict = {"Carrier": 5 , "Battleship" : 4 , "Cruiser" : 3, "Submarine" : 3 , "Destroyer" : 2}
shot_list_P1 = []
shot_list_CPU = []
ls_all_ships_points_P1 = []
ls_all_ships_points_CPU = []
CPU_target = []

#Setup Phase
class Point:
    def __init__(self, initX, initY):
        self.x = initX
        self.y = initY
"""Board Setup"""
def initialise_board():
    pass
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
        stern_str = stern_str.upper()
        stern_bool = check_valid_point_P1(stern_str, "Stern") #check if string is garbage
        if stern_bool == True:
            return Point( stern_str[0] , stern_str[1] )
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

"""War Phase"""
"""P1 functions"""
def check_score(enemy_ship_dict):  #check if any enemy ships were sunk
    score = 0
    for ls_points in enemy_ship_dict.values():
        if ls_points == []:
            score +=1
    return score
    
def attack(): #returns a Point object with a valid shot.
    global shot_list_P1
    verified_shot = False
    while verified_shot == False:
        shot_str = input("Attack coordinates? e.g. A0 ")
        shot_str = shot_str.upper()
        if check_valid_point_P1(shot_str, "Shot"): #check if string is garbage
            shot = Point(shot_str[0], shot_str[1]) #save the shot as Point object
            if shot in shot_list_P1:
                print("You have taken this shot before! Choose another!") 
                verified_shot = False
            else:
                print("Shooting...")
                #sleep(3)
                verified_shot = True
        else:
            verified_shot = False
    shot_list_P1.append(shot)
    return shot

def check_hit(shot, enemy_ship_dict, enemy_ls_all_ships_points):
    if shot not in enemy_ls_all_ships_points: #check if shot hit anything
        print("You missed.")
    else: #finds the enemy ship with the shot and removes it from their list
        print("Shot to {} was succesful!".format(str(shot.x + shot.y)))
        for ls_points in enemy_ship_dict.values():
            if shot in ls_points:
                ls_points.remove(shot)


"""CPU functions"""
def attack_CPU_random():
    global shot_list_CPU
    verified_shot = False
    while verified_shot == False:
        shot_str = generate_random_point_str()
        shot = Point(shot_str[0], shot_str[1]) #save the shot as Point object
        if shot in shot_list_CPU:
            verified_shot = False
        else:
            print("CPU shooting...")
            verified_shot = True
    shot_list_CPU.append(shot)
    return shot

def generate_add_shot(shot, valid_dir_ls):
    #Generating addiional strike locations as a dict with direction : Point
    add_shot_dict = {}
    
    for direction in valid_dir_ls:
        if direction == "N":
            add_shot_dict[Point(shot.x, chr(ord(shot.y) - 1))] = "N"
        elif direction == "W":
            add_shot_dict[Point(chr(ord(shot.x) + 1) , shot.y)] = "W"
        elif direction == "S":
            add_shot_dict[Point(shot.x, chr(ord(shot.y) + 1))] = "S"
        elif direction == "E":
            add_shot_dict[Point(chr(ord(shot.x) - 1) , shot.y)] = "E"
    
    for point, direction in add_shot_dict.items(): #should try subtracting away and use a dictionary. useful to know the direction to whack
        if (not check_valid_point_CPU(str(point.x + point.y))) or (point in shot_list_CPU):
            del add_shot_dict[point]
    return add_shot_dict

def check_hit_CPU(shot, enemy_ship_dict, enemy_ls_all_ships_points, target_dict):
    if shot in target_dict.keys():
        if shot not in enemy_ls_all_ships_points: #target miss
            print("CPU missed.")
            #delete from target_dict and try another
            del target_dict[shot]
            return target_dict
        else: #target hit
            for ship_name, ls_points in enemy_ship_dict.items(): #finds the enemy ship with the shot and removes it from their list
                if shot in ls_points:
                    ls_points.remove(shot)
                    print("CPU hit", ship_name, "at", str(shot.x) +str(shot.y))
            #delete from target_dict and attack in known direction
            shot_dir = target_dict[shot]
            return generate_add_shot(shot, [shot_dir])
            
    else: #check for random shot
        if shot not in enemy_ls_all_ships_points: #random shot miss
            print("CPU missed.")
            return {}
        else: #random shot hit
            for ship_name, ls_points in enemy_ship_dict.items(): #finds the enemy ship with the shot and removes it from their list
                if shot in ls_points:
                    ls_points.remove(shot)
                    print("CPU hit", ship_name, "at", str(shot.x) +str(shot.y))
            return generate_add_shot(shot, ["N", "S","E", "W"] ) #len 2 to 4

"""main function"""
def main():
    game_not_over = True
    #Setting player ships
    P1_ship_dict = {}
    CPU_ship_dict = {}
    round_num = 0
    
    for ship_name in all_ships_dict:
        some_ship = place_ship_P1(ship_name)
        some_ship_name = some_ship[0]
        some_ls_points = some_ship[1]
        P1_ship_dict[some_ship_name] = some_ls_points
        print("{} written to {}!".format(some_ls_points, some_ship_name))
    
    #Setting CPU ships
    for ship_name in all_ships_dict:
        some_ship_CPU = place_ship_CPU(ship_name)
        some_ship_name = some_ship[0]
        some_ls_points = some_ship_CPU[1]
        CPU_ship_dict[some_ship_name] = some_ls_points
    
    #War Phase
    starting_player = random.choice(["P1", "CPU"])
    target_dict = {}
    if starting_player == "P1":
        player_turn = True
    else:
        player_turn = False

    while game_not_over:
        round_num += 1
        print("Round", round_num)
        if player_turn:
            print("Player's Turn!")
            shot = attack()
            check_hit(shot, CPU_ship_dict, ls_all_ships_points_CPU)
            player_turn = False
        else:
            print("CPU's Turn!")
            if target_dict == {}: #no targets
                CPU_shot = attack_CPU_random()
            else: #attack CPU target
                CPU_shot = random.choice(target_dict.keys())
            target_dict = check_hit_CPU(CPU_shot, P1_ship_dict, ls_all_ships_points_P1, target_dict) #update target_dict
            #pseudo code
            #if hit set last_CPU_ target = "hit"
            player_turn = True
        
        #CPU checks for game end
        CPU_score = check_score(P1_ship_dict)
        P1_score = check_score(CPU_ship_dict)
        if CPU_score == 5:
            print("You lost!")
            game_not_over == False # what if they are 5 at the same time
        elif P1_score == 5:
            print("You won!")
            game_not_over == False
        else:
            game_not_over == True


main()
