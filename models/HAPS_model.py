import numpy as np


class HAPS:
    def __init__(self, position, velocity, radius, name):
        """
        Initializes the HAPS class

        :param position: The initial position (x, y), Unit is kilometer
        :param velocity: velocity v, The unit is kilometers per hour
        """
        self.name = name
        self.velocity = velocity
        self.radius = radius
        self.position = np.array(position)
        self.UserNumber = 0

    def calculate_position(self, target_position, time):
        """
        Calculates the current position after the specified time.

        :param target_position: Target position (x, y), Unit is kilometer
        :param time: Time, in seconds
        :return: new position after the specified time (new x, new y)
        """
        # computed azimuth
        time = time/3600
        target_position = np.array(target_position)
        x_change = target_position[0] - self.position[0]
        y_change = target_position[1] - self.position[1]
        if x_change != 0 or y_change != 0:
            x_velocity = self.velocity * x_change / np.sqrt(x_change ** 2 + y_change ** 2)
            y_velocity = self.velocity * y_change / np.sqrt(x_change ** 2 + y_change ** 2)

            # Calculate the change in position
            delta_x = x_velocity * time
            delta_y = y_velocity * time

            # update location
            new_position_x = self.position[0] + delta_x
            new_position_y = self.position[1] + delta_y

            if x_change ** 2 < (new_position_x - self.position[0]) ** 2:
                new_position_x = target_position[0]
                new_position_y = target_position[1]

            new_position = np.array([new_position_x, new_position_y])

            self.position = new_position

    def calculate_position_dir(self, target_dir, time):
        """
        Calculates the current position after the specified time.

        :param target_dir: Target position (x, y), Unit is kilometer
        :param time: Time, in seconds
        :return: new position after the specified time (new x, new y)
        """
        # computed azimuth
        time = time/3600
        target_dir = np.array(target_dir)
        x_change = (target_dir[0]/np.sqrt(target_dir[0] ** 2 + target_dir[1] ** 2)) * time * self.velocity
        y_change = (target_dir[1]/np.sqrt(target_dir[0] ** 2 + target_dir[1] ** 2)) * time * self.velocity
        new_position_x = self.position[0] + x_change
        new_position_y = self.position[1] + y_change

        new_position = np.array([new_position_x, new_position_y])

        self.position = new_position

    def calculate_position_four_dir(self, target_four_dir, time):
        # computed azimuth
        time = time/3600
        target_dir = np.array(target_four_dir)
        new_position = np.array(self.position + target_dir * time * self.velocity)

        self.position = new_position

    def get_position(self):
        """
        Get current position

        :return: current position
        """
        return self.position

    def get_number(self, users):
        self.UserNumber = 0
        for i in range(len(users)):
            if self.name == users[f"User{i}"].affiliated:
                self.UserNumber += 1
        return self.UserNumber


