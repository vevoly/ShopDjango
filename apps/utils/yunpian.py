
import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2"

    def send_sms(self, code, mobile):
        params = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "您的验证码是{code}"
        }
        response = requests.post(self.single_send_url, data=params)
        import json
        re_dict = json.loads(response.text)
        print(re_dict)
