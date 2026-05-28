# 如何对应用进行编辑、删除等管理,如何进行API调用、如何查看调用量

本文档介绍如何对应用进行编辑、删除等管理，如何进行API调用、如何查看调用量。

## **我的应用**

路径：[应用广场](https://bailian.console.aliyun.com/#/app-market)→ 点击[应用实践](https://bailian.console.aliyun.com/?tab=app#/app-market/lightApplication)→ 找到**通义晓蜜CCAI-对话分析AIO**，选择[查看详情](https://bailian.console.aliyun.com/?tab=app#/app/app-market/ccai)，即可进入**我的应用****。**![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4679940671/p1016065.png)

### 3.1 应用复制、删除、修改

-   **应用复制：**在**我的应用**中，可以点击应用右上角选择复制应用，对该应用进行复制。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7209853471/p935536.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7209853471/p935538.png)
    
-   **应用修改：**同时可以点击应用右上角选择修改应用，对该应用名称进行修改。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7209853471/p935539.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0159666271/p850637.png)
    
-   **应用删除：**如果需要删除该应用，可以点击应用的右上角选择删除应用，对该应用进行删除，弹出“确认删除”二次确认框，选择确认删除，将成功删除。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7209853471/p935540.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0159666271/p850646.png)
    

### 3.2 API调用

-   应用API：应用提供标准化API接口，用于向客户系统输出对话分析结果。支持集成官方预置Agent模板或用户自定义模板，客户可通过API获取结构化响应，并自主设计前端展示样式。
    
    -   当通过**对话分析Agent创建方式**创建应用时，使用自定义指令的API调用：
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9774988371/p910406.png)
        
    -   通过**自定义创建方式**的API调用：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9774988371/p910410.png)
        

### **3.3 调用量**

-   调用次数按输入和输出token总数计量，以2000 tokens 为一个计量单位，输入与输出总token数小于等于2000 tokens为1次调用，大于2000小于等于4000 tokens 为2次调用，向上取整，以此类推。
    
-   调用次数按小时进行计量上报，查询当天时，折线图展示每小时调用量曲线。
    
-   查询某个日期区间数据时，折线图展示按天调用量曲线。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7209853471/p935534.png)
