# 应用观测

[阿里云百炼应用](https://help.aliyun.com/zh/model-studio/application-introduction)内部的多[节点](#0806932be6woi)架构为后续开发带来诸多挑战，例如：

-   追踪应用内部调用链路
    
-   查看模型响应延时
    
-   查看模型思考过程
    

通过[应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)功能，您可端到端查看业务空间内阿里云百炼应用的处理流程（如向量生成、向量检索和大模型调用）并获取延时、Token量等指标（更新频率为分钟级）。

> 应用观测目前暂无API。

## **效果示例**

**追踪应用内部的调用过程**

**查看模型的响应延时**

**查看模型的思考过程**

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7483579271/p862864.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7483579271/p862866.png)

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/4549379271/p862643.png)

## 支持的应用

[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)、[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)和[高代码应用](https://help.aliyun.com/zh/model-studio/rich-code-application/)。

> 应用观测目前暂不支持[通过Assistant API创建的智能体应用](https://help.aliyun.com/zh/model-studio/user-guide/what-is-assistant-api)。

## 开始使用

### **前提条件**

首次使用应用观测时，请单击应用观测页面右上角的**应用观测配置**，根据指引完成以下步骤：

1.  授权可观测链路OpenTelemetry服务角色权限。
    
2.  开通可观测链路OpenTelemetry服务。
    
3.  初始化可观测链路OpenTelemetry存储LogStore。
    

> 请使用[主账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)操作，开通后通常分钟级生效，但高峰期可能会稍有延迟。

> 如需使用[子账号](https://help.aliyun.com/zh/model-studio/permission-management-overview#24ca2dad7djzs)开通，需主账号为该子账号[配置必要权限](#7c0706567bkz9)。

### **使用方法**

#### **1\. 选择被观测的应用**

访问[应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)，单击**选择被观测的应用** > **添加**。如果列表中没有您已创建的应用，可能是因为：

-   该应用尚未发布**。**
    
    > 您可以单击**管理应用**，在列表中找到您想要发布的应用后，单击**管理** > **发布**。
    
-   该应用不属于当前业务空间。
    

#### **2\. 开始观测**

1.  添加完成后，被观测的应用将出现在[应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)列表中。所有在该应用中输入的Prompt及其相应的数据和指标将被自动追踪，并同步至应用观测（频率为分钟级）。
    
    > 单击**关闭观测**后，应用的追踪数据将停止同步。重新添加后仅同步新增数据。
    
    > **应用总量**、**应用平均延时**等指标能帮助您优化应用的运营效果和成本。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5023997471/p938387.png)
    

2.  单击**操作**列的**查看详情**，查看过往（最长可选30天）所有在该应用中输入的Prompt的内容、**输出**、**延时**、**调用时间**以及**Token量**（说明参见[附录](#f0ed9407canlv)）等概要信息。
    
    > **互动式体验**：列表中的**[CHAIN](#0806932be6woi)**节点表示一次完整的应用内部调用追踪，支持展开。查看[应用观测支持的所有节点类型](#0806932be6woi)。
    
    > **状态**：包括**正常**和**错误**。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1532430771/p1051566.png)
    
    支持基于**Request ID**、**Trace ID**或**Span ID**进行搜索，以及指定时间范围进行筛选。
    
    **如何获取 ID**：单击指定节点的名称即**名称**列内容（如AgentApp），展开**节点详情**后，再单击**查看 ID**，可查看Request ID、Trace ID和Span ID。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1532430771/p1051562.png)
    
    **表头设置**：单击列表右上角的表头编辑按钮，可以自定义显示的字段列。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0133430771/p1053005.png)
    

3.  单击指定[节点](#0806932be6woi)的**名称**，即可查看**详情**、**原始数据**、**标注记录**等信息（如有下属节点，支持展开）。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1532430771/p1051582.png)
    

#### **3\. 导出数据**

在应用详情页的 Trace 列表页签右上角，单击**导出数据**，可将当前筛选条件下的数据导出（JSONL 或 EXCEL 格式）。

#### **4\. 查看监控统计**

在应用详情页，单击**监控统计**页签，可查看该应用的性能监控数据，包括：

-   **调用次数**：应用调用次数趋势图。
    
    -   **失败次数**和**失败率**：应用调用失败统计。
        
    -   **Token总量**：全部、输入和输出Token总量趋势图。
        
    -   **平均单次请求Token量**：每次请求的平均输入和输出Token量。
        
    -   **平均首Token耗时**：流式调用场景下的首Token响应时间。
        
    -   **平均调用时长**：应用调用的平均延时。
        

支持按时间范围（最长30天）和聚合粒度（按分钟、按小时、按天）查看数据。每个图表支持放大、下载和复制操作。

### **添加到评测集**

应用观测支持将Span数据直接添加到评测集，用于后续的应用评测。通过此功能，您可以将真实的线上调用数据作为评测样本，构建更贴近实际业务场景的评测集。

1.  在应用观测列表中，点击指定应用右侧的**查看详情**进入Span列表页，再点击**批量操作**，勾选需要添加到评测集的Span数据（支持多选）。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1532430771/p1051589.png)
    
2.  单击**添加到评测集**按钮，进入配置页：![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1532430771/p1051594.png)
    
    -   选择**目标评测集**和**目标评测集名称**：可选择已有评测集或新建评测集。
        
    -   **导入方式**：支持**追加数据**或**全量覆盖**两种方式。
        
    -   **字段映射**：将Span数据中的字段映射到评测集字段。新建评测集时，默认提供input和output两个字段，支持添加更多自定义字段。选择已有评测集时，会自动带出已有的表头信息。
        
3.  配置完成后，单击**开始导入**，完成后会显示“添加到评测集完成”提示。
    
    > 字段映射支持从Span的完整参数中选择。每个评测集最多支持50个字段映射。
    

### **数据标注**

应用观测支持对Span数据进行标签标注，便于后续的数据分析、筛选和评测。标签与应用评测中的标签管理功能共享，统一管理。

**添加标注**

1.  在应用观测列表中，点击指定应用右侧的**查看详情**进入Span列表页，点击指定节点的名称即**名称**列内容（如AgentApp）进入数据详情页，单击**数据标注**按钮，即可为当前节点添加自定义标签。
    
2.  在弹出的侧边栏中，选择要添加的标签。如需创建新标签，单击**新建标签**跳转到标签管理页面。
    
3.  根据标签类型进行标注：
    
    -   **布尔值**：是/否 二选一
        
    -   **分类**：下拉多选
        
    -   **数字**：数字输入框
        
    -   **文本**：文本输入框
        

标注内容会立即自动保存。

#### **查看标注**

保存数据标注后，在Span列表页的**标签**列可以查看已标注的内容。多个标签的标注结果会分行显示在同一区域。![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1532430771/p1051618.png)

## **查看数据**

应用观测支持多维度的Span数据筛选，帮助您快速定位目标数据。

### **Span筛选模式**

-   **Root Span**：仅显示根节点，即每次调用的入口Span（默认模式）
    
-   **All Span**：显示所有Span，平铺展示
    
-   **Model Span**：仅显示包含模型调用的Span
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1532430771/p1051624.png)

### **过滤器：添加筛选条件**

1.  点击**过滤器**，然后点击**添加筛选条件**，可添加多个条件。
    
2.  完成条件添加后，点击**应用**即可过滤出指定Span数据。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/1532430771/p1051628.png)

#### **筛选条件**

**筛选类型**

**筛选字段**

**支持的条件**

状态

正常、错误（可按错误类型细分）

属于、不属于

Span Name

手动输入Span名称

包含、不包含

输入

手动输入关键词

包含、不包含

输出

手动输入关键词

包含、不包含

延时

手动输入数值（毫秒）

等于、大于、小于、大于等于、小于等于

Token总量

手动输入数值

等于、大于、小于、大于等于、小于等于

输入Token

手动输入数值

等于、大于、小于、大于等于、小于等于

输出Token

手动输入数值

等于、大于、小于、大于等于、小于等于

标签

用户已添加的标签

根据标签类型：分类（包含/不包含/等于/不等于）、布尔值（等于/不等于）、数字（数值比较）、文本（包含/不包含/等于/不等于）

## 计费说明

-   应用观测功能本身不收费。
    
-   应用观测产生的数据需要存储在可观测链路[OpenTelemetry](https://www.aliyun.com/product/developerservices/xtrace)服务中，您需要支付相关的费用。关于OpenTelemetry服务的费用详情，请参见[计费说明](https://help.aliyun.com/zh/arms/tracing-analysis/product-overview/untitled-document-1697525445039)。
    

## **附录**

### 名词解释

**名词**

**解释**

**节点**

在应用观测中，**节点**是指被追踪的一个操作单元。每个**节点**具有**名称**和**类型**等属性，并详细记录了操作的具体信息和起止时间。另外，**节点**之间还可以形成嵌套关系。

### 支持的节点类型

> **注意：以下节点仅在被触发或调用时展示。**

### **智能体应用**

**节点类型**

**说明**

**CHAIN**

**Chain**节点将大模型节点与其他类型的节点相连接，以实现复杂任务的处理。

> **Chain**节点可以包含其它类型节点，例如**Retriever**、**LLM**等。

当**Chain**作为根节点时，**名称**可能值为：**AgentApp**（[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)）、**WorkflowApp**（[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)）。

**AGENT**

**Agent**节点表示对智能体的调用。

**RETRIEVER**

**Retriever**节点用于执行检索操作。**KnowledgeRetriever**表示在[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)中进行检索。

> 目前暂不支持观测在[长期记忆](https://help.aliyun.com/zh/model-studio/long-term-memory)中的检索过程。

作为**KnowledgeRetriever**的子节点时，**Retriever**有两种**名称**：

-   **TextRetriever**：指触发了文本检索，文本相似度计算采用改进后的BM25算法，默认返回100个文本切片，暂不支持数量调整。
    
-   **VectorRetriever**：指触发了向量检索，默认返回100个文本切片，暂不支持数量调整。
    

**REWRITER**

**Rewriter**节点会基于会话上下文自动调整原始输入Prompt以提升知识检索效果。

**EMBEDDING**

**Embedding**节点用于将输入Prompt转化为数值化向量。

> **Token量**指Embedding模型本次向量化了多少Token。

**RERANKER**

**Reranker**节点会计算每个输入文本切片的相似度分数并按此降序排列。

**LLM**

**LLM**节点表示调用大模型（如千问Plus）进行推理或者文本生成。

> **Token量**指模型输入Token数 + 模型输出Token数。

> LLM节点的**延时**（**调用时长**）包括输出回复的过程。

**TOOL**

**Tool**节点表示对[插件](https://help.aliyun.com/zh/model-studio/plug-in-overview)的调用，支持官方插件和自定义插件，详见[插件概述](https://help.aliyun.com/zh/model-studio/plug-in-overview#00edef12dc50q)。

> 例如调用计算器或者夸克搜索。

**GUARDRAIL**

**Guardrail**节点表示对阿里绿网的调用，用于实时监控、检测和拦截多种违规内容，例如赌博、色情等。

> **ManualIntervention**指触发了您为智能体应用设定的干预规则；**SystemIntervention**指触发了系统干预规则。

### **工作流应用**

**节点类型**

**说明**

**CHAIN**

**Chain**节点将大模型节点与其他类型的节点相连接，以实现复杂任务的处理。

> **Chain**节点可以包含其它类型节点，例如**Retriever**、**LLM**等。

当**Chain**作为根节点时，**名称**可能值为：**AgentApp**（[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)）、**WorkflowApp**（[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)）。

**START**

表示[开始节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

**RETRIEVER**

**Retriever**节点用于执行检索操作。**KnowledgeRetriever**表示在[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)中进行检索。

> 目前暂不支持观测在[长期记忆](https://help.aliyun.com/zh/model-studio/long-term-memory)中的检索过程。

作为**KnowledgeRetriever**的子节点时，**Retriever**有两种**名称**：

-   **TextRetriever**：指触发了文本检索，文本相似度计算采用改进后的BM25算法，默认返回100个文本切片，暂不支持数量调整。
    
-   **VectorRetriever**：指触发了向量检索，默认返回100个文本切片，暂不支持数量调整。
    

**REWRITER**

**Rewriter**节点会基于会话上下文自动调整原始输入Prompt以提升知识检索效果。

**EMBEDDING**

**Embedding**节点用于将输入Prompt转化为数值化向量。

> **Token量**指Embedding模型本次向量化了多少Token。

**RERANKER**

**Reranker**节点会计算每个输入文本切片的相似度分数并按此降序排列。

**LLM**

表示[大模型节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

> **Token量**指模型输入Token数 + 模型输出Token数。

> LLM节点的**延时**（**调用时长**）包括输出回复的过程。

**API**

表示[API节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

**CLASSIFIER**

表示[意图分类节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

**TEXT\_CONVERTER**

表示[文本转换节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

**SCRIPT**

表示[脚本转换节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

**CONDITION**

表示[条件判断节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

**FUNCTION\_COMPUTE**

表示[函数计算节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

**APP\_FLOW**

表示[AppFlow节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

**GUARDRAIL**

**Guardrail**节点表示对阿里绿网的调用，用于实时监控、检测和拦截多种违规内容，例如赌博、色情等。

> **ManualIntervention**指触发了您为智能体应用设定的干预规则；**SystemIntervention**指触发了系统干预规则。

**END**

表示[结束节点](https://help.aliyun.com/zh/model-studio/workflow-application/#3a4fddcde4dcs)。

## 高代码应用

**节点类型**

**说明**

**CHAIN**

**FullCodeApp**指触发了一个已创建的[高代码应用](https://help.aliyun.com/zh/model-studio/rich-code-application/)，目前不支持追踪其内部调用链路。

## **常见问题**

**使用子账号开通应用观测，应如何配置权限？**

1.  为子账号配置`AliyunBailianFullAccess`[全局管理（阿里云百炼）权限](https://help.aliyun.com/zh/model-studio/member-management#cd0f1152d50hj)。
    
2.  为子账号配置`应用观测-操作`（或`管理员`）[页面权限](https://help.aliyun.com/zh/model-studio/member-management#febd776ce5lbx)，使其可在应用观测页面执行写入类操作。
    
3.  创建并授予子账号**创建服务关联角色**系统策略。
    
    1.  登录[RAM控制台](https://ram.console.aliyun.com/)，在左侧导航栏，选择**权限管理** > **权限策略**，然后单击界面上的**创建权限策略**。
        
    2.  在**脚本编辑**的`Effect`、`Action`、`Resource`、`Condition`中分别输入以下脚本中的对应内容后，单击**确定**。
        
        ```
        {
            "Version": "1",
            "Statement": [
                {
                    "Action": "ram:CreateServiceLinkedRole",
                    "Resource": "*",
                    "Effect": "Allow"
                }
            ]
        }
        ```
        
    3.  输入权限策略名称`CreateServiceLinkedRole`后，单击**确定**。
        
    4.  在左侧导航栏，选择**身份管理** > **用户**。从界面列表中找到待授权的子账号，然后单击子账号**操作**列的**添加权限**。
        
    5.  从**权限策略**列表中，选择刚创建的权限策略（CreateServiceLinkedRole），然后单击**确认新增授权**。至此，子账号拥有了创建服务关联角色的权限。
        
4.  完成以上所有权限配置后，返回[应用观测](https://bailian.console.aliyun.com/tab=app?tab=app#/app-observe)界面，使用子账号再尝试开启**应用观测**。
    

**已为高代码应用开启观测，但为什么看不到调用量等统计数据？**

请按以下清单排查：

-   已在代码中定义要上报的信息。可使用 AgentScope-AI 的 [Tracing模块](https://github.com/agentscope-ai/agentscope-runtime/tree/main/src/agentscope_runtime/engine/tracing) 定义。
    
-   在部署高代码应用时，已添加`--telemetry enable`参数开启可观测能力。
