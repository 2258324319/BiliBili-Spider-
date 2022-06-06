import requests
import json
import pymysql
import shutil, os
import re
import emoji
import time
import sys

sys.path.append('./')

class KuaishouSpider:

    @staticmethod
    def get_videos():

        stop_words = ['快手']  # 停止词

        # proxy_ip = {'http': KuaishouSpider.get_proxy()}

        index_url = 'https://video.kuaishou.com/graphql'



        # payloadData数据(爬短视频用的)
        payloadData = {
            "operationName": "brilliantTypeDataQuery",
            "variables": {
                "hotChannelId": "00",
                "page": "brilliant",
                "pcursor": "1"
            },
            "query": "fragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    id\n    duration\n    caption\n    likeCount\n    realLikeCount\n    coverUrl\n    photoUrl\n    coverUrls {\n      url\n      __typename\n    }\n    timestamp\n    expTag\n    animatedCoverUrl\n    distance\n    videoRatio\n    liked\n    stereoType\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  __typename\n}\n\nfragment photoResult on PhotoResult {\n  result\n  llsid\n  expTag\n  serverExpTag\n  pcursor\n  feeds {\n    ...feedContent\n    __typename\n  }\n  webPageArea\n  __typename\n}\n\nquery brilliantTypeDataQuery($pcursor: String, $hotChannelId: String, $page: String, $webPageArea: String) {\n  brilliantTypeData(pcursor: $pcursor, hotChannelId: $hotChannelId, page: $page, webPageArea: $webPageArea) {\n    ...photoResult\n    __typename\n  }\n}\n"
        }
        # # payloadData数据(爬长视频列表用的)
        # payloadData = {
        #     "operationName": "recoDataQuery",
        #     "variables": {
        #           "tabId": "0",
        #           "semKeyword": "",
        #           "semCrowd": "",
        #           "utmSource": "",
        #           "utmMedium": "",
        #           "page": "recommend",
        #           "pcursor": "1"
        #     },
        #     "query": "fragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    id\n    duration\n    caption\n    likeCount\n    realLikeCount\n    coverUrl\n    photoUrl\n    coverUrls {\n      url\n      __typename\n    }\n    timestamp\n    expTag\n    animatedCoverUrl\n    distance\n    videoRatio\n    liked\n    stereoType\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  __typename\n}\n\nfragment photoResult on PhotoResult {\n  result\n  llsid\n  expTag\n  serverExpTag\n  pcursor\n  feeds {\n    ...feedContent\n    __typename\n  }\n  webPageArea\n  __typename\n}\n\nquery recoDataQuery($tabId: Int, $pcursor: String, $semKeyword: String, $semCrowd: String, $utmSource: String, $utmMedium: String, $page: String) {\n  recoData(tabId: $tabId, pcursor: $pcursor, semKeyword: $semKeyword, semCrowd: $semCrowd, utmSource: $utmSource, utmMedium: $utmMedium, page: $page) {\n    ...photoResult\n    __typename\n  }\n}\n"
        # }

        # payload请求头设置
        payloadHeader = {
            'Host': 'video.kuaishou.com',
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            # 'Cookies': 'did=web_6fd1703ca8335d40c8278719bd32f0dd; didv=1619883516263; kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
        }

        page_response = requests.post(index_url, data=json.dumps(payloadData), headers=payloadHeader).content.decode('utf8')
        # 这里要对requests使用content属性再解码，直接用text属性会中文乱码
        #print("kuaishou_page_response:"+page_response)
        works_list = json.loads(page_response)['data']['brilliantTypeData']['feeds']
        print('获取快手数据成功')


        db = pymysql.connect(host="localhost", user="root", password="root", database="switcher")
        cursor = db.cursor()

        for piece in works_list:
            if any(stop_word in piece['photo']['caption'] for stop_word in stop_words):
                continue  # 有停止词就跳过这条
            # 赋值一些已经有的数据
            nid = piece['photo']['id']
            author_id = piece['author']['id']
            video_path = 'E:/项目目录/kuaishouSwitcher/video/' + nid + '.mp4'
            cover_path = 'E:/项目目录/kuaishouSwitcher/cover/' + nid + '.jpg'

            title = piece['photo']['caption']
            # 过滤掉emoji符号
            title = re.sub('(\:.*?\:)', '', emoji.demojize(title))
            if '#' in title:
                # title = re.sub('#.*?#', '', title)
                title = title.replace('#', '')
            if '@' in title:
                title = title[:(title.find('@'))]  # 切掉'@'后面所有的内容
            if title.strip() == '':
                continue

            video_url = piece['photo']['photoUrl']
            cover_url = piece['photo']['coverUrl']

            # 每一条下载中间要间隔5秒，防止访问太快被封ip
            # time.sleep(5)

            # # 爬长视频详情信息用的
            # referer = 'https://video.kuaishou.com/video/'+nid+'?authorId='+author_id+'&tabId=0'
            # payloadData_detail_headers = {
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            #     "Referer": referer,
            #     'Host': 'video.kuaishou.com'
            # }
            # payloadData_detail = {
            #     "operationName": "visionVideoDetail",
            #     "variables": {
            #         "photoId": nid,
            #         "page": "detail"
            #     },
            #     "query": "query visionVideoDetail($photoId: String, $type: String, $page: String, $webPageArea: String) {\n  visionVideoDetail(photoId: $photoId, type: $type, page: $page, webPageArea: $webPageArea) {\n    status\n    type\n    author {\n      id\n      name\n      following\n      headerUrl\n      __typename\n    }\n    photo {\n      id\n      duration\n      caption\n      likeCount\n      realLikeCount\n      coverUrl\n      photoUrl\n      liked\n      timestamp\n      expTag\n      llsid\n      viewCount\n      videoRatio\n      stereoType\n      croppedPhotoUrl\n      manifest {\n        mediaType\n        businessType\n        version\n        adaptationSet {\n          id\n          duration\n          representation {\n            id\n            defaultSelect\n            backupUrl\n            codecs\n            url\n            height\n            width\n            avgBitrate\n            maxBitrate\n            m3u8Slice\n            qualityType\n            qualityLabel\n            frameRate\n            featureP2sp\n            hidden\n            disableAdaptive\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    tags {\n      type\n      name\n      __typename\n    }\n    commentLimit {\n      canAddComment\n      __typename\n    }\n    llsid\n    __typename\n  }\n}\n"
            # }
            #
            # # 从详情页获取到视频的URL()
            # detail_response = requests.post(index_url, data=payloadData_detail, headers=payloadData_detail_headers, proxies=proxy_ip).content.decode('utf8')
            # print(detail_response)
            # detail_info = eval(detail_response)
            # print("detail_response:", detail_info)
            # video_url = detail_info['data']['photo']['photoUrl']

            # 下载视频和封面
            try:
                # proxy_ip = {'http': KuaishouSpider.get_proxy()}# 更新代理ip（根据代理设置，超时了它会换IP的）
                video_content = requests.get(url=video_url, headers=headers, timeout=60).content
                with open(video_path, 'wb') as fp:
                    fp.write(video_content)
                cover_content = requests.get(url=cover_url, headers=headers, timeout=60).content
                with open(cover_path, 'wb') as fp:
                    fp.write(cover_content)
            except Exception as e:
                print(e)
                continue

            sql = "INSERT IGNORE INTO works_list(title, id, video_path, cover_path, used) \
                    VALUES ('%s', '%s', '%s', '%s', 'False')" % (title, nid, video_path, cover_path)
            try:
                cursor.execute(sql)
                db.commit()
                print('insert'+nid+'success!')
            except Exception as e:
                db.rollback()  # 失败回滚
                print('insert'+nid+'fail!')
                print(e)


        db.close()

    @staticmethod
    def truncate_video():
            # 清空数据库表
            # db = pymysql.connect(host="localhost", user="root", password="root", database="switcher")
            # cursor = db.cursor()
            # sql = "TRUNCATE TABLE works_list"
            # try:
            #     cursor.execute(sql)
            #     db.commit()
            #     print('truncate success!')
            # except Exception as e:
            #     db.rollback()  # 失败回滚
            #     print('truncate fail!')
            #     print(e)

            #数据库表中全标为True
            db = pymysql.connect(host="localhost", user="root", password="root", database="switcher")
            cursor = db.cursor()
            sql = 'UPDATE works_list SET used="True"'
            try:
                cursor.execute(sql)
                db.commit()
                print('Mark used success!')
            except Exception as e:
                db.rollback()
                print('Mark used fail!')
                print(e)
            db.close()

            # 清空本地文件夹的文件
            shutil.rmtree(r"./video")
            shutil.rmtree(r"./cover")
            os.mkdir(r"./video")
            os.mkdir(r"./cover")
            # db.close()

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