# %%
import matplotlib.pyplot as plt


def plot_points(title, subplot_nums, field_size, point_lst, n_group):
    plt.subplot(subplot_nums[0], subplot_nums[1], subplot_nums[2])
    plt.xlim([0, field_size[0]])
    plt.ylim([0, field_size[1]])
    plt.title(title)
    for point in point_lst:
        if point.type == "center":
            marker = "x"
        elif point.type == "moon":
            marker = "^"
        elif point.type == "reversed moon":
            marker = "v"
        elif point.type == "free":
            marker = "o"
        color = point.group / n_group
        plt.scatter(point.x, point.y, color=str(color), marker=marker)


# standard_function.py에 있는 get_game_data 함수 잘 돌아가는지 확인하려고 임시로 만든 함수
def plot_game_data(game_data):
    figsize_x = 10
    figsize_y = 800 * 10 / 1800
    plt.figure(figsize=(figsize_x, figsize_y))
    for i in range(game_data['round_num']+1):
        plt.subplot(3, 4, i+1)
        plt.xlim([0, game_data['field_size'][0]])
        plt.ylim([0, game_data['field_size'][1]])
        if i == 0:
            plt.title(f"Init, Moved: 0")
        else:
            plt.title(f"Round: {i}, Moved: {game_data['movers'][i-1]}")
        x, y = [], []
        for coord in game_data['coord_record'][i]:
            x.append(coord[0])
            y.append(coord[1])
        plt.scatter(x, y)
    plt.show()