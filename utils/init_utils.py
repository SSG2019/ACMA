from models.HAPS_model import HAPS
from models.User_model import User
import numpy as np

# Initialize a certain number of HAPS
def init_haps(positions):
    haps = {}
    for i in range(len(positions)):
        haps[f"HAPS{i}"] = HAPS(positions[i], 40, 210, f"HAPS{i}")
    print(f"{len(haps)} HAPS were successfully initialized.")
    return haps

# Initialize a certain number of Users
def init_users(position_x, position_y):
    users = {}

    size = 500
    num_ones = 150
    num_zeros = size - num_ones
    list_data = [1] * num_ones + [0] * num_zeros
    np.random.shuffle(list_data)
    list_data = np.array(list_data)

    if len(position_x) == len(position_y):
        for i in range(len(position_x)):
            users[f"User{i}"] = User([position_x[i], position_y[i]], f"User{i}", list_data[i])
        print(f"{len(users)} Users were successfully initialized.")
        return users
    else:
        print("Input error")

