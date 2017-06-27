
__author__ = 'EpicZero'
import copy

# coord class to refer to squares on the screen.
class Coord(object):
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __hash__(self):
        return hash((self.i, self.j))

    def __eq__(self, other):
        if isinstance(other, Coord):
            return (self.i == other.i) and (self.j == other.j)

    def __lt__(self, other):
        if isinstance(other, Coord):
            if (self.i == other.i):
                return (self.j < other.j)
            return (self.i < self.j)


# A BoardState object at a fundamental level, is a list of coordinates of white and black pieces on a board.
# It represents a single "position" or "game state" after 0 (or many) turn iterations.
class BoardState(object):
    #defensive square matrix (not currently implimented)
    owngoal = [0, 0, 4, 3, 0, 0]
    wall = [0, 0, 3, 2, 6, 0]
    friendly = [4, 3, 2, 1, 2, 5, 6]
    blank = [3, 2, 2, 1, 0, 6]
    enemy = [0, 6, 5, 0, 1, 0]
    goal = [0, 0, 6, 6, 0, 0]
    defPtMatrix = []



    def __init__(self, white = ([]),black= ([])):
        self.white = white
        self.black = black

        BoardState.defPtMatrix.append(BoardState.owngoal)
        BoardState.defPtMatrix.append(BoardState.wall)
        BoardState.defPtMatrix.append(BoardState.friendly)
        BoardState.defPtMatrix.append(BoardState.blank)
        BoardState.defPtMatrix.append(BoardState.enemy)
        BoardState.defPtMatrix.append(BoardState.goal)


    def __hash__(self):
        return hash((tuple(self.getSortedWhiteList()), tuple(self.getSortedBlackList())))

    def remove(self,coord,color):
        if color == "white":
            self.white.remove(coord)
            return
        elif color == "black":
            self.black.remove(coord)
            return

    def addWhite(self, coord):
        self.white.add(coord)
    def addBlack(self, coord):
        self.black.add(coord)

    def removeWhite(self, coord):
        self.white.remove(coord)
    def removeBlack(self, coord):
        self.black.remove(coord)

    def isBlack(self,coord):
        return coord in self.black
    def isWhite(self,coord):
        return coord in self.white

    def inBounds(self, coord):
        ob = set([Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 0), Coord(1, 2), Coord(2, 0),
                  Coord(0, 5), Coord(0, 6), Coord(0, 7), Coord(1, 6), Coord(1, 7), Coord(2, 7),
                  Coord(11, 0), Coord(12, 0), Coord(12, 1), Coord(13, 0), Coord(13, 1), Coord(13, 2),
                  Coord(11, 7), Coord(12, 6), Coord(12, 7), Coord(13, 5), Coord(13, 6), Coord(13, 7)])
        if coord.i > 13 or coord.j > 7 or coord.i < 0 or coord.j < 0 or coord in ob:  # here
            return False
        else:
            return True

    def isEmpty(self,state, coord):
        # if inbounds and is = to empty or is goal
        # if inbounds and (not in black and not in white) or is the goal.
        if self.inBounds(coord) and not (self.isBlack(coord) or self.isWhite(coord)) or self.isGoal(coord):
            return True
        else:
            return False

    def isGoal(self, coord):
        goals = ([Coord(0, 3), Coord(0, 4), Coord(13, 3), Coord(13, 4)])
        if coord in goals:
            return True
        else:
            return False

    #check if black wins
    def winConditionBlack(self):
        # note that blacks goal tiles are at at bottom of the screen
        c1 = Coord(0, 3)
        c2 = Coord(0, 4)
        OpponantsPieceCount = self.getPieceCount("white")

        return self.isBlack(c1) or self.isBlack(c2) or OpponantsPieceCount == 0

    #check if white wins
    def winConditionWhite(self):
        c1 = Coord(13, 3)
        c2 = Coord(13, 4)
        OpponantsPieceCount = self.getPieceCount("black")

        # if white has won
        return self.isWhite(c1) or self.isWhite(c2) or OpponantsPieceCount == 0


    def hasCoord(self,coord,color):
        if color == "white":
            return coord in self.white
        elif color == "black":
            return coord in self.black

    def getSortedWhiteList(self):
        return sorted(list(self.white))
        #return sorted(list(self.white))
    def getSortedBlackList(self):
        return sorted(list(self.black))
        #return sorted(list(self.black))

    def getPieceCount(self,color):
        if color == "white":
            return len(self.white)
        elif color == "black":
            return len(self.black)

    def isEqual(self,state):
        return (self.getSortedWhiteList() == state.getSortedWhiteList()) and (self.getSortedBlackList() == state.getSortedBlackList())
        #return (self.getWhite() == State.getWhite()) and (self.getBlack() == State.getBlack())
    def draw(self):
        pass

    # run/rerun evaluation function on self ( white > black), tracks score

    def getDefPtOnSquare(self, source, target, owncolor):
        OWNGOAL = 0
        WALL = 1
        FRIENDLY = 2
        BLANK = 3
        ENEMY = 4
        GOAL = 5

        # get direction to look for tile
        di = -(target.i - source.i)
        dj = -(target.j - source.j)

        # get opposite adjacent piece
        opposite = Coord(target.i + di, target.j + dj)

        #start above and circle around
        if owncolor == "white":
            owngoal = [Coord(0, 3), Coord(0, 4)]
            goal = [Coord(13, 3), Coord(13, 4)]
            w = FRIENDLY
            b = ENEMY
        else:
            owngoal = [Coord(13, 3), Coord(13, 4)]
            goal = [Coord(0, 3), Coord(0, 4)]
            b = FRIENDLY
            w = ENEMY

        index = [0,1]
        i = 0
        for x in [target,opposite]:
            if x in owngoal:
                index[i] = OWNGOAL
            elif not self.inBounds(x):
                index[i] = WALL
            elif self.isWhite(x):
                index[i] = w
            elif self.isEmpty(self, target):
                index[i] = BLANK
            elif self.isBlack(x):
                index[i] = b
            elif target in goal:
                index[i] = GOAL
        return BoardState.defPtMatrix[index[0]][index[1]]

    def sumDefPtOnPiece(self, coord, clr):

        neighbors = [Coord(coord.i-1,coord.j),
                     Coord(coord.i-1,coord.j + 1),
                     Coord(coord.i, coord.j + 1),
                     Coord(coord.i+1, coord.j + 1)
                     ]

        for x in neighbors:
            sum = self.getDefPtOnSquare(coord, x, clr)

        return sum
    def sumDefPtsOnColor(self, clr):
        sum = 0
        if clr == "white" :
            mylist = self.getSortedWhiteList()
        else:
            mylist = self.getSortedBlackList()

        for x in mylist:
            sum += self.sumDefPtOnPiece(x,clr)
        return sum

    def getEvaluation(self):
        # calc difference in piece count
        numWhitePieces = self.getPieceCount("white")
        numBlackPieces = self.getPieceCount("black")
        pieceCount = numWhitePieces - numBlackPieces

        wClosestPiece = 14  # start at max
        wCloseness = 0  # sum of how close all pieces are for white
        bClosestPiece = 14
        bCloseness = 0

        ClosestPiecepts = 0
        CloserSidepts = 0
        goalPoints = 0

        defensiveBonus = 0

        # winning states are a big deal
        if self.winConditionWhite():
            goalPoints = 1
        elif self.winConditionBlack():
            goalPoints = -1
        else:
            # whitetargetgoalnodes = 13,3 and 13,4

            # get best pieces manhatten distance of each side, then subtract them to get whose pieces is closer to goal
            #not used currently
            # for white
            for coord in self.getSortedWhiteList():
                #i is the y axis, j is the x
                ydist = 13 - coord.i
                xdist = min(abs(3 - coord.j), abs(4 - coord.j))

                moves2goal = max(ydist, xdist) #changed from x+y

                wCloseness += moves2goal
                wClosestPiece = min(moves2goal, wClosestPiece)

            # for black
            for coord in self.getSortedBlackList():
                # i is the y axis, j is the x
                ydist = coord.i
                xdist = min(abs(3 - coord.j), abs(4 - coord.j))

                moves2goal = max(ydist, xdist)  # changed from x+y

                bCloseness += moves2goal
                bClosestPiece = min(moves2goal, bClosestPiece)

            #side w/ closest piece to goal gets aggression points (smaller best variable = closest)
            ClosestPiecepts = (1/wClosestPiece) - (1/bClosestPiece)

            #side with avg num pieces generally closer to goal gets bonus(neg because smaller the better
            avgWhiteCloseness = wCloseness/numWhitePieces
            avgBlackCloseness = bCloseness/numBlackPieces
            CloserSidepts = -(avgWhiteCloseness - avgBlackCloseness)

            #calculate defensive point bonus (more def points awarded when losing badly)
            defpoints = self.sumDefPtsOnColor("white") - self.sumDefPtsOnColor("black")


        # ****SATIC EVALUATION FUNCTION***
        evaluation = 10000*goalPoints +1000*pieceCount + 9000*ClosestPiecepts + 10*CloserSidepts # + (defpoints* (-pieceCount))
        #************************************

        #self.evaluation = evaluation

        return evaluation

    def update(self):
        return self.getEvaluation()

    def __eq__(self, other):
        return self.isEqual(other)

# ascii print the board to the commandline for debugging.
def printBoard(board):
    for i, row in enumerate(board):
        # using enumerate we get an integer index
        # for each row which we can use to calculate y
        # because rows run down the screen, they correspond to the y axis
        # and the columns correspond to the x axis
        x = ''
        for j, piece in enumerate(row):
            if piece == '':
                x = x + ' '
            else:
                x = x + piece

        # print(x)
        print(i, ' '.join(x))
        # for j,  piece in enumerate(row):
        # print piece, ' '.join(piece)


# prints the state to the screen for debugging. calls printBoard and statetobrd converter for now
def printState(state):
    printBoard(statetoascii(state))

# returns string of what piece is at this position. (row,col) used for debug
def checkPosition(state, coord):
    # check for valid position
    if not inBounds(coord) or isEmpty(state, coord):
        print("position empty or out of bounds")
        return

    # determine the color and piece type
    if state.isBlack(coord):
        print("black rook")
        return
    elif state.isWhite(coord):
        print("white rook")
        return
    if isGoal(coord):
        print(" is Goal")
        return

# returns a bool of whether a particular coord is jumpable. source is current tile. target is the tile to jump over
def canJump(state, source, target):
    if not inBounds(target) or isEmpty(state, target) or isEmpty(state, source):
        return False

    # get direction to jump
    di = target.i - source.i
    dj = target.j - source.j

    # check if distance is too far
    if abs(di) > 1 or abs(dj) > 1:
        print("di/dj > 1 distance failure at target " + str(target.i) + ", " + str(target.j))
        return False

    # get tile on the far side of the jump
    dest = Coord(target.i + di, target.j + dj)

    # if landing spot is empty and not same color then we know we can jump
    if inBounds(target) and isEmpty(state, dest) and not (sameColor(state, source, target)):
        return True
    else:
        return False

# returns whether piece at source tile can jump over a piece at target tile.
def canCantor(state, source, target):
    if not inBounds(target) or isEmpty(state, target) or isEmpty(state, source):
        return False

    # get direction to jump
    di = target.i - source.i  # 5,1 - 5,3 = 0 -2
    dj = target.j - source.j

    if abs(di) > 1 or abs(dj) > 1:
        return False

    # get tile on the far side of the jump
    dest = Coord(target.i + di, target.j + dj)

    # if landing spot is empty same color we know we can jump
    if inBounds(target) and isEmpty(state, dest) and (isWhite(state, source) == isWhite(state, target)):
        # return function to jump?
        #
        return True
    else:
        return False

# checks whether a plain move is possible from the source tile to the destination tile
def canPlain(state, source, destination):
    # error checking
    if isEmpty(state, source):
        return False

    # calculate distance between source and dest tiles
    di = destination.i - source.i
    dj = destination.j - source.j

    # if inbounds and adjacent and dest is
    if inBounds(destination) and abs(di) <= 1 and abs(dj) <= 1 and isEmpty(state, destination):
        return True
    else:
        return False

# checks if a coordinate on the board is empty
def isEmpty(state, coord):
    # if inbounds and is = to empty or is goal
    # if inbounds and (not in black and not in white) or is the goal.
    if inBounds(coord) and not (isBlack(state, coord) or isWhite(state, coord)) or isGoal(coord):
        return True
    else:
        return False

# checks if the coordinate is inboinds
def inBounds(coord):
    ob = set([Coord(0, 0), Coord(0, 1), Coord(0, 2), Coord(1, 0), Coord(1, 2), Coord(2, 0),
              Coord(0, 5), Coord(0, 6), Coord(0, 7), Coord(1, 6), Coord(1, 7), Coord(2, 7),
              Coord(11, 0), Coord(12, 0), Coord(12, 1), Coord(13, 0), Coord(13, 1), Coord(13, 2),
              Coord(11, 7), Coord(12, 6), Coord(12, 7), Coord(13, 5), Coord(13, 6), Coord(13, 7)])
    if coord.i > 13 or coord.j > 7 or coord.i < 0 or coord.j < 0 or coord in ob:  # here
        return False
    else:
        return True

# checks if the piece at a particular coordinate is black
def isBlack(state, coord):
    return state.isBlack(coord)

# checks if a piece at a coordinate is white
def isWhite(state, coord):
    return state.isWhite(coord)

# checks if the coordinate is a goal for any side. (not specific)
def isGoal(coord):
    goals = ([Coord(0, 3), Coord(0, 4), Coord(13, 3), Coord(13, 4)])
    if coord in goals:
        return True
    else:
        return False

# checks if pieces on 2 tiles are the same color.
def sameColor(state, source, target):
    return (isWhite(state, source) == isWhite(state, target)) \
           or (isBlack(state, source) == isBlack(state, target))

# checks if two coords are the same
def isEqual(source, target):
    return source == target

def copybyval(x):
    return copy.deepcopy(x)

# takes a state, and returns an ascii matrix of whats on each tile
def statetoascii(state):
    b = []
    # create rows for initial board

    bgoal = "x x x g g x x x"
    wgoal = "x x x G G x x x"
    blank = ' ' * 7
    firstrow = 'x ' + ' ' * 6 + 'x'
    secondrow = 'x x ' + ' ' * 4 + 'x x'

    # assemble the starting board
    b.append(wgoal.split(' '))
    b.append(secondrow.split(' '))
    b.append(firstrow.split(' '))

    # for i in range(2):
    b.append(blank.split(' '))

    # top two rows for white
    for i in range(2):
        b.append(blank.split(' '))

    for i in range(2):
        b.append(blank.split(' '))

    # bottom two rows for black
    for i in range(2):
        b.append(blank.split(' '))

    # for i in range(2):
    b.append(blank.split(' '))

    b.append(firstrow.split(' '))
    b.append(secondrow.split(' '))
    b.append(bgoal.split(' '))

    # place white pieces
    for coord in state.getSortedWhiteList():
        b[coord.i][coord.j] = "R"

    # place black pieces
    for coord in state.getSortedBlackList():
        b[coord.i][coord.j] = "r"

    # printBoard(b)
    return b

###private Utility functions that are called by jump,cantor, and plainmove functions. These do not update the state eval.
# generic move a piece on the board function.
def move(state, source, destination):
    """ check for errors first"""

    if not inBounds(source) or not inBounds(destination):
        return

    if isEqual(source, destination) or isEmpty(state, source):
        return

    if state.isBlack(source):
        # remove source coord from black
        state.removeBlack(source)

        # place destination in black
        state.addBlack(destination)

    elif state.isWhite(source):

        # remove source coord from white
        state.removeWhite(source)

        # place destination in white
        state.addWhite(destination)

# remove a piece from the board. add to players captured list.
def remove(state, target):
    # check for errors

    if state.isBlack(target):
        state.removeBlack(target)
    elif state.isWhite(target):
        state.removeWhite(target)

###GAME MOVES WHICH CALL STATES UPDATE / evaluation function when completed
# jump move for capturing pieces (calls update)
def jump(state, source, target, destination):
    if canJump(state, source, target):
        # leap first
        move(state, source, destination)

        # remove opponant's piece
        remove(state, target)

        # update evaluation
        state.update()
        # for dubug
        # printBoard(board)

# cantor move for knights (calls update)
def cantor(state, source, target, destination):
    # jump to destination
    if canCantor(state, source, target):
        move(state, source, destination)
        state.update()

# plain move for rooks and knights. (calls update)
def plainMove(state, source, destination):
    # execute a plain move
    if canPlain(state, source, destination):
        move(state, source, destination)
        # update evaluation
        state.update()

# returns a list of valid moves available at a Coord; in the form (move, parameters, destination coord)
def getMoveListForPiece(state, source):
    """returns list of [(function(), (*parameters), destination)] for a particular piece/coordinate"""
    movelist = []  # entry[(function, (parameters), destination)]
    jumplist = []

    directions = [Coord(source.i - 1, source.j - 1), Coord(source.i, source.j - 1),
                  Coord(source.i + 1, source.j - 1), Coord(source.i + 1, source.j),
                  Coord(source.i + 1, source.j + 1), Coord(source.i, source.j + 1),
                  Coord(source.i - 1, source.j + 1), Coord(source.i - 1, source.j)]

    """ directions are starting upperleft going counter clockwise around the tile"""

    # process moves in all directions
    for target in directions:

        if canJump(state, source, target):

            # calculate the destination tile on the far side of the jump
            di = target.i - source.i
            dj = target.j - source.j
            dest = Coord(target.i + di, target.j + dj)

            # apply move to a COPY of current state
            statecpy = copybyval(state)
            jump(statecpy, source, target, dest)

            # if we jump we must clear the entire move list and make it the only move in the list.
            # #(rules of camelot say we are forced to capture)
            # check for other jumpsfirst do not remove those

            jumplist.append((jump, statecpy, (statecpy, source, target, dest)))
            continue

            # to access destination use mylist[0][2] -> gives dest coordinate
            # to access parameters for the function
            # mylist[0][0](*mylist[0][1]) executes the function

        elif len(jumplist) == 0:
            if canCantor(state, source, target):
                # get tile on the far side of the jump
                di = target.i - source.i
                dj = target.j - source.j
                dest = Coord(target.i + di, target.j + dj)
                # print "it thinks we can cantor from (" + str(source.i) + ", " + str(source.j) + ") to ("+ str(dest.i) + ", " + str(dest.j) + ")."

                # perform move on a copy of the state
                statecpy = copybyval(state)
                cantor(statecpy, source, target, dest)

                # append function into move list
                movelist.append((cantor, statecpy, (statecpy, source, target, dest)))
                continue

            if canPlain(state, source, target):
                # print "it thinks we can plainmove from (" + str(source.i) + ", " + str(source.j) + ") to ("+ str(target.i) + ", " + str(target.j) + ")."

                # apply move to a copy of the state
                statecpy = copybyval(state)
                plainMove(statecpy, source, target)

                # append move to our list
                movelist.append((plainMove, statecpy, (statecpy, source, target)))
                continue
    if len(jumplist) > 0:
        return jumplist
    # else
    return movelist

# returns a bool of whether a particular color has reached the goal (won)
def checkWinner(state, color):
    # note that blacks goal tiles are at at bottom of the screen
    if color == "black":
        return state.winConditionBlack()

    elif color == "white":
        return state.winConditionWhite()

    print("bad goal test color: " + color)
    return False

# inverse search to return a list of descriptions of physical moves which describe the "absolute" difference in two
# succesive states. It is meant to mimic the real-life physical movements/instructions a human would need to make to a
# real life board state to generate the "next" or new state/turn. The "move" is represented intrinsicly by the
# difference between two succesive states).
def getMVlist(oldstate, newstate):

    wtaken = False
    btaken = False
    changes = False
    mvlist = []
    movestr = "Move "
    takenstr = "Take "
    movetype = "MOVE"
    color = "white"
    old = None
    new = None

    oldWlist = oldstate.getSortedWhiteList()
    newWlist = newstate.getSortedWhiteList()

    if len(oldWlist) != len(newWlist):
        wtaken = True

    # check for taken or new moves.
    for coord in oldWlist:
        if coord not in newWlist:
            changes = True
            old = coord
            if wtaken:
                # this piece was taken
                movetype = "TAKE"
                break
            else:
                # was a move, find the new coord in the list, this is where white moved
                movetype = "MOVE"
                for c in newWlist:
                    if c not in oldWlist:
                        # found the move
                        new = c

    # add that move (if any) to our list
    if changes == True:
        mvlist.append([movetype, old, new, color])

    # search black coords for changes
    movetype = "MOVE"
    color = "black"
    changes = False

    oldBlist = oldstate.getSortedBlackList()
    newBlist = newstate.getSortedBlackList()

    if len(oldBlist) != len(newBlist):  # todo check whether this checks size vs contents
        btaken = True  # flag piece for removal

    # check for taken or new moves.
    for coord in oldBlist:
        if coord not in newBlist:
            old = coord
            changes = True
            if btaken:
                # mark piece taken
                movetype = "TAKE"
            else:
                # this was a move, find new coord
                movetype = "MOVE"
                for c in newBlist:
                    if c not in oldBlist:
                        # found the move
                        new = c
    if changes == True:
        mvlist.append([movetype, old, new, color])

    # sort moves before returning as move description first, taken notification second (if any taken)
    mvlist.sort(key=lambda x: x[0])

    # return vals: [movetype, oldcoord, newcoord('None' for TAKE moves), color]
    return mvlist  # [[movetype, old, new, color]]

"print moves to the screen"

def printMVlist(mvlist):
    mystring = ""
    prevtask = None
    print()
    print("Most recent move:")
    for mv in mvlist:
        prevtask = mv
        color = mv[3]
        if mv[0] == "MOVE":
            if color == "white":
                mystring += 'W('
            elif color == "black":
                mystring += 'B('
            mystring += str(mv[1].i) + "," + str(mv[1].j)
            # get direction to jump
            di = mv[2].i - mv[1].i
            dj = mv[2].j - mv[1].j
            if (di == 2 or dj == 2):
                if prevtask != None:
                    mystring += ')x('  # jump took place
                else:
                    mystring += ')j('  # cantor took place
            # else regular move
            else:
                mystring += ')-('
            mystring += str(mv[2].i) + "," + str(mv[2].j) + ")"

        elif mv[0] == "TAKE":
            opponant = "White"
            pref = "B("
            if color == "white":
                opponant = "Black"
                pref = "W("
            mystring += "  |--" + opponant + " takes " + pref + str(mv[1].i) + "," + str(mv[1].j) + ")"

        print(mystring)


#for testing




'''
from Model import *
w = ([Coord(4,2),Coord(4,3),Coord(4,4),Coord(4,5),Coord(5,3),Coord(5,4)])
b = ([Coord(9,2),Coord(9,3),Coord(9,4),Coord(9,5),Coord(8,3),Coord(8,4)])
opening = BoardState(w,b)

statetobrd(opening)
'''