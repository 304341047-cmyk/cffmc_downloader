import pandas as pd

def parse_settlement(file_path):
    """解析结算单Excel文件"""
    sheets = pd.read_excel(file_path, sheet_name=None)
    print("检测到工作表：", list(sheets.keys()))
    return sheets