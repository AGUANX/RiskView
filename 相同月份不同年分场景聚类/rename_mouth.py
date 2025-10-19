import pandas as pd

data = pd.read_csv("cluster_count_per_month.csv")

data["年份"] = data["时间"].astype(str).str[:4]

data["月份"] = data["时间"].astype(str).str[4:]


data.to_csv("new_data.csv处理", index=False)