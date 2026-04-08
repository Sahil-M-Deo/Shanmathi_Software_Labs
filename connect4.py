import pygame
import numpy as np
import classGame as cg
import time
def play(screen,clock,font,username1,username2):
    
    play_again=False #to check if user wants to play again after a game ends
    name_of_winner=None
    name_of_loser=None
    
    #COLORS
    YELLOW=(255,220,0)
    RED=(255,0,0)
    BLACK=(0,0,0)
    #

    #window variables
    info=pygame.display.Info()
    width=info.current_w
    height=info.current_h
    tickrate=60
    bg_color=BLACK
    #

    #time related variables
    turn_time=10
    last_time=time.time()
    #
    
    pygame.display.set_caption("Connect 4")
    game_mode = None

    #initialising game board
    
    def checkWin(self,current_row,current_column):
        board=np.array(self.board)
        streak=4

        def count(arr):
            matches=(arr==game.turn)
            return np.argmax(~matches) if not matches.all() else len(matches)

        # vertical
        up=count(board[max(0,current_row-streak):current_row,current_column][::-1])
        down=count(board[current_row+1:min(self.boardHEIGHT,current_row+streak+1),current_column])

        # horizontal
        left=count(board[current_row,max(0,current_column-streak):current_column][::-1])
        right=count(board[current_row,current_column+1:min(self.boardWIDTH,current_column+streak+1)])

        # diagonal
        diag=board.diagonal(offset=current_column-current_row)
        idx=min(current_row,current_column)

        d1_left=count(diag[max(0,idx-streak):idx][::-1])
        d1_right=count(diag[idx+1:idx+1+streak])

        # / diagonal
        flipped=np.fliplr(board)
        colf=self.boardWIDTH-1-current_column

        diag=flipped.diagonal(offset=colf-current_row)
        idx=min(current_row,colf)

        d2_left=count(diag[max(0,idx-streak):idx][::-1])
        d2_right=count(diag[idx+1:idx+1+streak])

        if (up+down+1>=streak or left+right+1>=streak or d1_left+d1_right+1>=streak or d2_left+d2_right+1>=streak):
            return True
        return False
    
    game = cg.Game(checkWin,7,7)
    cell_size=round(100*height/864)
    x_start=round(width/2-(game.boardWIDTH/2)*cell_size)
    x_end=round(width/2+(game.boardWIDTH/2)*cell_size)
    y_start=round(height/2-(game.boardHEIGHT/2)*cell_size+cell_size*0.4)
    y_end=y_start+(game.boardHEIGHT*cell_size)
    r=round(cell_size/2-5) #radius of circle
    filled=0 #number of filled cells
    #

    #username1 is turn=True represented by Red
    #username2 is turn=False represented by Yellow

    from design_elements import Button

    from design_elements import Button

    ClassicRect=pygame.Rect(0,0,round(300*height/864),round(100*height/864))
    ClassicRect.center=(round(width/2),round(2*height/5))
    ClassicButton=Button(screen,font,ClassicRect,"Classic","menu")

    BlitzRect=pygame.Rect(0,0,300,100)
    BlitzRect.center=(round(width/2),round(3*height/5))
    BlitzButton=Button(screen,font,BlitzRect,"Blitz","menu")

    menu = True
    while menu:
        screen.fill(bg_color)
        mouse_pos=pygame.mouse.get_pos()
        mouse_pressed=pygame.mouse.get_pressed()[0] #(left, middle, right) mouse button states - for us [0] is relevant
        ClassicButton.draw(mouse_pos,mouse_pressed)
        BlitzButton.draw(mouse_pos,mouse_pressed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu = False
            if event.type == pygame.MOUSEBUTTONUP:
                mousepos=event.pos
                if ClassicButton.clicked(mousepos):
                    game_mode="classic"
                    menu=False
                if BlitzButton.clicked(mousepos):
                    game_mode="blitz"
                    menu=False
                    
        pygame.display.flip()
        clock.tick(tickrate)


    def draw_board():
        board_color="blue"
        hole_color=None
        # draw board rectangle
        pygame.draw.rect(screen,board_color,(x_start,y_start,game.boardWIDTH*cell_size,game.boardHEIGHT*cell_size))

        # draw holes
        for row in range(game.boardHEIGHT):
            for col in range(game.boardWIDTH):
                if game.board[row][col] == 0:
                    hole_color=YELLOW
                elif game.board[row][col] == 1:
                    hole_color=RED
                else:
                    hole_color="black"
                cx=round(x_start+col*cell_size+cell_size/2)
                cy=round(y_start+row*cell_size+cell_size/2)
                pygame.draw.circle(screen,hole_color,(cx,cy),radius=r)


    def hover(row,col,turn):
        OPACITY=90
        hover_rbgOPACITY=None
        if turn:
            hover_color="red"
            hover_rbgOPACITY=(255,0,0,OPACITY)
        else:
            hover_color=YELLOW
            hover_rbgOPACITY=(255,255,0,OPACITY)
        x_pos=round(x_start+col*cell_size+cell_size/2)
        y_pos=round(y_start+row*cell_size+cell_size/2)
        pygame.draw.circle(screen,hover_color,(x_pos,round(y_start-cell_size/2)),r)
        surface=pygame.Surface((2*r,2*r),pygame.SRCALPHA)
        pygame.draw.circle(surface,hover_rbgOPACITY,(r,r),r)
        screen.blit(surface,(x_pos-r,y_pos-r))

    rem_time=turn_time
    ticks=0
    running=True

    #when player clicks on an empty cell:
    col_filled=np.zeros(game.boardWIDTH,dtype=int) #number of filled cells in each column
    def move(row,col):
        
        centre_x=round(x_start+col*cell_size+cell_size/2)
        centre_y=round(y_start+row*cell_size+cell_size/2)

        nonlocal filled
        filled+=1
        
        col_filled[col]+=1
        
        game.board[row][col]=game.turn
        
        nonlocal last_time
        last_time=time.time()
        nonlocal rem_time
        rem_time=turn_time
            
        if game.checkWin(row,col):
            end(game.turn)
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
    finalDisplay=None
    finalColor=None
    def end(winner):
        nonlocal finalDisplay
        nonlocal game_over
        nonlocal finalColor
        nonlocal name_of_winner
        nonlocal name_of_loser
        game_over=True
        if winner == 1:
            name_of_winner=username1
            name_of_loser=username2
            finalDisplay=username1+" WINS!"
            finalColor="green"
        elif winner == 0:
            name_of_winner=username2
            name_of_loser=username1
            finalDisplay=username2+" WINS!"
            finalColor="green"
        else:
            name_of_winner="TIE"
            name_of_loser="TIE"
            finalDisplay="IT'S A TIE!"
            finalColor="grey"

    finalDisplay=None
    #main game loop:
    while running:
        screen.fill(bg_color)
        x,y = pygame.mouse.get_pos()
        col=(x-x_start)//cell_size

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            if not game_over:
                if event.type == pygame.MOUSEBUTTONUP:
                    if col<game.boardWIDTH and col>=0:
                        if col_filled[col]<game.boardHEIGHT:
                            row=game.boardHEIGHT-1-col_filled[col]
                            move(row,col)
            else:
                if event.type==pygame.MOUSEBUTTONUP:
                    pos=event.pos
                    if play_again_btn.collidepoint(pos):
                        play_again=True
                        running=False #go back to game.py, (stats will be updated and shown there)
                    if menu_btn.collidepoint(pos):
                        running=False      # go back to game.py, (stats will be updated and shown there)
                           
       
        # Board:
        draw_board()

        if game_mode=="blitz":
            left_x = round(x_start-1.5*cell_size)
            right_x = round(x_end+0.6*cell_size)
            top_y = round(y_start+0.2*cell_size)
            if filled:
                display_timer(left_x, top_y, True, game.turn)
                display_timer(right_x, top_y, False, game.turn)
            else:
                display_timer(left_x, top_y, not game.turn, game.turn)
                display_timer(right_x, top_y, not game.turn, game.turn)
        
        if not game_over:
            if(0<=col<game.boardWIDTH):
                row=game.boardHEIGHT-1-col_filled[col]
                hover(row,col,game.turn)
                
            if filled == game.boardHEIGHT*game.boardWIDTH:
                game_over=True
                end(-1)

            if game_mode=="blitz":
                rem_time = turn_time-(time.time()-last_time)
                if rem_time<=0:
                    rem_time=0
                    end(not game.turn)
        else:
            # dark overlay
            fade=pygame.Surface(screen.get_size(),pygame.SRCALPHA)
            fade.fill((0,0,0,180))
            screen.blit(fade,(0,0))

            # popup box
            box_w=500
            box_h=300
            box_rect=pygame.Rect(0,0,box_w,box_h)
            box_rect.center=(width//2,height//2)

            pygame.draw.rect(screen,(40,40,40),box_rect,border_radius=20)
            pygame.draw.rect(screen,(200,200,200),box_rect,3,border_radius=20)

            # winner text
            font_big=pygame.font.Font(None,80)
            text=font_big.render(finalDisplay,True,finalColor)
            screen.blit(text,text.get_rect(center=(box_rect.centerx,box_rect.top+80)))

            # buttons
            btn_w=180
            btn_h=60

            play_again_btn=pygame.Rect(0,0,btn_w,btn_h)
            menu_btn=pygame.Rect(0,0,btn_w,btn_h)

            play_again_btn.center=(box_rect.centerx-110,box_rect.bottom-80)
            menu_btn.center=(box_rect.centerx+110,box_rect.bottom-80)

            pygame.draw.rect(screen,(70,130,180),play_again_btn,border_radius=10)
            pygame.draw.rect(screen,(180,70,70),menu_btn,border_radius=10)

            font_small=pygame.font.Font(None,40)

            txt1=font_small.render("Play Again",True,"white")
            txt2=font_small.render("Leaderboard",True,"white")

            screen.blit(txt1,txt1.get_rect(center=play_again_btn.center))
            screen.blit(txt2,txt2.get_rect(center=menu_btn.center))
                           

        pygame.display.flip()
        clock.tick(tickrate)
    return name_of_winner,name_of_loser,play_again