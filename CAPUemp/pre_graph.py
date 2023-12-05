import pandas as pd
import json
from pyecharts import options as opts
from pyecharts.charts import Graph
from CAPUemp.dataclean import nan_result_df

def preprocess_forum_data(df):
    nodes = []
    links = []
    categories = []
    nodes_dict = {}

    for index, row in df.iterrows():
        category_name = row['author']

        if category_name not in categories:
            categories.append(category_name)

        if row['pid'] == 1:
            if row['author'] not in nodes_dict:
                nodes_dict[row['author']] = {
                    'symbolSize': 2,
                    'value': 0,
                    'draggable': 'False',
                    'category': category_name,
                    'label': {
                        'normal': {
                            'show': 'True'
                        }
                    }
                }

            nodes_dict[row['author']]['symbolSize'] += 1
            nodes_dict[row['author']]['value'] += 1

        else:
            if row['author'] not in nodes_dict:
                nodes_dict[row['author']] = {
                    'symbolSize': 2,
                    'value': 0,
                    'draggable': 'False',
                    'category': category_name,
                    'label': {
                        'normal': {
                            'show': 'True'
                        }
                    }
                }

            nodes_dict[row['author']]['symbolSize'] += 0.2  # Assuming 0.2 for comments
            nodes_dict[row['author']]['value'] += 1

            source = get_author_by_tid(df, row['tid'])
            target = row['author']
            links.append({
                'source': source,
                'target': target,
                'value': len(str(row['text']))
            })

    nodes = list(nodes_dict.values())
    save_data_to_json(nodes, links, categories)


def get_author_by_tid(df, tid):
    return df[df['tid'] == tid]['author'].iloc[0]


def save_data_to_json(nodes, links, categories):
    data = [nodes, links, categories]
    with open('forum_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def graph_forum() -> Graph:
    with open("forum_data.json", "r", encoding='utf-8') as f:
        j = json.load(f)
        nodes, links, categories = j
        nodes = nodes[:2000]

    # 将节点的名称设置为对应的类别
    for node in nodes:
        node["name"] = node["category"]

    # Ensure categories are in the correct format
    categories = [{"name": category} for category in categories]

    c = (
        Graph()
        .add(
            series_name="",
            nodes=nodes,
            links=links,  # 确保这里有 links
            categories=categories,
            repulsion=50,
            linestyle_opts=opts.LineStyleOpts(curve=0.2, color="black"),  # 设置线的颜色为黑色
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="Forum Graph")
        )
    )

    return c

if __name__ == '__main__':
    # Assuming nan_result_df is your DataFrame already loaded in memory
    nan_result_df = nan_result_df  # Replace with your DataFrame

    # Preprocess data and generate forum graph
    preprocess_forum_data(nan_result_df)
    graph_forum().render(r'D:\researches\Projects\CAPUemo\weibo-analysis-and-visualization\CAPUemp\soc_graph\forum_graph.html')
