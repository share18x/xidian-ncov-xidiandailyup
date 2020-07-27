#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json
import requests
import re
import sys
import os
import time

# output log
def print_output_log():
    print("正在记录日志中......\n")
    output_str = "最终输出：\n"
    output_str += str(predef) + "\n"
    output_str += result.text + "\n"
    output_str += time.strftime("%Y-%m-%d %H:%M:%S\n", time.localtime())
    with open(currentdir + "/output.log", "a") as fd:
        fd.write(output_str)

if os.path.exists("NOSUBMIT"):
    exit()

data = {}

currentdir = os.path.dirname(os.path.abspath(__file__))
with open(currentdir + "\\data.json") as fd:
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

# print("打印正则调试：\n%s" % re.search('"info":({.*}),"ontime"',result.text).group(1))
# print("打印输入：\n" + str(data))


#读取网页记录
predef = json.loads(re.search('"info":({.*}),"ontime"',result.text).group(1))
# print("打印上次提交记录：\n"+ str(predef))


if "dump_geo" in sys.argv:
    print(predef['geo_api_info'])
    exit()

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

#最终测试
# while True:
#     select = input("真的要提交吗？\n请输入YES\\NO\n")
#     if select == "YES":
#         break
#     elif select == "NO":
#         exit()

result = conn.post('https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save',data=predef)

print_output_log()
time.sleep(10)
