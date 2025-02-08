import math
import numpy as np


class User:
    def __init__(self, position, name, movement_flag):
        """
        Initializes the user model

        :param position: Initial position (x, y)
        """
        self.name = name
        self.position = np.array(position)
        self._distances = {}
        self.affiliated = "None"
        self.movement_flag = movement_flag

    def update_position(self, time, angle, speed):
        time = time / 3600
        if self.movement_flag==1:
            dx = speed * np.cos(angle) * time
            dy = speed * np.sin(angle) * time
            self.position[0] += dx
            self.position[1] += dy
            self.position[0] = np.clip(self.position[0], 0, 1000)
            self.position[1] = np.clip(self.position[1], 0, 1000)


    def get_position(self):
        return self.position

    def get_affiliated(self, haps_system):
        """
        Determine the user's membership.

        :param haps_system: HAPS_system dictionary
        :return:affiliation
        """
        points = []
        radius = {}
        for i in range(len(haps_system)):
            points.append(haps_system[f"HAPS{i}"].position)
            radius[f"HAPS{i}"] = haps_system[f"HAPS{i}"].radius
        for i in range(len(haps_system)):
            self._distances[f"HAPS{i}"] = math.sqrt((self.position[0] - points[i][0]) ** 2 + (self.position[1] - points[i][1]) ** 2)
        min_distance = float("inf")
        self.affiliated = "None"
        for key, value in self._distances.items():
            if value < min_distance and radius[key] >= value:
                min_distance = value
                self.affiliated = key
        return self.affiliated




