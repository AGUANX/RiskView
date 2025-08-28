import pandas as pd
from shapely.geometry import Polygon, Point
from scipy.spatial import Voronoi, voronoi_plot_2d
import numpy as np

# 读取保存的Voronoi数据
voronoi_df = pd.read_csv('voronoi_boundaries.csv')

# 将字符串形式的边界点转换为列表
voronoi_df['boundary'] = voronoi_df['boundary'].apply(eval)

# 读取原始边界点和中心点数据
boundary_df = pd.read_excel('南岭.xlsx')
boundary_points = boundary_df[['经度', '纬度']].values
boundary_polygon = Polygon(boundary_points)

center_df = pd.read_csv('all_unique_locations.csv')
center_points = center_df[['经度', '纬度']].values

# 验证每个Voronoi区域
for idx, row in voronoi_df.iterrows():
    boundary = row['boundary']
    center_point = Point(row['center_longitude'], row['center_latitude'])

    # 构造多边形
    try:
        region_polygon = Polygon(boundary)
    except:
        print(f"Warning: region {idx} has an invalid boundary.")
        continue

    # 面积验证
    if not region_polygon.is_valid:
        print(f"Warning: region {idx} has an invalid geometry.")
        continue

    # 计算面积
    saved_area = region_polygon.area

    # 重新计算该区域的面积（用于对比）
    vor = Voronoi(center_points)
    region_index = row['center_index']
    vor_region = vor.regions[vor.point_region[region_index]]
    if -1 in vor_region:
        print(f"Warning: region {idx} is unbounded.")
        continue
    original_polygon = Polygon([vor.vertices[i] for i in vor_region])
    clipped_polygon = boundary_polygon.intersection(original_polygon)
    recalculated_area = clipped_polygon.area

    # 面积对比
    if not np.isclose(saved_area, recalculated_area, rtol=1e-3):
        print(
            f"Warning: area mismatch for region {idx}. Saved area: {saved_area}, Recalculated area: {recalculated_area}")

    # 包含关系验证
    if not region_polygon.contains(center_point):
        print(f"Warning: center point of region {idx} is not within the saved boundary.")

print("Validation completed.")