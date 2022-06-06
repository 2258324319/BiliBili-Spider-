import requests
import json
import pymysql
import shutil, os
import re
import emoji
import time
import sys
import base64


# 解密video的URL
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

    return base64.b64decode(c).decode()


headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'Connection': 'close'
        }
params = {
    'page': '2',
    'count': '24',
    'tid': '474',
    'maxid': '6802413623728594235'
}
response = requests.get(url='https://www.meipai.com/squares/new_timeline', headers=headers, params=params).content.decode('utf8')
print(response)
time.sleep(1)
response =requests.get(url='https://img.app.meitudata.com/meitumv/template/recommendMediasTemplate.eot?v2.9.0' ,headers=headers).content.decode('utf8')

time.sleep(1)
response = requests.get(url='https://www.meipai.com/squares/new_timeline', headers=headers, params=params).content.decode('utf8')
print(response)


