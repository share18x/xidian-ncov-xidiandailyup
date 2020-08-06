#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import json
import requests
import re
import sys
import os
import time


def time_judge():
    t = int(time.strftime("%H", time.localtime()))
    if t < 8:
        return "凌晨\n"
    elif t < 12:
        return "早上\n"
    elif t < 14:
        return "中午\n"
    elif t < 18:
        return "下午\n"
    elif t < 24:
        return "晚上\n"
    else:
        print("输入错误")
        exit(1)


def notice_func(input):
    input = json.loads(input.text)
    text = time.strftime("时间：\n%Y-%m-%d %X\n", time.localtime()) + input['m']

    if not os.path.exists(currentdir + "/notice.json"):
        exit(0)
    with open(currentdir + "/notice.json", "r") as fd:
        data1 = json.load(fd)

    if data1['server_chan'] == 1:
        url = "https://sc.ftqq.com/" +\
             data1['key_server'] + \
                 ".send"
        data = {'text':'晨午晚检填报报告：' + time_judge(), 'desp':text}
        output = conn.post(url, data = data)


    if data1['telegram_bot'] == 1:
        url = "https://api.telegram.org/bot" + \
            data1['key_bot'] + \
                "/sendMessage"
        data = {'chat_id':data1['chat_id'], 'text':"晨午晚检填报报告：\n" + time_judge() + text}
        # 读取代理设置
        if  os.path.exists(currentdir + "/proxies.json"):
            with open(currentdir + "/proxies.json", "r") as fd:
                proxies = json.load(fd)        
            output1 = conn.post(url, data = data, proxies = proxies)
        else:
            output1 = conn.post(url, data = data)


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
with open(currentdir + "/data.json") as fd:
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



#读取网页记录
predef = json.loads(re.search('"info":({.*}),"ontime"',result.text).group(1))


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

result = conn.post('https://xxcapp.xidian.edu.cn/xisuncov/wap/open-report/save',data=predef)


print_output_log()
notice_func(result)
time.sleep(10)
