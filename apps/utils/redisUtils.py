# _*_ coding: utf-8 _*_
__author__ = 'jevoly'
__date__ = '2018/12/20 0020 上午 10:53'


from django.core.cache import cache


class MobileRedis(object):

    def set_mobile_code(self, mobile, code):
        """
        存储手机验证码
        :param mobile:
        :param code:
        :return:
        """
        cache.set(mobile, code, 600)
        print('{0}:{1}'.format(mobile, code))
        pass

    def get_mobile_code(self, mobile):
        """
        从缓存中取出手机验证码
        :param mobile:
        :return:
        """
        if not cache.has_key(mobile):
            return False
        return cache.get(mobile)





