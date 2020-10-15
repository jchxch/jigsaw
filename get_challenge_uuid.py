import base64
import json
import requests
import re
from bs4 import BeautifulSoup
# def gethtml(url):
#     try:
#         resp = requests.request('get', url)
#         resp.raise_for_status()
#         resp.encoding = resp.apparent_encoding
#         #print(resp.text)
#         return resp.text
#     except:
#         print('err')
#
#
# def getProblem():
#     url = "http://47.102.118.1:8089/api/challenge/list"
#     # 每次请求的结果都不一样，动态变化
#     text = json.loads(gethtml(url))
#     # print(text.keys())#dict_keys(['img', 'step', 'swap', 'uuid'])
#     # text["img"] = "none" #{'img': 'none', 'step': 0, 'swap': [7, 7], 'uuid': '3bc827e5008d460b893e5cb28769e6bf'}
#     return text
res = requests.get('http://47.102.118.1:8089/api/challenge/list')
soup = BeautifulSoup(res.text, 'html.parser')



print(re.findall(r'"uuid":"(.*?)"}',str(soup)))
