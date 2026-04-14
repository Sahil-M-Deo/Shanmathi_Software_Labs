import pygame
import numpy as np
import time
from classGame import *
from design_elements import *

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 50) #(font style,size)

#window variables
width = 1280 
height = 720
tickrate=60
bg_color="black"
#

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("TicTacToe")
clock = pygame.time.Clock()
game_mode = None



#initialising game board
def checkWin(self,row,col):
    if valid_cells:
        return None
    else:
        number_of_white=len(game.board[game.board==True].flatten())
        number_of_black=len(game.board[game.board==False].flatten())
        if number_of_white>number_of_black:
            return 1
        if number_of_white<number_of_black:
            return 0
        if number_of_white==number_of_black:
            return -1

game = Game(checkWin,8,8,80)
hover_color="blue"

x_start = width//2 - (game.boardWIDTH//2)*game.cell_size
x_end = width//2+ (game.boardWIDTH//2)*game.cell_size
y_start = 5
y_end = 5+(game.boardHEIGHT*game.cell_size)
r = (game.cell_size*2)//5 #radius of pieces

game.board[3][3]=game.board[4][4]=False  #othello board init
game.board[3][4]=game.board[4][3]=True

#

username1="player1"
username2="player2"

#time related variables
turn_time=10
last_time=time.time()
blitz_turn_time=10
#



#username1 is turn=True represented by Circle
#username2 is turn=False represented by Cross

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




def draw_board():
    pygame.draw.rect(screen,(222, 184, 135),(x_start,y_start,(x_end-x_start),(y_end-y_start)))
    for i in range(x_start, x_end+game.cell_size, game.cell_size):
        pygame.draw.line(screen, (139, 69, 19), (i,y_start), (i,y_end), 5) #(screen,color,start,end,width)

    for i in range(y_start, y_end+game.cell_size, game.cell_size):
        pygame.draw.line(screen, (139, 69, 19), (x_start,i), (x_end,i), 5)


def hover(row,col):
    if row<10 and col<10 and row>=0 and col>=0:
        pygame.draw.rect(screen, hover_color, (x_start+col*game.cell_size,y_start+row*game.cell_size,game.cell_size,game.cell_size))


running=True

def centre_x(col):
    return x_start+(game.cell_size//2)+(col*game.cell_size)
def centre_y(row):
    return y_start+(game.cell_size//2)+(row*game.cell_size)

valid_cells=[]
def validMoves():
    for i in range(game.boardHEIGHT):
        for j in range(game.boardWIDTH):
            if game.board[i][j]==None:
                score=0
                directions=([game.board[i,j:].flatten(),game.board[i,j::-1].flatten(),game.board[(i):,j],game.board[(i)::-1,j],(game.board[i::-1,j::-1]).diagonal(),(game.board[i::-1,j:]).diagonal(),(game.board[i:,j:]).diagonal(),(game.board[i:,j::-1]).diagonal()])

                for arr in directions:
                    arr1=arr[1:]
                    count=0
                    for k in arr1:
                        if k == (not game.turn):
                            count+=1
                        if k == (game.turn):
                            score+=count
                            break
                        if k == None:
                            break
                if score>0:
                    valid_cells.append((centre_x(j),centre_y(i)))

#when player clicks on an empty cell:
def move(row,col):
    global hover_color
    global filled
    global valid_cells
    global game
    
    if (centre_x(col),centre_y(row)) in valid_cells:
        
        game.board[row][col]=game.turn

        directions=([game.board[row,col:],game.board[row,col::-1],game.board[(row):,col],game.board[(row)::-1,col],(game.board[row::-1,col::-1]).diagonal(),(game.board[row::-1,col:]).diagonal(),(game.board[row:,col:]).diagonal(),(game.board[row:,col::-1]).diagonal()])
        for arr in directions:
            arr1=arr[1:]
            arr1.setflags(write=1)
            count=0
            change=False
            for idx,val in enumerate(arr1):
                if val == (not game.turn):
                    count+=1
                if val == (game.turn):
                    if count>0:
                        change=True
                    break
                if val == None:
                    break
            if change:
                for idx,val in enumerate(arr1):
                    if val == (not game.turn):
                        arr1[idx]=game.turn
                    if val == (game.turn):
                        break
                    if val == None:
                        break
        game.switchTurn()

        valid_cells.clear()
        validMoves()

        #if no valid move left
        if  not (game.checkWin(row,col)==None):
                game.turn = not game.turn
                validMoves()
                #checks for valid moves on other player
                if not (game.checkWin(row,col)==None): #if none then end game, else continue
                    end(game.checkWin(row,col))

#

def display_timer(x,y,player):
        w=game.cell_size
        h=game.boardHEIGHT*game.cell_size
        
        is_active=(player==game.turn)

        scale=1.06 if is_active else 1.0
        w_scaled=round(w*scale)
        h_scaled=round(h*scale)
        
        rect=pygame.Rect(round(x-(w_scaled-w)/2),round(y-(h_scaled-h)/2),w_scaled,h_scaled)

        if is_active:
            bg=(60,60,60)
            border_color=(25,25,25)
            border_thickness=5
        else:
            bg=(30,30,30)
            border_color=(15,15,15)
            border_thickness=2
        pygame.draw.rect(screen,bg,rect,border_radius=20)
        pygame.draw.rect(screen,border_color,rect,border_thickness,border_radius=20)

        if player==game.turn:
            t=rem_time
        else:
            t=turn_time

        ratio_raw=t/turn_time
        ratio=ratio_raw*ratio_raw*(3-2*ratio_raw)
        if ratio<0.5:
            r=255
            g=int(880*ratio*ratio) 
        else:
            r=510*(1-ratio)
            g=220
        color=(r,g,0)
        
        padding=6
        inner_w = rect.width-2*padding
        inner_h = rect.height-2*padding

        fill_h = round(inner_h * ratio)

        # surface for inner rounded shape
        fill_surf = pygame.Surface((inner_w, inner_h))

        # draw full rounded rect (defines the shape)
        pygame.draw.rect(fill_surf, color, (0, 0, inner_w, inner_h), border_radius = 15)
        # clip from bottom
        if fill_h > 0:
            clipped = fill_surf.subsurface((0, inner_h - fill_h, inner_w, fill_h))
            screen.blit(clipped, (rect.x + padding, rect.y + padding + inner_h - fill_h))

        if not is_active:
            overlay=pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
            overlay.fill((0,0,0,120))
            screen.blit(overlay,(rect.x,rect.y))

        txt=f"{t:.1f}"
        text=font.render(txt,True,"white")
        screen.blit(text,text.get_rect(center=(rect.centerx,rect.bottom+25)))


game_over = False
finalDisplay=""
finalColor="white"
name_of_winner=None
name_of_loser=None

def end(winner):
    global bg_color
    bg_color=(0,150,70)
    global game_over
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

filled=0 #number of filled cells

def end(winner):
    global finalDisplay
    global game_over
    global finalColor
    global name_of_winner
    global name_of_loser
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


validMoves()


if game_mode=="blitz":
        #init timers
        left_x = round(x_start-1.5*game.cell_size)
        right_x = round(x_end+0.6*game.cell_size)
        T1=Timer(screen,font,left_x,y_start-0.2*game.cell_size,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        T2=Timer(screen,font,right_x,y_start-0.2*game.cell_size,game.cell_size,game.cell_size*game.boardHEIGHT,blitz_turn_time)
        #
play_again=False
    #main game loop:
while running:
    screen.fill(bg_color)
    x,y = pygame.mouse.get_pos()
    col = (x-x_start)//game.cell_size
    row = (y-y_start)//game.cell_size

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        
        if not game_over:
            if event.type == pygame.MOUSEBUTTONUP:
                if col<game.boardWIDTH and col>=0 and row<game.boardHEIGHT and row>=0 and game.board[row][col]==None:
                    move(row,col)
        else:
            if event.type==pygame.MOUSEBUTTONUP:
                pos=event.pos
                if play_again_btn.collidepoint(pos):
                    play_again=True
                    running=False #go back to game.py, (stats will be updated and shown there)
                if menu_btn.collidepoint(pos):
                    running=False      # go back to game.py, (stats will be updated and shown there)
                                    

    # Hover effect:
    if row<game.boardHEIGHT and col<game.boardWIDTH and row>=0 and col>=0 and game.board[row][col]==None:
        hover(row,col)
    
    #Grid:
    draw_board()

    for i in range(game.boardHEIGHT):
        for j in range(game.boardWIDTH):
            if game.board[i][j]==True:
                pygame.draw.circle(screen, "white", (centre_x(j),centre_y(i)), r)
            if game.board[i][j]==False:
                pygame.draw.circle(screen, "black", (centre_x(j),centre_y(i)), r)

    for a,b in valid_cells:
        pygame.draw.circle(screen, "green", (a,b), r/5)

    if game_mode=="blitz":
        left_x = round(x_start-1.5*game.cell_size)
        right_x = round(x_end+0.6*game.cell_size)
        top_y = y_start
        
        display_timer(left_x, top_y, not game.turn)
        display_timer(right_x, top_y, game.turn)



    if not game_over:

        if game_mode=="blitz":
            rem_time = turn_time-(time.time()-last_time)
            if rem_time<=0:
                rem_time=0
                end(not game.turn)
    else:
        # dark overlay
        fade=pygame.Surface(screen.get_size(),pygame.SRCALPHA)
        fade.fill((0,0,0,180))
        screen.blit(fade,(0,0))

        # popup box
        box_w=500
        box_h=300
        box_rect=pygame.Rect(0,0,box_w,box_h)
        box_rect.center=(width//2,height//2)

        pygame.draw.rect(screen,(40,40,40),box_rect,border_radius=20)
        pygame.draw.rect(screen,(200,200,200),box_rect,3,border_radius=20)

        # winner text
        font_big=pygame.font.Font(None,80)
        text=font_big.render(finalDisplay,True,finalColor)
        screen.blit(text,text.get_rect(center=(box_rect.centerx,box_rect.top+80)))

        # buttons
        btn_w=180
        btn_h=60

        play_again_btn=pygame.Rect(0,0,btn_w,btn_h)
        menu_btn=pygame.Rect(0,0,btn_w,btn_h)

        play_again_btn.center=(box_rect.centerx-110,box_rect.bottom-80)
        menu_btn.center=(box_rect.centerx+110,box_rect.bottom-80)

        pygame.draw.rect(screen,(70,130,180),play_again_btn,border_radius=10)
        pygame.draw.rect(screen,(180,70,70),menu_btn,border_radius=10)

        font_small=pygame.font.Font(None,40)

        txt1=font_small.render("Play Again",True,"white")
        txt2=font_small.render("Leaderboard",True,"white")

        screen.blit(txt1,txt1.get_rect(center=play_again_btn.center))
        screen.blit(txt2,txt2.get_rect(center=menu_btn.center))

    pygame.display.flip()
    clock.tick(tickrate)


        

