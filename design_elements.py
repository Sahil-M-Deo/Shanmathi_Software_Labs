import pygame
import numpy as np
import time
#COLORS
BLACK=(0,0,0)
CROSS_PINK=(255,53,94)
CIRCLE_YELLOW=(200,217,102)
GRAY_3=(60,60,60)
GRAY_2=(30,30,30)
GRAY_1=(25,25,25)
GRAY_0=(15,15,15)
GRAY_4=(40, 40, 40)
DULL_WHITE=(200, 200, 200)
CALM_BLUE=(70, 130, 180)
CUTE_RED=(180, 70, 70)
#

def fit_font(text,rect):
    lo=1
    hi=100  # upper bound (adjust if needed)
    ans=1

    while lo<=hi:
        mid=(lo+hi)//2
        font=pygame.font.Font(None,mid)
        w,h=font.size(text)

        if w<=0.7*rect.width and h<=0.7*rect.height:
            ans=mid
            lo=mid+1
        else:
            hi=mid-1

    return pygame.font.Font(None,ans)

class Box:
    def __init__(self,screen,rect,text="",fill_color=GRAY_2,border_color=DULL_WHITE,border_thickness=3,border_radius=15):
        self.screen=screen
        self.font=fit_font(text,rect)
        self.rect=rect
        self.text=text
        self.fill_color=fill_color
        self.border_color=border_color
        self.border_radius=border_radius
        self.border_thickness=border_thickness

    def draw(self):
        r=self.rect
        fill_color=self.fill_color
        border_color=self.border_color

        pygame.draw.rect(self.screen,fill_color,r,border_radius=self.border_radius)
        pygame.draw.rect(self.screen,border_color,r,self.border_thickness,border_radius=self.border_radius)
    
def cap(x,low,high):
    if x<low:
        return low
    elif x>high:
        return high
    else:
        return x
    

class Button:
    def __init__(self,screen,rect,text,fill_color=GRAY_2,border_color=DULL_WHITE,mode="menu",border_thickness=3,border_radius=15):
        pygame.init()
        self.screen=screen
        self.font=fit_font(text,rect)
        self.rect=rect
        self.text=text
        self.mode=mode
        self.fill_color=fill_color
        self.border_color=border_color
        self.border_radius=border_radius
        self.border_thickness=border_thickness
        self.selected=False
    def draw(self,mouse_pos,mouse_pressed):
        if self.mode=="menu":
            offset=0
            if self.rect.collidepoint(mouse_pos):
                if mouse_pressed:
                    self.fill_color=(60,60,60)
                    offset=2
                else:
                    self.fill_color=(100,100,120)
            else:
                self.fill_color=(70,70,70)

            self.border_color=(150,150,150)
            r=self.rect.move(0,offset)

        elif self.mode=="leaderboard":
            if self.selected:
                self.fill_color=(100,100,120)
                self.border_color=(220,220,220)
            else:
                self.fill_color=(70,70,70)
                self.border_color=(150,150,150)
            r=self.rect

        pygame.draw.rect(self.screen,self.fill_color,r,border_radius=self.border_radius)
        pygame.draw.rect(self.screen,self.border_color,r,self.border_thickness,border_radius=self.border_radius)

        txt=self.font.render(self.text,True,"white")
        self.screen.blit(txt,txt.get_rect(center=r.center))
    
    def clicked(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class JaggedLine:
    def gen_path(self):
        x1,y1=self.p1
        x2,y2=self.p2
        rng=np.random.default_rng(int(time.time()))
        listX=np.linspace(x1,x2,self.segments+1)+rng.uniform(-self.jag,self.jag,self.segments+1)
        listY=np.linspace(y1,y2,self.segments+1)+rng.uniform(-self.jag,self.jag,self.segments+1)
        pts=list(zip(listX,listY))
        return pts
    def __init__(self,screen,p1,p2,color,segments=200,jag=1):
        self.screen=screen
        self.p1=p1
        self.p2=p2
        self.color=color
        self.segments=segments
        self.jag=jag
        self.parts=self.gen_path()
    
    def draw(self):	
        pygame.draw.lines(self.screen,self.color,False,self.parts,5)
    def draw_partial(self,fraction):
        n=cap(int(fraction*len(self.parts)),2,len(self.parts))
        partial=self.parts[:n]
        pygame.draw.lines(self.screen,self.color,False,partial,5)

class Timer:
    def __init__(self,screen,font,x,y,w,h,total_time):
        self.screen=screen
        self.font=font
        self.rect=pygame.Rect(x,y,w,h)
        self.total_time=total_time
        self.remaining=total_time
        self.active=False
        self.active_start=None  # when this player’s turn starts

    def update(self):
        if self.active:
            self.remaining=cap(self.total_time-(time.time()-self.active_start),0,self.total_time)
            return (self.remaining>0)
        else:
            return True

    def end(self):
        self.active=False
        self.remaining=self.total_time
    def switchTurn(self):
        self.active=not self.active
        if self.active:
            self.active_start=time.time()
        else:
            self.remaining=self.total_time

    def display(self):
        scale=1.06 if self.active else 1.0
        w=round(self.rect.width*scale)
        h=round(self.rect.height*scale)

        r=pygame.Rect(
            round(self.rect.x-(w-self.rect.width)/2),
            round(self.rect.y-(h-self.rect.height)/2),
            w,h
        )

        # colors
        if self.active:
            bg=GRAY_3
            border_color=GRAY_1
            border_thickness=5
        else:
            bg=GRAY_2
            border_color=GRAY_0
            border_thickness=2

        pygame.draw.rect(self.screen,bg,r,border_radius=20)
        pygame.draw.rect(self.screen,border_color,r,border_thickness,border_radius=20)

        # ratio
        ratio=self.remaining/self.total_time
        ratio=ratio*ratio*(3-2*ratio)

        if ratio<0.5:
            R=255
            G=int(880*ratio*ratio)
        else:
            R=int(510*(1-ratio))
            G=220

        color=(R,G,0)

        padding=6
        inner_w=r.width-2*padding
        inner_h=r.height-2*padding
        fill_h=round(inner_h*ratio)

        fill_surf=pygame.Surface((inner_w,inner_h))
        pygame.draw.rect(fill_surf,color,(0,0,inner_w,inner_h),border_radius=15)

        if fill_h>0:
            clipped=fill_surf.subsurface((0,inner_h-fill_h,inner_w,fill_h))
            self.screen.blit(clipped,(r.x+padding,r.y+padding+inner_h-fill_h))

        if not self.active:
            overlay=pygame.Surface((r.width,r.height),pygame.SRCALPHA)
            overlay.fill((0,0,0,120))
            self.screen.blit(overlay,(r.x,r.y))

        txt=f"{self.remaining:.1f}"
        text=self.font.render(txt,True,"white")
        self.screen.blit(text,text.get_rect(center=(r.centerx,r.bottom+25)))