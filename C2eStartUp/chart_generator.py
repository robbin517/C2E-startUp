import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime
import os
import seaborn as sns
import pandas as pd
from sklearn.cluster import KMeans


def generate_chart_general(data,analysis_results):
    try:
        # 生成直方图
        histogram_img_base64 = generate_graph_histogram(data)

        # 生成散点图
        scatter_img_base64 = generate_scatter_plot(data,analysis_results)

        # 生成折线图
        line_img_base64 = generate_line_chart(data, analysis_results)

        # 生成饼图
        pie_img_base64 = generate_pie_chart(data, analysis_results)

        return {
            "histogram_img_base64": histogram_img_base64,
            "scatter_img_base64": scatter_img_base64,
            "line_img_base64": line_img_base64,
            "pie_img_base64": pie_img_base64
        }
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}


def generate_graph_histogram(data):
    # 图片存储地址
    output_path = 'graph_place/graph_histogram'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 生成直方图
    plt.figure(figsize=(10, 6))
    numeric_columns = data.select_dtypes(include='number').columns
    data[numeric_columns].hist(bins=20, color='blue', edgecolor='black', linewidth=1.0)
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'chart_histogram_{timestamp}.png'

    # 保存图表到文件
    file_path = output_path + "/" + filename
    plt.savefig(file_path)
    plt.close()
    return img_base64


def generate_scatter_plot(data, analysis_results):
    # 图片存储地址
    output_path = 'graph_place/graph_scatter'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 获取数值列
    numeric_columns = data.select_dtypes(include='number').columns

    x = analysis_results['xy_fields']['x']
    y = analysis_results['xy_fields']['y']

    if x and y:
        x_column = x
        y_column = y
    else:
        # 默认选择前两个数值列作为X轴和Y轴
        x_column = numeric_columns[1]
        y_column = numeric_columns[0]

    # 生成散点图
    plt.figure(figsize=(10, 6))
    plt.scatter(data[x_column], data[y_column], color='blue', edgecolor='black', alpha=0.7)
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Scatter Plot of {x_column} vs {y_column}')

    # 将图像保存为Base64编码的字符串
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'scatter_{timestamp}.png'

    # 保存图表到文件
    file_path = os.path.join(output_path, filename)
    plt.savefig(file_path)
    plt.close()

    return img_base64


def generate_line_chart(data, analysis_results):
    # 图片存储地址
    output_path = 'graph_place/graph_line'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 获取数值列
    numeric_columns = data.select_dtypes(include='number').columns

    x = analysis_results['xy_fields']['x']
    y = analysis_results['xy_fields']['y']

    if x and y:
        x_column = x
        y_column = y
    else:
        # 默认选择前两个数值列作为X轴和Y轴
        x_column = numeric_columns[1]
        y_column = numeric_columns[0]

    # 动态分组并计算中位数
    # 开始动态分组并计算中位数
    min_val = data[x_column].min()
    max_val = data[x_column].max()
    bin_width = (max_val - min_val) / 7
    bins = [min_val + i * bin_width for i in range(8)]

    # 定义标签
    labels = [f'{bins[i]:.2f}-{bins[i + 1]:.2f}' for i in range(7)]

    # 分组
    data['bin_group'] = pd.cut(data[x_column], bins=bins, labels=labels, include_lowest=True)

    # 计算每个区间的中位数
    group_medians = data.groupby('bin_group')[y_column].median().reset_index()

    # 添加区间的中点
    group_medians['bin_midpoint'] = group_medians['bin_group'].apply(
        lambda x: (float(x.split('-')[0]) + float(x.split('-')[1])) / 2)

    # 按X轴中点排序
    group_medians = group_medians.sort_values(by='bin_midpoint')
    # 结束动态分组并计算中位数

    # 生成折线图
    plt.figure(figsize=(10, 6))
    plt.plot(group_medians['bin_midpoint'], group_medians[y_column], marker='o', linestyle='-', color='blue')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Line Chart of {x_column} vs {y_column}')

    # 将图像保存为Base64编码的字符串
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'line_{timestamp}.png'

    # 保存图表到文件
    file_path = os.path.join(output_path, filename)
    plt.savefig(file_path)
    plt.close()

    return img_base64

def generate_line_Kbean_chart(data, analysis_results):
    # 图片存储地址
    output_path = 'graph_place/graph_line'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 获取数值列
    numeric_columns = data.select_dtypes(include='number').columns

    x = analysis_results['xy_fields']['x']
    y = analysis_results['xy_fields']['y']

    if x and y:
        x_column = x
        y_column = y
    else:
        # 默认选择前两个数值列作为X轴和Y轴
        x_column = numeric_columns[1]
        y_column = numeric_columns[0]

    # 使用K-means聚类
    kmeans = KMeans(n_clusters=5, random_state=0).fit(data[[x_column]])
    data['cluster'] = kmeans.labels_

    # 计算每个聚类的中位数
    cluster_medians = data.groupby('cluster')[[x_column, y_column]].median().reset_index()

    # 按X轴排序
    cluster_medians = cluster_medians.sort_values(by=x_column)

    # 生成折线图
    plt.figure(figsize=(10, 6))
    plt.plot(cluster_medians[x_column], cluster_medians[y_column], marker='o', linestyle='-', color='blue')
    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f'Line Chart of {x_column} vs {y_column}')

    # 将图像保存为Base64编码的字符串
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'line_{timestamp}.png'

    # 保存图表到文件
    file_path = os.path.join(output_path, filename)
    plt.savefig(file_path)
    plt.close()

    return img_base64
def generate_pie_chart(data, analysis_results):
    # 图片存储地址
    output_path = 'graph_place/graph_pie'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 获取数值列
    numeric_columns = data.select_dtypes(include='number').columns

    # 选择一个数值列作为饼图的数据
    column = numeric_columns[0]

    # 生成饼图
    plt.figure(figsize=(10, 6))
    sizes = data[column].value_counts()
    labels = sizes.index
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title(f'Pie Chart of {column}')

    # 将图像保存为Base64编码的字符串
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')

    # 生成带有时间戳的文件名
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'pie_{timestamp}.png'

    # 保存图表到文件
    file_path = os.path.join(output_path, filename)
    plt.savefig(file_path)
    plt.close()

    return img_base64