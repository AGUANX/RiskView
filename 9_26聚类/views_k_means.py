import os

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
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


folder_path = 'count'
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        df = pd.read_csv(os.path.join(folder_path, filename))
        i = 1
        # 获取所有以“聚类标签”开头的列
        feature_columns = [col for col in df.columns if col.startswith('聚类标签')]
        # 提取特征
        X = df[feature_columns]

        # 确定最佳聚类数
        inertia = []
        K_range = list(range(1, 16))
        for n in range(1, 16):
            kmeans = KMeans(n_clusters=n, random_state=0)
            kmeans.fit(X)
            inertia.append(kmeans.inertia_)

        best_k = auto_elbow_k(K_range, inertia)


        # 最佳聚类数
        kmeans = KMeans(n_clusters=best_k, random_state=0)
        df['月份聚类标签'] = kmeans.fit_predict(X)

        # 输出结果
        print(df[['年份', '月份聚类标签']])
        df[['年份', '月份聚类标签']].to_csv('聚类月份/' + filename, index=False)
        i += 1
        # 可视化聚类结果（降维后可视化）
        from sklearn.decomposition import PCA

        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(X)

        plt.figure()
        scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['月份聚类标签'], cmap='viridis')
        plt.title('Mouth' + str(i - 1) )
        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.colorbar(scatter)
        plt.show()