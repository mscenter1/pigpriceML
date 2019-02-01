# -*- coding: utf-8 -*-
# 系统模块
import sys

# 获取文件目录模块
import os

# 时间处理模块
import datetime

# 数据处理模块
import pandas as pd
import numpy as np

# 日志记录模块
import logging

# web API所需使用的模块
from flask import Flask
from flask_cors import CORS, cross_origin
from gevent.pywsgi import WSGIServer

# 引入模型预测模块
path = os.path.dirname(sys.path[0])
path0 = path + '\\web_Project\\Data_Predict'
sys.path.append(path0)
from Predict_ML import Total_Data as TD

# 实例化
app = Flask(__name__)
CORS(app, resources={r"/*": {"origisns": "*"}})

# 封装日志记录函数
def setLogger():  
    logger = logging.getLogger('MyLogger')  
    logger.setLevel(logging.DEBUG)  

    # 创建一个handler，用于写入日志文件  
    fh = logging.FileHandler(os.path.join(os.path.dirname(__file__), 'app.txt'))  
    fh.setLevel(logging.INFO)  

    # 定义handler的输出格式  
    formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')  
    fh.setFormatter(formatter)  

    # 给logger添加handler  
    logger.addHandler(fh)
    return logger  

# 将数据结果转为js能接受的string形式
def change_type(Dataframe):
    Sentance = ''
    length = len(Dataframe)
    for i in range(length):
        Single_record = Dataframe.loc[i:i,].values[0]
        Sentance = Sentance+ '  '.join(str(n) for n in Single_record)
        Sentance = Sentance + '\n'
    return Sentance

# 选取未来6个日期
def datelist_future(input_date):
    lastday = input_date.day
    lastmonth = input_date.month
    lastyear = input_date.year
    datelist = []
    for i in range(1,7):
        # 当前日期是28日之前，未来的日期选取未来6个月对应天的预测值
        if(lastday <= 28):
            newday = lastday
            newmonth = lastmonth + i
            # 判断是否跨年
            if(newmonth > 12):
                newmonth = newmonth-12
                newyear = lastyear+1
            else:
                newyear = lastyear
        # 当前日期是29或30，针对闰年判断是否为28或29
        elif(lastday >= 29):
            newmonth = lastmonth + i
            # 判断是否跨年
            if(newmonth > 12):
                newmonth = newmonth - 12
                newyear = lastyear + 1
            else:
                newyear = lastyear
            # 判断是否为闰年
            if(newmonth == 2):
                if((newyear % 4 == 0 and newyear % 100 != 0) or newyear % 400 == 0):
                    newday = 29
                else:
                    newday = 28
            else:
                newday = lastday
        # 当前日期是31日，需判断是否为闰年、未来的6个月是否有31日，没有的话选取30日的
        else:
            newmonth = lastmonth + i
            if(newmonth>12):
                newmonth = newmonth-12
                newyear = lastyear+1
            else:
                newyear = lastyear
            # 判断是否为闰年
            if(newmonth == 2):
                if((newyear % 4 == 0 and newyear % 100 != 0) or newyear % 400 == 0):
                    newday = 29
                else:
                    newday = 28
            # 判断是否有31日
            elif(newmonth in [4, 6, 9, 11]):
                newday = 30
            else:
                newday = lastday
        newdate = datetime.date(newyear, newmonth, newday)
        newdate = newdate.strftime('%Y-%m-%d')
        datelist.append(newdate)
    return datelist

# 实例化日志读写函数
logger = setLogger()

# API1: PredictRes
# 返回未来6个月预测数据
# 输入省份+预测价格种类：waisan、neisan、tuza、corn
# 输出：6个日期+预测数据
@app.route('/PredictRes/<string:item>')
def PredictRes(item):
    try:
        Total_date = TD()
        Data0, Last_Data = Total_date.Total_data_return(item)
        datelist = datelist_future(Last_Data)
        Data1 = Data0[Data0.Date_Time.isin(datelist)]
        Data1 = Data1.reset_index(drop = True) 
        if(len(Data1) == 0):
            Sentance = 'No Data'
        else:
            if(item == 'corn'):
                Data1['Value'] = Data1['Value'] / 1000
            Sentance = change_type(Data1)
    except:
        logger.exception('PredictRes')
    return Sentance

# API2: PredictDay
# 返回未来某天的预测数据
# 输入省份+预测价格种类：waisan、neisan、tuza、corn
# 输出：1个预测数据
@app.route('/PredictDay/<string:item>/<int:year>/<int:month>/<int:day>')
def PredictDay(item, year, month, day):
    try:
        spc_date = datetime.date(year, month, day)
        Total_date = TD()
        Data1 = Total_date.Specific_day(item, spc_date)
        
        if(len(Data1) == 0):
            Sentance = 'No Data'
        else:
            if(item == 'corn'):
                Data1['Value'] = Data1['Value'] / 1000
            Sentance = str(Data1.values[0][0])
    except:
        logger.exception('PredictDay')
    
    return Sentance

# API3: Performance
# 返回训练集的表现
# 输入省份+预测价格种类：waisan、neisan、tuza、corn
# 输出：多个数据对
@app.route('/Performance/<string:item>')
def Performance(item):
    try:
        Total_date = TD()
        Data1 = Total_date.Predict_Performance(item)
        
        if(len(Data1) == 0):
            Sentance='No Data'
        else:
            if(item == 'corn'):
                Data1['real'] = Data1['real'] / 1000
                Data1['predict'] = Data1['predict'] / 1000
            Sentance = change_type(Data1)
    except:
        logger.exception('Performance')
    
    return Sentance

if __name__ == '__main__':
    #app.run()
    http_server = WSGIServer(('', 8000), app)
    http_server.serve_forever()
    app