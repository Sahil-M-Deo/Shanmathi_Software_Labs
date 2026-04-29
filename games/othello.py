import pygame
import numpy as np
import time
from classGame import *
from design_elements import *

def play(screen,clock,font,username1,username2,turn,game_mode,blitz_turn_time):
    exit_status="main_menu"
    name_of_winner=None
    name_of_loser=None
    
    if(turn==0):
        username1,username2=username2,username1
        
    pygame.display.set_caption("Othello")

    info=pygame.display.Info()
    width=info.current_w
    height=info.current_h
    tickrate=60
    bg_color=BLACK

    def checkWin(self,row,col):
        if valid_cells:
            return None
        else:
            number_of_black=np.sum(game.board==False)
            number_of_white=np.sum(game.board==True)
            if number_of_black>number_of_white:
                return-1
            if number_of_black<number_of_white:
                return 1
            if number_of_black==number_of_white:
                return 0

    game=Game(checkWin,8,8,scale_h(80))

    x_start=width/2-game.boardWIDTH*game.cell_size/2
    x_end=width/2+game.boardWIDTH*game.cell_size/2
    y_start = height//9
    y_end = y_start+(game.boardHEIGHT*game.cell_size)
    r=(game.cell_size*0.4)

    game.board[3][4]=game.board[4][3]=False
    game.board[3][3]=game.board[4][4]=True

    time_board=np.full((game.boardHEIGHT,game.boardWIDTH),0.0)

    BOARD_SURFACE=pygame.Surface(((x_end-x_start),(y_end-y_start)))
    BOARD_SURFACE.fill(bg_color)

    pygame.draw.rect(BOARD_SURFACE,MILKY_COFFEE,(0,0,(x_end-x_start),(y_end-y_start)))

    
    for i in np.linspace(0,x_end-x_start,game.boardWIDTH+1):
        pygame.draw.line(BOARD_SURFACE,DARK_COFFEE,(i,0),(i,y_end-y_start),5)

    for i in np.linspace(0,y_end-y_start,game.boardHEIGHT+1):
        pygame.draw.line(BOARD_SURFACE,DARK_COFFEE,(0,i),(x_end-x_start,i),5)
    
    
    opacity=150
    GHOST_BLACK_SURFACE=pygame.Surface((2*r, 2*r), pygame.SRCALPHA)
    pygame.draw.circle(GHOST_BLACK_SURFACE,(*BLACK,opacity),(r,r),r)

    GHOST_WHITE_SURFACE=pygame.Surface((2*r, 2*r), pygame.SRCALPHA)
    pygame.draw.circle(GHOST_WHITE_SURFACE,(*WHITE,opacity),(r,r),r)
    
    def hover(row, col):
        if 0 <= row < game.boardHEIGHT and 0 <= col < game.boardWIDTH:
            cell_x = (x_start + col * game.cell_size + 0.1*game.cell_size)
            cell_y = (y_start + row * game.cell_size + 0.1*game.cell_size)

            # 1. Cover cell with board color
            pygame.draw.rect(screen, MILKY_COFFEE,(cell_x, cell_y, game.cell_size*0.8, game.cell_size*0.8))

            # 3. Draw ghost disc
            if game.turn:
                screen.blit(GHOST_BLACK_SURFACE,(centreX[col]-r,centreY[row]-r))
            else:
                screen.blit(GHOST_WHITE_SURFACE,(centreX[col]-r,centreY[row]-r))
            

    def centre_x(col):
        return x_start+(game.cell_size//2)+(col*game.cell_size)
    centreX=[centre_x(col) for col in range(game.boardWIDTH)]

    def centre_y(row):
        return y_start+(game.cell_size//2)+(row*game.cell_size)
    centreY=[centre_y(row) for row in range(game.boardHEIGHT)]

    valid_cells=set()

    def validMoves():
        valid_cells.clear()
        for i in range(game.boardHEIGHT):
            for j in range(game.boardWIDTH):
                if game.board[i][j]==None:
                    score=0
                    directions=[
                        game.board[i,j:].flatten(),
                        game.board[i,j::-1].flatten(),
                        game.board[i:,j],
                        game.board[i::-1,j],
                        (game.board[i::-1,j::-1]).diagonal(),
                        (game.board[i::-1,j:]).diagonal(),
                        (game.board[i:,j:]).diagonal(),
                        (game.board[i:,j::-1]).diagonal()
                    ]

                    for arr in directions:
                        arr1=arr[1:]
                        count=0
                        for k in arr1:
                            if k==(not game.turn):
                                count+=1
                            if k==game.turn:
                                score+=count
                                break
                            if k is None:
                                break
                    if score>0:
                        valid_cells.add((centreX[j],centreY[i]))
    score={True:2,False:2}
    def move(row,col):
        nonlocal filled,valid_cells,game,score,name_color

        TIME=time.time()
        name_color[not game.turn]=GREEN
        name_color[game.turn]=WHITE
        filled+=1
        if game_mode=="blitz":
            if filled>1:
                T1.switchTurn()
            T2.switchTurn()

        if (centreX[col],centreY[row]) in valid_cells:
            game.board[row][col]=game.turn
            time_board[row][col]=0

            directions=[
                game.board[row,col:],game.board[row,col::-1],
                game.board[row:,col],game.board[row::-1,col],
                (game.board[row::-1,col::-1]).diagonal(),
                (game.board[row::-1,col:]).diagonal(),
                (game.board[row:,col:]).diagonal(),
                (game.board[row:,col::-1]).diagonal()
            ]

            time_board_directions=[
                time_board[row,col:],time_board[row,col::-1],
                time_board[row:,col],time_board[row::-1,col],
                (time_board[row::-1,col::-1]).diagonal(),
                (time_board[row::-1,col:]).diagonal(),
                (time_board[row:,col:]).diagonal(),
                (time_board[row:,col::-1]).diagonal()
            ]
            score[game.turn]+=1
            for index,arr in enumerate(directions):
                
                arr1=arr[1:]
                time_board1=time_board_directions[index][1:]
                arr1.setflags(write=1)
                time_board1.setflags(write=1)

                increase_score=0
                change=False

                for idx,val in enumerate(arr1):
                    if val==(not game.turn):
                        increase_score+=1
                    if val==game.turn:
                        if increase_score>0:
                            change=True
                        break
                    if val is None:
                        break

                if change:
                    score[game.turn]+=increase_score
                    score[not game.turn]-=increase_score
                    for idx,val in enumerate(arr1):
                        if val==(not game.turn):
                            arr1[idx]=game.turn
                            time_board1[idx]=TIME+0.1*idx
                        if val==game.turn:
                            break
                        if val is None:
                            break

        game.switchTurn()
        validMoves()

        if not valid_cells:
            game.switchTurn()
            validMoves()
            if not(game.checkWin(row,col)==None):
                end(game.checkWin(row,col))

    game_over=False
    finalDisplay=""
    finalColor="white"

    def end(winner):
        nonlocal game_over,finalColor,finalDisplay,name_of_winner,name_of_loser
        game_over=True

        if game_mode=="blitz":
            T1.end()
            T2.end()

        if winner==1:
            name_of_winner=username1
            name_of_loser=username2
            finalDisplay=username1+" WINS!"
            finalColor="green"
        elif winner==-1:
            name_of_winner=username2
            name_of_loser=username1
            finalDisplay=username2+" WINS!"
            finalColor="green"
        else:
            name_of_winner="TIE"
            name_of_loser="TIE"
            finalDisplay="IT'S A TIE!"
            finalColor="grey"

    filled=0
    validMoves()

    if game_mode=="blitz":
        left_x=x_start-1.5*game.cell_size
        right_x=x_end+0.6*game.cell_size

        T1=Timer(screen,font,left_x,y_start,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        T2=Timer(screen,font,right_x,y_start,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)

    running=True
    flip_time=0.3

    #popup box
    box_width=scale_w(500)
    box_height=scale_h(300)
    box_rect=pygame.rect.Rect(0,0,box_width,box_height)
    box_rect.center=(width/2,height/2)
    #
    
    #The two buttons
    btn_w=scale_w(180)
    btn_h=scale_h(60)

    play_again_rect=pygame.rect.Rect(0,0,btn_w,btn_h)
    menu_rect=pygame.rect.Rect(0,0,btn_w,btn_h)
    play_again_rect.center=(box_rect.centerx-scale_w(110),box_rect.bottom-scale_h(80))
    menu_rect.center=(box_rect.centerx+scale_w(110),box_rect.bottom-scale_h(80))
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

    #score board related
    score1_rect=pygame.rect.Rect(x_start,0,2*game.cell_size,y_start)
    score2_rect=pygame.rect.Rect(x_start+6*game.cell_size,0,2*game.cell_size,y_start)
    #username display
    name1_rect=pygame.rect.Rect(0,0,3*game.cell_size,y_start//2)
    name2_rect=pygame.rect.Rect(width-3*game.cell_size,0,3*game.cell_size,y_start//2)
    name_color={True:GREEN,False:WHITE}


    while running:
        screen.fill(bg_color)
        TIME=time.time()

        if game_mode=="blitz":
            if not T1.update():
                end(-1)
            if not T2.update():
                end(1)
                
        x,y=mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()[0] #(left, middle, right) mouse button states - for us [0] is relevant
        col=int((x-x_start)//game.cell_size)
        row=int((y-y_start)//game.cell_size)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                if not game_over:
                    return("","","incomplete")
                else:
                    return(name_of_winner,name_of_loser,"main_menu")

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    if not game_over:
                        return("","","incomplete")
                    else:
                        return(name_of_winner,name_of_loser,"main_menu")

            if not game_over:
                if event.type==pygame.MOUSEBUTTONUP:
                    if 0<=col<game.boardWIDTH and 0<=row<game.boardHEIGHT:
                        if (centreX[col],centreY[row]) in valid_cells:
                            move(row,col)
                            most_recent_time=TIME
            else:
                if event.type==pygame.MOUSEBUTTONUP:
                    if TIME-most_recent_time>flip_time*3:
                        if BTN_play_again.mouse_over(mouse_pos):
                            exit_status="play_game"
                            running=False #go back to game.py, (stats will be updated and shown there)
                        if main_menu.mouse_over(mouse_pos):
                            running=False      # go back to game.py, (stats will be updated and shown there)

        score1_board=Box(screen,score1_rect,str(score[True]),GRAY_2,DULL_WHITE,2,0)
        score2_board=Box(screen,score2_rect,str(score[False]),GRAY_2,DULL_WHITE,2,0)
        score1_board.draw()
        score2_board.draw()
        
        #displaying usernames:
        name1_box=Box(screen,name1_rect,username1,BLACK,BLACK,2,0,name_color[True])
        name2_box=Box(screen,name2_rect,username2,BLACK,BLACK,2,0,name_color[False])
        name1_box.draw()
        name2_box.draw()
        screen.blit(BOARD_SURFACE,(x_start,y_start))


        
        for a,b in valid_cells:
            pygame.draw.circle(screen,(90, 90, 90),(a,b),int(r/5))

        if not game_over:
            if 0<=row<game.boardHEIGHT and 0<=col<game.boardWIDTH:
                if (centreX[col],centreY[row]) in valid_cells:
                    hover(row,col)
        
        for i in range(game.boardHEIGHT):
            for j in range(game.boardWIDTH):
                if game.board[i][j]==True:
                    if (TIME-time_board[i][j])>flip_time:
                        pygame.draw.circle(screen, BLACK, (centreX[j],centreY[i]), int(r))
                    else:
                        frac=np.clip((TIME-time_board[i][j])/flip_time,0.01,0.99)
                        if frac<0.5:
                            rect=pygame.rect.Rect(0,0,2*r,2*r-frac*4*r)
                            rect.center=(centreX[j],centreY[i])
                            pygame.draw.ellipse(screen,WHITE,rect)
                        else:
                            rect=pygame.rect.Rect(0,0,2*r,(frac-0.5)*4*r)
                            rect.center=(centreX[j],centreY[i])
                            pygame.draw.ellipse(screen,BLACK,rect)
                if game.board[i][j]==False:
                    if (TIME-time_board[i][j])>flip_time:
                        pygame.draw.circle(screen, WHITE, (centreX[j],centreY[i]), int(r))
                    else:
                        frac=np.clip((TIME-time_board[i][j])/flip_time,0.01,0.99)
                        if frac<0.5:
                            rect=pygame.rect.Rect(0,0,2*r,2*r-frac*4*r)
                            rect.center=(centreX[j],centreY[i])
                            pygame.draw.ellipse(screen,BLACK,rect)
                        else:
                            rect=pygame.rect.Rect(0,0,2*r,(frac-0.5)*4*r)
                            rect.center=(centreX[j],centreY[i])
                            pygame.draw.ellipse(screen,WHITE,rect)

        
        if game_mode=="blitz":
            T1.display()
            T2.display()

        if game_over:
            if TIME-most_recent_time>flip_time*3:
            # dark overlay
                screen.blit(FADE_SURFACE,(0,0))

                #def draw(self,mouse_pos,mouse_pressed):
                # play again and main menu buttons
                popup.draw()
                text=font_big.render(finalDisplay,True,finalColor)
                screen.blit(text,text.get_rect(center=(box_rect.centerx,box_rect.top+scale_h(80))))
                BTN_play_again.draw(mouse_pos,mouse_pressed)
                main_menu.draw(mouse_pos,mouse_pressed)

        pygame.display.flip()
        clock.tick(tickrate)

    return name_of_winner,name_of_loser,exit_status