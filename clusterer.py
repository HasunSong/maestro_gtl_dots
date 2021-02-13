# %%
# K Mean Clustering을 이용한 군집화. 초기 점들은 center를 이용한다.

import numpy as np
from sklearn.cluster import KMeans

THRESHOLD = 2000000
K_MAX = 5


def cluster_points(point_lst, print_value=False):
    coord_lst = []
    for point in point_lst:
        coord_lst.append([point.x, point.y])
    coord_lst = np.array(coord_lst)

    # k값을 1부터 k_max까지 돌려보고 최소의 WSS score를 탐색한다.

    for k in range(1, K_MAX, 1):
        kmeans = KMeans(n_clusters=k).fit(coord_lst)
        centroids = kmeans.cluster_centers_
        labels = kmeans.labels_
        # wss 계산과정
        pred_clusters = kmeans.predict(coord_lst)
        curr_sse = 0

        # calculate square of Euclidean distance of each point from its cluster center and add to current WSS
        for i in range(len(point_lst)):
            curr_center = centroids[pred_clusters[i]]
            curr_sse += (coord_lst[i, 0] - curr_center[0]) ** 2 + (coord_lst[i, 1] - curr_center[1]) ** 2
        # 값 리스트에 저장
        # 날짜가 같은 기사끼리 명확하게 군집화되면 이 점수가 0에 매우 급격히 수렴한다.
        # 따라서  0.001 이하가 되는 최초의 k을 클러스터 수로 지정하고 label과 centroid를 return한다.
        if print_value:
            print(k, curr_sse)
        if curr_sse < THRESHOLD:
            for i in range(len(point_lst)):
                curr_point = point_lst[i]
                curr_label = labels[i]
                curr_point.group = curr_label
            return k
        # THRESHOLD 이하가 되지 않고 끝에 도달할 경우 그냥 마지막 label, centroid
        if k == K_MAX - 1:
            for i in range(len(point_lst)):
                curr_point = point_lst[i]
                curr_label = labels[i]
                curr_point.group = curr_label
            return k
