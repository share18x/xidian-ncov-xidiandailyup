#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import json

def AskInteractive(description, options, delta=0):
    print(description)
    for index in range(len(options)):
        print(str(index)+". "+options[index])
    while True:
        ret = input("你的选择: ")
        try:
            val = int(ret)
            if val >= 0 and val < len(options):
                return val+delta
        except:
            pass
    
def AskText(description):
    return input(description)
    
def AskBoolean(description):
    while True:
        ret = input(description+'<Y/N> ').upper()
        if ret == "Y":
            return 1
        elif ret == "N":
            return 0
def AskABC(description):
    while True:
        ret = input(description+"\nA 绿色\nB 黄色\nC 红色\n").upper()
        if ret == "A":
            return 0
        elif ret == "B":
            return 1
        elif ret == "C":
            return 2
# Configuration

# 具体填报项目

print("#####\n温馨提示： 不外出、不聚集、不吃野味， 戴口罩、勤洗手、咳嗽有礼，开窗通风，发热就诊\n#####\n\n")

data = {}

# 统一认证账号密码
data.update({"_u":AskText("统一认证账号: ")})
data.update({"_p":AskText("统一认证密码: ")})



    
# 所在地点
IsInChina = AskBoolean("是否在国内: ")
if IsInChina == 0:
    data.update({"area":"国外","city":"国外","province":"国外"})
else:
    # 定位
    data.update({"geo_api_info":AskText("请输入定位结果: ")})
    geo = json.loads(data["geo_api_info"])
    data.update({"address":geo["formattedAddress"],"area":geo["addressComponent"]["province"] + ' ' + geo["addressComponent"]["city"] + ' ' + geo["addressComponent"]["district"],"province":geo["addressComponent"]["province"],"city":geo["addressComponent"]["city"]})
    if data["city"].strip() == "" and data["province"] in ["北京市","上海市","重庆市","天津市"]:
        data["city"] = data["province"]

# 体温范围
data.update({"tw":AskInteractive("今日体温范围(℃): ",["(-inf, 36]","(36, 36.5]","(36.5, 36.9]","(36.9, 37.3]","(37.3, 38]","(38, 38.5]","(38.5, 39]","(39, 40]","(40, +inf)"],1)})

#填写一码通颜色        
data.update({"ymtys":AskABC("今日西安“一码通”颜色？:")}) 

# 今日是否在校
data.update({"sfzx":AskBoolean("今日是否在校: ")})

# 是否处于隔离期
data.update({"sfcyglq":AskBoolean("是否处于隔离期: ")})

#是否出现乏力、干咳、呼吸困难等症状？
data.update({"sfyzz":AskBoolean("是否出现乏力、干咳、呼吸困难等症状？:")})

#其他情况
data.update({"qtqk":AskText("其他情况:")})



with open("data.json","w") as fd:
    json.dump(data,fd)
    print("保存成功")
