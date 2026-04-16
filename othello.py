import pygame
import numpy as np
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
    play_again=False
    name_of_winner=None
    name_of_loser=None

    pygame.display.set_caption("Othello")
    game_mode=None

    info=pygame.display.Info()
    width=info.current_w
    height=info.current_h
    tickrate=60
    bg_color=BLACK

    def checkWin(self,row,col):
        if valid_cells:
            return None
        else:
            number_of_white=np.sum(game.board==False)
            number_of_black=np.sum(game.board==True)
            if number_of_white>number_of_black:
                return-1
            if number_of_white<number_of_black:
                return 1
            if number_of_white==number_of_black:
                return 0

    game=Game(checkWin,8,8,round(90*height/864))

    x_start=width//2-(game.boardWIDTH//2)*game.cell_size
    x_end=width//2+(game.boardWIDTH//2)*game.cell_size
    y_start=round((height-game.boardHEIGHT*game.cell_size)/2)
    y_end=round((height+game.boardHEIGHT*game.cell_size)/2)
    r=(game.cell_size*2)//5

    game.board[3][3]=game.board[4][4]=False
    game.board[3][4]=game.board[4][3]=True

    time_board=np.full((game.boardHEIGHT,game.boardWIDTH),0.0)

    blitz_turn_time=10

    ClassicRect=pygame.Rect(0,0,round(300*height/864),round(100*height/864))
    ClassicRect.center=(round(width/2),round(2*height/5))
    ClassicButton=Button(screen,ClassicRect,"Classic","menu")

    BlitzRect=pygame.Rect(0,0,round(300*height/864),round(100*height/864))
    BlitzRect.center=(round(width/2),round(3*height/5))
    BlitzButton=Button(screen,BlitzRect,"Blitz","menu")

    menu=True
    while menu:
        screen.fill(bg_color)
        mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()[0]

        ClassicButton.draw(mouse_pos,mouse_pressed)
        BlitzButton.draw(mouse_pos,mouse_pressed)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                menu=False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    menu=False
            if event.type==pygame.MOUSEBUTTONUP:
                mousepos=event.pos
                if ClassicButton.clicked(mousepos):
                    game_mode="classic"
                    menu=False
                if BlitzButton.clicked(mousepos):
                    game_mode="blitz"
                    menu=False

        pygame.display.flip()
        clock.tick(tickrate)

    BOARD_SURFACE=pygame.Surface((x_end-x_start,y_end-y_start))
    BOARD_SURFACE.fill(bg_color)

    pygame.draw.rect(BOARD_SURFACE,(222,184,135),(0,0,(x_end-x_start),(y_end-y_start)))

    for i in range(0,x_end-x_start+game.cell_size,game.cell_size):
        pygame.draw.line(BOARD_SURFACE,(139,69,19),(i,0),(i,y_end-y_start),5)

    for i in range(0,y_end-y_start+game.cell_size,game.cell_size):
        pygame.draw.line(BOARD_SURFACE,(139,69,19),(0,i),(x_end-x_start,i),5)
    
    
    opacity=150
    GHOST_BLACK_SURFACE=pygame.Surface((2*r, 2*r), pygame.SRCALPHA)
    pygame.draw.circle(GHOST_BLACK_SURFACE,(*BLACK,opacity),(r,r),r)

    GHOST_WHITE_SURFACE=pygame.Surface((2*r, 2*r), pygame.SRCALPHA)
    pygame.draw.circle(GHOST_WHITE_SURFACE,(*WHITE,opacity),(r,r),r)
    
    def hover(row, col):
        if 0 <= row < game.boardHEIGHT and 0 <= col < game.boardWIDTH:
            cell_x = x_start + col * game.cell_size + 0.1*game.cell_size
            cell_y = y_start + row * game.cell_size + 0.1*game.cell_size

            # 1. Cover cell with board color
            pygame.draw.rect(screen, (222, 184, 135),
                             (cell_x, cell_y, game.cell_size*0.8, game.cell_size*0.8))

            # 3. Draw ghost disc
            if game.turn:
                screen.blit(GHOST_WHITE_SURFACE,(centreX[col]-r,centreY[row]-r))
            else:
                screen.blit(GHOST_BLACK_SURFACE,(centreX[col]-r,centreY[row]-r))
            

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

    def move(row,col):
        nonlocal filled,valid_cells,game
        
        TIME=time.time()
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

            for index,arr in enumerate(directions):
                arr1=arr[1:]
                time_board1=time_board_directions[index][1:]
                arr1.setflags(write=1)
                time_board1.setflags(write=1)

                count=0
                change=False

                for idx,val in enumerate(arr1):
                    if val==(not game.turn):
                        count+=1
                    if val==game.turn:
                        if count>0:
                            change=True
                        break
                    if val is None:
                        break

                if change:
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
    game_over_time=None
    finalDisplay=""
    finalColor="white"

    def end(winner):
        nonlocal game_over,game_over_time,finalColor,finalDisplay,name_of_winner,name_of_loser

        game_over_time=time.time()
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
        left_x=round(x_start-1.5*game.cell_size)
        right_x=round(x_end+0.6*game.cell_size)

        T1=Timer(screen,font,left_x,y_start,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        T2=Timer(screen,font,right_x,y_start,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)

    running=True
    flip_time=0.3
    font_big=pygame.font.Font(None,80)
    font_small=pygame.font.Font(None,40)

    while running:
        screen.fill(bg_color)

        if game_mode=="blitz":
            if not T1.update():
                end(-1)
            if not T2.update():
                end(1)

        x,y=pygame.mouse.get_pos()
        col=(x-x_start)//game.cell_size
        row=(y-y_start)//game.cell_size

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                running=False

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    running=False

            if not game_over:
                if event.type==pygame.MOUSEBUTTONUP:
                    if 0<=col<game.boardWIDTH and 0<=row<game.boardHEIGHT:
                        if (centreX[col],centreY[row]) in valid_cells:
                            move(row,col)
            else:
                if event.type==pygame.MOUSEBUTTONUP:
                    pos=event.pos
                    if play_again_btn.collidepoint(pos):
                        play_again=True
                        running=False
                    if menu_btn.collidepoint(pos):
                        running=False

        screen.blit(BOARD_SURFACE,(x_start,y_start))

        for a,b in valid_cells:
            pygame.draw.circle(screen,(90, 90, 90),(a,b),r/5)

        if 0<=row<game.boardHEIGHT and 0<=col<game.boardWIDTH:
            if (centreX[col],centreY[row]) in valid_cells:
                hover(row,col)

        TIME=time.time()
        for i in range(game.boardHEIGHT):
            for j in range(game.boardWIDTH):
                if game.board[i][j]==True:
                    if (TIME-time_board[i][j])>flip_time:
                        pygame.draw.circle(screen, "white", (centreX[j],centreY[i]), r)
                    else:
                        frac=cap((TIME-time_board[i][j])/flip_time,0.01,0.99)
                        if frac<0.5:
                            rect=pygame.Rect(0,0,2*r,2*r-frac*4*r)
                            rect.center=((centreX[j],centreY[i]))
                            pygame.draw.ellipse(screen,"black",rect)
                        else:
                            rect=pygame.Rect(0,0,2*r,(frac-0.5)*4*r)
                            rect.center=((centreX[j],centreY[i]))
                            pygame.draw.ellipse(screen,"white",rect)
                if game.board[i][j]==False:
                    if (TIME-time_board[i][j])>flip_time:
                        pygame.draw.circle(screen, "black", (centreX[j],centreY[i]), r)
                    else:
                        frac=cap((TIME-time_board[i][j])/flip_time,0.01,0.99)
                        if frac<0.5:
                            rect=pygame.Rect(0,0,2*r,2*r-frac*4*r)
                            rect.center=((centreX[j],centreY[i]))
                            pygame.draw.ellipse(screen,"white",rect)
                        else:
                            rect=pygame.Rect(0,0,2*r,(frac-0.5)*4*r)
                            rect.center=((centreX[j],centreY[i]))
                            pygame.draw.ellipse(screen,"black",rect)

        
        if game_mode=="blitz":
            T1.display()
            T2.display()

        if game_over:
            fade=pygame.Surface(screen.get_size(),pygame.SRCALPHA)
            fade.fill((0,0,0,180))
            screen.blit(fade,(0,0))

            box_rect=pygame.Rect(0,0,500,300)
            box_rect.center=(width//2,height//2)

            pygame.draw.rect(screen,(40,40,40),box_rect,border_radius=20)
            pygame.draw.rect(screen,(200,200,200),box_rect,3,border_radius=20)

            text=font_big.render(finalDisplay,True,finalColor)
            screen.blit(text,text.get_rect(center=(box_rect.centerx,box_rect.top+80)))

            play_again_btn=pygame.Rect(0,0,180,60)
            menu_btn=pygame.Rect(0,0,180,60)

            play_again_btn.center=(box_rect.centerx-110,box_rect.bottom-80)
            menu_btn.center=(box_rect.centerx+110,box_rect.bottom-80)

            pygame.draw.rect(screen,(70,130,180),play_again_btn,border_radius=10)
            pygame.draw.rect(screen,(180,70,70),menu_btn,border_radius=10)

            txt1=font_small.render("Play Again",True,"white")
            txt2=font_small.render("Leaderboard",True,"white")

            screen.blit(txt1,txt1.get_rect(center=play_again_btn.center))
            screen.blit(txt2,txt2.get_rect(center=menu_btn.center))

        pygame.display.flip()
        clock.tick(tickrate)

    return name_of_winner,name_of_loser,play_again