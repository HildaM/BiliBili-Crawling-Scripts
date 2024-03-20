# 该脚本用于B站身份认证
from dotenv import load_dotenv
from bilibili_api import Credential
import os

class Auth:

    def __init__(self):
        # 加载.env文件
        load_dotenv()

        self.sessdata = os.getenv("sessdata")
        self.bili_jct = os.getenv("bili_jct")
        self.buvid3 = os.getenv("buvid3")
        # 下面2个可选
        self.dedeuserid = os.getenv("dedeuserid")
        self.ac_time_value = os.getenv("ac_time_value")

    def credential(self):
        return Credential(
            sessdata=self.sessdata,
            bili_jct=self.bili_jct,
            buvid3=self.buvid3,
            dedeuserid=self.dedeuserid,
            ac_time_value=self.ac_time_value
        )
