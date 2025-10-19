#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
批量把 region_risk_score.csv 中的四列拼到
月份01~12/聚类*.csv
python batch_merge_risk.py
"""
import pandas as pd
from pathlib import Path

# ---------- 1. 配置 ----------
ROOT_DIR       = Path(r'.')                 # 根目录（月份01~12所在目录）
RISK_FILE      = ROOT_DIR / 'region_risk_score.csv'
MONTH_FOLDERS  = [ROOT_DIR / '月份' / f'月份{i:02d}' for i in range(1, 13)]
CLUSTER_GLOB   = '聚类*.csv'                # 匹配规则

# 要追加的列
RISK_COLS      = ['region_id',
                  'total_score', 'fri_terrain']

# ---------- 2. 读风险表 ----------
risk = pd.read_csv(RISK_FILE, usecols=RISK_COLS)

# ---------- 3. 遍历处理 ----------
for mdir in MONTH_FOLDERS:
    if not mdir.is_dir():
        print(f'跳过不存在目录：{mdir}')
        continue
    for csv_path in mdir.glob(CLUSTER_GLOB):
        print(f'处理 {csv_path} ...')
        left = pd.read_csv(csv_path)
        out  = left.merge(risk, on='region_id', how='left')
        # 原地覆盖，如需另存可改名字
        out.to_csv(csv_path, index=False)
print('全部完成！')