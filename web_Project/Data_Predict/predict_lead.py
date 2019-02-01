# -*- coding: utf-8 -*-
# 系统模块
import sys

# 数据处理模块
import pandas as pd

# 引入外部模块
# 整理数据
from predict_prepare import Predict_Prepare as Prepare
# 获取价格预测结果
from predict_predict import Predict_Predict as Predict

class Predict_Lead:
    def __init__(self): 
        pass

    # 其他包调用的函数
    def predict_result(self):
        # 模型分两段进行预测
        period = [1, 2]

        # 实例化准备模块和模型预测模块
        PrePare_Data = Prepare()
        Predict_Data = Predict()

        # 获得第一段时间的预测结果
        # 整理样本数据集，进行模型预测准备工作
        # History_Model11、Predict_Model11：生猪预测模型所需使用的自变量和因变量
        # Last_data_model11：原始数据集中生猪价格的最后一条记录的时间
        # History_Model21、Predict_Model21：玉米预测模型所需使用的自变量和因变量
        # Last_data_model21：原始数据集中玉米价格的最后一条记录的时间
        History_Model11, Predict_Model11, Last_data_model11, History_Model21, Predict_Model21, Last_data_model21 = PrePare_Data.variables_prepar(period[0])
        
        # 获取预测结果
        # predict_result1：生猪价格和玉米价格的预测结果
        # y_test_compare11：第一时间段中生猪模型训练结果和实际价格的集合
        # y_test_compare12：第一时间段中玉米模型训练结果和实际价格的集合
        predict_result1, y_test_compare11, y_test_compare12 = Predict_Data.predict_result(History_Model11, Last_data_model11, Predict_Model11, History_Model21, Last_data_model21, Predict_Model21, period[0])

        # 获得第二段时间的预测结果
        # 整理样本数据集，进行模型预测准备工作
        History_Model12, Predict_Model12, Last_data_model12, History_Model22, Predict_Model22, Last_data_model22 = PrePare_Data.variables_prepar(period[1])
        
        # 获取预测结果
        predict_result2, y_test_compare21, y_test_compare22 = Predict_Data.predict_result(History_Model12, Last_data_model12, Predict_Model12, History_Model22, Last_data_model22, Predict_Model22, period[1])
        
        # 整合两端时间的预测结果
        predict_result = pd.concat([predict_result1, predict_result2])
        predict_result = predict_result.reset_index(drop=True)

        return predict_result, Last_data_model11, y_test_compare11, y_test_compare12


    