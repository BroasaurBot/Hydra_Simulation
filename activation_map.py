import numpy as np


class ActivationMap():

    def __init__(self, dim, pos, size):
        self.map = np.zeros(dim)
        self.pos = pos
        self.size = size

    def set_map(self, map):
        self.map = map

    def reset_map(self):
        self.map = np.zeros(self.map.shape)

    def change_map(self, x, y, value):
        self.map[x][y] += value
        if abs(self.map[x][y]) > 1:
            self.map[x][y] = 1 if self.map[x][y] > 0 else -1

    def save_map(self, path):
        with open(path, "w") as f:
            line = ""
            for i in range(self.map.shape[1]):
                for j in range(self.map.shape[0]):
                    line += str(self.map[j][i]) + ","
            line = line[:-1]
            line += "\n"
            f.write(line)
    
    def load_map(self, path):
        with open(path, "r") as f:
            lines = f.readline().strip().split(",")
            for i in range(self.map.shape[1]):
                for j in range(self.map.shape[0]):
                    self.map[j][i] = float(lines[i * self.map.shape[0] + j])
                    

    def draw(self, display):
        for i in range(self.map.shape[0]):
            for j in range(self.map.shape[1]):
                r_amount = np.clip(255 if self.map[i][j] < 0 else -abs(self.map[i][j]) * 255 + 255, 0, 255)
                g_amount = np.clip(255 if self.map[i][j] > 0 else -abs(self.map[i][j]) * 255 + 255, 0, 255)
                b_amount = np.clip(-abs(self.map[i][j]) * 255 + 255, 0 , 255)
                display.draw_circle((self.pos[0] + j*(self.size + 5), self.pos[1] + i*self.size), self.size/2, (r_amount, g_amount, b_amount), thickness=0)
                display.draw_circle((self.pos[0] + j*(self.size + 5), self.pos[1] + i*self.size), self.size/2, (0, 0, 0), thickness=1)

    def mouse(self, pos, amount):
        x, y = pos
        x -= self.pos[0] - self.size / 2
        y -= self.pos[1] - self.size / 2
        j = int(x / (self.size + 5))
        i = int(y / (self.size))
        if (i >= 0 and i < self.map.shape[0] and j >= 0 and j < self.map.shape[1]):
            self.change_map(i, j, amount)
