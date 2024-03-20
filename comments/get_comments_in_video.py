from bilibili_api import comment, sync, video

# 动态添加项目根目录到sys.path
import os, sys
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.append(root_dir)

from config.auth import Auth
from  utils.excel import save_comments_to_excel, auto_adjust_excel_column_width



"""
    获取指定视频下的所有评论，并以excel的形式存储
    获取内容：
        评论人，评论内容，点赞数，回复数，IP属地，评论时间
"""
async def get_comment_from_video(bvid: str, order_type, max_comments: int):
    # 用户凭证
    credential = Auth().credential()

    # 存储评论
    comments = []
    # 页码
    page = 1
    # 当前已获取数量
    count = 0
    while True:
        # 获取aid
        aid = video.Video(bvid=bvid).get_aid()

        # 获取评论
        c = await comment.get_comments(aid, comment.CommentResourceType.VIDEO, page, order_type, credential)

        # 存储评论
        comments.extend(c['replies'])
        # 增加已获取数量
        count += c['page']['size']
        # 增加页码
        page += 1

        if max_comments > 0 and count >= max_comments:
            break
        if count >= c['page']['count']:
            # 当前已获取数量已达到评论总数，跳出循环
            break
    

    # 保存为excel结构信息
    if order_type == comment.OrderType.TIME:
        order = "Time"
    else:
        order = "Like"
    file_name = bvid + "_Analysis_OrderBy_" + order + ".xlsx"
    save_comments_to_excel(comments, file_name)
    auto_adjust_excel_column_width(file_name)

    # 打印评论总数
    print(f"\n\n共有 {count} 条评论（不含子评论）")




if __name__ == "__main__":
    bvid = input("请输入待处理视频的BV号：")
    try:
        match input("请输入一个数字，确定评论的排序规则(1:按点赞数，2:按时间顺序)："):
            case '1':
                order_type = comment.OrderType.LIKE
            case '2':
                order_type = comment.OrderType.TIME
            case _:
                raise SystemExit("错误：输入了无效的选项。程序现在将退出。")
    except SystemExit as e:
        print(e)
        sys.exit(1)

    max_comments = input("请输入你想获取的最大评论数(如果置空则默认全部获取，有可能会触发风控导致获取失败)：")
    # 转换max_comments为整数，如果输入为空则设置为一个非常大的数.
    # 输入为空字符串，则将max_comments设置为float('inf')，这表示无穷大，逻辑上等同于获取所有评论。
    max_comments = int(max_comments) if max_comments.isdigit() else float('inf')
    
    sync(get_comment_from_video(bvid, order_type, max_comments))