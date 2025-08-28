import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from shapely.geometry import Polygon, Point, LineString

# 读取边界点和中心点数据
boundary_df = pd.read_excel('南岭.xlsx')  # 替换为你的边界点CSV文件路径
center_df = pd.read_csv('all_unique_locations.csv')     # 替换为你的中心点CSV文件路径

# 将数据转换为NumPy数组
boundary_points = boundary_df[['经度', '纬度']].values
center_points = center_df[['经度', '纬度']].values

# 创建边界多边形
boundary_polygon = Polygon(boundary_points)

# 生成Voronoi图
vor = Voronoi(center_points)

# 绘制基础Voronoi图
fig, ax = plt.subplots(figsize=(10, 10))
voronoi_plot_2d(vor, ax=ax, show_vertices=False, line_colors='blue', line_width=0.5, line_alpha=0.7)

# 获取Voronoi区域并进行边界裁剪
regions = []
region_boundaries = []  # 保存每个区域的边界点
center_indices = []     # 保存每个区域对应的中心点索引

for region_index in vor.point_region:
    if region_index < len(center_points):
        region = vor.regions[region_index]
        if not -1 in region:
            # 创建Voronoi区域的多边形
            polygon = Polygon([vor.vertices[i] for i in region])
            # 裁剪到边界
            clipped_polygon = boundary_polygon.intersection(polygon)
            regions.append(clipped_polygon)
            # 保存区域的边界点
            if isinstance(clipped_polygon, Polygon):
                region_boundaries.append(list(clipped_polygon.exterior.coords))
            elif isinstance(clipped_polygon, LineString):
                region_boundaries.append(list(clipped_polygon.coords))
            # 保存对应的中心点索引
            center_indices.append(region_index)
    else:
        print(f"Warning: region_index {region_index} is out of bounds for center_points")

# 绘制原始边界
ax.add_patch(plt.Polygon(boundary_points, fill=False, color='red', linewidth=2))

# 绘制裁剪后的Voronoi区域
for region in regions:
    if isinstance(region, Polygon):
        x, y = region.exterior.xy
        ax.plot(x, y, color='black', linewidth=1)
    elif isinstance(region, LineString):
        x, y = region.xy
        ax.plot(x, y, color='black', linewidth=1)

plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.title("Voronoi Diagram within Irregular Boundary")
plt.show()

# 保存Voronoi区域的边界点和中心点信息
voronoi_data = []
for i, boundary in enumerate(region_boundaries):
    center_idx = center_indices[i]
    center_point = center_points[center_idx]
    voronoi_data.append({
        'center_index': center_idx,
        'center_longitude': center_point[0],
        'center_latitude': center_point[1],
        'boundary': boundary
    })

# 将Voronoi数据保存到CSV文件，将边界点保存为字符串形式
voronoi_df = pd.DataFrame(voronoi_data)
voronoi_df['boundary'] = voronoi_df['boundary'].apply(lambda x: str(x))
voronoi_df.to_csv('voronoi_boundaries.csv', index=False)

print("Voronoi区域的边界点和中心点信息已保存到 'voronoi_boundaries.csv'")