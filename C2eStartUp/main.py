from file_reader import *
from quality_checker import *
from data_analyzer import *
from report_generator import *
from chart_generator import *
from data_cleaning import *


def process(file_path):
    # 读取 Excel 文件
    data = read_excel(file_path)

    # 数据质量监测
    quality_report = check_quality(data)

    #数据清洗（此处涉及值传递，后续可能改为class类传递 方便管理中间值状态）
    clean_data = data_cleaning_general(data)

    # 数据分析
    analysis_results = analyze_data_general(clean_data)

    # 生成报告
    report = generate_report_general(quality_report, analysis_results)

    # 生成图表
    chart_base64 = generate_chart_general(clean_data)

    return {"report": report, "chart_base64": chart_base64}


def main():
    file_path = 'test.xlsx'

    # 处理数据
    result = process(file_path)


    print(result['report'])
    print(f"Chart Base64: {result['chart_base64']}")


if __name__ == "__main__":
    main()