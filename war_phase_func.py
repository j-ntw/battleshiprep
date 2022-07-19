import random

def attack():
    shot_bool = False
    my_turn_bool = True
    while shot_bool == False:
        shot_str = input("Attack coordinates? e.g. A0 ")
        if check_valid_point_P1(shot_str, "Shot"): #check if string is garbage
            shot = Point(shot[0].upper(), shot[1]) #save the shot as Point object
            if shot in shot_list:
                print("You have taken this shot before! Choose another!") 
                shot_bool = False
            else:
                print("Shooting...")
                #sleep(3)
                shot_bool = True
        else:
            shot_bool = False
   
    if shot in enemy_all_ships_points_list:
        print("Shot to {} was succesful!".format(str(shot.x + shot.y)))
        shot_list.append(shot)
        #check if any enemy ships were sunk
        #check if all enemy ships sunk
    else:
        print("You missed.")
        shot_list.append(shot)
    myturn_bool = False

    def attack_CPU():
