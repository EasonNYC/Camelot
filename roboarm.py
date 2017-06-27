import time
import vrep
from board import Coord

class RobotArm(object):
    def __init__(self):
        self.z_floor = .515 #table height / resting height
        self.z_deck = .7 #ARM seeking height above the table to avoid collisions
        self.wtaken = [False,False,False,False,False,False]
        self.btaken = [False,False,False,False,False,False]
        self.x_takenWhite = .225
        self.x_takenBlack = -.225
        self.y_takenWhite = 1.125
        self.y_takenBlack = .875
        self.taken_offset = .05

        self.restPosXYZ = [ .0750, .5802, .7347]
        self.restOrein = [45, 0, 0]

        self.pickupOrein = [0,0,0]

        self.emptyBuff = bytearray()
                #initialize vrep
        vrep.simxFinish(-1)  # just in case, close all opened connections
        self.clientID = vrep.simxStart('127.0.0.1', 19997, True, True, 5000, 5)  # Connect to V-REP
        if self.clientID != -1:
            print("connected to vrep.")
        err = vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)

        #handles
        err, self.HALtipHandle = vrep.simxGetObjectHandle(self.clientID, "HAL_tip", vrep.simx_opmode_blocking)

        #populate board quickly

        #ready to play
        self.print2VREP("Hal is moving arm to resting position.")
        self.gotoRest(Coord(0,0))

    # FUNCTIONS
    def activateVac(self):
        err = vrep.simxSetIntegerSignal(self.clientID, "BaxterVacuumCup_active", 1,
                                        vrep.simx_opmode_blocking)  # 1 to close, 0 to open

    def deactivateVac(self):
        err = vrep.simxSetIntegerSignal(self.clientID, "BaxterVacuumCup_active", 0,
                                        vrep.simx_opmode_blocking)  # 1 to close, 0 to open

    def getNext(self, cur, target, unit):
        if cur < target:
            return cur + unit
        if cur > target:
            return cur - unit

    def updatePath(self,cur, target, unit):
        newx = 0
        newy = 0
        newz = 0

        if abs(cur[0] - target[0]) > unit:
            newx = self.getNext(cur[0], target[0], unit)
        else:
            newx = cur[0]
        if abs(cur[1] - target[1]) > unit:
            newy = self.getNext(cur[1], target[1], unit)
        else:
            newy = cur[1]
        if abs(cur[2] - target[2]) > unit:
            newz = self.getNext(cur[2], target[2], unit)
        else:
            newz = cur[2]
        return [newx, newy, newz]

    #slowly moves the EF target in little steps toward the specified pose and oreintation
    def move(self, pose, orein, u=.02):
        unit = u
        lastxyz = [0, 0, 0]
        tarpos = pose
        tarpos = [round(x, 4) for x in tarpos]

        #set the new EF oreintation first
        vrep.simxSetObjectOrientation(self.clientID, self.HALtipHandle, -1, orein, vrep.simx_opmode_oneshot_wait)

        while (True):
            #get current position rel to world frame
            err, curpos = vrep.simxGetObjectPosition(self.clientID, self.HALtipHandle, -1, vrep.simx_opmode_oneshot_wait)

            #roundoff precision
            curpos = [round(x, 4) for x in curpos]

            #if current position and target position are not the same, return xyz of next via
            if (curpos != tarpos):
                newxyz = self.updatePath(curpos, tarpos, unit)

                if newxyz == lastxyz:
                    #set object to exact final position we are done
                    pose[2] = newxyz[2]
                    vrep.simxSetObjectPosition(self.clientID, self.HALtipHandle, -1, pose,
                                               vrep.simx_opmode_oneshot_wait)

                    break
                vrep.simxSetObjectPosition(self.clientID, self.HALtipHandle, -1, newxyz, vrep.simx_opmode_oneshot_wait)
                lastxyz = newxyz
            else:
                print("never should get here")
                break



    """returns the x,y coordinates for vrep given an ingame coord"""
    def Conv_coord_to_XYZ(self, c):
        y = .675+(c.i * .05)
        x = .175-(c.j * .05)
        return x, y

    def Conv_xy_to_XYZ(self, a, b):
        y = .675+(a * .05)
        x = .175-(b * .05)
        return x, y

    """pick up a piece at the current location"""
    def pickupPiece(self, c):
        #2 seconds down, 2 seconds up

        x, y = self.Conv_coord_to_XYZ(c)
        print("picking up piece at (" + str(c.i) + "," + str(c.j) + ") =XYZ(" + str(x) + "," + str(y) + "," + str(self.z_floor)+")")
        xyz = [x, y, self.z_floor]
        self.move(xyz, self.pickupOrein,.005)
        time.sleep(2)

        self.activateVac()
        time.sleep(2)

        xyz = [x, y, self.z_deck]
        self.move(xyz, self.pickupOrein,.005)
        time.sleep(2)
        print("...done.")

    """put down piece at the current location"""
    def putdownPiece(self, c):
        # 2 seconds down, 2 seconds up
        if(c.i == -1):
            err, curpos = vrep.simxGetObjectPosition(self.clientID, self.HALtipHandle, -1, vrep.simx_opmode_oneshot_wait)
            x = curpos[0]
            y=curpos[1]
            xyz = [x, y, self.z_floor]
            self.move(xyz, self.pickupOrein, .005)
            time.sleep(2)

            self.deactivateVac()
            time.sleep(2)

            xyz = [x, y, self.z_deck]
            self.move(xyz, self.pickupOrein, .005)
            time.sleep(2)
            print("...done.")
            return
        x, y = self.Conv_coord_to_XYZ(c)
        print("putting down piece at (" + str(c.i) + "," + str(c.j) + ") =XYZ(" + str(x) + "," + str(y) + "," + str(self.z_floor)+")")

        xyz = [ x , y , self.z_floor]
        self.move(xyz, self.pickupOrein,.005)
        time.sleep(2)

        self.deactivateVac()
        time.sleep(2)

        xyz = [x, y, self.z_deck]
        self.move(xyz, self.pickupOrein,.005)
        time.sleep(2)
        print("...done.")


    """go from the current location to the specified hal coordinate in vrep"""
    def gotoCoord(self,c):
        #conv coord to XYZ
        #place target dummy at XYZ
        print('moving to coord(' + str(c.i)+ "," + str(c.j) + ")")
        x,y = self.Conv_coord_to_XYZ(c)
        xyz=[x,y,self.z_deck]
        self.move(xyz, self.pickupOrein)
        print("...done.")
        time.sleep(2)


    """go to the specified xyz position in vrep"""
    def gotoXYZ(self,xyzlist):
        # place target dummy at XYZ
        x=xyzlist[0]
        y=xyzlist[1]
        z=xyzlist[2]
        print('going to xyz(' + str(x) + "," + str(y) + "," + str(z)+")")
        xyz = [x, y, self.z_deck]
        self.move(xyz, self.pickupOrein)
        print("...done.")
        time.sleep(2)


    #move to resting pose
    def gotoRest(self,c):
        #conv coord to XYZ
        #place target dummy at XYZ
        print('moving to natural resting pose')
        self.move(self.restPosXYZ, self.restOrein)


    #returns xyz of an available taken spot for white or black
    def getNextFreeTakenXYZfor(self, cl):
        if cl == "white":
            takenlist = self.wtaken
            direction = 1
            x_taken = self.x_takenWhite
            y_taken = self.y_takenWhite
        elif cl == "black":
            takenlist = self.btaken
            direction = -1
            x_taken = self.x_takenBlack
            y_taken = self.y_takenBlack

        index = 0
        for x in takenlist:
            if takenlist[index] != True:
                takenlist[index] = True #mark taken
                #return x,y,z of next available free space for arm to move to

                y_taken = y_taken + direction* index * self.taken_offset
                return x_taken, y_taken
            index += 1
        print("bad takenlist calculation")
        return -1,-1

    def print2VREP(self, string):
        res, retInts, retFloats, retStrings, retBuffer = vrep.simxCallScriptFunction(self.clientID, 'remoteApiCommandServer',
                                                                                     vrep.sim_scripttype_childscript,
                                                                                     'displayText_function', [], [],
                                                                                     [string], self.emptyBuff,
                                                                                     vrep.simx_opmode_blocking)
        if res == vrep.simx_return_ok:
            print('Return string: ', retStrings[0])  # display the reply from V-REP (in this case, just a string)
        else:
            print('Remote function call failed')

    # call all functions in tasklist, return to rest pose when finished
    def executeCMD(self, tasklist):
        print()
        print("HAL is now executing a chain of robot ARM commands:")
        for task in tasklist:
            taskfuncptr = task[0]
            param = task[1]

            taskfuncptr(param[0])


    """returns a list of tasks for hal to execute from a movelist generated by the game"""
    def generateTasksFromMVlist(self, mvlist):
        generatedtasks = []

        for mv in mvlist:
            coord1 = mv[1]
            coord2 = mv[2]
            coordXYZ = Coord(-1,-1)
            colorparam = mv[3]

            if mv[0] == "MOVE": #mv = [movetype, old, new, color]
                print("OBJECTIVE: Hal's ARM is moving " + colorparam + ": (" + str(coord1.i) + "," + str(coord1.j) + ")->(" + str(coord2.i) + "," + str(coord2.j) + ")")
                # goto current piece coordinate
                func = self.gotoCoord
                param = coord1
                generatedtasks.append([func, [param]])

                # pickup piece
                func = self.pickupPiece
                param = coord1
                generatedtasks.append([func, [param]])

                # goto destination coordinate
                func = self.gotoCoord
                param = coord2
                generatedtasks.append([func, [param]])

                # putdown piece
                func = self.putdownPiece
                param = coord2
                generatedtasks.append([func, [param]])

            if mv[0] == "TAKE": #mv = [movetype, old, new, color]

                #find/assign a destination spot to put the piece
                x_vrep, y_vrep = self.getNextFreeTakenXYZfor(colorparam)
                print("OBJECTIVE: Hal's ARM is Taking " + colorparam + ": (" + str(coord1.i) + "," + str(coord1.j) + ")->TableXYZ:" + str(x_vrep) + "," + str(y_vrep) + ", Ztable")

                # goto current piece coordinate
                func = self.gotoCoord
                param = coord1
                generatedtasks.append([func, [param]])

                # pickup piece
                func = self.pickupPiece
                param = coord1
                generatedtasks.append([func, [param]])

                #go to free spot near color on table with piece
                func = self.gotoXYZ
                param = [x_vrep, y_vrep, self.z_deck]
                generatedtasks.append([func, [param]])

                # putdown piece
                func = self.putdownPiece
                param = coordXYZ
                generatedtasks.append([func, [param]])

        #go to resting position
        func = self.gotoRest
        param = coord1
        generatedtasks.append([func, [param]])

        # return generated task list
        return generatedtasks


