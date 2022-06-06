from kuaishouspider import KuaishouSpider as ksSpider
from haokanSpider import HaokanSpider as hkSpider
from meipaiSpider import MeipaiSpider as mpSpider
from bilibiliPost import  BilibiliPost as bbp
import pymysql
import time
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import  datetime

sys.path.append('./')




# 运行此文件即可投稿
if __name__ == "__main__":


    while True:

        print('当前时间', datetime.now())

        ksSpider.truncate_video()
        # try:
        #     hkSpider.get_videos('yingshi')
        # except Exception as e:
        #     print('hkyingshi:', e)




        # try:
        #     hkSpider.get_videos()
        # except Exception as e:
        #     print('hkyingshi:', e)
        try:
            ksSpider.get_videos()
        except Exception as e:
            print('ks:', e)
        try:
            mpSpider.get_hot_videos()
        except Exception as e:
            print('mp:', e)
        try:
            mpSpider.get_videos()
        except Exception as e:
            print('mp:', e)




        time.sleep(1)


        db = pymysql.connect(host="localhost", user="root", password="root", database="switcher")
        cursor = db.cursor()
        sql = "select title, id, video_path, cover_path from works_list where used='False'"
        cursor.execute(sql)
        works_list = cursor.fetchall()
        db.close()


        if len(works_list) == 0:
            #print('所有的都刷新到过，重新爬取')
            #time.sleep(180)
            #continue

        print('有', len(works_list), '个素材可供使用')

        for work_info in works_list:
            try:
                bbp.post_video(work_info)
                # time.sleep(60) # 投稿网页打开与关闭之间冷却1分钟
            except Exception:
                continue


        continue


