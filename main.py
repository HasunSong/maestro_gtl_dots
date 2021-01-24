# %%
from point import *
from visualization import *
from clusterer import *
from variation import *
import numpy as np

# %%
# 화면 크기
WIDTH = 70
HEIGHT = 50

# %%
# 시도 1

# center 초기화
centers = []
for i in range(3):
    new_point = Point(id=i, type="center", pos=(np.random.normal()*WIDTH/8+WIDTH/2, np.random.normal()*HEIGHT/8+HEIGHT/2))
    centers.append(new_point)

# moon 초기화
moons = []
for i in range(12):
    new_point = Point(id=i, type="moon",
                      pos=(np.random.normal() * WIDTH / 4 + WIDTH / 2, np.random.normal() * HEIGHT / 4 + HEIGHT / 2))
    moons.append(new_point)

point_list = centers + moons

# figure 초기화
figsize_x = 6.4
figsize_y = HEIGHT * 6.4 / WIDTH
plt.figure(figsize=(figsize_x, figsize_y))

# 초기 상태에서 군집화 및 plot
n_group = cluster_points(point_list)
plot_points("init", (3, 4, 1), (WIDTH, HEIGHT), point_list, n_group)

mover = 5  # 한 턴에 움직이는 거리
for i in range(11):  # 11번 움직일 거다.
    if i == 4:  # 4번 움직이고 난 후 center 재설정
        reset_centers_v1(point_list)
    for point in point_list:  # 각 점이 받는 힘 계산 및 저장
        point.update_force(point_list, (WIDTH, HEIGHT))
    for point in point_list:  # 위에서 저장한 힘에 랜덤 요소 추가하여, 지정된 거리만큼 이동
        point.move((WIDTH, HEIGHT), move_len=mover)
    # 군집화, 그룹 수 저장
    n_group = cluster_points(point_list)
    # plot, 제목은 '몇 번째 이동인지 / 이동거리'
    plot_points(f"{i+1}th / {round(mover,1)}", (3, 4, i+2), (WIDTH, HEIGHT), point_list, n_group)
    # 이동 거리의 지수적 감소
    mover /= 1.1

plt.show()

# %%
# 시도 2

# center 초기화
centers = []
for i in range(3):
    new_point = Point(id=i, type="center", pos=(np.random.normal()*WIDTH/8+WIDTH/2, np.random.normal()*HEIGHT/8+HEIGHT/2))
    centers.append(new_point)

# moon 초기화
moons = []
for i in range(12):
    new_point = Point(id=i, type="moon",
                      pos=(np.random.normal() * WIDTH / 4 + WIDTH / 2, np.random.normal() * HEIGHT / 4 + HEIGHT / 2))
    moons.append(new_point)

point_list = centers + moons

# figure 초기화
figsize_x = 6.4
figsize_y = HEIGHT * 6.4 / WIDTH
plt.figure(figsize=(figsize_x, figsize_y))

# 초기 상태에서 군집화 및 plot
n_group = cluster_points(point_list)
plot_points("init", (3, 4, 1), (WIDTH, HEIGHT), point_list, n_group)

mover = 5  # 한 턴에 움직이는 거리
for i in range(11):  # 11번 움직일 거다.
    # 3, 4 번째 움직임은 완전 랜덤
    if i == 2:
        for point in point_list:
            point.type = "free"
    # 5번째 시작에 다시 center 설정
    elif i == 4:
        for point in point_list:
            point.type = "moon"
        randomly_set_new_centers(point_list, 3)
    for point in point_list:  # 각 점이 받는 힘 계산 및 저장
        point.update_force(point_list, (WIDTH, HEIGHT))
    for point in point_list:  # 위에서 저장한 힘에 랜덤 요소 추가하여, 지정된 거리만큼 이동
        point.move((WIDTH, HEIGHT), move_len=mover)
    # 군집화, 그룹 수 저장
    n_group = cluster_points(point_list)
    # plot, 제목은 '몇 번째 이동인지 / 이동거리'
    plot_points(f"{i+1}th / {round(mover,1)}", (3, 4, i+2), (WIDTH, HEIGHT), point_list, n_group)
    # 이동 거리의 지수적 감소
    mover /= 1.1

plt.show()


# %%
"""
# %%
# centers 실험
centers = []
for i in range(3):
    new_point = Point(i, "center", (np.random.normal()*WIDTH/8+WIDTH/2, np.random.normal()*HEIGHT/8+HEIGHT/2))
    centers.append(new_point)

figsize_x = 6.4
figsize_y = HEIGHT * 6.4 / WIDTH
plt.figure(figsize=(figsize_x, figsize_y))

plot_points("init", (WIDTH, HEIGHT), [centers], (3, 4, 1))

center_mover = 1
for i in range(3*4-1):
    for point in centers:
        point.update_move_plan(centers, (WIDTH, HEIGHT))
    for point in centers:
        point.move((WIDTH, HEIGHT), move_len=center_mover)
    plot_points(f"move{i}", (WIDTH, HEIGHT), [centers], (3, 4, i+2))
    center_mover /= 1.2

plt.show()


# %%
# 고정된 centers에 대한 moons 실험
centers = [Point(i, "center", (1, 1)),
           Point(i, "center", (5, 1)),
           Point(i, "center", (3, 4))]

moons = []
for i in range(12):
    new_point = Point(i, "moon",
                      (np.random.normal() * WIDTH / 4 + WIDTH / 2, np.random.normal() * HEIGHT / 4 + HEIGHT / 2))
    moons.append(new_point)

figsize_x = 6.4
figsize_y = HEIGHT * 6.4 / WIDTH
plt.figure(figsize=(figsize_x, figsize_y))

plot_points("fixed_centers", (WIDTH, HEIGHT), [centers], (3, 4, 1))
plot_points("moons(init)", (WIDTH, HEIGHT), [moons], (3, 4, 2))

moon_mover = 1
for i in range(10):
    for point in moons:
        point.update_move_plan(centers, (WIDTH, HEIGHT))
    for point in moons:
        point.move((WIDTH, HEIGHT), move_len=moon_mover)
    plot_points(f"move{i}", (WIDTH, HEIGHT), [moons], (3, 4, i+3))
    moon_mover /= 1.2

plt.show()
"""