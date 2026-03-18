import sys
import numpy as np

u1=sys.argv[1]
username2=sys.argv[2]

print("Welcome to the game, " + username1 + " and " + username2 + "!")

class Game:
    def __init__(self):
        self.boardWIDTH=0 #x coordinate length
		self.boardHEIGHT=0 #y coordinate length
        self.board=[]
        self.turn=0

    def switchTurn(self):
        self.turn=not self.turn
    def check_win(self):
        raise NotImplementedError
