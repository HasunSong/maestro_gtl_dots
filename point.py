# %%
import math
import numpy as np

CC_REPULSION = 10  # center간 반발 가중치.
CM_ATTRACTION = 10  # center와 moon 간 인력 가중치
CRM_REPULSION = 10  # center와 reversed moon 간 반발력 가중치
W_REPULSION = 0  # 점들과 벽 간의 반발 가중치. 애초에 화면 넘어갈 상황을 안 주는 게 좋다.

C_RANDOM = 0  # center 움직임에 랜덤을 주는 강도
M_RANDOM = 0.75  # moon 움직임에 랜덤을 주는 강도. delta_theta = M_RANDOM * np.random.normal() * math.pi / 4
RM_RANDOM = 0.5  # reversed moon 랜덤


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
        self.id = id  # 만들어두긴 했는데 안 씀. 헿
        self.type = type  # center인지, moon인지 그런 거
        self.mass = 1  # 나중에 점마다 가중치 줄 일 생길까 해서 만들어둠
        self.x, self.y = pos  # 점 위치
        self.fx, self.fy = 0, 0  # 이 점이 받고 있는 힘의 x, y 성분
        self.group = 0  # 그룹화된 결과, 그룹 번호, 0~k-1

    # 다른 한 점에 의해 이 점이 받는 힘을 계산하여 업데이트한다.
    def update_force_for_one_point(self, another_point):
        d = distance(self, another_point)
        if d == 0:  # another_point == self
            return
        dir = dir_vector(self, another_point)
        if self.type == "center":
            if another_point.type == "center":
                power = CC_REPULSION * self.mass * another_point.mass
                self.fx += power / (d ** 2) * dir[0]
                self.fy += power / (d ** 2) * dir[1]
        elif self.type == "moon":
            if another_point.type == "center":
                power = CM_ATTRACTION * self.mass * another_point.mass
                self.fx += - power / (d ** 2) * dir[0]
                self.fy += - power / (d ** 2) * dir[1]
        elif self.type == "reversed moon":
            if another_point.type == "center":
                power = CRM_REPULSION * self.mass * another_point.mass
                self.fx += power / (d ** 2) * dir[0]
                self.fy += power / (d ** 2) * dir[1]

    # 이 점이 네 벽으로부터 받는 힘 계산하여 업데이트
    def update_force_for_walls(self, field_size):  # 벽과 멀 때는 약함. 가까워지면 엄청 강해짐.
        # 엄청 강해져봤자 이동거리 제한 있어서 튕 날라간다거나 하는 부작용은 없음.
        self.fx += W_REPULSION * (1 / (self.x ** 3) - 1 / ((field_size[0] - self.x) ** 3))
        self.fy += W_REPULSION * (1 / (self.y ** 3) - 1 / ((field_size[1] - self.y) ** 3))

    # 점 및 벽과의 상호작용을 고려하여, 현재 점이 받고 있는 힘 계산 및 저장.
    def update_force(self, point_lst, field_size):
        for point in point_lst:
            self.update_force_for_one_point(point)
        self.update_force_for_walls(field_size)

    # 점이 받고 있는 힘에 랜덤 요소를 더한 뒤, 정규화를 통해 지정된 이동거리만큼 이동.
    def move(self, field_size, move_len):
        if self.type == "free":  # 완전 랜덤
            theta = np.random.uniform(0, 2 * math.pi)
            vx = move_len * math.cos(theta)
            vy = move_len * math.sin(theta)
        else:
            # 랜덤 요소
            delta_theta = 0  # 이 각도를 랜덤하게 정해서, 이 각도만큼 힘의 방향을 변화시킨다.
            if self.type == "center":
                delta_theta = C_RANDOM * np.random.normal() * math.pi / 4
            elif self.type == "moon":
                delta_theta = M_RANDOM * np.random.normal() * math.pi / 4
            elif self.type == "reversed moon":
                delta_theta = RM_RANDOM * np.random.normal() * math.pi / 4
            # 회전편환 공식 이용하여 랜덤 적용
            fx_rand_added = math.cos(delta_theta) * self.fx - math.sin(delta_theta) * self.fy
            fy_rand_added = math.sin(delta_theta) * self.fx + math.cos(delta_theta) * self.fy
            # 지정된 이동거리로 정규화
            if self.type == "center":
                vx, vy = vector_normalizer(vector=(fx_rand_added, fy_rand_added), target_size=move_len / 2)
            else:
                vx, vy = vector_normalizer(vector=(fx_rand_added, fy_rand_added), target_size=move_len)
        # 실제 이동
        self.x, self.y = valid_move(self.x, self.y, vx, vy, field_size)
        # 벽과의 반발을 적용했기 때문에 벽 뚫을 일이 많지는 않겠지만 혹시 뚫을 경우
        # 일단 그냥 가다가 멈추는 거로 처리(어차피 티도 잘 안 날 듯)
        # 거리 1의 여유는 둔다. (안 그러면 다음 턴에 벽과의 반발력 무한대로 날라감)
        if self.type == "center" or "moon":
            if self.x < 0:
                self.x = 1
            elif self.x > field_size[0]:
                self.x = field_size[0] - 1
            if self.y < 0:
                self.y = 1
            elif self.y > field_size[1]:
                self.y = field_size[1] - 1
        else:
            while self.x < 0:
                self.x += field_size[0]
            while self.x > field_size[0]:
                self.x -= field_size[0]
            while self.y < 0:
                self.y += field_size[1]
            while self.y > field_size[1]:
                self.y -= field_size[1]
        # 점이 받고 있는 힘 초기화
        self.fx, self.fy = 0, 0


# 적당한 속도로 수렴
# 각 점들이 동시에 움직임
def update_points(point_lst, field_size, move_len):
    for point in point_lst:
        point.update_force(point_lst, field_size)
    for point in point_lst:
        point.move(field_size, move_len)


# 빠른 수렴을 위해, center들을 먼저 움직인 뒤, moon들이 그 결과를 보고 움직이도록 한다.
def update_points_fast(point_lst, field_size, move_len):
    for point in point_lst:
        if point.type == "center":
            point.update_force(point_lst, field_size)
            point.move(field_size, move_len)
    for point in point_lst:
        if point.type == "moon" or "reversed_moon":
            point.update_force(point_lst, field_size)
            point.move(field_size, move_len)
    for point in point_lst:
        if point.type == "free":
            point.update_force(point_lst, field_size)
            point.move(field_size, move_len)


# 특정 좌표가 필드 안에 있는지 확인하여 true false 리던
def in_field(x, y, field_size):
    return (0.1 <= x <= field_size[0]-0.1) and (0.1 <= y <= field_size[1]-0.1)


# 현재 위치 x, y, 움직이려는 변위 vx, vy, 필드 크기 field_size 입력받음.
# 가고자 하는 곳이 이동 가능한 위치면, 이동한 위치 리턴
# 가고자 하는 곳이 이동 불가능한 위치라면, 가능한 위치로 가서 그 위치 리턴.
def valid_move(x, y, vx, vy, field_size):
    if in_field(x + vx, y + vy, field_size):
        return x + vx, y + vy
    else:
        # 방향을 조금씩 틀어가면서, 이동 가능한 곳이 나오면 거기로 간다.
        for i in range(1, 32):
            theta = math.pi / 32 * i  # 방향을 theta만큼 튼다.
            temp_vx = math.cos(theta) * vx - math.sin(theta) * vy
            temp_vy = math.sin(theta) * vx + math.cos(theta) * vy
            #print(x+temp_vx,y+temp_vy)
            if in_field(x + temp_vx, y + temp_vy, field_size):
                return x + temp_vx, y + temp_vy
            temp_vx = math.cos(-theta) * vx - math.sin(-theta) * vy
            temp_vy = math.sin(-theta) * vx + math.cos(-theta) * vy
            #print(x+temp_vx, y+temp_vy)
            if in_field(x + temp_vx, y + temp_vy, field_size):
                return x + temp_vx, y + temp_vy
    print("Error!")
    return 1, 1


# point_list 받아서 각 type 개수 세는 함수
def count_type(point_lst):
    result = {}
    keys = ("center", "moon", "reversed moon", "free")
    for key in keys:
        result[key] = 0
    for point in point_lst:
        result[point.type] += 1
    return result


# point_list 받아서 좌표값만 뽑아낸 list 리턴하는 함수
def extract_coords(point_list):
    result = []
    for point in point_list:
        result.append([point.x, point.y])
    return result