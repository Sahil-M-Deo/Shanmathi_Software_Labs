import matplotlib.pyplot as plt
import numpy as np
from games.design_elements import *

#taking command line arguments
import sys
username1=sys.argv[1]
username2=sys.argv[2]
#

#game imports
sys.path.insert(0,"./games")
import games.tictactoe as ttt
import games.connect4 as cf	
import games.othello as oth
#

#centers the window
import os
os.environ['SDL_VIDEO_CENTERED']='1'
#

#pygame setup
import pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 50) #(font style,size)
pygame.display.set_caption("Game Hub")
#

#display sizes
info=pygame.display.Info()
width=info.current_w
height=info.current_h
screen=pygame.display.set_mode((width,height))
#

#time setup
clock=pygame.time.Clock()
import time
#

#current game
gameName=None
#

def toss():
    def gen_path(start,end,steps,noise_scale=0.02):
        t=np.linspace(0,1,steps)
        base=start+(end-start)*(3*t**2-2*t**3)

        noise=np.random.uniform(-noise_scale,noise_scale,steps)
        for i in range(1,steps):
            noise[i]=0.8*noise[i-1]+0.2*noise[i]

        seg=base+0.3*noise
        return np.clip(seg,0,1)

    start=0.5
    end=round(np.random.rand())

    path1=[0.1,0.8,0.4,0.9,0.05,1.0] #dramatic dance
    path2=[0.7,0.3,0.6,0.4,0.8,0.96,1.0] #Balanced battle

    if round(np.random.rand()):
        targets=path1
    else:
        targets=path2

    if(end==0):
        for i in range(len(targets)):
            targets[i]=1-targets[i]

    positions=[]
    curr=start
    base_steps=50
    speed=1.0

    for next in targets:
        steps=round(base_steps/speed)
        positions.extend(gen_path(curr,next,steps))
        curr=next
        speed*=1.05

    positions[-1]=end
    steps=len(positions)

    total_time=6.5
    seg_time=total_time/(steps)

    # -------- BAR SETUP --------
    bar_w,bar_h=width/1.5,height/7.5
    bar_x,bar_y=width/2,height/2
    bar_rect=Rect(bar_x-bar_w/2,bar_y-bar_h/2,bar_w,bar_h)
    
    #Player name boxes
    box_w,box_h=200,80

    left_box_rect=Rect(bar_x-bar_w/2-250,bar_y-box_h/2,box_w,box_h)
    right_box_rect=Rect(bar_x+bar_w/2+50,bar_y-box_h/2,box_w,box_h)
    #def __init__(self,screen,rect,text="",fill_color=GRAY_2,border_color=DULL_WHITE,border_thickness=3,border_radius=15):
    left_box=Box(screen,left_box_rect,username1,fill_color=BLACK,border_color=BLACK,font_color=TOSS_RED)
    right_box=Box(screen,right_box_rect,username2,fill_color=BLACK,border_color=BLACK,font_color=TOSS_BLUE)

    overlay=pygame.Surface(Coord(width,height),pygame.SRCALPHA)
    overlay.fill((*BLACK,180))
    
    font=pygame.font.Font(None,100)
    text=font.render("LET'S TOSS!",True,WHITE)
    text_rect=text.get_rect(center=Coord(bar_x,bar_y))

    start_time=time.time()
    while time.time()-start_time<2:
        screen.blit(overlay,(0,0))
        screen.blit(text,text_rect)
        pygame.display.flip()
        clock.tick(60)

    #ANIMATION SETUP
    idx=0
    seg_start=time.time()
    running=True
    
    screen.fill(GRAY_0)
    FNP_surf=pygame.Surface(Coord(bar_w,bar_h),pygame.SRCALPHA) #Fluid and Partition surface
    bar_surf=pygame.Surface(Coord(bar_w,bar_h),pygame.SRCALPHA) #The Bar surface acting as a transparent window
    bar_surf.fill((*BLACK,255))  #fully opaque black
    pygame.draw.rect(bar_surf,(*BLACK,0),Rect(0,0,bar_w,bar_h),border_radius=25) #the transparent window
    pygame.draw.rect(bar_surf,WHITE,Rect(0,0,bar_w,bar_h),5,border_radius=25) #border
    #
    
    while running:
        TIME=time.time()-seg_start
        idx=round(np.clip(TIME//seg_time,0,steps-2))
        f=np.clip((TIME-idx*seg_time)/seg_time,0,1)
        f=np.clip(f*f*(3-2*f),0,1) #smoother easing

        split_frac=np.clip((1-f)*positions[idx]+f*positions[idx+1],0,1)
        split=round(split_frac*bar_w)
        
        FNP_surf.fill(TOSS_RED,Rect(0,0,split,bar_h))
        FNP_surf.fill(TOSS_BLUE,Rect(split,0,bar_w-split,bar_h))
        
        #draw white partition of thickness 5
        pygame.draw.line(FNP_surf,WHITE,Coord(split,0),Coord(split,bar_h),5)

        FNP_surf.blit(bar_surf,(0,0))
        screen.blit(FNP_surf,bar_rect[:2])
        left_box.draw()
        right_box.draw()
        pygame.display.flip()
        clock.tick(60)

        if idx>=steps-2:
            running=False
    
    winner_name=username2 if end==0 else username1
    text=font.render(winner_name+' wins the toss!',True,TOSS_RED if end==1 else TOSS_BLUE)
    text_rect=text.get_rect(center=Coord(bar_x,bar_y))

    start_time=time.time()
    while time.time()-start_time<2:
        screen.blit(overlay,(0,0))
        screen.blit(text,text_rect)
        pygame.display.flip()
        clock.tick(60)
    return end

def time_control_menu():
    ClassicRect=Rect(0,0,300,100)
    ClassicRect.center=Coord(width/2,2*height/5)
    ClassicButton=Button(screen,ClassicRect,"Classic","menu")
    BlitzRect=Rect(0,0,300,100)
    BlitzRect.center=Coord(width/2,3*height/5)
    BlitzButton=Button(screen,BlitzRect,"Blitz","menu")
    tickrate=60
    menu=True
    while menu:
        screen.fill(BLACK)
        mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()[0] #(left, middle, right) mouse button states - for us [0] is relevant
        ClassicButton.draw(mouse_pos,mouse_pressed)
        BlitzButton.draw(mouse_pos,mouse_pressed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #LARISSA
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit() #LARISSA

            if event.type == pygame.MOUSEBUTTONUP:
                mousepos=event.pos
                if ClassicButton.mouse_over(mousepos):
                    return "classic"
                if BlitzButton.mouse_over(mousepos):
                    return "blitz"
        pygame.display.flip()
        clock.tick(tickrate)

def update_stats():
    if(winner=="TIE"):
        return 
    filepath=".user_files/.stats_"+gameName+".csv"
    os.system("touch " + filepath) 
    lines=None #list of lines
    with open(filepath, "r") as f:
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
    with open(filepath, "w") as f:
        f.writelines(lines)
    #
    
#game_frequencies is of form: game name, number of times played
#modifies .game_frequencies.csv to update the number of times each game has been played
def update_game_frequencies():
    filepath=".user_files/.game_frequencies.csv"
    os.system("touch " + filepath) #create the file if it doesn't exist
    lines=None
    with open(filepath, "r") as f:
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
    with open(filepath, "w") as f:
        f.writelines(lines)
    #
#

#modifies .user_total_wins.csv to update the number of times each user has won
#user_total_wins is of form: username, number of wins
def update_total_wins():
    if(winner=="TIE"):
        return 
    filepath=".user_files/.user_total_wins.csv"
    os.system("touch " + filepath)
    lines=None
    with open(filepath, "r") as f:
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
    with open(filepath, "w") as f:
        f.writelines(lines)
    #

#After each game concludes, game.py must append a row to .history.csv containing: Winner, Loser, Date, and Game name.
def update_history():
    t=time.localtime()
    date=str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)
    with open(".user_files/.history.csv", "a") as f:
        f.write(winner + "," + loser + "," + date + "," + gameName + "\n")

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
    button_width=200
    button_height=50
    WinRect=Rect(100,100,button_width,button_height)
    LoseRect=Rect(100,200,button_width,button_height)
    RatioRect=Rect(100,300,button_width,button_height)
    ExitRect=Rect(100,400,button_width,button_height)

    TTTRect=Rect(400,100,button_width,button_height)
    OthelloRect=Rect(400,200,button_width,button_height)
    Connect4Rect=Rect(400,300,button_width,button_height)
    ChartsRect=Rect(400,400,button_width,button_height)

    #Button constructor -> def __init__(self,screen,rect,text,fill_color=GRAY_2,border_color=DULL_WHITE,mode="menu",border_thickness=3,border_radius=15):
    Lbutton=Button(screen,LoseRect,"Losses",mode="leaderboard")
    Rbutton=Button(screen,RatioRect,"Ratio",mode="leaderboard")
    Ebutton=Button(screen,ExitRect,"Exit",mode="menu")
    Wbutton=Button(screen,WinRect,"Wins",mode="leaderboard")
    TTTbutton=Button(screen,TTTRect,"TicTacToe",mode="leaderboard")
    Obutton=Button(screen,OthelloRect,"Othello",mode="leaderboard")
    Cbutton=Button(screen,Connect4Rect,"Connect4",mode="leaderboard")
    Charts_button=Button(screen,ChartsRect,"See Charts",mode="menu")
    #

    #number of times each game is played for charts
    plays={"tictactoe":0,"connect4":0,"othello":0}
    #number of wins of each player for charts
    total_wins={}

    while running:
        screen.fill((30,30,30))
        global font
        font=pygame.font.Font(None,36)
        #def draw(self,mouse_pos,mouse_pressed):
        mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()[0]
        #
        
        Wbutton.draw(mouse_pos,mouse_pressed)
        Lbutton.draw(mouse_pos,mouse_pressed)
        Rbutton.draw(mouse_pos,mouse_pressed)
        Ebutton.draw(mouse_pos,mouse_pressed)
        TTTbutton.draw(mouse_pos,mouse_pressed)
        Obutton.draw(mouse_pos,mouse_pressed)
        Cbutton.draw(mouse_pos,mouse_pressed)
        Charts_button.draw(mouse_pos,mouse_pressed)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.MOUSEBUTTONUP:
                mousepos=event.pos
                
                if Wbutton.mouse_over(mousepos):
                    for i in Wbutton,Lbutton,Rbutton:
                        i.selected=False
                    Wbutton.selected=True
                    metric="wins"
                elif Lbutton.mouse_over(mousepos):
                    for i in Wbutton,Lbutton,Rbutton:
                        i.selected=False
                    Lbutton.selected=True
                    metric="losses"
                elif Rbutton.mouse_over(mousepos):
                    for i in Wbutton,Lbutton,Rbutton:
                        i.selected=False
                    Rbutton.selected=True
                    metric="ratio"
                elif Ebutton.mouse_over(mousepos):
                    running=False

                #game selection
                elif TTTbutton.mouse_over(mousepos):
                    for i in TTTbutton,Obutton,Cbutton:
                        i.selected=False
                    TTTbutton.selected=True
                    gameName="tictactoe"
                elif Obutton.mouse_over(mousepos):
                    for i in TTTbutton,Obutton,Cbutton:
                        i.selected=False
                    Obutton.selected=True
                    gameName="othello"
                elif Cbutton.mouse_over(mousepos):
                    for i in TTTbutton,Obutton,Cbutton:
                        i.selected=False
                    Cbutton.selected=True
                    gameName="connect4"

                #run command only if both selected
                if metric and gameName:
                    command="bash leaderboard.sh "+metric+" "+gameName
                    os.system(command)
                    metric=None
                    gameName=None
                    for i in TTTbutton,Obutton,Cbutton,Wbutton,Lbutton,Rbutton:
                        i.selected=False

                if Charts_button.mouse_over(mouse_pos):
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
                    fig, ax=plt.subplots(2,1)
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
#Buttondef __init__(self,screen,rect,text,fill_color=GRAY_2,border_color=DULL_WHITE,mode="menu",border_thickness=3,border_radius=15):
tttRect=Rect(0,0,300,100)
tttRect.center=Coord(width/2,200)
c4Rect=Rect(0,0,300,100)
c4Rect.center=Coord(width/2,350)
othRect=Rect(0,0,300,100)
othRect.center=Coord(width/2,500)
tttbutton=Button(screen,tttRect,"TicTacToe","menu")
c4button=Button(screen,c4Rect,"Connect4","menu")
othbutton=Button(screen,othRect,"Othello","menu")
#

#def show_main_menu():
#    pygame.display.init()
#    global screen
#    screen=pygame.display.set_mode((round(2*width/3),round(2*height/3)))

exit_status="play_game"
while gameName!="exit":
    screen.fill(BLACK)
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

        blitz_turn_time=10
        if event.type==pygame.MOUSEBUTTONUP:
            if tttbutton.mouse_over(mouse_pos):
                gameName="tictactoe"
                while exit_status=="play_game":
                    time_control=time_control_menu()
                    turn=toss()
                    winner,loser,exit_status=ttt.play(screen,clock,font,username1,username2,turn,time_control,blitz_turn_time)
                    if not (exit_status=="incomplete"):
                        update()
                    
            if c4button.mouse_over(mouse_pos):
                gameName="connect4"
                while exit_status=="play_game":
                    time_control=time_control_menu()
                    turn=toss()
                    winner,loser,exit_status=cf.play(screen,clock,font,username1,username2,turn,time_control,blitz_turn_time)
                    if not (exit_status=="incomplete"):
                        update()


            if othbutton.mouse_over(mouse_pos):
                gameName="othello"
                while exit_status=="play_game":
                    time_control=time_control_menu()
                    turn=toss()
                    winner,loser,exit_status=oth.play(screen,clock,font,username1,username2,turn,time_control,blitz_turn_time)
                    if not (exit_status=="incomplete"):    
                        update()
                        
    if not (exit_status=="play_game"):
        show_leaderboard()
        play_again=True
        os.environ['SDL_VIDEO_CENTERED']='1'
    pygame.display.flip()
    clock.tick(60)