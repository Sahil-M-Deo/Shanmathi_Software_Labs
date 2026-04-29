import pygame
import numpy as np
import time

from classGame import *
from design_elements import *

def play(screen,clock,font,username1,username2,turn,game_mode,blitz_turn_time):
    
    exit_status="main_menu" #to check if user wants to play again or go to main menu after a game ends
    name_of_winner=None
    name_of_loser=None
    
    if(turn==0):
        username1,username2=username2,username1
    
    #username1 is turn=True represented by Red
    #username2 is turn=False represented by Yellow
    
    pygame.display.set_caption("Connect 4")
    
    #window variables
    info=pygame.display.Info()
    width=info.current_w
    height=info.current_h
    tickrate=60
    bg_color=BLACK
    #

    #time related variables
    blitz_turn_time=10
    #

    #initialising game board
    
    def checkWin(self,current_row,current_column):
        streak=4

        def count(arr):
            
            matches=(arr==self.turn)
            return np.argmax(~matches) if not matches.all() else len(matches)

        # vertical
        up=count(self.board[max(0,current_row-streak):current_row,current_column][::-1])
        down=count(self.board[current_row+1:min(self.boardHEIGHT,current_row+streak+1),current_column])

        # horizontal
        left=count(self.board[current_row,max(0,current_column-streak):current_column][::-1])
        right=count(self.board[current_row,current_column+1:min(self.boardWIDTH,current_column+streak+1)])

        # diagonal
        diag=self.board.diagonal(offset=current_column-current_row)
        idx=min(current_row,current_column)

        d1_left=count(diag[max(0,idx-streak):idx][::-1])
        d1_right=count(diag[idx+1:idx+1+streak])

        # / diagonal
        flipped=np.fliplr(self.board)
        colf=self.boardWIDTH-1-current_column

        diag=flipped.diagonal(offset=colf-current_row)
        idx=min(current_row,colf)

        d2_left=count(diag[max(0,idx-streak):idx][::-1])
        d2_right=count(diag[idx+1:idx+1+streak])

        if (up+down+1>=streak or left+right+1>=streak or d1_left+d1_right+1>=streak or d2_left+d2_right+1>=streak):
            return True
        return False
    
    game = Game(checkWin,7,7,Size(105))
    x_start=Size(width/2-game.boardWIDTH*game.cell_size/2)
    x_end=Size(width/2+game.boardWIDTH*game.cell_size/2)
    y_start=Size(height-game.boardHEIGHT*game.cell_size+69)/2
    y_end=Size(height+game.boardHEIGHT*game.cell_size)/2
    r=Size(game.cell_size*0.415)
    filled=0 #number of filled cells
    #

    BOARD_SURFACE=pygame.Surface(Coord(game.boardWIDTH*game.cell_size,game.boardHEIGHT*game.cell_size),pygame.SRCALPHA)
    BOARD_SURFACE.fill((*BLACK,0))
    pygame.draw.rect(BOARD_SURFACE,BOARD_BLUE,Rect(0,0,game.boardWIDTH*game.cell_size,game.boardHEIGHT*game.cell_size))
    for row in range(game.boardHEIGHT):
            for col in range(game.boardWIDTH):
                cx=col*game.cell_size+game.cell_size/2
                cy=row*game.cell_size+game.cell_size/2
                pygame.draw.circle(BOARD_SURFACE,(*BLACK,0),Coord(cx,cy),int(r))

    def draw_board():
        screen.blit(BOARD_SURFACE,Coord(x_start,y_start))

    red_disc=None
    yellow_disc=None
    hover_yellow_disc=None
    hover_red_disc=None
    def init_discs(r):
        nonlocal red_disc
        nonlocal yellow_disc
        nonlocal hover_yellow_disc
        nonlocal hover_red_disc
        r*=1.68

        red_disc_img=pygame.image.load("images/red_disc.png").convert_alpha()
        yellow_disc_img=pygame.image.load("images/yellow_disc.png").convert_alpha()

        red_disc=pygame.transform.smoothscale(red_disc_img,Coord(2*r,2*r))
        red_disc.set_alpha(255)

        yellow_disc=pygame.transform.smoothscale(yellow_disc_img,Coord(2*r,2*r))
        yellow_disc.set_alpha(255)

        hover_yellow_disc=pygame.transform.smoothscale(yellow_disc_img,Coord(2*r,2*r))
        hover_yellow_disc.set_alpha(135)

        hover_red_disc=pygame.transform.smoothscale(red_disc_img,Coord(2*r,2*r))
        hover_red_disc.set_alpha(135)

    init_discs(int(r))

    def draw_disc(surface,color,coords,hover=False):
        cx,cy=coords
        if hover:
            if color==RED:
                img=hover_red_disc
            else:
                img=hover_yellow_disc
        else:
            if color==RED:
                img=red_disc
            else:
                img=yellow_disc
        rect=img.get_rect(center=(cx,cy))
        surface.blit(img,rect)
        

    def hover(row,col,turn):
        if turn:
            hover_color=RED
        else:
            hover_color=YELLOW
        x_pos=x_start+col*game.cell_size+game.cell_size/2
        y_pos=y_start+row*game.cell_size+game.cell_size/2
        draw_disc(screen,hover_color,Coord(x_pos,y_start-game.cell_size/2))
        draw_disc(screen,hover_color,Coord(x_pos,y_pos),hover=True)

    running=True
    col_filled=np.zeros(game.boardWIDTH,dtype=int) #number of filled cells in each column

    if game_mode=="blitz":
        #init timers
        left_x=x_start-1.5*game.cell_size
        right_x=x_end+0.6*game.cell_size
        T1=Timer(screen,font,left_x,y_start-40,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        T2=Timer(screen,font,right_x,y_start-40,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        #

    discs=[]
    def move(row,col):
        nonlocal filled
        filled+=1
        TIME=time.time()
        col_filled[col]+=1
        
        game.board[row][col]=game.turn

        centre_x=x_start+col*game.cell_size+game.cell_size/2
        centre_y=y_start+row*game.cell_size+game.cell_size/2

        if(game.turn):
            disc_info=(*Coord(centre_x,centre_y),TIME,RED)
        else:
            disc_info=(*Coord(centre_x,centre_y),TIME,YELLOW)
        discs.append(disc_info)

        if game_mode=="blitz":
            if filled>1:
                T1.switchTurn()
            T2.switchTurn()
            
        if game.checkWin(row,col):
            end(game.turn)
        game.switchTurn()
    #

    game_over = False
    finalDisplay=None
    finalColor=None

    def end(winner):
        nonlocal finalDisplay
        nonlocal game_over
        nonlocal finalColor
        nonlocal name_of_winner
        nonlocal name_of_loser

        if game_mode=="blitz":
            T1.end()
            T2.end()

        game_over=True
        if winner == 1:
            name_of_winner=username1
            name_of_loser=username2
            finalDisplay=username1+" WINS!"
            finalColor="green"
        elif winner == 0:
            name_of_winner=username2
            name_of_loser=username1
            finalDisplay=username2+" WINS!"
            finalColor="green"
        else:
            name_of_winner="TIE"
            name_of_loser="TIE"
            finalDisplay="IT'S A TIE!"
            finalColor="grey"

   #popup box
    box_width=500
    box_height=300
    box_rect=Rect(0,0,box_width,box_height)
    box_rect.center=Coord(width/2,height/2)
    #
    
    #The two buttons
    btn_w=180
    btn_h=60
    play_again_rect=Rect(0,0,btn_w,btn_h)
    menu_rect=Rect(0,0,btn_w,btn_h)
    play_again_rect.center=Coord(box_rect.centerx-110,box_rect.bottom-80)
    menu_rect.center=(box_rect.centerx+110,box_rect.bottom-80)
    #
    
    #Box init: def __init__(self,screen,rect,text="",fill_color=GRAY_2,border_color=DULL_WHITE,border_thickness=3,border_radius=15):
    popup=Box(screen,box_rect,"",GRAY_4,DULL_WHITE,2,10)
    #def __init__(self,screen,rect,text,fill_color,border_color,mode):
    BTN_play_again=Button(screen,play_again_rect,"PLAY AGAIN",CALM_BLUE,DULL_WHITE,"menu")
    main_menu=Button(screen,menu_rect,"MAIN MENU",CUTE_RED,DULL_WHITE,"menu")

    FADE_SURFACE=pygame.Surface((screen.get_size()),pygame.SRCALPHA)
    FADE_SURFACE.fill((*BLACK,180))
    font_big=pygame.font.Font(None,80)

    most_recent_time=0
    most_recent_column=-1

    g=2500
    fall_time=int(((game.boardHEIGHT*game.cell_size)*3/g)**0.5)
    #main game loop:
    while running:
        screen.fill(bg_color)
        TIME=time.time()
        if game_mode=="blitz":
            if not T1.update():
                end(0)
            if not T2.update():
                end(1)

        #simulate falling - TIME-t = time since release, using 1/2 g t^2
        for cx,cy,t,draw_color in discs:
            y_curr=np.clip(int(y_start+0.5*g*(TIME-t)**2-game.cell_size/2),int(-game.cell_size/2),int(cy))
            draw_disc(screen,draw_color,(cx,y_curr))
        #

        x,y=mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()[0]
        col=int((x-x_start)//game.cell_size)

        if not game_over:
            if(0<=col<game.boardWIDTH):
                row=game.boardHEIGHT-1-col_filled[col]
                if TIME-most_recent_time>fall_time or most_recent_column!=col:                
                    hover(row,col,game.turn)
            # Board:
            draw_board()
                
            if filled==game.boardHEIGHT*game.boardWIDTH:
                game_over=True
                end(-1)
        else:
            # Board:
            draw_board()
            if TIME-most_recent_time>fall_time:
                #dark overlay
                screen.blit(FADE_SURFACE,(0,0))

                #def draw(self,mouse_pos,mouse_pressed):
                #play again and main menu buttons
                popup.draw()
                text=font_big.render(finalDisplay,True,finalColor)
                screen.blit(text,text.get_rect(center=Coord(box_rect.centerx,box_rect.top+80)))
                BTN_play_again.draw(mouse_pos,mouse_pressed)
                main_menu.draw(mouse_pos,mouse_pressed)

        
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                if not game_over:
                    return("","","incomplete")
                else:
                    return(name_of_winner,name_of_loser,"main_menu")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not game_over:
                        return("","","incomplete")
                    else:
                        return(name_of_winner,name_of_loser,"main_menu")
            
            if not game_over:
                if event.type == pygame.MOUSEBUTTONUP:
                    if col<game.boardWIDTH and col>=0 and col_filled[col]<game.boardHEIGHT:
                        if TIME-most_recent_time>fall_time or most_recent_column!=col:
                            row=game.boardHEIGHT-1-col_filled[col]
                            move(row,col)
                            most_recent_column=col
                            most_recent_time=TIME
            else:
                if event.type==pygame.MOUSEBUTTONUP:
                    if TIME-most_recent_time>fall_time:
                        if BTN_play_again.mouse_over(mouse_pos):
                            exit_status="play_game"
                            running=False #go back to game.py, (stats will be updated and shown there)
                        if main_menu.mouse_over(mouse_pos):
                            running=False      # go back to game.py, (stats will be updated and shown there)
                                   

        if game_mode=="blitz":
            T1.display()
            T2.display()
                           

        pygame.display.flip()
        clock.tick(tickrate)
    return name_of_winner,name_of_loser,exit_status