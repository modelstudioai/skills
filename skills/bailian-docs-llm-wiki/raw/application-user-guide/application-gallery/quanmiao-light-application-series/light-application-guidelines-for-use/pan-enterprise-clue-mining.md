# 泛企业线索挖掘

泛企业线索挖掘应用支持从社交媒体数据、通话记录等渠道挖掘用户画像及二次销售机会，同时收集竞品和行业趋势相关线索。

## **功能入口**

登录**阿里云百炼大模型服务平台**，在**应用广场**页面，点击[**泛企业线索挖掘**](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.134172147obHXO#/app/app-market/quanmiao/enterprise-clue-mining)即可进入该轻应用控制台。

## **功能介绍**

### **应用详情**

在**泛企业线索挖掘**应用的**应用详情**页签，您可以查看功能描述、目标客群、最佳实践、计费规则、全妙相关应用推荐五部分内容。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932099.png)

### **效果调试**

点击**效果调试**页签，您可以参考以下步骤设置配置项。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932106.png)

#### **第一步：上传素材**

1.  把待挖掘内容粘贴至文本框，可以是一段对话或通话记录，可参考官方示例填写。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932795.png)
    
2.  选择线索的模型，默认为**千问-Max**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932807.png)
    

#### **第二步：设置内容标签**

1.  输入**任务描述**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932812.png)
    
2.  自定义线索标签。
    
    -   按照格式**输入标签名称、标签含义和取值**，支持单个/批量输入。可参考官方提供的**示例**填写。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932816.png)
        
    -   点击**批量输入**，可一键粘贴所有的标签名称、标签含义和取值，自动识别。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932823.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932819.png)
        
    -   点击**添加自定义标签**，可支持自定义标签，精准挖掘信息。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932820.png)
        
    
3.  **可选**：补充业务知识。
    
    您可以在此文本框中输入业务背景、此任务的注意事项或者任务示例等补充内容。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932825.png)
    

#### **第三步：设置输出格式**

您可根据右侧**格式示例**填写输出格式，也可以点击输入框内的**智能生成JSON格式**，一键生成输出格式。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932829.png)

#### **第四步：开始挖掘**

点击**开始挖掘**按钮，挖掘结果将在挖掘结束后显示在右侧，您可复制或下载至本地查阅。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932831.png)

### **查看API示例**

效果调试完成后，点击**API**页签，您可以查看对应生成的API示例。

**说明**

支持单条实时流式API和批处理API两种调用方式：

-   单条实时流式API：请求一次接口（输入一段文本、发起一次调用），就实时处理并流式返回结果。流式响应协议为Server-Sent Events（SSE）。
    
-   批处理API：输入待挖掘文件或多段文本，后台会创建一个任务，用户需通过任务ID轮询任务的状态、直到任务结束后，返回结果。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7718982471/p932832.png)
