# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd

file_path = 'D:/researches/database/CAPU/xingzhezuyin.csv'
df = pd.read_csv(file_path, on_bad_lines='skip', names=['bid', 'tid', 'pid', 'title', 'author', 'text', 'replytime', 'updatetime', 'sig'])

# 将 'tid' 和 'pid' 列转换为数值型数据
df['tid'] = pd.to_numeric(df['tid'], errors='coerce')
df['pid'] = pd.to_numeric(df['pid'], errors='coerce')

# 删除包含非数字的行
df = df.dropna(subset=['tid', 'pid'])

# 将 'tid' 和 'pid' 限制在 1 到 10000 范围内
df = df[df['tid'].between(1, 10000) & df['pid'].between(1, 10000)]

# 根据 tid、pid、author 进行排序
df_sorted = df.sort_values(by=['tid', 'pid', 'author'], ascending=[True, True, True])

# 按照 'tid' 列进行分组
grouped = df.groupby('tid')

# 保留每个组中 pid=1 对应的 author
selected_rows = []
for name, group in grouped:
    pid1_author = group.loc[group['pid'] == 1, 'author'].values
    selected_rows.extend(group[group['author'].isin(pid1_author)].values)

# 将结果转换为DataFrame
result_df = pd.DataFrame(selected_rows, columns=df.columns)