from PIL import Image
import numpy as np
from collections import deque


class Robot:
    right = (1, 0)
    left = (-1, 0)
    up = (0, -1)
    down = (0, 1)

    def __init__(self, start_position: np.array, target_position: np.array, battery_charge: float, max_speed: float):
        if battery_charge == -1:
            battery_charge = float("inf")

        self.target_position = tuple(target_position)
        self.battery_charge = battery_charge
        self.position = np.array(start_position)
        self.max_speed = max_speed
        self.blind_search_mode = True

        self.yet_to_visit = deque()
        self.visited = set()
        self.visible = dict()

        self.move = [[-1, 0], [0, -1], [1, 0], [0, 1]]

        self.bfs_way = deque()

    def step(self, current_position: np.array, camera_image: Image):
        current_position = tuple(current_position)
        half_camera_shape = (camera_image.shape[0] // 2, camera_image.shape[1] // 2)
        for x in range(-half_camera_shape[0], half_camera_shape[0] + 1):
            for y in range(-half_camera_shape[1], half_camera_shape[1] + 1):
                self.visible[(current_position[0] + x, current_position[1] + y)] \
                    = camera_image[y + half_camera_shape[1], x + half_camera_shape[0]]
        self.visited.add(current_position)
        try:
            self.yet_to_visit.remove(current_position)
        except ValueError:
            pass

        self.calibrate_move()
        for vector in self.move:
            child = tuple(current_position + np.array(vector))
            if camera_image[vector[1] + half_camera_shape[0]][vector[0] + half_camera_shape[1]] == 0 \
                    and child not in self.visited:
                self.yet_to_visit.append(child)

        if self.target_position == current_position:
            return 0, 0

        if self.blind_search_mode or len(self.bfs_way) == 0:
            self.blind_search_mode = True
            direction = self.blind_search(current_position)
        else:
            direction = self.bfs_step(current_position)

        return direction

    def blind_search(self, current_position):
        direction = np.array(self.move[-1])
        pos = self.yet_to_visit.pop()
        self.bfs_way = deque( self.bfs(tuple(pos), tuple(current_position))[1:] )
        if len(self.bfs_way) > 0:
            direction = self.bfs_step(current_position)
            self.blind_search_mode = False
        return direction

    def bfs_step(self, current_position):
        target_position = np.array(self.bfs_way.popleft())
        return target_position - current_position

    def calibrate_move(self):
        # if current_position[1] > self.target_position[1]:
        #    self.move = (Robot.left, Robot.down, Robot.right, Robot.up)
        # else:
        #    self.move = (Robot.left, Robot.up, Robot.right, Robot.down)
        pass

    def bfs(self, start, goal):
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break

            for next_node in self.get_next_nodes(cur_node):
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node

        path_segment = goal
        path = []
        while path_segment in visited:
            path.append(path_segment)
            path_segment = visited[path_segment]
        return path

    def get_next_nodes(self, pos):
        next_nodes = []
        for dx, dy in self.move:
            node = (pos[0] + dx, pos[1] + dy)
            if node in self.visible and self.visible[node] == 0:
                next_nodes.append(node)
        return next_nodes

