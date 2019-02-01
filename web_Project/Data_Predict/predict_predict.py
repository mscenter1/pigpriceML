# -*- coding: utf-8 -*-
# 系统模块
import sys

# 获取文件目录模块
import os

# 复制Dataframe模块
import copy

# 时间处理模块
import datetime

# 数据处理模块
import pandas as pd
import numpy as np

# 机器学习模块
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib

# 引入外部模块
# 机器学习模型设置
import model_setting as MD_S

class Predict_Predict:
    def __init__(self): 
        pass

    # 调用主函数
    # History_Model1：用作第一个模型训练的数据
    # Predict_Model1：需要用第一个模型进行预测的数据
    # Last_data_model1：需要用第一个模型进行预测的数据集的最后一天
    # period：当前模型正处于的时间段
    def predict_result(self, History_Model1, Last_data_model1, Predict_Model1, History_Model2, Last_data_model2, Predict_Model2, period):
        
        # 获得ML模型预测范围设置
        # premonthlist：模型中包含的历史自变量的月份
        # predictmonthinter：需要使用模型进行预测的未来月份区间
        ML_var = MD_S.ml_prepare()
        Monthlist, premonthlist, predictmonthinter, max_length, modelnum = ML_var.ml_return(period)

        # 预测生猪价格
        predict_data_model1, y_test_compare1= self.predict_price(History_Model1, Predict_Model1, Last_data_model1, Monthlist, 1, predictmonthinter, premonthlist, period)

        # 预测玉米价格
        predict_data_model2, y_test_compare2= self.predict_price(History_Model2, Predict_Model2, Last_data_model2, Monthlist, 2, predictmonthinter, premonthlist, period)

        # 整合预测数据
        predict_result = pd.concat([predict_data_model1, predict_data_model2], axis = 0)
        return predict_result, y_test_compare1, y_test_compare2
    

    def predict_price(self, Total_data, Predict_data, lastdate, Monthlist, modelnum, predictmonthinter, premonthlist, period):

        # 获得ML模型变量设置
        ML_var = MD_S.ml_prepare()
        IndependentV, dependentV = ML_var.variable_return(modelnum)
        itemlist = dependentV
        
        # 添加季节因子
        Total_data = self.add_seasonal(Total_data, Monthlist)
        Predict_data = self.add_seasonal(Predict_data, Monthlist)
        
        Predict_result = pd.DataFrame()
        y_test_compare = pd.DataFrame()

        # 预测计算
        for item in itemlist:
            Predict_result, y_test_compare0 = self.model_predict(Total_data, Predict_data, Predict_result, item, itemlist, lastdate, predictmonthinter, premonthlist, period)

            y_test_compare0['Price_ID'] = item
            y_test_compare = pd.concat([y_test_compare, y_test_compare0],axis=0)
        
        return Predict_result, y_test_compare

    def model_predict(self, Total_data, Predict_data, Predict_result, item, itemlist, lastdate, predictmonthinter, premonthlist, period):
        # 删除不需要的自变量
        list1 = []
        for premonth in premonthlist:
            for item1 in itemlist:
                if(item1 != item):
                    X1 = str(item1)+'_'+str(premonth)
                    list1.append(X1)  

        Total_data = Total_data.drop(list1, axis = 1)
        Predict_data = Predict_data.drop(list1, axis = 1)

        # 获取模型训练表现与真实价格
        # 拆分模型训练集与测试集
        Trained_data, test_set = train_test_split(Total_data, train_size = 0.80, test_size = 0.20)
        # 获取训练集的因变量
        y_train = Trained_data[item].values
        # 获取训练集的自变量
        independent_V = Trained_data.drop(itemlist, axis = 1)
        x_train=independent_V.values
        # 获取预测集的因变量
        y_test=test_set[item].values
        # 获取预测集的自变量
        independent_V = test_set.drop(itemlist, axis = 1)
        x_test=independent_V.values

        # 获取模型训练结果
        y_test_compare = self.LR_model_train(x_train, y_train, x_test, y_test, item, period)

        # 实际预测时，训练模型所需的因变量
        y_train = Total_data[item].values
        # 实际预测时，训练模型所需的自变量
        Pre1 = copy.deepcopy(Total_data)
        independent_V = Pre1.drop(itemlist, axis = 1)
        x_train = independent_V.values
        # 预测模型所需的自变量
        x_predict = Predict_data.values

        # 获取模型预测结果
        y_predict_LR = self.LR_model_predict(x_train, y_train, x_predict, item, period)

        # 为预测结果匹配对应日期
        predict_result = self.select_predict_result(lastdate, y_predict_LR, predictmonthinter)
        predict_result.rename(columns = {"predict": "Value"}, inplace = True)
        predict_result['Price_ID'] = item
        Predict_result = pd.concat([Predict_result, predict_result], axis = 0)

        return Predict_result, y_test_compare

    def LR_model_predict(self, x_train, y_train, x_predict, item, period):
        # 可调用已存在模型
        #name = item + '_Model_' + str(period) + '.m'
        #path = os.path.dirname(sys.path[0]) + "\\" + name
        #reg = joblib.load(path)

        # 使用贝叶斯线性回归模型
        reg = linear_model.BayesianRidge()
        reg.fit(x_train, y_train)
        # 模型预测
        y_predict0 = reg.predict(x_predict)
        y_predict = pd.DataFrame()
        y_predict['predict'] = y_predict0
        y_predict = y_predict.reset_index(drop = True)

        # 保存模型
        #joblib.dump(reg, name)  
        return y_predict

    def LR_model_train(self, x_train, y_train, x_test, y_test, item, period):
        # 可调用已存在模型
        #name = item + '_Model_' + str(period) + '.m'
        #path = os.path.dirname(sys.path[0]) + "\\" + name
        #reg = joblib.load(path)
        
        # 使用贝叶斯线性回归模型
        reg = linear_model.BayesianRidge()
        reg.fit(x_train, y_train)
        # 模型预测
        y_test0 = reg.predict(x_test)
        y_test_compare = pd.DataFrame()
        y_test_compare['real'] = y_test
        y_test_compare['predict'] = y_test0
        # 保存模型
        #joblib.dump(reg, name)  

        # 输出Python内预测结果与真实数据的对比图
        #self.Result_show('Bayesian Linear Regression', y_test_compare)
        return y_test_compare

    # 拆分类别变量至多个0-1变量
    def add_seasonal(self, Total_data, Monthlist):
        Total_data = pd.get_dummies(Total_data)
        replement_list = [0] * len(Total_data)
        column_title = Total_data.columns.tolist()
        column_title = [x for x in column_title if 'mnth_' in x]  
        Reple = [i for i in Monthlist if i not in column_title]
        for title in Reple:
            Total_data[title] = replement_list
        return Total_data

    # 为预测结果添加对应日期
    def select_predict_result(self, lastdate, y_predict, predictmonthinter):
        datelist=[]
        startdate = lastdate + datetime.timedelta(days = 1)
        enddate = lastdate + datetime.timedelta(days = len(y_predict))
        while startdate <= enddate:
            datelist.append(startdate.strftime('%Y-%m-%d'))
            startdate += datetime.timedelta(days =+ 1)
        y_predict['Date_Time'] = datelist
        return y_predict

    