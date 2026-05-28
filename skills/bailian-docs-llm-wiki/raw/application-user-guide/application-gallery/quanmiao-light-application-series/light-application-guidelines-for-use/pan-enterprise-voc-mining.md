# 泛企业VOC挖掘

泛企业VOC挖掘工具通过大模型对评论、论坛、客服聊天及通话等非结构化VOC数据实现智能标签化处理，支持标签选择或自定义，相比人工或规则打标，具备更高的准确率及响应速度，可快速适配业务标签的动态变化需求。

## **功能入口**

登录**阿里云百炼大模型服务平台**，在**应用广场**页面，点击[**泛企业VOC挖掘**](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.134172147obHXO#/app/app-market/quanmiao/voc)即可进入该轻应用控制台。

## **功能介绍**

### **应用详情**

在**泛企业VOC挖掘**应用的**应用详情**页签，您可以查看功能描述、目标客群、最佳实践、计费规则、全妙相关应用推荐五部分内容。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2718982471/p932062.png)

### **效果调试**

在**效果调试**页签，如果您是首次使用，可以参考官方示例完成相关配置填写（本文以**电商平台用户反馈分析**为例说明）。

点击**电商平台用户反馈分析**，在弹出的文本框中点击**使用本示例**一键填充单个示例。您也可以点击**批量挖掘**，系统将自动填充批量挖掘示例。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944696.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944697.png)

#### **第一步：上传素材**

1.  输入**待挖掘素材**内容，您可以选择以下两种素材输入方式：
    
    -   **单个素材**：输入单条VOC，快速体验。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944713.png)
        
    -   **批量素材**：支持批量数据同时分析。先点击**批量挖掘**，再点击**下载模板**后上传，提高效率。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944712.png)
        
        支持.xlsx、.xls、.txt、.csv、.pdf、.docx、.md格式的文件，文件最大20MB。
        
    
2.  选择模型，默认为**千问-Max**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944434.png)
    

#### **第二步：**设置内容标签

1.  输入**任务描述**，帮助模型理解内容。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944715.png)
    
2.  设置**内容标签**：
    
    -   按照格式输入**标签名称**、**标签含义**，支持单个/批量输入。可参考官方提供的示例填写。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944765.png)
        
    -   添加自定义内容标签：点击**添加自定义标签**，可支持自定义标签，精准挖掘信息。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944752.png)
        
        > 支持多级标签，目前支持两级，层级间用"-"区分，例如：品牌名称-产品功能。
        
    -   批量输入多个自定义内容标签：点击**批量输入**，可一键粘贴所有的标签名称、标签含义，自动识别。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944753.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944755.png)
        
        -   每行为一组，用换行区分；
            
        -   每组内，用分隔符隔开标签名称、标签含义，例如：
            
            性别 男、女、无法判断
            
            最高学历 小学、初中、大学、研究生、博士
            
        
3.  可选：补充业务知识。
    
    您可以在此文本框中输入业务背景、此任务的注意事项或者任务示例等补充内容。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944770.png)
    

#### **（可选）第三步：**设置输出格式

输出格式推荐使用`json`格式，且请注意KEY和您所需要挖掘的标签要能一一对应，您可以参考示例来修改。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944775.png)

-   在完整填写第一步与第二步的前提下，点击**智能生成JSON格式**，模型会根据当前数据生成输出格式作为参考，请自行检查并确认最终输出格式。
    
-   您也可以点击**重置**清空输出格式。
    

#### **（可选）第四步：设置高级功能**

1.  开启**设置筛选维度**开关后，模型会先对VOC进行筛选，仅符合设定条件的VOC才参与挖掘，进一步精准范围。可输入单条或多条筛选维度。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944808.png)
    

您也可以点击**添加自定义标签**或**批量输入**，添加筛选维度，具体操作请参见[设置内容标签](#4320da38d7iar)。

2.  选中**保存输入项**。
    
    > 选中后系统会默认保存本次设置的筛选条件、标签，以及标签内容。
    
    > 如果切换账号或清除浏览器本地存储，保存的配置数据将丢失。
    

#### **第五步：开始挖掘**

点击**开始挖掘**，挖掘结果将在挖掘结束后显示在右侧。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944863.png)

### **查看API示例**

效果调试完成后，点击**API**页签，您可以查看对应生成的API示例。

**说明**

支持单条实时流式API和批处理API两种调用方式：

-   单条实时流式API：请求一次接口（输入一段文本、发起一次调用），就实时处理并流式返回结果。流式响应协议为Server-Sent Events（SSE）。
    
-   批处理API：输入待挖掘文件或多段文本，后台会创建一个任务，用户需通过任务ID轮询任务的状态、直到任务结束后，返回结果。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3991694471/p944504.png)
