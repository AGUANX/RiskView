import os

import pandas as pd

folder_path = './output'

# 遍历所有csv文件
# 修改为每月聚类一次，然后根据聚类合并场景
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        filename = os.path.join(folder_path, filename)
        data = pd.read_csv(filename)

        # 1) 新增“年”“月”两列
        data['year'] = data['年份'] // 100
        data['month'] = data['年份'] % 100

        data.to_csv(filename, index=False)


