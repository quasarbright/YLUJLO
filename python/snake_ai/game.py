import random
from graphics import *

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))


class Game:
    def __init__(self, width, height, show=False):
        if show:
            pass
        else:
            pass
        self.width = width
        self.height = height
        startingHead = Vector(random.randint(0,width-1), random.randint(0, height-1))
        self.tail = [startingHead] # list of vectors
        self.tailLength = len(self.tail)
        self.fruitPos = Vector()
        self.spawn_fruit()
        self.direction = 0
    
    def spawn_fruit(self):
        self.fruitPos = Vector(random.randint(0, self.width-1), random.randint(0, self.height-1))
        while self.fruitPos == self.tail[0]:
            self.fruitPos = Vector(random.randint(0, self.width-1), random.randint(0, self.height-1))
    
    def is_in_bounds(self, p):
        '''
        is vector p in bounds?
        '''
        pass


    def return_state(self):
        '''
        return representation as a 1D list
        '''
        pass
    
    def move_player(self, newDirection):
        '''
        direction is 0, 1, 2, or 3, or 4
        nothing, right, up, left, down
        '''
        pass
    
    def render(self):
        pass
