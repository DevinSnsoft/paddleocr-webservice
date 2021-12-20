#!/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
from suds.client import Client  # 导入suds.client 模块下的Client类

wsdl_url = "http://210.30.0.92:8000/?wsdl"


def photo2unicode(url, imgstr):
    client = Client(url)  # 创建一个webservice接口对象
    print(client)
    client.service.photo2unicode(imgstr)  # 调用这个接口下的photo2unicode方法，并传入参数
    req = str(client.last_sent())  # 保存请求报文，因为返回的是一个实例，所以要转换成str
    response = str(client.last_received())  # 保存返回报文，返回的也是一个实例
    print(req)  # 打印请求报文
    print(response)  # 打印返回报文


def findunicode(url, zistr):
    client = Client(url)  # 创建一个webservice接口对象
    print(client)
    client.service.findunicode(zistr)  # 调用这个接口下的findunicode方法，并传入参数
    req = str(client.last_sent())  # 保存请求报文，因为返回的是一个实例，所以要转换成str
    response = str(client.last_received())  # 保存返回报文，返回的也是一个实例
    print(req)  # 打印请求报文
    print(response)  # 打印返回报文


if __name__ == '__main__':
    with open("/home/tesla4/wjj/PaddleOCR-release-2.3/result/0x4e0a.png", 'rb') as f:
        imgstr = base64.b64encode(f.read())
    photo2unicode(wsdl_url, str(imgstr, encoding="utf-8"))

#    zistr = "乌"
#    findunicode(wsdl_url, zistr)
