import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定黑体
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

for i in range(3):
    # 读取 CSV 文件
    file_name = '场景_with_flag' + str(i) + '.csv'  # 替换为你的文件路径
    data = pd.read_csv(file_name)

    # 创建一个散点图
    plt.figure(figsize=(12, 8))
    scatter = sns.scatterplot(
        x='经度',
        y='纬度',
        hue='标记',
        palette={1: 'red', 0: 'blue'},
        sizes=(20, 200),
        data=data
    )

    # 添加图例和标题
    plt.title('场景' + str(i) + '区域可视化（前30%均值标记为1）')
    plt.xlabel('经度')
    plt.ylabel('纬度')
    plt.legend(title='标记', loc='upper right')

    # 显示图形
    plt.show()