import time, os
import numpy as np
from utils.init_utils import init_haps, init_users
from utils.transform_llmoutput import get_current_decision
from utils.update_utils import update_affiliated, update_haps_number, update_haps_position, update_user_position
from datetime import datetime, timedelta
from Agent_enhance.Agents_interaction.Agent_HAPS import Agent_HAPS, Agent_analysis, Agent_overlap, Agent_event
from utils.graph_utils import get_data_graph_single, get_data_graph_global, get_gif_single, get_gif_single_new, save_data_single, save_data_global


os.environ["OPENAI_API_KEY"] = "YOUR_API_KEY"


# 初始化模型
model_name = 'gpt-4o-mini'
model_name_fine_tuning = 'ft:gpt-4o-mini-2024-07-18:li:haps-llm:ATqY0j9Y'    # Your fine-tuning model name
HAPS_Agent = Agent_HAPS(model_name_fine_tuning)
# HAPS_Agent = Agent_HAPS(model_name)
HAPS_analyst = Agent_analysis(model_name)
HAPS_overlap = Agent_overlap(model_name)
HAPS_event = Agent_event(model_name)
path_info_history = "data/info_history.json"    # Number of overwritten users corresponding to the historical location
path_decision_history = "data/decision_history.json"     # Store history decision
event_flag = 0   # Whether there are special events
if event_flag:
    path_event = "data/with_event.txt"
else:
    path_event = "data/without_event.txt"


with open(path_info_history, "w") as file:
    file.write("")
with open(path_decision_history, "w") as file:
    file.write("")

# Initialize HAPS
init_position = [[0, 750], [500, 900], [250, 200], [950, 50]]
HAPS_system = init_haps(init_position)

# Initialize Users
np.random.seed(20)
x_floats = np.random.uniform(300, 900, 500)
y_floats = np.random.uniform(0, 1000, 500)
Users_group = init_users(x_floats, y_floats)


total_time = 1*24*3600
# current_time = 0
step_time = 300
step_decision = 3600
decision_count = 0
start_time = datetime(2025, 3, 3, 0, 0, 0)
current_time = datetime(2025, 3, 3, 0, 0, 0)
cycle_time = datetime(2025, 3, 3, 0, 0, 0)
graph_time = start_time
graph_sign = 1

target_position = []
position_problem = []
images = []
time_index = [current_time]
update_affiliated(Users_group, HAPS_system)
update_haps_number(HAPS_system, Users_group)
haps_user_number_single = np.array([HAPS_system[f"HAPS{i}"].UserNumber for i in range(len(HAPS_system))]).reshape(1, 4)
haps_user_number_global = np.array([HAPS_system[f"HAPS{i}"].UserNumber for i in range(len(HAPS_system))]).reshape(1, 4).sum()

while True:
    cycle_time = current_time

    if int((current_time-start_time).total_seconds()) == step_decision*decision_count:
        decision_count += 1
        start = time.time()

        # 执行决策,生成数据
        # time.sleep(5)
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

        target_position = []
        target_info = get_current_decision(formatted_time, HAPS_system, Users_group, HAPS_Agent, HAPS_analyst, HAPS_overlap, HAPS_event, path_info_history, path_decision_history, path_event)
        for key, value in target_info[formatted_time].items():
            target_position.append(value["target_position"])

        # target_position = position_problem

        print("target_position:", target_position)

        end = time.time()
        elapsed_time = round((end - start), 0)

        # time
        current_time += timedelta(seconds=elapsed_time)

    # 时间更变
    current_time += timedelta(seconds=step_time)
    if int((current_time-start_time).total_seconds()) > step_decision*decision_count:
        current_time = start_time + timedelta(seconds=step_decision*decision_count)

    # 更新信息：飞行位置、（用户位置、）用户隶属、覆盖个数
    update_haps_position(HAPS_system, target_position, (current_time-cycle_time).total_seconds())
    update_user_position(Users_group, (current_time-cycle_time).total_seconds())
    update_affiliated(Users_group, HAPS_system)
    update_haps_number(HAPS_system, Users_group)
    position_problem = target_position

    # 数据生成
    haps_user_number_single = np.append(haps_user_number_single,
                                      np.array([HAPS_system[f"HAPS{j}"].UserNumber for j in range(len(HAPS_system))]).reshape(
                                          1,
                                          4),
                                      axis=0)
    haps_user_number_global = np.append(haps_user_number_global,
                                      np.array([HAPS_system[f"HAPS{j}"].UserNumber for j in range(len(HAPS_system))]).reshape(
                                          1,
                                          4).sum())

    # if int((current_time-graph_time).total_seconds()) > 3600*6:
    #     graph_time = current_time
    #     graph_sign = 1
    event_graph = 0
    if 3600*6 < int((current_time - start_time).total_seconds()) < 3600*15 and event_flag:
        event_graph = 1
    if int((current_time-graph_time).total_seconds()) > 3600*6:
        graph_time = current_time
        graph_sign = 1
    x = get_gif_single_new(HAPS_system, Users_group, current_time, graph_sign, event_graph)
    graph_sign = 0
    images.append(x)
    time_index.append(current_time)

    if (current_time-start_time).total_seconds() > total_time:
        get_gif_single(HAPS_system, Users_group, current_time)
        break

# 绘制图片
images[0].save('result/CoverageMap/Agent_gif.gif', save_all=True, append_images=images[1:], duration=50, loop=0)
get_data_graph_single('result/LineChart/single_coverage.png', haps_user_number_single, time_index)
get_data_graph_global(haps_user_number_global, time_index)

save_data_global("result/LineChart/global_LLM.csv", time_index, haps_user_number_global)
save_data_single("result/LineChart/single.csv", time_index, haps_user_number_single)



