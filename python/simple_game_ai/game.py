class Game:
    def __init__(self, width=3, height=3):
        self.width = width
        self.height = height
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.board[0][width - 1] = 2
        self.board[height - 1][0] = 1
        self.player_x = 0
        self.player_y = height - 1
        self.target_x = width - 1
        self.target_y = 0

    def return_state(self):
        flat = []
        for row in self.board:
            for x in row:
                flat.append(x)

        return flat

    def move_player(self, direction):
        distance = abs(self.target_x - self.player_x) + abs(self.target_x - self.player_y)

        # right
        if direction == 0 and self.player_x != self.width - 1:
            self.board[self.player_y][self.player_x] = 0
            self.player_x += 1
            self.board[self.player_y][self.player_x] = 1

        # up
        if direction == 1 and self.player_y != 0:
            self.board[self.player_y][self.player_x] = 0
            self.player_y -= 1
            self.board[self.player_y][self.player_x] = 1

        # left
        if direction == 2 and self.player_x != 0:
            self.board[self.player_y][self.player_x] = 0
            self.player_x -= 1
            self.board[self.player_y][self.player_x] = 1

        # down
        if direction == 3 and self.player_y != self.height - 1:
             self.board[self.player_y][self.player_x] = 0
             self.player_y += 1
             self.board[self.player_y][self.player_x] = 1

        new_distance = abs(self.target_x - self.player_x) + abs(self.target_x - self.player_y)
        reward = distance - new_distance
        if self.check_target():
            reward = 10
        elif reward == -1:
            reward = -2
        elif reward == 0:
            reward == -1:

        # print(reward, self.return_state(), self.check_target())
        return reward, self.return_state(), self.check_target()

    def check_target(self):
        return self.player_x == self.target_x and self.player_y == self.target_y

game = Game()
# right, then left
game.move_player(0)
game.move_player(2)
# up, then down
game.move_player(1)
game.move_player(3)
# win: up x3, right x3
game.move_player(1)
game.move_player(1)
game.move_player(0)
game.move_player(0)
