#  Mini Game Hub

A multi-user game hub built using **Bash, Python, and Pygame**, with authentication, multiple games, and persistent leaderboards.

---
##How to setup the game hub
- run `pip install numpy pygame matplotlib` on terminal

##How to Play
- Run `bash main.sh` on terminal in hub folder
- Enter username and password for both players
- Register username by entering new password if not already registered
- Navigate through the games by using buttons, press escape to exit

###  Games
- Tic-Tac-Toe (10*10)
- Othello (8*8)
- Connect Four (7*7)
---

## Ingenuity

- Adding time controls to make things more exciting
- Performance improvement (Time complexity-wise)
- Restricted usernames and passwords to a certain character set by rigorously testing and finding ways to crack the auth procedure
- Used pygame subsurface for a smooth timer animation
- Generalised design elements like buttons, boxes, jagged lines
- Used preprocessed surfaces to reduce pygame draw time
- Animated moves
- Ghost previews of moves
- (More to be added over time)
