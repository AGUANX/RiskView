import os

import pandas as pd

dir = "聚类月份/"

OUTDIR = "月份/月份"


# 读取气象数据
data = pd.read_csv("merged.csv")

mouths = [f"{i:02d}" for i in range(1, 13)]


for i in mouths:
    result = pd.read_csv(dir + str(int(i)) + 'result.csvcluster_count_per_month.csv')
    l = 0
    for j in range(result["月份聚类标签"].unique().shape[0]):
        years = result[result["月份聚类标签"] == j]
        merged_df = pd.DataFrame(columns=['longitude', 'latitude'])
        for year in years["年份"]:
            time = str(year)
            print(time)
            print(data.dtypes)
            df = data[data['年份'] == int(time)]
            print(df)
            if merged_df.empty:
                merged_df = df.copy()
            else:
                merged_df = pd.merge(merged_df, df, on=['longitude', 'latitude'], suffixes=('', '_' + time))
        numeric_columns = ['tmp', 'ndvi']  # 这些是数值列
        for col in numeric_columns:
            # 获取所有相关的列名（例如，'降水量', '降水量_temp', '降水量_temp_1', 等）
            related_cols = [c for c in merged_df.columns if c.startswith(col)]
            # 计算平均值
            merged_df[col + '_avg'] = merged_df[related_cols].mean(axis=1)
            # 删除临时列
            merged_df.drop(related_cols, axis=1, inplace=True)
        selected_columns = ['longitude', 'latitude', 'tmp_avg', 'ndvi_avg', 'region_id']
        output_dir = OUTDIR + str(i)
        os.makedirs(output_dir, exist_ok=True)
        merged_df[selected_columns].to_csv(output_dir + "/" + '聚类月份' + str(l) + '.csv', index=False)
        l += 1

