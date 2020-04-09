# -*- coding: utf-8 -*-
# @Time    : 2020/3/6 16:12
# @Author  : kevin shu
# @FileName: baidu_map_distance.py
# @Software: PyCharm
import requests
import json
import tkinter as tk
from tkinter import filedialog
import os
import pandas as pd



#获取地理编码
def getPosition(myaddress):
    '''返回经纬度信息'''
    url = r"http://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak={}".format(myaddress, myAK)
    res = requests.get(url)
    json_data = json.loads(res.text)

    if json_data['status'] == 0:
        lat = json_data['result']['location']['lat']  # 纬度
        lng = json_data['result']['location']['lng']  # 经度
    #如果请求不成功的话就输出报错提示
    else:
        print("Error output!")
        return json_data['status']
    return lat, lng

#获取两地距离，这里我们获取的是步行距离，其他距离参考官方文档
def getdistance(startlat,startlng,endlat,endlng):
    #{: .6f}保留小数点后六位
    distanceurl=r"http://api.map.baidu.com/directionlite/v1/walking?origin={:.6f},{:.6f}&destination={:.6f},{:.6f}&ak={}".format(startlat,startlng,endlat,endlng,myAK)
    res = requests.get(distanceurl)
    dis_json_data = json.loads(res.text)
    if dis_json_data['status'] == 0:
        #注意这里的返回的数据结构
        distance=dis_json_data['result']['routes'][0]['distance']
        return(distance)

#获取文件路径
def get_filename():
    root = tk.Tk()
    root.withdraw()
    #file_path为文件的路径，parent_path为文件所在的文件夹路径
    file_path = filedialog.askopenfilename()
    parent_path = os.path.dirname(file_path)
    return file_path, parent_path

def get_address(file_path):
    data=pd.read_excel(file_path)
    startaddress=data['地区']+data['出发行政区域']+data['出发地址']
    endaddress=data['地区']+data['到达行政区域']+data['到达地址']
    distance=[]
    #遍历series输入需要查询的起始地点
    for i in range(1,len(startaddress)+1):
        startlat, startlng = getPosition(startaddress[i-1])
        endlat, endlng = getPosition(endaddress[i-1])
        #将输出结果拼接为list
        distance.append(getdistance(startlat, startlng, endlat, endlng))
    dfdistance=pd.DataFrame(distance)
    #使用concat拼接两个dataframe，其中axis=1表示横向拼接，如果不加此参数或者为0表示纵向拼接
    result=pd.concat([data,dfdistance],axis=1)
    #更改列名称
    result.rename(columns={0: 'distance'}, inplace=True)
    result.to_excel(parent_path + '/结果文件.xlsx',index=None)


if __name__=='__main__':
    myAK = '你的AK'
    file_path, parent_path=get_filename()
    get_address(file_path)
    print('已完成，请查看结果文件')
