# -*- coding: GBK -*-

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

years = [f"{i:02d}" for i in range(3, 21)]

dataframes = []
# 读取数据
for year in years:
    file1 = 'merged/merged_data_' + year + '.csv处理'
    # 创建数据
    data = pd.read_csv(file1)
    dataframes.append(data)

# 合并
df = pd.concat(dataframes, ignore_index=True)


# 修改这一段，改成行列同时筛选
# 为了聚类，我们选择与气象场景相关的特征：降水量、相对湿度、温度
features = ['降水量', '相对湿度 (%)', '温度']
X = df[features]

# 数据标准化
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 使用 K-Means 算法进行聚类
kmeans = KMeans(n_clusters=3, random_state=0)  # 假设聚类数目为 3
kmeans.fit(X_scaled)

# 获取聚类结果
df['聚类标签'] = kmeans.labels_
df.to_csv('result/result.csv', index=False)

# 打印聚类结果
print(df[['月份', '降水量', '相对湿度 (%)', '温度', '聚类标签']])

# 可视化聚类结果（3D 散点图）
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(
    df['降水量'],
    df['相对湿度 (%)'],
    df['温度'],
    c=df['聚类标签'],
    cmap='viridis',
    marker='o'
)
ax.set_xlabel('降水量')
ax.set_ylabel('相对湿度 (%)')
ax.set_zlabel('温度')
plt.title('K-Means 聚类结果')
plt.colorbar(scatter)
plt.show()

# 肘部法则确定 K 值
sse = []
K_range = range(1, 16)
for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(X_scaled)
    sse.append(kmeans.inertia_)
    print(kmeans.inertia_)

plt.figure(figsize=(8, 6))
plt.plot(K_range, sse, 'bx-')
plt.xlabel('K')
plt.ylabel('SSE')
plt.title('肘部法则')
plt.show()