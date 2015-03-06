
import pygame, random

class Cell():
    """ The Cell class is the implementation of the basic organism in JGOL"""
    def __init__(self,world,x,y):
        self.world = world
        self.x = x
        self.y = y
        self.energy = 14
        self.isFood = True
        self.age = 0
        self.favDirection = -1

    def update(self):
        """ Main update loop. will be called on every cell """
        if self.isFood:
            if self.energy > 15:
                self.isFood = False
                return
        else:
            self.age += 1
            if self.energy > 40 and self.age > 2:
                if self.reproduce(39):
#                    print('r')
                    self.energy += 1
                    return
                else:
#                    print('fr')
                    self.energy -= 8
            elif self.energy > 15: 
                if self.eat():
#                    print('e')
                    return
                else:
#                    print('fe')
                    self.energy -= 5
            elif self.energy <= 15:
                self.isFood = True
                return

    def eat(self):
        direction = int(random.random() * 4)
        if direction == 0:
            if self.world.foodAt(self.x + 1, self.y):
                self.energy += self.world.eat(self.x + 1, self.y)
                self.favDirection = direction
                return True
        if direction == 1:
            if self.world.foodAt(self.x - 1, self.y):
                self.energy += self.world.eat(self.x - 1, self.y)
                self.favDirection = direction
                return True
        if direction == 2:
            if self.world.foodAt(self.x, self.y + 1):
                self.energy += self.world.eat(self.x, self.y + 1)
                self.favDirection = direction
                return True
        if direction == 3:
            if self.world.foodAt(self.x, self.y - 1):
                self.energy += self.world.eat(self.x, self.y - 1)
                self.favDirection = direction
                return True
        else:
            self.energy += 3
            return False

    def reproduce(self, transferEnergy):
        """ Returns true if cell successfully reproduced """
        if not self.favDirection == -1:
            direction = self.favDirection
        else:
            direction = int(random.random() * 4)
        if direction == 0:
            if not self.world.isOccupied(self.x + 1, self.y):
                self.world.reviveCell(self.x + 1, self.y, transferEnergy)
                self.energy -= transferEnergy
                return True
        elif direction == 1:
            if not self.world.isOccupied(self.x - 1, self.y):
                self.world.reviveCell(self.x - 1, self.y, transferEnergy)
                self.energy -= transferEnergy
                return True
        elif direction == 2:
            if not self.world.isOccupied(self.x, self.y + 1):
                self.world.reviveCell(self.x, self.y + 1, transferEnergy)
                self.energy -= transferEnergy
                return True
        elif direction == 3:
            if not self.world.isOccupied(self.x, self.y - 1):
                self.world.reviveCell(self.x, self.y - 1, transferEnergy)
                self.energy -= transferEnergy
                return True
        else: 
            return False


class World():
    """ The World class will contain global resource data and information about
        specific cells"""
    def __init__(self,x_max, y_max):
        self.x_max = x_max
        self.y_max = y_max
        self.cells = []

        # fill in the array of cells
        for y in range(self.y_max):
            column = []
            for x in range(self.x_max):
                column.append(Cell(self, x, y))
            self.cells.append(column)

    def reviveCell(self, x_coord, y_coord, transferEnergy):
        if x_coord >= self.x_max or x_coord < 0:
            return
        if y_coord >= self.y_max or y_coord < 0:
            return 
        self.cells[x_coord][y_coord].energy += transferEnergy

    def eat(self, x, y):
        transferEnergy = self.cells[x][y].energy 
        self.cells[x][y].energy = 0
        return transferEnergy

    def foodAt(self,x,y):
        if x >= self.x_max or x < 0:
            return False
        if y >= self.y_max or y < 0:
            return False
        return self.cells[x][y].isFood and self.cells[x][y].energy > 0

    def isOccupied(self,x,y):
        if x >= self.x_max or x < 0:
            return True
        if y >= self.y_max or y < 0:
            return True
        return not self.cells[x][y].isFood
