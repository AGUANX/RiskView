import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


df = pd.read_csv('cluster_count_per_month.csv')

# 获取所有以“聚类标签”开头的列
feature_columns = [col for col in df.columns if col.startswith('聚类标签')]
# 提取特征
X = df[feature_columns]

# 确定最佳聚类数
inertia = []
for n in range(1, 11):
    kmeans = KMeans(n_clusters=n, random_state=0)
    kmeans.fit(X)
    inertia.append(kmeans.inertia_)

plt.figure()
plt.plot(range(1, 11), inertia)
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('Inertia')
plt.show()

# 最佳聚类数
kmeans = KMeans(n_clusters=3, random_state=0)
df['月份聚类标签'] = kmeans.fit_predict(X)

# 输出结果
print(df[['月份', '月份聚类标签']])
df[['月份', '月份聚类标签']].to_csv('month_clustering_results.csv', index=False)

# 可视化聚类结果（降维后可视化）
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)

plt.figure()
scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=df['月份聚类标签'], cmap='viridis')
plt.title('PCA of Months Clustering')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(scatter)
plt.show()