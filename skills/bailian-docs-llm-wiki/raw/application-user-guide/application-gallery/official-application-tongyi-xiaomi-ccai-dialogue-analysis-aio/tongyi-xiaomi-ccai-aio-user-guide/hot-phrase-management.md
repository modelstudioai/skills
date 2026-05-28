# 热词组配置管理与使用

为提升语音转译的准确性，您可以在语音质检分析场景中使用热词组。本文档将介绍其配置与使用方法。

## **热词配置**

热词组仅对离线/实时语音质检分析场景生效，用于提升语音转译的准确性。

### **1.热词组管理**

-   进入热词组管理的路径：
    
    -   路径1：进入[**通义晓蜜CCAI-对话分析AIO**](https://bailian.console.aliyun.com/?tab=app#/app/app-market/ccai)后，点击我的应用，可在界面中看到**热词组管理**按钮。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6179940671/p1016061.png)
        
    -   路径2：通过进入具体应用的配置页面，点击**选择热词组**时进行添加对应的热词组。
        
        **说明**
        
        目前热词组支持通过自定义创建的应用；通过Agent创建的应用，需在‘专业构建模式’下才能找到并配置热词组。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7898424471/p939307.png)
        
-   在热词组管理界面，点击‘**新建热词组**’，填写名称和热词后，点击‘**确定**’完成创建。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7898424471/p939100.png)
    
    -   热词组名称：不超过10个字。
        
    -   热词：每个热词组不超过128个热词。
        
        -   热词：填入对应需要提高准确率的热词，重要限制：当前版本热词仅支持纯汉字，不支持英文、数字及特殊字符。包含非汉字的热词将无法生效。
            
        -   权重：取值范围为1到5之间的整数，默认值：2；如果效果不明显可以适当增加权重，但是当权重较大时可能会引起负面效果，导致其他词语识别不准确。
            
    -   操作：删除已添加的热词。
        
-   创建成功后，新的热词组将显示在列表中，并支持编辑或删除。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7898424471/p939301.png)
    

### **2.热词组在应用中的使用**

进入具体应用的设置，选择并绑定所需的热词组。

**说明**

每个应用仅支持绑定一个热词组。

1.  选择对应的热词组![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7898424471/p939328.png)
    
2.  选择完成后可以查看绑定情况![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7898424471/p939541.png)
