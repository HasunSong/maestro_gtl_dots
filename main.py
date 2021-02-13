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
# 초기화
# center 초기화
centers = []
for i in range(3):
    new_point = Point(id=i, type="center",
                      pos=(np.random.normal() * WIDTH / 8 + WIDTH / 2, np.random.normal() * HEIGHT / 8 + HEIGHT / 2))
    centers.append(new_point)

# moon 초기화
moons = []
for i in range(17):
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

# %%
# 기본
mover = 15  # 한 턴에 움직이는 거리, 초기값
end_mover = 2  # 마지막 턴에 움직일 거리
n_turn = 8  # 몇 라운드로 진행할지
ratio = (end_mover / mover) ** (1 / (n_turn - 1))  # 지수적 감소 비율

for i in range(11):  # 11번 움직일 거다.
    for point in point_list:  # 각 점이 받는 힘 계산 및 저장
        point.update_force(point_list, (WIDTH, HEIGHT))
    for point in point_list:  # 위에서 저장한 힘에 랜덤 요소 추가하여, 지정된 거리만큼 이동
        point.move((WIDTH, HEIGHT), move_len=mover)
    # 군집화, 그룹 수 저장
    n_group = cluster_points(point_list)
    # plot, 제목은 '몇 번째 이동인지 / 이동거리'
    plot_points(f"{i + 1}th / {round(mover, 1)}", (3, 4, i + 2), (WIDTH, HEIGHT), point_list, n_group)
    # 이동 거리의 지수적 감소
    mover *= ratio

plt.show()

# %%
# 기본 - 하나씩 업데이트
mover = 15  # 한 턴에 움직이는 거리, 초기값
end_mover = 2  # 마지막 턴에 움직일 거리
n_turn = 8  # 몇 라운드로 진행할지
ratio = (end_mover / mover) ** (1 / (n_turn - 1))  # 지수적 감소 비율

for i in range(11):  # 11번 움직일 거다.
    for point in point_list:  # 각 점이 받는 힘 계산 및 저장, 바로 움직임
        point.update_force(point_list, (WIDTH, HEIGHT))
        point.move((WIDTH, HEIGHT), move_len=mover)
    # 군집화, 그룹 수 저장
    n_group = cluster_points(point_list)
    # plot, 제목은 '몇 번째 이동인지 / 이동거리'
    plot_points(f"{i + 1}th / {round(mover, 1)}", (3, 4, i + 2), (WIDTH, HEIGHT), point_list, n_group)
    # 이동 거리의 지수적 감소
    mover *= ratio

plt.show()

# %%
# 시도 1
mover = 15  # 한 턴에 움직이는 거리, 초기값
end_mover = 2  # 마지막 턴에 움직일 거리
n_turn = 8  # 몇 라운드로 진행할지
ratio = (end_mover / mover) ** (1 / (n_turn - 1))  # 지수적 감소 비율

for i in range(11):  # 11번 움직일 거다/
    if i == 4:  # 4번 움직이고 난 후 center 재설정
        reset_centers_v1(point_list)
    for point in point_list:  # 각 점이 받는 힘 계산 및 저장
        point.update_force(point_list, (WIDTH, HEIGHT))
        point.move((WIDTH, HEIGHT), move_len=mover)
    # for point in point_list:  # 위에서 저장한 힘에 랜덤 요소 추가하여, 지정된 거리만큼 이동
    #    point.move((WIDTH, HEIGHT), move_len=mover)
    # 군집화, 그룹 수 저장
    n_group = cluster_points(point_list)
    # plot, 제목은 '몇 번째 이동인지 / 이동거리'
    plot_points(f"{i + 1}th / {round(mover, 1)}", (3, 4, i + 2), (WIDTH, HEIGHT), point_list, n_group)
    # 이동 거리의 지수적 감소
    mover *= ratio

plt.show()

# %%
# 화면 크기
WIDTH = 1800
HEIGHT = 800

# 초기화
# center 초기화
centers = []
for i in range(3):
    new_point = Point(id=i, type="center",
                      pos=(np.random.normal() * WIDTH / 8 + WIDTH / 2, np.random.normal() * HEIGHT / 8 + HEIGHT / 2))
    centers.append(new_point)

# moon 초기화
moons = []
for i in range(36):
    new_point = Point(id=i, type="moon",
                      pos=(np.random.normal() * WIDTH / 4 + WIDTH / 2, np.random.normal() * HEIGHT / 4 + HEIGHT / 2))
    moons.append(new_point)

point_list = centers + moons

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
    movers.append(init_mover * (ratio**i))
movers = [50,100,150,300,400,300,150,100,50]

for i in range(n_turn):  # 11번 움직일 거다.
    mover = movers[i]
    if i == 0:
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    elif i == 1 or i == 2:
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    elif i == 3:  # 그룹 빠르게 박살내기, moon들을 center로부터 멀어지게 한다.
        for point in point_list:
            if point.type == "moon":
                point.type = "reversed moon"
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    elif i == 4:
        for point in point_list:
            point.type = "free"
        update_points(point_list, (WIDTH, HEIGHT), mover)
    elif i == 5:
        for point in point_list:
            point.type = "moon"
        centers_to_centers(point_list, np.random.randint(1, n_group+1))
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    else:
        update_points_fast(point_list, (WIDTH, HEIGHT), mover)
    n_group = cluster_points(point_list)
    # plot, 제목은 '몇 번째 이동인지 / 이동거리'
    plot_points(f"{i}th / {round(mover, 1)} / {round(sum(movers[i+1:]), 0)}", (3, 4, i + 2), (WIDTH, HEIGHT), point_list, n_group)

plt.show()
print("group size: ", cal_group_size(point_list))

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

# %%
