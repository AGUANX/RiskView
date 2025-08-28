import pandas as pd
import os

# 设置包含CSV文件的文件夹路径
folder_path = '相对湿度/extracted_20'
back_path = '01_rh_data.csv'  # 替换为你的文件夹路径


# 初始化一个空的DataFrame来存储所有经纬度
all_locations = pd.DataFrame()

years = [f"{i:02d}" for i in range(3, 21)]

# 遍历每个CSV文件
for year in years:
    file_path = folder_path + year + back_path
    # 读取CSV文件
    df = pd.read_csv(file_path)
    # 提取经纬度
    locations = df[['经度', '纬度']].drop_duplicates()
    # 将当前文件的经纬度添加到总数据框中
    all_locations = pd.concat([all_locations, locations], ignore_index=True)

# 去除所有文件中的重复经纬度
unique_locations = all_locations.drop_duplicates()

# 保存到新的CSV文件
unique_locations.to_csv('all_unique_locations.csv', index=False)

print(f"提取完成，所有文件的唯一经纬度已保存到 all_unique_locations.csv，共 {len(unique_locations)} 个唯一地点")