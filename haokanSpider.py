import requests
import json
import pymysql
import shutil, os
import re
import emoji
import time
import sys
from random import choice

sys.path.append('./')

# 用代理就会报max tries的错误，原因不明，可能是网速慢？

class HaokanSpider:
    @staticmethod
    def get_videos():

        kind_list = ['yingshi', 'chongwu', 'keji', 'shishang', 'yinyue']
        kind_now = choice(kind_list)
        section_name = kind_now

        stop_words = []

        # proxy_ip = {'http': HaokanSpider.get_proxy()}

        index_url = 'https://haokan.baidu.com/web/video/feed'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'Referer': 'https://haokan.baidu.com/tab/gaoxiao_new',
            'Host': 'haokan.baidu.com',
            'Connection': 'close'
        }

        params = {
            'tab': section_name+'_new',
            'act': 'pcFeed',
            'pd': 'pc',
            'num': '20'
        }

        # #1、增加重试连接次数
        # requests.DEFAULT_RETRIES = 5
        # s = requests.session()
        # #2、关闭多余的连接
        # s.keep_alive = False


        page_response = requests.get(index_url, headers=headers, params=params).content.decode('utf8')
        works_list = json.loads(page_response)['data']['response']['videos']
        print('获取好看数据成功：'+section_name)

        db = pymysql.connect(host="localhost", user="root", password="root", database="switcher")
        cursor = db.cursor()

        for piece in works_list:
            if any(stop_word in piece['photo']['caption'] for stop_word in stop_words):
                continue  # 有停止词就跳过这条
            # 赋值一些已经有的数据
            nid = piece['id']
            video_path = 'E:/项目目录/kuaishouSwitcher/video/' + nid + '.mp4'
            cover_path = 'E:/项目目录/kuaishouSwitcher/cover/' + nid + '.jpg'

            title = piece['title']
            # 过滤掉emoji符号
            title = re.sub('(\:.*?\:)', '', emoji.demojize(title))
            if '#' in title:
                # title = re.sub('#.*?#', '', title)
                title = title.replace('#', '')
            if '@' in title:
                title = title[:(title.find('@'))]  # 切掉'@'后面所有的内容
            if title.strip() == '':
                continue

            video_url = piece['play_url']
            cover_url = piece['poster_pc']

            # 每一条下载中间要间隔5秒，防止访问太快被封ip
            time.sleep(1)

            # 下载视频和封面
            try:
                # proxy_ip = {'http': HaokanSpider.get_proxy()}  # 更新代理ip（根据代理设置，超时了它会换IP的）
                video_content = requests.get(url=video_url, headers=headers).content
                print(video_url)
                print(video_content)
                with open(video_path, 'wb') as fp:
                    fp.write(video_content)
                cover_content = requests.get(url=cover_url, headers=headers).content
                with open(cover_path, 'wb') as fp:
                    fp.write(cover_content)
            except Exception as e:
                print(e)
                #requests.get('http://api.thread.zdaye.com/?action=Change')
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

