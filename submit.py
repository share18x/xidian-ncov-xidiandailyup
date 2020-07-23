#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import requests
import re
import sys
import os
import time

if os.path.exists("NOSUBMIT"):
    exit()

data = {}

currentdir = os.getcwd()
#print(currentdir + "\\data.json")
with open(currentdir + "\\data.json","r") as fd:
    data=json.load(fd)
    
conn = requests.Session()

# Login
result = conn.post('https://xxcapp.xidian.edu.cn/uc/wap/login/check',data={'username':data['_u'],'password':data['_p']})
if result.status_code != 200:
    print('认证大失败')
    exit()

# Submit
result = conn.get('https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/index')
if result.status_code != 200:
    print('获取页面大失败')
    exit()

with open("last_get.html","w") as fd:
    fd.write(result.text)

#读取网页记录
predef = json.loads(re.search('"info":({.*}),"ontime"',result.text).group(1))

# if "dump_geo" in sys.argv:
#     print(predef['geo_api_info'])
#     exit()

try:
    del predef['jrdqtlqk']
    del predef['jrdqjcqk']
except:
    pass
del data['_u']
del data['_p']
del predef['date']
del predef['flag']
del predef['uid']
del predef['creator']
del predef['created']
del predef['id']
predef.update(data)

print("最终输出：\n" + str(predef))

result = conn.post('https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save',data=predef)
print(result.text)
time.sleep(10)
