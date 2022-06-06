import requests
import json
import pymysql
import shutil, os
import re
import emoji
import time
import sys
from random import choice
from random import randint
import base64

sys.path.append('./')

# 用代理就会报max tries的错误，原因不明，可能是网速慢？

class MeipaiSpider:

    MAX_PAGE = 200
    # 最大页数参数

    def Decrypt_video_url(content):
        str_start = content[4:]

        list_temp = []
        list_temp.extend(content[:4])
        list_temp.reverse()
        hex = ''.join(list_temp)

        dec = str(int(hex, 16))
        list_temp1 = []
        list_temp1.extend(dec[:2])
        pre = list_temp1

        list_temp2 = []
        list_temp2.extend(dec[2:])
        tail = list_temp2

        str0 = str_start[:int(pre[0])]
        str1 = str_start[int(pre[0]):int(pre[0]) + int(pre[1])]

        result1 = str0 + str_start[int(pre[0]):].replace(str1, '')

        tail[0] = len(result1) - int(tail[0]) - int(tail[1])

        a = result1[:int(tail[0])]
        b = result1[int(tail[0]):int(tail[0]) + int(tail[1])]
        c = (a + result1[int(tail[0]):].replace(b, ''))

        return base64.urlsafe_b64decode(c).decode()



    @staticmethod
    def get_videos():

        stop_words = []

        # 从里面抽一个类型的来爬
        kinds_list = ['62', '63', '474', '13', '16', '62', '460', '59', '27', '6', '426', '487', '450']
        kind_now = choice(kinds_list)

        #proxy_ip = {'http': HaokanSpider.get_proxy()}

        index_url = 'https://www.meipai.com/squares/new_timeline/'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'Connection': 'close'
        }

        page = str(randint(1, 200))
        params = {
            'page': page,
            'count': '24',
            'tid': kind_now
        }

        page_response = requests.get(index_url, headers=headers, params=params).content.decode('utf8')
        works_list = json.loads(page_response)['medias']
        print('获取美拍数据成功：'+kind_now+' page:', page)

        db = pymysql.connect(host="localhost", user="root", password="root", database="switcher")
        cursor = db.cursor()

        for piece in works_list:
            if any(stop_word in piece['caption'] for stop_word in stop_words):
                continue  # 有停止词就跳过这条
            # 赋值一些已经有的数据
            nid = piece['id']
            video_path = 'E:/项目目录/kuaishouSwitcher/video/' + nid + '.mp4'
            cover_path = 'E:/项目目录/kuaishouSwitcher/cover/' + nid + '.jpg'

            title = piece['caption']
            # 过滤掉emoji符号
            title = re.sub('(\:.*?\:)', '', emoji.demojize(title))
            if '#' in title:
                # title = re.sub('#.*?#', '', title)
                title = title.replace('#', '')
            if '@' in title:
                title = title[:(title.find('@'))]  # 切掉'@'后面所有的内容

            try:
                video_url = MeipaiSpider.Decrypt_video_url(piece['video'])
                cover_url = piece['cover_pic']
            except Exception as e:
                print('mp:', e)
                continue

            # 每一条下载中间要间隔1秒，防止访问太快被封ip
            time.sleep(1)

            # requests.adapters.DEFAULT_RETRIES = 5

            # 下载视频和封面
            try:
                # proxy_ip = {'http': HaokanSpider.get_proxy()}  # 更新代理ip（根据代理设置，超时了它会换IP的）
                video_content = requests.get(url=video_url, headers=headers).content
                with open(video_path, 'wb') as fp:
                    fp.write(video_content)
                cover_content = requests.get(url=cover_url, headers=headers).content
                with open(cover_path, 'wb') as fp:
                    fp.write(cover_content)
            except Exception as e:
                print(e)
                # requests.get('http://api.thread.zdaye.com/?action=Change')
                continue

            sql = "INSERT IGNORE INTO works_list(title, id, video_path, cover_path, used) \
                                VALUES ('%s', '%s', '%s', '%s', 'False')" % (title, nid, video_path, cover_path)
            try:
                cursor.execute(sql)
                db.commit()
                print('insert' + nid + 'success!')
            except Exception as e:
                db.rollback()  # 失败回滚
                print('insert' + nid + 'fail!')
                print(e)

        db.close()

    @staticmethod
    def get_hot_videos():

        stop_words = []

        # proxy_ip = {'http': HaokanSpider.get_proxy()}

        index_url = 'https://www.meipai.com/home/hot_timeline/'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'Connection': 'close'
        }

        page = str(randint(1, 10000000))
        params = {
            'page': page,
            'count': '12'
        }

        page_response = requests.get(index_url, headers=headers, params=params).content.decode('utf8')
        works_list = json.loads(page_response)['medias']
        print('获取美拍热门数据成功：'+ ' page:', page)

        db = pymysql.connect(host="localhost", user="root", password="root", database="switcher")
        cursor = db.cursor()

        for piece in works_list:
            if any(stop_word in piece['caption'] for stop_word in stop_words):
                continue  # 有停止词就跳过这条
            # 赋值一些已经有的数据
            nid = piece['id']
            video_path = 'E:/项目目录/kuaishouSwitcher/video/' + nid + '.mp4'
            cover_path = 'E:/项目目录/kuaishouSwitcher/cover/' + nid + '.jpg'

            title = piece['caption']
            # 过滤掉emoji符号
            title = re.sub('(\:.*?\:)', '', emoji.demojize(title))
            if '#' in title:
                # title = re.sub('#.*?#', '', title)
                title = title.replace('#', '')
            if '@' in title:
                title = title[:(title.find('@'))]  # 切掉'@'后面所有的内容
            if title.strip() == '':
                continue

            try:
                video_url = MeipaiSpider.Decrypt_video_url(piece['video'])
                cover_url = piece['cover_pic']
            except Exception as e:
                print('mp:', e)
                continue

            # 每一条下载中间要间隔1秒，防止访问太快被封ip
            time.sleep(1)

            # requests.adapters.DEFAULT_RETRIES = 5

            # 下载视频和封面
            try:
                # proxy_ip = {'http': HaokanSpider.get_proxy()}  # 更新代理ip（根据代理设置，超时了它会换IP的）
                video_content = requests.get(url=video_url, headers=headers).content
                with open(video_path, 'wb') as fp:
                    fp.write(video_content)
                cover_content = requests.get(url=cover_url, headers=headers).content
                with open(cover_path, 'wb') as fp:
                    fp.write(cover_content)
            except Exception as e:
                print(e)
                # requests.get('http://api.thread.zdaye.com/?action=Change')
                continue

            sql = "INSERT IGNORE INTO works_list(title, id, video_path, cover_path, used) \
                                    VALUES ('%s', '%s', '%s', '%s', 'False')" % (title, nid, video_path, cover_path)
            try:
                cursor.execute(sql)
                db.commit()
                print('insert' + nid + 'success!')
            except Exception as e:
                db.rollback()  # 失败回滚
                print('insert' + nid + 'fail!')
                print(e)

        db.close()



# 切换并获得代理ip
    @staticmethod
    def get_proxy():
        headers = {
            'host': 'api.thread.zdaye.com'
        }
        proxy_ip = requests.get('http://api.thread.zdaye.com/?action=Show', headers=headers).content.decode('utf8')
        proxy_ip = "".join(proxy_ip.split())
        proxy_ip = proxy_ip.replace(r'\"', '"')
        proxy_ip_json = eval(proxy_ip)
        print("刷新代理IP:", proxy_ip_json['thisip'])
        proxy_ip = proxy_ip_json['thisip']['ip']
        return proxy_ip


