import pandas as pd

try:
    df = pd.read_csv('格式化后的数据.csv')
    print("读取成功！")
    print(f"数据形状：{df.shape}")
    print(f"列名：{list(df.columns)}")
    print("\n前5行数据：")
    print(df.head())
except Exception as e:
    print(f"读取失败：{e}")
