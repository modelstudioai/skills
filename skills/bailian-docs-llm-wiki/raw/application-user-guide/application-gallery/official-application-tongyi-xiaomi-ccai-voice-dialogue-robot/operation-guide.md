# 语音对话机器人操作指南

本文档介绍通义晓蜜CCAI-语音对话机器人在阿里云百炼控制台如何操作。

## **1\. 创建应用**

-   路径：**[应用广场](https://bailian.console.aliyun.com/#/app-market)**\-应用实践-通义晓蜜CCAI-语音对话机器人-立即查看
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000691.png)
    
-   第一步：首先点击**我的应用**按钮，再点击**创建应用**按钮；![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000694.png)
    
-   第二步：进入新建应用弹窗，编辑应用名称与应用创建方式。点击**确定**。进入调试窗口。
    
    -   **应用名称：**根据实际业务需要修改应用名称。
        
    -   **应用描述：**自定义填入应用实际使用描述说明。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000698.png)
        

## **2.机器人配置**

机器人配置目前使用的为prompt构建模式。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9886579371/p914777.png)

-   **模型选择：**通义晓蜜-Plus、通义晓蜜-Max、通义晓蜜-Turbo。
    
-   **指令信息：**选择指令模板，可以选择直接使用官方预置模板，当前线上提供了通用场景、服务满意度调研、家电上门安装预约、游戏福利推送介绍四种模板。同时支持自定义指令模板。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000715.png)
    
-   **变量配置：**可在指令信息中通过**${xxx}**样式进行插入。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000733.png)
    
-   **指令配置：**如果当前参考的流程话术中存在特殊指令#\[...\]，请在回复中添加#\[...\]，目前支持传入挂机指令#\[HangUp\]。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000747.png)
    
-   **语音配置：**进行音色选择配置，配置完成后可在机器人呼叫时运用。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000739.png)
    
    -   音色模板：可选择大模型音色，如：龙小夏V2、龙小夏等。
        
    -   音量：范围为0～100，值越大声音越响亮。
        
    -   语速：范围为-500～500，值越大语速越快。
        
    -   音调：范围为-500～500，值越大音调越高昂。
        
-   **高级配置：**对机器人的其他能力进行配置。
    
    -   静默超时：自定义配置时长，范围在1～60秒，当对话过程中用户回复超过配置的静默时长后播报静默话术。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000740.png)
        
-   **点击“呼叫”按钮，查看测试结果。**
    
    **说明**
    
    目前通过控制台测试时不支持变量传入。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000746.png)
    
-   **发布机器人：**点击**发布**按钮，当页面提出**发布成功**，即表示为成功发布。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000757.png)
    

## **3.我的应用**

路径：**[应用广场](https://bailian.console.aliyun.com/#/app-market)**\-应用实践-通义晓蜜CCAI-语音对话机器人-立即查看。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000691.png)

### **3.1 调用量**

-   调用次数按小时进行计量上报，查询当天时，折线图展示每小时调用量曲线。
    
-   查询某个日期区间数据时，折线图展示按天调用量曲线。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000755.png)

### 3.2 应用修改、删除

-   **应用修改：**进入我的应用后，可以点击应用右上角选择修改应用，对该应用名称进行修改。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000750.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000751.png)
    
-   **删除应用：**进入我的应用后，可以点击应用的右上角选择删除应用，对该应用进行删除，弹出“确认删除”二次确认框，选择确认删除，将成功删除。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000752.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000753.png)
    

### **3.3API调用**

应用API：通过API服务输出给客户，方便客户进行集成和使用官方预置模板或自定义模板，客户自定义前端样式

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9719585571/p1000756.png)
