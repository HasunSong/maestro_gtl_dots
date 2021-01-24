# %%
import math
import numpy as np

CC_REPULSION = 10  # center간 반발 가중치.
CM_ATTRACTION = 10  # center와 moon 간 인력 가중치
W_REPULSION = 1  # 점들과 벽 간의 반발 가중치. 애초에 화면 넘어갈 상황을 안 주는 게 좋다.

C_RANDOM = 0  # center 움직임에 랜덤을 주는 강도
M_RANDOM = 1  # moon 움직임에 랜덤을 주는 강도. delta_theta = M_RANDOM * np.random.normal() * math.pi / 4


def distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def dir_vector(p1, p2):
    d = distance(p1, p2)
    return (p1.x - p2.x) / d, (p1.y - p2.y) / d


def vector_normalizer(vector, target_size):
    vector_size = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
    if vector_size == 0:  # 에러 떴다. 아무 벡터나 리턴하자.
        theta = np.random.uniform(0, 2 * math.pi)
        return target_size * math.cos(theta), target_size * math.sin(theta)
    new_x = vector[0] / vector_size * target_size
    new_y = vector[1] / vector_size * target_size
    return new_x, new_y


class Point:
    def __init__(self, id, type, pos):
        self.id = id
        self.type = type
        self.x, self.y = pos
        self.fx, self.fy = 0, 0
        self.group = 0

    def update_force_for_one_point(self, another_point):
        d = distance(self, another_point)
        if d == 0:  # another_point == self
            return
        dir = dir_vector(self, another_point)
        if self.type == "center":
            if another_point.type == "center":
                self.fx += CC_REPULSION / (d ** 2) * dir[0]
                self.fy += CC_REPULSION / (d ** 2) * dir[1]
        elif self.type == "moon":
            if another_point.type == "center":
                self.fx += - CM_ATTRACTION / (d ** 2) * dir[0]
                self.fy += - CM_ATTRACTION / (d ** 2) * dir[1]

    def update_force_for_walls(self, field_size):  # 벽과 멀 때는 약함. 가까워지면 엄청 강해짐.
        # 엄청 강해져봤자 이동거리 제한 있어서 튕 날라간다거나 하는 부작용은 없음.
        self.fx += W_REPULSION * (1 / (self.x ** 4) - 1 / ((field_size[0] - self.x) ** 4))
        self.fy += W_REPULSION * (1 / (self.y ** 4) - 1 / ((field_size[1] - self.y) ** 4))

    # 점 및 벽과의 상호작용을 고려하여, 현재 점이 받고 있는 힘 계산 및 저장.
    def update_force(self, point_lst, field_size):
        for point in point_lst:
            self.update_force_for_one_point(point)
        self.update_force_for_walls(field_size)

    # 점이 받고 있는 힘에 랜덤 요소를 더한 뒤, 정규화를 통해 지정된 이동거리만큼 이동.
    def move(self, field_size, move_len):
        if self.type == "free":  # 완전 랜덤
            theta = np.random.uniform(0, 2*math.pi)
            vx = move_len * math.cos(theta)
            vy = move_len * math.sin(theta)
        else:
            # 랜덤 요소
            delta_theta = 0  # 이 각도를 랜덤하게 정해서, 이 각도만큼 힘의 방향을 변화시킨다.
            if self.type == "center":
                delta_theta = C_RANDOM * np.random.normal() * math.pi / 4
            elif self.type == "moon":
                delta_theta = M_RANDOM * np.random.normal() * math.pi / 4
            # 회전편환 공식 이용하여 랜덤 적용
            fx_rand_added = math.cos(delta_theta)*self.fx - math.sin(delta_theta)*self.fy
            fy_rand_added = math.sin(delta_theta)*self.fx + math.cos(delta_theta)*self.fy
            # 지정된 이동거리로 정규화
            vx, vy = vector_normalizer(vector=(fx_rand_added, fy_rand_added), target_size=move_len)
        # 실제 이동
        self.x += vx
        self.y += vy
        # 벽과의 반발을 적용했기 때문에 벽 뚫을 일이 많지는 않겠지만 혹시 뚫을 경우
        # 일단 그냥 가다가 멈추는 거로 처리(어차피 티도 잘 안 날 듯)
        # 거리 1의 여유는 둔다. (안 그러면 다음 턴에 벽 간의 반발력 무한대로 날라감)
        while self.x < 0:
            self.x = 1
        while self.x > field_size[0]:
            self.x = field_size[0] - 1
        while self.y < 0:
            self.y = 1
        while self.y > field_size[1]:
            self.y = field_size[1] - 1
        # 점이 받고 있는 힘 초기화
        self.fx, self.fy = 0, 0
