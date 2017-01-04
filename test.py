# -*- coding: UTF-8 -*-
import urllib, urllib2, sys

"""
host = 'http://ali-mobile.showapi.com'
path = '/6-1'
method = 'GET'
appcode = '08f4bf1b1c4a42a69188cf88f0735998'
querys = 'num=18618328507'
bodys = {}
url = host + path + '?' + querys
"""
host = 'http://sms.market.alicloudapi.com'
path = '/singleSendSms'
method = 'GET'
appcode = '08f4bf1b1c4a42a69188cf88f0735998'
querys = 'ParamString={"name":"杰哥","from":"韩飞","something":"女朋友"}&RecNum=18665385920&SignName=韩飞&TemplateCode=SMS_36135018'
bodys = {}
url = host + path + '?' + querys

request = urllib2.Request(url)
request.add_header('Authorization', 'APPCODE ' + appcode)
response = urllib2.urlopen(request)
content = response.read()
if (content):
    print(content)