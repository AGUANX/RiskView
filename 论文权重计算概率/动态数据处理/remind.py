import os

import pandas as pd
import numpy as np
from math import radians, cos, sin, sqrt, atan2

# Haversine 计算两点间距离（单位：公里）
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# 找到最近的 region_id
def find_nearest_region_id(lat, lon, regions_df):
    distances = regions_df.apply(
        lambda row: haversine(lat, lon, row['latitude'], row['longitude']), axis=1
    )
    idx_min = distances.idxmin()
    return regions_df.loc[idx_min, 'region_id']

# 主函数：原地更新源文件
def add_region_id_to_source(source_file, regions_file):
    source_df = pd.read_csv(source_file)
    regions_df = pd.read_csv(regions_file)

    if 'latitude' not in source_df.columns or 'longitude' not in source_df.columns:
        raise ValueError("源文件缺少 latitude 或 longitude 列")

    source_df['region_id'] = source_df.apply(
        lambda row: find_nearest_region_id(row['latitude'], row['longitude'], regions_df), axis=1
    )

    # 原地写回
    source_df.to_csv(source_file, index=False, encoding='utf-8')
    print(f"已更新文件：{source_file}")

# 示例用法
if __name__ == '__main__':
    regions_file = './vegetation_data_by_month/2003_01.csv'  # 替换为你的区域文件路径
    # 设置你的文件夹路径
    folder_path = '.\save_tmp'  # 替换为你的实际路径
    # 遍历所有csv文件
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            print(file_path)

            add_region_id_to_source(file_path, regions_file)
            print(f"✅ 已处理：{filename}")

