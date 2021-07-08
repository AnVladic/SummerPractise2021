from PIL import Image
import numpy as np
from collections import deque


class Robot:
    def __init__(self, start_position: np.array, target_position: np.array, battery_charge: float, max_speed: float):
        if battery_charge == -1:
            battery_charge = float("inf")

        self.target_position = target_position
        self.battery_charge = battery_charge
        self.position = np.array(start_position)
        self.max_speed = max_speed

        self.yet_to_visit = deque()
        self.visited = set()
        self.visible = set()

        self.move = np.array([[-1, 0], [0, -1], [1, 0], [0, 1]])

    def step(self, current_position: np.array, camera_image: Image):
        current_position = np.array(current_position)
        camera_image = np.array(camera_image)
        for x in range(-(camera_image.shape[0] // 2), camera_image.shape[0] // 2 + 1):
            for y in range(-(camera_image.shape[1] // 2), camera_image.shape[1] // 2 + 1):
                self.visible.add((current_position[0] + x, current_position[1] + y))
        self.visited.add(tuple(current_position))
        try:
            self.yet_to_visit.remove(current_position)
        except ValueError:
            pass

        direction = np.array([1, 0])

        for vector in self.move:
            child = tuple(current_position + vector)
            if camera_image[vector[1] + 1][vector[0] + 1] == 0 and child not in self.visited:
                self.yet_to_visit.append(np.array(child))

        if camera_image[direction[1] + 1][direction[0] + 1] == 1 or tuple(current_position + direction) in self.visited:
            pos = self.yet_to_visit.pop()
            #print(current_position, self.bfs(tuple(pos), tuple(current_position)))
            direction = np.array(pos) - current_position

        return direction

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
        return [(pos[0] + dx, pos[1] + dy) for dx, dy in self.move if (pos[0] + dx, pos[1] + dy) in self.visible]

