import pandas as pd

# 1. 读取您的Excel文件
df = pd.read_excel('原始数据.xlsx')

# 2. 使用pandas的to_csv方法，它会自动处理引号
#    quoting=1 参数代表“为所有非数字字段添加引号”，这是最保险的做法。
df.to_csv('格式化后的数据.csv', index=False, encoding='utf-8-sig', quoting=1)

print("处理完成！文件已保存为 '格式化后的数据.csv'")
