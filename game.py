from datetime import date
import sys
import os
import pygame
import matplotlib
import numpy as np

username1=sys.argv[1]
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
	


gameName=None

import tictactoe as ttt
import connectfour as cf	
import othello as oth
#main game loop, where the user can select which game to play and the game will be executed accordingly
while running:
	#insert pygame stuff here
	if(selection==)
	ttt.play(username1,username2)
#

sys.path.insert("../")
if gameName=="tictactoe":
	winner,loser=ttt.tictactoe(username1,username2)
elif gameName=="connect4":
	winner,loser=cf.connectfour(username1,username2)	
elif gameName=="othello":
	winner,loser=oth.othello(username1,username2)

#modifies stats_{gameName}.csv to update the number of wins and losses for each player
def update_stats(winner,loser,gameName):
	filename="stats_"+gameName+".csv"
	lines=None
	with open(filename, "r") as f:
		lines=f.readlines()
		winnerfound=False
		loserfound=False
		for i in lines:
			if(i.split(",")[0]==winner):
				wins=int(i.split(",")[1])
				losses=int(i.split(",")[2])
				wins+=1
				winnerfound=True
				i=winner + "," + str(wins) + "," + str(losses) + "," + str(wins/losses) + "\n"
			elif(i.split(",")[0]==loser):
				wins=int(i.split(",")[1])
				losses=int(i.split(",")[2])
				losses+=1
				loserfound=True
				i=loser + "," + str(wins) + "," + str(losses) + "," + str(wins/losses) + "\n"
		if(not winnerfound):
			lines.append(winner + ",1,0,inf\n")
		if(not loserfound):
			lines.append(loser + ",0,1,0\n")
	with open(filename, "w") as f:
		f.writelines(lines)
def update_game_frequencies(gameName):
	#modifies game_frequencies.csv to update the number of times each game has been played
	filename="game_frequencies.csv"
	lines=None
	with open(filename, "r") as f:
		lines=f.readlines()
		found=False
		for i in lines:
			if(i.split(",")[0]==gameName):
				freq=int(i.split(",")[1])
				freq+=1
				found=True
				i=gameName + "," + str(freq) + "\n"
		if(not found):
			lines.append(gameName + ",1\n")
	with open(filename, "w") as f:
		f.writelines(lines)

def update_total_wins(winner):
	#modifies user_total_wins.csv to update the number of times each user has won
	filename="user_total_wins.csv"
	lines=None
	with open(filename, "r") as f:
		lines=f.readlines()
		found=False
		for i in lines:
			if(i.split(",")[0]==winner):
				freq=int(i.split(",")[1])
				freq+=1
				found=True
				i=winner + "," + str(freq) + "\n"
		if(not found):
			lines.append(winner + ",1\n")
	with open(filename, "w") as f:
		f.writelines(lines)

update_stats(winner,loser,gameName)
update_game_frequencies(gameName)
update_total_wins(winner)
#username,number of wins, number of losses, and Win/Loss ratio
#game_frequencies is of form: game name, number of times played
#user_total_wins is of form: username, number of wins


#After each game concludes, game.py must append a row to history.csv containing: Winner, Loser, Date, and Game name.
import time
t=time.localtime()
date=t.tm_year+"-"+t.tm_mon+"-"+t.tm_mday
with open("history.csv", "a") as f:
	f.write(winner + "," + loser + "," + date + "," + gameName + "\n")

def show_leaderboard(metric, gameName):
	pygame.init()
	screen=pygame.display.set_mode((800,600))
	pygame.display.set_caption("Leaderboard")

	running=True
	metric=None
	Wbutton=pygame.Rect(100,100,200,50)
	Lbutton=pygame.Rect(100,200,200,50)
	Rbutton=pygame.Rect(100,300,200,50)
	Ebutton=pygame.Rect(100,400,200,50)
	gameName="othello"

	while running:
		screen.fill((30,30,30))
		pygame.draw.rect(screen,(0,200,0),Wbutton)
		pygame.draw.rect(screen,(200,0,0),Lbutton)
		pygame.draw.rect(screen,(0,0,200),Rbutton)
		pygame.draw.rect(screen,(200,200,0),Ebutton)
		font=pygame.font.Font(None,36)
		Wtext=font.render("Wins",True,(0,0,0))
		Ltext=font.render("Losses",True,(0,0,0))
		Rtext=font.render("Ratio",True,(0,0,0))
		ExitText=font.render("See Charts",True,(0,0,0))
		screen.blit(Wtext,Wtext.get_rect(center=Wbutton.center))
		screen.blit(Ltext,Ltext.get_rect(center=Lbutton.center))
		screen.blit(Rtext,Rtext.get_rect(center=Rbutton.center))
		screen.blit(ExitText,ExitText.get_rect(center=Ebutton.center))
		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				running=False
			#pygame.Rect(x, y, width, height)
			if event.type==pygame.MOUSEBUTTONDOWN:
				mousepos=event.pos
				if Wbutton.collidepoint(mousepos):
					metric="wins"
				elif Lbutton.collidepoint(mousepos):
					metric="losses"
				elif Rbutton.collidepoint(mousepos):
					metric="ratio"
				elif Ebutton.collidepoint(mousepos):
					metric="exit"
		if (metric!="exit" and metric!=None):
			command="bash leaderboard.sh " + metric + " " + gameName
			os.system(command)
			metric=None
		if(metric=="exit"):
			running=False
		pygame.display.flip()	

		
show_leaderboard(metric, gameName)