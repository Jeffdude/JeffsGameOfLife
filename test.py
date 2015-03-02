"""
Main file of my experiments with game of life

Written by Jeff
"""
import pygame, random, time, sys
from pygame.locals import *
from environment import World
from environment import Cell

#DEFINE CONSTANTS

MAX_X = 134
MAX_Y = 134
SIZE = 6

WHITE = (255, 255, 255)
RED = (255, 255, 0)
BLACK = (0, 0, 0)

pygame.init()
pygame.display.set_caption('Jeff\'s Conway Game of Life Test')
screen = pygame.display.set_mode([MAX_X * SIZE, MAX_Y * SIZE])
screen.fill(WHITE)

# creating the world
myWorld = World(MAX_X, MAX_Y)
# adding a single cell
myCell = myWorld.addCell( Cell(myWorld, 10, 10) )


# Used to draw the cell
def drawCell(c):
    if(c.x < 0  or  c.x > MAX_X  or  c.y < 0  or  c.y > MAX_Y):
        return False

    if(c.isFood):
        print("drawing food")
        pygame.draw.rect(screen, RED, ((c.x * SIZE, c.y * SIZE), (SIZE, SIZE)))
    elif(not c.isFood):
        pygame.draw.rect(screen, BLACK, ((c.x * SIZE, c.y * SIZE), (SIZE, SIZE)))
    return True


# Main Loop
while True:
    screen.fill(WHITE)
    for cell in myWorld.cells:
        cell.update()
        drawCell(cell)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
