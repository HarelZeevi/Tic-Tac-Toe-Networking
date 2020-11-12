import turtle
import random
import sys
import client
from client import *
import socket
import threading
from playsound import playsound


OPENING_SCREEN = '''

  _____     _                     _____                           _____    ___     ___   
 |_   _|   (_)     __      ___   |_   _|  __ _     __      ___   |_   _|  / _ \   | __|  
   | |     | |    / _|    |___|    | |   / _` |   / _|    |___|    | |   | (_) |  | _|   
  _|_|_   _|_|_   \__|_   _____   _|_|_  \__,_|   \__|_   _____   _|_|_   \___/   |___|  
_|"""""|_|"""""|_|"""""|_|     |_|"""""|_|"""""|_|"""""|_|     |_|"""""|_|"""""|_|"""""| 
"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-'"`-0-0-' 
'''

def play_sound():
        playsound("sound_effects\\start_game.mp3")


wn = turtle.Screen()
drawer = turtle.Turtle()
drawer.speed(100)
T = turtle.Turtle()
T.hideturtle()
T.pu()
T.speed(100)


def background_drawing():
    drawer.hideturtle()
    drawer.pu()
    drawer.setpos(-100,0)
    drawer.pd()
    flag = True
    for i in range(2):
        for i in range(2):
            drawer.fd(100)
            if flag == True:
                drawer.lt(90)
            else:
                drawer.rt(90)
            drawer.fd(100)
            drawer.bk(200)
            drawer.fd(100)
            if flag == True:
                drawer.rt(90)
            else:
                drawer.lt(90)
        drawer.fd(100)
        flag = False
        drawer.bk(300)
        drawer.pu()
        drawer.sety(-100)
        drawer.pd()
    drawer.fd(100)
    drawer.pu()


   
def locate_drawer_on_pos(pos, playing_type):
    locate_drawer_on_pos.counter += 1
    pos = str(pos)
    drawer.pu()
    if playing_type == "x":
        drawer.setpos(-50 + (int(pos[0]) - 1) * 100, 40 - 100 * (int(pos[1]) - 1))
    elif (playing_type == "o") and (locate_drawer_on_pos.counter != 1):
        drawer.setpos(-40 + (int(pos[0]) - 1) * 100, 60 - 100 * (int(pos[1]) - 1))
    else:
        drawer.setpos(-30 + (int(pos[0]) - 1) * 100, 30 - 100 * (int(pos[1]) - 1))
    drawer.pd()
    drawer.pensize(10)
locate_drawer_on_pos.counter = 0 

    
def x_sound():
    playsound("sound_effects\\drawing_x.mp3")
    
def draw_x():
    playsound("sound_effects\\drawing_x.wav")
    drawer.pd()
    drawer.setheading(45)
    drawer.fd(18)
    drawer.bk(36)
    drawer.fd(18)
    drawer.setheading(135)
    drawer.fd(18)
    drawer.bk(36)
    drawer.fd(18)
    drawer.pu()

def o_sound():
    mixer.init() # initiate the mixer instance
    mixer.music.load('drawing_o.mp3') # loads the music, can be also mp3 file.
    mixer.music.play()
    
def draw_o():
    playsound("sound_effects\\drawing_o.wav")
    drawer.pd()
    drawer.circle(20)
    drawer.pu()



def click_position(x, y):
    possible_poses = ['11', '21', '31', '12', '22', '32', '13', '23', '33']
    #print(WAIT_MSG)       
    if (messages) and (messages[-1] != WAIT_MSG) and (messages[-1] != str(client_socket)):
        print(x,y)
        if (x > -100) and (x < 0) and (y > 0) and (y < 100):
            pos = 11
        elif (x > 0) and (x < 100) and (y > 0) and (y < 100):
            pos = 21
        elif (x > 100) and (x < 200) and (y > 0) and (y < 100):
            pos = 31
        elif (x > -100) and (x < 0) and (y > -100) and (y < 0):
            pos = 12
        elif (x > 0) and (x < 100) and (y > -100) and (y < 0):
            pos = 22
        elif (x > 100) and (x < 200) and (y > -100) and (y < 0):
            pos = 32
        elif (x > -100) and (x < 0) and (y > -200) and (y < -100):
            pos = 13
        elif (x > 0) and (x < 100) and (y > -200) and (y < -100):
            pos = 23
        elif (x > 100) and (x < 200) and (y > -200) and (y < -100):
            pos = 33

        
        if pos:
            possible_poses.remove(str(pos))
            if "o" in messages:
                player_type = "o"
                opposite_type = "x"
                T.sety(250)
                T.write("You are O", font=("Machine Gunk", 20, 'normal')) 
        
            else:
                player_type = "x"
                opposite_type = "o"
                T.sety(250)
                T.write("You are X",  font=("Machine Gunk", 20, 'normal'))

            locate_drawer_on_pos(pos, playing_type=player_type)
                    
            if player_type == "o":
                draw_o()
            else:
                draw_x()
            print("<pos> is sending to the server...")
            client.send_msg(str(pos))
            print(pos)
            client.send_msg(str(client_socket))
        else:
            print("<pos> is not defined...")

        
        win_or_lose(str(pos), p_type=player_type, player_or_opponent="player")
        
def opponent_moves_handler():
    possible_poses = ['11', '21', '31', '12', '22', '32', '13', '23', '33']
    while True:
        if not("you lose!" in messages):   
            if "o" in messages:
                opponent_type = "x"
            else:
                opponent_type= "o"

            if (len(messages) > 2) and (messages[-2] in possible_poses):
                locate_drawer_on_pos(pos=messages[-2], playing_type=opponent_type)
                possible_poses.remove(messages[-2])
                if opponent_type == "x":
                    draw_x()
                else:
                    draw_o()
                win_or_lose(pos=messages[-2], p_type=opponent_type, player_or_opponent="opponent")
        else:
            print("you lose!")
            playsound("sound_effects\\you-lose.mp3")
            sys.exit("error exiting")
            break
            
            
board  = [["-", "-", "-"],
         ["-", "-", "-"],
         ["-", "-", "-"]]

def win_or_lose(pos, p_type, player_or_opponent):
    print(messages)
    board[int(pos[0]) - 1][int(pos[1]) - 1] = p_type
    print(board)
    for i in range(3):
        if (player_or_opponent == "player") and ((board[i].count(p_type) == 3) or ((board[0][2] == p_type) and (board[0][2] == board[1][2]) and (board[1][2] == board[2][2])) or ((board[0][1] == p_type) and (board[0][1] == board[1][1]) and (board[1][1] == board[2][1])) or((board[0][0] == p_type) and (board[0][0] == board[1][1]) and (board[1][1] == board[2][2])) or ((board[0][0] == p_type) and (board[0][0] == board[1][0]) and (board[1][0] == board[2][0])) or ((board[0][0] == p_type) and (board[0][0] == board[1][0]) and (board[1][0] == board[2][0])) or ((board[0][2] == p_type) and (board[0][2] == board[1][1]) and (board[1][1] == board[2][0]))):
            print("you win!")
            playsound("sound_effects\\win.mp3")
            client.send_msg("you lose!")
            client_socket.close()
            sys.exit("error exiting")
            play_again = input("want to play again?(y//n)")
            if play_again == "y":
                main()
            break

        

                
def game_funcs():
    background_drawing()
    opponent_moves_thread = threading.Thread(target=opponent_moves_handler)
    opponent_moves_thread.daemon = True
    opponent_moves_thread.start()
    wn.onclick(click_position)


def main():
    print(OPENING_SCREEN)
    sound_thread = threading.Thread(target=play_sound)
    sound_thread.daemon = True
    sound_thread.start()

    client_thread = threading.Thread(target=client.main)
    client_thread.daemon = True
    client_thread.start()
    game_funcs()


if __name__ == "__main__":
    main()



wn.mainloop()
