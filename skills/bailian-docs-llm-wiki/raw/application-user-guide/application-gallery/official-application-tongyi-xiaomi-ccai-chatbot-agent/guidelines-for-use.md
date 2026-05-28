# 使用指南

本篇文档主要介绍通义晓蜜对话Agent中对话Agent构建和可视化流程技能编排的使用指南。

## **1\. 开通产品**

-   路径：[阿里云百炼-应用广场-通义晓蜜对话Agent](https://bailian.console.aliyun.com/?spm=5176.29619931.J__Z58Z6CX7MY__Ll8p1ZOR.1.74cd521cS5IvE8#/app/app-market/beebot)。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0220563471/p935960.png)

-   进入晓蜜对话Agent应用操作控制台，在右上角点击**免费开通**。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0220563471/p935961.png)

-   进入通义晓蜜对话Agent的开通界面，开通后，按实际调用量收费，即按日生成账单在阿里云账户余额中扣除。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932056.png)

## **2\.** Agent构建

### **2.1 创建应用**

点击**创建应用**，输入应用名称和应用描述，即可完成基础的Agent创建。

-   应用名称：按照业务需求填写Agent的名称；
    
-   应用描述：按照业务应用场景添加Agent的描述。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0220563471/p935962.png)

创建完成后的操作控制台：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6538449471/p965131.png)

### **2.2 配置界面**

#### **1\. 人设**

-   定义：在机器人空间，每个机器人可以添加人设，即通过提示词的方式调试机器人，可以在人设中对机器人的角色、工作流、技能、限制要求等内容在人设中作对应的定义要求。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932089.png)
    
-   选择模板：您可在**选择模板**窗口，插入通用模板，按照模板要求输入对应的人设限制。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932111.png)
    
-   优化：当您编辑完人设后，可以点击**优化**，模型会根据您的输入，优化人设内容。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932123.png)
    

#### **2\. 机器人开场白**

-   定义：指您打开机器人对话框时，机器人发起对话的开场白。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932121.png)
    

#### **3\. 知识库（流程技能、高频问答知识）**

-   定义：可绑定当前Agent对应的流程技能和高频问答知识。流程技能的具体的配置步骤可参考《[3\. 可视化流程技能编排](#a7e7986fc4k9q)》，高频问答知识的配置步骤可参考《[4\. 高频问答知识的配置](#d0b14121834k6)》。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965135.png)
    

#### **4\. 更多设置**

-   模型：当前内置**通义晓蜜大模型**，其中您可更改温度系数和上下文轮次来修改模型
    
-   通识知识：
    
-   回复语言：指机器人回复的语言
    
    -   与用户语言相同：指机器人回复的语言根据您提问的语言进行回复；
        
    -   仅中文：指无论您用什么语言提问，机器人都用中文回复；
        
    -   仅英文：指无论您用什么语言提问，机器人都用英文回复。
        
-   安全：
    
    -   安全拦截：当系统检查到输入和输出内容涉及到“答案敏感词”时，自动回复“敏感词话术”；
        
    -   安全预设话术：用户问题包含“用户敏感词”或模型生成回复包含敏感内容时，机器人自动使用敏感回复话术进行回复。默认安全预设话术为：“您说的这个问题我不能回答，您可以尝试询问其他问题”。
        
-   模型生成异常：当系统发生异常或服务超时情况下，机器人兜底回复话术。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932146.png)

### **2.3 调用量界面**

在调用量界面可以查看token的消耗量。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932315.png)

### **2.4 API界面**

对话Agent的调试信息会同步到API接口中，您可复制当前代码进行调用。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932320.png)

## **3\.** 可视化流程技能编排

### **3.1 新建流程**

1.  点击**知识库管理>流程**或者**+绑定流程**，打开流程列表窗口。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932331.png)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932343.png)
    
2.  点击**新建流程**，打开新建流程创建。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932344.png)
    
3.  按照要求填写对应流程**名称**和**描述**，点击**确认**，即可创建空白流程
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932352.png)
    
4.  找到新建的流程，点击**编辑**，进入流程编排页面。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932353.png)
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2963872471/p932356.png)
    
5.  新建开启分支，进入流程画布，在开始节点后，添加“分支”设置触发进入流程后继分支的条件。具体的操作步骤可查看下面的小视频：
    
    ![image.gif](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8133542471/p931138.gif)
    
6.  根据对话逻辑选择节点编排对话流程。
    
    ![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8133542471/p931139.png)
    

**重要**

流程编排完成后，点击**测试**，机器人将自动进行流程完整性检测，如果错误，请根据错误提示优化流程。具体情况可参考如下小视频：

![image.gif](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8133542471/p931140.gif)

### **3.2 流程调试**

1.  调试前需对环境进行设置
    

-   服务模拟：流程内的 API 插件会直接使用 mock 值进行返回，适用于 API 还没有准备好的情况。
    
-   随路参数：在用户发送问题时，同时带给机器人的外部参数，如电话接通时，可以将用户呼入号码以随路参数传递给机器人，后续在 API 插件调用时可以使用该参数。
    

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8133542471/p931141.png)

2.  对话调试
    
    直接进行对话，机器人回复后，可以点击**生成完成**查看机器人输出的内容，针对参数收集可以查看到机器人收集到的具体参数信息。
    
    ![image.gif](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8133542471/p931142.gif)
    

## **4**. 高频问答知识的配置

### **4.1 新建高频问答知识**

1.  点击**知识库管理>高频问答**或者**+绑定高频问答**，打开高频问答列表窗口。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965149.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965150.png)
    
2.  点击**创建高频问答库**，打开创建窗口，填写高频问答库名称。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965152.png)
    
3.  找到新建的高频问答库，点击编辑，进入添加高频问答知识的页面。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965154.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965155.png)
    
4.  点击**新增高频问答**或者**导入高频问答**，在高频问答库中添加对应的高频问题，按照要求填写问题、答案类型、问题答案、生效时间、相似问法，点击**提交**，即可新增成功。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965159.png)![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965160.png)
    
    新增成功后：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965161.png)
    

### **4.2 绑定高频问答知识库及测试效果**

1.  点击**绑定**，即可将对应知识库绑定到机器人上。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965162.png)
    

绑定成功展示：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965165.png)

2.  在左侧对话测试窗测试效果，如下图所示：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5538449471/p965166.png)
