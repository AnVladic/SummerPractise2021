import pygame as pg
import numpy as np
from random import random

pg.init()


class World:
    def __init__(self, map_size, tile, robots, camera_view_radius=1):
        self.map_size = map_size
        self.tile = tile
        self.sc = pg.display.set_mode((map_size[0] * tile, map_size[1] * tile))
        self.clock = pg.time.Clock()

        # grid
        self.grid = np.array([[1 if random() < 0.2 else 0 for col in range(map_size[0])] for row in range(map_size[1])])
        for x in range(0, self.map_size[0]):
            self.grid[x][0] = 1
            self.grid[x][self.map_size[1] - 1] = 1
        for y in range(1, self.map_size[1] - 1):
            self.grid[0][y] = 1
            self.grid[self.map_size[0] - 1][y] = 1

        # BFS settings
        self.camera_view_radius = camera_view_radius
        self.robots = robots
        self.direction = np.array([0, 0])
        self.way = set()

    def run(self):
        running = True
        while running:
            # fill screen
            self.sc.fill(pg.Color('black'))

            for robot in self.robots:
                # draw BFS work
                for x, y in robot.visible:
                    color = 'forestgreen'
                    if robot.visible[(x, y)] == 1:
                        color = 'red'
                    pg.draw.rect(self.sc, pg.Color(color), self.get_rect(x, y))

                # draw way
                [pg.draw.rect(self.sc, pg.Color('LIGHTGREEN'), self.get_rect(x, y)) for x, y in self.way]

                pg.draw.rect(self.sc, pg.Color('blue'), self.get_rect(*robot.position),
                             border_radius=self.tile // 3)

                robot.position += self.direction
                self.way.add(tuple(robot.position))
                self.direction = robot.step(robot.position,
                                            self.get_camera_view(robot.position, self.camera_view_radius))

                pg.draw.rect(self.sc, pg.Color('PURPLE'),
                             self.get_rect(robot.target_position[0], robot.target_position[1]),
                             border_radius=self.tile // 5)

            # draw grid
            [[pg.draw.rect(self.sc, pg.Color('darkorange'), self.get_rect(x, y), border_radius=self.tile // 5)
              for x, col in enumerate(row) if col] for y, row in enumerate(self.grid)]

            # draw path
            # pygame necessary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(7)
        pg.quit()

    def get_rect(self, x, y):
        return x * self.tile + 1, y * self.tile + 1, self.tile - 2, self.tile - 2

    def get_border_camera(self, position, axis):
        border = [position[axis] - self.camera_view_radius,
                  position[axis] + self.camera_view_radius + 1]
        if border[0] < 0:
            border[0] = 0
        if border[1] > self.map_size[axis]:
            border[1] = self.map_size[axis]
        return border

    def get_camera_view(self, position, camera_radius):

        grid = np.ones((self.grid.shape[0] + camera_radius * 2, self.grid.shape[1] + camera_radius * 2))
        grid[camera_radius:camera_radius+self.grid.shape[0], camera_radius:camera_radius+self.grid.shape[1]] = self.grid
        view_grid = grid[position[1]:position[1] + camera_radius * 2 + 1,
                         position[0]:position[0] + camera_radius * 2 + 1]
        return view_grid
