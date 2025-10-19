import numpy as np
import pandas as pd

# ---------------- 参数区（按需修改） ----------------
road_file      = 'center_match_pixel_risk.csv'        # 含 center_to_road_m 的文件
resident_file  = 'region_summary_resident.csv'    # 含 avg_resident_dist_m 的文件
out_file       = 'region_risk_score.csv'

# 权重（加起来等于 1 即可）
w_road     = 0.0707
w_resident = 0.2122

# 分段打分规则：闭开区间左闭右开，(lower, upper] -> score
# 注意：最左/最右区间用 -inf / +inf 兜底
road_bins = [-float('inf'), 300, 1200, float('inf')]
road_scores = [5, 1, 1]          # 对应 <=300, (300,1200], >1200

resident_bins = [-float('inf'), 400, 1600, float('inf')]
resident_scores = [5, 1, 1]      # 对应 <=400, (400,1600], >1600
# --------------------------------------------------

def score_by_bins(x, bins, scores):
    """
    连续线性评分函数，区间规则 (lower, upper]（左开右闭）。
    x       : 标量、数组或 pandas Series
    bins    : 升序边界，可含 -np.inf / np.inf，长度 = len(scores)+1
    scores  : 每个区间对应的分数，长度 = len(bins)-1
    返回    : 与 x 同形状的连续分数（float）
    """
    bins = np.asarray(bins, dtype=float)
    scores = np.asarray(scores, dtype=float)

    # 构造插值节点：右边界 -> 对应分数，-inf 用第一个分数，+inf 用最后一个分数
    x_vals = np.r_[-np.inf, bins[1:-1], np.inf]
    y_vals = np.r_[scores[0], scores]

    # 线性插值（np.interp 自动处理 inf）
    if isinstance(x, pd.Series):
        return pd.Series(np.interp(x.values, x_vals, y_vals), index=x.index, name=x.name+'_score')
    return np.interp(x, x_vals, y_vals)

# 1. 读取数据
df_road = pd.read_csv(road_file)
df_res  = pd.read_csv(resident_file)

# 2. 计算单指标得分
df_road['road_score'] = score_by_bins(df_road['center_to_road_m'],
                                      road_bins, road_scores)
df_res['resident_score'] = score_by_bins(df_res['avg_resident_dist_m'],
                                         resident_bins, resident_scores)

# 3. 合并
df_merge = pd.merge(df_road[['region_id', 'road_score']],
                    df_res[['region_id', 'resident_score']],
                    on='region_id', how='outer')

# 4. 加权总分
df_merge['total_score'] = (w_road * df_merge['road_score'] +
                           w_resident * df_merge['resident_score'])

# 5. 输出
df_merge.to_csv(out_file, index=False)
print('Done! 结果已写入', out_file)