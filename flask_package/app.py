from flask import Flask,request, jsonify, send_file
from flask_package.routes import process_blueprint
import os

from flask_package.routes.process_blueprint import main_bp

app = Flask(__name__)
# 配置文件
app.config.from_object('flask.config.Config')

# 注册蓝图
app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=True)