import  hashlib
from djangoProject1 import settings
from datetime import datetime
import random
import math

#定义一个加密方法
def md5(data_string):
    """MD5加密，并返回加密值
    data_string：需要加密的文本信息
    """
    obj=hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode("utf-8"))
    return obj.hexdigest()


def makeid(pr="DD",rad="%y%m%d",lg=6):
    """生成一个ID的方法
    pr：前缀，可以输入一个前缀，默认DD
    rad：时间格式，默认年月日
    lg：随机数位数，默认6位
    """
    id=str(pr)+datetime.now().strftime(rad)+str(random.randint(math.pow(10,lg),math.pow(10,lg+1)))
    return id


if __name__ == '__main__':
    print(md5("123"))
    print(makeid(pr="LD",lg=1))