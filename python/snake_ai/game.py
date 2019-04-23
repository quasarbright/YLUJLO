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
    
    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError(str(type(other)))
        return Vector(self.x + other.x, self.y + other.y)


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        startingHead = Vector(random.randint(0,width-1), random.randint(0, height-1))
        self.tail = [startingHead] # list of vectors, from tail to head
        self.tailLength = len(self.tail)
        self.fruitPos = Vector()
        self.spawn_fruit()
        self.direction = 1 # can be 1, 2, 3, or 4
    
    def spawn_fruit(self):
        self.fruitPos = Vector(random.randint(0, self.width-1), random.randint(0, self.height-1))
        while self.fruitPos == self.tail[-1]:
            self.fruitPos = Vector(random.randint(0, self.width-1), random.randint(0, self.height-1))
    
    def is_in_bounds(self, p):
        '''
        is vector p in bounds?
        '''
        return p.x >=0 and p.x < self.width and p.y >= 0 and p.y < self.height


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


class VisibleGame(Game):
    '''
    a game that is rendered on screen
    '''
    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        self.window_width = 500
        self.window_height = 500
        self.win = GraphWin("Snake", self.window_width, self.window_height)
        self.rect_width = self.window_width / self.width
        self.rect_height = self.window_height / self.height
    
    def background(self):
        b = Rectangle(Point(0,0), Point(self.window_width, self.window_height))
        b.setFill('gray')
        b.draw(self.win)
        for r in range(self.height):
            for c in range(self.width):
                p1 = Point(c*self.rect_width, r*self.rect_height)
                p1 = Point((c+1)*self.rect_width, (r+1)*self.rect_height)
                

    
    def close(self):
        self.win.close()
    

