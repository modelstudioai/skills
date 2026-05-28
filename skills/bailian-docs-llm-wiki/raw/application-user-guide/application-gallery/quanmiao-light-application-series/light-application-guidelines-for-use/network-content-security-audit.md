# 网络内容安全审核

网络内容安全审核工具能够扫描文本，快速检测涉黄、暴恐、侵权等违规内容，辅助人工审核，提高效率，确保网络环境合法合规、积极健康。此外，该工具还具备对文档进行审核与校对的功能，能够识别文字、标点及表达方面的问题，并提供相应的修改建议。

## **功能入口**

登录**阿里云百炼大模型服务平台**，在**应用广场**页面，点击[**网络内容安全审核**](https://bailian.console.aliyun.com/?spm=a2c4g.11186623.0.0.134172147obHXO#/app/app-market/quanmiao/network-content-audit)即可进入该轻应用控制台。

## **功能介绍**

### **应用详情**

在**网络内容安全审核**应用的**应用详情**页签，您可以查看功能描述、目标客群、最佳实践、计费规则、全妙相关应用推荐五部分内容。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932103.png)

### **效果调试**

点击**效果调试**页签，您可以参考以下步骤设置配置项。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932105.png)

#### **第一步：上传素材**

1.  把待审核内容贴入文本框，可以是文章、评论等，可参考官方示例填写。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932861.png)
    
2.  选择线索的模型，默认为**千问-Max**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932862.png)
    

#### **第二步：设置审核维度**

1.  输入**任务描述**。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932864.png)
    
2.  自定义审核维度。
    

-   按照格式输入**审核维度、审核标准**，支持单个或批量输入。可参考右侧官方提供的**示例**填写。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932865.png)
    
-   点击**批量输入**，可一键粘贴所有的审核维度、审核标准，自动识别。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932866.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932867.png)
    
-   点击**添加自定义维度**，可支持用户自定义新增维度，精准挖掘信息。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932868.png)
    

3.  **可选**：补充业务知识。
    

您可以在此输入业务背景、此任务的注意事项或者任务示例等补充内容。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932870.png)

#### **第三步：输出格式**

可根据右侧**格式示例**填写输出格式，也可以点击输入框内**智能生成JSON格式**一键生成输出格式。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932872.png)

### **查看API示例**

效果调试完成后，点击**API**页签，您可以查看对应生成的API示例。

**说明**

支持单条实时流式API和批处理API两种调用方式：

-   单条实时流式API：请求一次接口（输入一段文本、发起一次调用），就实时处理并流式返回结果。流式响应协议为Server-Sent Events（SSE）。
    
-   批处理API：输入待挖掘文件或多段文本，后台会创建一个任务，用户需通过任务ID轮询任务的状态、直到任务结束后，返回结果。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2818982471/p932846.png)
