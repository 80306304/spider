import base64
import hashlib
import json
from datetime import datetime

import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


class driverUtils:
    def __init__(self):
        with open("./config/baseConfig.json", 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            self.chrome_driver_path = json_data.get("chrome_driver_path")
            self.Privacy = json_data.get("isPrivacy")
            self.timeOut = json_data.get("timeOut")
            self.mobile = json_data.get("mobile")

    # 初始化chrome
    def begin(self):
        service = Service(self.chrome_driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1080,720")  # 设置窗口大小
        options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 禁用自动化提示
        options.add_experimental_option("detach", True)  # 防止脚本结束时不关闭浏览器
        if self.mobile:
            mobile_emulation = {
                "deviceName": "iPhone X"  # 可以是任何预定义的设备名称，如 'iPhone X'
            }
            options.add_experimental_option("mobileEmulation", mobile_emulation)
        if self.Privacy:
            options.add_argument("--incognito")  # 无痕模式
            driver = webdriver.Chrome(service=service, options=options)
        else:
            driver = webdriver.Chrome(service=service, options=options)
        driver.implicitly_wait(self.timeOut)
        return driver


def log(text):
    print(f"[{getNowTime()}]{text}")

def getNowTime():
    return datetime.now().strftime("%m/%d %H:%M:%S")
# 写入文件
def addContent(file_path, new_content):
    try:
        # 以读取模式打开文件
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取文件所有内容
            lines = file.readlines()

        # 在已有内容后添加新行
        lines.append(new_content+'\n')

        # 以写入模式打开文件
        with open(file_path, 'w', encoding='utf-8') as file:
            # 将更新后的内容写回文件
            file.writelines(lines)

        log("内容添加成功。")
    except FileNotFoundError:
        log("错误：文件未找到。")
    except Exception as e:
        log(f"发生未知错误：{e}")

# 提起文件中的数据(养号)
def parseTxtFile(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取每一行并去掉换行符
            lines = [line.rstrip('\n') for line in file.readlines()]
            result = [item.split("----") for item in lines]
            line_count = len(result)
            return {"lines":result, "count":line_count}
    except FileNotFoundError:
        log(f"错误：未找到文件 {file_path}。")
        return [], 0
    except Exception as e:
        log(f"发生未知错误：{e}")
        return [], 0

def parseTonText(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # 读取每一行并去掉换行符
            lines = [line.rstrip('\n') for line in file.readlines()]
            line_count = len(lines)
            return {"lines":lines, "count":line_count}
    except FileNotFoundError:
        log(f"错误：未找到文件 {file_path}。")
        return [], 0
    except Exception as e:
        log(f"发生未知错误：{e}")
        return [], 0

def delete_line(file_path, line_number):
    try:
        # 以只读模式打开文件并读取所有行
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # 过滤掉指定行（行号从 1 开始）
        new_lines = [line for i, line in enumerate(lines, start=1) if i != line_number]

        # 以写入模式打开文件并将过滤后的内容写回
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

        log(f"成功删除第 {line_number} 行。")
    except FileNotFoundError:
        log(f"错误：未找到文件 {file_path}。")
    except Exception as e:
        log(f"发生未知错误：{e}")


def aes_encrypt(data: str, key: str, iv: str) -> str:
    # 1. 将密钥和 IV 转换为字节（必须为 bytes 类型）
    key_bytes = key.encode('utf-8')
    iv_bytes = iv.encode('utf-8')

    # 2. 校验密钥和 IV 长度（AES 要求）
    if len(key_bytes) not in [16, 24, 32]:
        raise ValueError("密钥长度需为 16/24/32 字节（对应 AES-128/192/256）")
    if len(iv_bytes) != 16:
        raise ValueError("IV 长度必须为 16 字节（CBC 模式要求）")

    # 3. 准备待加密数据（转换为字节并填充）
    data_bytes = data.encode('utf-8')
    padded_data = pad(data_bytes, AES.block_size)  # 按 AES 块大小（16字节）填充

    # 4. 创建 AES 加密器（CBC 模式）
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)

    # 5. 加密并转换为 base64 编码
    encrypted_data = cipher.encrypt(padded_data)
    base64_encrypted = base64.b64encode(encrypted_data).decode('utf-8')  # 字节转字符串

    return base64_encrypted

def aes_decrypt(encrypted_base64: str, key: str, iv: str) -> str:
    """
    AES-CBC 解密 base64 编码的密文，返回原始明文
    :param encrypted_base64: base64 编码的加密数据
    :param key: 密钥（需与加密时一致）
    :param iv: 初始化向量（需与加密时一致）
    :return: 解密后的原始字符串
    """
    # 转换密钥和 IV 为字节
    key_bytes = key.encode('utf-8')
    iv_bytes = iv.encode('utf-8')

    # 校验长度（与加密时一致）
    if len(key_bytes) not in [16, 24, 32]:
        raise ValueError("密钥长度需为 16/24/32 字节（对应 AES-128/192/256）")
    if len(iv_bytes) != 16:
        raise ValueError("IV 长度必须为 16 字节（CBC 模式要求）")

    # 将 base64 密文解码为字节
    encrypted_data = base64.b64decode(encrypted_base64)

    # 创建解密器并解密
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    decrypted_padded = cipher.decrypt(encrypted_data)

    # 去除填充并转换为字符串
    decrypted_data = unpad(decrypted_padded, AES.block_size)  # 移除 PKCS#7 填充
    return decrypted_data.decode('utf-8')  # 字节转原始字符串

def md5_encrypt(data: str, encoding: str = 'utf-8') -> str:
    """
    计算字符串的 MD5 哈希值（十六进制格式）
    :param data: 待加密的原始字符串
    :param encoding: 字符串编码方式（默认 utf-8）
    :return: MD5 十六进制哈希字符串（小写）
    """
    # 将字符串转换为字节（MD5 要求输入为 bytes）
    data_bytes = data.encode(encoding)

    # 创建 MD5 哈希对象并计算哈希值
    md5_obj = hashlib.md5()
    md5_obj.update(data_bytes)

    # 返回十六进制字符串（小写）
    return md5_obj.hexdigest()

def getIp(self):
    if(self.ipUrl == None):ip = "localhost"
    else : ip = requests.get(self.ipUrl).text
    return ip

def varifyIp(self):
    ip = self.getIp()
    proxys={
        "http":f"http://{ip}",
        "https": f"https://{ip}"
    }
    code = requests.get("http://www.baidu.com",proxies=proxys,timeout=5).status_code
    try:
        if code == 200:
            print(f"ip地址：{ip}有效")
            return ip
        else:
            print(f"ip地址：{ip}无效")
            return False
    except Exception as e:
        print(f"有报错：{e}")
        return False


if __name__ == '__main__':
    #es = "sEWywWmGaMBl3RGOBsaqC/6q+cMdYfPiZeTpWGoPCOQ+fS6LgPJyp9ysjTDBgGHZ9A75Aq1+XO5kp+RuH5zKeeNJgAH1caeqRkUNA6iFrbaoaQHMoOYNRbc6pEdWvEYXFlT00eNCqd1WvqDUyx6QMhH4Glqc8EtDTccUNaPqeusoaQBn0QHQOnRFPNPJ04UYG0odKqLX00atnzcs0Xrp97yYPpHTe7l6WbnHEepinRQ="
    #es = "6V+oGo0n2cjed/zS1PEVz7gU4ZsYGPOhoWrF0He/4n5NB8jLPEHUL2FyqtTLCxPPi1PFj5rUYf+0aCd5b1H+52OmC4zAEuinSxr52xXUMQNGrwYI5upPt/hQRB6w4QX+D0gEIcs8fVIhZfp+D8XK60Mc5YsmDUtW9yToOXFXjyTlu22CUbLCX7KvuJ2KUfG6PIG69DjmeMAMkTJe+kDpIhwiuxwyn8SYSRmomdCAi9aJJmKsQ/gznwUdxmFVC+G8"
    #aes_u = '{"type":0,"privateKey":"","password":"","mnemonic":"fresh gasp region science goddess ski physical tip adapt prevent aunt open","channel":1,"fnejnreoi":"1234567891234567"}'
    #print(aes_decrypt(es,"123V5c78912j4F6r","1234567891234567"))
    #print(aes_encrypt(str(aes_u),"123V5c78912j4F6r","1234567891234567"))


    # data = '{data:sEWywWmGaMBl3RGOBsaqC/6q+cMdYfPiZeTpWGoPCOQ+fS6LgPJyp9ysjTDBgGHZAC8IiumTPyhkQzPafv1WQdKFZ8oosKb52tn836pyqwFwRF/VQ6CRt/r4rbSiLhHdx1PIHwAZctwbsuLqgZmsH+c862pngJpde9W+fFmI+peeRRQSipyz973jzgRujCb8T1hOGA63YS7cCKZVLV8Lh0OM+1/QYnbKup8Y20k7Hks=}'
    #
    # response = requests.post('https://siw.spiderweb.work/api/user/login', headers=headers, data=data)
    # print(response.text)
    req_aes_key = "123V5c78912j4F6r"
    req_aes_IV = "1234567891234567"
    res_aes_key = "0123456789abcdef"
    res_aes_IV = "1234567890abcdef"
    data = "Y5Kqz96dIfaGDAL1Kjw+IbWZOdXyGpEu9ftHqc9923KUAmUxA59AhRuq8irG8assRU2RxbaRoo0aAHYW5icwxk3VVGO6wULVjcSRbnqsNkCBlQayvIcfiGwAWPQll+TP"
    print(aes_decrypt(data, req_aes_key, req_aes_IV))