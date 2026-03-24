import pygame
import numpy as np

class Game:

    def __init__(self):
        self.boardWIDTH=0 # x coordinate length
        self.boardHEIGHT=0 # y coordinate length
        self.board=[]
        self.turn= True

    def switchTurn(self):
        self.turn= not self.turn
    def checkWin(self):
        raise NotImplementedError


	