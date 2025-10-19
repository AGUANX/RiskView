import os

import pandas as pd


folder_path = 'result'  # 替换为你的文件路径


def count_cluster_labels_per_month(filename):

    # 读取 CSV 文件
    df = pd.read_csv(os.path.join(folder_path, filename))

    # 按“月份”分组，然后统计每个组中聚类标签为 0 和 1 的数量
    result = pd.crosstab(df['年份'], df['聚类标签']).rename(columns=lambda x: f'聚类标签{x}数量')

    # 打印结果
    print(result)

    # 如果需要保存结果到文件
    result.to_csv(filename + 'cluster_count_per_month.csv', index=True)
    print("结果已保存到 cluster_count_per_month.csv")

# 使用方法

for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        count_cluster_labels_per_month(filename, i)
