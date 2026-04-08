import pygame
import numpy as np
import classGame as cg
import time

def play(screen,clock,font,username1,username2):
    
    #COLORS
    YELLOW=(255,220,0)
    RED=(255,0,0)
    BLACK=(0,0,0)
    #

    pygame.display.set_caption("TicTacToe")
    
    #window variables
    info=pygame.display.Info()
    width=info.current_w
    height=info.current_h
    tickrate=60
    bg_color=BLACK
    #

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
    def checkWin(self,current_row,current_column):
        board=np.array(self.board)
        streak=5

        def count(arr):            
            matches=(arr==game.turn)
            if matches.all():
                return len(matches)
            else:
                return np.argmax(~matches)

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

        if(up+down+1==streak):
            return ((current_row-up+1/8,current_column+1/2),(current_row+down+7/8,current_column+1/2))
        elif(left+right+1==streak):
            return ((current_row+1/2,current_column-left+1/8),(current_row+1/2,current_column+right+7/8))
        elif(d1_left+d1_right+1==streak):
            return ((current_row-d1_left+1/6,current_column-d1_left+1/6),(current_row+d1_right+5/6,current_column+d1_right+5/6))
        elif(d2_left+d2_right+1==streak):
            return ((current_row-d2_left+1/6,current_column+d2_left+5/6),(current_row+d2_right+5/6,current_column-d2_right+1/6))
        else:
            return False
    
    game = cg.Game(checkWin,10,10)
    cell_size=round(70*height/864)
    x_start = round(width/2-(game.boardWIDTH/2)*cell_size)
    x_end = round(width/2+(game.boardWIDTH/2)*cell_size)
    y_start = round(height/2-(game.boardHEIGHT/2)*cell_size)
    y_end = round(height/2+(game.boardHEIGHT/2)*cell_size)
    r = round(cell_size*7/20) #radius of circle/cross
    #

    #username1 is turn=True represented by Circle
    #username2 is turn=False represented by Cross

    from design_elements import Button

    ClassicRect=pygame.Rect(0,0,round(300*height/864),round(100*height/864))
    ClassicRect.center=(round(width/2),round(2*height/5))
    ClassicButton=Button(screen,font,ClassicRect,"Classic","menu")

    BlitzRect=pygame.Rect(0,0,round(300*height/864),round(100*height/864))
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

    board_paths=[]
    def gen_path(p1,p2,segments=20,jag=1,seed=0):
        import random
        random.seed(seed)
        
        x1,y1=p1
        x2,y2=p2
        
        pts=[]
        for i in range(segments+1):
            f=i/segments
            x=x1+(x2-x1)*f+random.uniform(-jag,jag)
            y=y1+(y2-y1)*f+random.uniform(-jag,jag)
            pts.append((x,y))
        return pts
    def init_board():
        seed=12345
        
        # vertical lines
        for idx,i in enumerate(range(x_start+cell_size,x_end,cell_size)):
            path=gen_path((i,y_start),(i,y_end),segments=2000,jag=1,seed=seed+idx)
            path[0]=(i,y_start)
            path[-1]=(i,y_end)
            board_paths.append(path)
        
        # horizontal lines
        offset=len(board_paths)
        for idx,i in enumerate(range(y_start+cell_size,y_end,cell_size)):
            path=gen_path((x_start,i),(x_end,i),segments=2000,jag=1,seed=seed+offset+idx)
            path[0]=(x_start,i)
            path[-1]=(x_end,i)
            board_paths.append(path)
    init_board()
    def draw_board():
        for path in board_paths:
            pygame.draw.lines(screen,(180,180,180),False,path,5)


    def hover(row,col):
        if game.turn:
            hover_color="dark green"
        else:
            hover_color="blue"
        pygame.draw.rect(screen, hover_color, (x_start+col*cell_size,y_start+row*cell_size,cell_size,cell_size))

    running=True
    win_path=None
    #when player clicks on an empty cell:
    def move(row,col):
        centre_x = round(x_start+cell_size/2+col*cell_size) 
        centre_y = round(y_start+cell_size/2+row*cell_size)

        nonlocal filled
        filled+=1
        game.board[row][col]=game.turn
        
        nonlocal last_time
        last_time=time.time()
        nonlocal rem_time
        rem_time=turn_time
        
        if game.turn:
            circ.append((centre_x,centre_y,time.time()))
        else:
            t=time.time()
            
            # when adding a cross:
            a=centre_x
            b=centre_y
            seed_base=int(time.time()*1000)  # unique but stable
            path1=gen_path((a-r,b-r),(a+r,b+r),seed=seed_base)
            path2=gen_path((a+r,b-r),(a-r,b+r),seed=seed_base+1)
            cross.append((a,b,t,path1,path2))
        
        check=game.checkWin(row,col)
        nonlocal win_path

        if check:
            (r1,c1),(r2,c2)=check

            x1=round(x_start+c1*cell_size)
            y1=round(y_start+r1*cell_size)
            x2=round(x_start+c2*cell_size)
            y2=round(y_start+r2*cell_size)

            win_path=gen_path((x1,y1),(x2,y2),segments=200,jag=1.5,seed=999)
            end(game.turn)
        game.switchTurn()
    #

    def display_timer(x,y,player):
        w=cell_size
        h=game.boardHEIGHT*cell_size
        
        is_active=(player==game.turn)

        scale=1.06 if is_active else 1.0
        w_scaled=round(w*scale)
        h_scaled=round(h*scale)
        
        rect=pygame.Rect(round(x-(w_scaled-w)/2),round(y-(h_scaled-h)/2),w_scaled,h_scaled)

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

        if player==game.turn:
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
        
        padding=6
        inner_w = rect.width-2*padding
        inner_h = rect.height-2*padding

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
    game_over_time=None
    finalDisplay=""
    finalColor="white"
    name_of_winner=None
    name_of_loser=None

    def end(winner):
        nonlocal finalDisplay

        nonlocal game_over
        nonlocal game_over_time
        game_over_time=time.time()
        game_over=True

        nonlocal finalColor
        nonlocal name_of_winner
        nonlocal name_of_loser
        
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

    filled=0 #number of filled cells

    play_again=False
    #main game loop:
    while running:
        screen.fill(bg_color)
        x,y = pygame.mouse.get_pos()
        col = (x-x_start)//cell_size
        row = (y-y_start)//cell_size

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            if not game_over:
                if event.type == pygame.MOUSEBUTTONUP:
                    if col<game.boardWIDTH and col>=0 and row<game.boardHEIGHT and row>=0 and game.board[row][col]==None:
                        move(row,col)
            else:
                if event.type==pygame.MOUSEBUTTONUP:
                    pos=event.pos
                    if play_again_btn.collidepoint(pos):
                        play_again=True
                        running=False #go back to game.py, (stats will be updated and shown there)
                    if menu_btn.collidepoint(pos):
                        running=False      # go back to game.py, (stats will be updated and shown there)
                                       

        # Hover effect:
        if (not game_over) and row<game.boardHEIGHT and col<game.boardWIDTH and row>=0 and col>=0 and game.board[row][col]==None:
            hover(row,col)
       
        #Grid:
        draw_board()

        # adding crosses
        for a,b,t,path1,path2 in cross:
            curr_time=time.time()-t
            draw_time=0.4
            
            f=min(1,curr_time/draw_time)
            
            # first stroke (0 → 0.5)
            PINK=(255, 53, 94)
            if f>0:
                f1=min(1,f/0.3)
                n=int(f1*(len(path1)-1))
                if n>=1:
                    pygame.draw.lines(screen,PINK,False,path1[:n+1],6)
            
            # second stroke (0.5 → 1)
            if f>0.7:
                f2=(f-0.7)/0.3
                n=int(f2*(len(path2)-1))
                if n>=1:
                    pygame.draw.lines(screen,PINK,False,path2[:n+1],6)
            

        # adding circles
        import math
        for a, b, t in circ:
            curr_time=time.time()-t
            draw_time=0.4
            f=min(1,curr_time/draw_time)
            pygame.draw.arc(screen,(200, 217, 102),(a-r,b-r,2*r,2*r),0,2*math.pi*f,3)

        if game_mode=="blitz":
            left_x = round(x_start-1.5*cell_size)
            right_x = round(x_end+0.6*cell_size)
            top_y = y_start
            if filled:
                display_timer(left_x, top_y, True)
                display_timer(right_x, top_y, False)
            else:
                display_timer(left_x, top_y, not game.turn)
                display_timer(right_x, top_y, not game.turn)

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
            if 0.4<time.time()-game_over_time:
                if win_path:
                    draw_time=0.7
                    t=time.time()-game_over_time
                    f=min(1,t/draw_time)

                    n=int(f*(len(win_path)-1))
                    if n>=1:
                        if game.turn:
                            line_color=(255, 53, 94)
                        else:
                            line_color=(200, 217, 102)
                        pygame.draw.lines(screen,line_color,False,win_path[:n+1],8)
            if 1.1<time.time()-game_over_time:
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
