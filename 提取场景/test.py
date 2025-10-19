import pandas as pd

data = pd.read_csv('result.csv')

mouth_result = pd.read_csv('month_clustering_results.csv')

for i in range(3):
    filtered_df = mouth_result[mouth_result['月份聚类标签'] == i]
    merged_df = pd.DataFrame(columns=['经度', '纬度'])
    for mouth in filtered_df['月份']:
        mouth_str = str(mouth)
        df = data[data['月份'] == mouth]
        if merged_df.empty:
            merged_df = df.copy()
        else:
            merged_df = pd.merge(merged_df, df, on=['经度', '纬度'], suffixes=('', '_' + mouth_str))
    print(merged_df)
    numeric_columns = ['降水量', '相对湿度 (%)', '温度']  # 这些是数值列
    for col in numeric_columns:
        # 获取所有相关的列名（例如，'降水量', '降水量_temp', '降水量_temp_1', 等）
        related_cols = [c for c in merged_df.columns if c.startswith(col)]
        # 计算平均值
        merged_df[col + '_avg'] = merged_df[related_cols].mean(axis=1)
        # 删除临时列
        merged_df.drop(related_cols, axis=1, inplace=True)
    selected_columns = ['经度', '纬度', '降水量_avg', '相对湿度 (%)_avg', '温度_avg']
    merged_df[selected_columns].to_csv('聚类月份' + str(i) + '.csv处理', index=False)
