class GameWorld:
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
        return self.board

    def move_player(self, direction):
        distance = abs(self.target_x - self.player_x) + abs(self.target_x - self.player_y)

        # left
        if direction == 0 and self.player_x != 0:
            self.board[self.player_y][self.player_x] = 0
            self.player_x -= 1
            self.board[self.player_y][self.player_x] = 1

        # up
        if direction == 1 and player_y != 0:
            self.board[self.player_y][self.player_x] = 0
            self.player_y -= 1
            self.board[self.player_y][self.player_x] = 1

        # right
        if direction == 2 and player_x != width - 1:
            self.board[self.player_y][self.player_x] = 0
            self.player_x += 1
            self.board[self.player_y][self.player_x] = 1

        # down
        if direction == 3 and player_y != height - 1:
             self.board[self.player_y][self.player_x] = 0
             self.player_y += 1
             self.board[self.player_y][self.player_x] = 1

        new_distance = abs(self.target_x - self.player_x) + abs(self.target_x - self.player_y)
        reward = new_distance - distance

        return reward, return_state(self), check_target(self)


    def check_targert(self):
        return playerX == targetX and playerY == targetY
