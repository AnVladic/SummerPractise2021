import pygame as pg
from random import random
from collections import deque

pg.init()


class Visualization:
    def __init__(self, map_size, tile):
        self.map_size = map_size
        self.tile = tile
        self.sc = pg.display.set_mode((map_size[0] * tile, map_size[1] * tile))
        self.clock = pg.time.Clock()

        # grid
        self.grid = [[1 if random() < 0.2 else 0 for col in range(map_size[0])] for row in range(map_size[1])]
        # dict of adjacency lists
        self.graph = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

        # BFS settings
        self.start = (0, 0)
        self.queue = deque([self.start])
        self.visited = {self.start: None}
        self.cur_node = self.start

    def run(self):
        running = True
        while running:
            # fill screen
            self.sc.fill(pg.Color('black'))
            # draw grid
            [[pg.draw.rect(self.sc, pg.Color('darkorange'), self.get_rect(x, y), border_radius=self.tile // 5)
              for x, col in enumerate(row) if col] for y, row in enumerate(self.grid)]
            # draw BFS work
            [pg.draw.rect(self.sc, pg.Color('forestgreen'), self.get_rect(x, y)) for x, y in self.visited]
            [pg.draw.rect(self.sc, pg.Color('darkslategray'), self.get_rect(x, y)) for x, y in self.queue]

            # BFS logic
            if self.queue:
                cur_node = self.queue.popleft()
                next_nodes = self.graph[cur_node]
                for next_node in next_nodes:
                    if next_node not in self.visited:
                        self.queue.append(next_node)
                        self.visited[next_node] = cur_node

            # draw path
            path_head, path_segment = cur_node, cur_node
            while path_segment:
                pg.draw.rect(self.sc, pg.Color('white'), self.get_rect(*path_segment), self.tile,
                             border_radius=self.tile // 3)
                path_segment = self.visited[path_segment]
            pg.draw.rect(self.sc, pg.Color('blue'), self.get_rect(*self.start), border_radius=self.tile // 3)
            pg.draw.rect(self.sc, pg.Color('magenta'), self.get_rect(*path_head), border_radius=self.tile // 3)
            # pygame necessary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(7)
        pg.quit()

    def get_rect(self, x, y):
        return x * self.tile + 1, y * self.tile + 1, self.tile - 2, self.tile - 2

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: 0 <= x < self.map_size[0] and 0 <= y < self.map_size[1] and not self.grid[y][x]
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]
