import os
import re
import pandas as pd

left_dir  = r'.\save_tmp'          # 年数据文件夹
right_dir = r'.\vegetation_data_by_month'  # 月数据文件夹
os.makedirs('output', exist_ok=True)        # 结果保存目录

months = [f"{i:02d}" for i in range(1, 13)]

for filename in os.listdir(left_dir):
    if filename.endswith('.csv'):
        left_path = os.path.join(left_dir, filename)
        left = pd.read_csv(left_path)          # 必须有 region_id 和年份列
        year = re.search(r'(\d{4})', filename).group(1)  # 从文件名拿年份

        # 收集该年所有月份文件
        df_month_list = []
        for month in months:
            right_name = f'{year}_{month}.csv'
            right_path = os.path.join(right_dir, right_name)
            if not os.path.exists(right_path):   # 缺月文件直接跳过
                continue
            month_df = pd.read_csv(right_path)
            month_df['年份'] =  year + month      # 200301
            df_month_list.append(month_df)

        if not df_month_list:                   # 该年无月数据
            continue
        month_all = pd.concat(df_month_list, ignore_index=True)

        name_map = {'longitude_x': 'longitude',
                       'latitude_x': 'latitude',
                       'region_id': 'region_id',
                       'tmp': 'tmp',
                       'ndvi': 'ndvi',
                       '年份': '年份'}  # 写你实际要的

        # 合并
        left['年份'] = left['年份'].astype(str)
        month_all['年份'] = month_all['年份'].astype(str)
        merged = pd.merge(left, month_all, on=['region_id', '年份'], how='left')
        merged = merged[list(name_map.keys())].rename(columns=name_map)
        out_file = os.path.join('output', f'{year}_tmp_navi.csv')
        merged.to_csv(out_file, index=False, encoding='utf-8-sig')
        print(f'{year} 完成 → {out_file}')