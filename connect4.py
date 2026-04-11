import pygame
import numpy as np
import math
import time

from classGame import *
from design_elements import *

def cap(x,low,high):
    if x<low:
        return low
    elif x>high:
        return high
    else:
        return x
    
def play(screen,clock,font,username1,username2):
    
    play_again=False #to check if user wants to play again after a game ends
    name_of_winner=None
    name_of_loser=None
    
    pygame.display.set_caption("Connect 4")
    #window variables
    info=pygame.display.Info()
    width=info.current_w
    height=info.current_h
    tickrate=60
    bg_color=BLACK
    #

    
    game_mode = None

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
    
    game = Game(checkWin,7,7,round(100*height/864))
    x_start=round(width/2-(game.boardWIDTH/2)*game.cell_size)
    x_end=round(width/2+(game.boardWIDTH/2)*game.cell_size)
    y_start=round(height/2-(game.boardHEIGHT/2)*game.cell_size+game.cell_size*0.4)
    y_end=y_start+(game.boardHEIGHT*game.cell_size)
    r=round(game.cell_size/2-2) #radius of circle
    filled=0 #number of filled cells
    #

    #username1 is turn=True represented by Red
    #username2 is turn=False represented by Yellow

    ClassicRect=pygame.Rect(0,0,round(300*height/864),round(100*height/864))
    ClassicRect.center=(round(width/2),round(2*height/5))
    ClassicButton=Button(screen,ClassicRect,"Classic","menu")

    BlitzRect=pygame.Rect(0,0,round(300*height/864),round(100*height/864))
    BlitzRect.center=(round(width/2),round(3*height/5))
    BlitzButton=Button(screen,BlitzRect,"Blitz","menu")

    menu = True
    while menu:
        screen.fill(bg_color)
        mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()[0] #(left, middle, right) mouse button states - for us [0] is relevant
        ClassicButton.draw(mouse_pos,mouse_pressed)
        BlitzButton.draw(mouse_pos,mouse_pressed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = False
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos=event.pos
                if ClassicButton.clicked(mousepos):
                    game_mode="classic"
                    menu=False
                if BlitzButton.clicked(mousepos):
                    game_mode="blitz"
                    menu=False
                    
        pygame.display.flip()
        clock.tick(tickrate)

    board_surface=pygame.Surface((game.boardWIDTH*game.cell_size,game.boardHEIGHT*game.cell_size),pygame.SRCALPHA)
    def draw_board():
        board_surface.fill((0,0,0,0))
        # draw board rectangle
        pygame.draw.rect(board_surface,BLUE,(0,0,game.boardWIDTH*game.cell_size,game.boardHEIGHT*game.cell_size))

        # draw holes
        for row in range(game.boardHEIGHT):
            for col in range(game.boardWIDTH):
                cx=round(col*game.cell_size+game.cell_size/2)
                cy=round(row*game.cell_size+game.cell_size/2)
                pygame.draw.circle(board_surface,(0,0,0,0),(cx,cy),r)
        screen.blit(board_surface,(x_start,y_start))

    yellow_disc_img=None
    red_disc_img=None
    def draw_disc(surface,color,coords,r,opacity=255):
        r*=1.66
        nonlocal yellow_disc_img,red_disc_img
        cx,cy=coords
        if color==RED:
            if red_disc_img is None:
                red_disc_img=pygame.image.load("red_disc.png").convert_alpha()
            red_disc=pygame.transform.smoothscale(red_disc_img,(2*r,2*r))
            red_disc.set_alpha(opacity)
            surface.blit(red_disc,(round(cx-r),round(cy-r)))
        else:
            if yellow_disc_img is None:
                yellow_disc_img=pygame.image.load("yellow_disc.png").convert_alpha()
            yellow_disc=pygame.transform.smoothscale(yellow_disc_img,(2*r,2*r))
            yellow_disc.set_alpha(opacity)
            surface.blit(yellow_disc,(round(cx-r),round(cy-r)))
        

    def hover(row,col,turn):
        OPACITY=135
        hover_rbgOPACITY=None
        if turn:
            hover_color=RED
            hover_rbgOPACITY=(255,0,0,OPACITY)
        else:
            hover_color=YELLOW
            hover_rbgOPACITY=(255,255,0,OPACITY)
        x_pos=round(x_start+col*game.cell_size+game.cell_size/2)
        y_pos=round(y_start+row*game.cell_size+game.cell_size/2)
        draw_disc(screen,hover_color,(x_pos,round(y_start-game.cell_size/2)),r)
        draw_disc(screen,hover_color,(x_pos,y_pos),r,opacity=OPACITY)

    running=True
    col_filled=np.zeros(game.boardWIDTH,dtype=int) #number of filled cells in each column

    if game_mode=="blitz":
        #init timers
        left_x = round(x_start-1.5*game.cell_size)
        right_x = round(x_end+0.6*game.cell_size)
        T1=Timer(screen,font,left_x,y_start-0.2*game.cell_size,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        T2=Timer(screen,font,right_x,y_start-0.2*game.cell_size,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        #

    discs=[]
    def move(row,col):
        nonlocal filled
        filled+=1
        
        col_filled[col]+=1
        
        game.board[row][col]=game.turn

        centre_x = round(x_start+col*game.cell_size+game.cell_size/2)
        centre_y = round(y_start+row*game.cell_size+game.cell_size/2)

        if(game.turn):
            disc_info=(centre_x,centre_y,time.time(),RED)
        else:
            disc_info=(centre_x,centre_y,time.time(),YELLOW)
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
    game_over_time=None
    finalDisplay=None
    finalColor=None

    def end(winner):
        nonlocal finalDisplay
        nonlocal game_over
        nonlocal finalColor
        nonlocal name_of_winner
        nonlocal name_of_loser
        nonlocal game_over_time
        game_over_time=time.time()

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
    box_rect=pygame.Rect(0,0,box_width,box_height)
    box_rect.center=(round(width/2),round(height/2))
    #
    
    #The two buttons
    btn_w=180
    btn_h=60
    play_again_rect=pygame.Rect(0,0,btn_w,btn_h)
    menu_rect=pygame.Rect(0,0,btn_w,btn_h)
    play_again_rect.center=(box_rect.centerx-110,box_rect.bottom-80)
    menu_rect.center=(box_rect.centerx+110,box_rect.bottom-80)
    #
    
    #Box init: def __init__(self,screen,rect,text="",fill_color=GRAY_2,border_color=DULL_WHITE,border_thickness=3,border_radius=15):
    popup=Box(screen,box_rect,"",GRAY_4,DULL_WHITE,2,10)
    #def __init__(self,screen,rect,text,fill_color,border_color,mode):
    BTN_play_again=Button(screen,play_again_rect,"PLAY AGAIN",CALM_BLUE,DULL_WHITE,"menu")
    main_menu=Button(screen,menu_rect,"MAIN MENU",CUTE_RED,DULL_WHITE,"menu")

    #main game loop:
    while running:
        screen.fill(bg_color)
        TIME=time.time()
        if game_mode=="blitz":
            if not T1.update():
                end(0)
            if not T2.update():
                end(1)

        #draw the discs
        #simulate falling - TIME-t = time since release, using 1/2 g t^2
        most_recent=1
        most_recent_column=None
        g=2500
        fall_time=((game.cell_size+game.boardHEIGHT*game.cell_size)/g)**0.5
        for cx,cy,t,draw_color in discs:
            if most_recent>TIME-t:
                most_recent=TIME-t
                most_recent_column=(cx-x_start)//game.cell_size
            y_curr=cap(y_start+0.5*g*(TIME-t)**2-game.cell_size/2,-game.cell_size,cy)
            draw_disc(screen,draw_color,(cx,y_curr),r)
        #

        # Board:
        draw_board()

        x,y=mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()[0]
        col=(x-x_start)//game.cell_size

        if not game_over:
            if(0<=col<game.boardWIDTH):
                row=game.boardHEIGHT-1-col_filled[col]
                if most_recent>fall_time or most_recent_column!=col:                
                    hover(row,col,game.turn)
                
            if filled==game.boardHEIGHT*game.boardWIDTH:
                game_over=True
                end(-1)
        else:
            if TIME-game_over_time>1.3*fall_time:
            # dark overlay
                fade=pygame.Surface(screen.get_size(),pygame.SRCALPHA)
                fade.fill((0,0,0,180))
                screen.blit(fade,(0,0))

                #def draw(self,mouse_pos,mouse_pressed):
                # play again and main menu buttons
                popup.draw()
                font_big=pygame.font.Font(None,80)
                text=font_big.render(finalDisplay,True,finalColor)
                screen.blit(text,text.get_rect(center=(box_rect.centerx,box_rect.top+80)))
                BTN_play_again.draw(mouse_pos,mouse_pressed)
                main_menu.draw(mouse_pos,mouse_pressed)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            if not game_over:
                if event.type == pygame.MOUSEBUTTONUP:
                    if col<game.boardWIDTH and col>=0:
                        if col_filled[col]<game.boardHEIGHT:
                            row=game.boardHEIGHT-1-col_filled[col]
                            move(row,col)
            else:
                if event.type==pygame.MOUSEBUTTONUP:
                    if BTN_play_again.clicked(mouse_pos):
                        play_again=True
                        running=False #go back to game.py, (stats will be updated and shown there)
                    if main_menu.clicked(mouse_pos):
                        running=False      # go back to game.py, (stats will be updated and shown there)
                                   

        if game_mode=="blitz":
            T1.display()
            T2.display()
                           

        pygame.display.flip()
        clock.tick(tickrate)
    return name_of_winner,name_of_loser,play_again