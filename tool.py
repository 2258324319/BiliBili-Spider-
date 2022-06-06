from PIL import Image
from time import sleep
import requests
from lxml import etree
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ChromeOptions
from PIL import Image
import subprocess
import json
import re
import pymysql
import random,time
import sys

sys.path.append('./')


def cut_code_img(driver, code_xpath, plat_name): # code_xpath是验证码在页面中的xpath， platname是平台名字
    # 截图整张页面
    driver.maximize_window()  # 窗口最大化
    sleep(0.5)
    driver.save_screenshot('./login_page_'+plat_name+'.png')
    # 确定验证码图片左上角和右下角坐标（裁剪区域）
    # code_img_ele.location 返回验证码左上角坐标(字典)
    # code_img_size 长度和宽度（字典）
    code_img = driver.find_element_by_xpath(code_xpath)
    location = code_img.location
    size = code_img.size
    # 左上角和右下角坐标(笔记本默认125%缩放)
    rangle = (
        int(location['x'] * 1.25), int(location['y'] * 1.25), int((location['x'] + size['width']) * 1.25),
        int((location['y'] + size['height']) * 1.25)
    )

    # 裁剪
    i = Image.open('./login_page_'+plat_name+'.png')
    code_img_name = './code_'+plat_name+'.png'
    # 根据指定区域裁剪
    frame = i.crop(rangle)
    frame.save(code_img_name)


def verify_code(plat_name, code_type):
    chaojiying = Chaojiying_Client('whybiyesheji', 'Uestc105455', '912623')	#用户中心>>软件ID 生成一个替换 96001
    im = open('./code_'+plat_name+'.png', 'rb').read()													#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    return chaojiying.PostPic(im, code_type)											#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
#


# 下面两个函数都是返回selenium的隐藏设置
def chrome_options_settings(): # 返回一个option
    # 反反爬，隐藏selenium(借鉴) 超级超级重要
    command = R"C:\Users\WuHanyu\AppData\Local\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir=C:\\selenium\\AutomationProfile"
    subprocess.Popen(command, shell=True)
    chrome_options = Options()
    # 无头
    chrome_options.headless = True
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chrome_options.add_argument("window-size=1920,1080")
    return chrome_options

def options_settings():
    # 无头浏览器提高性能
    options = ChromeOptions()
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')

    return options


# 清空某表的数据
def empty_table(tableName):
    db = pymysql.connect(host="localhost", user="root", password="root", database="spiderSys")
    cursor = db.cursor()

    sql = 'TRUNCATE TABLE ' + tableName + ';' ## 清空表

    try:
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()# 失败回滚
        print('truncate table fail!')
        print(e)

    db.close()