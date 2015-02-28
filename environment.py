
import pygame, random

class Cell():
    """ The Cell class is the implementation of the basic organism in JGOL"""
    def __init__(self,world,x,y):
        self.world = world
        self.x = x
        self.y = y
        self.energy = 100
        self.hunger = 0
        self.desire = 0
        self.alpha = random.random()

    def update(self):
        """ Main update loop. will be called on every cell """
        if self.energy > 0:
            direction = int(random.random() * 6)
            if direction == 0:
                self.move(1,0)
            elif direction == 1:
                self.move(-1,0)
            elif direction == 2:
                self.move(0,1)
            elif direction == 3:
                self.move(0,-1)

    def move(self, x_motion, y_motion):
        """Cell will move if its destination is empty"""
        if not self.world.isOccupied(self.x + x_motion, self.y + y_motion):
            self.x += x_motion
            self.y += y_motion


class World():
    """ The World class will contain global resource data """
    def __init__(self,x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.cells = []
        self.food = []

    def addCell(self, newCell):
        self.cells.append(newCell)

    def organismNear(self,x,y):
        return False
    def foodNear(self,x,y):
        return False
    def isOccupied(self,x,y):
        return False
    def isOrganism(self,x,y):
        return False
    def isFood(self,x,y):
        return False
