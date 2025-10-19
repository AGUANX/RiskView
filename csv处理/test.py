import os

import numpy as np
import pandas as pd

BASE_PATH = './场景'
file_names = os.listdir(BASE_PATH)
print(file_names)

for file_name in file_names:
    file_path = os.path.join(BASE_PATH, file_name)
    df = pd.read_csv(file_path)
    df['id'] = np.arange(1, len(df) + 1)
    print(df)
    df.to_csv(file_path, index=False)
