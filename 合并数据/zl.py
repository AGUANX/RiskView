import pandas as pd
import glob

def delete_year_column():
    # 获取当前目录下所有 CSV 文件
    csv_files = glob.glob('merged/merged_data_*.csv处理')

    for file in csv_files:
        # 读取 CSV 文件
        df = pd.read_csv(file)

        # 删除“年份降水量”列（如果存在）
        if '年份降水量' in df.columns:
            df.drop('年份降水量', axis=1, inplace=True)

            # 覆盖写回原文件
            df.to_csv(file, index=False)
            print(f"已删除文件 {file} 中的“年份降水量”列")
        else:
            print(f"文件 {file} 中不存在“年份降水量”列")


        # 删除“年份”列（如果存在）
        if '年份相对湿度' in df.columns:
            df.drop('年份相对湿度', axis=1, inplace=True)

            # 覆盖写回原文件
            df.to_csv(file, index=False)
            print(f"已删除文件 {file} 中的“年份相对湿度”列")
        else:
            print(f"文件 {file} 中不存在“年份相对湿度”列")

delete_year_column()