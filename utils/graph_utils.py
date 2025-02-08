import io, os, csv
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np
from fontTools.misc.symfont import green
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib.lines import Line2D
import matplotlib.dates as mdates

Picture_number = 0

def get_single_graph(haps_system, users_group):
    fig, ax = plt.subplots(figsize=(4, 4))
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1000)
    radius = 210
    labels = [f"HAP{i}" for i in range(len(haps_system))]
    x1 = []
    y1 = []
    x = []
    y = []
    for i in haps_system.values():
        center = i.position
        x1.append(center[0])
        y1.append(center[1])
        circle = plt.Circle(center, radius, edgecolor='blue', facecolor='none', linewidth=2)
        ax.scatter(center[0], center[1], color='green', s=70, marker='*')
        ax.add_patch(circle)
    for i, label in enumerate(labels):
        plt.text(x1[i], y1[i], label, fontsize=9, ha='center', va='top')
    for i in range(len(users_group)):
        x.append(users_group[f"User{i}"].position[0])
        y.append(users_group[f"User{i}"].position[1])
    ax.scatter(x, y, color='red', s=10)
    ax.grid(True)
    ax.set_aspect('equal')

    plt.show()

# def get_statistics(HAP_single, HAP_global):
#     for keys, values in HAP_single.items():

def get_data_graph_single(path, haps_user_number_single, time_index):
    plt.rc('font', family='Times New Roman')

    haps_one = haps_user_number_single[:, 0]
    haps_two = haps_user_number_single[:, 1]
    haps_three = haps_user_number_single[:, 2]
    haps_four = haps_user_number_single[:, 3]

    color1 = (0.556, 0.812, 0.788)
    color2 = (1.0, 0.745, 0.478)
    color3 = (0.980, 0.498, 0.435)
    color4 = (0.588, 0.765, 0.490)              #  (0.510, 0.690, 0.824)

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_ylim(0, 150)

    # time_index = time_index/3600

    ax.set_xlabel('Time', fontsize=8)
    ax.set_ylabel('Number of Covered Users', fontsize=8)
    ax.set_title('Coverage Performance of Single HAPS', fontsize=8)

    ax.plot(time_index, haps_one, marker='o', markevery=15, color=color1, label='HAPS0', markersize=4, linewidth=1.2)
    ax.plot(time_index, haps_two, marker='s', markevery=15, color=color2, label='HAPS1', markersize=4, linewidth=1.2)
    ax.plot(time_index, haps_three, marker='^', markevery=15, color=color3, label='HAPS2', markersize=4, linewidth=1.2)
    ax.plot(time_index, haps_four, marker='D', markevery=15, color=color4, label='HAPS3', markersize=4, linewidth=1.2)

    ax.set_yticks(np.arange(0, 141, 20))
    ax.grid(True, which='both', linestyle='--', linewidth=0.75, color='grey', alpha=0.5)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xticks(rotation=45)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.legend(loc='upper left', fontsize=8)
    plt.savefig(path, dpi=600, bbox_inches='tight', format='png')
    plt.show()
    plt.close(fig)

def graph_global_comparison(x_haps_llm, y_haps_llm, x_no_method, y_no_method, x_rl, y_rl, x_si, y_si, x_rl_all, y_rl_all):
    plt.rc('font', family='Times New Roman')
    # time_index = time_index/3600
    color1 = (0.843, 0.388, 0.392)
    color2 = (0.576, 0.580, 0.906)
    color3 = (0.373, 0.592, 0.824)
    color4 = (0.616, 0.765, 0.906)

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_ylim(0, 500)
    ax.set_xlabel('Time', fontsize=8)
    ax.set_ylabel('Number of Covered Users', fontsize=8)
    ax.set_title('Coverage Performance of All HAPS', fontsize=8)

    line1, = ax.plot(x_haps_llm, y_haps_llm, color=color1, label='Autonomous Coverage Multi-Agent', linewidth=1.2, marker='o', markevery=15, markersize=4)
    line2, = ax.plot(x_no_method, y_no_method, color=color2, label='Random Walk', linewidth=1.2, marker='s', markevery=15, markersize=4)
    line3, = ax.plot(x_rl, y_rl, color=color3, label='Reinforcement Learning', linewidth=1.2, marker='^', markevery=15, markersize=4)
    line4, = ax.plot(x_si, y_si, color=color4, label='Swarm Intelligence', linewidth=1.2, marker='D', markevery=15, markersize=4)
    ax.set_yticks(np.arange(0, 501, 50))
    ax.grid(True, which='both', linestyle='--', linewidth=0.75, color='grey', alpha=0.5)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())

    plt.xticks(rotation=45)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)

    ax_inset = inset_axes(ax, width="40%", height="22%", loc='upper right', borderpad=0.2)
    line5, = ax_inset.plot(x_rl_all, y_rl_all, color=color3, label='Reinforcement Learning',
                           linewidth=1.2, marker='^', markevery=100, markersize=4)
    # ax_inset.set_ylim(0, 500)
    ax_inset.set_yticks([100, 300, 500])
    ax_inset.tick_params(axis='x', labelsize=6)
    ax_inset.tick_params(axis='y', labelsize=6)

    ax_inset.set_xticks([x_rl_all[0], x_rl_all[-1]])
    ax_inset.text(
        0.5, 0.95,
        'Five-day simulation of Reinforcement \nLearning algorithm',
        fontsize=5.5,
        ha='center',
        va='top',
        transform=ax_inset.transAxes
    )
    # ax_inset.set_title('Reinforcement Learning', fontsize=6)

    lines = [line1, line2, line3, line4, Line2D([0], [0], color=color3, linewidth=1.2, marker='D', markersize=4)]
    labels = ['Autonomous Coverage Multi-Agent', 'Random Walk', 'Reinforcement Learning', 'Swarm Intelligence']
    ax.legend(lines, labels, loc='upper left', fontsize=8)
    plt.savefig('result_graph/comparison_coverage.png', dpi=600, bbox_inches='tight', format='png')
    plt.show()
    plt.close(fig)

def get_data_graph_global(hap_user_number_global, time_index):
    # time_index = time_index/3600
    plt.rc('font', family='Times New Roman')
    color1 = (0.843, 0.388, 0.392)

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.set_ylim(0, 500)
    ax.set_xlabel('Time', fontsize=8)
    ax.set_ylabel('Number of Covered Users', fontsize=8)
    ax.set_title('Coverage Performance of Global HAPS', fontsize=8)

    ax.plot(time_index, hap_user_number_global, color=color1, label='Autonomous Coverage Multi-Agent', linewidth=1.2, marker='o', markevery=15, markersize=4)

    plt.xticks(rotation=45)
    ax.tick_params(axis='x', labelsize=8)
    ax.tick_params(axis='y', labelsize=8)
    ax.legend(loc='upper left', fontsize=8)
    plt.savefig('result/LineChart/global_coverage.png', dpi=600, bbox_inches='tight', format='png')
    plt.show()
    plt.close(fig)

def get_gif_single(haps_system, users_group, time):
    global Picture_number

    plt.figure(figsize=(5.3, 5))
    plt.xlim(0, 1000)
    plt.ylim(0, 1000)
    plt.xlabel('kilometer')
    plt.ylabel('kilometer', labelpad=-5)

    stationary_users = []
    moving_users = []

    for key, value in users_group.items():
        if value.movement_flag == 0:
            stationary_users.append(value.position.tolist())
        elif value.movement_flag == 1:
            moving_users.append(value.position.tolist())


    moving_color = (1.0, 0.6, 0.6)
    stationary_color = (0.635, 0.655, 0.827)

    stationary_users = np.array(stationary_users)
    moving_users = np.array(moving_users)

    plt.scatter(moving_users[:, 0], moving_users[:, 1], c=[moving_color], label='Mobile user', s=30)
    plt.scatter(stationary_users[:, 0], stationary_users[:, 1], c=[stationary_color], label='Non-mobile user', s=15)

    plt.legend(loc="lower left", fontsize=8)

    haps_positions = []
    coverage_radius = []

    for key, value in haps_system.items():
        haps_positions.append(value.position)
        coverage_radius.append(value.radius)

    haps_labels = ['HAPS0', 'HAPS1', 'HAPS2', 'HAPS3']

    haps_color = (0.6, 0.741, 0.882)
    haps_alpha = 0.42

    for i, (x, y) in enumerate(haps_positions):
        plt.plot(x, y, marker='*', color='green', markersize=10)
        plt.text(x + 10, y + 10, haps_labels[i], fontsize=10)
        circle = plt.Circle((x, y), coverage_radius[i], color=haps_color, alpha=haps_alpha)
        plt.gca().add_patch(circle)

    plt.title(f'User Distribution and HAPS Coverage    {time}', fontsize=8)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(f'result/CoverageMap/{Picture_number}.png', bbox_inches='tight', dpi=600)


def get_gif_single_new(haps_system, users_group, time, graph_sign, event_flag):
    global Picture_number

    plt.figure(figsize=(5.3, 5))
    plt.xlim(0, 1000)
    plt.ylim(0, 1000)
    plt.xlabel('kilometer')
    plt.ylabel('kilometer', labelpad=-5)

    stationary_users = []
    moving_users = []

    if event_flag:
        if datetime(2025, 3, 3, 6, 0, 0) < time < datetime(2025, 3, 3, 15, 0, 0):
            icon = plt.imread('data/point.png')
            imagebox = OffsetImage(icon, zoom=0.04)
            ab = AnnotationBbox(imagebox, (50, 500), frameon=False)
            plt.gca().add_artist(ab)

    for key, value in users_group.items():
        if value.movement_flag == 0:
            stationary_users.append(value.position.tolist())
        elif value.movement_flag == 1:
            moving_users.append(value.position.tolist())

    moving_color = (1.0, 0.6, 0.6)
    stationary_color = (0.635, 0.655, 0.827)

    stationary_users = np.array(stationary_users)
    moving_users = np.array(moving_users)

    plt.scatter(moving_users[:, 0], moving_users[:, 1], c=[moving_color], label='Mobile user', s=30)
    plt.scatter(stationary_users[:, 0], stationary_users[:, 1], c=[stationary_color], label='Non-mobile user', s=15)

    plt.legend(loc="lower left", fontsize=8)

    haps_positions = []
    coverage_radius = []

    for key, value in haps_system.items():
        haps_positions.append(value.position)
        coverage_radius.append(value.radius)

    haps_labels = ['HAPS0', 'HAPS1', 'HAPS2', 'HAPS3']

    haps_color = (0.6, 0.741, 0.882)
    haps_alpha = 0.42

    for i, (x, y) in enumerate(haps_positions):
        plt.plot(x, y, marker='*', color='green', markersize=10)
        plt.text(x + 10, y + 10, haps_labels[i], fontsize=10)
        circle = plt.Circle((x, y), coverage_radius[i], color=haps_color, alpha=haps_alpha)
        plt.gca().add_patch(circle)

    plt.title(f'User Distribution and HAPS Coverage    {time}', fontsize=8)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    if graph_sign:
        plt.savefig(f'result/CoverageMap/{Picture_number}.png', bbox_inches='tight', dpi=600)
        Picture_number += 1
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    plt.close()
    return img

def save_data_single(path, x, y):
    combined_data = [[str(x)] + list(y) for x, y in zip(x, y)]

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "HAPS0", "HAPS1", "HAPS2", "HAPS3"])
        writer.writerows(combined_data)

def save_data_global(path, x, y):
    combined_data = [[str(x), y_val] for x, y_val in zip(x, y)]

    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "global"])
        writer.writerows(combined_data)

def read_data_single(file_path):
    data_x = []
    data_y = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            values = list(map(int, row[1:]))
            data_x.append(timestamp)
            data_y.append(values)

    data_y = np.array(data_y)
    return data_x, data_y

def read_data_global(file_path):
    data_x = []
    data_y = []

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            timestamp = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
            label = int(row[1])
            data_x.append(timestamp)
            data_y.append(label)

    data_y = np.array(data_y)
    return data_x, data_y



