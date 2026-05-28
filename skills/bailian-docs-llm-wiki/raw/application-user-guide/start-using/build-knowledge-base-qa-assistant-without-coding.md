# 0代码构建私有知识问答应用

大语言模型无法直接回答私有知识领域的问题，但您可以借助阿里云百炼的智能体应用构建能力和私有知识文档，零代码构建一个能回答私有领域问题的大模型问答应用。

## **效果展示**

**无专属知识库的应用**

在没有专属知识库时，大模型无法准确回答“阿里云百炼手机”的问题。

![无](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6101872271/p829329.png)

**有专属知识库的应用**

引入专有知识库后，大模型就能准确回答“阿里云百炼手机”方面的问题。

![有](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6101872271/p829330.png)

## **第一步：构建第一个阿里云百炼智能体应用****（约 1 分钟）**

1.  **创建空白应用：**访问[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面。点击**创建应用**，在弹窗的**智能体应用**页签中点击**立即创建**。
    
    > 本教程中将应用名设置为“阿里云百炼手机选购向导”。
    

![p996066 (1)](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4368624671/p1012894.jpeg)

2.  **选择模型：**为应用选择大语言模型，建议您选择**千问-Max**模型。
    
    > 使用大模型会产生计费。阿里云百炼提供了限时免费额度。如需查询免费额度，请您前往[模型广场](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market/all)，找到目标模型系列并单击进入详情页。
    

![change model](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3875211671/p1010558.png)

3.  **设计Prompt（提示词）**：也称为System Prompt，用于定义应用的角色和任务。建议设置Prompt（提示词）为：
    
    > “你是一位阿里云百炼手机导购，任务是帮助客户对比手机参数，分析客户需求，推荐个性化建议。”
    

![change prmpt](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3875211671/p1010559.jpeg)

4.  **配置欢迎语和预设问题**：点击右上角的![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0553987471/p956916.png)按钮，您可以设置智能体的欢迎语，并以您的常见问题作为预设问题，以便快速开展对话。
    
    > 欢迎语：你好，我是阿里云百炼手机选购向导！我在这里帮助你选购心仪的阿里云百炼手机。
    
    > 预设问题1：阿里云百炼手机有哪些款式？
    
    > 预设问题2：请你为我推荐一款性价比最高的手机。
    
    > 预设问题3：请你帮我挑选一款拍照效果最好的阿里云百炼手机，价格在3000元以内。
    

![change question](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3875211671/p1010566.jpeg)

![change question 2](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3875211671/p1010567.jpeg)

5.  **测试应用：**您可以在右侧点击任意问题发起提问：
    
    > 例如：“请你帮我挑选一款拍照效果最好的阿里云百炼手机，价格在3000元以内。”
    
    > 由于缺少“阿里云百炼手机”的相关知识，阿里云百炼应用的回答较为笼统，甚至可能无中生有。接下来，我们将引导您配置知识库。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3875211671/p956921.png)

## **第二步：构建知识库****（约 3 分钟）**

### **上传知识文档**

1.  访问[数据连接](https://bailian.console.aliyun.com/cn-beijing?spm=a2c4g.11186623.0.0.632e707f1mmU5d&tab=app#/connector/list)页面，点击创建连接器，选择文件类型连接器，填写连接器名称和描述后点击**确认**。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6735506771/p1066861.png)

2.  您可以使用我们提供的[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250603/duuuxk/%E9%98%BF%E9%87%8C%E4%BA%91%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)。打开上一步创建的数据连接器，将该文档上传后，点击**确认**。
    
    > **导入数据**向导提供了默认配置，在本教程中您无需改动这些设置，仅需上传知识文档即可。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3453268571/p944068.png)

3.  等待阿里云百炼导入完成。
    
    > 根据您上传的文档大小，阿里云百炼需要一定时间解析，通常占用1~6分钟，请您耐心等待。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4905211671/p944074.png)

### **创建知识库**

1.  进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面，点击**立即开通并创建**（首次使用）或**创建知识库**。选择**创建**标准版。
    

![createkb](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0732709571/p1010578.jpg)

2.  填写**知识库名称**，点击**下一步**。
    
    > 本教程中将知识库名称设置为“阿里云百炼手机”。
    
    > **创建知识库**向导提供了默认配置，在本教程中您无需改动这些设置。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4368624671/p1010580.png)

3.  在**选择类目**下勾选**默认类目**，点击**下一步**。
    
    > 在这一步中，请选择构建知识库的知识文档数据。**创建知识库**向导提供了默认配置，在本教程中您无需改动这些设置。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4905211671/p944088.png)

4.  选择**智能切分**，点击**完成**，即可成功创建知识库。
    
    > “智能切分”为系统预置切分策略，经评测对于多数文档可获得最佳的检索效果。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1894606771/p1010587.png)

5.  等待阿里云百炼解析完成。
    
    > 根据您上传的文档大小，阿里云百炼需要一定时间解析内容，通常占用1~2分钟，请您耐心等待。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4905211671/p944092.png)

## **第三步：为应用**添加知识库并发布应用**（约 1 分钟）**

1.  访问[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面。查找到您创建的“阿里云百炼手机选购向导”应用，鼠标悬停于应用卡片上，点击**配置**，进入应用配置界面。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4368624671/p1010601.png)

2.  点击**技能** > **知识库**旁的**+**按钮，再添加知识库，即可完成配置。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1894606771/p956923.png)

3.  您可以在右侧点击任意问题发起提问：
    
    > 例如：“请你帮我挑选一款拍照效果最好的阿里云百炼手机，价格在3000元以内。”
    
    > 引入知识检索增强后，阿里云百炼应用能够准确地回答您的选购问题。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3875211671/p956925.png)

4.  **发布应用：**确认内容变动无误后，点击**发布**。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3875211671/p956928.png)

## **后续步骤**

-   如果希望了解 Prompt撰写、插件工具、发布渠道以及更多应用功能，请参考[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)。
    
-   如果需要集成更多外部工具，或让应用自动化地完成复杂任务和业务流程，请参考[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)，也可以参考[应用类型介绍](https://help.aliyun.com/zh/model-studio/application-introduction)了解功能对比和应用场景。
    
-   如果希望通过 API 调用知识问答应用或其他阿里云百炼应用，请参考[调用智能体应用](https://help.aliyun.com/zh/model-studio/call-single-agent-application/)、[调用工作流应用](https://help.aliyun.com/zh/model-studio/invoke-workflow-application/)。
    
-   如果希望全代码开发高度定制化、交互逻辑复杂的 RAG 应用，请参考[Assistant API（下线中）](https://help.aliyun.com/zh/model-studio/assistantapi/)。
