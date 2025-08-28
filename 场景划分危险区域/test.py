import pandas as pd



for i in range(3):
    # 读取 CSV 文件

    data = pd.read_csv('场景' + str(i) + '_normalized' + '.csv')

    # 计算均值的前30%分位数
    top_30_percentile = data['加权均值'].quantile(0.7)

    # 新增一列标记前30%的行
    data['标记'] = data['加权均值'].apply(lambda x: 1 if x >= top_30_percentile else 0)

    # 保存结果到新的 CSV 文件
    output_file_name = '场景_with_flag' + str(i) + '.csv'
    data.to_csv(output_file_name, index=False)

    # 显示结果
    print(data)