import pygame
import numpy as np
import sys
#sys.path.insert("../")
import classGame as cg


pygame.init()

width = 1280 
height = 720
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Learning")
clock = pygame.time.Clock()
running = True
circ = []
cross = []

game = cg.Game()
game.boardHEIGHT=10
game.boardWIDTH=10

game.board = np.zeros((10, 10), dtype=int)

def check(self, value):
    for i in range(0,6):
        for j in range(0,10):
            if (game.board[i:(i+5),j] == value).all():
                return True
    for i in range(0,6):
        for j in range(0,10):
            if (game.board[j,i:(i+5)] == value).all():
                return True
    for i in range(0,6):
        for j in range(0,6):
            if ((game.board[i:(i+5),j:(j+5)].diagonal() == value).all()) or ((np.fliplr(game.board[i:(i+5),j:(j+5)]).diagonal() == value).all()):
                return True
    return False

cg.Game.checkWin = check

#username1 is turn=True represented by 1 in storing value and Circle in the visible board
#username2 is turn=False represented by -1 in storing value and Cross in the visible board
bg_color="black"
game_over = False

def win(name_of_winner):
    global bg_color
    bg_color=(0,150,70)
    global game_over
    game_over=True
    print(name_of_winner, " wins")

cell_size=60
x_start = width//2 - 5*cell_size
x_end = width//2+ 5*cell_size
y_start = 5
y_end = 5+(10*cell_size)
filled=0
r = (cell_size*7)//20
while running:
    screen.fill(bg_color)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                row = ((x-x_start)*10)//(10*cell_size)
                col = ((y-y_start)*10)//(10*cell_size)
                centre_x = x_start+(cell_size//2)+(row*cell_size)
                centre_y = y_start+(cell_size//2)+(col*cell_size)
                if (game.turn) and (game.board[row][col]==0):
                    circ.append((centre_x,centre_y))
                    game.switchTurn()
                    game.board[row][col]=1
                    filled+=1
                    if game.checkWin(1):
                        win("player1")

                elif (not game.turn) and (game.board[row][col]==0):
                    cross.append((centre_x,centre_y))
                    game.switchTurn()
                    game.board[row][col]=-1
                    filled+=1
                    if game.checkWin(-1):
                        win("player2")
    
    # Hover effect:
    x,y = pygame.mouse.get_pos()
    row = ((x-x_start)*10)//(10*cell_size)
    col = ((y-y_start)*10)//(10*cell_size)
    if row<10 and col<10 and row>=0 and col>=0:
        pygame.draw.rect(screen, "blue", (x_start+row*cell_size,y_start+col*cell_size,cell_size,cell_size))
   
    # 10x10 Grid:
    for i in range(x_start, x_end+cell_size, cell_size):
        pygame.draw.line(screen, (200,40,40), (i,y_start), (i,y_end), 5)

    for i in range(y_start, y_end+cell_size, cell_size):
        pygame.draw.line(screen, "red", (x_start,i), (x_end,i), 5)

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
        #print("it's a tie")


    pygame.display.flip()
    clock.tick(60)

            
pygame.quit()
