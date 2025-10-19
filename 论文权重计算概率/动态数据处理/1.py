import os
import pandas as pd

# 设置你的文件夹路径
folder_path = './save_tmp'  # 替换为你的实际路径

# 列名映射
rename_map = {'0': 'longitude', '1': 'latitude', '2': 'tmp'}

# 遍历所有csv文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        df = pd.read_csv(file_path)

        # 只重命名存在的列
        df.rename(columns=rename_map, inplace=True)

        # 保存回原文件（覆盖）
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        print(f"✅ 已处理：{filename}")