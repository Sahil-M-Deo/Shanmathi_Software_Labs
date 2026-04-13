#  Mini Game Hub

A multi-user game hub built using **Bash, Python, and Pygame**, with authentication, multiple games, and persistent leaderboards.

---

##  Overview

- Two users authenticate via Bash
- Python (Pygame) handles gameplay
- Results stored in `history.csv`
- Leaderboards and analytics generated
---

##  Features

###  Authentication
- SHA-256 hashed passwords
- Stored in `users.tsv`
- Login + registration support
- Two-player authentication
- **3-attempt limit per user**
- **Temporary lockout using time-based restriction (tracks last failed attempt)**

---

###  Game Engine
- GUI-based menu (Pygame)
- Base class for all games
---

###  Games
- Tic-Tac-Toe (10*10)
- Othello
- Connect Four (7*7)
- JKLM-style word game (extension)
- Not decided which more (if any)
---

##  File Structure

```
hub/
├── main.sh
├── game.py
├── leaderboard.sh
├── games/ (one .py file per game and one file containing the class Game inherited by all games)
├── users.tsv
└── history.csv
```

---

##  Design

- Common base class:
  - Players, turns, board (NumPy)
  - Win-condition abstraction
- Each game implemented separately
- Clear separation:
  - Bash → auth + leaderboard
  - Python → gameplay

---

##  Performance Improvement

Denote number of games to be n, number of users to be u

**Issue:** Recomputing stats from `history.csv` each time is O(nlogn+n) after every game, since we have to sort by user and combine stats pertaining to different games

**Solution:** Maintain incremental stats: O(u) after every game
- Update per-user stats after each match
- Simple linear-scan

Note: It is logical to conclude that n>u so this optimisation is very much justified, this requires every user to play on an average at least two games (Sum of degrees of vertices = number of edges/2)

**Result:** Faster and scalable leaderboard generation.

---

##  Leaderboard

- Tracks wins, losses, ratio
- Sorting by different metrics supported
- Matplotlib charts:
  - Top players
  - Most played games

---


##  Dependencies

- Python 3
- pygame-ce
- numpy
- matplotlib
- os
- time
---
## Ingenuity

- Adding time controls to make things more exciting
- Performance improvement (Time complexity-wise)
- Restricted usernames and passwords to a certain character set by rigorously testing and finding ways to crack the auth procedure
- Used pygame subsurface for a smooth timer animation
- Generalised design elements like buttons
- (More to be added over time)
