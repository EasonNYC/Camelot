from pygame import *
import os
import sys
position = 25, 25
os.environ['SDL_VIDEO_WINDOW_POS'] = str(position[0]) + "," + str(position[1])
# switch to modules folder
sys.path.append('modules')
from Game import *
from button import *

from AI import *
# from globals import *

#initialize a model view and hal
game = CamelotGame()

#TILE_WIDTH = 45

#setup hal animation sprite
hals_eye_sprite = HALSprite()
halsEyeAnimation = pygame.sprite.Group(hals_eye_sprite)

#background sound setup
pygame.mixer.music.load('sound/bgsfx.mp3')
pygame.mixer.music.play(-1)  #play infinitly

#main font to use
font = pygame.font.SysFont("comicsansms", 14)






"""predefined colors"""
#black = (0, 0, 0)
#white = (255, 255, 255)
#Grey = (128, 128, 128)
#Green = (0, 128, 0)
#Yellow = (255, 255, 0)


"""game loop"""
#pygame stuff
init()
#screen = pygame.display.set_mode((1100, 900))

pygame.display.set_caption('Camelot with VREP interface - by David Eason Smith (des460@NYU.edu)')

game.draw() #initial draw of gameboard and pieces and black bg

print("hal is playing as "+ game.hal.getColor())

#### main game loop
game.loop()

#play_sound('sound/goodbye.wav')
pygame.quit()

