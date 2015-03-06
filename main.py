"""
Main file of my experiments with game of life

Written by Jeff
"""
import pygame, random, time, sys
from pygame.locals import *
from environment import World
from environment import Cell

#DEFINE CONSTANTS

MAX_X = 268
MAX_Y = 268
SIZE = 3

WHITE = (255, 255, 255)
GREEN = (0, 80, 0)
RED = (150, 0, 0)
BLACK = (0, 0, 0)

pygame.init()
pygame.display.set_caption('Jeff\'s Conway Game of Life Test')
screen = pygame.display.set_mode([MAX_X * SIZE, MAX_Y * SIZE])
screen.fill(WHITE)

# creating the world
myWorld = World(MAX_X, MAX_Y)
# adding a single cell
myWorld.reviveCell(124,124,150)


# Used to draw the cell
def drawCell(c):
    if(c.x < 0  or  c.x > MAX_X  or  c.y < 0  or  c.y > MAX_Y):
        return False
    if(c.isFood):
        cell_color = (0,0 ,(5 * c.energy)%255)
        pygame.draw.rect(screen, cell_color, ((c.x * SIZE, c.y * SIZE), (SIZE, SIZE)))
    else:
        cell_color = ((c.energy*10)%255, 40, 0)
        pygame.draw.rect(screen, cell_color, ((c.x * SIZE, c.y * SIZE), (SIZE, SIZE)))

    return True


# Main Loop
while True:
    screen.fill(WHITE)
    for column in myWorld.cells:
        for cell in column:
            cell.update()
            drawCell(cell)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
