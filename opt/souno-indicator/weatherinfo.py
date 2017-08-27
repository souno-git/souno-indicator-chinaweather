#!/usr/bin/env python3
# coding:utf-8

import json
import urllib
import urllib.request
import urllib.parse
import sys
import re
import zlib
import citynum


json_str = json.dumps(citynum.CITYNUM)
city_data = json.loads(json_str)


def get_wea():
    city_info = urllib.request.urlopen('http://ip.ws.126.net/ipquery').read().decode('gbk')
    #print(city_info)
    json_str_city = json.dumps(city_info)
    city_data_str = json.loads(json_str_city)
    shi_pattern = 'lc="(.+?)";'
    shi = re.findall(shi_pattern, city_data_str)
    print(shi[0])
    if not shi:
        wea_city = "101010100"
    elif shi[len(shi)-1][len(shi[len(shi)-1])-1] =="区":
        shi_pattern = '(.+?)地区'
        cache_shi = re.findall(shi_pattern, shi[0])
        if not shi[0]:
            shi_pattern = '(.+?)区'
            cache_shi = re.findall(shi_pattern, shi[0])
        shi = cache_shi
        wea_city = city_data[shi[0]]
    elif shi[len(shi)-1][len(shi[len(shi)-1])-1] =="县":
        shi_pattern = '(.+?)县'
        shi = re.findall(shi_pattern, shi[0])
        wea_city = city_data[shi[0]]
    else:
        shi_pattern = '(.+?)市'
        shi = re.findall(shi_pattern, shi[0])
        wea_city = city_data[shi[0]]

    print(shi[0])
    print(wea_city)
    url = 'http://wthrcdn.etouch.cn/weather_mini?citykey=%s'%(wea_city)
    print(url)
    wea_info = urllib.request.urlopen(url).read()
    wea_info = zlib.decompress(wea_info,16+zlib.MAX_WBITS)
    wea_info = wea_info.decode("utf8")
    json_wea = json.dumps(wea_info)
    wea_city= json.loads(json_wea)
    wea_city = eval(wea_city)
    print(wea_city)
    wea_data = '{"weatherinfo":{"city":"' + wea_city['data']['city'] + '","ganmao":"' + wea_city['data']['ganmao'] + '","fengli":"' + wea_city['data']['forecast'][0]['fengli'][10:12] + '","fengxiang":"' + wea_city['data']['forecast'][0]['fengxiang'] + '","weather":"' + wea_city['data']['forecast'][0]['type'] + '","temp1":"' + wea_city['data']['forecast'][0]['low'][3:] + '","temp2":"'+wea_city['data']['forecast'][0]['high'][3:]+'","ptime":"16:00","ntemp":"' + wea_city['data']['wendu'] + '℃"}}'
    print(wea_data)
    return (wea_data)


