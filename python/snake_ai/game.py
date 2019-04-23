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
        self.direction = 1

    def spawn_fruit(self):
        self.fruitPos = Vector(random.randint(0, self.width-1), random.randint(0, self.height-1))
        while self.fruitPos == self.tail[0]:
            self.fruitPos = Vector(random.randint(0, self.width-1), random.randint(0, self.height-1))

    def is_in_bounds(self, p):
        '''
        is vector p in bounds?
        '''
        pass

    def is_eating_tail(self, p):
        '''
        is vector somewhere in the tail?
        '''

        # assume it's not dead
        dead = False

        # if the vector is the same as one of the tail vectors, it's dead
        for t in self.tail:
            dead = p == t

        return dead

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
        
        # establish the head of the snake's position
        head = self.tail[-1]

        # increment tail length if it ate
        if head == self.fruitPos:
            self.tailLength += 1

        # no change: make newDirection the previous direction
        if newDirection == 0:
            newDirection = self.direction

        # go right, up, left, or down
        if newDirection == 1:
            self.tail.append(Vector(head.x + 1, head.y))
        elif newDirection == 2:
            self.tail.append(Vector(head.x, head.y - 1))
        elif newDirection == 3:
            self.tail.append(Vector(head.x - 1, head.y))
        elif newDirection == 4:
            self.tail.append(Vector(head.x, head.y + 1))

        # update direction
        self.direction = newDirection

        # remove end of tail if didn't eat
        if len(self.tail) > self.tailLength:
            self.tail.pop(0)

        # spawn a new fruit if it ate
        if head == self.fruitPos:
            self.spawn_fruit()

        # check if you've died
        dead = self.is_in_bounds(head) or self.is_eating_tail(head)

    def render(self):
        pass
