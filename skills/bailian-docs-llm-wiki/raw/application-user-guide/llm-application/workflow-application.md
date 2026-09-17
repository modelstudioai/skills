# 工作流应用

工作流应用将复杂的任务拆分成一系列有序执行的步骤，以降低系统复杂度。在阿里云百炼，通过工作流组合使用大模型、API和函数计算等节点，可有效降低编码成本。本文介绍如何创建工作流。

## 应用介绍

### 为什么使用工作流应用

工作流是一种将复杂任务拆分为一系列有序步骤的方法，旨在简化系统复杂度，提高工作效率。在现代软件开发和业务流程管理中，工作流应用变得尤为重要。通过在阿里云百炼平台上创建工作流应用，可以清晰地定义任务的执行顺序、责任分配以及各步骤之间的依赖关系，从而实现自动化和优化。

工作流应用有许多使用场景，如：

-   **旅行规划**：用户可通过工作流插件选择目的地等参数，自动生成旅行计划，包括航班、住宿、景点推荐等。
-   **报告分析**：针对复杂数据集，通过组合数据处理、分析和可视化插件，生成结构化和格式化的分析报告，满足不同业务需求。
-   **客服支持**：通过自动化工作流处理客户咨询，包括问题分类等，提高客服响应速度和准确性。
-   **内容创作**：实现文章、市场营销文案等内容的生成，用户只需输入主题和要求，系统自动生成符合要求的文稿。
-   **教育培训**：通过工作流设计个性化学习方案，包括学习进度跟踪、测评等，实现学生的自主学习。
-   **医疗问诊**：根据患者输入的症状，通过组合多种分析工具生成初步诊断或推荐相关检查，辅助医生进行进一步判断。

## 节点类型

工作流由多种功能节点组合而成。

### 基础节点

-   [开始和结束节点](raw/application-user-guide/llm-application/workflow-application/start-end-node.md)
-   [条件判断节点](raw/application-user-guide/llm-application/workflow-application/conditional-node.md)
-   [循环节点](raw/application-user-guide/llm-application/workflow-application/loop-node.md)
-   [批处理节点](raw/application-user-guide/llm-application/workflow-application/batch-node.md)
-   [流程输出节点](raw/application-user-guide/llm-application/workflow-application/process-output-node.md)

### AI 节点

-   [大模型节点](raw/application-user-guide/llm-application/workflow-application/llm-node.md)
-   [知识库节点](raw/application-user-guide/llm-application/workflow-application/knowledge-base-node.md)
-   [意图分类节点](raw/application-user-guide/llm-application/workflow-application/intent-node.md)
-   [参数提取节点](raw/application-user-guide/llm-application/workflow-application/parameter-extraction-node.md)
-   [多模态生成节点](raw/application-user-guide/llm-application/workflow-application/multimodal-generation-node.md)
-   [智能体创建节点](raw/application-user-guide/llm-application/workflow-application/agent-create-node.md)
-   [智能体群组节点](raw/application-user-guide/llm-application/workflow-application/agent-group-node.md)

### 工具节点

-   [API节点](raw/application-user-guide/llm-application/workflow-application/api-node.md)
-   [函数计算节点](raw/application-user-guide/llm-application/workflow-application/fc-node.md)
-   [脚本节点](raw/application-user-guide/llm-application/workflow-application/script-node.md)
-   [插件节点](raw/application-user-guide/llm-application/workflow-application/plugin-node.md)
-   [MCP节点](raw/application-user-guide/llm-application/workflow-application/mcp-node.md)
-   [AppFlow节点](raw/application-user-guide/llm-application/workflow-application/appflow-node.md)
-   [应用组件节点](raw/application-user-guide/llm-application/workflow-application/component-node.md)

### 数据处理节点

-   [变量处理节点](https://help.aliyun.com/zh/model-studio/workflow/variable-processing-node)
-   [变量赋值节点](raw/application-user-guide/llm-application/workflow-application/variable-assignment-node.md)
-   [文档解析节点](raw/application-user-guide/llm-application/workflow-application/document-extraction-node.md)
-   [图片解析节点](raw/application-user-guide/llm-application/workflow-application/image-extraction-node.md)
-   [音频解析节点](raw/application-user-guide/llm-application/workflow-application/audio-extraction-node.md)
-   [视频解析节点](raw/application-user-guide/llm-application/workflow-application/video-extraction-node.md)
-   [数据连接器节点](raw/application-user-guide/llm-application/workflow-application/data-connector-node.md)

## 会话变量

会话变量作为全局变量，能够在当前工作流的全生命周期内记录参数信息，并可在各个节点中进行引用。可在画布配置页面右上角单击会话变量图标进行配置。

## 测试应用

在工作流配置完成后，可以通过测试功能验证工作流的运行效果。单击右上角**测试**按钮，打开测试面板。测试面板支持多种测试模式，可根据不同的使用场景选择合适的模式测试。

### 文本对话

文本对话是默认的测试模式，会保留历史对话上下文，支持连续的多轮对话交互。

1.  在测试面板顶部的下拉框中选择文本对话模式（默认模式）。如果工作流中包含自定义变量，在参数配置区域填写变量值。
2.  在输入框输入测试内容（支持文本输入和附件上传），单击**发送**按钮（或按 Enter 键）执行测试。
3.  查看测试结果，可以单击节点查看详细的输入输出，也可以切换输出格式（Text/JSON 格式）查看结果。
4.  如需继续多轮对话，在输入框输入下一轮对话内容并发送；如需重新开始对话，可单击**清空**按钮。

### 文本生成

文本生成模式为单轮交互，每次测试都是独立的，不会保留历史对话上下文，支持两种模式：

-   **同步运行**：适用于执行时间较短的简单任务，工作流执行完成后直接返回结果。
-   **异步运行**：适用于执行时间较长的复杂应用，系统返回 Task ID，可通过 Task ID 查询任务执行结果。

#### 同步运行

同步运行模式下，工作流会立即执行并等待完成，执行完成后直接返回结果。

1.  在输入框中输入测试内容，单击**运行**按钮执行测试。
2.  等待工作流运行完成后，切换到结果标签页查看输出结果。可以单击节点查看详细的输入输出，也可以切换输出格式（Text/JSON 格式）查看结果。

#### 异步运行

异步运行模式下，工作流会在后台执行。系统会立即返回 Task ID，可通过 Task ID 查询任务执行结果。在[任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center)中可以查看历史异步任务。

1.  在输入框中输入测试内容，单击**运行**按钮执行测试。系统会立即返回 Task ID。
2.  异步任务执行过程中，测试面板会显示"执行中"状态，可单击**刷新**按钮刷新任务状态。
3.  任务执行完成后，在结果标签页中查看输出结果，结果中会显示"异步"标签和 Task ID。可以单击节点查看详细的输入输出，也可以切换输出格式（Text/JSON 格式）查看结果。

### 音视频互动

阿里云百炼可以将工作流应用发布为音视频实时对话应用，并提供便捷的调试窗口，支持通过 H5/APP 快速体验 demo 效果，也可以通过音视频 SDK 集成到 Web/iOS/Android 应用中。

> -   不推荐使用深度思考模式的模型进行实时音视频对话，会影响对话体验，如 DeepSeek-R1、QwQ 系列模型。
> -   DeepSeek V3 模型不支持视频对话功能。

1.  选择开始节点、大模型节点和结束节点，配置一个可正常执行的工作流。
2.  通过测试文本对话，先在文本对话中调试出符合预期的应用效果。
3.  文本会话效果满意后，切换到**语音互动**或**视频互动**，再单击**去配置**配置 API Key 用于调用应用。
4.  进行**音视频设置**，配置参数后，再单击**拨打**调试音视频互动效果。其中语音转文字可进行语种选择，文字转语音可进行语音模型选择和音色选择。
5.  效果测试满意后，单击右上角**体验**按钮，生成临时体验二维码，通过手机微信/钉钉/浏览器扫码体验交互效果。二维码有效期为 24 小时。
6.  效果确认后，单击**发布**按钮发布应用。再进入**发布渠道**，完成智能媒体服务开通和 SLR 授权后，创建互动智能体。

## 检查清单

在检查清单中可以查看为确保工作流成功运行所需进行的配置。可在画布配置页面右上角单击检查清单图标查看。

## 发布应用

发布后的应用可以被 API 调用，也可以通过 Web 页面分享给同一主账号下的 RAM 子账号使用。您可以单击智能体应用管理界面右上角的**发布**按钮。

### 通过API调用

您可以在工作流应用**发布渠道**页签，单击 **API** 右侧的**查看API**，查看通过 API 调用智能体应用的方法。

> 注：您需用您的 API Key 对 `DASHSCOPE_API_KEY` 进行替换才可发起调用。

关于 API 调用的相关问题总结：

-   关于调用方式（HTTP/SDK），请参见[调用工作流应用](raw/application-user-guide/bailian-application-calling/invoke-workflow-application.md)。
-   关于调用接口的详细参数信息，请参见[应用调用参数信息](raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)。
-   关于调用参数传递问题，请参见[应用的参数传递](raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
-   关于调用报错信息，请参见[错误码](raw/model-api-reference/preparations/error-code.md)进行解决。
-   关于调用并发数限制问题，应用本身不限流，主要与内部调用的模型有关，有关模型内容请参见[百炼控制台](https://bailian.console.aliyun.com/cn-beijing/?tab=model#/model-market/all)。

目前不支持在工作流中调用析言服务，可以通过 API 节点调用自定义的 API 服务。

> API 调用的超时时间为 600 秒，暂不支持修改。如可能超时，建议采用以下方案：
> 
> -   使用异步模式：选择异步运行模式，系统返回 Task ID，可通过 Task ID 查询结果，不受同步超时限制。
> -   拆分任务：将任务拆分为多个步骤，或将批量数据分批处理，避免单次执行超时。

### 发布为组件

您可以将工作流应用发布为组件，以供其他智能体或工作流应用使用。详细的组件配置方法请参考[发布为组件](raw/application-user-guide/application-publishing-and-sharing/use-agent-or-workflow-as-component.md)。

### 其他调用方式

其他分享方式，请参见[应用分享](raw/application-user-guide/application-publishing-and-sharing/share-an-application.md)。

## 工作流导入/导出

1.  **导入/导出百炼工作流**
    
    单击工作流页面上方的更多图标，选择**导出 DSL** 或**导入百炼 DSL**。
    
2.  **导入 Dify 工作流**
    
    百炼支持一键导入 Dify 工作流，便于迁移和复用。
    
    1.  单击工作流页面上方的更多图标，选择**导入 Dify DSL**。
    2.  调整各节点的参数配置。节点兼容性详情如下：
    
    Dify 节点
    
    对应的百炼节点
    
    兼容性
    
    开始
    
    开始
    
    `sys.query` 对应百炼的 `query`；`sys.dialogue_count` 对应百炼的最大记忆轮次。
    
    LLM
    
    大模型
    
    模型：百炼不支持的模型会置空，需自行选择，百炼支持模型完全兼容；Prompt：Dify 的 System 对应百炼的提示词，User 对应用户提示词；视觉能力完全一致；上下文：百炼将 Dify 上下文的原始字段直接纳入 System Prompt。
    
    知识检索
    
    知识库
    
    输入：统一引入 `content` 字段作为输入；知识库：导入后置空，需手动关联；召回设置：Dify 的 `Top-k` 映射为百炼的召回片段数。
    
    直接回复
    
    输出节点
    
    完全兼容。
    
    Agent
    
    无
    
    仅保留名称，需单击以选择具体的百炼节点进行替换。
    
    问题分类器
    
    意图分类
    
    百炼不支持的模型会置空，需自行选择，百炼支持模型完全兼容。
    
    迭代
    
    批处理
    
    输入对应百炼的批处理数组；输出变量对应百炼的输出变量。
    
    循环
    
    循环
    
    完全兼容。
    
    代码执行
    
    脚本
    
    区分 Python 和 JavaScript 脚本。
    
    模板转换
    
    无
    
    不兼容，生成自定义节点。
    
    变量聚合器
    
    变量处理
    
    对应百炼变量处理节点的聚合分组输出模型。
    
    文档提取器
    
    无
    
    不兼容，生成自定义节点。
    
    变量赋值
    
    变量设置
    
    完全兼容。
    
    参数提取器
    
    参数提取
    
    百炼不支持推理模式，其余完全兼容。
    
    HTTP 请求
    
    API
    
    完全兼容，但需要重新鉴权。
    
    列表操作
    
    无
    
    不兼容，生成自定义节点。
    
    工具
    
    插件、MCP
    
    不兼容，生成自定义节点。
    
    注释
    
    无
    
    不兼容。
    
    结束
    
    结束
    
    若 Dify 工作流中存在多个结束节点，百炼会将其转换为一个变量聚合节点和一个结束节点。
    

## 查看工作流应用版本

1.  单击工作流配置页面右上角的**发布**，在发布对话框中输入版本信息（例如 1.0.0）后，单击**确定**。
2.  单击页面顶部的**版本管理**，可在**历史版本**面板按需查看或使用（单击**覆盖当前草稿**或**回到当前版本**）当前工作流应用的不同版本。也可以单击顶部的 **DSL 导出该版本**，导出所选历史版本工作流的 DSL。
3.  （可选）在**节点库**中查看或搜索节点。

## 删除与复制工作流应用

您可以在**应用管理**找到已发布的应用卡片，单击更多图标，进行**删除与复制工作流、修改应用名**操作。

## 常见问题

### 工作流应用相关

1.  **怎么把工作流运行的结果写入数据库？**
    
    使用脚本转换节点，可将上一节点的内容写入数据库。
    
2.  **如何上传文件？**
    
    您可以在工作流应用中加入一个 API 节点来实现文件上传功能。
    
3.  **如何上传图片？**
    
    使用 VL 模型，通过指定参数传入图片 URL 地址。
    
4.  **能否在工作流应用里使用异步任务 API？**
    
    工作流应用超时时间为 600 秒，不建议在流程里使用异步任务 API。
    
5.  **工作流前端应该怎么调用 API 并且流式输出？**
    
    暂时不支持前端调用。
    
6.  **工作流无法导入单独的 .yaml 文件？**
    
    不支持单独导入 .yaml 文件，需提供包含 md5 文件的压缩包，建议重新生成 MD5。
    
7.  **工作流变量名可以为中文吗？**
    
    变量名不支持使用中文。
    
8.  **对话记录存储问题？**
    
    工作流应用仅保存一个月数据，需自行保存对话记录，session\_id 有效时间为一小时。
    

### 节点相关

1.  **若意图分类节点开启上下文，运行报错？**
    
    若意图分类节点开启上下文，则您传入该节点的变量类型需为 List 类型。
    
2.  **API 节点使用流式输出报错？**
    
    工作流中的 API 节点不支持流式输出，HTTP API 本身是支持的。
    
3.  **如何处理条件判断节点响应速度慢？**
    
    -   检查工作流配置：确保每个节点配置正确，尤其是条件判断节点，避免不必要的复杂计算或数据处理。
    -   优化代码逻辑：如果条件判断中涉及自定义脚本，尝试优化脚本逻辑，减少不必要的循环或数据处理。
    -   批量测试：批量测试当前工作流的平均响应时间，以确定是否存在特定条件下的性能瓶颈。
4.  **大模型节点流式如何输出思考过程？**
    
    需要在大模型节点后添加文本转换节点并配置 `reasoning_content` 变量，打开结果返回开关。返回条件需要结束节点接收。
    
5.  **大模型节点输出参数无法自定义？**
    
    -   使用脚本节点处理输出：在大模型节点之后添加一个脚本节点，通过脚本处理大模型节点的输出，将其转换为需要的格式或添加额外的输出参数。
    -   配置批量节点：如果在批量节点中使用大模型节点，可以在批量节点的配置中选择大模型节点的输出作为最终输出 `resultList`。
    
    更多详细信息，请参考[应用的参数传递](raw/application-user-guide/bailian-application-calling/pass-through-of-application-parameters.md)。
    
6.  **工作流 API 调用节点无返回结果及参数传递问题？**
    
    确认 API Key 和 Base URL 正确。确认输入参数配置正确，调整字段输入类型，通过模型观测查看模型使用详情。
    
7.  **调用知识库的 Excel 数据问题？**
    
    无法直接调用本地文件，可通过 MCP 实现本地调用；知识库节点输出需自行处理文字内容，建议增加大模型完成表格转换后再传入脚本处理。
