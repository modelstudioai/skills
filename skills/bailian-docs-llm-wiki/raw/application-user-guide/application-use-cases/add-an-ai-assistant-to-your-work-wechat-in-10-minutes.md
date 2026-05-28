# 10分钟在企业微信中集成一个 AI 助手

在阿里云上，您只需 10 分钟，无需任何编码，即可为您的组织在企业微信上集成一个有大模型能力加成的 AI 助手。这个助手可以全天候（7x24）响应用户咨询，还能解答私域问题，成为您企业的专属助手，提升用户体验，增强业务竞争力。

## **方案概览**

在企业微信中集成一个 AI 助手，只需几步：

1.  **创建大模型问答应用**：通过阿里云百炼创建一个大模型应用，并获取调用大模型应用 API 的相关凭证。
    
2.  **创建企业微信应用**：创建一个企业微信应用，为您的企业微信组织提供问答服务。
    
3.  **创建企业微信连接流：**基于阿里云的 AppFlow 服务，在无需编写代码的情况下，完成企业微信应用和阿里云百炼 RAG 应用的关联，最终实现用户在企业微信聊天中和 RAG 应用对话。
    
4.  **配置企业微信应用**：为企业微信应用配置接收消息，即可在聊天中回答用户问题。
    
5.  **为大模型问答应用增加私有知识：**开启知识检索增强（RAG），为大模型问答应用增加知识库，让 AI 机器人能回答私有领域的问题，帮助您更好地应对用户咨询。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4005080371/p833943.png)

![b681241d-ee05-4416-a3f9-52bca113ff81](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7752553271/p834112.gif)

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
    

## **2\. 创建企业微信应用**

接下来您需要在您的组织中创建应用，作为 AI 助手回答用户问题。

### **2.1 创建应用**

1.  访问[企业微信开发者中心](https://developer.work.weixin.qq.com/login)，扫码登录，点击**立即创建**。根据指引选择**以企业身份创建**和**企业内部应用**。![2024-08-12\_16-48-56](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7752553271/p833961.png)
    
2.  在顶部导航栏中，选择**应用管理**，在**应用**页面下半部分点击**创建应用**。![2024-08-12\_17-50-42](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7752553271/p834042.png)
    
3.  在**创建应用**页面，填写**应用名称**和**应用介绍**，上传应用 logo，选择可见范围，完成后点击**创建应用**。![2024-08-12\_17-53-01](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4648953271/p834043.png)
    

### **2.2 获取**企业 ID**、应用** AgentId **和 Secret**

1.  在应用详情页面，复制 AgentID和 Secret，用于下一步创建连接流。
    
    ![2024-08-12\_17-56-23](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4648953271/p834048.png)
    
2.  在顶部导航栏中，选择**我的企业**，在**企业信息**页面，复制企业 ID，用于下一步创建连接流。![2024-08-12\_18-04-56](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4648953271/p834054.png)
    

## 3\. 创建企业微信连接流

AppFlow 可以让您在不写代码的情况下，通过界面配置就可以将阿里云百炼 RAG 应用和企业微信连接起来。您可以通过预置的 AppFlow 模板创建一个企业微信连接流。

1.  使用[AppFlow模板](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/fastTemplate/tl-qiyeweixinself0813shzoa?from=solution)创建连接流，点击**立即使用**进入创建流程。![2024-08-13\_16-22-35](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4648953271/p834553.png)
    
2.  在企业微信的**账户授权**配置向导页，点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6252853471/p935918.png)按钮，再点击**添加新凭证**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8677115371/p884244.png)
    
3.  在**创建凭证**对话框中，设置一个自定义凭证名称，填入之前获取的企业微信的企业ID、应用 AgentId 和 Secret。保存AppFlow生成的 Token 和 EncodingAESKey到本地（[4.1 配置API接收消息](#d6e2ae9678564)时需要填写）、保存IP白名单到本地（在[4.2 配置企业可信IP](#9bbf4aacacund)时需要填写）。点击**下一步**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3916131471/p924261.png)
    
4.  点击**保存**，完成配置。
    
5.  在阿里云百炼的**账户授权**配置向导页，点击![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6252853471/p935919.png)按钮，再点击**添加新凭证**。在**创建凭证**对话框中，设置一个自定义凭证名称，并填入之前获取的 API-KEY。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8677115371/p884505.png)
    
6.  在**执行动作**配置向导页，填写**应用Id**，**应用Id**可以[在阿里云百炼控制台应用管理](https://bailian.console.aliyun.com/#/app-center)获取，完成后点击**下一步**。![2024-08-13\_18-06-24](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4648953271/p834563.png)
    
7.  在**基本信息**配置向导页，填写**连接流名称**和**连接流描述**（建议保持默认），完成后点击**下一步**。
    
8.  界面提示流程配置成功，复制并保存 **WebhookUrl**（[4.1 配置API接收消息](#d6e2ae9678564)时需要填写），点击**发布**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8677115371/p883865.png)
    

## 4\. 配置企业微信应用

有了 Webhook 地址后，接下来您可以在企业微信应用中配置接收消息来回答用户问题了。

### 4.1 配置API接收消息

1.  访问[企业微信应用列表](https://work.weixin.qq.com/wework_admin/frame#apps)。找到刚刚创建的应用，点击应用名称进入详情页面。
    
2.  在应用详情页面，找到接收消息卡片，点击**设置API接收**。![2024-08-12\_17-54-59](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4648953271/p834066.png)
    
3.  在**API接收消息**页面，您可以参考下图完成配置，然后点击**保存**。
    
    ![2024-08-12\_18-06-33](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4648953271/p834067.png)
    
    -   **URL**填入上一步复制的 **WebhookUrl**。
        
        如果之前未保存WebhookUrl，可访问[AppFlow连接流](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/manage)页面，在**操作**列点击**webhookUrl**进行查看。
        
    -   **Token** 和 **EncodingAESKey** 填入上一步复制的值。
        
        如果之前未保存，可访问[AppFlow连接凭证](https://appflow.console.aliyun.com/vendor/cn-hangzhou/connector/user/auth/manage)页面，在**公共连接器** > **企业微信**中，找到刚刚配置的凭证，点击**操作**列的**编辑**从凭证中获取。
        
    
    > 如果域名主体校验未通过，请参考[域名主体校验未通过怎么办？](#b33565bed3d8w)进行处理。
    

### **4.2 配置企业可信IP**

1.  在应用详情页面，在页面下方开发者接口找到**企业可信IP**卡片，点击**配置**。![2024-08-12\_22-13-09](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7752553271/p834113.png)
    
2.  在企业可信IP对话框，粘贴复制的 IP 地址，然后点击**确定**。
    

### 4.3 测试应用

你可以在企业微信中搜索应用并发送消息，查看效果。

1.  在企业微信顶部搜索框搜索应用名称，点击应用进入聊天。![2024-08-12\_22-23-04](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4648953271/p834109.png)
    
2.  与应用对话，进行交流互动。![2024-08-12\_22-23-58](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7752553271/p834110.png)
    

## 5\. 为大模型问答应用增加私有知识

### **5.1 配置知识库**

接下来，我们可以尝试让大模型在面对客户问题时参考这份文档，以产出一个更准确的回答和建议。

假设您在一家售卖智能手机的公司工作。您的企业微信用户会有很多涉及智能手机相关的问题，如支持双卡双待、屏幕、电池容量、内存等信息。不同机型的详细配置清单参考：[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240701/geijms/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)。

1.  **上传文件：**在阿里云百炼控制台的[文件](https://bailian.console.aliyun.com/?tab=app#/data-center?dataType=0)页签中点击**导入数据**，根据引导上传我们虚构的百炼系列手机产品介绍：
    
    > 根据您上传的文档大小，百炼需要一定时间解析，通常占用1~6分钟，请您耐心等待。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5603325471/p944474.png)
    
2.  **创建知识库：**进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面，点击**立即开通并创建**（首次使用）或**创建知识库**。选择**创建**标准版，填写**知识库名称**，其余设置可保持默认，点击**下一步**，选择刚才上传的文档，其他参数保持默认即可。后续大模型回答时可以检索参考知识库中的文档。
    
    > 选择向量存储类型时，如果您希望集中存储、灵活管理多个应用的向量数据，可选择**ADB-PG**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5301724671/p944483.png)
    
3.  **引用知识：**完成知识库的创建后，可以返回[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)进入到刚才创建的应用配置界面，打开**知识库**开关、单击**+知识库**选择目标知识库，测试验证符合预期后点击**发布**。Prompt 中会被自动添加一段信息，以便大模型在后续回答时参考检索出来的信息。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9805168571/p944485.png)
    

### **5.2 检验效果**

有了参考知识，AI 应用就能准确回答您关于阿里云百炼手机的问题了。![2024-08-12\_22-24-56](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7752553271/p834111.png)

## 总结

通过前面的学习，您已经能搭建一个大模型 RAG 应用，并且将其以应用的形式添加到企业微信中来应对客户咨询，过程仅需 0 元（免费试用额度内）10分钟。

### **应用评测**

建议您在正式上线 AI 应用前，组织业务人员一起参与[应用评测](https://help.aliyun.com/zh/model-studio/evaluate-application/)，确保大模型应用的回答效果符合预期。如果不符合预期，可以通过[优化提示词](https://edu.aliyun.com/course/3126500/lesson/342551535)、完善补充私有知识、调整文档切分策略等方法来改进回答效果。

### 持续改进

#### **大模型课程**

系统体验的改进优化永远没有终点，您可以考虑学习并通过[阿里云大模型ACA认证](https://edu.aliyun.com/certification/aca13)，该认证配套的免费课程能帮助您进一步了解大模型的能力和应用场景，以及如何优化通过大模型的应用效果。

## **常见问题**

### **域名主体校验未通过怎么办？**

当您在企业微信后台配置 API 接收消息时，报错提示“域名主体校验未通过，需配置备案主体与当前企业主体相同或有关联关系的域名”。这通常是由于企业微信的相关限制所引起的。为解决此问题，您需要配置一个企业自有域名。

-   如果您的域名已在阿里云备案，您可以参考如下步骤创建一个二级域名作为企业自有域名。
    
    1.  访问[AppFlow域名管理](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/domain/manage)页面，单击**添加域名**按钮，进入**添加域名**页面，填入可用的二级域名，如`airobot.example.com`。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6628845571/p979298.png)
        
    2.  参考[CNAME 记录](https://help.aliyun.com/zh/dns/add-a-dns-record#a11de0e439vrv)，将该二级域名解析到上一步的**记录值**。
        
    3.  解析配置完成后，返回**添加域名**页面，点击**提交**。
        
    4.  使用该二级域名替换[API接收消息](#d6e2ae9678564)的URL（即已经填写的WebhookUrl）中的主机名。
        
-   如果您的域名没有在阿里云备案，您可以参考如下步骤，将API接收消息中的URL配置为您的企业自有域名，并在企业自有域名对外提供服务的Nginx上配置转发规则，将请求转发到连接流的WebhookUrl。
    
    1.  在AppFlow的[连接凭证](https://appflow.console.aliyun.com/vendor/cn-hangzhou/connector/user/auth/manage)页面编辑企业微信的连接凭证。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5577115371/p893881.png)
        
    2.  点击**下一步**，勾选**内网代理**。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5577115371/p893391.png)
        
    3.  首次勾选**内网代理**时，会弹出AppFlow服务关联角色授权创建页面，请您确认并授权。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5577115371/p893399.png)
        
    4.  配置可信域名。
        
        ## 使用计算巢Nginx代理
        
        如果您没有在阿里云备案的可信主体域名，同时也没有Nginx代理，可以通过点击**部署Nginx代理实例**一键自动为您部署并配置Nginx代理。按控制台提示直接确认订单或更改您期望的配置下单，等待部署完成即可。部署过程通常耗时1-3分钟，请刷新列表并耐心等待。
        
        部署完成后，点击下拉框选择计算巢实例，用计算巢实例Host替换[API接收消息](#d6e2ae9678564)的URL（即已经填写的WebhookUrl）中的主机名，复制IP白名单并添加到[企业可信IP](#9bbf4aacacund)中，点击**保存**，完成配置。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5577115371/p893430.png)
        
        ## 使用自有的Nginx代理
        
        使用您自有的Nginx进行代理，同时也需要一台ECS或托管实例进行消息转发。
        
        1.  选择ECS实例或托管实例，并将IP白名单添加到[企业可信IP](#9bbf4aacacund)中。
            
        2.  如果您没有实例，可单击**新增实例**前往ECS购买页新购ECS，或者创建托管实例。
            
            > 托管实例需要您在非阿里云服务器中找一台可以访问公网的机器，再按照[阿里云托管实例](https://help.aliyun.com/zh/ecs/user-guide/manage-servers-that-are-not-provided-by-alibaba-cloud)安装云助手。
            
        3.  点击**保存**，完成配置。
            
        4.  使用Nginx的IP地址替换[API接收消息](#d6e2ae9678564)的URL（即已经填写的WebhookUrl）中的主机名。
            
        

### 配置企业可信 IP 时，报错“以下IP属于第三方服务商，为保证企业数据安全，请配置本企业服务器的IP”？

报错原因：企业微信出于安全考虑，调用通讯录、身份校验接口时需要校验可信域名和可信 IP，其中一个可信 IP 仅能用于企业微信中的一个企业，如果用于多个企业将被认定为服务商，从而导致通讯录、身份校验等接口不可用。

如果您有阿里云的云服务器 ECS，您可以使用阿里云服务器进行请求转发，解决可信 IP 的问题：

1.  修改 AppFlow 中配置的企业微信的连接凭证。![2024-09-04\_14-19-00](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5111255271/p844476.png)
    
2.  修改内容：在**内网代理配置**页面选择**使用可信主体域名** > **ECS实例**或**使用自有Nginx代理** > **ECS实例**，选择对应地域和实例， 点击保存。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5577115371/p884603.png)
    
3.  将代理机器的 IP 添加到企业微信可信 IP。访问[企业微信应用列表](https://work.weixin.qq.com/wework_admin/frame#apps)，进入应用详情页面，在页面下方开发者接口找到**企业可信IP**卡片，点击**配置**。
    

如果您有自己的非阿里云的机器，您可以将自有机器托管到阿里云，并使用托管机器进行请求转发，解决可信 IP 的问题：

1.  在您的非阿里云服务器中找一台可以访问公网的机器，按照[文档](https://help.aliyun.com/zh/ecs/user-guide/manage-servers-that-are-not-provided-by-alibaba-cloud)安装云助手 。
    
2.  修改 AppFlow 中配置的企业微信的连接凭证。![2024-09-04\_14-19-00](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5111255271/p844476.png)
    
3.  修改内容：在**内网代理配置**页面选择**使用可信主体域名** > **ECS实例**或**使用自有Nginx代理** > **ECS实例**，选择对应托管地域和托管实例， 点击**保存**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5577115371/p884602.png)
    

4\. 将代理机器的 IP 添加到企业微信可信 IP。访问[企业微信应用列表](https://work.weixin.qq.com/wework_admin/frame#apps)，进入应用详情页面，在页面下方开发者接口找到**企业可信IP**卡片，点击**配置**。

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
    

### **如何查看连接流的WebhookUrl？**

1.  访问[AppFlow控制台的连接流](https://appflow.console.aliyun.com/vendor/cn-hangzhou/flow/manage)页面。
    
2.  在**操作**列点击**webhookUrl**进行查看。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8677115371/p883573.png)
