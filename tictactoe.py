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

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("TicTacToe")
clock = pygame.time.Clock()
game_mode = None

#positions of circles and crosses
circ = [] 
cross = []
#

#initialising game board
game = cg.Game()
game.boardHEIGHT=10
game.boardWIDTH=10
game.board = np.full((game.boardHEIGHT,game.boardWIDTH),None) 
hover_color="blue"
cell_size=60
x_start = width//2 - (game.boardWIDTH//2)*cell_size
x_end = width//2+ (game.boardWIDTH//2)*cell_size
y_start = 5
y_end = 5+(game.boardHEIGHT*cell_size)
r = (cell_size*7)//20 #radius of circle/cross
#

username1="player1"
username2="player2"


def check(self, turn):
    streak=5
    for i in range(0,6):
        for j in range(0,10):
            if (game.board[i:(i+5),j] == turn).all(): #checks rows
                return True
    for i in range(0,6):
        for j in range(0,10):
            if (game.board[j,i:(i+5)] == turn).all(): #checks columns
                return True
    for i in range(0,6):
        for j in range(0,6):
            if ((game.board[i:(i+5),j:(j+5)].diagonal() == turn).all()) or ((np.fliplr(game.board[i:(i+5),j:(j+5)]).diagonal() == turn).all()): #checks diagonals
                return True
    return False

cg.Game.checkWin = check #implementation done

#username1 is turn=True represented by Circle
#username2 is turn=False represented by Cross

menu = True
while menu:
    screen.fill(bg_color)
    #classic tictactoe button
    classic = pygame.Rect(0,0,300,100) #topleft_coordinates,width,height
    classic.center= (width/2,100)
    pygame.draw.rect(screen,"purple",classic)
    
    Ctext = font.render("Classic", True, "pink") #true kya karta hai?
    screen.blit(Ctext, Ctext.get_rect(center=classic.center)) #Text Surface, rectangle to be drawn at

    #blitz tictactoe button
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
    for i in range(x_start, x_end+cell_size, cell_size):
        pygame.draw.line(screen, (200,40,40), (i,y_start), (i,y_end), 5) #(screen,color,start,end,width)

    for i in range(y_start, y_end+cell_size, cell_size):
        pygame.draw.line(screen, "red", (x_start,i), (x_end,i), 5)


def hover(row,col):
    if row<10 and col<10 and row>=0 and col>=0:
        pygame.draw.rect(screen, hover_color, (x_start+row*cell_size,y_start+col*cell_size,cell_size,cell_size))



'''
while classic_game:
    screen.fill(bg_color)
    x,y = pygame.mouse.get_pos()
    row = ((x-x_start)*10)//(10*cell_size)
    col = ((y-y_start)*10)//(10*cell_size)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            classic_game = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                classic_game = False

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if row<10 and col<10 and row>=0 and col>=0:
                    if (game.turn) and (game.board[row][col]==0):
                        u1_move(row,col)

                    elif (not game.turn) and (game.board[row][col]==0):
                        u2_move(row,col)
                        
    
    # Hover effect:
    hover(row,col)
   
    # 10x10 Grid:
    draw_board()

    # adding crosses
    for a, b in cross:
        pygame.draw.line(screen, "white", (a - r, b - r), (a + r, b + r), 6)
        pygame.draw.line(screen, "white", (a + r, b - r), (a - r, b + r), 6)

    # adding circles
    for a, b in circ:
        pygame.draw.circle(screen, "white", (a,b), r, 6)

    # dealing with a tie
    if (filled == 100) and (not game_over):
        game_over=True
        print("it's a tie")

    pygame.display.flip()
    clock.tick(tickrate)
    '''




turn_time=5
time=turn_time
ticks=0
running=True

#when player clicks on an empty cell:
def move(row,col,turn):
    centre_x = x_start+(cell_size//2)+(row*cell_size)
    centre_y = y_start+(cell_size//2)+(col*cell_size)
    global hover_color
    global filled
    global time
    filled+=1
    game.board[row][col]=turn
    time=turn_time
    if turn:
        circ.append((centre_x,centre_y))
        hover_color="dark green"
        if game.checkWin(turn):
            win(turn)
    else:
        cross.append((centre_x,centre_y))
        hover_color="blue"
        if game.checkWin(turn):
            win(turn)
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
                if row<10 and col<10 and row>=0 and col>=0:
                    if game.board[row][col]==None:
                        move(row,col,game.turn)
                        ticks=0
                        

    # Hover effect:
    hover(row,col)
   
    # 10x10 Grid:
    draw_board()

    # adding crosses
    for a, b in cross:
        pygame.draw.line(screen, "white", (a - r, b - r), (a + r, b + r), 6)
        pygame.draw.line(screen, "white", (a + r, b - r), (a - r, b + r), 6)

    # adding circles
    for a, b in circ:
        pygame.draw.circle(screen, "white", (a,b), r, 6)

    if game_mode=="blitz":
        display_timer(0,0,True,game.turn)
        display_timer(980,0,False,game.turn)



    if not game_over:
        # dealing with a tie
        if filled == 100:
            game_over=True
            #print("it's a tie")

        if game_mode=="blitz":
            ticks+=1
            if ticks==tickrate:
                time-=1
                ticks=0
            if time==0:
                win(not game.turn)

                game_over=True

    pygame.display.flip()
    clock.tick(tickrate)

            
pygame.quit()
