# 文件问答

在 智能体应用 中上传文件后，可以与文件内容进行智能问答。此功能通过三种不同的处理模式，支持对文档、图片、音视频等多种文件进行内容理解、信息提取和智能问答。根据您的具体需求，可以选择以下三种处理模式：

处理模式

说明

适合场景

特点

**全文引用**

通过内置解析器解析文件内容，将文件内容（在上下文长度限制内）作为整体提供给模型。

需要全局理解的任务，如文档总结、全文翻译、风格润色。

简单直接，但受限于模型的上下文长度。

**切片检索**（[RAG](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)）

通过内置解析器解析文件内容，将文件切分成小片段，提问时，系统会从文件切片中检索最相关的内容片段，并将其与用户问题一并提供给模型以生成回答。

长文档问答、知识库检索、需要精确定位信息来源的场景。

能处理超长文件，回答效果依赖切片和检索策略。

**自定义处理**

将文件信息（如 URL 或内容本身）提供给模型，允许模型根据任务需求自主调用外部工具来处理文件。

需要对文件进行其他操作的任务，如图片风格转换、视频内容分析后生成报告等。

功能强大灵活，依赖于所配置的工具（[插件](raw/application-user-guide/agent-development/llm-application/plug-in/plug-in-overview.md)、[MCP](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp#8319d03864jym) 等）。

上述模式为 API 语义层面的处理方式。在当前控制台中，处理方式通过应用**规划**区的**预解析文件**开关与**知识库关联**配置，对应关系参见[如何使用](https://help.aliyun.com/zh/model-studio/file-q-a#f10ae14445ecz)。

## 工作原理

智能体应用的文件问答功能通过以下流程实现：

1.  **文件解析**：系统自动识别并解析上传的文档、图片、音视频等多种格式文件，提取其中的文本、图像或音频信息。内置解析器专注于从各类文件中提取纯文本内容。
2.  **内容处理**：根据应用的文件处理配置（**预解析文件**开关、知识库关联），对解析后的文件内容进行处理。检索场景下，解析结果会结合用户意图和知识库内容进行复杂规划和检索。开启**预解析文件**时，通过解析器获取文件内容传给智能体用于回复，超长内容自动截断。
3.  **智能问答**：大模型结合文件内容和用户问题，生成准确、相关的答案。

## 适用范围

### 支持的地域

本文档仅适用于中国大陆版（北京地域）。

### 支持的模型

文本类文档问答无特殊模型要求；处理图片等视觉类文件时，需选择千问 VL 系列等多模态模型，图片处理方式参见[特定模型图片处理配置](https://help.aliyun.com/zh/model-studio/file-q-a#ebc0edfb8a3xq)。

**说明**数据更新可能存在延迟，模型的支持情况以智能体应用内显示为准。

**文本生成模型**

-   [选择模型](raw/model-user-guide/get-started-with-models/models.md)、[选择模型](raw/model-user-guide/get-started-with-models/models.md)、[选择模型](raw/model-user-guide/get-started-with-models/models.md)、[选择模型](raw/model-user-guide/get-started-with-models/models.md)
-   [千问3-Coder-Plus](raw/model-user-guide/get-started-with-models/models.md)
-   [千问3开源模型](raw/model-user-guide/get-started-with-models/models.md)、[千问2.5开源模型](raw/model-user-guide/get-started-with-models/models.md)、[千问2开源模型](raw/model-user-guide/get-started-with-models/models.md)
-   [千问-QwQ](raw/model-user-guide/get-started-with-models/models.md)、[千问-QwQ-Preview](raw/model-user-guide/get-started-with-models/models.md)
-   [选择模型](raw/model-user-guide/get-started-with-models/models.md)

[视觉理解模型](raw/model-user-guide/get-started-with-models/models.md)

-   千问VL-Max、千问VL-Plus、千问VL-OCR

### 支持的文件格式

**说明**

-   单个会话支持上传的文件上限 10 个，且单文件不超过 10MB。
-   上传的文件仅在**当前会话**中有效，刷新或关闭页面将导致文件丢失。请及时完成所需操作。

支持上传本地的文档、图片、视频或音频，格式要求为：

-   **文档**：`.doc`、`.docx`、`.ppt`、`.pptx`、`.xls`、`.xlsx`、`.md`、`.txt`、`.pdf`
-   **图片**：`.png`、`.jpg`、`.jpeg`、`.bmp`、`.gif`
-   **视频**：`.mp4`、`.mkv`、`.avi`、`.mov`、`.wmv`、`.webm`、`.flv`
-   **音频**：`.aac`、`.amr`、`.flac`、`.m4a`、`.mp3`、`.mpeg`、`.ogg`、`.opus`、`.wav`、`.wma`

对于需要处理超过 10MB 文件的场景，推荐使用文件上传 API，详见本文的 [API 参考](https://help.aliyun.com/zh/model-studio/file-q-a#25a34d7090ck8)章节。

## 如何使用

文件问答的处理方式由智能体应用**规划**区的**预解析文件**开关与**知识库关联**共同决定：

处理方式

配置

行为

适合场景

**全文理解**

预解析文件**开启**

上传的文档、图像、视频、音频文件经预置解析器解析，文本内容直接提供给模型，模型基于完整文件内容回复。

文档总结、全文翻译、风格润色等全局理解任务

**检索问答**

关联知识库

上传文件与知识库内容一同参与检索，基于召回的最相关片段生成回答。

长文档问答、需要精确定位信息来源的场景

**自定义处理**

预解析文件**关闭**

文件 URL 直接透传给模型，由模型结合已配置的工具（[插件](raw/application-user-guide/agent-development/llm-application/plug-in/plug-in-overview.md)、[MCP](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp#8319d03864jym) 等）自行处理。

图片风格转换、视频内容分析等需要工具参与的任务

### 配置步骤

1.  在[智能体应用](https://bailian.console.aliyun.com/flow-agent/app-center)中选择一个模型。
2.  按需在**规划**区设置**预解析文件**开关：开启则解析文件内容传给模型，关闭则文件 URL 向后透传。
3.  （可选）如需文件与知识库混合问答，在**知识库**模块中关联知识库，详见[新版智能体应用（Agent 2.0）](raw/application-user-guide/agent-development/llm-application/new-single-agent-application.md)或[智能体应用（Agent 1.0）](raw/application-user-guide/agent-development/llm-application/single-agent-application.md)。
4.  （可选，自定义处理）在**工具**下添加所需的工具。工具区提供基础工具、Connector、应用组件和 MCP 服务；插件需先转换为 MCP 服务后接入。

**说明**开启**预解析文件**时，通过解析器获取文件内容传给智能体用于回复，超长内容自动截断。对于超长文件，建议关联知识库并以检索方式处理。

### 上传文件并对话

在右侧测试对话窗口输入框旁点击上传图标，上传本地文件后，即可围绕文件内容进行对话。

**示例一：全文理解**

上传[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/faqsct/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)，提问：“请帮我总结这个文件的内容。”

AI 助手返回文件摘要：该文档为智能手机产品介绍，涵盖阿里云百炼、通义、星尘等品牌旗下六款机型，包含产品概览表格，列出型号、主要特点、屏幕及存储/内存信息。

**示例二：仅检索当前上传文件**

上传[阿里云百炼系列手机产品介绍.docx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250414/faqsct/%E7%99%BE%E7%82%BC%E7%B3%BB%E5%88%97%E6%89%8B%E6%9C%BA%E4%BA%A7%E5%93%81%E4%BB%8B%E7%BB%8D.docx)，提问：“请帮我推荐一款5000元左右的手机。”

系统从上传文件中执行知识检索，返回 4 条检索结果（得分分别为 0.99、0.47、0.46、0.44），AI 基于检索到的文件内容生成手机推荐回复（如“阿里云百炼 X1”，售价 4599-4999 元，含屏幕、性能、续航、影像等核心亮点）。

**示例三：文件与知识库混合检索**

先在知识库中存入一份视频文件，然后在输入框旁点击上传图标上传 [test.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250922/ltuaji/test.mp4)，提问：“这个视频中的人物有没有出现在知识库中？”

系统执行知识检索，返回两条结果。AI 助手综合对比后判定视频中的真人角色与知识库中的动漫风格插画角色不匹配，回复“视频中的人物没有出现在知识库中”。

### 特定模型图片处理配置

选择[千问VL系列模型](raw/model-user-guide/model-experience/vision-model/vision.md)并上传图片文件后，可对图片的处理方式进行配置：

-   **模型处理**：模型仅使用自己的视觉能力来分析图片并直接回答，不会调用外部工具。适用于“看图问答”。
-   **模型处理 + 规划**：模型在看懂图片后，会判断是否需要调用已配置的外部工具（如插件）来完成更复杂的任务。适用于需要编辑、转换或借助工具分析图片的场景。

对于图片之外的其他文件（文档、音视频等），模型将自主判断是否需要调用工具处理。

**示例四：自定义处理**

智能体配置：

1.  选择**千问VL系列模型**，将图片处理方式设为**模型处理 + 规划**。
2.  在**工具**处添加**人物风格重绘**工具。

使用：上传示例文件 [girl.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250922/lnfliw/girl.png)，提问：“帮我把这张图的画风转为炫彩卡通风格。”

智能体调用 `MCP: bailian_image_style_repaint` 工具执行完成，成功将上传的人物照片转换为炫彩卡通风格图片。

## API 参考

### 前提条件

1.  **应用发布**：调用 API 前，请确保应用已在控制台发布。
2.  **处理方式**：文件按照智能体应用中保存的配置（**预解析文件**开关、知识库关联）进行处理，API 调用时无法动态切换处理方式。

### 调用限制

文件问答功能的 API 调用遵循其所属**智能体应用**的统一限流策略。

-   **单应用**：默认调用频率上限为 **100 QPS**（每秒请求数），按应用 ID（`app_id`）统计，涵盖对该应用的全部 API 请求（包括文件问答调用）。
-   **账号维度**：默认调用频率上限为 **15000 QPM**（每分钟请求数），涵盖同一阿里云主账号下全部应用的全部 API 请求。
-   超出阈值的请求会被拒绝并返回 HTTP 429，错误码为 `Throttling.RateQuota`，通常在一分钟内自动恢复，详见[错误码](raw/model-api-reference/preparations/error-code.md)。

### 文件传递方式和参数说明

文件传递方式

API 参数

主要用途 / 特点

通过 `image_list` 参数传递图片 URL

`image_list`

进行**图片检索、视觉理解**，单文件大小限制 10MB。

通过 `file_list` 参数传递通用文件 URL

`file_list`

传递通用文件的 URL。**预解析文件**开启或关联知识库时，系统会提取并使用文件文本；**预解析文件**关闭时，模型将接收原始文件 URL 以调用工具。单文件大小限制 10MB。

通过文件上传 API 接口

`parameters.session_file_ids`

**生产环境推荐。** 流程：1. 依次调用 ApplyFileUploadLease、AddFile 接口上传文件，获取以 `file_session_` 开头的会话文件 ID。2. 在对话 API 请求的 `parameters` 对象中通过 `session_file_ids` 传入该 ID（Java SDK 中为 `sessionFileIds`）。优点：支持更大文件，传输更稳定。

**更多调用信息请参考**：[上传文件（文档、图片、视频或音频）](https://help.aliyun.com/zh/model-studio/call-single-agent-application#30619780ddy93)。

## 计费说明

-   **上传文件**：文件上传操作本身不收取费用。
-   **模型调用**：基于文件内容进行问答会消耗模型的输入和输出 Token，按所选模型的标准计费，详情请参考[选择模型](raw/model-user-guide/get-started-with-models/models.md)。不同模式下输入 Token 的计算方式不同：
    -   **全文引用模式**：会将整个文件内容（或截断后的内容）作为输入传递给模型，因此输入 Token 消耗较大。
    -   **切片检索模式**：仅将用户问题和检索到的最相关文本片段作为输入，输入 Token 消耗通常远小于全文引用模式，更适合处理长文档。
    -   **自定义处理模式**：Token 消耗取决于模型与工具交互的复杂性，包括理解用户指令、调用工具、总结工具返回结果等环节。
-   **工具调用**：部分工具收费，具体费用在工具详情页展示。

## 常见问题

如何为 API 提供公网可访问的文件 URL？

推荐使用[阿里云对象存储 OSS](https://help.aliyun.com/zh/oss/user-guide/simple-upload#a632b50f190j8)，它提供了高可用、高可靠的存储服务，并且可以方便地生成公网访问 URL。

请确保您提供的 URL 可被阿里云百炼的服务正常访问：可在浏览器或通过 curl 命令访问该 URL，确保文件能够成功下载。

文件的有效期是多久？

-   **通过聊天窗口上传**：仅在**当前会话**中有效，关闭、刷新页面或会话超时都将导致文件失效。
-   **通过文件上传 API（**`session_file_ids`**）**：仅在当前会话内有效，会话关闭后文件过期，最长有效期为 7 天，不支持长期保存。
-   **通过 URL（**`image_list`**、**`file_list`**）**：文件的可访问性由您提供的 URL 自身决定。

为什么我的文件上传失败？

上传失败可能由多种原因导致：

-   **文件本身**：检查文件大小、格式是否符合[支持的文件格式](https://help.aliyun.com/zh/model-studio/file-q-a#ec857a7815nnc)。
-   **网络问题**：检查您的网络连接以及到服务终端节点的网络连通性。
-   **URL 方式**：确认 URL 公网可访问，且非临时签名 URL。
-   **API 调用**：检查请求认证信息及参数格式是否正确。
-   **错误信息**：仔细阅读 API 返回的错误响应体，它通常会指出具体问题。

为什么模型的回答不完整或不准确？

可能的原因：

-   **内容截断**：文件内容被 Token 限制截断。开启**预解析文件**时，通过解析器获取文件内容传给智能体用于回复，超长内容自动截断。对于超长文件，建议关联知识库并以检索方式处理。
-   **提问模糊**：提问不够具体，建议明确指出需要的信息类型，以便模型更好地理解您的意图。
-   **检索效果不佳**：关联知识库检索时，回答不准确可能是以下两点：1、检索到的相关片段不佳；2、切片策略不当。可优化提问使其更具指向性，或调整知识库的检索配置。
-   **文件内容质量不佳**：解析器可能难以处理低清晰度的扫描件、包含复杂表格/公式的文档、或编码不规范的文本文件。请尽量提供内容清晰、结构简单的源文件。

主账号的子业务空间在智能体应用中选择模型时显示未授权？

子业务空间需获得主业务空间对指定模型的授权，请参考授权子业务空间模型调用指南。
