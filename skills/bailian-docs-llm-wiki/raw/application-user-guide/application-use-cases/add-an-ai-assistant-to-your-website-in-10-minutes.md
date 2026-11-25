# 在网站上增加一个AI助手

在阿里云上您可快速为您的网站添加一个可高度自定义的AI 助手，以便全天候（7x24小时）回应客户咨询，提升用户体验、增强业务竞争力。

<a id="方案概览"></a>

<a id="9f090f0e31045"></a>

## 方案概览

![c8ac5d01471a4cda8935c678d9462613](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980978.gif)

在网站中引入一个 AI 助手，只需 4 步：

1.  **创建大模型问答应用**：我们将先通过阿里云百炼创建一个大模型应用，并获取调用大模型应用 API 的相关凭证。
2.  **创建 AI 助手**： 我们将通过 Appflow 创建AI助手，并对其进行配置。
3.  **引入 AI 助手：**接着我们将通过修改几行代码，实现在网站中引入一个 AI 助手。
4.  **增加私有知识：**最后添加私有知识，让 AI 助手准确回答专业问题。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5482562571/p983292.png)

<a id="1-创建大模型问答应用"></a>

<a id="e9e4d5a24buxu"></a>

### 1\. 创建大模型问答应用

首先创建百炼应用，获取大模型推理 API 服务。

> AppFlow 的 AI 助手功能本身不收费，但使用该功能关联的底层资源可能产生费用，包括百炼的模型调用费用、知识库实例运行费用，以及使用函数计算 FC 部署示例网站时产生的费用。各费用项按对应云产品的计费规则收取，具体请参见[模型调用价格](../../model-user-guide/test-1/model-pricing.md)、[知识库计费说明](../agent-billing/billing-for-knowledge-base.md)与[函数计算计费概述](https://help.aliyun.com/zh/functioncompute/billing-overview-of-fc)。[新用户免费额度](../../model-user-guide/test-1/new-free-quota.md)的适用模型、领取条件与有效期以实际规则为准，不能据此认定本教程涉及的全部资源免费。

<a id="1-1-创建应用"></a>

<a id="4f8c2f65a6wpc"></a>

#### 1.1 创建应用

1.  进入百炼控制台的[应用管理](https://bailian.console.aliyun.com/flow-agent/app-center)页面，单击**创建智能体**，在**创建智能体应用**弹窗中输入**应用名称**，其余保持默认，单击**立即创建**，创建完成后自动进入应用配置页面。
    
    > 当前默认创建新版智能体应用（Agent 2.0），本教程后续步骤均已基于新版控制台验证。如需创建旧版应用，可单击弹窗底部的**旧版 Agent 创建入口**。
    
    ![创建智能体应用弹窗](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9108.png)
2.  在应用配置页面的**规划**区域选择模型。默认为**智能模式**（`AUTO`），由平台自动平衡成本与效果，推荐新手使用；也可以单击模型选择器指定具体模型（如`千问-Plus`），单击**更多模型**可选择其他模型。其他参数保持默认。
    
    > 您可在**规划**区域的提示词输入框中设置角色，引导模型应对客户咨询。
    

<a id="code-block"></a>

```text
你叫小助，可以帮助用户解答产品选购、使用等方面的问题。
```

![应用配置页规划区域](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f910e.png)

3.  在页面右侧对话框中提问验证模型效果。不过目前它还无法准确回答您公司的商品信息。单击右上角的**发布**，在**发布版本**窗口中确认版本信息后单击**确认发布**，我们将在后面的步骤中解决这一问题。
    
    ![发布版本弹窗](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f910d.png)

<a id="1-2-获取调用-api-所需的应用id和api-key"></a>

<a id="48d862bea9yrn"></a>

#### 1.2 获取调用 API 所需的应用ID和API Key

为了在后续通过 API 调用大模型应用的能力，需要获取阿里云百炼API Key和应用 ID。

1.  在[应用管理](https://bailian.console.aliyun.com/flow-agent/app-center)页面的应用卡片上查看并复制应用 ID。保存应用 ID 到本地用于后续配置。
    
    ![应用卡片上的应用 ID](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f910f.png)
2.  前往[API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key)页面，单击**创建 API Key**，在弹窗中保持默认配置并单击**确定**。创建成功后立即复制 API Key 并保存到本地，完整密钥仅在创建时显示一次。详细说明请参见[获取与配置 API Key](../../model-api-reference/preparations/get-api-key.md)。
    
    ![API Key 页面](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f910c.png)

<a id="2-创建ai助手"></a>

<a id="9ce1153dd92j7"></a>

### 2\. 创建AI助手

AppFlow 无需代码即可连接网页与模型服务平台。

<a id="2-1-创建ai助手"></a>

<a id="16e7895596rvz"></a>

#### 2.1 创建AI助手

1.  登录[AppFlow控制台](https://appflow.console.aliyun.com/)。
    
2.  在左侧导航栏中选择**模型服务** > **AI助手**。
    
3.  在 AI 助手页面，单击**创建AI助手**设置基本信息。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2115805571/p975439.png)
4.  在创建AI助手页面中，**AI助手类型**选择**智能体Agent**，并自定义AI助手图标、**AI助手名称**和**AI助手描述**。配置完成单击**提交**，跳转至AI助手详情页面。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2115805571/p975441.png)

<a id="2-2-导入并配置您的模型"></a>

<a id="ae84a3861171e"></a>

#### 2.2 导入并配置您的模型

1.  点击 **导入模型** 按钮，选择 **阿里云百炼**作为模型服务平台并点击 **确定**，您也可以根据自身业务需求选择其他平台作为模型服务提供平台。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/3601275771/p1066034.png)
    
2.  在配置向导的**选择连接凭证**步骤中单击下拉框，选择**添加新凭证**。完成创建后，后续可于选择连接凭证中复用该凭证。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p975447.png)
3.  输入凭证名称与先前获取的调用所需的API Key，以便AppFlow进行后续凭证认证。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p976224.png)
4.  单击**下一步**进入**参数配置**步骤，输入先前获取的**应用Id**，**站点选择**保持**公共云国内站**，**业务空间标识（AgentKey）**填写百炼业务空间 ID（可在百炼控制台[业务空间管理](https://bailian.console.aliyun.com/cn-beijing/settings/workspace)页面查看）。单击**保存**，将先前创建的百炼大模型应用与AI助手进行关联。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p976234.png)

<a id="2-3-创建ai助手web页面集成"></a>

<a id="d871505a38sgb"></a>

#### 2.3 创建AI助手Web页面集成

1.  **AI助手详情**页面中点击**集成**并选择**web页面集成**，对页面集成进行创建或配置。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p976654.png)
2.  web页面集成配置页面中点击**创建集成**按钮，输入**集成名称**后点击确定进入详情配置页面。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p976655.png)
3.  对照右方可视化界面，您可针对集成效果进行个性化修改，如字体颜色、背景颜色、嵌入界面大小、头像图标、预置问题等。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980743.png)
4.  完成配置后点击**提交**按钮进行保存。
    

<a id="3-为网站增加-ai-助手"></a>

<a id="fce03efe12i3v"></a>

### 3\. 为网站增加 AI 助手

在网站中增加 AI 助手非常简单，您只需要在网站的 HTML 文件中插入几行代码。

<a id="3-1-搭建示例网站"></a>

<a id="32ffb45d50hz8"></a>

#### 3.1 搭建示例网站

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

> **说明**
>
> 如果首次使用阿里云函数计算服务，需要按照页面引导，授权“AliyunFCServerlessDevsRole”角色所需的权限。

<a id="3-2-增加-ai-助手相关代码"></a>

<a id="b45c1ace092mo"></a>

#### 3.2 增加 AI 助手相关代码

示例代码中包含了被注释的引入 AI 助手代码与说明，您需要找到您的专属悬浮挂件部署脚本代码并粘贴于注释下方。详细操作步骤如下：

1.  回到**AI助手Web集成**页面，在最底部找到**登录配置**，点击**匿名方式**，复制**悬浮挂件部署**脚本。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980779.png)
2.  使用**代码编辑器**将悬浮挂件部署脚本代码粘贴至HTML文件中注释的下方。
    
    若您使用函数计算 FC 一键部署了示例网站，可在**环境详情**页底部点击函数名称进入函数详情。在代码编辑器中切换至 `index.html`，根据文件内的注释提示，将悬浮挂件部署脚本粘贴到指定位置。
    
    您也可以根据注释说明，选择是否启用 AI 助手的图标拖拽功能。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5482562571/p985886.png)
3.  重新运行HTML文件或代码视图中的**部署代码**按钮并重新访问域名，即可看到增加了AI助手的网页效果。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5482562571/p985889.png)

<a id="3-3-验证网站上的-ai-助手"></a>

<a id="80d3029cb9q06"></a>

#### 3.3 验证网站上的 AI 助手

现在，您可以重新访问示例网站页面以查看最新效果。此时您会发现网站的右下角出现了 AI 助手图标![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980795.png)，点击即可唤起 AI 助手。

> 本方案提供的网站为示例网站，网站本身细节内容仅展示样式，效果如下图。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980799.png)

<a id="常见问题"></a>

<a id="h2-faq-request-error"></a>

## 常见问题

<a id="嵌入-ai-助手后出现-request-error-怎么办"></a>

<a id="h3-request-error"></a>

### 嵌入 AI 助手后出现 request error 怎么办？

网站嵌入 AI 助手后，如果对话出现 request error，按以下步骤排查：

1.  **检查 API Key 是否可用**：在 `AppFlow` 控制台 AI 助手详情页，点击已导入模型旁的编辑图标，在**选择连接凭证**步骤中查看 API Key，前往百炼控制台 [API Key](https://bailian.console.aliyun.com/cn-beijing/model/settings/api-key) 页面确认状态。
2.  **确认智能体与 API Key 在同一业务空间**：在**参数配置**步骤中检查**业务空间标识（`AgentKey`）**。智能体与 API Key 分属不同业务空间会导致鉴权失败。
3.  **核实应用 Id 是否正确**：在**参数配置**步骤中确认**应用 Id**字段值，前往百炼[应用管理](https://bailian.console.aliyun.com/flow-agent/app-center)页面的应用卡片上对比核实。

以上三项均正确配置后，AI 助手可正常对话。

<a id="4-为-ai-助手增加私有知识"></a>

<a id="bdc1ba5739qp6"></a>

### 4\. 为 AI 助手增加私有知识

通过前面的步骤，您已经拥有了一个可以和客户对话的 AI 助手。但是，如果想让 AI 助手像公司员工一样，更加精准且专业地回答与商品相关的问题，我们还需要为大模型应用配置知识库。

假设您在一家售卖智能手机的公司工作。您的网站上会有很多与智能手机相关的信息，如支持双卡双待、屏幕、电池容量、内存等信息。不同机型的详细配置清单参考：[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20240701/geijms/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)。

<a id="4-1-配置知识库"></a>

<a id="f3ccbb6a53e4b"></a>

#### 4.1 配置知识库

接下来，我们可以尝试让大模型在面对客户问题时参考这份文档，以产出一个更准确的回答和建议。

1.  **创建知识库：**进入百炼控制台，在左侧导航栏选择**数据接入** > **知识管理**，进入[知识管理](https://bailian.console.aliyun.com/cn-beijing/rag/knowledge/list)页面，单击**创建**。填写**名称**和**描述**，知识库类型选择**文档搜索**，使用场景选择**基础文档问答**，单击**下一步**。
    
    ![知识管理列表与创建入口](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9103.png)
2.  **上传文件：**数据来源选择**上传文件**，根据引导上传我们虚构的阿里云百炼系列手机产品介绍，**索引设置**保持默认，单击**创建知识库**。系统将自动完成解析、切片、向量化与索引构建，知识库状态变为**已就绪**后即可用于检索。
    
    > 根据您上传的文档大小，阿里云百炼需要一定时间解析，通常占用1~6分钟，请您耐心等待。
    
3.  **创建并发布知识检索服务：**新版智能体应用通过关联**知识检索服务**使用知识库。在左侧导航栏选择**知识服务** > **知识检索**，进入[知识检索](https://bailian.console.aliyun.com/cn-beijing/rag/retrieval/list)页面，单击**创建**，填写**服务名称**后单击**确认**。在配置页面单击**\+ 添加**绑定刚才创建的知识库，然后单击右上角**发布**。发布后该检索服务才可被应用关联。
    
    ![知识检索服务列表与创建入口](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9102.png)
4.  **引用知识：**访问[应用管理](https://bailian.console.aliyun.com/flow-agent/app-center)页面，找到之前创建的应用，单击**配置**进入应用配置页面。在**知识库**区域的**检索策略**中单击**立即配置**，在**配置检索服务**面板中选择已发布的检索服务并单击**关联**。在右侧对话框中测试验证符合预期后，单击右上角**发布**并**确认发布**。
    
    ![应用配置页知识库检索策略区域](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9101.png) ![配置检索服务面板](https://g-adoc.alcasset.com/media/maas_docs/sfm-cn/common/images/6a4b3c2d1e0f9100.png)

<a id="4-2-检验效果"></a>

<a id="221e51e470e4u"></a>

#### 4.2 检验效果

有了参考知识，AI 助手就能准确回答关于您公司的商品的问题了。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4742151571/p980819.png)

<a id="总结"></a>

<a id="2ef9cb54c8ml8"></a>

## 总结

通过前面的学习，您已搭建大模型 RAG 应用并部署到网站，以应对客户咨询。实际费用取决于使用的模型及底层资源，具体请参见前文的计费说明。

<a id="应用评测"></a>

<a id="012a3cbc50fpn"></a>

### 应用评测

建议在正式上线 AI 助手前，组织业务人员一起参与[人工评测](../agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)，确保大模型应用的回答效果符合预期。如果不符合预期，可以通过[优化提示词](../../model-user-guide/use-cases/prompt-engineering-guide.md)、完善补充私有知识、调整文档切分策略等方法来改进回答效果。

<a id="持续改进"></a>

<a id="f978b19e7dwyg"></a>

### 持续改进

<a id="大模型课程"></a>

<a id="6b40f0f011n3v"></a>

#### 大模型课程

系统体验的改进优化永远没有终点，您可以考虑学习并通过[阿里云大模型 ACA 认证](https://edu.aliyun.com/certification/aca13)，该认证配套的免费课程能帮助您进一步了解大模型的能力和应用场景，以及如何优化大模型的应用效果。

<a id="常见问题-2"></a>

<a id="b5e8c3d7f1a2m"></a>

## 常见问题

<a id="ai-助手报错-failed-to-stream-content"></a>

<a id="d8e0f5a7b3c4p"></a>

### AI 助手报错"Failed to stream content"

**问题现象**

在网站中嵌入 AI 助手后，用户与 AI 助手对话时出现"Failed to stream content"错误。

**可能原因**

该错误通常是由于前端代码中的请求地址配置不正确导致的。例如，在定制前端组件时，直接复制了示例代码中的默认请求地址（如`/chat`），但未将其替换为实际的后端服务地址。

**解决方案**

1.  检查前端代码中的请求地址配置，确认是否已将默认地址替换为您实际的后端服务地址。
2.  如果您使用了 AppFlow 的悬浮挂件部署脚本，请确保脚本代码来自您自己的 AI 助手 Web 集成页面，而不是其他来源的示例代码。
3.  确认 AI 助手的模型配置正确，包括 API Key 和应用 ID 是否填写正确。
4.  使用浏览器开发者工具（F12）检查控制台和网络请求，查看具体的错误信息和请求地址，排查请求是否发送到了正确的后端服务。
