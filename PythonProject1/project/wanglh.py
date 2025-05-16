import time

from utils._http import RequestClient
from utils.seleniumUtils import *
# import pytest

client = RequestClient(base_headers={"Content-Type": "application/x-www-form-urlencoded"})


def login(mobile:str="16756803148",pwd:str="lsw56449"):
    url = "http://system.wanlh.com/index.php/api/user.userweb/login"
    data = {
        'mobile': mobile,
        'password': pwd,
        'token': '',
        'app_id': '10001',
    }
    res = client.post(url=url, data=data)
    res_data = res.get("response").json().get("data")
    try:
        user_id = res_data.get("user_id")
        token = res_data.get("token")
        log(f"userId是{user_id},token是{token}")
    except Exception as e:
        log(res)

    return user_id, token

def sign(token:str="57680ab7714d6d748af1dabd6709a140"):
    url = f"http://system.wanlh.com/index.php/api/plus.sign.sign/add?token={token}&app_id=10001"
    res = client.get(url=url)
    # res_data = res.get("response").json()
    # msg = res_data.get("data")
    log(res)

def batch():
    regisiterTXT = parseTxtFile("../record/wanglh.txt")
    arr = regisiterTXT.get("lines")
    for i in arr:
        phone = i[0]
        pwd = i[1]
        uid,token = login(phone, pwd)
        log(token)
        sign(token)
        time.sleep(0.5)
if __name__ == '__main__':
    batch()
    # sign()
