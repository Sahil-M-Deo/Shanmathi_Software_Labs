import pygame
import numpy as np
import classGame as cg
import time


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
game = cg.Game()
game.boardHEIGHT=8
game.boardWIDTH=8
game.board = np.full((game.boardHEIGHT,game.boardWIDTH),None) 
hover_color="blue"
cell_size=80
x_start = width//2 - (game.boardWIDTH//2)*cell_size
x_end = width//2+ (game.boardWIDTH//2)*cell_size
y_start = 5
y_end = 5+(game.boardHEIGHT*cell_size)
r = (cell_size*2)//5 #radius of pieces

game.board[3][3]=game.board[4][4]=False  #othello board init
game.board[3][4]=game.board[4][3]=True
#

username1="player1"
username2="player2"

#time related variables
turn_time=10
last_time=time.time()

def check(self, turn):
    streak=5
    #yet to write
    return False

cg.Game.checkWin = check #implementation done

#username1 is turn=True represented by Circle
#username2 is turn=False represented by Cross

from design_elements import Button

ClassicRect=pygame.Rect(0,0,round(300*height/864),round(100*height/864))
ClassicRect.center=(round(width/2),round(2*height/5))
ClassicButton=Button(screen,font,ClassicRect,"Classic","menu")

BlitzRect=pygame.Rect(0,0,round(300*height/864),round(100*height/864))
BlitzRect.center=(round(width/2),round(3*height/5))
BlitzButton=Button(screen,font,BlitzRect,"Blitz","menu")

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
    for i in range(x_start, x_end+cell_size, cell_size):
        pygame.draw.line(screen, (139, 69, 19), (i,y_start), (i,y_end), 5) #(screen,color,start,end,width)

    for i in range(y_start, y_end+cell_size, cell_size):
        pygame.draw.line(screen, (139, 69, 19), (x_start,i), (x_end,i), 5)


def hover(row,col):
    if row<10 and col<10 and row>=0 and col>=0:
        pygame.draw.rect(screen, hover_color, (x_start+row*cell_size,y_start+col*cell_size,cell_size,cell_size))





turn_time=5
time=turn_time
ticks=0
running=True

def centre_x(row):
    return x_start+(cell_size//2)+(row*cell_size)
def centre_y(col):
    return y_start+(cell_size//2)+(col*cell_size)


#positions of white and black pieces
white = [(centre_x(3),centre_y(4)),(centre_x(4),centre_y(3))] 
black = [(centre_x(3),centre_y(3)),(centre_x(4),centre_y(4))]
#


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
                            valid_cells.append((centre_x(i),centre_y(j)))


#when player clicks on an empty cell:
def move(row,col):
    global hover_color
    global filled
    global time
    filled+=1
    game.board[row][col]=game.turn
    time=turn_time
    if game.turn:
        white.append((centre_x(row),centre_y(col)))
        hover_color="dark green"
        if game.checkWin(game.turn):
            win(game.turn)
    else:
        black.append((centre_x(row),centre_y(col)))
        hover_color="blue"
        if game.checkWin(game.turn):
            win(game.turn)
    game.switchTurn()
    global valid_cells
    valid_cells.clear()
    validMoves()
#

def display_timer(x,y,player,turn):
    timer_box = pygame.Rect(x,y,300,100)
    pygame.draw.rect(screen, "yellow", timer_box)
    if player==turn:
        display=str(time)
    else:
        display=str(turn_time)

    display_time = font.render(display, True, (0,0,0))
    screen.blit(display_time, display_time.get_rect(center=timer_box.center))


game_over = False
finalDisplay=""
finalColor="white"
name_of_winner=None
name_of_loser=None

def win(turn):
    global bg_color
    bg_color=(0,150,70)
    global game_over
    game_over=True
    if turn:
        name_of_winner=username1
    else:
        name_of_winner=username2

    print(name_of_winner, " wins")

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
play_again=False
    #main game loop:
while running:
    screen.fill(bg_color)
    x,y = pygame.mouse.get_pos()
    row = (x-x_start)//cell_size
    col = (y-y_start)//cell_size

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

    # adding crosses
    for a, b in white:
        pygame.draw.circle(screen, "white", (a,b), r)

    # adding circles
    for a, b in black:
        pygame.draw.circle(screen, "black", (a,b), r)

    for a,b in valid_cells:
        pygame.draw.circle(screen, "green", (a,b), r/5)

    if game_mode=="blitz":
        left_x = round(x_start-1.5*cell_size)
        right_x = round(x_end+0.6*cell_size)
        top_y = y_start
        if filled:
            display_timer(left_x, top_y, True)
            display_timer(right_x, top_y, False)
        else:
            display_timer(left_x, top_y, not game.turn)
            display_timer(right_x, top_y, not game.turn)



    if not game_over:
        # dealing with a tie
        if filled == game.boardHEIGHT*game.boardWIDTH:
            game_over=True
            end(-1)

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


        

