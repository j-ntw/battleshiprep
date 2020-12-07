"""CDT 1D Project (Player vs CPU).ipynb

Original file is located at
    https://colab.research.google.com/drive/12Dwgjhpcj9YJ0E3_7TBHte6XTNIQue90
"""

"""Global Variables"""
all_ships_dict = {"Carrier": 5 , "Battleship" : 4 , "Cruiser" : 3, "Submarine" : 3 , "Destroyer" : 2}
shot_list_P1 = []
shot_list_CPU = []
ls_all_ships_points_P1 = []
ls_all_ships_points_CPU = []
CPU_target = []
#make a dictionary: key = input letter, value = what it would mean as an x-coordinate
letter_to_xcoord_dict = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'J': 8, 'K': 9}
point_to_ycoord_dict = { "9":0, "8":1, "7":2, "6":3, "5":4, "4":5, "3":6, "2":7, "1":8, "0":9}

"""Initialise matplotlib board"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

board = plt.figure(figsize=[6,6])
board.patch.set_facecolor((1,1,.8))
ax = board.add_subplot(111)

# draw the grid
for x in range(11):
    ax.plot([x, x], [0,10], 'k')
for y in range(11):
    ax.plot([0, 10], [y,y], 'k')

# scale the axis area to fill the whole figure
ax.set_position([0,0,1,1])

# get rid of axes and everything (the figure background will show through)
ax.set_axis_off()

# scale the plot area conveniently (the board is in 0,0..18,18)
ax.set_xlim(-1,11)
ax.set_ylim(-1,11)

# add axis labels to the axes
x_axis_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K'] #x-axis names for plotting
for i in range(10):
    ax.text(i+0.4, 10.2, x_axis_letters[i])
    ax.text(-0.4, 9.4-i, list(range(10))[i])

"""Matplotlib draw_rectangle function : Changes a square's colour to black, grey or red"""

def draw_rectangle(point, colour):
    #convert the letter into an x-coordinate number
    chosen_xcoord = letter_to_xcoord_dict[point[0]]
    chosen_ycoord = point_to_ycoord_dict[point[1]]
    
    if colour == 'b': # makes the square turn black
        rect = patches.Rectangle((chosen_xcoord, chosen_ycoord), 1, 1, facecolor='black') #ship points
        ax.add_patch(rect)
    elif colour == 'r': # makes the square turn red
        rect = patches.Rectangle((chosen_xcoord, chosen_ycoord), 1, 1, facecolor='red') #hit
        ax.add_patch(rect)
    elif colour == 'g': # makes the square turn grey
        rect = patches.Rectangle((chosen_xcoord, chosen_ycoord), 1, 1, facecolor='grey') #miss
        ax.add_patch(rect)
    # add the patch to the axes
    

"""Player 1 Set-Up

check_valid_point_P1 : Check if point is valid
Used in place_stern_P1
"""

#Setup Phase
"""P1 Setup"""
def check_valid_point_P1(point, thing):
    #returns False if string is in invalid format, True if valid.
    if (len(point) != 2) or (point[0].upper() not in "ABCDEFGHJK") or (point[1] not in "0123456789"):
        return False
        #Check if thing is within the board using ASCII index
    elif (ord(point[0]) > 75 or ord(point[0]) < 65 or ord(point[1]) > 57 or ord(point[1]) < 48): 
        print(thing, " is out of board!")
        return False
    else:
        return True

"""place_stern_P1 : Place stern by asking for user input
"""

def place_stern_P1(ship_name, ship_length):
    stern_bool = False
    
    while stern_bool == False :
        stern = input("Where would you like the stern of your {} ({}) to be? e.g. A0. 'I' is not valid.".format(ship_name, ship_length))#A0
        stern = stern.upper()
        stern_bool = check_valid_point_P1(stern, "Stern") #check if string is garbage
        if stern_bool == True:
            draw_rectangle(int(stern[0]), int(stern[1]), 'black') #display stern as black square
            return stern
            #returns stern coordinates as a string
        else:
            print("Please enter valid coordinates! e.g. B1")

"""**generate_ship_sections_P1 : Generates a list of points containing the shape of the ship, depending on ship_name** Returns the list of points ls_points"""

def generate_ship_sections_P1(stern, ship_name, size ):
    direction_bool = False
    ls_points = [stern]
    
    while direction_bool == False:
        #Generating ships points based on direction
        direction = input("Which direction would you like your {} to face? Type 'X' to choose another point. [N/S/E/W/X] ".format(ship_name))
        direction = direction.upper()
        if direction in "NSEWX":
            for i in range(1, size):
                if direction == "N":
                    ls_points.append(stern[0] + chr(ord(stern[1]) - i))
                elif direction == "W":
                    ls_points.append(chr(ord(stern[0]) + i) + stern[1])
                elif direction == "S":
                    ls_points.append(stern[0] + chr(ord(stern[1]) + i))
                elif direction == "E":
                    ls_points.append(chr(ord(stern[0]) - i) + stern[1])
                elif direction == "X":
                    return "X"
            direction_bool = True
        else:
            print("Please type [N/S/E/W/X]!")
            direction_bool = False

    for point in ls_points:
      draw_rectangle(point[0], point[1], 'black') #display ship as black squares     
    return ls_points

"""**check_ship_sections_P1 : Check if all points within ls_points are valid (within board and not overlapping other ships)** Similar to check_valid_point_P1 but for ls_points instead of place_stern_P1"""

def check_ship_sections_P1(ship_name, ls_points):
    points_valid = True
    #use ASCII numbering to check
    for point in ls_points:
        #if point is out of board, break for loop
        if not check_valid_point_P1(point, ship_name):
            points_valid = False
            print("Choose another direction, ya ship's hangin' off the board ya dingus")
            break
        #check if point conflicts with another ship's points
        elif point in ls_all_ships_points_P1:
            print(ship_name, " overlaps an existing ship!")
            points_valid = False
            break
        else:
            continue
    return points_valid

"""**place_ship_P1 : Matches ls_points to ship_name in global list ls_all_ships_points_P1** Uses results of check_valid_point_P1 and check_ship_sections_P1, and points from place_stern_P1 and generate_ship_sections_P1"""

def place_ship_P1(ship_name):
    global all_ships_dict
    global ls_all_ships_points_P1 # necessary to check if current ship conflicts with previously placed ship
    size = all_ships_dict.get(ship_name) #get ship's size from dictionary
    ship_placed = False 

    while ship_placed == False:
        stern = place_stern_P1(ship_name, all_ships_dict[ship_name]) #ask player for stern position
        #generate list of ship points based on known stern and requested direction
        ls_points = generate_ship_sections_P1(stern, ship_name, size)
        if ls_points == "X":
            ship_placed = False
            points_valid = False
        else:
            #check if the ships points are valid based on the known board and known ships
            points_valid = check_ship_sections_P1(ship_name, ls_points)
        #if any of the ship's points are invalid, points_valid = False and the for loop breaks, restarting the while loop
        #If the for loop doesn't break, all ship points are valid and we set direction_bool to True to break the while loop
        if points_valid:
            ship_placed = True

    print("Ship placed!") #tell the player the ship is placed
    
    for i in ls_points: #add the ship's points to list of known ships points
        ls_all_ships_points_P1.append(i)
        draw_rectangle(i[0], i[1], 'black') #display ships as black squares
    return [ship_name, ls_points]

"""CPU setup"""
def check_valid_point_CPU(point):
    #Check if thing is within the board using ASCII index
    if (ord(point[0]) > 75 or ord(point[0]) < 65 or ord(point[1]) > 57 or ord(point[1]) < 48): 
        return False
    else:
        return True

import random

def generate_random_point():
    ls_valid_points = []
    for char in "ABCDEFGHJK":
        for num in "0123456789":
            ls_valid_points.append(char+num)
    return random.choice(ls_valid_points)
    
def generate_ship_sections_CPU(stern, ship_name, size ):
    ls_points = [stern]
    #Generating ships points based on random direction
    valid_dir_ls = ["N", "S","E", "W"]
    direction = random.choice(valid_dir_ls)
    for i in range(1, size):
        if direction == "N":
            ls_points.append(stern[0] + chr(ord(stern[1]) - i))
        elif direction == "W":
            ls_points.append(chr(ord(stern[0]) + i) + stern[1])
        elif direction == "S":
            ls_points.append(stern[0] + chr(ord(stern[1]) + i))
        elif direction == "E":
            ls_points.append(chr(ord(stern[0]) - i) + stern[1])
    return ls_points

def check_ship_sections_CPU(ship_name, ls_points):
    points_valid = True
    #use ASCII numbering to check
    for point in ls_points:
        #if point is out of board, break for loop
        if not check_valid_point_CPU(point):
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
    stern = generate_random_point()
    
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

"""# War Phase: Player 1
"""

def check_score(enemy_ship_dict):  #check if any enemy ships were sunk
    score = 0
    for ls_points in enemy_ship_dict.values():
        if ls_points == []:
            score +=1
    return score

def attack(): #returns a valid shot.
    global shot_list_P1
    verified_shot = False
    while verified_shot == False:
        shot = input("Attack coordinates? e.g. A0 ")
        shot = shot.upper()
        if check_valid_point_P1(shot, "Shot"): #check if string is garbage            
            if shot in shot_list_P1:
                print("You have taken this shot before! Choose another!") 
                verified_shot = False
            else:
                print("Shooting...")
                #sleep(3)
                verified_shot = True
        else:
            verified_shot = False
            print("Please enter valid coordinates! e.g. B1")
    shot_list_P1.append(shot)
    print(shot_list_P1)
    return shot

def check_hit(shot, enemy_ship_dict, enemy_ls_all_ships_points):
    if shot not in enemy_ls_all_ships_points: #check if shot hit anything
        print("You missed.")
        draw_rectangle(shot[0], shot[1], 'grey')
    else: #finds the enemy ship with the shot and removes it from their list
        print("Shot to {} was succesful!".format(shot) )
        draw_rectangle(shot[0], shot[1], 'red')
        for ls_points in enemy_ship_dict.values():
            if shot in ls_points:
                ls_points.remove(shot)

"""# War Phase: CPU"""
def attack_CPU_random():
    verified_shot = False
    while verified_shot == False:
        shot = generate_random_point()
        if shot in shot_list_CPU:
            verified_shot = False
        else:
            print("CPU shooting...")
            verified_shot = True
    return shot

def generate_add_shot(shot, valid_dir_ls):
    #Generating addiional strike locations as a dict with direction : Point
    add_shot_dict = {}
    for direction in valid_dir_ls:
        if direction == "N":
            add_shot_dict[shot[0] + chr(ord(shot[1]) - 1)] = "N"
        elif direction == "W":
            add_shot_dict[chr(ord(shot[0]) + 1) + shot[1]] = "W"
        elif direction == "S":
            add_shot_dict[shot[0] + chr(ord(shot[1]) + 1)] = "S"
        elif direction == "E":
            add_shot_dict[chr(ord(shot[0]) - 1) + shot[1]] = "E"
    
    for point, direction in add_shot_dict.items(): #should try subtracting away and use a dictionary. useful to know the direction to whack
        if (not check_valid_point_CPU(point)) or (point in shot_list_CPU):
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
                    print("CPU hit", ship_name, "at", shot)
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
                    print("CPU hit", ship_name, "at", shot)
            return generate_add_shot(shot, ["N", "S","E", "W"] ) #len 2 to 4

"""# Main Function

**main : Puts everything together**
"""

"""main function"""
def main():
    plt.show(block = False)
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
        plt.show(block = False)   

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
            plt.show(block = False)
        else:
            print("CPU's Turn!")
            if target_dict == {}: #no targets
                CPU_shot = attack_CPU_random()
            else: #attack CPU target
                CPU_shot = random.choice(target_dict.keys())
            target_dict = check_hit_CPU(CPU_shot, P1_ship_dict, ls_all_ships_points_P1, target_dict) #update target_dict
            shot_list_CPU.append(CPU_shot)
            player_turn = True
            plt.show(block = False)
        
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
