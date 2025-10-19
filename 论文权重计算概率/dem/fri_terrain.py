#!/usr/bin/env python
import os
import re
import numpy as np
import pandas as pd

# ---------- 1. 权重表 ----------
W = {
    'alt': 0.0303,
    'slope': 0.0193,
    'aspect': 0.0103,
    'twi': 0.0461
}

# ---------- 2. 工具 ----------
def find_factor_csv(root_dir, keys):
    """返回 dict{key: 第一个匹配到的csv绝对路径}"""
    found = {}
    for dirpath, _, files in os.walk(root_dir):
        for f in files:
            if not f.lower().endswith('.csv'):
                continue
            low = f.lower()
            for k in keys:
                if k in low and k not in found:
                    found[k] = os.path.join(dirpath, f)
    return found

def load_replace(fp):
    """读csv并把-999→nan"""
    return pd.read_csv(fp, header=None).replace(-999, np.nan).to_numpy()

# ---------- 3. 主流程 ----------
def main(scan_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    found = find_factor_csv(scan_dir, W.keys())
    if len(found) != 4:
        missing = set(W.keys()) - set(found.keys())
        print(f'缺少因子文件: {missing} ，程序终止。')
        return
    print(found)

    # 读入
    data = {k: load_replace(fp) for k, fp in found.items()}
    base_key = 'alt'  # 任取一个做形状校验
    base_shape = data[base_key].shape
    for k, arr in data.items():
        if arr.shape != base_shape:
            print(f'{k}.csv 尺寸不一致，程序终止。')
            return

    # 无效掩膜
    mask = np.zeros(base_shape, dtype=bool)
    for arr in data.values():
        mask |= np.isnan(arr)

    # 加权求和
    fri = np.zeros(base_shape)
    for k, w in W.items():
        fri += data[k] * w
    fri = np.where(mask, -999, fri)

    # 保存
    out_file = os.path.join(out_dir, 'fri_terrain.csv')
    np.savetxt(out_file, fri, delimiter=',', fmt='%.4f')
    print(f'合并完成 → {out_file}')

# ---------- 4. 入口 ----------
if __name__ == '__main__':
    main('./out', '.')
