# 在网站上增加一个AI助手

在阿里云上您可快速为您的网站添加一个可高度自定义的AI 助手，以便全天候（7x24小时）回应客户咨询，提升用户体验、增强业务竞争力。

## **方案概览**

![c8ac5d01471a4cda8935c678d9462613](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980978.gif)

在网站中引入一个 AI 助手，只需 4 步：

1.  **创建大模型问答应用**：我们将先通过阿里云百炼创建一个大模型应用，并获取调用大模型应用 API 的相关凭证。
    
2.  **创建 AI 助手**： 我们将通过 Appflow 创建AI助手，并对其进行配置。
    
3.  **引入 AI 助手：**接着我们将通过修改几行代码，实现在网站中引入一个 AI 助手。
    
4.  **增加私有知识：**最后添加私有知识，让 AI 助手准确回答专业问题。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5482562571/p983292.png)

### **1\. 创建大模型问答应用**

首先创建百炼应用，获取大模型推理 API 服务。

> 阿里云百炼提供的[新用户免费额度](https://help.aliyun.com/zh/model-studio/new-free-quota)可以完全覆盖本教程所需资源消耗。额度消耗完后按 token 计费，相比自行部署大模型可以显著降低初期投入成本。

#### **1.1 创建应用**

1.  进入百炼控制台的[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)页面**，**点击右上角**创建应用**，选择**智能体应用**并输入应用名称，其余参数保持默认，点击**立即创建**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1601275771/p1066018.png)
    
2.  在**应用配置**页面，选择**更多模型**；模型选择**Qwen3.5-Plus**。该模型能力均衡，推理效果、成本和速度介于千问Max和千问Flash之间，适合本场景中的任务需求。其他参数保持默认。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3601275771/p1066019.png)
    
    > 您可输入Prompt设置角色，引导模型应对客户咨询。
    
    ```
    你叫小助，可以帮助用户解答产品选购、使用等方面的问题。
    ```
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3601275771/p1066021.png)
    
3.  在页面右侧可以提问验证模型效果。不过目前它还无法准确回答您公司的商品信息。点击右上角的**发布**，我们将在后面的步骤中去解决这一问题。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5082715571/p996997.png)
    

#### **1.2 获取调用 API 所需的应用ID和API Key**

为了在后续通过 API 调用大模型应用的能力，需要获取阿里云百炼API Key和应用 ID。

1.  在[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)中可以查看所有百炼应用 ID。保存应用 ID 到本地用于后续配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2115805571/p959107.png)
    
2.  前往[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)页面，点击**创建API Key**，在弹出窗口中创建一个新 API-Key。保存 API-Key 到本地用于后续配置。
    

### **2\. 创建AI助手**

AppFlow 无需代码即可连接网页与模型服务平台。

#### 2.1 创建AI助手

1.  登录[AppFlow控制台](https://appflow.console.aliyun.com/)。
    
2.  在左侧导航栏中选择**模型服务** > **AI助手**。
    
3.  在 AI 助手页面，单击**创建AI助手**设置基本信息。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2115805571/p975439.png)
    
4.  在创建AI助手页面中可以自定义您的AI助手图标和名称。配置完成单击**提交**，跳转至AI助手详情页面。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2115805571/p975441.png)
    

#### 2.2 导入并配置您的模型

1.  点击 **导入模型** 按钮，选择 **阿里云百炼** 作为模型服务平台并点击 **确定**，您也可以根据自身业务需求选择其他平台作为模型服务提供平台。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3601275771/p1066034.png)
    
2.  于配置界面中选择连接凭证选项下点击 **添加新凭证** 按钮。完成创建后，后续可于选择连接凭证选项中复用自身业务凭证。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p975447.png)
    
3.  输入凭证名称与先前获取的调用所需的API Key，以便AppFlow进行后续凭证认证。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p976224.png)
    
4.  输入先前获取的调用所需的应用ID后点击确定，将先前创建的百炼大模型应用与AI助手进行关联。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p976234.png)
    

#### **2.3 创建AI助手Web页面集成**

1.  **AI助手详情**页面中点击**集成**并选择**web页面集成**，对页面集成进行创建或配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p976654.png)
    
2.  web页面集成配置页面中点击**创建集成**按钮，输入**集成名称**后点击确定进入详情配置页面。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p976655.png)
    
3.  对照右方可视化界面，您可针对集成效果进行个性化修改，如字体颜色、背景颜色、嵌入界面大小、头像图标、预置问题等。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980743.png)
    
4.  完成配置后点击**提交**按钮进行保存。
    

### **3\. 为网站增加 AI 助手**

在网站中增加 AI 助手非常简单，您只需要在网站的 HTML 文件中插入几行代码。

#### **3.1 搭建示例网站**

在让 AI 助手能准确回答问题之前，我们可以先尝试快速将 AI 助手集成到网站中。

为了能够快速体验 AI 助手的嵌入效果，我们提供了一份简单的 HTML 模板，您只需下载并用浏览器打开即可本地预览，适用于临时模拟企业官网或其他页面。详细步骤如下：

1.  下载HTML文件：[index.html](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250703/wzbals/index.html)。
    
2.  使用浏览器运行HTML文件或双击打开HTML文件即可查看未嵌入AI助手的示例网站效果。
    

若您希望搭建一个更完整的示例网站（包括临时访问域名等），我们也提供了基于函数计算 FC 的一键部署模板。通过此方式，您无需手动配置环境，即可体验一个具备 AI 助手能力的可访问网站。详细步骤如下：

1.  请点击[这里](https://fcnext.console.aliyun.com/applications/create?template=web-page-deploy)打开我们提供的函数计算应用模板。
    
    > 首次使用，需要按照引导开通函数计算服务。
    
2.  选择**直接部署**。
    
3.  其他表单项保持默认，点击页面左下角的**创建并部署默认环境**，等待项目部署完成即可（预计耗时 1 分钟）。
    
4.  应用部署完成后，您可以在应用详情的**环境信息**中找到示例网站的访问域名，点击即可查看，确认示例网站已经部署成功。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5482562571/p985864.png)
    

**说明**

如果首次使用阿里云函数计算服务，需要按照页面引导，授权“AliyunFCServerlessDevsRole”角色所需的权限。

#### **3.2 增加 AI 助手相关代码**

示例代码中包含了被注释的引入 AI 助手代码与说明，您需要找到您的专属悬浮挂件部署脚本代码并粘贴于注释下方。详细操作步骤如下：

1.  回到**AI助手Web集成**页面，在最底部找到**登录配置**，点击**匿名方式**，复制**悬浮挂件部署**脚本。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980779.png)
    
2.  使用**代码编辑器**将悬浮挂件部署脚本代码粘贴至HTML文件中注释的下方。
    
    若您使用函数计算 FC 一键部署了示例网站，可在**环境详情**页底部点击函数名称进入函数详情。在代码编辑器中切换至 `index.html`，根据文件内的注释提示，将悬浮挂件部署脚本粘贴到指定位置。
    
    您也可以根据注释说明，选择是否启用 AI 助手的图标拖拽功能。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5482562571/p985886.png)
    
3.  重新运行HTML文件或代码视图中的**部署代码**按钮并重新访问域名，即可看到增加了AI助手的网页效果。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5482562571/p985889.png)
    

#### **3.3 验证网站上的 AI 助手**

现在，您可以重新访问示例网站页面以查看最新效果。此时您会发现网站的右下角出现了 AI 助手图标![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980795.png)，点击即可唤起 AI 助手。

> 本方案提供的网站为示例网站，网站本身细节内容仅展示样式，效果如下图。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980799.png)

### **4\. 为 AI 助手增加私有知识**

通过前面的步骤，您已经拥有了一个可以和客户对话的 AI 助手。但是，如果想让 AI 助手像公司员工一样，更加精准且专业地回答与商品相关的问题，我们还需要为大模型应用配置知识库。

假设您在一家售卖智能手机的公司工作。您的网站上会有很多与智能手机相关的信息，如支持双卡双待、屏幕、电池容量、内存等信息。不同机型的详细配置清单参考：[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240701/geijms/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)。

#### **4.1 配置知识库**

接下来，我们可以尝试让大模型在面对客户问题时参考这份文档，以产出一个更准确的回答和建议。

1.  **数据连接：**进入阿里云百炼控制台的[数据连接](https://bailian.console.aliyun.com/cn-beijing?tab=app#/connector/list)页签，点击**默认文件连接器**的**详情**按钮。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9501275771/p1066004.png)
    
2.  **上传文件：**在连接器详情的右上角点击**导入数据**，根据引导上传我们虚构的阿里云百炼系列手机产品介绍：
    
    > 根据您上传的文档大小，阿里云百炼需要一定时间解析，通常占用1~6分钟，请您耐心等待。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0601275771/p1066012.png)
    
3.  **创建知识库：**进入[知识库](https://bailian.console.aliyun.com/?tab=app#/knowledge-base)页面，点击**立即开通并创建**（首次使用）或**创建知识库**。选择**创建**标准版，填写**知识库名称**及**知识库描述**，其余设置可保持默认，点击**下一步**，选择刚才上传的文档，其他参数及**索引设置**保持默认即可。后续大模型回答时可以检索参考知识库中的文档。
    
    > 选择向量存储类型时，如果您希望集中存储、灵活管理多个应用的向量数据，可选择**ADB-PG**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5301724671/p944483.png)
    
4.  **引用知识：**完成知识库的创建后，访问[应用管理](https://bailian.console.aliyun.com/?&tab=app#/app-center)页面，选择之前创建的应用。**文档**中添加目标知识库，调用方式选择**必定调用**。测试验证符合预期后点击**发布**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0601275771/p1066026.png)
    

#### **4.2 检验效果**

有了参考知识，AI 助手就能准确回答关于您公司的商品的问题了。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980819.png)

## 总结

通过前面的学习，您已在 10 分钟内免费搭建大模型 RAG 应用并部署到网站，以应对客户咨询。

### **应用评测**

建议在正式上线 AI 助手前，组织业务人员一起参与[人工评测](https://help.aliyun.com/zh/model-studio/evaluate-manual-application)，确保大模型应用的回答效果符合预期。如果不符合预期，可以通过[优化提示词](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide)、完善补充私有知识、调整文档切分策略等方法来改进回答效果。

### 持续改进

#### **大模型课程**

系统体验的改进优化永远没有终点，您可以考虑学习并通过[阿里云大模型 ACA 认证](https://edu.aliyun.com/certification/aca13)，该认证配套的免费课程能帮助您进一步了解大模型的能力和应用场景，以及如何优化大模型的应用效果。
