# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import re


file_path = 'D:/researches/database/CAPU/xingzhezuyin.csv'
df = pd.read_csv(file_path, error_bad_lines=False, names=['bid', 'tid', 'pid', 'title', 'author', 'text', 'replytime', 'updatetime', 'sig'])


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

result_df.to_csv('D:/researches/database/CAPU/output.csv', index=False)

# 将replytime列转换为数字，如果无法转换，则设为NaN
result_df['replytime'] = pd.to_numeric(result_df['replytime'], errors='coerce')

# 筛选包含 NaN 值的行
nan_rows = result_df[result_df['replytime'].isna() | result_df['updatetime'].isna()]

# 删除包含NaN值的行
nan_result_df = result_df.dropna()

# 删除格式不符合Unix时间戳的数据行
nan_result_df = nan_result_df[(nan_result_df['replytime'] >= 1035290648) & (nan_result_df['replytime'] <= 1699893811)]
nan_result_df['replytime'] = pd.to_datetime(nan_result_df['replytime'], unit='s').dt.strftime('%Y%m%d')
nan_result_df['updatetime'] = pd.to_datetime(nan_result_df['updatetime'], unit='s').dt.strftime('%Y%m%d')

# 去除text中的HTML标签
nan_result_df['text'] = nan_result_df['text'].apply(lambda x: re.sub(r'<.*?>', '', str(x)))

# 筛选包含“自述”关键词的行数据
df_self_description = nan_result_df[nan_result_df['title'].str.contains('自述', na=False, case=False)]
df_self_description_nan = result_df[result_df['title'].str.contains('自述', na=False, case=False)]

# 将text列按tid分组，同时保留其他变量的最小值
grouped_self_df = df_self_description.groupby('tid').agg({
    'pid': 'min',
    'title': 'first',
    'author': 'first',
    'text': ' '.join,  # 使用空格连接text列中的文本内容
    'replytime': 'min',
    'updatetime': 'max',
    'sig': 'first'
}).reset_index()

# 删除pid大于1,text<400的行
df_self_pid1 = grouped_self_df[grouped_self_df['pid'] <= 1]
df_self_pidtext400 = df_self_pid1[df_self_pid1['text'].str.len() >= 600]

# 筛多年自述，在 'title' 列中筛选包含指定关键词的行
keywords = ["二年", "三年", "四年"]
df_2nd_yearpre = df_self_pidtext400[df_self_pidtext400['title'].str.contains('|'.join(keywords), na=False, case=False)]
# 按 'author' 列进行分组，并保留每个分组中除了 'tid' 最小的行以外的其他行
df_2nd_yearpre2 = df_self_pidtext400.groupby('author').apply(lambda group: group[group['tid'] != group['tid'].min()] if len(group) > 1 else pd.DataFrame())
# 使用 concat 方法按行连接两个表格，并移除重复行
self2nd_df = pd.concat([df_2nd_yearpre, df_2nd_yearpre2]).drop_duplicates()

#筛一年自述
# 将两个 DataFrame 合并，并使用 '_merge' 列指示哪些行在两个 DataFrame 中存在
merged_df = pd.merge(df_self_pidtext400, self2nd_df, on=['tid', 'pid', 'title', 'author', 'text', 'replytime', 'updatetime', 'sig'], how='left', indicator=True)

# 从 merged_df 中选择只在 df_self_pidtext400 中存在的行
self1st_df = merged_df[merged_df['_merge'] == 'left_only']

# 删除 '_merge' 列
self1st_df = self1st_df.drop(columns=['_merge'])

# 现在，result_df_minus_self2nd 包含了只在 df_self_pidtext400 中存在的行
