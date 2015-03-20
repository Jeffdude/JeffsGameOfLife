"""
Main file of 2d ecosystem

Written by Jeff
"""
import pygame, random, time, sys
from pygame.locals import *

#DEFINE CONSTANTS
RESOLUTION = 4

VIEW_WIDTH   = 256 * RESOLUTION
VIEW_HEIGHT  = 256 * RESOLUTION
WORLD_WIDTH  = 256 * RESOLUTION
WORLD_HEIGHT = 256 * RESOLUTION

WHITE = (255, 255, 255)

def drawHeight(x, y, res, height):
    if(x < 0 or y < 0 or x > VIEW_WIDTH or y > VIEW_HEIGHT):
        return False
    color = (0, 0, (50 + 10*height)%255) 
    pygame.draw.rect(screen, color, ((x * res, y * res),(res, res)))
    return True

def generateHeightMap(worldWidth, worldLength, resolution):
    resWidth = int(worldWidth/resolution)
    resLength = int(worldLength/resolution)
    startHeight = 10
    randMagnitude = 15
    heightMap = [[startHeight for x in range(int(resWidth))] for y in range(int(resWidth))]

    # first, randomly seed the corners
    heightMap[0][0] = random.random() * (2 * randMagnitude)
    heightMap[resWidth - 1][0] = random.random() * (2 * randMagnitude)
    heightMap[0][resLength - 1] = random.random() * (2 * randMagnitude)
    heightMap[resWidth - 1][resLength - 1] = random.random() * (2 * randMagnitude)
    # then, begin diamond square algorithm
    diamondSquare(heightMap, (0,0), resWidth - 1, resLength - 1, randMagnitude)
    return heightMap

def diamondSquare(heightMap, origCoord, width, length, randMagnitude):
    width = int(width)
    length = int(length)

    # base case
    if width <= 1 or length <= 1:
        return
    
    # get corner values
    tl = heightMap[origCoord[0]][origCoord[1]]
    tr = heightMap[int(origCoord[0] + width)][origCoord[1]]
    bl = heightMap[origCoord[0]][int(origCoord[1] + length)]
    br = heightMap[int(origCoord[0] + width)][int(origCoord[1] + length)]
    
    # locate center
    centerW = int(width/2)
    centerL = int(length/2)

    ### Square ### 
    # generate and assign center height
    avg = (tl + tr + bl + br) / 4
    heightMod = random.random() * (2 * randMagnitude)
    cHeight = avg + heightMod
    heightMap[origCoord[0] + centerW][origCoord[1] + centerL] = cHeight

    ### Diamond ###
    # get off-side values if they exist, 10 is default
    tOff = lOff = bOff = rOff = 10  
    if origCoord[1] - centerL > 0:
        tOff = heightMap[int(origCoord[0] + centerW)][int(origCoord[1] - centerL)]
    if origCoord[0] - centerW > 0:
        lOff = heightMap[int(origCoord[0] - centerW)][int(origCoord[1] + centerL)]
    if origCoord[1] + length + centerL <= len(heightMap[0]):
        bOff = heightMap[int(origCoord[0] + centerW)][int(origCoord[1] + length + centerL)]
    if origCoord[0] + width + centerW <= len(heightMap):
        rOff = heightMap[int(origCoord[0] + width + centerW)][int(origCoord[1] - centerL)]

    # generate and assign edge heights
    tAvg = int((tl + tr + cHeight + tOff) / 4)
    lAvg = int((tl + bl + cHeight + lOff) / 4)
    rAvg = int((tr + br + cHeight + rOff) / 4)
    bAvg = int((bl + br + cHeight + bOff) / 4)
    # top
    tHMod = random.random() * (2 * randMagnitude)
    tHeight = tAvg + tHMod
    heightMap[origCoord[0] + centerW][origCoord[1]] = tHeight
    # left
    lHMod = random.random() * (2 * randMagnitude)
    lHeight = lAvg + lHMod
    heightMap[origCoord[0]][origCoord[1] - centerL] = lHeight
    # bottom
    bHMod = random.random() * (2 * randMagnitude)
    bHeight = bAvg + bHMod
    heightMap[origCoord[0] + centerW][origCoord[1] + length] = bHeight
    # right
    rHMod = random.random() * (2 * randMagnitude)
    rHeight = rAvg + rHMod
    heightMap[origCoord[0] + width][origCoord[1] + centerL] = rHeight

#    randMagnitude = randMagnitude - 2 * random.random()

    # recursive calls
    # top left square
    diamondSquare(heightMap, origCoord, centerW, centerL, randMagnitude)
    # top right square
    trOrig = (origCoord[0] + centerW, origCoord[1])
    diamondSquare(heightMap, trOrig, centerW, centerL, randMagnitude)
    # bottom left square
    blOrig = (origCoord[0], origCoord[1] + centerL)
    diamondSquare(heightMap, blOrig, centerW, centerL, randMagnitude)
    # bottom right square
    brOrig = (origCoord[0] + centerW, origCoord[1] + centerL)
    diamondSquare(heightMap, brOrig, centerW, centerL, randMagnitude)

pygame.init()
pygame.display.set_caption('What SHOULD be the diamond square algorithm')
screen = pygame.display.set_mode([VIEW_WIDTH, VIEW_HEIGHT])
screen.fill(WHITE)
heightMap = generateHeightMap(WORLD_WIDTH, WORLD_HEIGHT, RESOLUTION)

while True:
    for x in range(len(heightMap)):
        for y in range(len(heightMap[1])):
            drawHeight(x, y, RESOLUTION, heightMap[x][y])
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_r:
                heightMap = generateHeightMap(WORLD_WIDTH, WORLD_HEIGHT, RESOLUTION)
    pygame.display.update()




def generateHeightMapOld(worldWidth, worldHeight, resolution):
    resWidth = worldWidth/resolution
    resHeight = worldHeight/resolution
    numIterations = 10
    numPoints = 10
    modifiedCoords = []
    startHeight = 10
    heightRange = 100
    heightMap = [[startHeight for x in range(resWidth)] for y in range(resWidth)]

    for n in range(numIterations):
        for i in range(numPoints):
            coord = (-1,-1)
            while coord not in modifiedCoords:
                x = random.random() * resWidth
                y = random.random() * resHeight
                coord = (x, y)
            modifiedCoords.append(coord)
            heightVal = random.random() * (2 * heightRange)
            heightVal = heightVal - (heightRange / 2)
            heightMap[coord[0]][coord[1]] = heightVal + startHeight

