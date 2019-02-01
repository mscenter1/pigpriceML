# 用作制作月份分类变量
MonthList = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

# 模型设置
# 第一时间段
# 使用过去3、4个月的历史数据作为自变量
premonthlist1 = [3, 4]
# 预测未来1-3个月的价格
predictmonthinter1 = [1, 3]
# 第二时间段
# 使用过去6、7个月的历史数据作为自变量
premonthlist2 = [6, 7]
# 预测未来4-6个月的价格
predictmonthinter2 = [4, 6]

# 输入数据的列名
ModelList = ['date', 'waisan', 'neisan', 'tuza', 'bean', 'corn']
# 使用两个模型：生猪价格+玉米价格
ModelNum = 2
# 生猪预测模型自变量和因变量
IndependentV_Model1 = ['waisan', 'neisan', 'tuza', 'bean', 'corn']
dependentV_Model1 = ['waisan', 'neisan', 'tuza']
# 玉米预测模型自变量和因变量
IndependentV_Model2 = ['corn']
dependentV_Model2 = ['corn']

class ml_prepare:
    def __init__(self): 
        pass
    
    # 生成月份变量
    def MonthListPrepare(self):
        string1 = 'mnth_'
        MonthList0 = [string1 + x for x in MonthList]
        return MonthList0
    
    # 返回模型设置
    # MonthList0：月份变量
    # premonthlist：自变量月份
    # predictmonthinter：预测间隔
    # max_length： 自变量数目
    # ModelNum：模型总数（玉米+生猪）
    def ml_return(self, period):
        string1 = 'mnth_'
        MonthList0 = [string1 + x for x in MonthList]
        if(period == 1):
            max_length = max(premonthlist1)
            premonthlist = premonthlist1
            predictmonthinter = predictmonthinter1
        else:
            max_length = max(premonthlist2)
            premonthlist = premonthlist2
            predictmonthinter = predictmonthinter2
        return MonthList0, premonthlist, predictmonthinter, max_length, ModelNum

    # 返回模型自变量
    def variable_return(self, model):
        if (model == 1):
            IndependentV = IndependentV_Model1
            dependentV = dependentV_Model1
        elif (model == 2):
            IndependentV = IndependentV_Model2
            dependentV = dependentV_Model2
        return IndependentV, dependentV