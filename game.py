from datetime import date
import matplotlib
import numpy as np

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

#rect is pygame.Rect object (x,y,width,height)
#text is the text to be displayed on the button
#is_selected is whether the button is highlighted or not
def draw_leaderboard_button(rect,text,is_selected):
    if is_selected:
        fill_color=(100,100,120)      # same hover-style brightness
        border_color=(220,220,220)    # brighter version of border
    else:
        fill_color=(70,70,70)
        border_color=(150,150,150)

    pygame.draw.rect(screen,fill_color,rect,border_radius=15)
    pygame.draw.rect(screen,border_color,rect,3,border_radius=15)

    txt=font.render(text,True,"white")
    screen.blit(txt,txt.get_rect(center=rect.center))

#rect is pygame.Rect object (x,y,width,height)
#text is the text to be displayed on the button
def draw_menu_button(rect,text,mouse_pos,mouse_pressed):
    offset=0
    if rect.collidepoint(mouse_pos):
        if mouse_pressed:
            fill_color=(60,60,60)        # pressed
            offset=2
        else:
            fill_color=(100,100,120)     # hover
    else:
        fill_color=(70,70,70)            # idle

    border_color=(150,150,150)

    r=rect.move(0,offset) #button pressed down effect 

    pygame.draw.rect(screen,fill_color,r,border_radius=15)
    pygame.draw.rect(screen,border_color,r,3,border_radius=15)

    txt=font.render(text,True,"white")
    screen.blit(txt,txt.get_rect(center=r.center))

sys.path.insert(0,"./games")
import tictactoe as ttt
import connect4 as cf	
#import othello as oth

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
    pygame.display.set_caption("Leaderboard")
    global screen
    screen=pygame.display.set_mode((round(2*width/3),round(2*height/3)))
    running=True
    metric=None
    gameName=None

    #Buttons setup
    Wbutton=pygame.Rect(100,100,200,50)
    Lbutton=pygame.Rect(100,200,200,50)
    Rbutton=pygame.Rect(100,300,200,50)
    Ebutton=pygame.Rect(100,400,200,50)

    TTTbutton=pygame.Rect(400,100,200,50)
    Obutton=pygame.Rect(400,200,200,50)
    Cbutton=pygame.Rect(400,300,200,50)
    #

    while running:
        screen.fill((30,30,30))

        #draw metric buttons
        draw_leaderboard_button(Wbutton,"Wins",metric=="wins")
        draw_leaderboard_button(Lbutton,"Losses",metric=="losses")
        draw_leaderboard_button(Rbutton,"Ratio",metric=="ratio")
        draw_leaderboard_button(Ebutton,"Exit",False)

        #draw game buttons
        draw_leaderboard_button(TTTbutton,"TicTacToe",gameName=="tictactoe")
        draw_leaderboard_button(Obutton,"Othello",gameName=="othello")
        draw_leaderboard_button(Cbutton,"Connect4",gameName=="connect4")

        font=pygame.font.Font(None,36)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.MOUSEBUTTONDOWN:
                mousepos=event.pos

                #metric selection
                if Wbutton.collidepoint(mousepos):
                    metric="wins"
                elif Lbutton.collidepoint(mousepos):
                    metric="losses"
                elif Rbutton.collidepoint(mousepos):
                    metric="ratio"
                elif Ebutton.collidepoint(mousepos):
                    running=False

                #game selection
                elif TTTbutton.collidepoint(mousepos):
                    gameName="tictactoe"
                elif Obutton.collidepoint(mousepos):
                    gameName="othello"
                elif Cbutton.collidepoint(mousepos):
                    gameName="connect4"

                #run command only if both selected
                if metric in ["wins","losses","ratio"] and gameName!=None:
                    command="bash leaderboard.sh "+metric+" "+gameName
                    os.system(command)

        pygame.display.flip()
      
play_again=True
while gameName!="exit":
    screen.fill((20,20,20))

    #mouse data
    mouse_pos=pygame.mouse.get_pos()
    mouse_pressed=pygame.mouse.get_pressed() #(left, middle, right) mouse button states - for us [0] is relevant
    #

    #menu buttons
    ttt_btn=pygame.Rect(0,0,300,100)
    ttt_btn.center=(round(width/2),200)

    c4_btn=pygame.Rect(0,0,300,100)
    c4_btn.center=(round(width/2),350)

    oth_btn=pygame.Rect(0,0,300,100)
    oth_btn.center=(round(width/2),500)

    draw_menu_button(ttt_btn,"Tic Tac Toe", mouse_pos, mouse_pressed[0])
    draw_menu_button(c4_btn,"Connect 4", mouse_pos, mouse_pressed[0])
    draw_menu_button(oth_btn,"Othello", mouse_pos, mouse_pressed[0])
    #

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
                while play_again:
                    winner,loser,play_again=ttt.play(screen,clock,font,username1,username2)
                    update()
                    

            if c4_btn.collidepoint(pos):
                gameName="connect4"
                while play_again:
                    winner,loser,play_again=cf.play(screen,clock,font,username1,username2)
                    update()


            if oth_btn.collidepoint(pos):
                gameName="othello"
                while play_again:
                    winner,loser,play_again=oth.play(screen,clock,font,username1,username2)
                    update()
    if not play_again:
        show_leaderboard()
        play_again=True
        screen=pygame.display.set_mode((width,height))
    pygame.display.flip()
    clock.tick(60)