import unittest
from game import *
class TestSnake(unittest.TestCase):
    def setUp(self):
        self.g = Game(5,5)
        g = self.g
        g.tail = [Vector(0,0)]
        g.fruitPos = Vector(2,0)
    
    def test_init(self):
        self.assertEqual(self.g.tail, [Vector(0,0)])
        self.assertEqual(self.g.fruitPos, Vector(2,0))
        self.assertEqual(self.g.tailLength, 1)
    def test_fruit_eat(self):
        g = self.g
        g.move_player(1)
        g.move_player(1) # eats fruit
        self.assertEqual(g.tail, [Vector(2,0)])
        self.assertEqual(g.tailLength, 2)
        self.assertNotEqual(g.fruitPos, Vector(2,0))
        g.fruitPos = Vector(0,0) # keep it out of the way
        g.move_player(4)
        self.assertEqual(g.tail, [Vector(2,0), Vector(2,1)])
        self.assertEqual(g.tailLength, 2)
        g.move_player(4)
        self.assertEqual(g.tail, [Vector(2,1), Vector(2,2)])
        self.assertEqual(g.tailLength, 2)

if __name__ == '__main__':
    unittest.main()