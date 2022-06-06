import requests
import json

headers = {
    'host': 'api.thread.zdaye.com'
}
response = requests.get('http://api.thread.zdaye.com/?action=Change', headers=headers)
print(response.text)

# payloadData_detail_headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
#     "Referer": "https://video.kuaishou.com/video/3x7u4ybaxqwd6yq?authorId=3xi4a3vru5ze6gy&tabId=0",
#     'Host': 'video.kuaishou.com',
# }
# payloadData_detail = {
#     "operationName": "visionVideoDetail",
#     "variables": {
#         "photoId": "3x7u4ybaxqwd6yq",
#         "page": "detail"
#     },
#     "query": "query visionVideoDetail($photoId: String, $type: String, $page: String, $webPageArea: String) {\n  visionVideoDetail(photoId: $photoId, type: $type, page: $page, webPageArea: $webPageArea) {\n    status\n    type\n    author {\n      id\n      name\n      following\n      headerUrl\n      __typename\n    }\n    photo {\n      id\n      duration\n      caption\n      likeCount\n      realLikeCount\n      coverUrl\n      photoUrl\n      liked\n      timestamp\n      expTag\n      llsid\n      viewCount\n      videoRatio\n      stereoType\n      croppedPhotoUrl\n      manifest {\n        mediaType\n        businessType\n        version\n        adaptationSet {\n          id\n          duration\n          representation {\n            id\n            defaultSelect\n            backupUrl\n            codecs\n            url\n            height\n            width\n            avgBitrate\n            maxBitrate\n            m3u8Slice\n            qualityType\n            qualityLabel\n            frameRate\n            featureP2sp\n            hidden\n            disableAdaptive\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    tags {\n      type\n      name\n      __typename\n    }\n    commentLimit {\n      canAddComment\n      __typename\n    }\n    llsid\n    __typename\n  }\n}\n"
# }
#
# # 从详情页获取到视频的URL()
# detail_response = requests.post('https://video.kuaishou.com/graphql', data=payloadData_detail, headers=payloadData_detail_headers).content.decode('utf8')
# print(detail_response)