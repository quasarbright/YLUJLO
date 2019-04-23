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

    def __str__(self):
        return '<{}, {}>'.format(self.x, self.y)

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
        # save snake's head vector
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

class VisibleGame(Game):
    '''
    a game that is rendered on screen
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_width = 500
        self.window_height = 500
        self.win = GraphWin("Snake", self.window_width, self.window_height)
        self.rect_width = self.window_width / self.width
        self.rect_height = self.window_height / self.height
    
    def draw_rectangle_at(self, r, c, color):
        p1 = Point(c*self.rect_width, r*self.rect_height)
        p2 = Point((c+1)*self.rect_width, (r+1)*self.rect_height)
        r = Rectangle(p1, p2)
        r.setFill(color)
        r.setWidth(1)
        r.setOutline('black')
        r.draw(self.win)
    
    def draw_background(self):
        for r in range(self.height):
            for c in range(self.width):
                self.draw_rectangle_at(r, c, 'gray')
    
    def draw_tail(self):
        for position in self.tail:
            c = position.x
            r = position.y
            self.draw_rectangle_at(r, c, 'white')
    
    def draw_fruit(self):
        c = self.fruitPos.x
        r = self.fruitPos.y
        self.draw_rectangle_at(r, c, 'red')
    
    def draw(self):
        self.draw_background()
        self.draw_tail()
        self.draw_fruit()

    def close(self):
        self.win.close()

class PlayableGame(VisibleGame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def handle_keypress(self):
        pass


if __name__ == '__main__':
    vg = VisibleGame(5, 5)
    vg.draw()
    while True:
        print(list(map(str, vg.tail)), vg.fruitPos)
        vg.win.getMouse()
