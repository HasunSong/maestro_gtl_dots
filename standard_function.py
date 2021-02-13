# %%
# API 만드려고 잠깐 임시로 만든 파일. 지금 API에 이 함수 올라가 있음.

# 기본적으로 첫 3라운드 동안 1차 그룹을 형성한 뒤, 다음 3라운드 동안 그 그룹을 해체하고 새로운 그룹을 형성, 마지막 3라운드 동안 최종 그룹을 확실히 하는 양상을 띠게 된다.
# points_num은 AI 점의 개수
# init_group_num은 1차 그룹 개수
# final_group_num은 최종 그룹 개수(random_final_group_num이 false일 때만 지정)
# random_final_group_num은 최종 그룹 개수를 알고리즘에 따라 랜점하게 정할지 여부
# movers는 매 라운드마다 움직일 거리
# width와 heigth는 화면 크기
from point import *
from clusterer import *
from variation import *


def get_game_data(points_num=39, init_group_num=3, random_final_group_num=True, final_group_num=2,
               movers=(50, 100, 150, 300, 400, 300, 150, 100, 50), width=1800, height=800):
    record = []  # 움직인 기록, 라운드별 점들의 좌표를 저장

    # 점 초기화
    point_list = []
    for i in range(points_num):
        x = min(max(np.random.normal() * width / 4 + width / 2, 1), width - 1)
        y = min(max(np.random.normal() * height / 4 + height / 2, 1), height - 1)
        new_point = Point(id=i, type="free", pos=(x, y))
        point_list.append(new_point)
    for i in range(3):
        update_points(point_list, (width, height), 200)
    for i in range(points_num):
        if i < init_group_num:
            point_list[i].type = "center"
        else:
            point_list[i].type = "moon"
    record.append(extract_coords(point_list))

    # 라운드 진행
    n_group = 1  # 매 라운드마다 군집화된 그룹 개수 저장
    for turn in range(1, 10):
        mover = movers[turn-1]  # 이동거리 mover에 저장
        if turn == 4:  # 2차 그룹화, 1차 그룹 병합
            if random_final_group_num:
                centers_to_centers(point_list, np.random.randint(1, n_group + 1))  # 그룹 개수 n_group개 -> 1~n_group개
            else:
                centers_to_centers(point_list, final_group_num)  # 그룹 개수 n_group개 -> final_group_num개
            for point in point_list:
                if point.type == "moon":
                    if np.random.randint(100) < 20:  # 20%의 점은 랜덤하게 움직인다.
                        point.type = "free"
        elif turn == 5:
            for point in point_list:  # 위에서 랜덤으로 설정했던 20% 다시 정신 차린다
                if point.type == "free":
                    point.type = "moon"
        elif turn == 6:
            if count_type(point_list)["center"] == 1:   # 최종 그룹이 하나가 될 기미가 보일 경우
                if np.random.randint(100) < 70:  # 70%의 확률로 그 그룹을 두 개로 찢는다.
                    for point in point_list:
                        if point.type == "moon":
                            point.type = "center"
                            break
        update_points_fast(point_list, (width, height), mover)  # 위에서 지정해준 패턴대로 움직임
        n_group = cluster_points(point_list)  # 클러스터링
        record.append(extract_coords(point_list))  # 움직인 결과 저장

        print(f"Round{turn}, #Center: {count_type(point_list)['center']}, #Cluster: {n_group}, Group Sizes:{cal_group_size(point_list)}")

    return {
        "coord_record": record,  # 0: 초기값, 1~9: @라운드 진행 후 점들의 위치
        "movers": movers,
        "points_num": points_num,
        "round_num": 9,
        "field_size": (width, height),
    }
