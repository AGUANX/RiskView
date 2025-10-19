import pandas as pd
from pathlib import Path

dir_path = Path(r'output')          # 文件夹路径
dfs = [pd.read_csv(f) for f in dir_path.glob('*.csv')]
big_df = pd.concat(dfs, ignore_index=True)      # 纵向拼接
big_df.to_csv(dir_path / 'merged.csv', index=False)