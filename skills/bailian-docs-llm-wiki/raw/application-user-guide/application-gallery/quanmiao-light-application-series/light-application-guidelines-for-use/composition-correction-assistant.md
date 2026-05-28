# 作文批改助手

作文批改助手帮助教师高效批改作文。它自动分析学生作文，检查语法和拼写错误，识别诗词典故。快速生成结构化评分评语和修改建议，减少手动批改时间，提升批改效率和反馈质量。

## **功能入口**

登录**阿里云百炼大模型服务平台**，在**应用广场**页面，点击[**作文批改助手**](https://bailian.console.aliyun.com/?tab=app#/app/app-market/quanmiao/homework-correction)即可进入轻应用控制台。

## **功能介绍**

### **应用详情**

在作文批改助手应用的**应用详情**页签，您可以查看功能描述、目标客群、最佳实践、计费规则、全妙相关应用推荐五部分内容。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981515.png)

### **效果调试**

点击**效果调试**页签，参考以下步骤设置配置项。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981516.png)

#### **第一步：**设置科目及试题

1.  选择年级
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981522.png)

2.  设置作文总分
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981524.png)

3.  设置作文题目，可一键填入示例
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981526.png)

#### **第二步：**上传学生作文

选择输入方式

1.  直接输出文字：适用于已有作文文本的情况。
    
2.  从照片中AI提取文字：通过大模型自动识别图片上的文字。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981528.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981530.png)

#### **第三步：**确认评阅点

1.  选择模型。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981534.png)

2.  （可选）补充其他评阅要点：系统预置的评阅要点有打分、优点总结、改进建议及评语。如您有其他的要点，请在此处输入。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981536.png)

### **查看API示例**

效果调试完成后，点击**API**页签，查看对应生成的API示例。

**说明**

支持单条实时流式API和批处理API两种调用方式：

-   单条实时流式API：请求一次接口（输入一段文本、发起一次调用），就实时处理并流式返回结果。流式响应协议为Server-Sent Events（SSE）。
    
-   批处理API：输入待挖掘文件或多段文本，后台会创建一个任务，用户需通过任务ID轮询任务的状态、直到任务结束后，返回结果。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4357951571/p981537.png)
