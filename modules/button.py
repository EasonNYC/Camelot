#general button class for camelot. used for next turn. reset?


import pygame
from pygame.locals import *
pygame.init()
class Button:
    def __init__(self):
        self.curText = ""
    def createButton(self, surface, color, length, height, x, y, width):
        for i in range(1,10):
            #create button surface
            s = pygame.Surface((length+(i*2),height+i*2))
            #fill in button with color
            s.fill(color)
            
            alpha = (255/(i+2))
            if alpha <= 0:
                alpha = 1
            s.set_alpha(alpha)
            
            pygame.draw.rect(s, color, (x-i, y-i, length+i,height+i), width)
            surface.blit(s, (x-i,y-i))
        pygame.draw.rect(surface, color, (x,y, length, height),0)
        pygame.draw.rect(surface, (190,190,190), (x,y,length,height),1)
        return surface

    def writetext(self, surface, text, text_color, length, height, x, y):
        fontsize = int(length//len(text))
        myFont = pygame.font.SysFont("Ariel", fontsize)
        myText = myFont.render(text, 1, text_color)
        surface.blit(myText, ((x+length/2) - myText.get_width()/2, (y+height/2) - myText.get_height()/2))
        return surface
    
    def draw(self, surface, color, x, y, length, height, width, text, text_color):
        surface = self.createButton(surface, color, length, height, x, y, width)
        surface = self.writetext(surface, text, text_color, length, height, x, y)
        self.rect = pygame.Rect( x, y, length, height)
        self.curText = text
        return surface

    #returns true when mouse is hovering over this button instance
    def pressed(self, mouse):
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        #print("A button was pressed.")
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False
    
