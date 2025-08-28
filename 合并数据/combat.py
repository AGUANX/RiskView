import pandas as pd



def combat(file1, file2, file3, year):
    # 读取两个 CSV 文件
    pre_df = pd.read_csv(file1)
    rh_df = pd.read_csv(file2)
    tmp_df = pd.read_csv(file3)

    pre_df.rename(columns={'月份': '年份'}, inplace=True)


    # 基于经纬度对齐数据
    merged_df = pd.merge(pre_df, rh_df, on=['经度', '纬度', '时间步长'], suffixes=('降水量', '相对湿度'))
    merged_df = pd.merge(merged_df, tmp_df, on=['经度', '纬度', '时间步长'], suffixes=('_前', '温度'))

    # 保存合并后的数据
    merged_df.to_csv('merged/merged_data_' + year + '.csv', index=False)


years = [f"{i:02d}" for i in range(3, 21)]
for year in years:
    file1 = 'deal/deal/save_pre/pre_data_20' + year + '.csv'
    file2 = 'deal/deal/save_rh/extracted_20' + year + '01_rh_data.csv'
    file3 = 'deal/deal/save_tmp/tmp_data_20' + year + '.csv'

    combat(file1, file2, file3, year)