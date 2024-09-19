import matplotlib.pyplot as plt
import io
import base64

def generate_chart_general(data):
    plt.figure(figsize=(10, 6))
    numeric_columns = data.select_dtypes(include='number').columns
    data[numeric_columns].hist(bins=20, color='blue', edgecolor='black', linewidth=1.0)
    img_stream = io.BytesIO()
    plt.savefig(img_stream, format='png')
    img_stream.seek(0)
    img_base64 = base64.b64encode(img_stream.getvalue()).decode('utf-8')
    return img_base64

#后续加入seaborn以及定制化场景
def generate_chart_customized(data):
    pass