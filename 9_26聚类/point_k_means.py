# -*- coding: GBK -*-
import os

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt



# ---------- 自动肘部法则 ----------
def auto_elbow_k(K_range, sse, threshold=0.05):
    """
    K_range: 1~K_max 的 list
    sse:     对应 SSE  list
    threshold: SSE 下降率阈值，防止二阶差分找不到
    return:  推荐 K 值
    """
    # 一阶差分（相邻 SSE 差值）
    diff1 = np.diff(sse)
    # 二阶差分
    diff2 = np.diff(diff1)
    # 找二阶差分最大点（肘点）
    elbow_idx = np.argmax(diff2) + 2   # +2 因为 diff2 比 K_range 短 2
    recommended_k = K_range[elbow_idx]

    # 兜底：如果 SSE 下降率已很小，直接停
    for k, ratio in enumerate(np.abs(diff1 / sse[:-1]), start=2):
        if ratio < threshold:
            recommended_k = k
            break
    return recommended_k

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

years = [f"{i:02d}" for i in range(3, 21)]

dataframes = []
# 设置你的文件夹路径
folder_path = './output'  # 替换为你的实际路径

# 遍历所有csv文件
# 修改为每月聚类一次，然后根据聚类合并场景
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        filename = os.path.join(folder_path, filename)
        data = pd.read_csv(filename)
        dataframes.append(data)
# 合并
df = pd.concat(dataframes, ignore_index=True)


for mou in range(1, 13):
    # 修改这一段，改成行列同时筛选
    # 为了聚类，我们选择与气象场景相关的特征：降水量、相对湿度、温度
    features = ['tmp', 'ndvi']
    re = df[df['month'] == mou].copy()
    X = re[features]

    # 数据标准化
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 计算 SSE 序列（1~15）
    sse = []
    K_range = list(range(1, 16))
    for k in K_range:
        kmeans = KMeans(n_clusters=k, random_state=0, n_init='auto')
        kmeans.fit(X_scaled)
        sse.append(kmeans.inertia_)

    # 自动选 K
    best_k = auto_elbow_k(K_range, sse)
    print('自动肘部法则推荐 K =', best_k)

    # 用推荐 K 重新聚类
    kmeans = KMeans(n_clusters=best_k, random_state=0, n_init='auto')
    kmeans.fit(X_scaled)
    re['聚类标签'] = kmeans.labels_
    re.to_csv('result/' + str(mou) + 'result.csv', index=False)

    # 可视化聚类结果（3D 散点图）
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    scatter = ax.scatter(
        re['tmp'],
        re['ndvi'],
        c=re['聚类标签'],
        cmap='viridis',
        marker='o'
    )
    ax.set_xlabel('tmp')
    ax.set_ylabel('ndvi')
    plt.title('K-Means 聚类结果')
    plt.colorbar(scatter)
    plt.show()
