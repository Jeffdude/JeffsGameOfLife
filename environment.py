
import pygame, random

class Cell():
    """ The Cell class is the implementation of the basic organism in JGOL"""
    def __init__(self,world,x,y):
        self.world = world
        self.x = x
        self.y = y
        self.energy = 70
        self.isFood = False

    def update(self):
        """ Main update loop. will be called on every cell """
        if self.isFood:
            return
        else:
            if self.energy <= 0:
                self.isFood = True
                return

            decision = int(random.random() * 6)
            if self.energy > 45 and decision < 3:
                if self.reproduce():
                    self.energy -= 20
                    return
            elif self.energy > 0 and decision < 5:
                if self.eat():
                    return
                else: 
                    self.randomWalk()
                    return
            else:
                self.energy -= 5
                return


    def randomWalk(self):
        """ choose a random direction and move if possible """
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
            self.energy -= 10
        else: 
            self.energy -= 5

    def eat(self):
        if self.world.foodAt(self.x + 1, self.y):
            self.world.eat(self.x + 1, self.y)
            self.energy += 10
            return True
        elif self.world.foodAt(self.x - 1, self.y):
            self.world.eat(self.x - 1, self.y)
            self.energy += 10
            return True
        elif self.world.foodAt(self.x, self.y + 1):
            self.world.eat(self.x, self.y + 1)
            self.energy += 10
            return True
        elif self.world.foodAt(self.x, self.y - 1):
            self.world.eat(self.x, self.y - 1)
            self.energy += 10
            return True
        else: 
            self.energy -= 5
            return False

    def reproduce(self):
        """ Returns true if cell successfully reproduced """
        direction = int(random.random() * 4)
        if direction == 0:
            if not self.world.isOccupied(self.x + 1, self.y):
                self.world.addCell( Cell(self.world, self.x + 1, self.y))
                return True
        elif direction == 1:
            if not self.world.isOccupied(self.x - 1, self.y):
                self.world.addCell( Cell(self.world, self.x - 1, self.y))
                return True
        elif direction == 2:
            if not self.world.isOccupied(self.x, self.y + 1):
                self.world.addCell( Cell(self.world, self.x, self.y + 1))
                return True
        elif direction == 3:
            if not self.world.isOccupied(self.x, self.y - 1):
                self.world.addCell( Cell(self.world, self.x, self.y - 1))
                return True
        return False


class World():
    """ The World class will contain global resource data and information about
        specific cells"""
    def __init__(self,x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.cells = []
        self.food = []

    def addCell(self, newCell):
        self.cells.append(newCell)

    def eat(self, x, y):
        for c in self.cells:
            if c.isFood and c.x == x and c.y == y:
                self.cells.remove(c)
                return True
        return False

    def foodAt(self,x,y):
        for c in self.cells:
            if c.isFood and c.x == x and c.y == y:
                return True
        return False

    def isOccupied(self,x,y):
        for c in self.cells:
            if c.x == x and c.y == y:
                return True
        return False
    def organismNear(self,x,y):
        return False
    def isOrganism(self,x,y):
        return False
    def isFood(self,x,y):
        return False
