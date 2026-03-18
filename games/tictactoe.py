import pygame
import numpy as np
import sys
#sys.path.insert("../")
#import game.py as 

pygame.init()

width = 600
height = 600
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Learning")
clock = pygame.time.Clock()
running = True
circ = []
cross = []
player1 = True

visited = np.zeros((10, 10), dtype=bool)

while running:
    screen.fill("light blue")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()
            row = ((x-5)*10)//500
            col = ((y-5)*10)//500
            centre_x = 30+row*50
            centre_y = 30+col*50
            if player1 and (not visited[row][col]):
                circ.append((centre_x,centre_y))
                player1 = False
                visited[row][col]=True
            elif (not player1) and (not visited[row][col]):
                cross.append((centre_x,centre_y))
                player1 = True
                visited[row][col]=True
            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    x,y = pygame.mouse.get_pos()
    row = ((x-5)*10)//500
    col = ((y-5)*10)//500
    if row<10 and col<10 and row>=0 and col>=0:
        pygame.draw.rect(screen, "pink", (5+row*50,5+col*50,50,50))

    for i in range(5, 555, 50):
        pygame.draw.line(screen, "black", (i,5), (i,505), 5)

    for i in range(5, 555, 50):
        pygame.draw.line(screen, "black", (5,i), (505,i), 5)

    for a, b in cross:
        pygame.draw.line(screen, "red", (a - 18, b - 18), (a + 18, b + 18), 6)
        pygame.draw.line(screen, "red", (a + 18, b - 18), (a - 18, b + 18), 6)
    for a, b in circ:
        pygame.draw.circle(screen, "black", (a,b), 20, 6)

    pygame.display.flip()

            
pygame.quit()
