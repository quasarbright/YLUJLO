import random
from graphics import *
import keyboard
import time
import p5


class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, other):
        self.x += other.x
        self.y += other.y

    def copy(self):
        return Vector(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other):
        if type(self) is not type(other):
            raise TypeError(str(type(other)))
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        if type(self) is not type(other):
            raise TypeError(str(type(other)))
        return Vector(self.x - other.x, self.y - other.y)

    def __str__(self):
        return '<{}, {}>'.format(self.x, self.y)

    def __repr__(self):
        return str(self)


class Game:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        startingHead = Vector(random.randint(0, width//2),
                              random.randint(0, height-1))
        self.tail = [startingHead]  # list of vectors, from tail to head
        self.tailLength = len(self.tail)
        self.fruitPos = Vector()
        self.spawn_fruit()
        self.direction = 0  # can be 0, 1, 2, 3
        self.dead = False
        self.age = 0
        self.score = 0  # fruits eaten

    def spawn_fruit(self):
        self.fruitPos = Vector(random.randint(
            0, self.width-1), random.randint(0, self.height-1))
        while self.fruitPos in self.tail:
            self.fruitPos = Vector(random.randint(
                0, self.width-1), random.randint(0, self.height-1))

    def is_in_bounds(self, p):
        '''
        is vector p in bounds?
        '''
        return p.x >= 0 and p.x < self.width and p.y >= 0 and p.y < self.height

    def is_eating_tail(self, p):
        '''
        is vector somewhere in the tail?
        '''
        return p in self.tail[0:-1]

    def return_state(self):
        '''
        return representation as a 1D list: distance from head to nearest object in all
        4 directions, and x and y distance to the fruit
        '''
        # save snake's head vector
        head = self.tail[-1]
        # for both of these lists, they're in the order right, up, left, down
        # is there an obstacle adjacent in this direction?
        danger = [0 for _ in range(4)]
        offs = [Vector(1, 0), Vector(0, -1), Vector(-1, 0),
                Vector(0, 1)]  # offsets of position
        for i, off in enumerate(offs):
            newPos = head + off
            if self.is_eating_tail(newPos) or not self.is_in_bounds(newPos):
                danger[i] = 1  # you'll die if you go that way

        direction = [0 for _ in range(4)]
        direction[self.direction] = 1

        fruit = [0 for _ in range(4)]
        toFruit = self.fruitPos - head
        if toFruit.x > 0:
            fruit[0] = 1
        elif toFruit.x < 0:
            fruit[2] = 1
        if toFruit.y > 0:
            fruit[3] = 1  # fruit is below
        elif toFruit.y < 0:
            fruit[1] = 1

        return [*danger, *direction, *fruit]  # bunch of 1s and 0s, size of 12

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
            return 0
            oldDistance = abs(oldHead.x - oldFruit.x) + \
                abs(oldHead.y - oldFruit.y)
            newDistance = abs(newHead.x - newFruit.x) + \
                abs(newHead.y - newFruit.y)
            return oldDistance - newDistance

    def move_player(self, newDirection):
        '''
        direction is 0, 1, 2, or 3, or 4
        nothing, right, up, left, down
        '''
        # assert newDirection in [0,1,2,3,4]
        if not self.dead:
            # save snake's head vector
            head = self.tail[-1]

            # no change: make newDirection the previous direction
            if newDirection == 4:
                newDirection = self.direction

            # go right, up, left, or down
            newPosition = Vector(-1, -1)
            if newDirection == 0:
                newPosition = Vector(head.x + 1, head.y)
            elif newDirection == 1:
                newPosition = Vector(head.x, head.y - 1)
            elif newDirection == 2:
                newPosition = Vector(head.x - 1, head.y)
            elif newDirection == 3:
                newPosition = Vector(head.x, head.y + 1)
            # only move the snake if it's not about to go out of bounds
            if self.is_in_bounds(newPosition) and not self.is_eating_tail(newPosition):
                self.tail.append(newPosition)
            else:
                self.dead = True
            # update direction
            self.direction = newDirection

            # remove end of tail if didn't eat
            if len(self.tail) > self.tailLength and not self.dead:
                self.tail.pop(0)

            # spawn a new fruit if it ate
            ate = self.tail[-1] == self.fruitPos
            oldFruit = self.fruitPos.copy()
            # increment tail length if it ate
            if ate:
                self.tailLength += 1
                self.spawn_fruit()
                self.score += 1
            self.age += 1

            # check if you've died
            self.dead = self.dead or self.is_eating_tail(
                self.tail[-1]) or not self.is_in_bounds(self.tail[-1])

            # calculate reward
            reward = self.reward(
                head, oldFruit, self.tail[-1], self.fruitPos, ate, self.dead)

            # check state
            state = self.return_state()

            return reward, state, self.dead

    def copy(self):
        ans = Game(self.width, self.height)
        ans.width = self.width
        ans.height = self.height
        ans.tail = [v.copy() for v in self.tail]
        ans.tailLength = self.tailLength
        ans.fruitPos = self.fruitPos.copy()
        ans.direction = self.direction
        ans.dead = self.dead
        ans.age = self.age
        ans.score = self.score
        return ans

    def check_move(self, newDirection):
        g = self.copy()
        return g.move_player(newDirection)

    def best_move(self):
        def key(newDirection):
            reward, state, dead = self.check_move(newDirection)
            return reward
        return max(range(5), key=key)

    def status(self):
        return 'age: {}, score: {}'.format(self.age, self.score)


class VisibleGame(Game):
    '''
    a game that is rendered on screen
    '''

    def __init__(self, *args, run=True, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_width = 250
        self.window_height = 250
        self.rect_width = self.window_width / self.width
        self.rect_height = self.window_height / self.height
        if run:
            p5.run(self.setup, self.draw, 5)

    def setup(self):
        p5.size(self.window_width, self.window_height)
        p5.background(0)
        p5.no_loop()

    def draw_rectangle_at(self, r, c, color):
        p1 = Vector(c*self.rect_width, r*self.rect_height)
        p2 = Vector((c+1)*self.rect_width, (r+1)*self.rect_height)
        p5.fill(*color)
        p5.rect((p1.x, p1.y), self.rect_width, self.rect_height)

    def draw_background(self):
        p5.background(52)

    def draw_tail(self):
        for position in self.tail:
            c = position.x
            r = position.y
            self.draw_rectangle_at(r, c, (255,))

    def draw_fruit(self):
        c = self.fruitPos.x
        r = self.fruitPos.y
        self.draw_rectangle_at(r, c, (255,0,0))

    def draw(self):
        print(random.randint(0, 1))
        print(self.direction)
        self.draw_background()
        self.draw_tail()
        self.draw_fruit()

class PlayableGame(VisibleGame):
    def __init__(self, *args, **kwargs):
        keyboard.on_press(self.key_listener)
        self.keyQueue = []
        super().__init__(*args, **kwargs)

    def key_listener(self, ke):
        self.keyQueue.append(ke.name)

    def handle_keypress(self, name):
        if name == 'd' or name == 'right':
            self.move_player(0)
        elif name == 'w' or name == 'up':
            self.move_player(1)
        elif name == 'a' or name == 'left':
            self.move_player(2)
        elif name == 's' or name == 'down':
            self.move_player(3)
        else:
            self.move_player(4)

    def update(self):
        if self.keyQueue == []:
            self.handle_keypress('')
        for i in range(len(self.keyQueue)):
            self.handle_keypress(self.keyQueue.pop(0))
    
    def draw(self):
        self.update()
        super().draw()




if __name__ == '__main__':
    global vg
    vg = PlayableGame(10, 10)