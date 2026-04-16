from datetime import date
import matplotlib.pyplot as plt
import numpy as np
from design_elements import *
import csv
#centers the window
import os
os.environ['SDL_VIDEO_CENTERED']='1'
#

#taking command line arguments
import sys
username1=sys.argv[1]
username2=sys.argv[2]
#

print("Welcome to the game, " + username1 + " and " + username2 + "!")
gameName=None

#pygame setup
import pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 50) #(font style,size)
pygame.display.set_caption("Game Hub")

#display sizes
info=pygame.display.Info()
width=info.current_w
height=info.current_h
screen=pygame.display.set_mode((width,height))
#

clock=pygame.time.Clock()
#

#modifies .stats_{gameName}.csv to update the number of wins and losses for each player
#.stats_{gameName}.csv is of form username,number of wins, number of losses, and Win/Loss ratio
def update_stats():
    filename=".stats_"+gameName+".csv"
    os.system("touch " + filename) 
    
    lines=None #list of lines
    with open(filename, "r") as f:
        lines=f.readlines()
        winnerfound=False
        loserfound=False
        for idx,i in enumerate(lines):
            if(i.split(",")[0]==winner):
                wins=int(i.split(",")[1])
                losses=int(i.split(",")[2])
                wins+=1
                winnerfound=True
                if losses!=0:
                    WuponL=str(wins/losses)
                else:
                    WuponL="inf"
                lines[idx]=winner + "," + str(wins) + "," + str(losses) + "," + WuponL + "\n"
            elif(i.split(",")[0]==loser):
                wins=int(i.split(",")[1])
                losses=int(i.split(",")[2])
                losses+=1
                loserfound=True
                lines[idx]=loser + "," + str(wins) + "," + str(losses) + "," + str(wins/losses)+ "\n"
        
        #If its the first time a user has won or lost
        if(not winnerfound):
            lines.append(winner + ",1,0,inf\n")
        if(not loserfound):
            lines.append(loser + ",0,1,0\n")
        #
        
    #overwrite the file with the updated stats
    with open(filename, "w") as f:
        f.writelines(lines)
    #
    
#game_frequencies is of form: game name, number of times played
#modifies .game_frequencies.csv to update the number of times each game has been played
def update_game_frequencies():
    filename=".game_frequencies.csv"
    os.system("touch " + filename) 
    lines=None
    with open(filename, "r") as f:
        lines=f.readlines()
        found=False
        for i,line in enumerate(lines):
            if(line.split(",")[0]==gameName):
                freq=int(line.split(",")[1])
                freq+=1
                found=True
                lines[i]=gameName + "," + str(freq) + "\n"
                
        #If its the first time a game has been played
        if(not found):
            lines.append(gameName + ",1\n")
        #
    
    #Overwrite the file with the updated frequencies
    with open(filename, "w") as f:
        f.writelines(lines)
    #
#

#modifies .user_total_wins.csv to update the number of times each user has won
#user_total_wins is of form: username, number of wins
def update_total_wins():
    filename=".user_total_wins.csv"
    os.system("touch " + filename)
    lines=None
    with open(filename, "r") as f:
        lines=f.readlines()
        found=False
        for i,line in enumerate(lines):
            if(line.split(",")[0]==winner):
                freq=int(line.split(",")[1]) #ignores trailing space characters so don't have to worry
                freq+=1
                found=True
                lines[i]=winner + "," + str(freq) + "\n"
                
        #If its the first time a user has won
        if(not found):
            lines.append(winner + ",1\n")
        #
    
    #Overwrite the file with the updated frequencies
    with open(filename, "w") as f:
        f.writelines(lines)
    #

#After each game concludes, game.py must append a row to history.csv containing: Winner, Loser, Date, and Game name.
def update_history():
    import time
    t=time.localtime()
    date=str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)
    with open("history.csv", "a") as f:
        f.write(winner + "," + loser + "," + date + "," + gameName + "\n")

sys.path.insert(0,"./games")
import tictactoe as ttt
import connect4 as cf	
import othello as oth

#variables to be updated after each game
winner=None
loser=None
#

def update():
    update_stats()
    update_game_frequencies()
    update_total_wins()
    update_history()
    
def show_leaderboard():
    pygame.display.quit()

    os.environ['SDL_VIDEO_CENTERED']='0'
    os.environ['SDL_VIDEO_WINDOW_POS']="0,"+str(round(height/6))

    pygame.display.init()
    global screen
    screen=pygame.display.set_mode((round(2*width/3),round(2*height/3)))

    pygame.display.set_caption("Leaderboard")
    
    running=True
    metric=None
    gameName=None

    #Buttons setup
    WinRect=pygame.Rect(100,100,200,50)
    LoseRect=pygame.Rect(100,200,200,50)
    RatioRect=pygame.Rect(100,300,200,50)
    ExitRect=pygame.Rect(100,400,200,50)

    TTTRect=pygame.Rect(400,100,200,50)
    OthelloRect=pygame.Rect(400,200,200,50)
    Connect4Rect=pygame.Rect(400,300,200,50)

    global font
    Wbutton=Button(screen,WinRect,"Wins","leaderboard")
    Lbutton=Button(screen,LoseRect,"Losses","leaderboard")
    Rbutton=Button(screen,RatioRect,"Ratio","leaderboard")
    Ebutton=Button(screen,ExitRect,"Exit","leaderboard")
    
	#def __init__(self,screen,rect,text,fill_color,border_color,mode):
    TTTbutton=Button(screen,TTTRect,"TicTacToe","leaderboard")
    Obutton=Button(screen,OthelloRect,"Othello","leaderboard")
    Cbutton=Button(screen,Connect4Rect,"Connect4","leaderboard")

    #
    #Button init - def __init__(self,screen,rect,text,mode):

    #number of times each game is played
    plays={"tictactoe":0,"connect4":0,"othello":0}
    #number of wins of each player
    total_wins={}

    while running:
        screen.fill((30,30,30))
        font=pygame.font.Font(None,36)
        #def draw(self,mouse_pos,mouse_pressed):
        mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()[0]
        Wbutton.draw(mouse_pos,mouse_pressed)
        Lbutton.draw(mouse_pos,mouse_pressed)
        Rbutton.draw(mouse_pos,mouse_pressed)
        Ebutton.draw(mouse_pos,mouse_pressed)

        TTTbutton.draw(mouse_pos,mouse_pressed)
        Obutton.draw(mouse_pos,mouse_pressed)
        Cbutton.draw(mouse_pos,mouse_pressed)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.MOUSEBUTTONUP:
                mousepos=event.pos
                
                if Wbutton.clicked(mousepos):
                    for i in Wbutton,Lbutton,Rbutton,Ebutton:
                        i.selected=False
                    Wbutton.selected=True
                    metric="wins"
                elif Lbutton.clicked(mousepos):
                    for i in Wbutton,Lbutton,Rbutton,Ebutton:
                        i.selected=False
                    Lbutton.selected=True
                    metric="losses"
                elif Rbutton.clicked(mousepos):
                    for i in Wbutton,Lbutton,Rbutton,Ebutton:
                        i.selected=False
                    Rbutton.selected=True
                    metric="ratio"
                elif Ebutton.clicked(mousepos):
                    running=False

                #game selection
                elif TTTbutton.clicked(mousepos):
                    for i in TTTbutton,Obutton,Cbutton:
                        i.selected=False
                    TTTbutton.selected=True
                    gameName="tictactoe"
                elif Obutton.clicked(mousepos):
                    for i in TTTbutton,Obutton,Cbutton:
                        i.selected=False
                    Obutton.selected=True
                    gameName="othello"
                elif Cbutton.clicked(mousepos):
                    for i in TTTbutton,Obutton,Cbutton:
                        i.selected=False
                    Cbutton.selected=True
                    gameName="connect4"

                #run command only if both selected
                if metric and gameName:
                    command="bash leaderboard.sh "+metric+" "+gameName
                    os.system(command)
                    
                    #storing game freq
                    with open('.game_frequencies.csv', mode='r') as file:
                        lines=file.readlines()
                    for line in lines:
                        plays[line.split(sep=',')[0].strip()]=int(line.split(sep=',')[1].strip())
                    #
                    #storing wins of top 5 players
                    with open('.top5.txt', mode='r') as file:
                        lines=file.readlines()
                        for line in lines:
                            total_wins[line.split()[0].strip()]=int(line.split()[1].strip())
                    #plot settings
                    fig, ax=plt.subplots(2,1, figsize=(8,8))
                    fig.canvas.manager.set_window_title("Game Stats")
                    plt.subplots_adjust(hspace=0.4)
                    fig.patch.set_facecolor('#FFF0F3')

                    #plot1: bar graph for game freq
                    bar_colors = ['#6C8EBF', '#93C47D', '#F6B26B']
                    ax[1].barh(plays.keys(),plays.values(), height=0.3, color=bar_colors)
                    ax[1].set_ylabel("Game",weight='bold')
                    ax[1].set_xlabel("Number of Plays",weight='bold')
                    ax[1].set_title("Number of Plays per Game", fontsize=16, weight='bold', pad=15)
                        # Hide the right and top spines
                    ax[1].spines.right.set_visible(False)
                    ax[1].spines.top.set_visible(False)


                    #plot2: pie chart for top 5 players
                    colors = ['#6C8EBF', '#93C47D', '#F6B26B', '#E06666', '#8E7CC3']
                    value,label,pct= ax[0].pie(
                        total_wins.values(), 
                        labels=total_wins.keys(),
                        autopct='%1.1f%%',
                        wedgeprops={'edgecolor': 'white'},
                        colors=colors
                    )
                        #bold the labels
                    for text in label:
                        text.set_fontweight('bold')
                    for text in pct:
                        text.set_color('white')
                    ax[0].set_title("Top 5 Players by Wins", fontsize=16, weight='bold', pad=15)
                    
                    plt.show()




        pygame.display.flip()
      
#menu buttons
#Button init - def __init__(self,screen,rect,text,mode):
tttRect=pygame.Rect(0,0,300,100)
tttRect.center=(round(width/2),200)
c4Rect=pygame.Rect(0,0,300,100)
c4Rect.center=(round(width/2),350)
othRect=pygame.Rect(0,0,300,100)
othRect.center=(round(width/2),500)

tttbutton=Button(screen,tttRect,"TicTacToe","menu")
c4button=Button(screen,c4Rect,"Connect4","menu")
othbutton=Button(screen,othRect,"Othello","menu")
#

play_again=True
while gameName!="exit":
    screen.fill((20,20,20))

    #mouse data
    mouse_pos=pygame.mouse.get_pos()
    mouse_pressed=pygame.mouse.get_pressed() #(left, middle, right) mouse button states - for us [0] is relevant
    #

    tttbutton.draw(mouse_pos,mouse_pressed)
    c4button.draw(mouse_pos,mouse_pressed)
    othbutton.draw(mouse_pos,mouse_pressed)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            gameName="exit" 

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                gameName="exit"

        if event.type==pygame.MOUSEBUTTONUP:
            pos=event.pos
            if tttbutton.clicked(pos):
                gameName="tictactoe"
                while play_again:
                    winner,loser,play_again=ttt.play(screen,clock,font,username1,username2)
                    update()
                    

            if c4button.clicked(pos):
                gameName="connect4"
                while play_again:
                    winner,loser,play_again=cf.play(screen,clock,font,username1,username2)
                    update()


            if othbutton.clicked(pos):
                gameName="othello"
                while play_again:
                    winner,loser,play_again=oth.play(screen,clock,font,username1,username2)
                    update()
    if not play_again:
        show_leaderboard()
        play_again=True
        screen=pygame.display.set_mode((width,height))
        os.environ['SDL_VIDEO_CENTERED']='1'
    pygame.display.flip()
    clock.tick(60)