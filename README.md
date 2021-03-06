# 商品猪价格预测系统

## 目录

- [概述](#概述)
- [使用技术](#使用技术)
- [预测模型](#预测模型)
  - [预测目标](#预测目标)
  - [模型变量](#模型变量)
    - [生猪价格预测模型](#生猪价格预测模型)
    - [玉米价格预测模型](#玉米价格预测模型)
    - [原始数据集样式](#原始数据集样式)
  - [模型预测效果](#模型预测效果)
    - [生猪价格预测模型](#生猪价格预测模型-1)
    - [玉米价格预测模型](#玉米价格预测模型-1)
  - [模型建立过程](#模型建立过程)
- [结果展示](#结果展示)
- [安装说明](#安装说明)
- [程序结构说明](#程序结构说明)
- [使用说明](#使用说明)

## 概述

本系统是针对商品猪养殖行业搭建的价格预测系统，能够根据已有数据，通过贝叶斯线性回归模型，预测未来六个月内的生猪价格和饲料价格，为商品猪养殖、销售行业的决策提供参考。

## 使用技术

1. Python编程技术：实现机器学习模型，用于预测两种价格数据；
2. JavaScript与html编程技术：实现前端展示页面。

## 预测模型

机器学习是当下进行数据分析、研究的主流方法之一。机器学习算法可从已有数据中自动分析、推断出数据中存在的规律，并将归纳得出的规律用于未知数据的分类或预测。在针对问题合理选择模型的情况下，具有很高的精确度，也因此，机器学习被广泛应用于多个领域，如数据挖掘、人脸识别、医学诊断等。

本系统使用的预测模型即为机器学习模型中的**贝叶斯线性回归模型**。该算法可根据样本数据集训练模型，获取待预测指标与相关因素之间的关系，并根据该关系进行预测。受到模型本身原理的影响，该模型将问题中的不确定性也纳入考虑，一方面，描述了实际生活中的待预测数据的不确定性，另一方面，对于数据记录较少的情况，能够自行排除受到极端条件影响的数据，更加精准进行数据的预测。贝叶斯线性回归模型作为常用机器学习模型的一种，也具有广泛的应用领域，如市场销售、期货交易等，并格外**适合历史数据集规模较小**的情况。

本系统旨在根据已有的过去一年中的每日价格数据，输出未来六个月的选定预测目标的预测值。考虑到数据记录量较少，及应用不同模型进行预测实验的结果，最终决定将贝叶斯线性回归模型应用于商品猪养殖业中，为养殖者在养殖过程中提供决策指导，同时也提供将机器学习模型应用于养殖业的思路。

在使用本系统进行价格预测时，需要提供预测时间前6个月至1年的数据作为训练数据，供模型进行参数训练及预测。在当前模型中，提供了样本数据（见sampledata.csv)。

### 预测目标

在商品猪养殖过程中，生猪价格和饲料成本对于养殖者进行养殖决策具有重要的影响。生猪价格直接关系到养殖收入，而饲料成本在养殖成本中占比达到60%~70%。因此，本系统将**生猪价格**、**饲料价格**作为预测目标。

考虑到商品猪具有外三元、内三元、土杂猪三种类别的区别，类别之间存在显著价格差异，因此在预测生猪收购价格时，本系统分别针对这三种类别搭建模型，获得预测数据。对于饲料成本，相关资料显示，在饲料成分中，有60%以上均为玉米，玉米价格变化对于饲料价格的影响最大，因此使用玉米价格作为饲料价格的代表，进行模型预测。

### 模型变量

针对生猪价格预测和玉米价格预测，本系统建立了两个不同的模型，以获得更加精准的预测效果。

#### 生猪价格预测模型

考虑到生猪价格由整个养殖过程中的成本决定，因此在预测时，将历史的生猪价格、玉米价格和豆粕价格纳入模型的输入参数。

当进行未来第一个月至第三个月的价格预测时，模型将预测时间点前第三个月和第四个月的生猪价格、玉米价格和豆粕价格作为自变量，即当预测`2019-05-01`的生猪价格时，模型会根据`2019-01-01`和`2019-02-01`的历史数据作为输入数据。而当进行未来第四个月至第七个月的生猪价格预测时，模型则将预测时间点前第六个月和第七个月的生猪价格、玉米价格和豆粕价格作为自变量，进行价格预测.

#### 玉米价格预测模型

玉米是重要的粮食作物和饲料作物，用途十分广泛，影响其价格的因素也种类繁多，因此在预测时，仅将历史的玉米价格纳入影响未来玉米价格的考虑因素。

当进行未来第一个月至第三个月的价格预测时，模型将预测时间过去第三个月和第四个月的玉米价格作为自变量。而当进行未来第四个月至第七个月的价格预测时，模型则将预测时间过去第六个月和第七个月的玉米价格作为自变量，进行价格预测。

#### 原始数据集样式

本系统可根据过去的历史数据，自动生成模型使用的自变量序列。在使用本系统时，将目录中的sampledata.csv替换为希望使用的原始数据集，并按下表样式存储数据：

| 数据列名称 | 数据含义 | 数据格式|
| :-: | :-: | :-: |
| date | 日期 | 2019/01/01 |
| waisan | 外三元生猪价格 | 13.54 |
| neisan | 内三元生猪价格 | 12.46 |
| tuza | 土杂猪生猪价格 | 10.43 |
| corn | 玉米价格 | 1.87 |
| bean | 豆粕价格 | 2.35 |

下图为当前目录中[sampledata.csv](/web_Project/sampledata.csv)文件样例内容：

![sampledata](/image/sampledata.png)

### 模型预测效果

#### 生猪价格预测模型

当随机选择80%的数据点训练模型时，使用剩余20%的数据点用作模型的预测结果与实际价格的对比，以测试模型预测信度与效度。模型预测结果和实际价格对比图如下图所示，其中橙色曲线为实际价格，蓝色曲线为预测价格。

由对比图可以看出，模型的预测结果与实际价格大致相同，最大的价格偏差为实际价格平均值的3%，平均价格偏差为1%，表明该模型具有较高的预测准确度。

![dis_LR_pig](/image/Dis_LR_pig.png )

同时，考察对于一段连续时间内模型的预测效果，即选取一段连续时间用作预测结果与实际价格对比试验，剩余数据用作模型训练集。预测结果如下图所示，橙色曲线为实际价格，蓝色曲线为预测结果。

对比结果显示，模型的预测结果能够反映出实际价格的大体变化趋势，但是对于短期内的价格突变，无法进行准确的反映。

![con_LR_pig](/image/Con_LR_pig1.png )

建立好模型后，我们持续运行模型多天，记录了模型的预测效果，并与实际价格进行比对，结果如下图所示，其中橙色曲线表示实际生猪价格，蓝色曲线表示预测结果。

由对比图可看出，该模型预测的结果与真实数据趋势相近，但是无法预测短期内小幅度的价格波动。

![con_LR_pig](/image/Con_LR_pig.png )

#### 玉米价格预测模型

和生猪价格预测模型相同，首先当随机选择80%的数据点训练模型时，使用剩余20%的数据点用作模型的预测结果与实际价格的对比，以测试模型预测信度与效度。模型预测结果和实际价格对比图如下图所示，其中橙色曲线为实际价格，蓝色曲线为预测价格。

由对比图可以看出，模型的预测结果与实际价格大致相同，最大的价格偏差为实际价格平均值的3%，平均价格偏差为1%，表明该模型能够根据自变量，较精准的预测出对应的玉米价格。

![dis_LR_cor](/image/Dis_LR_cor.png )

对于玉米价格预测模型，考察对于一段连续时间内玉米价格的预测结果，即选取一段连续时间用作预测结果与实际价格对比试验，剩余数据用作模型训练集。预测结果如下图所示，橙色曲线为实际价格，蓝色曲线为预测结果。

对比结果显示，在预测时间段中，玉米价格波动较小（最大变动幅度仅为实际价格平均值的0.7%），保持平稳价格水平，而预测结果曲线近乎保持水平，变化幅度明显弱于实际价格曲线。因此预测结果仅能反映出实际价格的大体变化趋势，但是无法对于价格小幅度的变化无法准确反映。

![con_LR_cor](/image/Con_LR_cor1.png )

建立好玉米价格预测模型后，我们持续运行模型多天，记录了模型的预测效果，并与实际价格进行比对，结果如下图所示，其中橙色曲线表示实际生猪价格，蓝色曲线表示预测结果。

由对比图可看出，在预测时间段中，实际价格缓慢上升，而预测结果也表现出了价格上升的趋势，但是幅度较小，无法预测短期内微小的价格波动。

![con_LR_pig](/image/Con_LR_cor.png )

### 模型建立过程

可参考[模型建立过程说明文档](/模型建立过程.md )

## 结果展示

本系统通过一个简单网页，可将外三元、内三元、土杂猪和玉米预测价格呈现给使用者。

该界面分为3部分。第一部分为未来价格走势展示，第二部分为针对当前数据的模型训练表现，第三部分为选定日期，展示特定日期预测价格。

![web_Page](/image/WebPage.png )

页面中第一个图表显示未来6个月的预测价格走势，页面中第二个图表显示随机抽取80%的原始数据作为训练数据，剩余20%数据作为预测输入数据的预测效果对比图，可根据该图查看模型的预测表现。下方提供一个查询未来6个月内某天的数据的功能，使用者可通过选择日期，查询生猪或玉米预测价格。

## 安装说明

本系统以Python编程技术为核心进行预测模型的搭建与实施，因此在使用前，需要安装Python并完成环境搭建工作。

1. 从GitHub中将程序代码下载到本地。

    ```bat
    git clone https://github.com/mscenter1/pigpriceML.git
    ```

2. 下载安装Python（推荐下载[3.7版本](https://www.python.org/downloads/release/python-372/)）。

   注：在安装时，勾选将Python 3.7加入系统环境变量的选项。

3. 待安装结束后，进行虚拟环境配置。

   注：以下操作均在命令行中进行。

    - 安装创建虚拟环境的Python模块。

        ```bat
        pip install virtualenv
        ```

    - 安装成功后，在切换路径至保存本系统程序的文件夹。

        如将程序保存在my_folder文件夹下，建立虚拟环境，命名为env_name（可替换为任意名称）。

        ```bat
        cd .../.../my_folder
        virtualenv env_name
        ```

    - 等待虚拟环境创建成功后，激活虚拟环境。

        ```bat
        cd env_name/Scripts
        activate
        ```

        激活成功后，命令行前端会显示(env_name)

    - 若后续需要退出此虚拟环境，在命令提示符中输入下方命令行。

        ```bat
        cd env_name/Scripts
        deactivate
        ```

4. 安装所需要使用的Python模块。

    - 在命令行中定位到项目中requirements.txt所在文件下。

        ```bat
        cd web_Project
        pip install -r requirements.txt
        ```

待安装成功后，Python环境搭建完成.

## 程序结构说明

本项目由4个文件夹和3个独立文件组成。

- 在web_Project文件夹下，存放有3个独立文件。

    sampledata.csv存放供程序进行预测的样本数据，为一段时间内全国平均的生猪价格、玉米价格和豆粕价格。

    requirements.txt存放本系统所需使用的Python安装模块，供使用者配置Python环境所用。

    app.py为本系统所需使用的web API接口。

- Data_Predict文件夹中存放预测模型的代码。

- Settings文件夹中存放模型所需使用的自变量名称等配置文件。

- static文件夹中存放显示网页界面所需使用的JavaScript和CSS文件。

- templates文件夹中存放网页的home.html文件，双击该文件即可访问展示网页。

## 使用说明

1. 将原始数据集保存为Web_Project文件下的sampledata.csv文件。

2. 在Python中，启动Web API接口:

    - 在命令提示符中，切换到app.py所在文件夹，输入：

        ```bat
        python app.py
        ```

    待程序成功运行后，即可访问展示页面。

3. 在浏览器中打开项目中template下的homepage.html文件

    - 在浏览器中，首先可在左上角的下拉框中，选择希望查看的价格类型的预测结果。当选择某项价格种类后，比如选择“外三元”后，下方所有数据均呈现外三元相关内容。
        
        <img src="./image/changetype.png" width="300">

    - 点击每张图表右上角的按钮，可依次切换图表呈现方式为：列表形式、折线图形式、柱状图形式，同时还可保存当前图表为png文件。

        <img src="./image/chartmanage.png" width="150">

    - 在界面下方，有一个选择日期输入框：

        <img src="./image/dateinput.png" width="500">

        通过点击输入框，会弹出日期选择栏目。选定一个未来日期后，并点击查询价格，界面会返回选定价格种类在那一天的预测价格。

        注：预测价格查询仅支持到2019年6月，即给定数据文件中数据记录的最后一天的6月后。

        <img src="./image/calender.png" width="500">
