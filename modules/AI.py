# AI class for hal. contains all of the AI methods hal uses.
import copy
import time
import threading
import roboarm
from board import getMoveListForPiece, jump, printState

#import Game

inf = float('infinity')


class AI(object):
    def __init__(self, color="white", difficulty=2):

        #controls the time HAL spends searching
        self.timeout = 45.0

        #stats related

        #self.nodesgenerated = 0
        self.nummaxdisplay = 0
        self.nummindisplay = 0
        self.totalnodesdisplay = 0

        self.finalval = 0
        self.finaldepth = 0

        self.color = color
        self.TT = {}
        self.difficulty = difficulty

        #may not need these
        self.IDalpha = -float('infinity')
        self.IDbeta = float('infinity')

        #initializes HALS vrep link and RRRRRR manipulator
        self.arm = roboarm.RobotArm()

        # create map of tile values
        self.TileDefensiveValueMap = []
        # rows for value map
        goalw = "x x x 0 0 x x x"
        rowa = "x x 6 5 5 6 x x"
        rowb = "x 6 5 4 4 5 6 x"
        rowc = "6 5 4 3 3 4 5 6"
        rowd = "5 4 3 2 2 3 4 5"
        rowe = "4 3 2 1 1 2 3 4"
        rowf = "3 2 1 0 0 1 2 3"

        rowg = "3 2 1 0 0 1 2 3"
        rowh = "4 3 2 1 1 2 3 4"
        rowi = "5 4 3 2 2 3 4 5"
        rowj = "6 5 4 3 3 4 5 6"
        rowk = "x 6 5 4 4 5 6 x"
        rowl = "x x 6 5 5 6 x x"
        goalb = "x x x 0 0 x x x"

        # create the map of valued tiles
        self.TileDefensiveValueMap.append(goalw.split())
        self.TileDefensiveValueMap.append(rowa.split())
        self.TileDefensiveValueMap.append(rowb.split())
        self.TileDefensiveValueMap.append(rowc.split())
        self.TileDefensiveValueMap.append(rowd.split())
        self.TileDefensiveValueMap.append(rowe.split())
        self.TileDefensiveValueMap.append(rowf.split())
        self.TileDefensiveValueMap.append(rowf.split())
        self.TileDefensiveValueMap.append(rowe.split())
        self.TileDefensiveValueMap.append(rowd.split())
        self.TileDefensiveValueMap.append(rowc.split())
        self.TileDefensiveValueMap.append(rowb.split())
        self.TileDefensiveValueMap.append(rowa.split())
        self.TileDefensiveValueMap.append(goalb.split())

    # returns hal's color
    def getColor(self):
        return self.color

    # evaluation function ( white > black)
    def evaluateState(self, state):
        return state.getEvaluation()

    #main alphabeta pruning workhorse function run over and over by the AI in IDSEARCH up to a certain depth. Calls evaluate a lot.
    def alphabetasearch(self, state, a, b, depthlimit=10, AIcolor=None, t=time.clock()):

        if AIcolor == None:
            AIcolor = self.getColor()


        self.abNumMaxNodes = 1
        self.abNumMinNodes = 0
        self.abTotalNodesGend = 0
        self.abnodesevaluated = 0
        self.abTotalminnodesPrunedbyMax = 0
        self.abTotalMaxnodesPrunedbyMin = 0
        self.abMinPrunings = 0
        self.abMaxPrunings = 0
        self.abNumTimeoutEvals = 0

        self.maxDepthReached = 0
        self.startingdepth = 0
        self.blackwinsfound = 0
        self.whitewinsfound = 0

        self.nodesaftertimeout = 0

        self.abAlpha = a
        self.abBeta = b

        # for next iteration
        if AIcolor == "white":
            playercolor = "black"
        else:
            playercolor = "white"

        origstatecpy = copy.deepcopy(state)  # save the current board. Work on a copy.

        # function to tests whether to end the current alphabeta search
        def cutofftest(self, state, curdepth, dl):
            #secs = tm - start
            #if secs > self.timeout: #if timeout condition
            #    self.nodesaftertimeout = self.nodesaftertimeout + 1
            #    return True
            if self.IDcutoff:
                self.abNumTimeoutEvals += 1
                return True
            if state.winConditionBlack():
                self.blackwinsfound = self.blackwinsfound + 1
                return True
            if state.winConditionWhite():
                self.whitewinsfound = self.whitewinsfound + 1
                return True
            if curdepth >= dl:
                self.maxDepthReached = curdepth
                return True
            return False

        #  max function, given minnode returns the best value for white (largest evaluation values)
        def abMax(maxnode, depth, alpha, beta):
            #print("abmax @d=" + str(depth))
            # track depth reached
            if depth > self.maxDepthReached:
                self.maxDepthReached = depth
                print("Max@D=" + str(depth))

            # before doing anything check our lookup table for this state (TTlookup eturns eval, depth, flag)
            # and return immediately with a value (first arg) if we've computed this state before
            #TTeval = TTlookup(minstate, depth)
            #if TTeval != None:
            #     return TTeval[0]

            # if cutoff , store and return evaluation of this state (we are a leaf node)
            if cutofftest(self, maxnode, depth, depthlimit):
                retvalue = maxnode.getEvaluation()
                self.abnodesevaluated += 1
                #TTstore(minstate, depth, self.alpha, self.beta, retvalue)
                return retvalue

            #generate child states for white/MaxNode
            childrenstates = self.generateChildStates(maxnode, "white") #self.generateChildStates(givenstate, AIcolor)

            numchildren = len(childrenstates)
            self.abNumMinNodes += numchildren
            self.abTotalNodesGend += numchildren

            index = 1
            v = -float('infinity') #initialize alpha for new node
            for minnode in childrenstates:

                # v is the evaluation returned from minnode child. (pass in alpha and beta)
                v = max(v, abMin(minnode, depth + 1,alpha,beta)) # v is max (curr alpha, children)

                #update alpha if v is new best max has seen so far at this depth
                alpha = max(alpha, v)

                #prune/return alpha if best max eval so far is better than passed in beta
                if alpha >= beta:
                    numprunes = numchildren - index
                    self.abTotalminnodesPrunedbyMax += numprunes
                    self.abMaxPrunings += 1
                    return alpha
                else:
                    index += 1

            #TTstore(minstate, depth, self.alpha, self.beta, v)
            #return evaluation
            return v

        #generates maxnodes and return best/min eval
        def abMin(minnode, depth, alpha, beta):

            if depth > self.maxDepthReached:
                self.maxDepthReached = depth
                print("Min@D=" + str(depth))

            ##TT is a transposition table. TT stores return value, current depth, alpha, and beta.
            # TT is only updated within minfunction and only for exact scores (goal,depthlimit,timeout,etc)
            # or beta cutoffs (refutation moves).
            # The TT should still exist between iterative deepenings
            # TT should also only update if depth greater than or equal to (or only == for debug) current depth of this node.
            # TTeval = TTlookup(maxstate, depth)
            #if TTeval != None:
            #    return TTeval[0]  # return immediately with the value, we've seen this before (update alpha and beta?)

            # cutoff test (checks against depth limit, win condition, and timeout)
            if cutofftest(self, minnode, depth, depthlimit):
                retvalue = minnode.getEvaluation()
                self.abnodesevaluated += 1
                #TTstore(maxstate, depth, self.alpha, self.beta, retvalue)
                return retvalue

            #generate children
            childrenstates = self.generateChildStates(minnode, "black")

            #track nodes generated
            numchildren = len(childrenstates)
            self.abNumMaxNodes += numchildren
            self.abTotalNodesGend += numchildren

            index = 1
            v = float('infinity')
            for maxNode in childrenstates:

                #v is child maxnode's return evaluation
                v = min(v, abMax(maxNode, depth + 1, alpha, beta))

                #update beta if best so far for min
                beta = min(beta, v)

                #prune/return best for min if our parent node's best seen so far is greater than our best evaluation so far
                if alpha >= beta:
                    numprunes = numchildren - index
                    self.abTotalMaxnodesPrunedbyMin += numprunes #plus remaining nodes
                    self.abMinPrunings += 1
                    #TTstore(maxstate, depth, self.alpha, self.beta, v)
                    return beta
                else:
                    index += 1

            #TTstore(maxstate, depth, self.alpha, self.beta, v)
            return v

        #main call @D=0 that generates children(minnodes) and returns the max eval + state found
        def abSearchMax(children, a,b):

            curalpha = a
            numchildren = len(children)
            bestState = children[0]

            #run min on hals children. return nbode with eval
            v = -float('infinity')  # initialize alpha for new node
            for minNode in children:
                curMinNode = copy.deepcopy(minNode)
                v = max(v, abMin(curMinNode, self.startingdepth + 1, curalpha, b))  # v is max (curr alpha, children)

                #update curalpha if new best
                if(v > curalpha):
                    #print("\nnewAlphaState" + str(v) + ">" + str(curalpha))
                    #printState(minNode)
                    curalpha = v
                    bestState = minNode

                #check for alpha cutoff (rethink this with b = inf)
                #if curalpha >= b:
                #    numprunes = numchildren - index
                #    self.abTotalminnodesPrunedbyMax += numprunes
                #    self.abMaxPrunings += 1
                #    return minNode, curalpha  # bestState, bestEval

                #else:
                #    index += 1

            return bestState, curalpha

                #check if we should prune childnode return eval >= beta
                #if v >= curbeta:
                    #(prune)return immediately with evaluation
                #    bestState = minNode
                #    bestEval = v
                #    return bestState, bestEval

            #return max(states, key=f)
            #return bestState, bestEval

        # Transposition table helper functions
        def TTlookup(state, depth):  # add alpha and beta here
            # global bestmovedict
            # todo alpha update
            return self.TT.get(hash((state, depth)), None)  # returns bestval, alpha, beta
        def TTstore(state, depth, alpha, beta, value):
            # global bestmovedict
            self.TT[hash((state, depth))] = [value, alpha, beta]


       ####begin alphabeta function routine###


        #####ALPHABETA MAIN ROUTINE
        print("==========[ AB@D=" + str(depthlimit) + " Started]==========")

        # generate initial child states, basic move ordering
        canidateMoves = self.generateChildStates(origstatecpy, AIcolor)
        self.abNumMinNodes = len(canidateMoves)
        self.abTotalNodesGend += self.abNumMinNodes
        self.abTotalNodesGend += self.abNumMaxNodes

        ##AB SEARCH FUNCTION CALL
        retState,retEval = abSearchMax(canidateMoves, self.abAlpha, self.abBeta)



        # print stats and info
        result = " Completed"
        if self.IDcutoff == True:
            result = " Aborted"
        print()
        print ("==========[ AB@D=" + str(depthlimit) + result + " ]==========")
        if(self.abNumTimeoutEvals > 0):
            print("Nodes: " + str(self.abNumMaxNodes) + "W" + "+" + str(self.abNumMinNodes) + "B | Total: " + str(
                self.abTotalNodesGend) + " | Evaluations: " + str(self.abnodesevaluated) + "| Eval after timeout: " + str(
                self.abNumTimeoutEvals))
        else:
            print("Nodes: " + str(self.abNumMaxNodes) + "W" + "+" + str(self.abNumMinNodes) + "B | Total: " + str(
                self.abTotalNodesGend) + " | Evaluations: " + str(self.abnodesevaluated))
        print("Beta Cutoffs: " + str(self.abMinPrunings) +" times. | skipped " + str(self.abTotalMaxnodesPrunedbyMin) + " maxnodes")
        print("Alpha Cutoffs: " + str(self.abMaxPrunings) + " times. | skipped " + str(self.abTotalminnodesPrunedbyMax) + " minnodes")
        if self.whitewinsfound or self.blackwinsfound:
            print("Wins found: White=" + str(self.whitewinsfound) + " Black=" + str(self.blackwinsfound))

        #return evaluation, best move, alpha and beta
        return retEval, retState, retEval, self.abBeta # return eval, State


    #Hal calls IDsearch up to a certain depth, returning the next state(board) and it's value
    def IDsearch(self, state, depth, halscolor=None):
        # runs iterative deepening / alphabetasearch up to a specified depth to improve the performance of the AI
        #returns chosen value and chosen state

        #self.abTotalminnodesPrunedbyMax = 0
        #self.abTotalMaxnodesPrunedbyMin = 0
        #self.IDTotalNodesGenerated = 0

        self.IDalpha = -float('infinity')
        self.IDbeta = float('infinity')

        self.IDcutoff = False

        if halscolor == None:
            halscolor = self.getColor()
        print("Hal begins Iterative Deepening search.... " + " [Depth=" + str(depth)+ "] [Timeout=" + str(self.timeout) + "s]")

        # copy the current state
        origstatecpy = copy.deepcopy(state)
        #print("\nIDstartState:")
        #printState(origstatecpy)
        # erase the TT dict on startup of idsearch
        #self.TT = {}  # Looku table which holds known best moves

        self.bestValueSoFar = None #pv
        self.bestStateForHal = None
        self.depthreached = 0

        try:
            p = threading.Thread(target=self.signalTimeout, name="mytimer")
            p.daemon = True
            p.start()  # run thread for 15 seconds
        except:
            print("unable to start timeout timer thread")


        tempalpha = self.IDalpha
        #run alphabeta for each depth. iterating up to depth n
        for n in range(1, depth + 1, 1):

            #return best move up to depth n
            EvalofHalsMove, bestStateForHal, newalpha, newbeta = self.alphabetasearch(origstatecpy, tempalpha, self.IDbeta, n, halscolor)

            #cutoff or update stats
            if self.IDcutoff:
                print("IDsearch: Ending due to timeout(" + str(self.timeout)+ "s) on d:" + str(n))
                break
            else:
                self.bestValueSoFar = EvalofHalsMove
                self.depthreached = self.depthreached + 1
                self.nummaxdisplay = self.abNumMaxNodes
                self.nummindisplay = self.abNumMinNodes
                self.totalnodesdisplay = self.abTotalNodesGend
                print("IDsearch: storing result AB@d=" + str(n) + " (ev=" + str(EvalofHalsMove) + " a:" + str(newalpha) + " b:" + str(self.IDbeta))
                self.IDalpha = tempalpha
                print("\nbestStateFound: (eval of " + str(EvalofHalsMove) + ")")
                printState(bestStateForHal)
        print("")
        # printState(chosenState)

        # save for display to screen
        self.finalval = self.bestValueSoFar
        self.finaldepth = self.depthreached

        print("IDSearch returning value: " + str(self.bestValueSoFar) + " (@d=" + str(self.depthreached) + ")")
        return EvalofHalsMove, bestStateForHal

    #used by thread for timeout
    def signalTimeout(self):
        time.sleep(self.timeout)
        #print("timeout")
        self.IDcutoff = True

    def generateChildStates(self, state, color):
        """returns list of succesor (eval, state) pairs, in order, from a given board state and color
        (sorted by (largest first if white, smallest first if black)"""

        allMovesSideCanMake = []
        total = 0

        # get a list of all nodes for the given color
        if color == "white":
            pieceslist = state.getSortedWhiteList()
        elif color == "black":
            pieceslist = state.getSortedBlackList()

        # generate available moves from list of pieces from 1 side for the given state
        for coord in pieceslist:
            mymoves = getMoveListForPiece(state, coord) #returns list of (Movetype, Statecpy, ParamsForMovetype)
            # if jump is one of those moves (always ordered first), erase the rest. We must jump
            if mymoves[0][0] == jump:
                allMovesSideCanMake = mymoves
                break

            # append this list of moves to master move list for this board position
            allMovesSideCanMake = allMovesSideCanMake + mymoves
            continue

        # presort for basic move ordering here. needs history function
        # sorted(completemovelist)
        # move ordering: pre-evaluate and sort depending on what color hal is
        # _ = "dummy"

        #list of children
        orderedChildStates = [s for m, s, p in allMovesSideCanMake]

        #order states depending on which color we are (white=Max)
        if color == "white":
            #order max first
            orderedChildStates.sort(reverse=True, key= lambda s: s.getEvaluation())  # sort with most positive values on the left and most negative to the right (good for white)
        else:
            #order min first
            orderedChildStates.sort(key= lambda s: s.getEvaluation())

        return orderedChildStates
