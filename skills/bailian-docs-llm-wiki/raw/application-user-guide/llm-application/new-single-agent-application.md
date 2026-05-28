# 新版智能体应用

新版智能体应用（Agent 2.0）将知识库、MCP 等多种能力统一为工具，并通过自主思考和规划来调用，以解决复杂任务。

## 版本对比与选型建议

新版智能体为大多数应用场景提供了更优的性能和开发体验，在没有旧版本依赖需求时，推荐使用新版。

**对比维度**

**旧版本（Agent 1.0）**

**新版本（Agent 2.0）**

规划与调度

智能体在检索知识库后，再决策是否调用 MCP 等其他工具。

将知识库、MCP 统一为工具，由智能体自主规划在何时、以何种顺序进行调用。

过程透明度

只展示最终结果，无法完整回溯中间决策。

能完整展示每一轮的“规划-执行-反思”链路的全过程。

适用场景

适用于意图单一、流程固定的简单任务。

能够完成从简单问答到复杂规划的各类任务。

## 示例对比

**旧版**

**新版**

1.  **知识库检索先行，再决策是否调用后续工具**
    

![20251226183243](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1039482.jpg)

1.  **知识库与 MCP 统一作为工具，由智能体自主规划调用**
    

![20251226183204](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1039483.jpg)

2.  **缺乏任务规划，无法完成复杂研究任务**
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1039475.png)
    

2.  **自主规划并拆解复杂任务，生成完整回复**
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1039473.png)
    

## 快速开始：创建一个基础智能体

1.  访问阿里云百炼控制台[应用管理](https://bailian.console.aliyun.com/?tab=app#/app-center)，单击**创建应用**，选择**智能体应用** > **Agent 2.0**。
    
2.  填写应用名称，单击**立即创建**。创建完毕后自动跳转至应用配置界面。
    
    ![截屏2025-12-25 13](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1038483.png)
    
3.  在模型选择器的下拉菜单中选择模型，例如`千问-Plus-Latest`。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1038599.png)
    
4.  在右侧对话框中输入问题：`你是谁？`。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1036624.png)
    

## 能力配置

### 模型选择

为确保多步规划效果，推荐选用具备强工具调用能力的模型，如`千问-Max`系列模型。

1.  在模型选择器的下拉菜单中选择模型。单击**更多模型**可以选择其他模型。
    
2.  单击模型选择器右侧的参数配置器，支持修改的参数如下：
    
    -   **最长回复长度**：模型生成的长度限制，不包含提示词。
        
    -   **temperature**：控制生成随机性和多样性，数值越高随机性越强。
        
    -   **enable\_thinking**：是否开启思考模式。开启思考模式有助于提升智能体的反思效果。不支持思考模式的模型无法配置 enable\_thinking 参数。
        
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1036629.png)
    

### 系统提示词

系统提示词用于定义智能体角色、行为指令与能力边界，以确保其在交互中始终保持一致性、可控性和任务合规性。

1.  **配置系统提示词**
    
    配置系统提示词为`请你模仿《百年孤独》的风格来回答我的问题`，以下是效果对比：
    
    -   无系统提示词：
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1039068.png)
        
    -   配置系统提示词：
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1039066.png)
        
2.  **在系统提示词中使用自定义变量（可选）**
    
    除了支持输入静态文本，系统提示词还允许嵌入自定义变量。
    
    1.  单击系统提示词右上方的**新建变量**，设置自定义变量，单击**确定**保存。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1036638.png)
        
    2.  输入`/`，使用已配置的变量。
        
        ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1038792.png)
        

### 预解析文件

预解析文件功能用于控制上传文件的处理方式。

-   **关闭预解析**：关闭后，系统不会主动解析文件。文件的 URL 会作为上下文信息传递给智能体，智能体可在后续步骤中决策是否调用工具，并将该 URL 作为参数传入。
    
    ![截屏2025-12-25 20](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1038795.png)
    
-   **开启预解析**：开启后，系统将使用预置解析器处理上传的文档、图像、视频、音频等文件，并返回解析后的文本内容给模型作为参考。
    
    ![截屏2025-12-26 09](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1038832.png)
    

> 千问-VL 系列模型由于具备多模态能力，即使关闭预解析文件，也能够直接解析图片和视频文件。

> 在其他所有情况下（例如，使用不具备多模态能力的文本模型，或使用千问-VL 系列模型处理非图像/视频文件时），智能体的文件处理能力则严格遵循上述“开启”或“关闭”的逻辑。

### **知识库**

知识库使智能体能够查询外部信息，并将检索到的内容作为生成答案的依据。在新版智能体中，知识库作为智能体的一项技能，作为工具由智能体自主规划调用。这种主动获取知识的方式，在处理私有知识或垂直领域问答时，能提升回答的准确率并有效减少内容幻觉。详情请参考[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。

> 在[回复](#ed4f2ba20av9d)中开启**展示回答来源**可以展示知识来源和源文件地址。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1036709.png)

新版智能体支持通过标签来限定知识库的查询范围。通过为知识库文件设置标签，并在系统提示词（Prompt）中定义使用规则，可以引导智能体根据用户意图，在更小的、更精准的文件范围内进行检索，从而显著提升回答的准确性和相关性。详情请参考[新版智能体知识库标签过滤](https://help.aliyun.com/zh/model-studio/rag-optimization#3c8a459e854md)。

### **MCP**

在新版智能体中，外部工具均以 MCP 协议接入智能体，并纳入调度体系，包括来自[MCP 广场](https://bailian.console.aliyun.com/?&tab=app&scm=20140722.S_%E7%99%BE%E7%82%BCprompt._.RL_%E7%99%BE%E7%82%BCprompt-LOC_aillm-OR_chat-V_3-RC_llm#/mcp-market)的官方 MCP 和自定义 MCP 服务。智能体能够在多步推理中，对 MCP 进行动态的、非固定顺序的调用，以解决更复杂的任务。此外，插件也支持一键转换为 MCP 服务。

![截屏2025-12-26 12](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1039012.png)

### 应用组件

将已创建的智能体或工作流作为工具接入。需要先将智能体或工作流应用[发布为组件](https://help.aliyun.com/zh/model-studio/use-agent-or-workflow-as-component)。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5461060771/p1050786.png)

### 记忆

-   **短期记忆**：新版智能体支持短期记忆功能，即在多轮会话中为智能体提供上下文信息。可以设置 0 到 30 轮的上下文（0 代表不传递多轮对话记录）；轮数越多，对话相关性越强，但输入长度也会相应增加。
    
-   **长期记忆**：该功能计划在未来的迭代中支持。
    

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1037574.png)

### 回复

回复支持展示回答来源。开启后，将以角标形式展示知识来源和源文件/源网页地址。该功能推荐与知识库和联网搜索 MCP 组合使用。

![20251223150244](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1037577.jpg)

## 运行与结果分析

完成应用配置后，可在页面右侧的对话窗口中运行智能体。对于需要多步规划的复杂请求，新版智能体会以卡片流的形式，展示其决策过程和运行轨迹，该过程主要包含以下两种步骤：

1.  **思考 (Thinking)**：此步骤展示模型的推理逻辑，便于分析其决策路径并定位非预期行为的根源**（仅当选用支持思考模式的模型时出现）**。
    
2.  **工具调用**：此步骤记录了模型执行的具体工具调用入参及其返回的结果。
    
    ![截屏2025-12-23 15](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1037618.png)
    

通过配置 **ReAct 最大轮次**（取值范围 1-50），用于限制智能体在单次会话中可以调用工具的最大次数，当超出此限制后将会自动退出工具调用链路，并由智能体生成最终回复。

![截屏2025-12-24 17](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1038333.png)

## 应用发布与集成

**重要**

应用发布是后续所有智能体应用调用、集成的前提条件。

### 应用发布

在应用配置页面的右上角，单击**发布**按钮，在弹出窗口中会展示自上次发布以来的配置变更差异。确认发布信息无误后，单击**确认发布**，即可完成应用发布。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1037673.png)

### **通过 API 调用**

您可以在智能体应用**发布渠道**页签，单击**API调用**右侧的**查看API**，查看通过 API 调用新版智能体应用的方法。详情参考[新版智能体应用 API 参考](https://help.aliyun.com/zh/model-studio/new-agent-application-api-reference)。

![20251226183929](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1039484.jpg)

## 应用管理

### 版本管理

通过版本管理功能，可以编辑历史版本描述信息，或回滚发布过的历史版本。

1.  在应用配置页，单击顶部导航栏右侧的**版本管理**。
    
    ![截屏2025-12-25 17](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1038625.png)
    
2.  选中需要回滚的历史版本，将鼠标悬浮至卡片上，单击右上角编辑图标，在**编辑版本描述**对话框中按需完成修改后，单击**确定**，即可修改历史版本描述信息。单击**覆盖当前草稿**，即可回滚至该版本。
    
    ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5823576671/p1038630.png)
    

## 安全与合规

### 应用合规备案

若应用对外提供服务，必须遵守国家网信办《生成式人工智能服务管理暂行办法》等法规，完成必要的[应用合规备案](https://help.aliyun.com/zh/model-studio/compliance-and-launch-filing-guide-for-ai-apps-powered-by-the-tongyi-model)。

## 计费说明

智能体功能计费主要体现在以下几个方面：

1.  **模型调用**
    
    -   智能体会产生模型调用费用，具体费用取决于模型类型、输入和输出 Token 数量。
        
    -   具体的模型类型和对应的计费规则请参考[模型列表](https://help.aliyun.com/zh/model-studio/models)。
        
2.  **知识库**
    
    -   知识库按量付费，详情请参见[知识库计费说明](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base)。
        
    -   从知识库召回的文本切片会增加模型输入 Token 数量，可能导致模型推理（调用）费用的增加。
        
3.  **MCP**
    
    -   部分官方 MCP 按模型调用计费，如文生图、文生视频、语音合成等 MCP。
        
    -   部分 MCP 服务涉及第三方 API 调用，使用后可能会产生费用。这部分费用由第三方收取，阿里云百炼不收取费用。
        

## 常见问题

### 支持将旧版智能体升级到新版本吗？

不支持。旧版智能体和新版智能体基于不同的技术架构，彼此不兼容，无法进行直接的版本切换、升级或降级。

如果您当前在使用旧版智能体，并希望体验新版智能体的功能，请您前往控制台**重新创建一个新版智能体应用**。

### 为什么智能体未按预期调用已配置的工具？

可从以下四个层面进行排查：

-   技能配置与挂载：请核实该技能是否已成功创建并正确挂载到当前智能体应用中。
    
-   系统提示词的引导性：请检查系统提示词是否清晰地描述了该技能的功能、参数以及适用的场景。模型依赖这些描述信息来决策何时调用技能。
    
-   意图与技能的相关性：请评估问题的表述是否清晰，其意图是否能明确指向特定技能。如果意图模糊或与技能功能不相关，模型可能选择不调用。
    
-   执行轮次限制：请检查是否达到了 ReAct 轮次上限。智能体可能已规划调用该技能，但在执行到该步骤前因轮次耗尽而被强制终止。
