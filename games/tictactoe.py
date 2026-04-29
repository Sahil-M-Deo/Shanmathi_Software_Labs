import pygame
import numpy as np
import math
import time

from classGame import *
from design_elements import *
    
def play(screen,clock,font,username1,username2,turn,game_mode,blitz_turn_time):
    exit_status="main_menu" #to check if user wants to play again or go to main menu after a game ends
    name_of_winner=None
    name_of_loser=None
    
    if(turn==1):
        username1,username2=username2,username1
        
    pygame.display.set_caption("TicTacToe")
    
    #display sizes
    info=pygame.display.Info()
    SCREEN_WIDTH=info.current_w
    SCREEN_HEIGHT=info.current_h
    SAHIL_WIDTH=1536
    SAHIL_HEIGHT=864
    screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    tickrate=60
    bg_color=BLACK
    #

    #positions of circles and crosses
    circ = [] #(centre_x,centre_y,start_time)
    cross = [] #(Line_1,Line_2,start_time)
    #

    #time related variables
    blitz_turn_time=10
    #

    #initialising game board
    def checkWin(self,current_row,current_column):
        streak=5

        def count(arr):            
            matches=(arr==self.turn)
            if matches.all():
                return len(matches)
            else:
                return np.argmax(~matches)

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

        if(up+down+1==streak):
            return ((current_row-up+1/8,current_column+1/2),(current_row+down+7/8,current_column+1/2))
        elif(left+right+1==streak):
            return ((current_row+1/2,current_column-left+1/8),(current_row+1/2,current_column+right+7/8))
        elif(d1_left+d1_right+1==streak):
            return ((current_row-d1_left+1/6,current_column-d1_left+1/6),(current_row+d1_right+5/6,current_column+d1_right+5/6))
        elif(d2_left+d2_right+1==streak):
            return ((current_row-d2_left+1/6,current_column+d2_left+5/6),(current_row+d2_right+5/6,current_column-d2_right+1/6))
        else:
            return False
    
    game=Game(checkWin,10,10,Size(70))
    x_start=Size(SAHIL_WIDTH/2-game.boardWIDTH*game.cell_size/2)
    x_end=Size(SAHIL_WIDTH/2+game.boardWIDTH*game.cell_size/2)
    y_start=Size(SAHIL_HEIGHT/2-game.boardHEIGHT*game.cell_size/2)
    y_end=Size(SAHIL_HEIGHT/2+game.boardHEIGHT*game.cell_size/2)
    r=game.cell_size*0.34

    game.switchTurn()
    #username1 is turn=False represented by Circle
    #username2 is turn=True represented by Cross
    
    BOARD_SURFACE=pygame.Surface(Coord(x_end-x_start,y_end-y_start))
    def init_board():
        board_paths=[]
        # vertical lines
        strtx=strty=int(game.cell_size)
        brd_ht=int(y_end-y_start)
        brd_wdth=int(x_end-x_start)
        endx=int(x_end-x_start-game.cell_size)
        endy=int(y_end-y_start-game.cell_size)
        for i in np.linspace(strtx,endx,game.boardWIDTH-1):
            board_paths.append(JaggedLine(BOARD_SURFACE,Coord(i,0),Coord(i,brd_ht),"white",segments=2000,jag=1))
        # horizontal lines
        for i in np.linspace(strty,endy,game.boardHEIGHT-1):
            board_paths.append(JaggedLine(BOARD_SURFACE,Coord(0,i),Coord(brd_wdth,i),"white",segments=2000,jag=1))
        for path in board_paths:
            path.draw()
    
    init_board()
    def draw_board():
        screen.blit(BOARD_SURFACE,Coord(x_start,y_start))

    def hover(row,col):
        if game.turn:
            hover_color=CIRCLE_YELLOW
        else:
            hover_color=CROSS_PINK
        hov_rect=Rect(0,0,0.92*game.cell_size,0.92*game.cell_size)
        hov_rect.center=Coord(x_start+(col+1/2)*game.cell_size,y_start+(row+1/2)*game.cell_size)
        pygame.draw.rect(screen,hover_color,hov_rect)

    if game_mode=="blitz":
        #init timers
        left_x=x_start-1.5*game.cell_size
        right_x=x_end+0.6*game.cell_size
        T1=Timer(screen,font,left_x,y_start,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        T2=Timer(screen,font,right_x,y_start,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        #

    running=True
    WINLINE=None
    #when player clicks on an empty cell:
    def move(row,col):
        centre_x=x_start+game.cell_size/2+col*game.cell_size
        centre_y=y_start+game.cell_size/2+row*game.cell_size

        nonlocal filled
        filled+=1
        game.board[row][col]=game.turn

        TIME=time.time()
        
        if game_mode=="blitz":
            if filled>1:
                T1.switchTurn()
            T2.switchTurn()
        
        if game.turn:
            circ.append((*Coord(centre_x,centre_y),TIME))
        else:
            # when adding a cross:
            a=centre_x
            b=centre_y

            path1=JaggedLine(screen,Coord(a-r,b-r),Coord(a+r,b+r),CROSS_PINK,50)
            path2=JaggedLine(screen,Coord(a+r,b-r),Coord(a-r,b+r),CROSS_PINK,50)
            cross.append((path1,path2,TIME))
        
        check=game.checkWin(row,col)

        if check:
            (r1,c1),(r2,c2)=check
            x1=x_start+c1*game.cell_size
            y1=y_start+r1*game.cell_size
            x2=x_start+c2*game.cell_size
            y2=y_start+r2*game.cell_size
            nonlocal WINLINE
            if(game.turn):
                winlinecolor=CROSS_PINK
            else:
                winlinecolor=CIRCLE_YELLOW
            WINLINE=JaggedLine(screen,Coord(x1,y1),Coord(x2,y2),winlinecolor,segments=200,jag=1.5)
            end(game.turn)
        game.switchTurn()
    #

    game_over = False
    finalDisplay=""
    finalColor="white"

    def end(winner):
        nonlocal game_over
        game_over=True

        if game_mode=="blitz":
            T1.end()
            T2.end()

        nonlocal name_of_winner
        nonlocal name_of_loser
        nonlocal finalDisplay
        nonlocal finalColor
        
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

    filled=0 #number of filled cells

    #popup box
    box_width=500
    box_height=300
    box_rect=Rect(0,0,box_width,box_height)
    box_rect.center=Coord(SAHIL_WIDTH/2,SAHIL_HEIGHT/2)
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
    
    most_recent_time=0

    FADE_SURFACE=pygame.Surface((screen.get_size()),pygame.SRCALPHA)
    FADE_SURFACE.fill((*BLACK,180))
    font_big=pygame.font.Font(None,80)
    
    #main game loop:
    while running:
        
        #setup new frame
        screen.fill(bg_color)
        if game_mode=="blitz":
            if not T1.update():
                end(0)
            if not T2.update():
                end(1)

        x,y=mouse_pos=pygame.mouse.get_pos()
    
        mouse_pressed=pygame.mouse.get_pressed()[0]
        col = int((x-x_start)//game.cell_size)
        row = int((y-y_start)//game.cell_size)
        TIME=time.time()
        #
        
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
                    if game.valid_move(row,col) and game.board[row][col]==None:
                        move(row,col)
                        most_recent_time=TIME
            else:
                if event.type==pygame.MOUSEBUTTONUP:
                    if TIME-most_recent_time>1.3:
                        if BTN_play_again.mouse_over(mouse_pos):
                            exit_status="play_game"
                            running=False #go back to game.py, (stats will be updated and shown there)
                        if main_menu.mouse_over(mouse_pos):
                            exit_status="main_menu"
                            running=False #go back to game.py, (stats will be updated and shown there)
                                              
        #Grid:
        draw_board()

        # Hover effect:
        if (not game_over) and game.valid_move(row,col) and game.board[row][col]==None:
            hover(row,col)

        # adding crosses
        for path1,path2,t in cross:
            curr_time=TIME-t
            draw_time=0.4
            
            f=np.clip(curr_time/draw_time,0,1)
            
            # first stroke (0 → 0.5)
            if f>0:
                f1=np.clip(f/0.3,0,1)
                path1.draw_partial(f1)
            
            # second stroke (0.5 → 1)
            if f>0.7:
                f2=np.clip((f-0.7)/0.3,0,1)
                path2.draw_partial(f2)
        #

        # adding circles        
        for a, b, t in circ:
            curr_time=TIME-t
            draw_time=0.4
            f=np.clip(curr_time/draw_time,0.001,0.9999)
            pygame.draw.arc(screen,CIRCLE_YELLOW,Rect(a-r,b-r,2*r,2*r),0,2*math.pi*f,3)
        #

        if game_mode=="blitz":
            T1.display()
            T2.display()

        if not game_over:
            # dealing with a tie
            if filled == game.boardHEIGHT*game.boardWIDTH:
                game_over=True
                end(-1)
        else:
            T=TIME-most_recent_time
            if 0.6<T:
                if WINLINE:
                    draw_time=0.4
                    f=np.clip((T-0.6)/draw_time,0,1)
                    if game.turn:
                        WINLINE.color=CROSS_PINK
                    else:
                        WINLINE.color=CIRCLE_YELLOW
                    WINLINE.draw_partial(f)

            if 1.3<T:
                # dark overlay
                screen.blit(FADE_SURFACE,(0,0))

                #def draw(self,mouse_pos,mouse_pressed):
                # play again and main menu buttons
                popup.draw()
                text=font_big.render(finalDisplay,True,finalColor)
                screen.blit(text,text.get_rect(center=(box_rect.centerx,box_rect.top+80)))
                BTN_play_again.draw(mouse_pos,mouse_pressed)
                main_menu.draw(mouse_pos,mouse_pressed)


        pygame.display.flip()
        clock.tick(tickrate)

    return name_of_winner,name_of_loser,exit_status