# 应用功能动态

## **公告通知**

-   [阿里云百炼知识库商业化公告](https://www.aliyun.com/notice/117726)
    

## **功能动态**

> 关于阿里云百炼模型的动态信息，请参见[模型上下架与更新](https://help.aliyun.com/zh/model-studio/newly-released-models)和[模型平台功能更新](https://help.aliyun.com/zh/model-studio/model-release-notes)。

### **2026年**

**2月**

**日期**

**功能模块**

**功能点**

**功能说明**

2月10日

知识库

知识库支持订阅计费资源包

知识库提供后付费（按量付费）和[资源包](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#a06c023507qq3)两种计费方式。资源包可前往控制台[RAG标准版资源包](https://common-buy.aliyun.com/?commodityCode=sfm_ragservicestandard_dp_cn)或[RAG旗舰版资源包](https://common-buy.aliyun.com/?commodityCode=sfm_ragserviceenterprise_dp_cn)开通。详情请参见[知识库计费说明](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base)。

2月6日

应用评测

新版应用评测

支持智能体、工作流和自定义三种类型的评测集，构建适合业务需求的评测体系。详情请参见[新版评测集](https://help.aliyun.com/zh/model-studio/new-version-of-evaluation-set)。

**1月**

**日期**

**功能模块**

**功能点**

**功能说明**

1月31日

长期记忆

上线新版 长期记忆&用户画像管理 API

[长期记忆（新）](https://help.aliyun.com/zh/model-studio/long-term-memory-2-0)相比[长期记忆（旧）](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-dir-long-term-memory/)的改进：

-   通过开放的 API 接口，可接入任意应用，也支持多应用共享同一记忆库。
    
-   速度与效率高：拥有更低的延迟，更高的记忆检索召回效果。
    
-   自动提取能力：支持从对话中自动提取关键信息，自动去重，无需手动输入。
    
-   检索算法优化：新增语义检索能力，检索准确性显著提升，响应速度更快。
    
-   用户画像能力：新增完整的用户画像提取和管理能力。
    

1月30日

知识库

支持通过API创建音视频知识库

使用此API可创建两类知识库：基于文档或音视频的非结构化知识库，以及用于数据查询或图片问答的结构化知识库。详情请参见[CreateIndex - 创建知识库](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-createindex)。

1月23日

工作流应用

新增多模态生成节点

多模态生成节点用于调用阿里云多模态模型，根据配置的提示词和参数生成图像、视频或音频内容。

1月19日

知识库

增加知识库监控API

查询指定知识库在特定时间范围内的监控数据。详情请参见[GetIndexMonitor - 获取知识库监控数据](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-getindexmonitor)。

1月19日

知识库

增加更新知识库API

更新指定知识库的部分配置。详情请参见[UpdateIndex - 更新知识库](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-updateindex)。

1月15日

工作流应用

新增异步运行模式

-   文本生成模式下，新增异步运行模式。
    
-   异步运行模式下，工作流会在后台执行。系统会立即返回Task ID，可通过Task ID查询任务执行结果。在[任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center)中可以查看历史异步任务。
    

1月10日

知识库

支持子账号开通知识库，支持分账管理

如果您需要将费用归属到不同的部门或项目，可以使用“标签”功能对业务空间进行标记进行分账管理。详情请参见[分账管理](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#48ad5a9cd3cjr)。

1月6日

知识库

支持调整知识库检索过程初步召回参数

通过降低**初步向量检索TopK**和**初步关键词检索TopK**的数值，可减少送入排序模型的 Token 量，从而显著降低成本。详情请参见[模型调用费用](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#eef4441635v0f)。

1月4日

知识库

知识库商业化计费

阿里云百炼知识库服务自 2026 年 1 月 4 日起正式开始计费。总费用构成为规格费用和模型调用费用两部分。详情请参见[知识库计费说明](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base)。

### **2025年**

**12月**

**日期**

**功能模块**

**功能点**

**功能说明**

12月26日

智能体应用

上线新版智能体应用（Agent 2.0）

-   [新版智能体应用](https://help.aliyun.com/zh/model-studio/new-single-agent-application)将知识库、MCP 统一为工具，由智能体自主规划在何时、以何种顺序进行调用。能完整展示模型思考和工具调用的全过程。
    

12月25日

知识库

支持音视频知识库

-   支持上传音视频文件创建知识库，可实现：
    
    -   基于音视频内容的智能检索与问答，如直播回放问答、课程助教、客服质检等；
        
    -   对音视频素材进行二次创作，如生成脚本和字幕、给出剪辑建议等。
        
    
    详情请参见[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。
    

12月17日

工作流应用

知识库节点支持不同调用方式

-   知识库节点支持必定调用、智能调用和旧版调用三种调用方式，支持解析文档、图片、表格类型的知识库。
    

**11月**

**日期**

**功能模块**

**功能点**

**功能说明**

11月28日

工作流应用

新增多模态数据节点，开始节点新增 file 类型参数

-   新增文档解析、图片解析、视频解析和音频解析四个节点，用于提取对应输入文件的结构化参数。
    
-   开始节点新增 file 类型参数，用于上传文件
    

11月3日

应用调用

支持通过Responses API 调用阿里云百炼应用

-   同步调用 API：适用于需要即时获取结果的实时交互场景，可轻松复用现有的 OpenAI 代码库，或快速集成来自 OpenAI 生态的各类工具。详情请参见[同步调用 API 参考](https://help.aliyun.com/zh/model-studio/synchronous-call-api-reference)。
    
-   异步调用 API：对于耗时较长的任务，只需在请求中设置 background 为 true，API 便会立即返回一个任务 ID，用于后续的查询与管理。详情请参见[异步调用 API 参考](https://help.aliyun.com/zh/model-studio/asynchronous-call-api-reference)。
    

**9月**

**日期**

**功能模块**

**功能点**

**功能说明**

9月24日

高代码应用

新的应用类型

-   支持基于Python项目结构部署AI后端服务，内置自动化运维、可观测性及日志服务等企业级能力。使用方法请参见[高代码应用](https://help.aliyun.com/zh/model-studio/rich-code-application/)。
    

9月23日

工作流应用

新增 Dify 工作流一键导入

-   支持 Dify 工作流一键导入，导入后自动映射节点类型与参数。使用方法请参见[工作流导入/导出](https://help.aliyun.com/zh/model-studio/workflow-application/#5c0d7e6950p7i)。
    

9月23日

智能体应用

文件问答升级

-   支持全文引用、切片检索和自定义处理三种模式，对文档、图片、音视频等多种文件进行深度分析和自动化任务处理。使用方法请参见[文件问答](https://help.aliyun.com/zh/model-studio/file-q-a)。
    

9月23日

智能体应用

回复功能升级

-   当主模型在特定场景下表现受限时，将自动切换至更优模型。详情请参见[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)。
    

9月23日

知识库

数据导入流程简化

-   创建知识库时，可直接导入文件或数据，无需预先在应用数据页面导入。
    

9月23日

知识库

数据源支持DMS

-   创建知识库时，可直接从 DMS 指定数据表同步数据，详情请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。
    

9月23日

知识库

创建流程优化

-   根据应用场景，将知识库类型分为**文档**、**数据**和**图片**三类，以简化创建过程，详情请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。
    

9月23日

知识库

新增调试面板

-   编辑智能体应用时，可直接在线调整知识库参数，并实时验证检索召回效果。使用方法请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。
    

**8月**

**日期**

**功能模块**

**功能点**

**功能说明**

8月13日

MCP

新增外部调用功能

-   集成至第三方应用：支持一键自动配置到第三方应用，快速实现外部调用。
    
-   集成至个人项目：通过 MCP SDK 调用，实现灵活编码和深度定制。
    

8月12日

工作流应用

界面升级

-   智能体编排应用下线。
    
-   工作流应用界面升级。
    

**7月**

**日期**

**功能模块**

**功能点**

**功能说明**

7月28日

知识库

知识库数据源支持自建MySQL

-   结构化知识库支持从自建MySQL给定数据表同步数据。配置方法详见[集成MySQL数据至知识库](https://help.aliyun.com/zh/model-studio/connect-to-rds-for-knowledge-base)。
    

7月28日

知识库

知识库支持text-embedding-v4模型

-   text-embedding-v4模型在语种支持、代码片段向量化效果和向量维度选择等方面，相比v3模型进行了全面升级，适用于大部分场景。
    

**5月**

**日期**

**功能模块**

**功能点**

**功能说明**

5月22日

知识库

知识库支持text-embedding-v3模型

-   text-embedding-v3模型在语种支持、输入长度和向量维度自定义等方面，相比v2模型进行了全面升级，适用于大部分场景。
    

5月12日

知识库

导入图片可选择Qwen VL进行解析

-   您可选择qwen-vl-max或qwen-vl-plus模型，通过传入Prompt指引需识别的版面、元素和内容，适用于解析复杂图片或图表，详情请参见[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。
    

5月8日

知识库

非结构化知识库支持导入离线HTML文件

-   支持基于离线HTML文件构建非结构化知识库，详情请参见[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。
    

**4月**

**日期**

**功能模块**

**功能点**

**功能说明**

4月10日

知识库

新增权重设置功能

-   当智能体应用同时关联多个知识库时，您可以按信息源的重要性为每个知识库设置权重。系统将优先召回权重更高的知识库中的相关信息。使用方法请参见[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)。
    

4月9日

MCP

新增MCP市场与MCP管理功能

-   您可以开通阿里云百炼预置的MCP服务或部署自定义MCP服务，并在智能体应用和工作流应用中引用这些 MCP 服务，使应用具备更强大的能力。使用方法请参见[官方 MCP 服务](https://help.aliyun.com/zh/model-studio/official-and-third-party-mcp)和[自定义MCP服务](https://help.aliyun.com/zh/model-studio/custom-mcp)。
    

4月1日

智能体应用

[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)支持QwQ系列模型

> 不包括插件、流程、音视频交互能力

-   [QwQ](https://help.aliyun.com/zh/model-studio/deep-thinking)模型具有强大的推理能力，模型会先输出思考过程，再输出回答内容。数学/代码能力（AIME 24/25、LiveCodeBench）及通用指标（IFEval等）达DeepSeek-R1满血版水平，显著优于同源精简版DeepSeek-R1-Distill。
    

**3月**

**日期**

**功能模块**

**功能点**

**功能说明**

3月25日

工作流应用

[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)大模型节点支持qwq-plus、qwq-32b模型

-   [QwQ](https://help.aliyun.com/zh/model-studio/deep-thinking)模型具有强大的推理能力，模型会先输出思考过程，再输出回答内容。数学/代码能力（AIME 24/25、LiveCodeBench）及通用指标（IFEval等）达DeepSeek-R1满血版水平，显著优于同源精简版DeepSeek-R1-Distill。
    

3月24日

智能体应用

[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)检索配置新增 “多模态回复增强”开关

-   开启多模态识别能力，使智能体应用能够解析知识库中的图表与图像内容，提供结合视觉信息的精准回答。
    

3月18日

智能体应用

[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)支持qwen-vl-plus-latest、qwen-vl-plus-2025-01-25

-   qwen-vl-plus-latest始终等同最新快照版。
    
-   qwen-vl-plus-2025-01-25，又称qwen-vl-plus-0125。此版本属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列模型，扩展上下文至128k，显著增强图像和视频的理解能力。
    

**2月**

**日期**

**功能模块**

**功能点**

**功能说明**

2月24日

工作流应用

工作流应用支持批量节点

-   批量节点是[工作流](https://help.aliyun.com/zh/model-studio/workflow-application/)中用于处理批量任务的功能节点，详情请参见[批处理](https://help.aliyun.com/zh/model-studio/workflow-application/#b66db1f209yzt)。
    

2月18日

工作流应用

工作流应用支持 DeepSeek 系列模型

-   [工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/)可使用 DeepSeek 系列模型构建任务型和对话型工作流。
    

2月18日

智能体应用

智能体应用支持 DeepSeek 系列模型

-   [智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)可集成 DeepSeek 系列模型，并结合知识库、长期记忆和 Prompt 模板，构建私有知识问答应用。
    

### **2024年**

**12月**

**日期**

**功能模块**

**功能点**

**功能说明**

12月16日

工作流应用

工作流画布功能优化

-   意图分类节点支持选择意图模式：
    
    -   单选模式：大模型将从现有的意图配置中挑选最合适的意图作为输出。
        
    -   多选模式：大模型将从现有的意图配置中挑选所有匹配的意图作为输出。
        
    
-   文本转换节点支持JSON格式输出。
    

详情请参见[工作流应用](https://help.aliyun.com/zh/model-studio/workflow-application/#fb1d023cadqq5)。

12月16日

智能体编排应用

智能体编排应用支持条件判断节点

-   智能体编排应用支持条件判断节点。详情请参见[智能体编排应用](https://help.aliyun.com/zh/model-studio/multi-agent-application)。
    

12月10日

工作流应用

新增“音视频实时互动”

-   可将图文对话类应用轻松转为音视频实时互动应用。
    
-   提供 H5/APP 调试窗口，可通过音视频 SDK 发布到用户的 WEB/iOS/Android 应用中。
    

12月10日

智能体应用

新增“音视频实时互动”

-   可将图文对话类应用轻松转为音视频实时互动应用。
    
-   提供 H5/APP 调试窗口，可通过音视频 SDK 发布到用户的 WEB/iOS/Android 应用中。
    

12月3日

应用组件

新增Prompt样例优化文档

-   大量实践表明，FewShot方法在提升大模型的推理效果和性能方面具有显著的助益。Prompt样例库功能作为阿里云百炼的FewShot能力，通过录入用户输入（Query）和期望的模型回复（Answer）作为样例信息源，在模型调用时根据用户输入，检索召回相关样例信息，以此作为输出参考，从而提高大模型的回答准确性，适用于客服及问答等场景。详情请参见[Prompt样例库](https://help.aliyun.com/zh/model-studio/prompt-sample-optimization/)。
    

**11月**

**日期**

**功能模块**

**功能点**

**功能说明**

11月27日

应用分享

新增微信、钉钉分享渠道

-   支持创建钉钉AI机器人和微信公众号AI机器人，创建完成后，您可以按需将AI机器人回调地址或二维码分享给目标用户。详情请参见[应用分享](https://help.aliyun.com/zh/model-studio/share-an-application#40bff17c8bk2p)。
    

11月1日

知识库

非结构化知识库支持导入Excel文档

-   除了结构化知识库，非结构化知识库也支持导入Excel文档，适用于：
    
    -   导入的文档可能包括非Excel格式（例如pdf、doc等）；
        
    -   导入多个具有不同表结构的Excel文档。
        
    
    详情请参见[知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#6028cfefaauhu)。
    

**10月**

**日期**

**功能模块**

**功能点**

**功能说明**

10月24日

应用观测

新增应用观测能力

-   新增的[应用观测](https://bailian.console.aliyun.com/knowledge-base#/app-observe)支持端到端查看阿里云百炼应用的处理流程，详情请参见[用量监控与性能分析](https://help.aliyun.com/zh/model-studio/application-observation)。
    

10月24日

SFM服务关联角色

新增AliyunServiceRoleForSFMTelemetry角色

-   用于阿里云百炼应用观测的服务关联角色，应用观测使用此角色来访问您的OpenTelemetry实例。单击[SFM服务关联角色](https://help.aliyun.com/zh/model-studio/bailian-service-linked-role#4223df3814svi)查看。
    

**9月**

**日期**

**功能模块**

**功能点**

**功能说明**

9月29日

SFM服务关联角色

新增AliyunServiceRoleForSFMAccessingMNS角色

-   用于OSS变更自动同步的服务关联角色，阿里云百炼数据中心使用此角色来访问您在MNS队列中的OSS变更消息。单击[服务关联角色](https://help.aliyun.com/zh/model-studio/bailian-service-linked-role)查看。
    

9月25日

知识库

结构化知识库数据源支持云上数据库

-   结构化知识库的数据源支持云数据库RDS。具体说明请参见[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#70b5d361ed01j)。
    

非结构化知识库支持自定义metadata

-   支持为非结构化知识库中的文档附加metadata，以提升知识库检索的效率和精准度。具体说明请参见[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#65f260310fz0l)。
    

支持图文检索

-   知识库支持解析文档中的图片，结构化文档中的图片将被转为向量，非结构化文档中的图片将被提取文字然后再转为向量。具体说明请参见[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#b3c78a1ef11wi)。
    
-   如果智能体应用关联的结构化知识库包含图片索引，可以在提问时上传图片，与输入图片相关的数据记录会与提问一起提供给大模型。具体说明请参见[智能体应用](https://help.aliyun.com/zh/model-studio/single-agent-application)。
    
-   测试知识库页面同样支持了图文输入，便于您评估知识库的图文检索能力。具体说明请参见[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#96a228f196y1b)。
    

9月17日

数据管理

非结构化数据文件支持标签分类

-   非结构化数据支持标签分类，点击[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base)查看详情。
    

9月4日

应用中心

智能体应用新增“检索配置”功能

-   智能体应用中，打开“知识检索增强”开关后，增加“检索配置”功能，用于设置大模型的回答范围、是否展示回答来源等。点击[创建和使用知识库](https://help.aliyun.com/zh/model-studio/rag-knowledge-base#04fac0b0438j5)查看完整信息。
    

**8月**

**日期**

**功能模块**

**功能点**

**功能说明**

8月27日

数据管理

结构化数据能力更新

-   结构化数据支持增量导入、支持设置表头数据类型，请点击[数据管理](https://bailian.console.aliyun.com/#/data-center)进行体验。
    

8月26日

应用中心

新增自定义参数的调用说明

-   调用工作流应用和智能体编排应用时，需要传入自定义参数，详情请参见[应用调用](https://help.aliyun.com/zh/model-studio/application-calling-guide#f26019986182v)。
    

8月26日

应用中心

新增自定义参数的透传示例

-   调用工作流应用和智能体编排应用时，需要传入自定义参数。点击，查看“请求参数（工作流和智能体编排应用的参数透传）”中内容。
    

8月24日

应用中心

新增自定义参数的传入说明

-   调用工作流应用和智能体编排应用时，需要传入自定义参数。点击[自定义节点参数传递](https://help.aliyun.com/zh/model-studio/pass-through-of-application-parameters#uPwcs)查看完整信息。
    

8月23日

应用中心

新增应用类型

-   新增应用-**流程编排应用**，点击[应用流程编排应用](https://bailian.console.aliyun.com/?accounttraceid=04966e8c43324e508d4aa5e02268236ccabs#/app-center)进行体验。
    

8月22日

应用广场

新增传媒/零售文章风格与格式学习、电商零售推广文案写作应用

-   点击[应用广场](https://bailian.console.aliyun.com/#/app-market)进行体验，点击[传媒/零售文章风格与格式学习](https://help.aliyun.com/zh/model-studio/media-retail-article-style-and-format-learning)、[电商文案智能可控生成](https://help.aliyun.com/zh/model-studio/intelligent-and-controllable-generation-of-e-commerce-copywriting)查看完整信息。
    

8月22日

应用中心

应用模型展示更新

-   ​我的应用中选择模型后，**展示最大长度数据**。
    

8月22日

应用中心

智能体应用能力更新

-   智能体应用**支持多函数调用**，**支持循环调用的打断**。
    

8月14日

应用中心

应用测试窗新增测试能力

-   应用测试窗**支持长期记忆用户洞察和用户画像**，点击[我的应用](https://help.aliyun.com/zh/document_detail/2782133.html)查看完整信息。
    

8月12日

插件管理

新增内置插件类型

-   新增生成二维码、GitHub搜索插件内容。
    

**7月**

**日期**

**功能模块**

**功能点**

**功能说明**

7月30日

应用中心

创建自定义应用支持qwen2模型

-   创建自定义应用支持​**qwen2-72b-instruct**​，​**qwen2-57b-a14b-instruct模型。**​
    

7月24日

数据中心

知识索引更新

-   知识索引支持召回命中测试，点击[知识索引](https://help.aliyun.com/zh/model-studio/knowledge-index)查看详情。
    

7月23日

应用广场

自定义应用支持分享

-   已发布的应用支持分享Web端（PC/h5）。
    

> **API调用**：即现有的API调用方式，无论应用是否配置，API 调用都会发布。>

> **Web(PC/h5)**：基于阿里云百炼现有的页面及魔笔的模板内容进行搭建。

> **官方分享渠道**：为您提供应用的测试 Web 页面，仅支持小范围分享体验。

**魔笔分享渠道**：魔笔是一个低代码开发平台，提供多种模板，灵活选用，支持定制用户交互界面和自定义域名，轻松发布生产级 Web 应用。 >"

7月19日

数据管理

OSS授权方式更新

-   数据管理中的文档数据支持本地上传和OSS导入两种模式，**在关联OSS文件存储Bucket后**，**可实现OSS授权及跨域访问。**点击[从OSS导入数据](https://help.aliyun.com/zh/model-studio/oss-data-import-guide)查看详情。
    

7月18日

应用中心

插件服务

-   应用中心支持**自定义参数**透传点击[应用的参数传递](https://help.aliyun.com/zh/model-studio/pass-through-of-application-parameters)查看详情。
    

7月8日

开发指南

知识索引新增权限控制

-   阿里云主账号或RAM管理员给RAM用户授权后，RAM用户才能使用阿里云百炼知识索引能力。点击[知识索引自定义权限策略](https://help.aliyun.com/zh/model-studio/use-and-authorize-ram-user#efdb989adcx52)查看完整信息。
    

7月3日

数据管理

支持上传 Excel格式文件

-   支持结构化数据导入，并且支持自定义设置结构列信息。点击[数据导入](https://help.aliyun.com/zh/model-studio/data-import-instructions)查看详情。
    

7月3日

应用中心

支持结构化数据构建知识库及RAG在线推理

-   支持结构化和非结构化数据构建及关联知识库并进行知识检索。点击[知识索引](https://help.aliyun.com/zh/model-studio/knowledge-index)查看详情。
    

**6月**

**日期**

**功能模块**

**功能点**

**功能说明**

6月20日

应用广场

应用中心

-   新建的应用支持测试版本，编辑应用后默认保存为测试版本。
    

6月20日

应用广场

流程管理

-   流程画布支持业务参数透传，点击[流程编排（旧版待下线）](https://help.aliyun.com/zh/model-studio/manage-processes-old/)查看详情。
    

6月13日

数据中心

新增数据增强能力

-   数据增强支持通过参数配置及prompt配置对数据进行增强处理，提升处理数据效果。
    

6月5日

数据中心

数据管理支持多种格式上传

-   数据管理新增支持md、txt、ppt、pptx文件的导入和解析，以及页面预览。
    

6月5日

数据应用

知识索引支持切片管理

-   支持切片的管理（开关、内容编辑）。
    

**5月**

**日期**

**功能模块**

**功能点**

**功能说明**

5月3日

我的应用

新增多模型创建应用

-   全新应用创建流程，基于Assistant API机制的RAG、工作流、插件调度机制。
    
-   max、plus、turbo多模型选择，多维效果/成本配置。
    
-   全新Memory长期记忆机制，支持长期记忆存储，个性化Assistant效果。点击[我的应用](https://help.aliyun.com/zh/model-studio/application-building-instructions)查看详情。
    

数据管理

新增平台统一的数据管理模块

-   全新统一数据管理能力，支持本地数据上传、OSS数据导入，支持大批量非结构化文档导入。
    
-   一键IDP解析为可应用数据，支持多类目管理。
    

知识索引

创建和管理用于RAG应用的知识库索引，基于对数据中心的统一引用

-   基于LLamaindex提供完整知识索引配置，包括Chunk切分、向量配置。
    
-   支持多种召回索引配置，满足不同粒度的RAG效果。
    

**3月**

**日期**

**功能模块**

**功能点**

**功能说明**

3月31日

应用工具

新增官方插件能力

-   上线新版插件中心，新增“**图片生成**”、“**夸克搜索**”、“**Python代码解释器**”和“**计算器**”四款官方插件，点击[插件中心](https://help.aliyun.com/zh/model-studio/plug-in-overview)查看详情。
    

3月31日

应用广场

智能体API应用支持API调用

-   新增[Assistant API](https://help.aliyun.com/zh/model-studio/api-agent)及[Python SDK](https://help.aliyun.com/zh/model-studio/sdk-agent)接口；点击[最佳实践](https://help.aliyun.com/zh/model-studio/prompt-engineering-guide)查看详情。
    

**2月**

**日期**

**功能模块**

**功能点**

**功能说明**

2月22日

企业知识库

新增企业检索链路

-   新增ES向量存储数据库，知识库名称为**默认知识库**，检索效果增强。详情查看。
    

2月22日

企业知识库

支持上传FAQ形式文件

-   新增上传Excel格式的文件，详情查看[配置企业知识库](https://help.aliyun.com/zh/model-studio/user-guide/configure-enterprise-knowledge-base)。
    

2月5日

企业知识库

新增上传格式

-   支持OSS上传文档，详情查看[配置企业知识库](https://help.aliyun.com/zh/model-studio/user-guide/configure-enterprise-knowledge-base)。
    

2月5日

Prompt工程

新增Prompt模板类型

-   新增**110个**Prompt模板。
    

2月1日

流程编排

新增流程编排版本

-   流程编排支持一键调整布局，优化流程画布交互体验。
    

**1月**

**日期**

**功能模块**

**功能点**

**功能说明**

1月30日

应用管理

新增会话记录备份

-   通过ADB-PG备份会话记录，支持手动关闭/开启。
    

1月24日

流程编排

新增流程画布版本

-   脚本节点是面向开发者提供简单的代码开发能力，新增Python语言。
    

1月24日

流程编排

流程画布增加大模型节点

-   大模型节点，用于关联包括但不限于官方模型、SFT模型，旨在使用大模型能力详情查看[LLM节点说明](https://help.aliyun.com/zh/model-studio/llm-node)。
    

1月15日

API相关

修复文档上传字段缺失

-   相关字段已更新，详情查看[应用调用SDK参考（旧）](https://help.aliyun.com/zh/model-studio/call-alibaba-cloud-model-studio-v1-through-sdk/)。
