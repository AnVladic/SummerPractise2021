from PIL import Image
import numpy as np


class Robot:
    def __init__(self, start_position: np.array, target_position: np.array, battery_charge: float, max_speed: float):
        if battery_charge == -1:
            battery_charge = float("inf")

        self.target_position = target_position
        self.battery_charge = battery_charge
        self.position = start_position
        self.max_speed = max_speed

    def step(self, current_position: np.array, camera_image: Image):
        print(camera_image)
        return (1, 0)

