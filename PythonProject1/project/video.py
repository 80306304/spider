from datetime import time

import pyperclip
import pytest
from selenium.webdriver.common.by import By

from utils._http import RequestClient
from utils.seleniumUtils import *


def test_regisiter():
    driver = driverUtils().begin()
    driver.get("https://www.mindvideo.ai/zh/auth/signup/?utm_source=invitation&invite_code=4WT0M7ZO")
    # 输入邮箱、昵称、密码
    input_email = driver.find_element(By.XPATH,'//*[@id="email"]')
    input_nickname = driver.find_element(By.XPATH,'//*[@id="nickname"]')
    input_pwd = driver.find_element(By.XPATH,'//*[@id="password"]')
    input_email.send_keys("121216")
    input_nickname.send_keys("121216")
    input_pwd.send_keys("121216")

    log(f"昵称：{input_email} 密码：121216")
    time.sleep(0.5)
    # 确认按钮
    enter_button = driver.find_element(By.XPATH,'/html/body/div[3]/div[2]/div/section/div/form/div[4]/div/div/div/div/button')
    enter_button.click()
    # 获取助记词
    copy_button = driver.find_element(By.XPATH,
                                      '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[1]/uni-view[2]/uni-view[1]/uni-view[2]/uni-image')
    copy_button.click()
    # clipboard_content = pyperclip.paste()
    # split_content = clipboard_content.split()
    # log(f"助记词：{clipboard_content}")
    # driver.find_element(By.XPATH,
    #                     '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view').click()
    # # 输入助剂次
    # for i in split_content:
    #     driver.find_element(By.XPATH, f"//*[text()='{i}']").click()
    #     time.sleep(0.2)
    # driver.find_element(By.XPATH,
    #                     "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[2]/uni-view").click()
    # # 复制链接地址
    # driver.find_element(By.XPATH,
    #                     "/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[2]/uni-view[1]/uni-view[2]/uni-view[1]/uni-view[2]/uni-view[2]/uni-image").click()
    # pocket = pyperclip.paste()
    # log(f"钱包地址：{pocket}")
    # # 点击绑定按钮
    # driver.find_element(By.XPATH, '//*[@id="Book"]').click()
    # driver.find_element(By.XPATH,
    #                     '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[3]/uni-view/uni-text/span').click()
    # addr_input = driver.find_element(By.XPATH,
    #                                  '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view[2]/uni-view/uni-view/uni-view/uni-view[1]/uni-view/uni-input/div/input')
    # addr_input.send_keys(TonAddr)
    # time.sleep(0.5)
    # driver.find_element(By.XPATH,
    #                     '/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[7]/uni-view[2]/uni-view/uni-view/uni-view/uni-view[2]').click()
    # # 记录数据
    # out_txt = f"{}----121216----{clipboard_content}----{pocket}----{getNowTime()}"

    # 回到首页
    #driver.find_element(By.XPATH,"/html/body/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view[2]/uni-view[2]/uni-view/uni-view/uni-view/uni-text").click()
    driver.back()
    driver.quit()

if __name__ == '__main__':
    pytest.main()