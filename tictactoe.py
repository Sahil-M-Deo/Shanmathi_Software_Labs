import pygame
import numpy as np
import classGame as cg
import time

def play(screen,clock,font,username1,username2):
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(None, 50) #(font style,size)

    #COLORS
    YELLOW=(255,220,0)
    RED=(255,0,0)
    BLACK=(0,0,0)
    #

    #window variables
    info=pygame.display.Info()
    width=info.current_w
    height=info.current_h
    print(width,height)
    tickrate=60
    bg_color=BLACK
    #

    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("TicTacToe")
    clock = pygame.time.Clock()
    game_mode = None

    #positions of circles and crosses
    circ = [] 
    cross = []
    #

    #time related variables
    turn_time=10
    last_time=time.time()
    #

    #initialising game board
    game = cg.Game()
    game.boardHEIGHT=10
    game.boardWIDTH=10
    game.board = np.full((game.boardHEIGHT,game.boardWIDTH),None) 
    hover_color="blue"
    cell_size=round(70*height/864)
    x_start = round(width/2-(game.boardWIDTH/2)*cell_size)
    x_end = round(width/2+(game.boardWIDTH/2)*cell_size)
    y_start = round(height/2-(game.boardHEIGHT/2)*cell_size)
    y_end = round(height/2+(game.boardHEIGHT/2)*cell_size)
    r = round(cell_size*7/20) #radius of circle/cross
    #

    username1="player1"
    username2="player2"


    def check(self, turn):
        streak=5
        for i in range(0,6):
            for j in range(0,10):
                if (game.board[i:(i+5),j] == turn).all(): #checks rows
                    return True
        for i in range(0,6):
            for j in range(0,10):
                if (game.board[j,i:(i+5)] == turn).all(): #checks columns
                    return True
        for i in range(0,6):
            for j in range(0,6):
                if ((game.board[i:(i+5),j:(j+5)].diagonal() == turn).all()) or ((np.fliplr(game.board[i:(i+5),j:(j+5)]).diagonal() == turn).all()): #checks diagonals
                    return True
        return False

    cg.Game.checkWin = check #implementation done

    #username1 is turn=True represented by Circle
    #username2 is turn=False represented by Cross

    menu = True
    while menu:
        screen.fill(bg_color)
        #classic tictactoe button
        classic = pygame.Rect(0,0,300,100) #topleft_coordinates,width,height
        classic.center= (width/2,100)
        pygame.draw.rect(screen,"purple",classic)
        
        Ctext = font.render("Classic", True, "pink") #true kya karta hai?
        screen.blit(Ctext, Ctext.get_rect(center=classic.center)) #Text Surface, rectangle to be drawn at

        #blitz tictactoe button
        blitz = pygame.Rect(0,0,300,100)
        blitz.center= (width/2,300)
        pygame.draw.rect(screen,"purple",blitz)
        
        Btext = font.render("Blitz", True, "pink")
        screen.blit(Btext, Btext.get_rect(center=blitz.center))


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                menu = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = False

            if event.type == pygame.MOUSEBUTTONUP:
                mousepos=event.pos
                if classic.collidepoint(mousepos):
                    game_mode="classic"
                    menu=False

                if blitz.collidepoint(mousepos):
                    game_mode="blitz"
                    menu=False
                    
        pygame.display.flip()
        clock.tick(tickrate)



    def draw_board():
        for i in range(x_start, x_end+cell_size, cell_size):
            pygame.draw.line(screen, (200,40,40), (i,y_start), (i,y_end), 5) #(screen,color,start,end,width)

        for i in range(y_start, y_end+cell_size, cell_size):
            pygame.draw.line(screen, "red", (x_start,i), (x_end,i), 5)


    def hover(row,col):
        if row<10 and col<10 and row>=0 and col>=0:
            if game.turn:
                hover_color="dark green"
            else:
                hover_color="blue"
            pygame.draw.rect(screen, hover_color, (x_start+row*cell_size,y_start+col*cell_size,cell_size,cell_size))

    running=True
    #when player clicks on an empty cell:
    def move(row,col,turn):
        centre_x = round(x_start+cell_size/2+row*cell_size) 
        centre_y = round(y_start+cell_size/2+col*cell_size)
        global hover_color
        global filled
        filled+=1
        game.board[row][col]=turn
        
        global last_time
        last_time=time.time()
        global rem_time
        rem_time=turn_time
        
        if turn:
            circ.append((centre_x,centre_y))
            if game.checkWin(turn):
                end(turn)
        else:
            cross.append((centre_x,centre_y))
            if game.checkWin(turn):
                end(turn)
        game.switchTurn()
    #

    def display_timer(x,y,player,turn):
        w=cell_size
        h=game.boardHEIGHT*cell_size
        
        is_active=(player==turn)

        scale=1.06 if is_active else 1.0
        w_scaled=round(w*scale)
        h_scaled=round(h*scale)
        
        rect=pygame.Rect(
            x-(w_scaled-w)//2,
            y-(h_scaled-h)//2,
            w_scaled,
            h_scaled
        )

        if is_active:
            bg=(60,60,60)
            border_color=(25,25,25)
            border_thickness=5
        else:
            bg=(30,30,30)
            border_color=(15,15,15)
            border_thickness=2
        pygame.draw.rect(screen,bg,rect,border_radius=20)
        pygame.draw.rect(screen,border_color,rect,border_thickness,border_radius=20)

        if player==turn:
            t=rem_time
        else:
            t=turn_time

        ratio_raw=t/turn_time
        ratio=ratio_raw*ratio_raw*(3-2*ratio_raw)
        if ratio<0.5:
            r=255
            g=int(880*ratio*ratio) 
        else:
            r=510*(1-ratio)
            g=220
        color=(r,g,0)
        
        padding = 6
        inner_w = rect.width - 2 * padding
        inner_h = rect.height - 2 * padding

        fill_h = round(inner_h * ratio)

        # surface for inner rounded shape
        fill_surf = pygame.Surface((inner_w, inner_h))

        # draw full rounded rect (defines the shape)
        pygame.draw.rect(fill_surf, color, (0, 0, inner_w, inner_h), border_radius = 15)
        # clip from bottom
        if fill_h > 0:
            clipped = fill_surf.subsurface((0, inner_h - fill_h, inner_w, fill_h))
            screen.blit(clipped, (rect.x + padding, rect.y + padding + inner_h - fill_h))

        if not is_active:
            overlay=pygame.Surface((rect.width,rect.height),pygame.SRCALPHA)
            overlay.fill((0,0,0,120))
            screen.blit(overlay,(rect.x,rect.y))

        txt=f"{t:.1f}"
        text=font.render(txt,True,"white")
        screen.blit(text,text.get_rect(center=(rect.centerx,rect.bottom+25)))

    game_over = False

    def end(winner):
        global finalDisplay
        global game_over
        global finalColor
        game_over=True
        if winner == 1:
            name_of_winner=username1
            finalDisplay="RED WINS!"
            finalColor="green"
        elif winner == 0:
            name_of_winner=username2
            finalDisplay="YELLOW WINS!"
            finalColor="green"
        else:
            name_of_winner="TIE"
            finalDisplay="IT'S A TIE!"
            finalColor="grey"

    filled=0 #number of filled cells


    #main game loop:
    while running:
        screen.fill(bg_color)
        x,y = pygame.mouse.get_pos()
        row = (x-x_start)//cell_size
        col = (y-y_start)//cell_size

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            if not game_over:
                if event.type == pygame.MOUSEBUTTONUP:
                    if row<10 and col<10 and row>=0 and col>=0:
                        if game.board[row][col]==None:
                            move(row,col,game.turn)
                            ticks=0
                            

        # Hover effect:
        hover(row,col)
       
        # 10x10 Grid:
        draw_board()

        # adding crosses
        for a, b in cross:
            pygame.draw.line(screen, "white", (a - r, b - r), (a + r, b + r), 6)
            pygame.draw.line(screen, "white", (a + r, b - r), (a - r, b + r), 6)

        # adding circles
        for a, b in circ:
            pygame.draw.circle(screen, "white", (a,b), r, 6)

        if game_mode=="blitz":
            left_x = x_start-1.5*cell_size
            right_x = x_end+0.6*cell_size
            top_y = y_start
            if filled:
                display_timer(left_x, top_y, True, game.turn)
                display_timer(right_x, top_y, False, game.turn)
            else:
                display_timer(left_x, top_y, not game.turn, game.turn)
                display_timer(right_x, top_y, not game.turn, game.turn)



        if not game_over:
            # dealing with a tie
            if filled == game.boardHEIGHT*game.boardWIDTH:
                game_over=True
                end(-1)

            if game_mode=="blitz":
                rem_time = turn_time-(time.time()-last_time)
                if rem_time<=0:
                    rem_time=0
                    end(not game.turn)
        else:
            fade=pygame.Surface(screen.get_size(),pygame.SRCALPHA)
            fade.fill((0,0,0,180))  # (R,G,B,alpha)
            screen.blit(fade,(0,0))
            font2 = pygame.font.Font(None, 100)
            display_winner = font2.render(finalDisplay, True, finalColor)
            screen.blit(display_winner, display_winner.get_rect(center=(width/2,height/2)))

        pygame.display.flip()
        clock.tick(tickrate)

                
    pygame.quit()
