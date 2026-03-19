import pygame
import numpy as np
import sys
#sys.path.insert("../")
import classGame as cg


pygame.init()

width = 600
height = 600
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
    bg_color="green"
    global game_over
    game_over=True
    print(name_of_winner, " wins")

while running:
    screen.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over:
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                row = ((x-5)*10)//500
                col = ((y-5)*10)//500
                centre_x = 30+row*50
                centre_y = 30+col*50
                if (game.turn) and (game.board[row][col]==0):
                    circ.append((centre_x,centre_y))
                    game.switchTurn()
                    game.board[row][col]=1
                    if game.checkWin(1):
                        win("player1")

                elif (not game.turn) and (game.board[row][col]==0):
                    cross.append((centre_x,centre_y))
                    game.switchTurn()
                    game.board[row][col]=-1
                    if game.checkWin(-1):
                        win("player2")
            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    x,y = pygame.mouse.get_pos()
    row = ((x-5)*10)//500
    col = ((y-5)*10)//500
    if row<10 and col<10 and row>=0 and col>=0:
        pygame.draw.rect(screen, "blue", (5+row*50,5+col*50,50,50))

    for i in range(5, 555, 50):
        pygame.draw.line(screen, "red", (i,5), (i,505), 5)

    for i in range(5, 555, 50):
        pygame.draw.line(screen, "red", (5,i), (505,i), 5)

    for a, b in cross:
        pygame.draw.line(screen, "white", (a - 18, b - 18), (a + 18, b + 18), 6)
        pygame.draw.line(screen, "white", (a + 18, b - 18), (a - 18, b + 18), 6)
    for a, b in circ:
        pygame.draw.circle(screen, "white", (a,b), 20, 6)

    pygame.display.flip()
    clock.tick(60)

            
pygame.quit()
