# 10分钟在钉钉上增加一个AI机器人

在阿里云上，您只需 10 分钟，无需任何编码，即可为您的组织在钉钉平台上创建一个有大模型能力加成的 AI 机器人。这个机器人可以全天候（7x24）响应用户咨询，还能解答私域问题，成为您业务的专属机器人，提升用户体验，增强业务竞争力。

## **方案概览**

在钉钉中添加一个 AI 机器人，只需几步：

1.  **创建大模型问答应用**：通过阿里云百炼创建一个大模型应用，并获取调用大模型应用 API 的相关凭证。
    
2.  **创建钉钉应用**：创建一个钉钉应用，在您的钉钉组织中提供机器人问答服务。
    
3.  **创建钉钉连接流：**基于阿里云的 AppFlow 服务，在无需编写代码的情况下，完成钉钉机器人和阿里云百炼 RAG 应用的关联，最终实现用户在钉钉聊天中和 RAG 应用对话。
    
4.  **配置钉钉机器人**：为钉钉应用配置机器人，添加到群聊中可以回答用户问题。
    
5.  **为大模型问答应用增加私有知识：**开启知识检索增强（RAG），为大模型问答应用增加知识库，让 AI 机器人能回答私有领域的问题，帮助您更好地应对用户咨询。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2205080371/p868333.png)

![d022fe9c-c5d5-4c0b-a7fb-85b277b3eb91](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830568.gif)

## **1\. 创建大模型问答应用**

首先创建百炼应用，获取大模型推理 API 服务。

> 阿里云百炼提供的[新用户免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)可以完全覆盖本教程所需资源消耗。额度消耗完后按 token 计费，相比自行部署大模型可以显著降低初期投入成本。

### **1.1 创建应用**

1.  进入百炼控制台的[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面**，**点击右上角**创建应用**，选择**智能体应用**，点击**立即创建**。
    
2.  在**应用配置**页面，模型选择千问-Plus，其他参数保持默认。
    
    > 您可输入Prompt设置角色，引导模型应对客户咨询。
    
    ```
    你叫小助，可以帮助用户解答产品选购、使用等方面的问题。
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9805168571/p944468.png)
    
3.  在页面右侧可以提问验证模型效果。不过目前它还无法准确回答您公司的商品信息。点击右上角的**发布**，我们将在后面的步骤中去解决这一问题。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5082715571/p996997.png)
    

### **1.2 获取调用 API 所需的应用ID和API Key**

为了在后续通过 API 调用大模型应用的能力，需要获取阿里云百炼API Key和应用 ID。

1.  在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中可以查看所有百炼应用 ID。保存应用 ID 到本地用于后续配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2115805571/p959107.png)
    
2.  前往[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面，点击**创建API Key**，在弹出窗口中创建一个新 API-Key。保存 API-Key 到本地用于后续配置。
    

## **2\. 创建钉钉应用**

接下来您需要在您的组织中创建钉钉应用，作为 AI 助手回答用户问题。

**重要**

创建钉钉应用需要您的钉钉账号有开发者权限。您可以联系您的组织管理员获取钉钉开放平台的开发权限，具体操作请参见[获取开发者权限](https://open.dingtalk.com/document/orgapp/obtain-developer-permissions)。

### **2.1 创建应用**

1.  访问[钉钉开放平台](https://open-dev.dingtalk.com/)，点击**创建**。如果创建过应用未展示应用开发指引，点击**立即开始**进入钉钉应用页面。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830053.png)
    
2.  在应用开发的左侧导航栏中，点击**钉钉应用**，在**钉钉应用**页面右上角点击**创建应用**。![11](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830054.png)
    
3.  在**创建应用**面板，填写**应用名称**和**应用描述**，上传应用图标，完成后点击**保存**。![12](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830055.png)
    

### **2.2 查看应用 Client ID 和 Client Secret**

在左侧菜单选择**凭证与基础信息**，复制 Client ID 和 Client Secret，用于下一步创建连接流。

![21](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830138.png)

### **2.3 授予应用**发送卡片消息**权限**

创建卡片后，您需要给应用授予发送卡片消息的权限。

1.  访问[钉钉应用列表](https://open-dev.dingtalk.com/fe/app)。找到刚刚创建的应用，点击应用名称进入详情页面。
    
2.  在左侧菜单选择**开发配置** > **权限管理**，在左侧搜索框分别输入`Card.Streaming.Write`和`Card.Instance.Write`，并在操作列点击**立即开通**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8160854771/p1061820.png)
    

## 3\. 创建钉钉连接流

AppFlow 可以让您在不写代码的情况下，通过界面配置就可以将大模型应用和钉钉连接起来。您可以通过预置的 AppFlow 模板创建一个钉钉机器人连接流。

1.  使用[AppFlow模板](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/tl-cd3233c4582285f4de63?from=solution)创建连接流，点击**立即使用**进入创建流程。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8160854771/p1061818.png)
    
2.  在连接流的**账户授权**配置向导页，点击**添加新凭证**。在创建凭证对话框中，填入之前获取的钉钉应用的 Client ID 和 Client Secret，并设置一个自定义凭证名称。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0862101571/p979454.png)
    
3.  在连接流的**账户授权**配置向导页，点击**添加新凭证**。在创建凭证对话框中，填入之前获取的 API-KEY，并设置一个自定义凭证名称。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0862101571/p979479.png)
    
4.  在**执行动作**配置向导页，填写**应用Id**；**模版类型**保持默认**公共模版**；完成后点击**下一步**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8160854771/p1061819.png)
    
5.  在**基本信息**配置向导页，填写**连接流名称**和**连接流描述**（建议保持默认），完成后点击**下一步**。
    
6.  界面提示流程配置成功，复制 **WebhookUrl**，点击**发布**。![27](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830229.png)
    

## 4\. 配置钉钉机器人

有了webhook地址后，接下来您可以在钉钉应用中配置机器人来回答用户问题了。

### 4.1 配置钉钉机器人

1.  访问[钉钉应用列表](https://open-dev.dingtalk.com/fe/app)。找到刚刚创建的应用，点击应用名称进入详情页面。
    
2.  在**添加应用能力**页面，找到机器人卡片，点击**添加**。![13](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830056.png)
    
3.  在机器人配置页面，打开**机器人配置**开关，您可以参考下图完成配置。**消息接收模式**请选择**HTTP模式**，**消息接收地址**为刚刚的 **WebhookUrl**。然后点击**发布**。
    
    **重要**
    
    **消息接收模式**请选择**HTTP模式**，目前AppFlow仅支持HTTP模式，选择Stream模式会导致无法返回消息。
    
    ![30](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830299.png)
    

### **4.2 发布应用版本**

应用创建完成后，如果需要将应用供企业内其他用户使用，需要发布一个版本。

1.  点击**应用开发**，在**钉钉应用**页面，点击目标应用（**阿里云百炼手机答疑**）。![8](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830050.png)
    
2.  在目标应用开发导航栏，点击**版本管理与发布**，在**版本管理与发布**页面，点击**创建新版本**。进入版本详情页面，输入**应用版本号**和**版本描述**信息，选择合适的**应用可见范围**，完成后点击**保存**。并在弹窗中点击**直接发布**。![10](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830052.png)
    

### 4.3 测试机器人

你可以创建群聊或在已有群聊中添加机器人，并与机器人对话，查看效果。

1.  在钉钉**群管理**中添加机器人​。进入钉钉群**群设置**页面，点击**机器人**卡片区域，在**机器人管理**页面，点击**添加机器人**。在**添加机器人**的**搜索**文本框中输入目标机器人名称，并选中要添加的机器人。点击**添加**，完成后再点击**完成添加**。![14](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830057.png)
    
2.  在钉钉群中或私聊时**@机器人**，进行交流互动。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830339.png)
    

## 5\. 为大模型问答应用增加私有知识

### **5.1 配置知识库**

接下来，我们可以尝试让大模型在面对客户问题时参考这份文档，以产出一个更准确的回答和建议。

假设您在一家售卖智能手机的公司工作。您的钉钉用户群上会有很多涉及智能手机相关的问题，如支持双卡双待、屏幕、电池容量、内存等信息。不同机型的详细配置清单参考：[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240701/geijms/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)。

1.  **上传文件：**在阿里云百炼控制台的[文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)页签中点击**导入数据**，根据引导上传我们虚构的阿里云百炼系列手机产品介绍：
    
    > 根据您上传的文档大小，阿里云百炼需要一定时间解析，通常占用1~6分钟，请您耐心等待。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5603325471/p944474.png)
    
2.  **创建知识库：**进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面，点击**立即开通并创建**（首次使用）或**创建知识库**。选择**创建**标准版，填写**知识库名称**，其余设置可保持默认，点击**下一步**，选择刚才上传的文档，其他参数保持默认即可。后续大模型回答时可以检索参考知识库中的文档。
    
    > 选择向量存储类型时，如果您希望集中存储、灵活管理多个应用的向量数据，可选择**ADB-PG**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5301724671/p944483.png)
    
3.  **引用知识：**完成知识库的创建后，访问[应用管理](https://bailian.console.aliyun.com/?&tab=app#/app-center)页面，选择之前创建的应用。添加目标知识库，调用方式选择**必定调用**。测试验证符合预期后点击**发布**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9805168571/p944485.png)
    

### **5.2 检验效果**

有了参考知识，AI 机器人就能准确回答您关于阿里云百炼手机的问题了。![66-1](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830454.png)

## 总结

通过前面的学习，您已经能搭建一个大模型 RAG 应用，并且将其以 AI 机器人的形式添加到钉钉群中来应对客户咨询，过程仅需 0 元（免费试用额度内）10分钟。

### **应用评测**

建议您在正式上线 AI 机器人前，组织业务人员一起参与[应用评测](https://help.aliyun.com/zh/model-studio/evaluate-application/)，确保大模型应用的回答效果符合预期。

### 持续改进

#### **大模型课程**

系统体验的改进优化永远没有终点，您可以考虑学习并通过[阿里云大模型ACA认证](https://edu.aliyun.com/certification/aca13)，该认证配套的免费课程能帮助您进一步了解大模型的能力和应用场景，以及如何优化通过大模型的应用效果。

## 常见问题

### **记录 AI 助理对话日志**

如果您想要记录 AI 助理对话日志并进行分析，您可以参考如下内容在 Appflow 中添加日志节点，将对话内容记录在阿里云日志服务中。

1.  访问[AppFlow控制台](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/manage)，在表格操作列点击**详情**，在详情页面右上角点击**创建新版本**。![2024-10-08\_17-48-33](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p855970.png)
    
2.  在编辑页面阿里云百炼步骤之后，点击**+**添加新的步骤。**行业类型**选择**阿里云**，**公共连接器**选择**SLS日志云服务**。![2024-10-08\_17-51-32](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p855976.png)![2024-10-08\_17-52-43](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p855977.png)
    
3.  选择执行动作**写入日志**，点击**保存，进入下一步**。![2024-10-09\_10-22-08](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856039.png)
    
4.  点击**添加新凭证**。在创建凭证对话框，根据表单填入信息，完成角色创建和授权。创建完成后，选择凭证，并点击**保存，进入下一步**。![2024-10-09\_10-25-29](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856043.png)![2024-10-09\_10-27-29](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856049.png)
    
5.  选择地域、Project 和 Logstore。填入所需的日志信息，左侧输入框是日志Key，直接输入，右侧是日志Value，通过插入变量获取上下文中信息。
    
    1.  如果您已经创建过用于存储 AI 助手日志的阿里云日志服务的Project和Logstore，则可以直接使用，如果没有创建过，可以参考[创建Project和Logstore](https://help.aliyun.com/zh/sls/getting-started#section-2l7-ol2-zro)创建。创建完成后无需接入日志，进入Logstore详情页面，在页面右上角点击开启索引，使用默认的全文索引即可。开启索引后才可以在日志服务进行在线日志查询和分析。![2024-10-09\_10-36-53](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856063.png)![2024-10-09\_10-38-45](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7255448271/p856067.png)
        
    2.  选择地域、Project 和 Logstore。填入所需的日志信息，左侧输入框是日志Key，直接输入，右侧是日志Value，通过插入变量获取上下文中信息。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856069.png)
        
6.  保存并发布连接流版本。![2024-10-09\_11-02-12](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6255448271/p856082.png)
    
7.  进行对话测试，并查看日志。![2024-10-09\_11-35-40](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1868712371/p856122.png)
    

### **如何展示回答引用的文档**

如果您想要在回答中展示引用的文档，可以参考如下步骤操作：

1.  下载[阿里云百炼应用展示文档来源模板.json](https://service-info-public.oss-cn-hangzhou.aliyuncs.com/1563457855438522/dingding-card/template/%E7%99%BE%E7%82%BC%E5%BA%94%E7%94%A8%E5%B1%95%E7%A4%BA%E6%96%87%E6%A1%A3%E6%9D%A5%E6%BA%90%E6%A8%A1%E7%89%88.json)。
    
2.  访问[卡片平台](https://open-dev.dingtalk.com/fe/card)，点击**新建模版**。
    
    ![29](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830244.png)
    
3.  在创建模板输入框，填入模板信息并选择**AI卡片**作为**卡片模版场景**，选择关联先前完成创建的应用后点击**创建**。。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2120582271/p830272.png)
    
4.  导入步骤 1 下载的模板，保存并发布模板。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8160854771/p1061823.png)
    
5.  返回模板列表获取模板 ID。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8160854771/p1061824.png)
    
6.  使用支持展示引用文档的[Appflow工作流模板](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/tl-d58065a5ce5f4de4b71f)创建流。
    

### **支持展示 DeepSeek 深度思考过程**

如果您想要在回答中展示 DeepSeek 深度思考过程，可以参考如下步骤进行配置：

1.  在列表中找到创建的工作流，单击修改
    
2.  找到发送 AI 卡片阶段，填入下面的代码。
    
    ```
    <font color=\"grey-400\"> 思考过程： {{Node2.reasoning}} </font> <br><br> 推理结果： {{Node2.text}}
    ```
    
3.  保存并发布。
