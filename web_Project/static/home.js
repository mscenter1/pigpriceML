var typePara='waisan'
// 定义下拉框切换函数
function ChangeTypeF(){
    typePara = document.getElementById("ChangeType").value
    getPredictData()
    getPerformanceData()
}
var a = echarts;
// 显示预测走势
var myChart = a.init(document.getElementById('Predict_Result'));
// 显示模型训练结果对比
var myChart_Train = a.init(document.getElementById('Train_Result'));

var yMin_P = 10
var yMax_P = 15
var yMin_T = 10
var yMax_T = 15
// 图表设置
myChart.setOption({
    title: {
        text: '未来6个月预测走势'
    },
    tooltip : {
        trigger: 'axis'
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [{
            type : 'category',
            boundaryGap : false,
            data : []
    }],
    yAxis : [{
        type : 'value',
        axisLabel : {
            formatter: '{value}'
        },
        min: yMin_P,
        max: yMax_P,
    }],
    series : [{
        name:'预测数据',
        type:'line',
        smooth:true,
        data:[]
        }]
});

myChart_Train.setOption({
    title: {
        text: '模型训练表现'
    },
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['预测价格','真实价格']
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataView : {show: true, readOnly: false},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    calculable : true,
    xAxis : [{
            type : 'category',
            boundaryGap : false,
            data : []
    }],
    yAxis : [{
        type : 'value',
        axisLabel : {
            formatter: '{value}'
        }
    }],
    series : [
        {
            name:'预测价格',
            type:'line',
            data:[]
        },
        {
            name:'真实价格',
            type:'line',
            data:[]
            }]
});
//数据加载完之前先显示一段简单的loading动画
myChart.showLoading();    
myChart_Train.showLoading(); 

//存放显示预测走势图标的X轴内容（日期）
var X_Dates = []; 
//存放显示预测走势图标的Y轴内容（价格数据）
var Y_Values = []; 

//存放显示模型训练效果的X轴内容
var X_Dates_Train = []; 
//存放显示模型训练效果的Y轴内容（真实价格）
var Y_Values_True = []; 
//存放显示模型训练效果的Y轴内容（预测结果）
var Y_Values_Pre = [];

//获取数据并显示
getPredictData()
getPerformanceData()


//显示预测走势
function getPredictData(){
    //初始化X、Y轴内容
    X_Dates = [];
    Y_Values = []; 
    $.ajax({
        type : "get",
        url : "http://localhost:8000/PredictRes/"+typePara,
        success : function(result) {
            if (result) {
                //将数据填充到X、Y轴内容中
                result = result.split('\n')
                for (var i = 0; i < result.length - 1; i++) {
                    var dataItem1 = result[i].split('  ');
                    var x2 = (dataItem1[1] - 0).toFixed(2)
                    X_Dates.push(dataItem1[0]);
                    Y_Values.push(x2);
                }
                //设置坐标轴范围
                var y1 = Array.min(Y_Values)
                var y2 = Array.max(Y_Values)
                
                if(typePara === 'corn'){
                    yMin_P = (y1 - 0.1).toFixed(2)
                    yMax_P = (y2 + 0.1).toFixed(2)
                }
                else{
                    yMin_P = (y1 - 1).toFixed(2)
                    yMax_P = (y2 + 1).toFixed(2)
                }

                //隐藏加载动画
                myChart.hideLoading(); 

                //加载数据图表
                myChart.setOption({
                    xAxis: {
                        data: X_Dates
                    },
                    yAxis:{
                        min: yMin_P,
                        max: yMax_P,
                    },
                    series: [{
                        //根据名字对应到相应的系列
                        name: '预测数据',
                        data: Y_Values
                    }]
                });
            }
        },
        error : function(errorMsg) {
            //请求失败时执行该函数
            alert("图表请求数据失败!");
            myChart.hideLoading();
        }
    })
}

//显示模型训练效果图表
function getPerformanceData(){
    //初始化X、Y轴内容
    X_Dates_Train = []; 
    Y_Values_True = [];
    Y_Values_Pre = [];
    $.ajax({
        type : "get",
        url : "http://localhost:8000/Performance/"+typePara,
        success : function(result) {
            if (result) {
                //将数据填充到X、Y轴内容中
                result = result.split('\n')
                for (var i = 0; i < result.length - 1; i++) {
                    var dataItem1 = result[i].split('  ');
                    X_Dates_Train.push(i+1)
                    Y_Values_True.push((dataItem1[0] - 0).toFixed(2));
                    Y_Values_Pre.push((dataItem1[1] - 0).toFixed(2));
                }
                
                //设置坐标轴范围
                var yt_min = Array.min(Y_Values_True)
                var yp_min = Array.min(Y_Values_Pre)
                var yt_max = Array.max(Y_Values_True) 
                var yp_max = Array.max(Y_Values_Pre)
                var y1, y2
                yt_min>yp_min ? y1 = yp_min: y1 = yt_min
                yt_max>yp_max ? y2 = yt_max: y2 = yp_max
                if(typePara === 'corn'){
                    yMin_T = (y1 - 0.1).toFixed(2)
                    yMax_T = (y2 + 0.1).toFixed(2)
                }
                else{
                    yMin_T = (y1 - 1).toFixed(2)
                    yMax_T = (y2 + 1).toFixed(2)
                }

                //隐藏加载动画
                myChart_Train.hideLoading();

                //加载数据图表
                myChart_Train.setOption({
                    xAxis: {
                        data: X_Dates_Train
                    },
                    yAxis:{
                        min: yMin_T,
                        max: yMax_T
                    },
                    series: [
                        {
                            // 根据名字对应到相应的系列
                            name: '预测价格',
                            data: Y_Values_Pre
                        },
                        {
                            // 根据名字对应到相应的系列
                            name: '真实价格',
                            data: Y_Values_True
                        }
                    ]
                });
            }
        },
        error : function(errorMsg) {
            //请求失败时执行该函数
            alert("图表请求数据失败!");
            myChart_Train.hideLoading();
        }
    })
}

//显示指定日期预测价格
function getDateData(SpcDate){
    var date1 = SpcDate.split('-');
    var year = date1[0];
    var month = date1[1];
    var day = date1[2];
    var dateurl = year+'/'+month+'/'+day
    $.ajax({
        type : "get",
        url : "http://localhost:8000/PredictDay/"+typePara+"/"+dateurl,
        success : function(result) {
            if (result === 'No Data') {
                var div1 = document.getElementById("PedictDay");
                var div2 = document.getElementById("Nodata");
                if(div1.style.display=='block'){
                    div1.style.display='none';
                }
                if(div2.style.display=='none'){
                    div2.style.display='block';
                }
            }
            else{
                var div1 = document.getElementById("PedictDay");
                var div2 = document.getElementById("Nodata");
                if(typePara === 'waisan'){
                    $('#TypeName').html('外三元价格');
                }
                else if(typePara === 'neisan'){
                    $('#TypeName').html('内三元价格');
                }
                else if(typePara === 'tuza'){
                    $('#TypeName').html('土杂猪价格');
                }
                else{
                    $('#TypeName').html('玉米价格');
                }
                $('#TypePrice').html('￥' + (result - 0).toFixed(2));
                if(div1.style.display=='none'){
                    div1.style.display='block';
                }
                if(div2.style.display=='block'){
                    div2.style.display='none';
                }
            }
            
        }
    })
}

// 取出数组中最大值
Array.max = function (array) {
    return Math.max.apply(Math, array);
};
// 取出数组中最小值
Array.min = function (array) {
    return Math.min.apply(Math, array);
};