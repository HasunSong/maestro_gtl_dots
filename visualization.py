# %%
import matplotlib.pyplot as plt


def plot_points(title, subplot_nums, field_size, point_lst, n_group):
    plt.subplot(subplot_nums[0], subplot_nums[1], subplot_nums[2])
    plt.xlim([0, field_size[0]])
    plt.ylim([0, field_size[1]])
    plt.title(title)
    for point in point_lst:
        marker = "o"
        if point.type == "center":
            marker = "x"
        elif point.type == "free":
            marker = "^"
        color = point.group / n_group
        plt.scatter(point.x, point.y, color=str(color), marker=marker)
