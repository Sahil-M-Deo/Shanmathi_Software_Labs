from datetime import date
import sys
import os
import pygame
import matplotlib
import numpy as np

username1=sys.argv[1]
username2=sys.argv[2]

print("Welcome to the game, " + username1 + " and " + username2 + "!")
gameName=None

sys.path.insert(0,"./games")
import tictactoe as ttt
import connect4 as cf	
#import othello as oth
#main game loop, where the user can select which game to play and the game will be executed accordingly
#pygame setup
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 50) #(font style,size)
#
info=pygame.display.Info()
width=info.current_w
height=info.current_h
screen=pygame.display.set_mode((width,height))
pygame.display.set_caption("Game Hub")
clock=pygame.time.Clock()

#modifies stats_{gameName}.csv to update the number of wins and losses for each player
def update_stats():
    filename=".stats_"+gameName+".csv"
    os.system("touch " + filename) 
    lines=None
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
                lines[idx]=winner + "," + str(wins) + "," + str(losses) + "," + str(wins/losses) if losses!=0 else "inf" + "\n"
            elif(i.split(",")[0]==loser):
                wins=int(i.split(",")[1])
                losses=int(i.split(",")[2])
                losses+=1
                loserfound=True
                lines[idx]=loser + "," + str(wins) + "," + str(losses) + "," + str(wins/losses)+ "\n"
        if(not winnerfound):
            lines.append(winner + ",1,0,inf\n")
        if(not loserfound):
            lines.append(loser + ",0,1,0\n")
    with open(filename, "w") as f:
        f.writelines(lines)
def update_game_frequencies():
    #modifies game_frequencies.csv to update the number of times each game has been played
    filename=".game_frequencies.csv"
    os.system("touch " + filename) 
    lines=None
    with open(filename, "r") as f:
        lines=f.readlines()
        found=False
        for i in lines:
            if(i.split(",")[0]==gameName):
                freq=int(i.split(",")[1])
                freq+=1
                found=True
                i=gameName + "," + str(freq) + "\n"
        if(not found):
            lines.append(gameName + ",1\n")
    with open(filename, "w") as f:
        f.writelines(lines)

def update_total_wins():
    #modifies user_total_wins.csv to update the number of times each user has won
    filename=".user_total_wins.csv"
    os.system("touch " + filename)
    lines=None
    with open(filename, "r") as f:
        lines=f.readlines()
        found=False
        for i in lines:
            if(i.split(",")[0]==winner):
                freq=int(i.split(",")[1])
                freq+=1
                found=True
                i=winner + "," + str(freq) + "\n"
        if(not found):
            lines.append(winner + ",1\n")
    with open(filename, "w") as f:
        f.writelines(lines)

#username,number of wins, number of losses, and Win/Loss ratio
#game_frequencies is of form: game name, number of times played
#user_total_wins is of form: username, number of wins


#After each game concludes, game.py must append a row to history.csv containing: Winner, Loser, Date, and Game name.
def update_history():
    import time
    t=time.localtime()
    date=str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)
    with open("history.csv", "a") as f:
        f.write(winner + "," + loser + "," + date + "," + gameName + "\n")

def draw_button(rect,text,is_selected):
    if is_selected:
        color=(255,255,0)   # highlight color
    else:
        color=(100,100,100)

    pygame.draw.rect(screen,color,rect)

    txt=font.render(text,True,(0,0,0))
    screen.blit(txt,txt.get_rect(center=rect.center))

def draw_button2(rect,text):
    pygame.draw.rect(screen,(70,70,70),rect,border_radius=15)
    pygame.draw.rect(screen,(150,150,150),rect,3,border_radius=15)
    txt=font.render(text,True,"white")
    screen.blit(txt,txt.get_rect(center=rect.center))

winner=None
loser=None
while gameName==None:
    screen.fill((20,20,20))

    # Buttons
    ttt_btn=pygame.Rect(0,0,300,100)
    ttt_btn.center=(width//2,200)

    c4_btn=pygame.Rect(0,0,300,100)
    c4_btn.center=(width//2,350)

    oth_btn=pygame.Rect(0,0,300,100)
    oth_btn.center=(width//2,500)

    draw_button2(ttt_btn,"Tic Tac Toe")
    draw_button2(c4_btn,"Connect 4")
    draw_button2(oth_btn,"Othello")

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            gameName="exit" 

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                gameName="exit"

        if event.type==pygame.MOUSEBUTTONUP:
            pos=event.pos
            if ttt_btn.collidepoint(pos):
                gameName="tictactoe"
                ttt.play(screen,clock,font,username1,username2)

            if c4_btn.collidepoint(pos):
                gameName="connect4"
                play_again=True
                while play_again:
                    winner,loser,play_again=cf.play(screen,clock,font,username1,username2)
                    update_stats()
                    update_game_frequencies()
                    update_total_wins()
                    update_history()

            if oth_btn.collidepoint(pos):
                gameName="othello"
                #oth.play(screen,clock,font,username1,username2)

    pygame.display.flip()
    clock.tick(60)

def show_leaderboard():
    pygame.display.set_caption("Leaderboard")
    screen=pygame.display.set_mode((width/2,height/2))
    running=True
    metric=None
    Wbutton=pygame.Rect(100,100,200,50)
    Lbutton=pygame.Rect(100,200,200,50)
    Rbutton=pygame.Rect(100,300,200,50)
    Ebutton=pygame.Rect(100,400,200,50)

    while running:
        screen.fill((30,30,30))
        draw_button(Wbutton,"Wins",metric=="wins")
        draw_button(Lbutton,"Losses",metric=="losses")
        draw_button(Rbutton,"Ratio",metric=="ratio")
        draw_button(Ebutton,"See Charts",metric=="exit")
        font=pygame.font.Font(None,36)
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False
            #pygame.Rect(x, y, width, height)
            if event.type==pygame.MOUSEBUTTONDOWN:
                mousepos=event.pos
                if Wbutton.collidepoint(mousepos):
                    metric="wins"
                elif Lbutton.collidepoint(mousepos):
                    metric="losses"
                elif Rbutton.collidepoint(mousepos):
                    metric="ratio"
                elif Ebutton.collidepoint(mousepos):
                    metric="exit"
                else:
                    metric=None
                if metric in ["wins","losses","ratio"]:
                    command="bash leaderboard.sh " + metric + " " + gameName
                    os.system(command)
        if(metric=="exit"):
            running=False
        pygame.display.flip()	

show_leaderboard()