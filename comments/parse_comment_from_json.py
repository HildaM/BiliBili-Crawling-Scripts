import json
from get_comments_in_video import save_comments_to_excel



if __name__ == "__main__":
    json_file = input("输入json文件地址：")
    # 读取JSON文件并解析为变量
    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    comments = []
    comments.extend(json_data['data']['replies'])
    save_comments_to_excel(comments, "json_comments_analysis.xlsx")
    