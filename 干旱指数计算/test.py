import pandas as pd

# 对每个场景文件进行处理
for i in range(3):
    file_name = f'场景/场景{i}.csv'
    data = pd.read_csv(file_name)

    columns_to_normalize = ['降水量_avg', '相对湿度 (%)_avg', '温度_avg']

    for column in columns_to_normalize:
        min_val = data[column].min()
        max_val = data[column].max()
        data[column + '_normalized'] = (data[column] - min_val) / (max_val - min_val)
    normalized_columns = [col + '_normalized' for col in columns_to_normalize]

    weights = {
        '降水量_avg_normalized': 0.378,
        '相对湿度 (%)_avg_normalized': 0.324,
        '温度_avg_normalized': 0.298
    }

    # 对需要反转的列进行反转
    reversed_columns = ['降水量_avg_normalized', '相对湿度 (%)_avg_normalized']  # 假设需要反转温度列的值
    for column in reversed_columns:
        data[column] = 1 - data[column]

    # 确保权重总和为1
    total_weight = sum(weights.values())
    for key in weights:
        weights[key] /= total_weight

    # 计算加权均值
    data['加权均值'] = sum(data[col] * weights[col] for col in normalized_columns)
    normalized_file_name = f'场景{i}_normalized.csv'
    data.to_csv(normalized_file_name, index=False)
    print(f'已将 {file_name} 归一化后保存为 {normalized_file_name}')