from flask import Blueprint, request, jsonify, render_template
from flask import current_app
import data_analyzer
from file_reader import *
from QwenModel_Client import QwenClient
from util.extract_file_KB import *
from quality_checker import *
from data_cleaning import *
from chart_generator import *
from report_generator import *


main_bp = Blueprint('main_bp', __name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/upload_and_process', methods=['POST'])
def upload_and_process():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"}), 400
    if file and allowed_file(file.filename):
        # 读取文件到内存中
        file_stream = io.BytesIO()
        file.save(file_stream)
        file_stream.seek(0)

        # 读取 Excel 文件
        data, data_id = read_excel(file_stream)
        has_content, file_id_dir = create_and_check_directory(data_id)

        # 数据质量监测
        quality_report = check_quality(data)

        # 数据清洗（此处涉及值传递，后续可能改为class类传递 方便管理中间值状态）
        clean_data = data_cleaning_general(data)

        # 初始化通义千问客户端
        qwen_client = QwenClient()

        # 数据分析
        analysis_results = data_analyzer.analyze_data(clean_data, qwen_client)

        # 生成报告
        report = generate_report_general(quality_report, analysis_results)
        report_structured = generate_report_Json_structured(quality_report, analysis_results)
        # 生成图表
        selected_keys = ["histogram_img_base64", "scatter_img_base64"]
        chart_set = generate_chart_general(clean_data, analysis_results, file_id_dir)
        chart_base64 = {key: chart_set[key] for key in selected_keys if key in chart_set}
        # Img_path
        selected_keys = ["histogram_img_path", "scatter_img_path"]
        Img_path = {key: chart_set[key] for key in selected_keys if key in chart_set}

        return {"report": report, "chart_base64": chart_base64}, Img_path, report_structured
    else:
        return jsonify({"status": "error", "message": "啊哦，小飞棍来喽"}), 400

# 导出蓝图
__all__ = ['main_bp']