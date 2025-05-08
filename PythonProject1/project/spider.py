import json
import time

import pyperclip
import pytest
import requests
from selenium.webdriver.common.by import By
from utils.seleniumUtils import driverUtils, log, addContent, parseTxtFile, getNowTime, parseTonText, delete_line,aes_decrypt,aes_encrypt,md5_encrypt
from utils._http import RequestClient

# 初始化项目
req_aes_key = "123V5c78912j4F6r"
req_aes_IV = "1234567891234567"
res_aes_key = "0123456789abcdef"
res_aes_IV = "1234567890abcdef"
client = RequestClient()

with open("../config/baseConfig.json", 'r', encoding='utf-8') as f:
        json_data = json.load(f)
        regisiterPath = json_data.get("regisiterPath")
        TonPath = json_data.get("TonPath")
        spiderPath = json_data.get("spiderPath")
        inviteUrl = json_data.get("inviteUrl")
        failPath = json_data.get("failPath")
        successPath = json_data.get("successPath")
        receiveId = json_data.get("receiveId")

def setHeader(signData,token:str=""):
    timestamp = str(int(time.time() * 1000))
    sign = "data="+str(signData)+"&domain=https://siw.spiderweb.work&key=MINGYANGB7D0C9D279892857DE5490AB856772FE&pathinfo=/api/user/login&timestamp="+timestamp
    if token != "":
        return {
            "sign":str(md5_encrypt(sign)),
            "timestamp":timestamp,
            "token":token
        }
    else:
        return {
            "sign":str(md5_encrypt(sign)),
            "timestamp":timestamp
        }
def getBuyHeader(token:str=""):
    timestamp = str(int(time.time() * 1000))
    sign = "box_id=24&domain=https://siw.spiderweb.work&key=MINGYANGB7D0C9D279892857DE5490AB856772FE&num=1&pathinfo=/api/index/createOrder&pay_type=1&price_amount=480.00&timestamp="+timestamp
    return {
        "sign":str(md5_encrypt(sign)),
        "timestamp":timestamp,
        "token":token
    }
def setData(data):
    return {
        "data":str(aes_encrypt(data,req_aes_key,req_aes_IV))
    }

def getData(data):
    return {
        "data":str(aes_decrypt(str(data),res_aes_key,res_aes_IV))
    }
# 转账
def test_sendSiw(receiveId:str="4518054bdcd6e68ce5d4cf35d2a52dd76e147841",giveNum:str="1.08",token:str="7018d2fa-3aad-43a0-93d9-924928f0f68d"):
    if giveNum == "0.00":
        log("无余额可转")
        return
    url = "https://siw.spiderweb.work/api/user/siwGive"
    data = '{"receiveId":"'+receiveId+'","giveNum":"'+giveNum+'","fnejnreoi":"1234567891234567"}'
    aes_data = setData(data)
    res = client.post(url=url,json=aes_data,headers=setHeader(data,token))
    log(res.get("content"))

def test_regisiter(TonAddr):
    driver = driverUtils().begin()
    driver.get(inviteUrl)
    # 点击创建按钮
    create_button = driver.find_element(By.XPATH, '//*[@id="home"]/uni-view/uni-view[4]/uni-view[2]')
    create_button.click()
    # 姓名
    nickName_input = driver.find_element(By.XPATH,
                                         '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[1]/uni-view[2]/uni-view[1]/uni-view[2]/uni-input/div/input')
    nikeName = nickName_input.get_attribute('value')
    # 输入密码
    pwd1_input = driver.find_element(By.XPATH,
                                     '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[1]/uni-view[2]/uni-view[2]/uni-view[2]/uni-input/div/input')
    pwd2_input = driver.find_element(By.XPATH,
                                     '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[1]/uni-view[2]/uni-view[3]/uni-view[2]/uni-input/div/input')
    pwd1_input.send_keys("121216")
    pwd2_input.send_keys("121216")
    log(f"昵称：{nikeName} 密码：121216")
    time.sleep(0.5)
    # 确认按钮
    enter_button = driver.find_element(By.XPATH,
                                       '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view')
    enter_button.click()
    # 获取助记词
    copy_button = driver.find_element(By.XPATH,
                                      '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[1]/uni-view[2]/uni-view[1]/uni-view[2]/uni-image')
    copy_button.click()
    clipboard_content = pyperclip.paste()
    split_content = clipboard_content.split()
    log(f"助记词：{clipboard_content}")
    driver.find_element(By.XPATH,
                        '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view').click()
    # 输入助剂次
    for i in split_content:
        driver.find_element(By.XPATH, f"//*[text()='{i}']").click()
        time.sleep(0.2)
    driver.find_element(By.XPATH,
                        "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view").click()
    # 复制链接地址
    driver.find_element(By.XPATH,
                        "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[1]/uni-view[2]/uni-view[1]/uni-view[2]/uni-view[2]/uni-image").click()
    pocket = pyperclip.paste()
    log(f"钱包地址：{pocket}")
    # 点击绑定按钮
    driver.find_element(By.XPATH, '//*[@id="Book"]').click()
    driver.find_element(By.XPATH,
                        '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view/uni-text/span').click()
    addr_input = driver.find_element(By.XPATH,
                                     '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view[2]/uni-view/uni-view/uni-view/uni-view[1]/uni-view/uni-input/div/input')
    addr_input.send_keys(TonAddr)
    time.sleep(0.5)
    driver.find_element(By.XPATH,
                        '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view[2]/uni-view/uni-view/uni-view/uni-view[2]').click()
    # 记录数据
    out_txt = f"{nikeName}----121216----{clipboard_content}----{pocket}----{getNowTime()}"
    addContent(regisiterPath, out_txt)
    addContent(spiderPath, pocket)
    # 回到首页
    #driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view/uni-view/uni-view/uni-text").click()
    driver.back()
    place_spider(driver)
    driver.quit()

def test_login(word):
    driver = driverUtils().begin()
    driver.get(inviteUrl)
    # 点击登陆按钮
    driver.find_element(By.XPATH, '//*[@id="home"]/uni-view/uni-view[4]/uni-view[1]').click()
    # 输入助记词
    driver.find_element(By.XPATH, '//*[@id="MnemonicConfirm"]/uni-view/uni-textarea/div/textarea').send_keys(word)
    time.sleep(0.5)
    driver.find_element(By.XPATH, '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view').click()
    driver.find_element(By.XPATH, '//*[@id="Book"]/uni-view').click()
    shopping(driver)
    place_spider(driver)
    driver.quit()

def place_spider(driver):
    # 进入Island
    driver.find_element(By.XPATH,'//*[@id="StartSpiders"]').click()
    #点击云朵
    time.sleep(0.5)
    driver.find_element(By.XPATH,'/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[6]').click()
    #点击坑位
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[11]/uni-view[2]/uni-view/uni-view/uni-view[3]/uni-scroll-view/div/div/div/uni-checkbox-group/uni-view/uni-view[1]").click()
    # 放置蜘蛛
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[16]/uni-view[2]/uni-view/uni-view/uni-view[3]/uni-scroll-view/div/div/div/uni-checkbox-group/uni-view/uni-view[1]/uni-view[1]/uni-checkbox/div").click()
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[16]/uni-view[2]/uni-view/uni-view/uni-view[3]/uni-scroll-view/div/div/div/uni-checkbox-group/uni-view/uni-view[2]/uni-view[1]/uni-checkbox/div").click()
    # 确认
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[16]/uni-view[2]/uni-view/uni-view/uni-view[4]/uni-button").click()
    # 推出
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[11]/uni-view[2]/uni-view/uni-view/uni-image/img").click()

def shopping(driver):
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[8]/uni-view[1]/uni-image").click()
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[17]/uni-view[2]/uni-view/uni-view/uni-view[2]/uni-scroll-view/div/div/div/uni-view[1]/uni-view[1]/uni-view[2]/uni-view[1]/uni-view").click()
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[17]/uni-view[2]/uni-view/uni-view/uni-view[2]/uni-scroll-view/div/div/div/uni-view[1]/uni-view[1]/uni-view[2]/uni-view[1]/uni-view").click()
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[17]/uni-view[2]/uni-view/uni-view/uni-view[2]/uni-scroll-view/div/div/div/uni-view[1]/uni-view[1]/uni-view[2]/uni-view[1]/uni-view").click()
    driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[17]/uni-view[2]/uni-view/uni-view/uni-image/img").click()

def test_http_login(word:str="require desk evil visit panther copy ethics topple memory area smart weekend"):
    url = "https://siw.spiderweb.work/api/user/login"
    baseData = '{"type":0,"privateKey":"","password":"","mnemonic":"'+word+'","channel":1,"fnejnreoi":"1234567891234567"}'
    encrypt_data = setData(baseData)
    aes_encrypt(baseData, req_aes_key, req_aes_IV)
    try:
        res = client.post(url, json=encrypt_data,headers=setHeader(aes_encrypt(baseData,req_aes_key,req_aes_IV)))
        res_json = res.get("response").json().get("data")
        data = getData(res_json).get("data")
        data = json.loads(data).get("userinfo")
        atoken = data.get("atoken")
        siw = data.get("siw")
        token = data.get("token")
        task_step = data.get("task_step")
        if task_step == 0:
            log(f"账号token{token},未过认证")
        else:
            log(f"账号token{token}已认证,atoken余额{atoken},siw余额{siw}")
        return token,task_step
    except:
        log("账号异常")
        return ""

# 获取个人信息
def test_userInfo(token:str="935d14cd-c628-4260-8114-bbb0052db892"):
    data = {"token":token}
    url = "https://siw.spiderweb.work/api/user/userInfo"
    res = client.post(url, data=data,headers=setHeader(data,token))
    data = getData(res.get('response').json().get('data')).get('data')
    data = json.loads(data)
    userInfo = data.get('userinfo')
    atoken =  userInfo.get("atoken")
    siw = userInfo.get("siw")
    siw = str(int(float(siw)*100)/100)
    nickname = userInfo.get("nickname")
    score = userInfo.get("score")
    log(f"账号{nickname}登陆成功,atoken数量为{atoken},siw{siw},积分为数量为{score}")
    return score,siw

# 签到
def test_usermining(token:str="413dbcc9-a914-4e40-99fd-b3bf191e235b"):
    url = "https://siw.spiderweb.work/api/user/usermining"
    res = client.post(url, data={},headers=setHeader("",token))
    log(res.get("content"))

# 开矿场
def test_unlock(token:str="8e1751a3-638c-465d-ad3a-db5bed91a764"):
    url = "https://siw.spiderweb.work/api/user/kuangWeiUnlockV2"
    data = {"kuang_id":1,"unLock_type":0}
    res = client.post(url,json=data,headers=setHeader(data,token))
    log(res.get("content"))
# 挖矿详情
def test_mining(token:str="8e1751a3-638c-465d-ad3a-db5bed91a764"):
    url = "https://siw.spiderweb.work/api/user/wakuanging"
    data = {"kuang_id":1,"page":1}
    res = client.post(url,json=data,headers=setHeader(data,token))
    res_data = res.get('response').json().get('data')
    data = getData(res_data).get('data')
    data =  json.loads(data)
    limitCount = data.get('kuang_limit')
    miningCount = data.get('miner_num')
    minering = data.get('minering')
    zeroArr = []
    for i in minering:
        id = i.get("id")
        energy = i.get("energy")
        if energy == "0.00":
            zeroArr.append(id)
    log(f"当前有{limitCount}个矿坑,已放入{miningCount}个矿工，有{len(zeroArr)}个矿工已过期")
    return limitCount,miningCount,zeroArr

# 选择我的空闲矿工
def test_myMiner(token:str="8e1751a3-638c-465d-ad3a-db5bed91a764"):
    jackArr = []
    petterArr = []
    zeroArr = []
    url = "https://siw.spiderweb.work/api/user/myAllKuangGong"
    data = {"page":1}
    res = client.post(url,json=data,headers=setHeader(data,token))
    res_data = res.get("response")
    res_json = res_data.json().get("data")
    res_des = getData(res_json)
    data = res_des.get('data')
    data = json.loads(data).get("data")
    for d in data:
        energy = d.get("energy")
        box_name = d.get('box_name')
        id = d.get('id')
        if(energy == "0.00"):
            zeroArr.append(id)
        else:
            if(box_name == "Jack"):
                jackArr.append(id)
            else:
                petterArr.append(id)
    log(f"总体情况:jack有{len(jackArr)}个，peter有{len(petterArr)}个，已过期有{len(zeroArr)}个")
    return jackArr, petterArr, zeroArr

# 取下矿工
def test_cancelMiner(ids:str="100651",token:str="935d14cd-c628-4260-8114-bbb0052db892"):
    url = "https://siw.spiderweb.work/api/user/batchCancelKuangShan"
    data_raw = '{"group_id":1,"sell_ids":"'+ids+'","fnejnreoi":"1234567891234567"}'
    data_enc = setData(data_raw)
    res = client.post(url,json=data_enc,headers=setHeader(data_enc,token))
    log(res.get('content'))

# 买蜘蛛
def test_buy(token:str="935d14cd-c628-4260-8114-bbb0052db892"):
    url = "https://siw.spiderweb.work/api/index/createOrder"
    data = {"box_id":24,"pay_type":1,"num":1,"price_amount":"480.00"}
    res = client.post(url,json=data,headers=getBuyHeader(token))
    log(res.get("content"))
# 上矿工
def test_batchMiner(ids:str="45535",token:str="8e1751a3-638c-465d-ad3a-db5bed91a764"):
    url = "https://siw.spiderweb.work/api/user/batchStoreKuangShan"
    data_enc = '{"sell_ids":"'+ids+'","group_id":1,"fnejnreoi":"1234567891234567"}'
    data_raw = setData(data_enc)
    res = client.post(url,json=data_raw,headers=setHeader(data_enc,token))
    log(res.get('content'))

def test_mine(token):
    limitCount, miningCount, zeroArr = test_mining(token)
    if limitCount-miningCount == 0 and len(zeroArr) == 0:
        log("矿场状态正常")
    else:
        if len(zeroArr) != 0 :
            zeroStr = ""
            for i in range(len(zeroArr)):
                if(i != len(zeroArr)-1):
                    zeroStr = zeroStr + zeroArr[i] + ","
                else:
                    zeroStr = zeroStr + zeroArr[i]
            log(f"矿坑正在下架，id为{zeroStr}")
            test_cancelMiner(zeroStr,token)
            miningCount = miningCount - len(zeroArr)
        log(f"正在选择上架矿工")
        jackArr, petterArr, zeroArr = test_myMiner(token)
        # mindCount是空余坑位 最大坑位-在挖坑位
        mindCount = limitCount - miningCount
        if mindCount == 0:
            log("所有矿坑正在正常工作")
        else:
            minerStr = ""
            # 空余坑位-jack数量 若小于零则全放jack，若大于零则为放jack数量+jackCount(peter数量)
            jackCount = mindCount - len(jackArr)
            if jackCount < 0:
                for i in range(mindCount):
                    if i != mindCount - 1:
                        minerStr = minerStr + jackArr[i] + ","
                    else:
                        minerStr = minerStr + jackArr[i]
            else:
                # peter的需求量 - peter的已有量
                # 若小于0则放peterCount个peter数量和jack数量
                # 若大于0则放 peter的已有量 和 jack数量
                peterCount = jackCount-len(petterArr)
                if peterCount < 0:
                    if len(jackArr) != 0:
                        for i in range(len(jackArr)):
                            if i != len(jackArr)-1:
                                minerStr = minerStr+jackArr[i]+","
                            else:
                                minerStr = minerStr + jackArr[i]
                    for i in range(len(petterArr)):
                        if i != len(petterArr)-1:
                            minerStr = minerStr+petterArr[i]+","
                        else:
                            minerStr = minerStr + petterArr[i]
                else:
                    if len(jackArr) != 0:
                        for i in range(len(jackArr)):
                            if i != len(jackArr)-1:
                                minerStr = minerStr+jackArr[i]+","
                            else:
                                minerStr = minerStr + jackArr[i]
                    for i in range(len(petterArr)):
                        if i != len(petterArr)-1:
                            minerStr = minerStr+petterArr[i]+","
                        else:
                            minerStr = minerStr + petterArr[i]
            log(f"上架蜘蛛id{minerStr}")
            test_batchMiner(minerStr,token)

def test_batchRegisiter():
    TonAddr = parseTonText(TonPath)
    count = TonAddr.get("count")
    lines = TonAddr.get("lines")
    log(f"共找到{count}个Ton钱包")
    for i in range(int(count)):
        test_regisiter(lines[count-i-1])
        delete_line(TonPath,count-i)


def test_batchAdopt():
    successCount = 0
    failCount = 0
    regisiterTXT = parseTxtFile(regisiterPath)
    count = regisiterTXT.get("count")
    lines = regisiterTXT.get("lines")
    log(f"总共发现{count}个账号")
    for id in range(int(count)):
        log(f"正在养第{id+1}个账号")
        account = lines[id]
        accountWord = account[2]
        # 开始养号
        token,task_step = test_http_login(accountWord)
        txt = account[0] + "----" + account[1] + "----" + account[2] + "----" + account[3] + "----" + account[4]
        if task_step == 0:
            log(f"登陆失败,已记录数据")
            addContent(failPath, txt)
            failCount = failCount + 1
            print("\n")
            continue;
        else:
            score,siw = test_userInfo(token)
            buyCount = int(int(score.replace(',', ''))//480)
            log(f"登陆成功,token为{token}")
            log(f"正在签到")
            test_usermining(token)
            log(f"签到已完成,正在进行转账")
            test_sendSiw(receiveId,siw,token)
            log(f"，正在购买蜘蛛,可以购买{buyCount}次蜘蛛")
            for i in range(buyCount):
                test_buy(token)
                time.sleep(1)
            log(f"蜘蛛购买完成，正在买矿池")
            test_unlock(token)
            time.sleep(1)
            test_unlock(token)
            time.sleep(1)
            test_unlock(token)
            log(f"买矿完成，正在更换矿工")
            test_mine(token)
            log(f"第{id+1}个账号已养号完毕")
            successCount = successCount + 1
            addContent(successPath, txt)
            print("\n")
    print(f"共养号{count}个，成功{successCount}个，失败{failCount}个")


if __name__ == '__main__':
    pytest.main()
    # # 注册脚本
    # test_batchRegisiter()
    # #登陆脚本
    # test_batchLoginr()
