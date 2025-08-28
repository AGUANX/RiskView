'''
离散化
经度间隔  0.012837
纬度间隔  0.00847
边界左上
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 读取CSV文件
df = pd.read_csv('all_unique_locations.csv')

# 提取经度和纬度范围
min_lon = df['经度'].min()
max_lon = df['经度'].max()
min_lat = df['纬度'].min()
max_lat = df['纬度'].max()

# 确定网格间隔（根据数据中的间隔）
lon_interval = 0.012837  # 经度间隔
lat_interval = 0.00847  # 纬度间隔

# 计算边界扩展量
extend_lon = lon_interval / 2
extend_lat = lat_interval / 2

# 调整后的经度和纬度范围，确保边界中心点与其他中心点有相同大小的区域
adjusted_lon_min = min_lon - extend_lon
adjusted_lon_max = max_lon + extend_lon
adjusted_lat_min = min_lat - extend_lat
adjusted_lat_max = max_lat + extend_lat
print("纬度上下限", adjusted_lat_min, adjusted_lat_max)
print("经度上下限", adjusted_lon_min, adjusted_lon_max)

# 生成经度和纬度边界点
lon_bins = np.arange(adjusted_lon_min, adjusted_lon_max + lon_interval, lon_interval)
lat_bins = np.arange(adjusted_lat_min, adjusted_lat_max + lat_interval, lat_interval)

# 生成网格单元格并匹配中心点
grid_cells_with_center = []
for index, row in df.iterrows():
    center_lon = row['经度']
    center_lat = row['纬度']

    # 计算中心点所在的网格边界
    left_lon = center_lon - extend_lon
    right_lon = center_lon + extend_lon
    bottom_lat = center_lat - extend_lat
    top_lat = center_lat + extend_lat

    grid_cells_with_center.append({
        'center_lon': center_lon,
        'center_lat': center_lat,
        'left_lon': left_lon,
        'right_lon': right_lon,
        'bottom_lat': bottom_lat,
        'top_lat': top_lat
    })

# 将网格单元格保存为CSV文件
grid_df = pd.DataFrame(grid_cells_with_center)
grid_df.to_csv('grid_cells.csv', index=False)

# 可视化网格
plt.figure(figsize=(12, 8))
plt.xlabel('经度')
plt.ylabel('纬度')
plt.title('离散化网格可视化')

# 绘制网格
for cell in grid_cells_with_center:
    # 绘制经度网格线
    plt.axvline(x=cell['left_lon'], color='gray', linestyle='--', linewidth=0.5)
    plt.axvline(x=cell['right_lon'], color='gray', linestyle='--', linewidth=0.5)
    # 绘制纬度网格线
    plt.axhline(y=cell['bottom_lat'], color='gray', linestyle='--', linewidth=0.5)
    plt.axhline(y=cell['top_lat'], color='gray', linestyle='--', linewidth=0.5)

# 绘制中心点
for index, row in df.iterrows():
    plt.scatter(row['经度'], row['纬度'], color='blue', marker='o', s=10)

plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()