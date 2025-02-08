import json
from utils.update_utils import get_haps_position, update_affiliated, update_haps_number
import os


def get_history_info(time, haps_system, covered_number, position, data_path):
    history_info = dict()
    history_info[time] = {}
    for key in position.keys():
        history_info[time][key] = {}
        history_info[time][key]["position"] = position[key].tolist()
        history_info[time][key]["radius_km"] = haps_system[key].radius
        history_info[time][key]["users_covered"] = covered_number[key]


    if os.path.getsize(data_path) == 0:
        data = {}
    else:
        with open(data_path, "r") as file:
            data = json.load(file)
    data.update(history_info)
    with open(data_path, "w") as file:
        json.dump(data, file, indent=4)

def get_history_decision(current_decision, data_path):
    if os.path.getsize(data_path) == 0:
        data = {}
    else:
        with open(data_path, "r") as file:
            data = json.load(file)
    data.update(current_decision)
    with open(data_path, "w") as file:
        json.dump(data, file, indent=4)

def get_current_state(time, haps_system, position):
    current_state = dict()
    current_state[time] = {}
    for key in position.keys():
        current_state[time][key] = {}
        current_state[time][key]["current_position"] = position[key].tolist()
        current_state[time][key]["radius_km"] = haps_system[key].radius
        current_state[time][key]["speed"] = haps_system[key].velocity
        current_state[time][key]["users_covered"] = haps_system[key].UserNumber
    return current_state







