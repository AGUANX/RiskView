"""
k_means_months.py  ——  每月自动聚类并落盘结果与可视化
"""
import os
os.environ["OMP_NUM_THREADS"] = "1"   # 必须在 import sklearn 之前

import pandas as pd
import numpy as np
from kneed import KneeLocator
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

# ---------------------------- 参数区 -----------------------------
DATA_FILE   = "new_data.csv"
OUT_DIR     = "月份"
MAX_K       = 10                     # 最大候选聚类数
RANDOM_SEED = 42                     # 复现用
# ----------------------------------------------------------------

os.makedirs(OUT_DIR, exist_ok=True)
data = pd.read_csv(DATA_FILE)

# 确保月份列是整数
data["月份"] = pd.to_numeric(data["月份"], errors="coerce").astype("Int64")

for month_int in range(1, 13):
    month_str = f"{month_int:02d}"
    month_df  = data[data["月份"] == month_int].copy()

    # 1. 过滤空数据
    if month_df.empty:
        print(f"[{month_str}] 无数据，跳过")
        continue

    # 2. 特征列
    feat_cols = [c for c in month_df.columns if c.startswith("聚类标签")]
    X = month_df[feat_cols].dropna(axis=0)   # 去掉缺失值
    if X.empty:
        print(f"[{month_str}] 无有效特征，跳过")
        continue

    # 3. 自动选 k：肘部法 + 兜底
    inertia = []
    k_range = range(1, min(MAX_K, len(X)) + 1)   # 样本太少时自动缩小 k 范围
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=RANDOM_SEED, n_init="auto")
        km.fit(X)
        inertia.append(km.inertia_)

    kn = KneeLocator(k_range, inertia, curve="convex", direction="decreasing")
    best_k = kn.elbow if kn.elbow is not None else 1   # 兜底至少 1 类

    # 4. 最终聚类
    final_km = KMeans(n_clusters=best_k, random_state=RANDOM_SEED, n_init="auto")
    month_df["月份聚类标签"] = final_km.fit_predict(X)

    # 5. 保存标签
    label_file = os.path.join(OUT_DIR, f"月份{month_int}.csv")
    month_df[["年份", "月份聚类标签"]].to_csv(label_file, index=False, encoding="utf-8-sig")
    print(f"[{month_str}] 聚类完成，k={best_k}，结果已保存至 {label_file}")

    # 6. PCA 可视化
    pca = PCA(n_components=2, random_state=RANDOM_SEED)
    X_pca = pca.fit_transform(X)
    plt.figure(figsize=(5, 4))
    scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1],
                          c=month_df["月份聚类标签"], cmap="viridis", s=25)
    plt.title(f"{month_str} 月聚类结果 (k={best_k})")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.colorbar(scatter)
    vis_file = os.path.join(OUT_DIR, f"月份{month_int}.png")
    plt.tight_layout()
    plt.savefig(vis_file, dpi=150)
    plt.close()
    print(f"[{month_str}] 可视化已保存至 {vis_file}")

print("全部月份处理完毕！")