import pygame as pg
from random import random
from collections import deque

pg.init()


class World:
    def __init__(self, map_size, tile, robots, camera_view_radius=1):
        self.map_size = map_size
        self.tile = tile
        self.sc = pg.display.set_mode((map_size[0] * tile, map_size[1] * tile))
        self.clock = pg.time.Clock()

        # grid
        self.grid = [[1 if random() < 0.2 else 0 for col in range(map_size[0])] for row in range(map_size[1])]
        for x in range(0, self.map_size[0]):
            self.grid[x][0] = 1
            self.grid[x][self.map_size[1]-1] = 1
        for y in range(1, self.map_size[1]-1):
            self.grid[0][y] = 1
            self.grid[self.map_size[0]-1][y] = 1
        # dict of adjacency lists
        self.graph = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

        # BFS settings
        self.camera_view_radius = camera_view_radius
        self.visited = set()
        self.robots = robots

    def run(self):
        running = True
        while running:
            # fill screen
            self.sc.fill(pg.Color('black'))

            for robot in self.robots:
                vector = robot.step(robot.position,
                                    self.get_camera_view(robot.position, self.camera_view_radius))
                robot.position[0] += vector[0]
                robot.position[1] += vector[1]

                # visible map
                x_border = self.get_border_camera(robot.position, 0)
                y_border = self.get_border_camera(robot.position, 1)
                for x in range(x_border[0], x_border[1]):
                    for y in range(y_border[0], y_border[1]):
                        self.visited.add((x, y))

            # draw BFS work
            [pg.draw.rect(self.sc, pg.Color('forestgreen'), self.get_rect(x, y)) for x, y in self.visited]
            for robot in self.robots:
                pg.draw.rect(self.sc, pg.Color('blue'), self.get_rect(*robot.position),
                             border_radius=self.tile // 3)
            # draw grid
            [[pg.draw.rect(self.sc, pg.Color('darkorange'), self.get_rect(x, y), border_radius=self.tile // 5)
              for x, col in enumerate(row) if col] for y, row in enumerate(self.grid)]

            # draw path
            # pygame necessary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(1)
        pg.quit()

    def get_rect(self, x, y):
        return x * self.tile + 1, y * self.tile + 1, self.tile - 2, self.tile - 2

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1] and not self.grid[y][x]
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def get_border_camera(self, position, axis):
        border = [position[axis] - self.camera_view_radius,
                  position[axis] + self.camera_view_radius + 1]
        if border[0] < 0:
            border[0] = 0
        if border[1] > self.map_size[axis]:
            border[1] = self.map_size[axis]
        return border

    def get_camera_view(self, position, camera_radius):
        view_grid = [None] * (camera_radius * 2 + 1)
        for i in range(0, camera_radius + 2):
            view_grid[i] = self.grid[position[1] - 1 + i][position[0]-camera_radius:position[0]+camera_radius+1]
        return view_grid
