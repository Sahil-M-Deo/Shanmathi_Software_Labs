import pygame
import numpy as np

class Game:
    def __init__(self,checkWin,boardWIDTH,boardHEIGHT,cell_size):
        self.checkwin=checkWin
        self.boardWIDTH=boardWIDTH # x coordinate length
        self.boardHEIGHT=boardHEIGHT # y coordinate length
        self.cell_size=cell_size
        self.board=np.full((boardHEIGHT,boardWIDTH),None) 
        self.turn=True

    def switchTurn(self):
        self.turn=not(self.turn)	
    def checkWin(self,row,col):
        return self.checkwin(self,row,col)
    
    def valid_move(self,row,col):
        return row<self.boardHEIGHT and col<self.boardWIDTH and col>=0 and row>=0


    