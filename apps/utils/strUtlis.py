# _*_ coding: utf-8 _*_
import random
import time

__author__ = 'jevoly'
__date__ = '2018/12/22 0022 下午 3:48'


def generic_code():
    """
    生成4位验证码
    :return:
    """
    random_str = []
    for i in range(4):
        random_str.append(str(int(random.random() * 10)))
    return "".join(random_str)


def generic_order_sn(user_id=""):
    """
    生成订单号
    :param user_id:
    :return:
    """
    order_sn = "{time_str}{user_id}{rand_str}".format(
        time_str=time.strftime('%Y%m%d%H%M%S'),
        user_id=user_id,
        rand_str=random.Random().randint(10, 99)
    )
    return order_sn


if __name__ == "__main__":
    # print(generic_code())
    print(generic_order_sn())
