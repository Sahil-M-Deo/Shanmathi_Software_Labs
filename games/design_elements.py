#Getting screen height
import pygame
pygame.init()
info=pygame.display.Info()
HEIGHT=info.current_h
pygame.quit()
#

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
YELLOW=(255,220,0)
RED=(255,0,0)
BOARD_BLUE=(0,0,220)
GREEN=(0,150,0)
WHITE=(255,255,255)
MID_WHITE=(125,125,125)
MILKY_COFFEE=(222,184,135)
DARK_COFFEE=(139,69,19)
TOSS_BLUE=(100,100,250)
TOSS_RED=(250,100,100)
#

def Rect(x,y,w,h): 
    return pygame.Rect(int(Size(x)),int(Size(y)),int(Size(w)),int(Size(h))) #pygame.Rect(x,y,w,h)
def Coord(x,y): 
    return (int(Size(x)),int(Size(y))) #simple tuple of coordinates
class Size:
    SCALE=864 #sahil's screen height
    def __init__(self,val):
        if(isinstance(val,Size)):
            self.val=val.val
        else:
            self.val=float(val)

    def _wrap(self,x):
        return Size(x)

    def _get(self,other):
        if isinstance(other,Size):
            return other.val 
        else:
            return other

    def __add__(self,other):
        return self._wrap(self.val+self._get(other))

    def __radd__(self,other):
        return self.__add__(other)

    def __sub__(self,other):
        return self._wrap(self.val-self._get(other))

    def __rsub__(self,other):
        return self._wrap(self._get(other)-self.val)

    def __neg__(self):
        return self._wrap(-self.val)
    def __mul__(self,other):
        return self._wrap(self.val*self._get(other))

    def __rmul__(self,other):
        return self.__mul__(other)

    def __truediv__(self,other):
        return self._wrap(self.val/self._get(other))

    def __rtruediv__(self,other):
        return self._wrap(self._get(other)/self.val)
    
    def __floordiv__(self, other):
        return self._wrap(self.val//self._get(other))
    
    def __rfloordiv__(self, other):
        return self._wrap(self._get(other)//self.val)
    
    def __pow__(self,other):
        return self._wrap(self.val**self._get(other))

    def __rpow__(self,other):
        return self._wrap(self._get(other)**self.val)

    def px(self):
        return round(HEIGHT*self.val/self.SCALE)

    def __int__(self):
        return self.px()

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
    def __init__(self,screen,rect,text="",fill_color=GRAY_2,border_color=DULL_WHITE,border_thickness=3,border_radius=15,font_color=WHITE):
        self.screen=screen
        self.font=fit_font(text,rect)
        self.rect=rect
        self.text=text
        self.fill_color=fill_color
        self.border_color=border_color
        self.font_color=font_color
        self.border_radius=border_radius
        self.border_thickness=border_thickness

    def draw(self):
        r=self.rect
        fill_color=self.fill_color
        border_color=self.border_color
        pygame.draw.rect(self.screen,fill_color,r,border_radius=self.border_radius)
        pygame.draw.rect(self.screen,border_color,r,self.border_thickness,border_radius=self.border_radius)
        txt=self.font.render(self.text,True,self.font_color)
        self.screen.blit(txt,txt.get_rect(center=r.center))
    

class Button:
    def __init__(self,screen,rect,text,fill_color=GRAY_2,border_color=DULL_WHITE,mode="menu",border_thickness=3,border_radius=15,font_color=WHITE):
        pygame.init()
        self.screen=screen
        self.font=fit_font(text,rect)
        self.rect=rect
        self.text=text
        self.mode=mode
        self.fill_color=fill_color
        self.border_color=border_color
        self.font_color=font_color
        self.border_radius=border_radius
        self.border_thickness=border_thickness
        self.selected=False
    def draw(self,mouse_pos,mouse_pressed):
        offset=0
        if self.mouse_over(mouse_pos):
            if mouse_pressed:
                self.fill_color=(60,60,60)
                offset=2
            else:
                self.fill_color=(100,100,120)
        else:
            self.fill_color=(70,70,70)

        self.border_color=(150,150,150)
        r=self.rect.move(0,offset)

        if self.mode=="leaderboard":
            if self.selected:
                self.fill_color="red"
                self.border_color=(220,220,220)

        pygame.draw.rect(self.screen,self.fill_color,r,border_radius=self.border_radius)
        pygame.draw.rect(self.screen,self.border_color,r,self.border_thickness,border_radius=self.border_radius)

        txt=self.font.render(self.text,True,self.font_color)
        self.screen.blit(txt,txt.get_rect(center=r.center))
    
    def mouse_over(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class JaggedLine:
    def gen_path(self):
        x1,y1=self.p1
        x2,y2=self.p2
        rng=np.random.default_rng(int(time.time_ns()))
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
        n=np.clip(int(fraction*len(self.parts)),2,len(self.parts))
        partial=self.parts[:n]
        pygame.draw.lines(self.screen,self.color,False,partial,5)

class Timer:
    def __init__(self,screen,font,x,y,w,h,total_time):
        self.screen=screen
        self.font=font
        self.rect=Rect(x,y,w,h)
        self.total_time=total_time
        self.remaining=total_time
        self.active=False
        self.active_start=None  # when this player’s turn starts

    def update(self):
        if self.active:
            self.remaining=np.clip(self.total_time-(time.time()-self.active_start),0,self.total_time)
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
        w=int(round(self.rect.width*scale))
        h=int(round(self.rect.height*scale))

        x=int(round(self.rect.x-(w-self.rect.width)/2))
        y=int(round(self.rect.y-(h-self.rect.height)/2))

        r=Rect(x,y,w,h)

        if self.active:
            bg=GRAY_3
            border_color=GRAY_1
            border_thickness=5
        else:
            bg=GRAY_2
            border_color=GRAY_0
            border_thickness=2

        ratio=self.remaining/self.total_time
        ratio=np.clip(ratio*ratio*(3-2*ratio),0,1)

        if ratio<0.5:
            R=255
            G=int(880*ratio*ratio)
        else:
            R=int(510*(1-ratio))
            G=220

        color=(R,G,0)
        fill_h=round(h*ratio)

        # --- SURFACES ---
        FLUID_SURF=pygame.Surface((w,h),pygame.SRCALPHA)
        WINDOW_SURF=pygame.Surface((w,h),pygame.SRCALPHA)
        BORDER_SURF=pygame.Surface((w,h),pygame.SRCALPHA)

        # --- FLUID ---
        FLUID_SURF.fill(BLACK)
        if fill_h>0:
            pygame.draw.rect(FLUID_SURF,color,(0,h-fill_h,w,fill_h))

        # --- WINDOW (cut-out mask) ---
        WINDOW_SURF.fill(BLACK)  # opaque black
        pygame.draw.rect(WINDOW_SURF,(*BLACK,0),(0,0,w,h),border_radius=20)  # special color = hole

        #draw fluid
        self.screen.blit(FLUID_SURF,(x,y))
        # --- APPLY WINDOW ---
        self.screen.blit(WINDOW_SURF,(x,y))
        # --- BORDER ---
        pygame.draw.rect(BORDER_SURF,border_color,(0,0,w,h),border_thickness,border_radius=20)
        self.screen.blit(BORDER_SURF,(x,y))

        if not self.active:
            overlay=pygame.Surface((w,h),pygame.SRCALPHA)
            overlay.fill((*BLACK,120))
            self.screen.blit(overlay,(x,y))

        txt=f"{self.remaining:.1f}"
        text=self.font.render(txt,True,WHITE)
        self.screen.blit(text,text.get_rect(center=(r.centerx,r.bottom+25)))