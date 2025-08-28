import pandas as pd

def count_cluster_labels_per_month(file_path):
    # 读取 CSV 文件
    df = pd.read_csv(file_path)

    # 按“月份”分组，然后统计每个组中聚类标签为 0 和 1 的数量
    result = pd.crosstab(df['月份'], df['聚类标签']).rename(columns=lambda x: f'聚类标签{x}数量')

    # 打印结果
    print(result)

    # 如果需要保存结果到文件
    result.to_csv('cluster_count_per_month.csv', index=True)
    print("结果已保存到 cluster_count_per_month.csv")

# 使用方法
file_path = 'result/result.csv'  # 替换为你的文件路径
count_cluster_labels_per_month(file_path)