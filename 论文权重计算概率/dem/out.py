#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
按 region 统计 fri_terrain.csv 矩阵中对应像元的平均值
python calc_region_terrain_mean_matrix.py
"""
import os, csv, numpy as np

# ========== 1. 参数 ==========
REGION_CSV  = 'total_pixels_with_region(1).csv'
TERRAIN_CSV = 'fri_terrain.csv'
OUT_CSV     = 'region_terrain_mean.csv'

# 无效值标记
NO_DATA = -999.0

# ========== 2. 读 region 文件 ==========
# 收集每个 region 的坐标集合：{region_id: {(col,row), ...}}
coord_by_region = {}
with open(REGION_CSV, newline='') as f:
    reader = csv.DictReader(f)
    for rec in reader:
        rid = int(rec['region_id'])
        c   = int(rec['col'])
        r   = int(rec['row'])
        coord_by_region.setdefault(rid, set()).add((c, r))

regions = sorted(coord_by_region)
print(f'loaded {len(coord_by_region)} regions')

# ========== 3. 初始化累加器 ==========
sum_by_region = {rid: 0.0 for rid in regions}
cnt_by_region = {rid: 0   for rid in regions}

# ========== 4. 逐行扫描 terrain 矩阵 ==========
with open(TERRAIN_CSV) as f:
    for row_idx, line in enumerate(f):
        line = line.strip()
        if not line:               # 跳过空行
            continue
        # 按逗号拆成浮点数组
        vals = np.fromstring(line, sep=',', dtype=np.float32)
        # 只关心本行那些落在某个 region 里的列
        for col_idx, val in enumerate(vals):
            if val == NO_DATA:     # 跳过无效
                print("格式不对")
                continue
            # 看这对 (col,row) 属于哪个 region
            for rid, coords in coord_by_region.items():
                if (col_idx, row_idx) in coords:
                    sum_by_region[rid] += float(val)
                    cnt_by_region[rid] += 1
                    break          # 一个像素理论上只属于一个 region

# ========== 5. 输出结果 ==========
with open(OUT_CSV, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['region_id', 'count', 'mean_value'])
    for rid in regions:
        s = sum_by_region[rid]
        n = cnt_by_region[rid]
        mean = np.nan if n == 0 else s / n
        w.writerow([rid, n, f'{mean:.6f}'])

print(f'done -> {OUT_CSV}')