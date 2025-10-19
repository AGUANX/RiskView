#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量给 月份01~12/聚类*.csv 新增 score 列
python batch_add_score.py
"""
import pandas as pd
from pathlib import Path

# ---------- 1. 配置 ----------
ROOT_DIR       = Path(r'.')                # 根目录（含月份01~12）
MONTH_FOLDERS  = [ROOT_DIR / '月份' / f'月份{i:02d}' for i in range(1, 13)]
CLUSTER_GLOB   = '聚类*.csv'


# ---------- 2. 评分函数 ----------
def calc_score(df: pd.DataFrame) -> pd.Series:
    # tmp 评分
    tmp = df['tmp_avg']
    tmp_score = pd.Series(index=tmp.index, dtype=float)
    tmp_score[tmp > 31] = 5
    tmp_score[tmp < 5] = 1
    mask = (5 <= tmp) & (tmp <= 31)
    tmp_score[mask] = (tmp[mask] - 5) / (31 - 5) * 4 + 1

    # ndvi 评分
    ndvi = df['ndvi_avg']
    ndvi_score = pd.Series(index=ndvi.index, dtype=float)
    ndvi_score[ndvi > 0.75] = 1
    ndvi_score[ndvi <= 0]   = 5
    mask = (0 < ndvi) & (ndvi <= 0.75)
    ndvi_score[mask] = (0.75 - ndvi[mask]) / 0.75 * 4 + 1

    return 0.1636 * tmp_score + 0.4476 * ndvi_score + df['total_score'] + df['fri_terrain']


# ---------- 3. 评分函数 ----------
def calc_level(df: pd.DataFrame) -> pd.Series:
    tmp = df['score']
    tmp_score = pd.Series(index=tmp.index, dtype=float)
    tmp_score[tmp >= 1.9] = 1
    tmp_score[tmp < 1.9] = 0
    return tmp_score

# ---------- 4. 批量处理 ----------
for mdir in MONTH_FOLDERS:
    if not mdir.is_dir():
        continue
    for csv_path in mdir.glob(CLUSTER_GLOB):
        print(f'处理 {csv_path}')
        df = pd.read_csv(csv_path)
        # 计算并新增
        df['score'] = calc_score(df)
        df['rick_level'] = calc_level(df)
        # 保存（原地覆盖）
        df.to_csv(csv_path, index=False)
print('全部完成！')