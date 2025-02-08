import json, os, time, re
from utils.transform_json import get_history_info, get_current_state, get_history_decision
from utils.update_utils import get_haps_position, update_affiliated, update_haps_number

def segment_output(text: str):
    _, after = text.split("```json")
    return after.split("```")[0]


def get_current_decision(timestamp, haps_system, users_group, haps_agent, haps_analyst, haps_overlap, haps_event, path_info_history, path_decision_history, path_event):
    # 更新信息
    position = get_haps_position(haps_system)
    update_affiliated(users_group, haps_system)
    covered_number = update_haps_number(haps_system, users_group)

    sorted_dict = list(dict(sorted(covered_number.items(), key=lambda item: item[1], reverse=True)).keys())
    airships_information = get_current_state(timestamp, haps_system, position)

    with open("config/analysis_template.txt", 'r', encoding='utf-8') as file:
        analysis_template = file.read()

    with open("config/template.json") as file:
        json_template = json.load(file)

    if os.path.getsize(path_info_history) == 0:
        info_history = {}
    else:
        with open(path_info_history, "r") as file:
            info_history = json.load(file)

    with open(path_event, 'r', encoding='utf-8') as file:
        event = file.read()

    current_decision = dict()
    current_decision[timestamp] = {}
    for i in range(len(haps_system)):
        current_decision[timestamp][f"HAPS{i}"] = {}

    analysis = haps_analyst.get_analysis(airships_information, info_history, analysis_template)

    for i in sorted_dict:
        try:
            decision = haps_agent.get_target(i, analysis, airships_information, current_decision,
                                             json_template)
            decision = json.loads(segment_output(decision))
            current_decision[timestamp][i] = decision
        except Exception as e:
            print("An error occurred:", e)
            time.sleep(0.1)

    while True:
        try:
            decision_new = haps_overlap.overlap_optimization_tools(current_decision)
            # print(decision_new)
            decision_new = segment_output(decision_new)
            # decision_new = re.sub(r"'(?=\w+:)|(?<=: )'", '"', decision_new)
            decision_new = json.loads(re.sub(r'//.*', '', decision_new))
            break
        except Exception as e:
            print("An error occurred:", e)
            time.sleep(0.1)

    current_time, = decision_new.keys()
    print(current_time)
    decision_final = haps_event.get_final(airships_information, decision_new, event, current_time)
    decision_final = segment_output(decision_final)  # .replace("'", '"')
    # decision_final = re.sub(r"'(?=\w+:)|(?<=: )'", '"', decision_final)
    decision_final = json.loads(re.sub(r'//.*', '', decision_final))
    print(decision_final)



    # print("a :", current_decision)
    # print("b :", decision_new)

    get_history_info(timestamp, haps_system, covered_number, position, path_info_history)
    get_history_decision(current_decision, path_decision_history)
    return decision_final

