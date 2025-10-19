import numpy as np
import pandas as pd


def main():
    folder = 'data/task_regions_final/task_regions_final/'
    out_folder = 'data/output/'
    for i in range(1, 187):
        file_name = 'region_' + str(i) + '_grid' + '.csv处理'
        df = pd.read_csv(folder + file_name)
        df.replace(-999, np.nan, inplace=True)
        df.to_csv(out_folder + file_name, index=False)

if __name__ == '__main__':
    main()