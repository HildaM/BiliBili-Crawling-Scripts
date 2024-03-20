"""
存储各种处理 excel 工具类
"""

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment


# 存储评论为excel文件
def save_comments_to_excel(json_data, excel_file_name):
    # 解析JSON数据
    comments_data = []
    for comment in json_data:
        comment_info = {
            "评论人": comment['member']['uname'],
            "评论内容": comment['content']['message'],
            "评论字数": len(comment['content']['message']),
            "点赞数": comment['like'],
            "回复数": comment['rcount'],
            "评论时间": pd.to_datetime(comment['ctime'], unit='s')
        }
        comments_data.append(comment_info)
    
    # 创建DataFrame
    df = pd.DataFrame(comments_data)
    
    # 保存为Excel文件
    df.to_excel(excel_file_name, index=False)




"""
    自动调整excel，提高可读性
    每个单元格超过60个字符就会自动换行
"""
def auto_adjust_excel_column_width(excel_file_name):
    # 加载工作簿
    workbook = load_workbook(excel_file_name)
    worksheet = workbook.active

    # 调整列宽并设置自动换行
    for col in worksheet.columns:
        max_length = 0
        column = col[0].column_letter  # 获取列字母

        for cell in col:
            # 设置自动换行
            cell.alignment = Alignment(wrap_text=True)
            try:
                # 需要尝试转换为字符串
                cell_length = len(str(cell.value))
                # 如果单元格内容超过60字符，考虑换行对列宽的影响
                if cell_length > 60:
                    cell_length = 60  # 假设每行最多60字符
                if cell_length > max_length:
                    max_length = cell_length
            except:
                pass
        
        adjusted_width = (max_length + 2) * 1.2  # 调整列宽
        worksheet.column_dimensions[column].width = adjusted_width

    # 保存工作簿
    workbook.save(excel_file_name)