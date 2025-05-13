from utils._http import RequestClient
from utils.seleniumUtils import *
import pytest

client = RequestClient(base_headers={"Content-Type": "application/x-www-form-urlencoded"})


def test_login(mobile:str,pwd:str):
    url = "http://system.wanlh.com/index.php/api/user.userweb/login"
    data = {
        'mobile': mobile,
        'password': pwd,
        'token': '',
        'app_id': '10001',
    }
    res = client.post(url=url, data=data)
    res_data = res.get("response").json().get("data")
    user_id = res_data.get("user_id")
    token = res_data.get("token")
    log(f"userId是{user_id},token是{token}")
    return user_id, token

def test_sign(token:str="0fb13686ab5f10423e7c7021d95d62bc"):
    url = f"http://system.wanlh.com/index.php/api/plus.sign.sign/add?token={token}&app_id=10001"
    res = client.get(url=url)
    res_data = res.get("response").json().get("data").get("msg")
    log(res_data)