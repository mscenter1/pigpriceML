# -*- coding: utf-8 -*-
# 系统模块
import sys

# 数据处理模块
import pandas as pd

# 引入外部模块
# 预测模型
from predict_lead import Predict_Lead as PRD

class Total_Data:
    def __init__(self): 
        pass

    # 获取未来6个月的预测结果并返回
    def Total_data_return(self, type):
        # 计算预测结果
        Predict_Proc = PRD()
        # Predict_result即为预测结果
        Predict_result, Last_Data, y_test_compare1, y_test_compare2 = Predict_Proc.predict_result()
        Data1 = Predict_result[(Predict_result.Price_ID == type)].reset_index(drop = True)
        Data1 = Data1.drop(['Price_ID'], axis = 1)
        order = ['Date_Time', 'Value']
        Data1 = Data1[order] 
        return Data1, Last_Data

    # 获取模型训练中预测结果与对应实际价格数据集
    def Predict_Performance(self, type):
        # 计算预测结果
        Predict_Proc = PRD()
        Predict_result, Last_Data, y_test_compare1, y_test_compare2 = Predict_Proc.predict_result()
        if(type == 'corn'):
            Data1 = y_test_compare2[(y_test_compare2.Price_ID == type)].reset_index(drop = True)
        else:
            Data1 = y_test_compare1[(y_test_compare1.Price_ID == type)].reset_index(drop = True)
            
        Data1 = Data1.drop(['Price_ID'], axis = 1)
        order = ['real', 'predict']
        Data1 = Data1[order] 
        return Data1

    # 返回指定日期的预测结果
    def Specific_day(self, type, spc_date):
        # 计算预测结果
        spc_date = spc_date.strftime('%Y-%m-%d')
        Predict_Proc = PRD()
        Predict_result, Last_Data, y_test_compare1, y_test_compare2 = Predict_Proc.predict_result()
        Data1 = Predict_result[(Predict_result.Date_Time == spc_date)&(Predict_result.Price_ID == type)].reset_index(drop = True)
        Data1 = Data1.drop(['Date_Time', 'Price_ID'],axis=1)
        return Data1
        

if __name__ == '__main__':
    Predict_Proc = PRD()
    Total_result = pd.DataFrame()
    Predict_result, Last_Data, y_test_compare1, y_test_compare2 = Predict_Proc.predict_result()