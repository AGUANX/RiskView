import numpy as np
import os

import pandas as pd


# ---------- 1. 分级函数（nan 自动传播） ----------
def alt_grade(arr):
    return np.piecewise(
        arr,
        [arr <= 100, arr >= 400],
        [5, 1, lambda x: 5 - (x - 100) / 300 * 4]
    )

def twi_grade(arr):
    return np.piecewise(
        arr,
        [arr <= 7, arr >= 10],
        [5, 1, lambda x: 5 - (x - 7) / 3 * 4]
    )

def slope_aspect(dem, cell_size=30):
    dy, dx = np.gradient(dem, cell_size)
    slope_rad = np.arctan(np.sqrt(dx**2 + dy**2))
    slope_deg = np.degrees(slope_rad)

    aspect_rad = np.arctan2(-dy, dx)
    aspect_deg = np.degrees(aspect_rad)
    aspect_deg = np.where(aspect_deg < 0, aspect_deg + 360, aspect_deg)

    # 1. 平地判定
    flat = (slope_deg < 0.1) | np.isnan(slope_deg)
    aspect_deg = np.where(flat, -1, aspect_deg)

    # 2. 把原始 nan 区域（原-999）重新置回 nan，不参与后续分级
    nan_mask = np.isnan(dem)
    slope_deg = np.where(nan_mask, np.nan, slope_deg)
    aspect_deg = np.where(nan_mask, np.nan, aspect_deg)

    return slope_deg, aspect_deg

def slope_grade(arr):
    return np.piecewise(
        arr,
        [arr >= 30, arr <= 5],
        [5, 1, lambda x: 1 + (x - 5) / 25 * 4]
    )

def aspect_grade(arr):
    grade = np.full_like(arr, 3, dtype=float)
    south = (arr >= 135) & (arr <= 225)
    grade = np.where(south, 5, grade)
    grade = np.where(arr == -1, 1, grade)
    return grade

# ---------- 2. 主流程 ----------
def main(dem_file, twi_file, out_dir, cell_size=30):
    # 读入并把 -999 变成 nan
    dem = pd.read_csv(dem_file, header=None).replace(-999, np.nan).to_numpy()
    twi = pd.read_csv(twi_file, header=None).replace(-999, np.nan).to_numpy()
    dem = np.where(dem == -999, np.nan, dem)
    twi = np.where(twi == -999, np.nan, twi)

    print(dem, twi)
    assert dem.shape == twi.shape, 'DEM 和 TWI 尺寸不一致'

    slope, aspect = slope_aspect(dem, cell_size)

    alt_g    = alt_grade(dem)
    twi_g    = twi_grade(twi)
    slope_g  = slope_grade(slope)
    aspect_g = aspect_grade(aspect)

    # 写出：先把 nan 替换成 -999 字符串
    for name, arr in zip(['alt_g', 'slope_g', 'aspect_g', 'twi_g'],
                         [alt_g, slope_g, aspect_g, twi_g]):
        out_path = os.path.join(out_dir, f'{name}.csv')
        # 临时把 nan 变成 -999 字符串
        with open(out_path, 'w') as f:
            for row in arr:
                line = ','.join('-999' if np.isnan(v) else f'{v:.4f}' for v in row)
                f.write(line + '\n')
        print(f'{name}.csv 已生成')

# ---------- 3. 运行 ----------
if __name__ == '__main__':
    main('nanling_final_matrix.csv', 'twi_irregular_matrix.csv', 'out')