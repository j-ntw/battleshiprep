"""Firebase"""
from libdw import pyrebase
from time import sleep

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


##########################

import string
import random
def generate_unique_id():
    letters = string.ascii_lowercase
    id_str = ""
    for i in range(4):
        id_str+=(random.choice(letters))
    return id_str 

##########################

# if player 2 has not joined, player 1 cannot start setting up his board.
"""
generates player 1 id and captures player 2 id. to create a list of player ids
All id are used as keys for database dictionaries
order of local ls_player_id matters but not that of database ls_player_id as
database version is just to exchange player id

"""
def get_id(P1_name):
    P1_id = generate_unique_id()
    print(P1_id)
    ls_player_id = db.child("Player_id").get(user['idToken']).val()
    id_timeout = 0 #max timeout is 15*5 seconds 
    
    #if no players, player 1 joins the game and update the database
    if (ls_player_id == None):
        print("joining game with id")
        db.child("Player_id").set([P1_id], user['idToken'])
    ls_player_id = list( db.child("Player_id").get(user['idToken']).val())
    while (len(ls_player_id) <=2) and (id_timeout <=15) :
        #if player 1 is the only one in the game, wait for player 2 
        if ls_player_id == [P1_id] :
            print("Player 2 has not yet joined.")
            sleep(5)
        #if player 1 is not in the game, but player 2 is, capture player 2 id,
        #player 1 joins the game and update the database
        elif len(ls_player_id) == 1 and ls_player_id != [P1_id]:
            print("Getting P2 id")
            P2_id = ls_player_id[0]
            ls_player_id = [P1_id, P2_id]
            db.child("Player_id").set(ls_player_id, user['idToken'])
        #if both players are in the game, capture player 2 id
        #no need to update the database
        elif len(ls_player_id) == 2 and P1_id in ls_player_id:
            ls_player_id.remove(P1_id)
            P2_id = ls_player_id[0]
            ls_player_id = [P1_id, P2_id]
            break
        else:
            print("get_id() error")
            break
        id_timeout += 1    
    return ls_player_id

##########################

def create_dict_player_name(P1_name, ls_player_id):
    P1_id = ls_player_id[0]
    P2_id = ls_player_id[1]
    #query a dictionary from the key "Player_name"
    dict_player_name = db.child("Player_name").get(user['idToken']).val()
    player_name_timeout = 0 #wait for max of 15*5 seconds to get player 2 name

    #if no names, write Player 1 name
    if dict_player_name == None:
        print("Adding Player 1")
        db.child("Player_name").set({P1_id : P1_name}, user['idToken'])
    dict_player_name = dict(db.child("Player_name").get(user['idToken']).val())
    while (len(dict_player_name) <=2) and (player_name_timeout <= 15) :
        if len(dict_player_name) == 1:
            #if player 1 name is inside and player 2 name is not yet written,wait
            if dict_player_name == {P1_id : P1_name}:
                print("Waiting for Player 2")
                sleep(5)
                continue
            #if player 1 name is not inside, but player 2 is
            #write player 1 name
            else:
                print("Player 2 is in the game. Joining game.")
                P2_name = dict_player_name[P2_id]
                dict_player_name = {P1_id : P1_name , P2_id : P2_name}
                db.child("Player_name").set(dict_player_name, user['idToken'])
                
        #if both player name in dictionary, break the while loop
        elif len(dict_player_name) == 2:
            print("both players are already in the game!")
            break
        else:
            print("create_dict_player_name() error")
        player_name_timeout +=1
    print(dict_player_name)    
    #use player 2 id to get player 2 name
    P2_name = dict_player_name.get(P2_id)
    print(P1_name, "is playing with", P2_name)
    return {P1_id : P1_name , P2_id : P2_name}

