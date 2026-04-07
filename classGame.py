import pygame
import numpy as np

class Game:

    def __init__(self,checkWin,boardWIDTH,boardHEIGHT):
        self.checkwin=checkWin
        self.boardWIDTH=boardWIDTH # x coordinate length
        self.boardHEIGHT=boardHEIGHT # y coordinate length
        self.board=np.full((boardHEIGHT,boardWIDTH),None) 
        self.turn=True

    def switchTurn(self):
        self.turn=not(self.turn)	
    def checkWin(self,row,col):
        return self.checkwin(self,row,col)


    