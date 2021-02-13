# %%
from point import *
from visualization import *
from clusterer import *
from variation import *
import numpy as np

# %%
# 화면 크기
WIDTH = 1800
HEIGHT = 800

# 점들 초기화
point_list = []
for i in range(39):
    x = min(max(np.random.normal() * WIDTH / 4 + WIDTH / 2, 1), WIDTH-1)
    y = min(max(np.random.normal() * HEIGHT / 4 + HEIGHT / 2, 1), HEIGHT-1)
    new_point = Point(id=i, type="free", pos=(x, y))
    point_list.append(new_point)
# 랜덤하게 3번 움직인다.
update_points(point_list, (WIDTH, HEIGHT), 200)
update_points(point_list, (WIDTH, HEIGHT), 200)
update_points(point_list, (WIDTH, HEIGHT), 200)
# center, moon 설정
for i in range(len(point_list)):
    if i < 3:
        point_list[i].type = "center"
    else:
        point_list[i].type = "moon"


# figure 초기화
figsize_x = 10
figsize_y = HEIGHT * 10 / WIDTH
plt.figure(figsize=(figsize_x, figsize_y))

# 초기 상태에서 군집화 및 plot
n_group = cluster_points(point_list)
plot_points("init", (3, 4, 1), (WIDTH, HEIGHT), point_list, n_group)

# 시도 2
init_mover = 400  # 한 턴에 움직이는 거리, 초기값
end_mover = 50  # 마지막 턴에 움직일 거리
n_turn = 9  # 몇 라운드로 진행할지
ratio = (end_mover / init_mover) ** (1 / (n_turn - 1))  # 지수적 감소 비율
dd = (end_mover - init_mover) / (n_turn - 1)  # 등차적 감소량
movers = []
for i in range(n_turn):
    movers.append(init_mover * (ratio ** i))
movers = [50, 100, 150, 300, 400, 300, 150, 100, 50]

for i in range(n_turn):
    mover = movers[i]
    if i < 3:
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    elif i == 3:
        center_num = centers_to_centers(point_list, np.random.randint(1, n_group + 1))
        print(f"New center num: {center_num}")
        for point in point_list:
            if point.type == "moon":
                if np.random.randint(100) < 20:
                    point.type = "free"
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    elif i == 4:
        for point in point_list:
            if point.type == "free":
                point.type = "moon"
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    elif i == 5:
        if count_type(point_list)["center"] == 1:
            if np.random.randint(100) < 100:
                for point in point_list:
                    if point.type == "moon":
                        point.type = "center"
                        break
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    else:
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    n_group = cluster_points(point_list)
    print(f"Round{i}, #Cluster: {n_group}, Group Size:{cal_group_size(point_list)}")
    # plot, 제목은 '몇 번째 이동인지 / 이동거리'
    plot_points(f"{i}th / {round(mover, 1)} / {round(sum(movers[i + 1:]), 0)}", (3, 4, i + 2), (WIDTH, HEIGHT),
                point_list, n_group)


plt.show()
