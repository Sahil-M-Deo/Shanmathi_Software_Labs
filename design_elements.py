import pygame
class Button:
    def __init__(self,screen,font,rect,text,mode):
        pygame.init()
        self.screen=screen
        self.font=font
        self.rect=rect
        self.text=text
        self.mode=mode
        self.selected=False
    def draw(self,mouse_pos,mouse_pressed):
        if self.mode=="menu":
            offset=0
            if self.rect.collidepoint(mouse_pos):
                if mouse_pressed:
                    fill_color=(60,60,60)
                    offset=2
                else:
                    fill_color=(100,100,120)
            else:
                fill_color=(70,70,70)

            border_color=(150,150,150)
            r=self.rect.move(0,offset)

        elif self.mode=="leaderboard":
            if self.selected:
                fill_color=(100,100,120)
                border_color=(220,220,220)
            else:
                fill_color=(70,70,70)
                border_color=(150,150,150)
            r=self.rect

        pygame.draw.rect(self.screen,fill_color,r,border_radius=15)
        pygame.draw.rect(self.screen,border_color,r,3,border_radius=15)

        txt=self.font.render(self.text,True,"white")
        self.screen.blit(txt,txt.get_rect(center=r.center))
    
    def clicked(self,mouse_pos):
        return self.rect.collidepoint(mouse_pos)