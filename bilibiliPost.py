# selenium

from selenium import webdriver
import win32gui
import win32con
from selenium.webdriver.common.keys import Keys
import time
import pymysql
import tool
import json
from  datetime import  datetime


class BilibiliPost:

    @staticmethod
    def post_video(work_info):
        # work_info就是works_list里的一个元素
        title = work_info[0]
        nid = work_info[1]
        video_path = work_info[2]
        cover_path = work_info[3]
        # 要把路路径的正斜杠全换成反斜杠，否则文件管理器找不到文件
        video_path = video_path.replace('/', '\\')
        cover_path = cover_path.replace('/', '\\')


        chrome_options = tool.chrome_options_settings()
        options = tool.options_settings()

        bro = webdriver.Chrome(executable_path='./chromedriver', options=options, chrome_options=chrome_options)
        bro.implicitly_wait(30)  # 设置隐式等待


        # bro.delete_all_cookies()
        # #   添加新cookie
        # with open('cookies.txt', 'r') as f:
        #     # 使用json读取cookies 注意读取的是文件 所以用load而不是loads
        #     cookies_list = json.load(f)
        #
        #     # 方法1 将expiry类型变为int
        #     for cookie in cookies_list:
        #         # 并不是所有cookie都含有expiry 所以要用dict的get方法来获取
        #         if isinstance(cookie.get('expiry'), float):
        #             cookie['expiry'] = int(cookie['expiry'])
        #         bro.add_cookie(cookie)
        #
        # bro.refresh()

        bro.get('https://member.bilibili.com/platform/upload/video/frame')
        try:
            bro.switch_to.alert.accept()
        except Exception as e:
            print(datetime.now())
        bro.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})", '')
        # try:
        #     bro.switch_to.alert.accept()
        # except Exception as e:
        #     print(e)

        time.sleep(2)# 先用这20秒登陆

        bro.switch_to.frame('videoUpload')# 进入iframe
        upload = bro.find_element_by_id('bili-upload-btn')
        upload.click()

        time.sleep(2)

        # win32gui解决文件选择窗口
        dialog = win32gui.FindWindow('#32770', u'打开')  # 对话框
        ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None)
        ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
        Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)  # 上面三句依次寻找对象，直到找到输入框Edit对象的句柄
        button = win32gui.FindWindowEx(dialog, 0, 'Button', None)  # 确定按钮Button

        win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, video_path)  # 往输入框输入绝对地址
        win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button)  # 按button
        print(upload.get_attribute('value'))

        # cover_upload = bro.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div[1]/div[2]/div[2]/div[1]/input')
        # cover_upload.send_keys(cover_path)  # send_keys
        # print(cover_upload.get_attribute('value'))

        # 选择接下来的一些参数
        # zizhi = bro.find_element_by_xpath('//*[@id="app"]/div[2]/div[2]/div[3]/div[1]/div[4]/div[2]/div[1]/span[2]')
        # zizhi.click()

        biaoti = bro.find_element_by_xpath('//*[@id="app"]//input[@placeholder="请输入稿件标题"]')
        biaoti.send_keys(Keys.CONTROL, 'a')
        biaoti.send_keys(title)

        # 选择分类
        # select_btn = bro.find_element_by_xpath('//*[@id="type-list-v2-container"]/div[2]/div')
        # select_btn.click()
        # tuijianxuanze = select_btn.find_element_by_xpath('./div[2]/div[1]/div[1]')
        # tuijianxuanze.click()
        # default_fenlei = bro.find_element_by_xpath('./div[2]/div[2]/div[1]')
        # default_fenlei.click()

        # # 点击第一个推荐标签
        # tag1 = bro.find_element_by_xpath('//*[@id="content-tag-v2-container"]/div[3]/div/div[1]/p/span')
        # tag1.click()
        #  再输入一个自己的标签
        tag_input = bro.find_element_by_xpath('//*[@id="content-tag-v2-container"]//input[@placeholder="按回车键Enter创建标签"]')
        tag_input.send_keys(Keys.CONTROL, 'a')
        tag_input.send_keys('短视频')
        tag_input.send_keys(Keys.ENTER)
        tag_input.click()#

        time.sleep(3) # 等待上面的操作彻底执行再提交稿件


        # 投稿
        tougao = bro.find_element_by_class_name('submit-btn-group-add')
        tougao.click()

        # 等待8分钟，防止视频没有上传完，并且减少频率
        time.sleep(60)
        bro.close()

        print('投稿成功')
