import random
from graphics import *
import keyboard

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
        return p in tail[0:-1]

    def return_state(self):
        '''
        return representation as a 1D list: distance from head to nearest object in all
        4 directions, and x and y distance to the fruit
        '''
        # save snake's head vector
        head = self.tail[-1]

        # find distance to next obstacle going right
        curr = head
        right = 0
        while self.is_in_bounds(curr) and not self.is_eating_tail(curr):
            curr.add(1,0)
            right += 1

        # find distance to next obstacle going up
        curr = head
        up = 0
        while self.is_in_bounds(curr) and not self.is_eating_tail(curr):
            curr.add(0,-1)
            up += 1

        # find distance to next obstacle going left
        curr = head
        left = 0
        while self.is_in_bounds(curr) and not self.is_eating_tail(curr):
            curr.add(-1,0)
            left += 1

        # find distance to next obstacle going down
        curr = head
        down = 0
        while self.is_in_bounds(curr) and not self.is_eating_tail(curr):
            curr.add(0,1)
            down += 1

        # find x distance to fruit
        x = abs(head.x - self.fruitPos.x)

        # find y distance to fruit
        y = abs(head.y - self.fruitPos.y)

        return [right, up, left, down, x, y]

    def reward(self, oldHead, oldFruit, newHead, newFruit, ate, died):
        '''
        calculates the reward for a movement given where the head
        was and where the head moved to
        '''

        if died:
            return -10
        elif ate:
            return 10
        else:
            oldDistance = abs(oldHead.x - oldFruit.x) + abs(oldHead.y - oldFruit.y)
            newDistance = abs(newHead.x - newFruit.x) + abs(newHead.y - newFruit.y)
            return newDistance - oldDistance


    def move_player(self, newDirection):
        '''
        direction is 0, 1, 2, or 3, or 4
        nothing, right, up, left, down
        '''
        # save snake's head vector
        head = self.tail[-1]

        ate = head == self.fruitPos
        oldFruit = selffruitPos
        # increment tail length if it ate
        if ate:
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
        if ate:
            self.spawn_fruit()

        # check if you've died
        dead = self.is_eating_tail(head) or not self.is_in_bounds(head)

        # calculate reward
        reward = self.reward(head, oldFruit, self.tail[-1], self.fruitPos, ate, died)

        # check state
        state = self.return_state()

        return reward, dead, state

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
        b = Rectangle(Point(0,0), Point(self.window_width, self.window_height))
        b.setFill('gray')
        b.draw(self.win)
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
        keyboard.on_press(self.handle_keypress)

    def handle_keypress(self, ke):
        name = ke.name
        pass
        if name == 'a':
            pass

if __name__ == '__main__':
    vg = VisibleGame(5, 5)
    vg.draw()
    while True:
        print(list(map(str, vg.tail)), vg.fruitPos)
        vg.win.getMouse()
