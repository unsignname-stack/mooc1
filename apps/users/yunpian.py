import json
import requests


class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "【爱慕课】爱慕课注册。您的验证码是{code}。如非本人操作，请忽略本短信。".format(code=code)
        }
        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict


if __name__ == "__main__":
    from mooc1.settings import APIKEY
    yun_pian = YunPian(APIKEY)
    # 750491da91aaa41e4cdecf722629117b
    #注意把这里的手机号改为自己的手机号
    yun_pian.send_sms("2021", "18948796072")