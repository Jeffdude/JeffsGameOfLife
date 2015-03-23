"""
Main file of 2d ecosystem

Written by Jeff
"""
import pygame, random, time, sys
from pygame.locals import *
from color import *

#DEFINE CONSTANTS
RESOLUTION = 2

WORLD_WIDTH  = 512 + 1
WORLD_LENGTH = 512 + 1
VIEW_WIDTH   = WORLD_WIDTH * RESOLUTION
VIEW_LENGTH  = WORLD_LENGTH * RESOLUTION

WHITE = (255, 255, 255)

def makeColor(toColorize):
    maxColorizable = 850
    if toColorize < maxColorizable:
        return rgb(toColorize,0,maxColorizable)
    else:
        print("Color exceeds max colorizable value")
        return (0,0,0)

def drawHeight(x, y, res, height):
    if(x < 0 or y < 0 or x > WORLD_WIDTH or y > WORLD_LENGTH):
        return False
    color = makeColor(height)
    pygame.draw.rect(screen, color, ((x * res, y * res),(res, res)))
    return True

def checkWorldParams(width, length):
    """ ensure width, length are of the for 2^n where n < 20"""
    wAcceptable = lAcceptable = False
    for i in range(20):
        p = 2**i
        if p == width:
            wAcceptable = True
        if p == length:
            lAcceptable = True
    return not wAcceptable or not lAcceptable
def generateHeightMap(worldWidth, worldLength):
    """ generate a heightmap of width worldWidth and length worldLength using
    the diamond square algorithm"""

    if not checkWorldParams(worldWidth, worldLength):
        raise ValueError("world width or world height not in the form of 2^n where n < 20")

    startHeight = 10
    randMagnitude = 100

    # creating the map
    heightMap = [[startHeight for x in range(worldWidth)] for y in range(worldLength)]

    # first, randomly seed the corners
    heightMap[0][0] = random.random() * randMagnitude
    heightMap[worldWidth - 1][0] = random.random() * randMagnitude
    heightMap[0][worldLength - 1] = random.random() * randMagnitude
    heightMap[worldWidth - 1][worldLength - 1] = random.random() * randMagnitude
    # then, begin diamond square algorithm
    diamondSquare(heightMap, (0,0), worldWidth - 1, worldLength - 1, randMagnitude)
    return heightMap

def diamondSquare(heightMap, origCoord, width, length, randMagnitude):
    # debug:
    # print('-- ds called on coords ({},{}) with width {} and length {} ---'.format(origCoord[0], origCoord[1], width, length))
    if width != int(width):
        print('Width division disparity:{} -> {}'.format(width, int(width)))
        width = int(width)
    if length != int(length):
        print('Length division disparity:{} -> {}'.format(length, int(length)))
        length = int(length)

    # base case
    if width <= 1 or length <= 1:
        return
    
    # coordinate formatting
    x, y = origCoord # origCoord = (x,y)
    # ensure the given origCoords are valid 
    if x != int(x):
        print('Central x integer disparity:{} -> {}'.format(x, int(x)))
    if y != int(y):
        print('Central y integer disparity:{} -> {}'.format(y, int(y)))
    
    # get corner values
    tl = heightMap[x][y]
    tr = heightMap[int(x + width)][y]
    bl = heightMap[x][int(y + length)]
    br = heightMap[int(x + width)][int(y + length)]
    
    # locate center and ensure proper coordinate division occurs
    centerW = int(width/2)
    centerL = int(length/2)
    if width/2 != int(width/2):
        print('Central width division disparity:{} -> {}'.format(width/2, int(width/2)))
        centerW = int(width/2)
    if length/2 != int(length/2):
        print('Central length division disparity:{} -> {}'.format(length/2, int(length/2)))
        centerL = int(length/2)

    ### Square ### 
    # generate and assign center height
    avg = (tl + tr + bl + br) / 4
    cHeight = avg + random.random() * randMagnitude
    heightMap[x + centerW][y + centerL] = cHeight

    ### Diamond ###
    # get off-side values if they exist, 10 is default
    tOff = lOff = bOff = rOff = 10  
    if y - centerL >= 0:
        tOff = heightMap[int(x + centerW)][int(y - centerL)]
    if x - centerW >= 0:
        lOff = heightMap[int(x - centerW)][int(y + centerL)]
    if y + length + centerL < len(heightMap[0]):
        bOff = heightMap[int(x + centerW)][int(y + length + centerL)]
    if x + width + centerW < len(heightMap):
        #print(x + width + centerW)
        rOff = heightMap[int(x + width + centerW)][int(y - centerL)]

    # generate and assign edge heights
    tAvg = int((tl + tr + cHeight + tOff) / 4)
    lAvg = int((tl + bl + cHeight + lOff) / 4)
    rAvg = int((tr + br + cHeight + rOff) / 4)
    bAvg = int((bl + br + cHeight + bOff) / 4)
    # top
    tHeight = tAvg + random.random() * randMagnitude
    heightMap[x + centerW][y] = tHeight
    # left
    lHeight = lAvg + random.random() * randMagnitude
    heightMap[x][y - centerL] = lHeight
    # bottom
    bHeight = bAvg + random.random() * randMagnitude
    heightMap[x + centerW][y + length] = bHeight
    # right
    rHeight = rAvg + random.random() * randMagnitude
    heightMap[x + width][y + centerL] = rHeight

    # recursive calls
    # top left square
    diamondSquare(heightMap, origCoord, centerW, centerL, randMagnitude)
    # top right square
    trOrig = (x + centerW, y)
    diamondSquare(heightMap, trOrig, centerW, centerL, randMagnitude)
    # bottom left square
    blOrig = (x, y + centerL)
    diamondSquare(heightMap, blOrig, centerW, centerL, randMagnitude)
    # bottom right square
    brOrig = (x + centerW, y + centerL)
    diamondSquare(heightMap, brOrig, centerW, centerL, randMagnitude)

def drawMap():
    for x in range(len(heightMap)):
        for y in range(len(heightMap[0])):
            drawHeight(x, y, RESOLUTION, heightMap[x][y])
pygame.init()
pygame.display.set_caption('What SHOULD be the diamond square algorithm')
screen = pygame.display.set_mode([VIEW_WIDTH, VIEW_LENGTH])
screen.fill(WHITE)
heightMap = generateHeightMap(WORLD_WIDTH, WORLD_LENGTH)
drawMap()

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_r:
                heightMap = generateHeightMap(WORLD_WIDTH, WORLD_LENGTH)
                drawMap()
    pygame.display.update()
