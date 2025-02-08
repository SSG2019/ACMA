import numpy as np

def update_affiliated(users_group, haps_system):
    for i in users_group.values():
        i.get_affiliated(haps_system)

def update_haps_position(haps_system, target_p, time):
    for i in range(len(haps_system)):
        haps_system[f"HAPS{i}"].calculate_position(target_p[i], time)
    position = get_haps_position(haps_system)
    return position

def update_user_position(users_group, time):
    num_users = len(users_group)
    angles = np.random.uniform(0, 2 * np.pi, num_users)
    speeds = np.random.normal(5, 2, num_users)
    speeds = np.clip(speeds, 2, 8)
    for i in range(len(users_group)):
        users_group[f"User{i}"].update_position(time, angles[i], speeds[i])

def update_haps_number(haps_system, users_group):
    for i in haps_system.values():
        i.get_number(users_group)
    haps_number = {}
    for i in range(len(haps_system)):
        haps_number[f"HAPS{i}"] = haps_system[f"HAPS{i}"].UserNumber
    return haps_number

def get_haps_position(haps_system):
    position = {}
    for i in range(len(haps_system)):
        position[f"HAPS{i}"] = haps_system[f"HAPS{i}"].position
    return position

def get_users_position(users_group):
    position = []
    for i in range(len(users_group)):
        position.append(users_group[f"User{i}"].position)
    return position

def clamp(value, min_value, max_value):
    x = min(value, max_value)
    y = max(min_value, x)
    return y
