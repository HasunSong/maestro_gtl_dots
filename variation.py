# %%
# 중간에 한 번 centers를 다시 설정해주는 기능
# 어떻게 해야 플레이어를 헷갈리게 할 수 있을지를 고려해서 짜야 함.
import copy
import numpy as np


# %%
# 각 그룹의 사이즈 계산
def cal_group_size(point_lst):
    groups = []
    for point in point_lst:
        groups.append(point.group)
    n_group = max(groups)+1
    group_size = [0]*n_group
    for group in groups:
        group_size[group] += 1
    return group_size


# 주어진 point 중 랜덤하게 n 개를 새로운 center로 지정
def randomly_set_new_centers(point_lst, n_centers):
    new_centers = np.random.choice(point_lst, n_centers, replace=False)
    for point in new_centers:
        point.type = "center"


# %%
# centers 재설정
# version 1. 두 번째로 큰 그룹에서 새로운 center 3개 등장.
# 두 번째로 큰 그룹이 쪼개지면서 다른 그룹을 흡수하는 그림 예상됨.
def reset_centers_v1(point_lst):
    # 두 번째로 큰 그룹 찾기
    group_size = cal_group_size(point_lst)
    temp_g_s = copy.copy(group_size)
    temp_g_s.sort(reverse=True)
    second_group_size = temp_g_s[1]
    second_group_name = 0
    for i in range(len(group_size)):
        if group_size[i] == second_group_size:
            second_group_name = i
    # 두 번째 그룹에 속한 점들 선별
    second_group_points = []
    for point in point_lst:
        if point.group == second_group_name:
            second_group_points.append(point)
    # 모든 point의 type을 moon으로 초기화. 두 번째 그룹 중 3개를 새로운 center로 지정
    for point in point_lst:
        point.type = "moon"
    randomly_set_new_centers(second_group_points, 3)