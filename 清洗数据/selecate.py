import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
import os


# # 设置读取文件路径
# folder_path = './降雨量加月均温度/pre/extracted_pre_data_20'
# back_path = '.csv'  # 替换为你的文件夹路径
# years = [f"{i:02d}" for i in range(3, 21)]
#
# # 保存路径
# save_path = './save_pre/pre_data_20'
# save_file = '.csv'
# 设置读取文件路径
folder_path = '降雨量加月均温度/tmp_normalized/extracted_tmp_data_normalized_20'
back_path = '.csv'  # 替换为你的文件夹路径
years = [f"{i:02d}" for i in range(3, 21)]

# 保存路径
save_path = 'save_tmp/tmp_data_20'
save_file = '.csv'

# 要插值的经纬度列表
points_to_interpolate = pd.read_csv("all_unique_locations.csv")


for year in years:
    # 原始气象数据
    original_data = pd.read_csv(folder_path + year + back_path)
    dataframes = []
    for mouth in range(1,13):
        # 假设属性名是 'score'
        filtered_df = original_data[original_data['时间步长'] == mouth]


        # 提取原始数据中的经度、纬度和温度
        original_lon_lat = filtered_df.iloc[:, 1:3].values
        original_temp = filtered_df.iloc[:, 3].values

        # 计算每个插值点到原始点的距离
        distances = cdist(points_to_interpolate, original_lon_lat)

        # 找出每个插值点的最近邻点索引（例如取最近的 4 个点）
        n_neighbors = 4
        nearest_indices = np.argsort(distances, axis=1)[:, :n_neighbors]

        # 计算每个插值点的插值温度
        interpolated_temps = np.zeros(points_to_interpolate.shape[0])
        for i in range(points_to_interpolate.shape[0]):
            neighbor_temps = original_temp[nearest_indices[i]]
            # 加权
            interpolated_temps[i] = np.mean(neighbor_temps)

        # 将结果与插值点组合
        interpolated_points = np.hstack((points_to_interpolate, interpolated_temps.reshape(-1, 1)))

        interpolated_points = pd.DataFrame(interpolated_points)
        interpolated_points['时间步长'] = mouth - 1
        interpolated_points['年份'] = '20' + year + "{:02d}".format(mouth)
        dataframes.append(interpolated_points)
    # 保存成文件
    df = pd.concat(dataframes, ignore_index=True)
    os.makedirs('save_tmp', exist_ok=True)
    df.to_csv(save_path + year + save_file, index=False)