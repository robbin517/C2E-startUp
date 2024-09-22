def analyze_data_general(data):

    if data is None:
        print("数据集为空")
        return None

    analysis_results = {}
    numeric_columns = data.select_dtypes(include='number').columns
    for col in numeric_columns:
        analysis_results[col] = {
            'median': data[col].median(),
            'max': data[col].max(),
            'min': data[col].min(),
            'std_dev': data[col].std()
        }
    return analysis_results


def analyze_data_customized(data):
    pass
