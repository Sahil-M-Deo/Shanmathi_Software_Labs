import pygame
import numpy as np
import classGame as cg

pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 50) #(font style,size)

#window variables
width = 1280 
height = 720
tickrate=60
bg_color="black"
#

#turn_time is the time given to each player to make a move in blitz mode
turn_time=5
#

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Connect 4")
clock = pygame.time.Clock()
game_mode = None

#positions of reds and yellows
red = [] 
yellow = []
#

#initialising game board
game = cg.Game()
game.boardHEIGHT=6
game.boardWIDTH=7
game.board = np.full((game.boardHEIGHT,game.boardWIDTH),None)
cell_size=90
x_start=round(width/2-(game.boardWIDTH/2)*cell_size)
x_end=round(width/2+(game.boardWIDTH/2)*cell_size)
y_start = 100
y_end = y_start+(game.boardHEIGHT*cell_size)
r=round(cell_size/2-10) #radius of circle
#

username1="player1"
username2="player2"


def check(self,turn,current_row,current_column):
    board=np.array(self.board)
    streak=4

    def count(arr):
        matches=(arr==turn)
        return np.argmax(~matches) if not matches.all() else len(matches)

    # vertical
    up=count(board[max(0,current_row-streak):current_row,current_column][::-1])
    down=count(board[current_row+1:min(self.boardHEIGHT,current_row+streak+1),current_column])

    # horizontal
    left=count(board[current_row,max(0,current_column-streak):current_column][::-1])
    right=count(board[current_row,current_column+1:min(self.boardWIDTH,current_column+streak+1)])

    # \ diagonal
    diag=board.diagonal(offset=current_column-current_row)
    idx=min(current_row,current_column)

    d1_left=count(diag[max(0,idx-streak):idx][::-1])
    d1_right=count(diag[idx+1:idx+1+streak])

    # / diagonal
    flipped=np.fliplr(board)
    colf=self.boardWIDTH-1-current_column

    diag=flipped.diagonal(offset=colf-current_row)
    idx=min(current_row,colf)

    d2_left=count(diag[max(0,idx-streak):idx][::-1])
    d2_right=count(diag[idx+1:idx+1+streak])

    if (up+down+1>=streak or
        left+right+1>=streak or
        d1_left+d1_right+1>=streak or
        d2_left+d2_right+1>=streak):
        return True

    return False

cg.Game.checkWin = check #implementation done

#username1 is turn=True represented by Red
#username2 is turn=False represented by Yellow

menu=True
while menu:
    screen.fill(bg_color)
    #classic connect4 button
    classic = pygame.Rect(0,0,300,100) #topleft_coordinates,width,height
    classic.center= (width/2,100)
    pygame.draw.rect(screen,"purple",classic)
    
    Ctext = font.render("Classic", True, "pink") #true kya karta hai?
    screen.blit(Ctext, Ctext.get_rect(center=classic.center)) #Text Surface, rectangle to be drawn at

    #blitz connect4 button
    blitz = pygame.Rect(0,0,300,100)
    blitz.center= (width/2,300)
    pygame.draw.rect(screen,"purple",blitz)
    
    Btext = font.render("Blitz", True, "pink")
    screen.blit(Btext, Btext.get_rect(center=blitz.center))


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            menu = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                menu = False

        if event.type == pygame.MOUSEBUTTONUP:
            mousepos=event.pos
            if classic.collidepoint(mousepos):
                game_mode="classic"
                menu=False

            if blitz.collidepoint(mousepos):
                game_mode="blitz"
                menu=False
                
    pygame.display.flip()
    clock.tick(tickrate)



def draw_board():
    board_color="blue"
    hole_color="black"

    # draw board rectangle
    pygame.draw.rect(screen,board_color,(x_start,y_start,7*cell_size,6*cell_size))

    # draw holes
    for row in range(6):
        for col in range(7):
            cx=round(x_start+col*cell_size+cell_size/2)
            cy=round(y_start+row*cell_size+cell_size/2)
            pygame.draw.circle(screen,hole_color,(cx,cy),round(cell_size/2)-5)


def hover(row,col,turn):
    OPACITY=90
    hover_rbgOPACITY=None
    if turn:
        hover_color="red"
        hover_rbgOPACITY=(255,0,0,OPACITY)
    else:
        hover_color="yellow"
        hover_rbgOPACITY=(255,255,0,OPACITY)
    x_pos=round(x_start+col*cell_size+cell_size/2)
    y_pos=round(y_start+row*cell_size+cell_size/2)
    pygame.draw.circle(screen,hover_color,(x_pos,round(y_start-cell_size/2)),r)
    surface=pygame.Surface((2*r,2*r),pygame.SRCALPHA)
    pygame.draw.circle(surface,hover_rbgOPACITY,(r,r),r)
    screen.blit(surface,(x_pos-r,y_pos-r))

time=turn_time
ticks=0
running=True

#when player clicks on an empty cell:
col_filled=np.zeros(game.boardWIDTH,dtype=int) #number of filled cells in each column
def move(row,col,turn):
    
    centre_x=round(x_start+col*cell_size+cell_size/2)
    centre_y=round(y_start+row*cell_size+cell_size/2)
    
    global filled
    filled+=1
    
    col_filled[col]+=1
    
    game.board[row][col]=turn
    
    global time
    time=turn_time
    
    if turn:
        red.append((centre_x,centre_y))
    else:
        yellow.append((centre_x,centre_y))
        
    if game.checkWin(turn,row,col):
        end(turn)
    game.switchTurn()
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
finalDisplay=None
finalColor=None
def end(winner):
    global finalDisplay
    global game_over
    global finalColor
    game_over=True
    if winner == 1:
        name_of_winner=username1
        finalDisplay="RED WINS!"
        finalColor="green"
    elif winner == 0:
        name_of_winner=username2
        finalDisplay="YELLOW WINS!"
        finalColor="green"
    else:
        name_of_winner="TIE"
        finalDisplay="IT'S A TIE!"
        finalColor="grey"

filled=0 #number of filled cells

finalDisplay=None
#main game loop:
while running:
    screen.fill(bg_color)
    x,y = pygame.mouse.get_pos()
    col=(x-x_start)//cell_size

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
                        move(row,col,game.turn)
                        ticks=0
                       
   
    # Board:
    draw_board()

    # adding yellow circles
    for a,b in yellow:
        pygame.draw.circle(screen,"yellow",(a,b),r,0)

    # adding red circles
    for a,b in red:
        pygame.draw.circle(screen,"red",(a,b),r,0)

    if game_mode=="blitz":
        display_timer(0,0,True,game.turn)
        display_timer(980,0,False,game.turn)
        
	# Hover effect:
    if not game_over:
	    if(0<=col<game.boardWIDTH):
	        row=game.boardHEIGHT-1-col_filled[col]
	        hover(row,col,game.turn)
    else:
        fade=pygame.Surface(screen.get_size(),pygame.SRCALPHA)
        fade.fill((0,0,0,180))  # (R,G,B,alpha)
        screen.blit(fade,(0,0))
        font2 = pygame.font.Font(None, 100)
        display_winner = font2.render(finalDisplay, True, finalColor)
        screen.blit(display_winner, display_winner.get_rect(center=(width/2,height/2)))
        
    if not game_over:
        # dealing with a tie
        if filled == game.boardHEIGHT*game.boardWIDTH:
            game_over=True
            end(-1)

        if game_mode=="blitz":
            ticks+=1
            if ticks==tickrate:
                time-=1
                ticks=0
            if time==0:
                end(not game.turn)

                game_over=True

    pygame.display.flip()
    clock.tick(tickrate)

            
pygame.quit()
