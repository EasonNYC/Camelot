#import bitarray
from bitarray import *

NUMROWS = 14
NUMCOLS = 8
NUMTILES = NUMROWS*NUMCOLS # need two 112 bit arrays representing white and black positions respectively


def printbits(map):
    print('          01234567')
    for x in range(NUMROWS):
        print(str(map[x*NUMCOLS:x*NUMCOLS+8:1]) + str(x))


#top left = 0,0
#x goes right 0 to 7
#y goes downward 0 to 13
bitarray('10001')


#blank board
blankboard = bitarray(NUMTILES)
blankboard.setall(False)

#goal tiles
goalrow = bitarray(NUMCOLS)
goalrow.setall(False)
goalrow[3:5] = True
whitegoal = blankboard.copy()
whitegoal[NUMTILES-8::1] |= goalrow #final row is whites target goal
blackgoal = blankboard.copy()
blackgoal[:8:1] |= goalrow

#out of Bounds
OBrow1 = ~goalrow.copy()
OBrow2 = bitarray('11000011')
OBrow3 = bitarray('10000001')
blankrow = bitarray('00000000')
outofbounds = bitarray('')
outofbounds += OBrow1
outofbounds += OBrow2
outofbounds += OBrow3
outofbounds += blankrow*8
outofbounds += OBrow3
outofbounds += OBrow2
outofbounds += OBrow1


#black and white start positions
backrow = bitarray('00111100')
frontrow = bitarray('00011000')
whiteStartPos = blankboard.copy()
whiteStartPos[NUMCOLS*4:NUMCOLS*4+8:1] = backrow
whiteStartPos[NUMCOLS*5:NUMCOLS*5+8:1] = frontrow
blackStartPos = blankboard.copy()
blackStartPos[NUMCOLS*8:NUMCOLS*8+8:1] = frontrow
blackStartPos[NUMCOLS*9:NUMCOLS*9+8:1] = backrow
printbits(whiteStartPos)
print()


#plainmove mask
plainmask = blankboard.copy()
row = 3
col = 2
pos = row*8 + col
if col == 0:
    #top
    plainmask[pos - 8:pos - 6:1] = bitarray('11')
    #samerow
    plainmask[pos + 1] = True
    #bottom
    plainmask[pos + 8:pos + 10:1] = bitarray('11')
elif col == 7:
    # top
    plainmask[pos - 9:pos - 7:1] = bitarray('11')
    # samerow
    plainmask[pos - 1] = True
    # bottom
    plainmask[pos + 7:pos + 9:1] = bitarray('11')
else:
    plainmask[pos-9:pos-6:1] = bitarray('111')
    plainmask[pos - 1:pos+2:1] = bitarray('101')
    plainmask[pos+7:pos+10:1] = bitarray('111')

result = plainmask & ~outofbounds #eleminate OB squares
printbits(result)
#result =result & ~whiteStartPos #eleminate enemy squares
#result = result & ~blackStartPos #eleminate friendly squares (minus out our pos)

#cantormask/jumpmask
#get plainmask
jumpmask = result & whiteStartPos
cantormask = result & blackStartPos
pos = row*8 + col
if col == 0:
    #top
    plainmask[pos - 8*2] = plainmask[pos - 8]
    plainmask[pos - 7*2] = plainmask[pos - 7]
    #samerow
    plainmask[pos + 1*2] = plainmask[pos + 1]
    #bottom
    plainmask[pos + 8*2] = plainmask[pos + 8]
    plainmask[pos+ 9*2] = plainmask[pos + 9]
elif col == 7:
    # top
    plainmask[pos - 9:pos - 7:1] = bitarray('11')
    # samerow
    plainmask[pos - 1] = True
    # bottom
    plainmask[pos + 7:pos + 9:1] = bitarray('11')
else:
    plainmask[pos-9:pos-6:1] = bitarray('111')
    plainmask[pos - 1:pos+2:1] = bitarray('101')
    plainmask[pos+7:pos+10:1] = bitarray('111')