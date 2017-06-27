import os
import pygame
import copy
import random
from board import *
from button import *
from AI import *
from time import gmtime, strftime


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

Gamestate = enum('mainmenu', 'play')
Difficulty = enum('Easy', 'Medium', 'Hard')

#sound
_sound_library = {}
def play_sound(path):
    global _sound_library
    sound = _sound_library.get(path)
    if sound == None:
        canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
        sound = pygame.mixer.Sound(canonicalized_path)
        _sound_library[path] = sound
    sound.play()

lastsound = None
def getSound(soundlist):
    global lastsound
    # returns a random name of the person
    x = random.choice(soundlist)

    # insures the same name wont be called twice
    while x == lastsound:
        x = random.choice(soundlist)
        lastsound = x
    return x


hal_greeting  = ['sound/chess2.wav',
             'sound/good_evening.wav',
             'sound/hello.wav',
             'sound/this_is_hal.wav']
hal_wins = ['sound/enjoyable_game.wav',
             'sound/well2.wav']
hal_loses = ['sound/atfullestuse.wav',
             'sound/goodbye.wav',
             'sound/stop.wav',]

hal_winning = ['sound/delay.wav',
              'sound/disconnect_me.wav',
              'sound/foolproof.wav',
              'sound/functional.wav',
              'sound/mission.wav',
              'sound/one_moment.wav',
              'sound/operational.wav',
              'sound/suggestion.wav',
              'sound/vocal_stress.wav',
              'sound/well.wav',
              'sound/fault.wav',
              'sound/moment.wav']

hal_losing = ['sound/chess2.wav',
             'sound/decision.wav',
             'sound/disconnect_me.wav',
             'sound/feel_much_better.wav',
             'sound/disconnectme.wav',
             'sound/HAL_9000.wav',
             'sound/human_error.wav',
             'sound/just_what',
             'sound/mind_is_going.wav',
             'sound/quite_like_this.wav',
             'sound/quite_sure.wav',
             'sound/stop.wav',
             'sound/stop2.wav',
             'sound/stress_pill.wav',
             'sound/quite_sure.wav',
             'sound/error.wav',
             'sound/halodd.wav',]



# this is the basic class which holds the current (prime) board displayed on the screen.
class CamelotGame(object):

    difficulty = Difficulty.Hard
    done = False
    def __init__(self):

        self.screen = pygame.display.set_mode((1100, 900))

        self.clock = pygame.time.Clock()

        """creates an initial camelot state(board) with 2 players and pieces at their starting positions"""
        w = set([Coord(4, 2), Coord(4, 3), Coord(4, 4), Coord(4, 5), Coord(5, 3), Coord(5, 4)])
        b = set([Coord(9, 2), Coord(9, 3), Coord(9, 4), Coord(9, 5), Coord(8, 3), Coord(8, 4)])

        # create opening Default Hal is white (max), player is black, white to move first
        self.playerColor = "black"
        self.hal = AI("white")

        self.state = BoardState(w, b) #official current board state of the game
        self.prevstate = self.state #holds state from previous turn
        self.turn = "white" #whose turn it is
        self.lastToMove = "black"

        #initialize gamestate to main menu (not used currently)
        self.gamestate = Gamestate.mainmenu #start at the menu

        # call render once on startup
        self.render = True

        # vrep off by default
        self.vrepON = False

        #initialize views into list
        self.Views = []
        self.Views.append(gameView(self))
        self.Views.append(mainmenuView(self))
        self.currentView = self.Views.pop()#removes and returns view at last index

    def whosTurn(self):
        return self.turn

    def NextTurn(self):
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def getBoard(self):
        return copy.deepcopy(self.state)

    def setBoard(self, state):
        self.state = copy.deepcopy(state)

    #returns gamestate ie main menu, playing, etc.
    def getCurrentGameState(self):
        return self.gamestate

    def popView(self, render=True):
        self.currentView = self.Views.pop()  # removes and returns view at last index
        self.render = True

    #def checkInput(self, ev):
    #    for event in pygame.event.get():
    #        self.currentView.update(ev)
    #    pass

    #master game update function
    def update(self):

        #update current View.
        for event in pygame.event.get():
            # check if we should exit
            if event.type == pygame.QUIT:
                done = True  #
            else:
                #run updates on event list
                self.currentView.update(event)

    def draw(self):
        #draw whatever needs drawing this round (call check input first.
        self.currentView.draw(self.state, self.screen)
        pygame.display.flip()
        self.clock.tick(60)

    def loop(self):
        #main gameloop
        while not self.done:
            #handle all recent input events
            self.update()
            #render all objects when nessisary
            self.draw()

#base class for each gamestate screen. sHas gameView, mainmenuView, and (todo) optionsView child classes
class View(object):

    #colors used
    HALblack = (14, 14, 21) #BG fill color
    Grey = (128, 128, 128) #button color
    """#other predefined colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    Red = (255, 0, 0)
    Green = (0, 128, 0)
    Yellow = (255, 255, 0)
    Lime = (0, 255, 0)
    Maroon = (128, 0, 0)
    NavyBlue = (0, 0, 128)
    Olive = (128, 128, 0)
    Purple = (128, 0, 128)
    Silver = (192, 192, 192)
    Teal = (0, 128, 128)
    White = (255, 255, 255)
    Aqua = (0, 255, 255)
    Blue = (0, 0, 255)
    Fuchsia = (255, 0, 255)
    """

    #common access/storage of image objects in the game
    image_library = {}

    #shared public pygame screen used by Views
    screen = None

    #game object that runs everything
    curgame = None

    def __init__(self, game):
        View.curgame = game
        View.screen = pygame.display.set_mode((1100, 900))
        pass

    # get pygame image object given a path
    def get_image(path):
        image = View.image_library.get(path)
        if image == None:
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path).convert_alpha()
            View.image_library[path] = image
        return image

    # draws the pieces from the current state, the board, and the black background
    def draw(self, state, targetscreen):
        if View.curgame.render:
            targetscreen.fill(self.HALblack)  # load bg color first (all black)

#this is the view for the main menu at the begining of the game. It changes button text mostly.
class mainmenuView(View):

    def __init__(self, game):
        super(mainmenuView, self).__init__(game) #draws black BG on init
        #create buttons
        self.colorButton = Button()
        self.difficultyButton = Button()
        self.startButton = Button()
        self.vrepButton = Button()

        self.diffstr = ["Easy", "Med", "Hard"]
        self.vrepstr = "OFF"

        self.boardSpriteGroup = pygame.sprite.Group()
        self.boardSpriteGroup.add(boardSprite())
        self.boardsprite = boardSprite()

    def draw(self, state, targetscreen):

        # draw parent (#fill screen with black BG)
        super(mainmenuView, self).draw(state, targetscreen)

        if View.curgame.render:

            #print("rendering")
            self.boardsprite.draw(targetscreen, state)  # render board and pieces


            buttoncolor = View.Grey

            #display current buttons and any text if we updated
            self.difficultyButton.draw(targetscreen, buttoncolor, 600, 100, 250, 100, 0, self.setDifficultyButtonText(self.diffstr[View.curgame.difficulty]), (255, 255, 255))
            self.colorButton.draw(targetscreen, buttoncolor, 600, 225, 250, 100, 0, self.setPlayerColorButtonText(View.curgame.playerColor), (255, 255, 255))
            self.vrepButton.draw(targetscreen, buttoncolor, 600, 350, 250, 100, 0, self.setVrepButtonText(self.vrepstr), (255, 255, 255))
            self.startButton.draw(targetscreen, buttoncolor, 600, 550, 250, 100, 0, "Start Game", (255, 255, 255))
            View.curgame.render = False

    def setDifficultyButtonText(self, text):
        return "MODE: " + text
    def setVrepButtonText(self, text):
        return "VREP: " + text
    def setPlayerColorButtonText(self, text):
        return "PLAYER: " + text

    def update(self,event):
        #chack for button presses, change button text accordingly

        # update based on button presses
        if event.type == MOUSEBUTTONDOWN:
            if self.colorButton.pressed(pygame.mouse.get_pos()):

                #assign hal's color based on players color (call hal.update(event)?
                if View.curgame.playerColor == "white":
                    View.curgame.hal.color = "white"
                    View.curgame.playerColor = "black"
                elif View.curgame.playerColor == "black":
                    View.curgame.hal.color = "black"
                    View.curgame.playerColor = "white"
                print("Player is playing as " + View.curgame.playerColor)
                View.curgame.render=True
                return

            elif self.difficultyButton.pressed(pygame.mouse.get_pos()):
                #set Difficulty level
                    #if rollover
                if View.curgame.difficulty == Difficulty.Hard:
                    View.curgame.difficulty = Difficulty.Easy
                    View.curgame.hal.difficulty = View.curgame.difficulty
                else:
                    #else incriment
                    View.curgame.difficulty += 1
                    View.curgame.hal.difficulty = View.curgame.difficulty
                print('difficulty cycled to %s' % View.curgame.hal.difficulty)
                View.curgame.render = True
                return

            elif self.vrepButton.pressed(pygame.mouse.get_pos()):
                if View.curgame.vrepON == True:
                    View.curgame.vrepON = False
                    self.vrepstr = "OFF"
                else:
                    View.curgame.vrepON = True
                    self.vrepstr = "ON"
                print('vrep interface is now %s' % self.vrepstr)
                View.curgame.render = True
                return

            elif self.startButton.pressed(pygame.mouse.get_pos()):
                print("starting game")
                View.curgame.popView()
                View.curgame.gamestate = Gamestate.play
                randgreeting = getSound(hal_greeting)
                play_sound(randgreeting)
                #View.curgame.render = True
                return


#this is the view used during the game. It updates the board, displays pieces, etc.
class gameView(View):

    def __init__(self, game):
        #call parent constructor
        super(gameView, self).__init__(game)
        self.nextTurnButton = Button()
        self.halsEye = pygame.sprite.Group()
        self.halsEye.add(HALSprite())
        self.boardsprite = boardSprite()
        self.sqrsprites = sqrSprite()
        self.boardSpriteGroup = pygame.sprite.Group()
        self.boardSpriteGroup.add([boardSprite(),sqrSprite()])

        #self.msgConsole = pygame.sprite.Group(msgConsole())

        self.message = ""


    def draw(self, state, targetscreen):
        # draw parent
        super(gameView, self).draw(state, targetscreen)

        #draw gameboard+pieces if anything has changed
        if View.curgame.render:

            #draw logo
            targetscreen.blit(View.get_image('art/HALlogo.png'), (640, 10))  # Hal9000 topright logo

            #draw board and pieces
            #self.boardSpriteGroup.draw(targetscreen)
            self.boardsprite.draw(targetscreen,View.curgame.state) #render board and pieces
            self.sqrsprites.draw(targetscreen) #render squares if nessisary

            # display text on the screen (working) unhighlight these 2 lines
            font = pygame.font.SysFont("comicsansms", 14)
            if checkWinner(state, "white"):
                self.displayMessage(targetscreen, font, "WHITE WINS", (800, 150))
                hal_says = getSound(hal_wins)
                play_sound(hal_says)
                print("WHITE WINS")

            elif checkWinner(state, "black"):
                self.displayMessage(targetscreen, font, "BLACK WINS", (800, 150))
                hal_says = getSound(hal_loses)
                play_sound(hal_says)
                #message = "BLACK WINS"
                print("BLACK WINS")

            # draw eye
            self.halsEye.draw(targetscreen)

            #draw messages
            # draw message box (todo: make Sprite class)
            # msgConsole.draw()
            font = pygame.font.SysFont("comicsansms", 14)
            self.displayMessage(targetscreen, font, self.message)
            self.displayMessage(targetscreen, font, "Evaluation: " + str(View.curgame.hal.finalval) + " @Depth= " + str(
                View.curgame.hal.finaldepth), (500, 250))
            self.displayMessage(targetscreen, font, "Total Nodes:" + str(View.curgame.hal.totalnodesdisplay),
                                (500, 300))
            self.displayMessage(targetscreen, font, "Max Prunes:" + str(View.curgame.hal.nummaxdisplay), (700, 300))
            self.displayMessage(targetscreen, font, "Min Prunes: " + str(View.curgame.hal.nummindisplay), (900, 300))
            self.displayMessage(targetscreen, font, 'FPS: %d' % View.curgame.clock.get_fps(), (20, 20))

            # draw next turn button
            self.nextTurnButton.draw(targetscreen, View.Grey, 770, 600, 200, 100, 0, "Next Turn", (255, 255, 255))

            View.curgame.render = False




    #check for next turn press, calculate coord of currently clicked tile
    def update(self,event):

        # update whos turn
        if View.curgame.whosTurn() != View.curgame.lastToMove:
            print(View.curgame.whosTurn() + " to move")
            self.message = View.curgame.whosTurn() + " to move"
            View.curgame.lastToMove = View.curgame.whosTurn()
        View.curgame.render = True

        # run AI if its time and cmd vrep arm (if enabled)
        #todo: run in own thread, print update stats as it runs. do vrep and nextturn when thread returns
        if View.curgame.whosTurn() == View.curgame.hal.getColor():
            if View.curgame.hal.difficulty == Difficulty.Easy:
                retEval, newState = View.curgame.hal.IDsearch(View.curgame.state, 3)
            elif View.curgame.hal.difficulty == Difficulty.Medium:
                retEval, newState = View.curgame.hal.IDsearch(View.curgame.state, 5)
            elif View.curgame.hal.difficulty == Difficulty.Hard:
                retEval, newState = self.curgame.hal.IDsearch(View.curgame.state, 10)

            #play HAL sound
            hal_says = None
            if retEval >= 0:
                hal_says = getSound(hal_winning)
            else:
                hal_says = getSound(hal_losing)
            play_sound(hal_says)

            # generate next state and robot arm moves
            if View.curgame.vrepON == True:
                # todo: put into thread pool
                mvlist = getMVlist(View.curgame.state, newState)
                #print("printing moves for state:")
                #printState(newState)
                printMVlist(mvlist)
                robottasks = View.curgame.hal.arm.generateTasksFromMVlist(mvlist)
                View.curgame.hal.arm.executeCMD(robottasks)

            # update board and signal next turn
            print("updating prevstate as:")
            printState(newState)
            View.curgame.prevstate = copy.deepcopy(newState)
            View.curgame.state = copy.deepcopy(newState)#update

            #printState(View.curgame.state)
            View.curgame.NextTurn()
            # else:
            # display "your turn in message"

        #handle next turn button press and vrep arm for users move
        if event.type == MOUSEBUTTONDOWN:

            #player pressed next turn, execute his moves on the board
            if self.nextTurnButton.pressed(pygame.mouse.get_pos()):
                print("Next Turn Pressed!")

                # play HAL sound
                eval = View.curgame.state.getEvaluation()
                hal_says = None
                if eval >= 0:
                    hal_says = getSound(hal_winning)
                else:
                    hal_says = getSound(hal_losing)
                play_sound(hal_says)

                # move robot arm for user (todo: put this in thread)
                if View.curgame.vrepON:
                    print()
                    print("Hal 9000 will move your pieces for you.")
                    print("Don't worry Dave. Hal never makes a mistake.")
                    #print("previous State:")
                    #printState(View.curgame.prevstate)
                    #print("printing moves for state:")
                    #printState(View.curgame.state)
                    mvlist = getMVlist(View.curgame.prevstate, View.curgame.state)
                    printMVlist(mvlist)
                    robottasks = View.curgame.hal.arm.generateTasksFromMVlist(mvlist)
                    View.curgame.hal.arm.executeCMD(robottasks)

                #print("Hal's Turn.")
                #message  = "Hal is thinking..."
                View.curgame.prevstate = copy.deepcopy(View.curgame.state)
                View.curgame.NextTurn()
                return

            #these go in Board Sprite.update(event)
            #self.boardSpriteGroup.update()
            self.sqrsprites.update(event)


    # display message text on the screen
    def displayMessage(self, screen, font, s, loc=(800, 200)):
        Red = (255, 0, 0)
        text = font.render(s, True, Red)
        screen.blit(text, loc)

#returns a pygame image object given a filename of a png
def load_image(name):
    image = pygame.image.load(name)
    return image


# this is the image of hal's red eye on the screen.(animated)
class HALSprite(pygame.sprite.Sprite):
    def __init__(self):
        #call base constructor
        super().__init__()

        #load images
        self.images = []
        self.images.append(load_image('art/HAL1.png'))
        self.images.append(load_image('art/HAL2.png'))

        #initialize image
        self.index = 0
        self.image = self.images[self.index]

        #size/location of image?
        #self.rect = pygame.Rect(620, 200, 500, 500)
        self.rect = self.image.get_rect()
        self.rect.x = 620
        self.rect.y = 200

    #(Animation) toggles between showing image1 and 2 every frame for flicker affect
    def update(self,screen):
        if self.index == 0:
            self.index = 1
        else:
            self.index = 0
        self.image = self.images[self.index]
        screen.blit

class boardSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # background image
        self.boardimage = View.get_image('art/background2.png')
        self.wrookimage = View.get_image('art/wrook.png')
        self.brookimage = View.get_image('art/brook.png')

        #pixel position of top left corner
        self.startx = 0
        self.starty = 0

        #create new rectangle
        self.image = self.boardimage
        self.rect = self.image.get_rect()
        self.rect.x = self.startx
        self.rect.y = self.starty

        self.TILEWIDTH = 45 #pixels

    #draw the board + pieces + selection squares?
    def update(self, event=None):
        print("in brdsprite update " + str(View.curgame.render))


    def draw(self,screen,state):

        #print("Rendering Board+Pieces:")
        #printState(View.curgame.state)
        #render board
        screen.blit(self.boardimage, (self.startx, self.starty))  # draw checkered board alone

        #render pieces
        whitePieces = state.getSortedWhiteList()
        blackPieces = state.getSortedBlackList()
        for coord in whitePieces:
            x = self.startx + coord.j * self.TILEWIDTH
            y = self.startx + coord.i * self.TILEWIDTH
            screen.blit(self.wrookimage, (x, y))
        for coord in blackPieces:
            x = self.startx + coord.j * self.TILEWIDTH
            y = self.starty + coord.i * self.TILEWIDTH
            screen.blit(self.brookimage, (x, y))

#delete later
"""
class rookSprite(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = None
        self.rect = None

        self.x = 0
        self.y = 0
        self.boardstartx = 0
        self.boardstarty = 0

        self.color = "black"

    def update(self):
        pass

    def setPiece(self, coord, color):
        if color == "black":
            self.image = View.get_image('art/brook.png')
        else:
            self.image = View.get_image('art/wrook.png')
        self.x = self.boardstartx + coord.j * 45  # adjust
        self.y = self.boardstarty + coord.i * 45  # adjust
"""

#checkered board + player pieces + colored square selection tiles
class sqrSprite(pygame.sprite.Sprite):
    def __init__(self):
        super(sqrSprite, self).__init__()

        #background image
        self.image = pygame.Surface([10, 10])
        self.rect=self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

        #square highlighting related
        self.sel_x = 0
        self.sel_y = 0
        self.sel_corner1 = [0, 0]
        self.sel_corner2 = [0, 0]
        self.SQR_SEL_STATE1 = False
        self.SQR_SEL_STATE2 = False
        self.prevSelectedCoord = Coord(0, 0)  # save coord of our selection
        self.SQR_SEL_STATE = 0

    def update(self, event=None):
        if event != None:
            self.onClick(event)

    #update squares around tiles when we click on them
    def onClick(self,event):
        # if it was on a tile, calculate variables to use for highlighting squares
        if event.button == 1:
            # get mouse xy pixel location, translate into board coord
            mouse_x, mouse_y = event.pos
            self.sel_x = int(mouse_x / 45)
            self.sel_y = int(mouse_y / 45)
            # calculate where the diagnal pixel locations are for that coord
            self.sel_corner1[0] = self.sel_y * 45
            self.sel_corner1[1] = self.sel_x * 45
            self.sel_corner2[0] = self.sel_corner1[0] + 45
            self.sel_corner2[1] = self.sel_corner1[1] + 45

            #figure out what to do based on square selection state
            if (mouse_x >= self.sel_corner1[1]) and (mouse_x <= self.sel_corner2[1]) and (
                mouse_y >= self.sel_corner1[0]) and (mouse_y <= self.sel_corner2[0]):
                if inBounds(Coord(self.sel_y, self.sel_x)):
                    if self.SQR_SEL_STATE == 2:
                        #execute move here?
                        #reset select state machine
                        self.SQR_SEL_STATE = 0
                    else:
                        self.SQR_SEL_STATE += 1
                    View.curgame.render = True

        # if deselection
        if event.button == 3:
            mouse_x, mouse_y = event.pos
            self.sel_x = int(mouse_x / 45)
            self.sel_y = int(mouse_y / 45)
            #print("x: " + str(self.sel_x) + ", y: " + str(self.sel_y))

            self.sel_corner1[0] = self.sel_y * 45
            self.sel_corner1[1] = self.sel_x * 45
            self.sel_corner2[0] = self.sel_corner1[0] + 45
            self.sel_corner2[1] = self.sel_corner1[1] + 45
            if (mouse_x >= self.sel_corner1[1]) and (mouse_x <= self.sel_corner2[1]) and (
                mouse_y >= self.sel_corner1[0]) and (mouse_y <= self.sel_corner2[0]):
                # print ("button deselected")
                if inBounds(Coord(self.sel_y, self.sel_x)):
                    self.SQR_SEL_STATE = 0
                    View.curgame.render = True

    #draw squares as nessesary
    def draw(self,screen):

        #HANDLE INPUT STATES todo: handle all input checks in a for loop
        if View.curgame.whosTurn() == View.curgame.playerColor:

            # currently selected position highlighted by the mouse
            curSelectedCoord = Coord(self.sel_y, self.sel_x)

            #state1 case: (highlight squares)
            if self.SQR_SEL_STATE == 1:

                # highlight the current selected square in blue
                print("drawing blue square")
                screen.blit(View.get_image('art/bluesquare.png'), (self.sel_corner1[1], self.sel_corner1[0]))

                # get list of potential destination/moves to highlight for this piece
                destinations = getMoveListForPiece(View.curgame.state, curSelectedCoord)
                # print(len(destinations))

                # also render different colored squares for the destinations and capturable pieces surrounding the tile
                for mv, newState, params in destinations:
                    if mv == jump:
                        # highlight threats in red squares, destinations in green
                        screen.blit(View.get_image('art/redsquare.png'), (params[2].j * 45, params[2].i * 45))
                        if inBounds(params[3]):
                            screen.blit(View.get_image('art/greensquare.png'), (params[3].j * 45, params[3].i * 45))
                    # highlight plain moves and canters in green
                    elif mv == cantor:
                        if inBounds(params[3]):
                            screen.blit(View.get_image('art/greensquare.png'), (params[3].j * 45, params[3].i * 45))
                    elif mv == plainMove:
                        if inBounds(params[2]):
                            screen.blit(View.get_image('art/greensquare.png'), (params[2].j * 45, params[2].i * 45))

            # State2 case: (execute move) #move to update?
            if self.SQR_SEL_STATE == 2:

                # grab all available moves from selected postion
                f = getMoveListForPiece(View.curgame.state, self.prevSelectedCoord)

                # search for move matching selected state, execute that move.
                for mv, selectedstate, params in f:  # move, nextstate, parameters note: function call would be like a(*c)
                    if (mv == jump or mv == cantor):
                        if params[3].i == curSelectedCoord.i and params[3].j == curSelectedCoord.j:
                            # NOTE: param 3 stores jump/cantor dest tile but param 2 stores plain move dest tile

                            #save cur state as last.
                            self.prevstate = copy.deepcopy(View.curgame.state)
                            View.curgame.state = selectedstate #deep copy this?

                            # reset square selection states
                            self.SQR_SEL_STATE = 0

                    elif mv == plainMove:
                        if params[2].i == curSelectedCoord.i and params[2].j == curSelectedCoord.j:
                            # Save move
                            self.prevstate = copy.deepcopy(View.curgame.state)
                            View.curgame.state = selectedstate

                            # reset square selection states
                            self.SQR_SEL_STATE = 0

            # save our current position for use in the next loop
            self.prevSelectedCoord = curSelectedCoord


#messages window
class consoleSprite(pygame.sprite.Sprite):

    def __init__(self):
        super(consoleSprite, self).__init__()
        self.msglist = ["", "", "", "", "", "", ""]
        self.font = pygame.font.SysFont("comicsansms", 14)

    # display all messages on the screen
    def draw(self, screen, loc=(500, 500)):
        # blit all messages
        x = loc[0]
        y = loc[1] - 20
        for message in self.msglist:
            lnpos = (x, y)
            y += 20
            Red = (255, 0, 0)
            text = self.font.render(message, True, Red)
            screen.blit(text, lnpos)

    #adds a message to be displayed (along with the time)
    def printmsg(self, text):
        # add msg to queue, delete oldest
        msg = strftime("[%H:%M:%S] ", gmtime())
        msg+= text
        self.msglist.insert(0, msg)
        del self.msglist[len(self.msglist) - 1]
