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
import numpy as np
import pandas as pd

# 引入外部模块
# 机器学习模型设置
import model_setting as MD_S

class Predict_Prepare:
    def __init__(self): 
        pass
    
    # 调用主函数
    def variables_prepar(self, period): 
        # 读取样本数据
        path1 = os.path.dirname(sys.path[0])
        path0 = path1 + '\\web_Project\\sampledata.csv'
        path_df = open(path0)
        Origin_data = pd.read_csv(path_df)

        # 获得ML模型预测范围设置
        ML_var = MD_S.ml_prepare()
        Monthlist, premonthlist, predictmonthinter, max_length, modelnum = ML_var.ml_return(period)

        # 调用整理函数
        # 生猪价格数据整理
        # 生成训练集
        Pig_Data_m1 = self.Train_Data_Gen(Origin_data, premonthlist, max_length,1)
        # 生成预测集
        Lastdate_Pig, Predict_Pig = self.Predict_Data_Gen(Origin_data, premonthlist, max_length, predictmonthinter, 1)
        
        # 玉米价格数据整理
        Corn_Data_m2 = self.Train_Data_Gen(Origin_data, premonthlist, max_length,2)
        Lastdate_Corn, Predict_Corn = self.Predict_Data_Gen(Origin_data, premonthlist, max_length, predictmonthinter, 2)

        return Pig_Data_m1, Predict_Pig, Lastdate_Pig, Corn_Data_m2, Predict_Corn, Lastdate_Corn

    # 生成训练集
    def Train_Data_Gen(self, Total_Data, premonthlist, max_length, modelnum):

        # 获得ML模型变量设置
        ML_var = MD_S.ml_prepare()
        IndependentV, dependentV = ML_var.variable_return(modelnum)

        # 填补缺省值
        Total_length = len(Total_Data)
        Total_Data = Total_Data.fillna(0)
        Total_Data = Total_Data.reset_index(drop = True) 
        # 将日期转化为分类变量
        Total_Data['date'] = pd.to_datetime(Total_Data['date'])
        Total_Data['mnth'] = Total_Data['date'].apply(lambda x: x.strftime('%B')) 
        
        # 选取因变量
        list1 = copy.deepcopy(dependentV)
        list1.append('mnth')
        Pre_Data = Total_Data.loc[31 * max_length : Total_length - 1, list1]
        Pre_Data = Pre_Data.reset_index(drop = True)

        # 生成自变量
        for premonth in premonthlist:
            start = 31 * (max_length - premonth)
            end = Total_length - 31 * premonth - 1
            for item in IndependentV:
                X0 = Total_Data.loc[start : end, [item]]
                X0 = X0.reset_index(drop = True) 
                Pre_Data[str(item) + '_' + str(premonth)] = X0.loc[:, [item]]
        Pre_Data = Pre_Data.reset_index(drop = True)
        return Pre_Data

    # 生成预测集
    def Predict_Data_Gen(self, Total_Data, premonthlist, max_length, predictmonthinter, modelnum):
        # 获得ML模型变量设置
        ML_var = MD_S.ml_prepare()
        IndependentV, dependentV = ML_var.variable_return(modelnum)

        # 填补缺省值
        Total_length = len(Total_Data)
        Total_Data = Total_Data.fillna(0)
        Total_Data = Total_Data.reset_index(drop = True)

        # 获得已有数据集的最后一天
        lastdate = Total_Data.loc[(Total_length - 1) : (Total_length - 1), ['date']].values[0][0]

        # 已有数据集最后一天到预测目标的第一天的间隔
        start_pre = Total_length + 31 * (predictmonthinter[0] - 1)
        # 已有数据集最后一天到预测目标的最后一天的间隔
        end_pre = Total_length + 31 * (predictmonthinter[1])
        Model_data = pd.DataFrame()

        # 生成预测数据集的时间序列及月份变量:
        lastdate = datetime.datetime.strptime(lastdate, '%Y/%m/%d')
        datestart = lastdate + datetime.timedelta(days = 31 * (predictmonthinter[0] - 1))
        dateend = lastdate + datetime.timedelta(days = 31 * (predictmonthinter[1]))
        data = []
        date1 = datestart
        while datestart < dateend:
            datestart += datetime.timedelta(days = 1)
            data.append(datestart)
        Model_data['date'] = data
        Model_data['date'] = pd.to_datetime(Model_data['date'])
        Model_data['mnth'] = Model_data['date'].apply(lambda x: x.strftime('%B')) 
        Model_data = Model_data.drop(['date'], axis = 1)
        Model_data = Model_data.reset_index(drop = True)

        # 生成预测时间集的自变量
        for premonth in premonthlist:
            start = start_pre - 31 * premonth
            end = end_pre - 31 * premonth - 1
            for item in IndependentV:
                X1 = Total_Data.loc[start : end, [item]]
                X1 = X1.reset_index(drop = True) 
                Model_data[str(item) + '_' + str(premonth)] = X1.loc[:, [item]]
        Model_data = Model_data.reset_index(drop = True)
        return date1, Model_data
