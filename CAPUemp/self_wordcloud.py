from CAPUemp.dataclean import self1st_df
from CAPUemp.dataclean import nan_result_df
from CAPUemp.dataclean import self2nd_df
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import re


# 读取词表文件
with open(r'D:\researches\Projects\CAPUemo\weibo-analysis-and-visualization\weibo-analysis-and-visualization\dict\哈工大停用词表.txt', 'r', encoding='utf-8') as file:
    wordlist = file.read().splitlines()


def remove_english(text):
    # 使用正则表达式匹配英文字符，并替换为空字符串
    return re.sub(r'[a-zA-Z]', '', text)

for i in [self2nd_df,self1st_df,nan_result_df]:
    # 处理 'text' 列，例如去除 HTML 标签和英文字符
    i['text'] = i['text'].apply(lambda x: remove_english(re.sub(r'<.*?>', '', str(x))))

    # 假设 df 是包含 'text' 列的 DataFrame
    text_data = i['text'].str.cat(sep=' ')


    # 在'text'列中去掉指定的字符串
    strings_to_remove = ['chexie','netattachboards','http','www','de', 'je', '0', 'que', '好', '不', '贴子', 'le', 're', 'dans', 'DIV', 'jpg', 'java', '编辑过',
                         '此帖子由', 'nbsp', 'bbs', 'img', 'quote', 'gif', 'gt', 'lt', 'div', 'br']
    for string in strings_to_remove:
        text_data = text_data.replace(string, '')

    # 在'text'列中去掉词表中的词语
    for word in wordlist:
        text_data = text_data.replace(word, '')

    # 指定中文字体（这里使用了一个中文字体文件，你需要替换成你本地的中文字体文件路径）
    font_path = 'C:\Windows\Fonts\simhei.ttf'
    my_font = FontProperties(fname=font_path, size=12)

    # 生成词云图
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text_data)

    # 显示词云图
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # 保存词云图为图像文件
    wordcloud.to_file(r'D:/researches/Projects/CAPUemo/wdtest/wordcloud2.png')

    # 显示图形
    plt.show()

