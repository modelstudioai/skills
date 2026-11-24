# Agent 平台功能更新

Agent 各模块的功能更新、优化、问题修复与计费变更，按日期倒序排列。

### 2026-11-24

新增

#### RAG：Wiki 与本体知识图谱上线

##### 新功能

-   旗舰版文档知识库支持开启 Wiki 与本体知识图谱：一次解析同时生成可阅读、可检索的主题知识页面（Wiki Page）与知识关系视图。Wiki Page 构建独立索引参与检索召回；图谱数据本身不参与检索，用于知识浏览与关系展示。
-   支持配置抽取模型（qwen3.8-max、qwen3.8-flash、qwen3.7-plus）、提取粒度、Wiki 内容生成要求与提取重点，文档新增或修改后自动更新；支持在控制台新建、编辑、回滚和删除 Wiki Page，并查看历史版本。
-   知识检索新增 Wiki 检索服务，与 Chunk 检索并列；知识问答可同时使用普通知识检索与 Wiki 检索。
-   Wiki 抽取模型按实际输入/输出 Token 独立计费，不包含在知识库规格费用或知识库免费额度内。

详见[Wiki 与本体知识图谱](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-wiki.md)和[计费说明](https://help.aliyun.com/zh/model-studio/rag-wiki#h-ragwiki-billing)。

### 2026-11-11

新增修复

#### Evolution：多模态评测上线

##### 新功能

-   评测 - 多模态评测功能上线，支持添加包含多模态数据的评测集，选择多模态评估器，发起针对多模态数据的评测任务

##### 修复

-   修复轨迹评测任务不支持选择应用输出中轨迹数据的问题

详见[添加多模态评测数据](raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)和[评测任务](raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

### 2026-11-08

新增

#### Managed Agent：沙箱持久化

##### 新功能

-   沙箱持久化上线：创建会话时可选择保留沙箱的工作文件和环境修改，保留期内再次运行会话时恢复。默认关闭，快照保留时长默认 3 天，支持 1–30 天。详见[沙箱持久化](https://help.aliyun.com/zh/model-studio/managed-agents-session-operations#h-sandbox-persistence)。
-   沙箱持久化按快照存在时长计费，详见[计费说明](https://help.aliyun.com/zh/model-studio/managed-agents-billing#h-sandbox-persistence-fee)。
-   创建 Session API 支持 `sandbox`；Get Session 响应增加 `usage.sandbox`。详见[创建 Session](https://help.aliyun.com/zh/model-studio/session-create#h-sc-req)与[获取 Session](https://help.aliyun.com/zh/model-studio/session-get#h-sg-dto)。

### 2026-10-21

新增改进

#### Evolution：轨迹评测上线与评测交互优化

##### 新功能

-   评测 - 轨迹评测功能上线，支持创建包含轨迹数据的评测集，选择轨迹评估器，发起针对轨迹的评测任务
-   评测 - 创建评测集、添加评测集数据、预置评估器筛选交互逻辑优化

详见[添加轨迹评测数据](raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)和[评测任务](raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

### 2026-10-15

新增

#### Managed Agent：功能更新

##### 新功能

-   内置工具新增 `todo_write`：智能体可维护结构化的待办列表，拆解多步任务并跟踪每一步的状态。详见[Agent 工具配置](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
    
-   可选模型新增 `deepseek-v4.1-flash`、`deepseek-v4.1-flash-1017`、`glm-5.3`。详见[定义 Agent](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
    

### 2026-10-14

新增

#### Managed Agent：功能更新

##### 新功能

-   会话级 Agent 配置覆盖与 MCP 请求头：创建会话时可通过 `agent` 对象覆盖系统提示词、工具、MCP Server 与技能，并通过 `mcp_configs` 为指定 MCP Server 注入自定义请求头。详见[发起会话](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md)。

### 2026-10-08

新增

#### Managed Agent：功能更新

##### 新功能

-   环境预热：配置预装包的环境创建后可能需要预热，准备中的环境无法被会话引用。详见[云端托管环境](raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
    
-   智能模式：`model.id` 新增 `auto`、`performance`、`balanced`、`economy` 四档路由。详见[定义 Agent](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
    

### 2026-09-21

新增

#### Managed Agent：功能更新

##### 新功能

-   单个文件上传上限提升至 50 MB。详见[文件上传与挂载](raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)。

### 2026-09-20

新增

#### Managed Agent：功能更新

##### 新功能

-   定时任务（Scheduled Task，原部署）上线：绑定智能体后按 cron 表达式或手动触发运行，每次触发创建一个会话。详见[定时任务](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-deployment.md)。

### 2026-09-18

新增改进

#### Managed Agent：新增网页搜索与读取工具

##### 新功能

-   内置工具新增 `web_search` 与 `web_fetch`：`web_search` 搜索互联网信息，返回相关网页的标题、链接和内容摘要（0.03 元/次）；`web_fetch` 读取指定网页地址的正文内容并转换为文本（限时免费）。详见[Agent 工具配置](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

#### Evolution：Prompt 优化上线

##### 新功能

-   应用优化 - Prompt 优化功能上线，支持版本对比优化、调试反馈优化 Prompt

详见[应用优化](raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。

#### Security：安全模块上线

##### 新功能

-   Security 安全模块上线，提供安全内生、开箱即用的原生安全能力：Agent 上线即可获得默认防护，无需额外接入或改造。
-   提供防护总览、Agent 资产、安全策略、风险与审计等能力，形成“量·发现与盘点—挡·拦截与防护—记·审计与留痕”的安全闭环。
-   高级防护提供 7 项可按需启用的安全策略与风险监测能力，当前处于限时免费阶段。

详见[Security 用户指南](raw/application-user-guide/agent-governance/security-guide.md)。

### 2026-09-17

新增

#### Managed Agent：记忆库（Memory Store）上线

##### 新功能

-   记忆库（Memory Store）上线：跨会话持久化的挂载资源，记忆库—记忆—版本三层模型，创建会话时挂载（只读/读写），智能体通过文件工具读写，历史版本自动记录并支持查询与擦除。控制台**记忆库**页面与 Memory Store API 同步开放。详见[记忆库](raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md)与 [Memory Store API](raw/application-api-reference/managed-agents-api/memory-store-api.md)。

#### Evolution：告警管理上线

##### 新功能

-   告警管理上线

详见[告警管理](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)。

### 2026-09-09

新增变更

#### Managed Agent：功能更新

##### 新功能

-   会话事件流支持 Delta 增量推送：订阅时通过 `event_deltas[]` 为 `message`、`reasoning` 开启逐块流式输出。详见[会话事件流](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)。

##### 变更

-   内置工具 `download_file` 下线，由 `mark_artifacts` 替代，用于登记智能体产物。详见[Agent 工具配置](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

### 2026-09-07

新增

#### Managed Agent：用户消息支持多模态内容

##### 新功能

-   发送 Event 接口（`POST /sessions/{session_id}/events`）的用户消息 `content` 新增多模态内容块：`image`（`image_url` / `file_id`）、`video`（`video_url` / `file_id`）、`file`（`file_id` + `filename`）。图片与视频进入模型多模态视觉通道；文件由平台物化到会话沙箱文件系统，模型通过工具按需读取。详见[发送 Event](raw/application-api-reference/managed-agents-api/session-api/event-post.md)。

#### Managed Agent：功能更新

##### 新功能

-   会话支持环境变量：创建或更新会话时可传入 `environment_variables`，运行时按名读取。详见[发起会话](raw/application-api-reference/managed-agents-api/session-api/session-create.md)。

### 2026-09-04

新增

#### Managed Agent：密钥库出网替换配置

##### 新功能

-   密钥库新增**密钥替换生效域名**和**替换位置**配置。密钥以占位符 `${变量名}` 形式供智能体引用，请求出网时由网关在指定域名的 Authorization 头中替换为真实密钥，未匹配域名只收到占位符。详见[密钥库认证](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-credential.md)。

### 2026-08-26

新增

#### Managed Agent：Webhook 通知上线

##### 新功能

-   Webhook 通知上线，支持将会话、智能体、定时任务等资源的状态变更事件推送到指定回调地址。接入方式见 [Webhook 通知](raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-webhook.md)，接口契约见 [Webhook API](raw/application-api-reference/managed-agents-api/webhook-api.md)。

#### Sandbox：云端隔离沙箱上线

##### 新功能

-   Sandbox 上线，提供云端隔离沙箱环境，支持代码执行、浏览器操作与文件处理。
-   提供 `code-interpreter-v1`、`browser`、`all-in-one` 三种基础镜像。
-   支持通过控制台创建与管理模版，配置资源规格、文件挂载、网络策略、环境变量与生命周期。
-   兼容 E2B SDK/API 协议，支持实例生命周期管理与数据面操作。

详见[Sandbox 快速开始](raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)。

### 2026-08-24

新增

#### Managed Agent：功能更新

##### 新功能

-   百炼 CLI 支持 Managed Agent：可通过 `bl managed-agent` 管理 Agent、环境、会话等资源。详见[使用 CLI](raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)。

### 2026-08-18

新增

#### Managed Agent：功能更新

##### 新功能

-   多智能体协作上线：由 coordinator 智能体编排多个成员智能体协同完成任务。详见[多智能体协作](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
    
-   工具审批策略上线：可按工具设置总是允许或每次询问。详见[Agent 工具配置](raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
    

### 2026-08-17

计费

#### Managed Agent：正式商业化计费

-   Managed Agents 正式商业化计费，自 2026-08-17 09:00:00（UTC+8）起生效。计费项、免费额度与示例详见 [计费说明](raw/application-user-guide/agent-billing/managed-agents-billing.md)。

### 2026-08-10

新增

#### Evolution：文档上线

##### 新功能

-   Evolution 文档上线

详见[Evolution 快速开始](raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)。

### 2026-07-27

新增

#### RAG：知识库文档上线

##### 新功能

-   RAG 知识库文档上线

详见[RAG 快速开始](raw/application-user-guide/agent-context/knowledge-base/rag-start-using/quickstart.md)。

### 2026-07-21

新增

#### Managed Agent：文档上线

##### 新功能

-   Managed Agent 文档上线

详见[Managed Agent 快速开始](raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-quick-start.md)。

#### Managed Agent：功能更新

##### 新功能

-   Managed Agent 功能上线

### 2026-06-29

新增

#### 智能体托管：智能体托管运行时上线

新增智能体托管运行时 API，平台托管会话与工具执行，[了解详情](raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md)

### 2026-06-23

新增

#### 知识库RAG：知识检索服务上线

新增知识检索服务，支持多知识库联合检索与混合排序，[了解详情](raw/application-user-guide/agent-context/knowledge-base/service/rag-knowledge-retrieval.md)

#### 知识库RAG：知识问答服务上线

新增知识问答服务，基于大模型结合检索生成回答，[了解详情](raw/application-user-guide/agent-context/knowledge-base/service/rag-knowledge-qa.md)

### 2026-06-10

新增

#### Skill技能：Skill 能力包上线

新增 Skill 能力包，智能体可添加官方或自定义技能，[了解详情](raw/application-user-guide/agent-store/skill/introduction-to-skill.md)

#### 数据连接：数据连接模块上线

新增数据连接模块，支持 MySQL/语雀/OSS 等数据源，[了解详情](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/data-connection.md)

### 2026-06-01

新增计费

#### 应用 - 通义听悟 Agent：通义听悟 Agent 新增特惠 ASR 资源包

新增通义听悟 Agent 特惠 ASR 资源包，覆盖汽车销售/客户画像等场景，[了解详情](https://help.aliyun.com/zh/model-studio/purchase-and-use-discount-asr#2fe6db248dqwx)

#### Spring AI Alibaba：Spring AI Alibaba 调用百炼应用文档上线

新增使用 Spring AI Alibaba 框架调用百炼智能体、工作流应用文档，[了解详情](https://help.aliyun.com/zh/model-studio/spring-ai-alibaba-integrate-llm-application#26239bc5e4is9)

### 2026-05-21

新增

#### 应用组件 - 数据连接：数据连接新增 ListCategory 接口

数据连接新增 ListCategory 接口, 查询原应用数据类目列表，[了解详情](raw/_short/api-bailian-2023-12-29-listcategory-2521532ef3e828b3.md)

#### 通义听悟 Agent：通义听悟 Agent 工业生产指令转写 WebSocket 协议上线

通义听悟 Agent 工业生产指令转写新增 WebSocket 交互协议文档，[了解详情](https://help.aliyun.com/zh/model-studio/tingwu-industrial-instruction-api-websocket#a2ed5abb5bmgm)

### 2026-05-15

新增

#### 应用 - 数据连接（原应用数据）：数据连接新增 ChangeParseSetting 接口

数据连接新增 ChangeParseSetting 接口, 支持按文件类型配置解析方式，[了解详情](raw/_short/api-bailian-2023-12-29-changeparsesetting-59a7c69675f499ad.md)

### 2026-05-11

新增

#### 应用调用 API：新版智能体应用 DashScope API 首发

发布新版智能体应用 DashScope API 参考，支持单轮/多轮、流式、文件问答、视觉理解，[了解详情](raw/_short/new-agent-application-api-reference-be3bf785ec80b8bd.md)

### 2026-04-28

新增

#### 应用 - 多模态交互开发套件：多模态交互开发套件服务端 Java SDK 上线

新增服务端 Java SDK，含下载安装、关键接口与代码示例，[了解详情](https://help.aliyun.com/zh/model-studio/multimodal-sdk-java#8017a962a1ysj)

### 2026-04-24

新增

#### 知识库 RAG：知识库新增日志与监控

知识库检索调用全量投递至 SLS 日志服务，支持审计/排查/统计/告警，[了解详情](raw/application-user-guide/agent-context/knowledge-base/reference/rag-knowledge-base-log-monitoring.md)

### 2026-04-14

新增

#### 应用 - 多模态交互开发套件：多模态交互开发套件移动端 Android SDK 上线

新增移动端 Android SDK，含下载安装、关键接口与代码示例，[了解详情](raw/_short/multimodal-sdk-android-5c6fac2dfb609de2.md)

### 2026-04-09

新增

#### 多模态交互 SDK：RTOS C SDK 新增 License 模式

多模态交互开发套件 RTOS C SDK 新增 License 模式，覆盖嵌入式硬件半托管/全托管接入，[了解详情](raw/_short/mmi-rtos-sdk-dbfd414713bc31c9.md)

### 2026-04-07

新增

#### 应用组件-Prompt 工程：应用组件 Prompt 工程 API 上线

应用组件新增 Prompt 工程模块及其 API，提供 Prompt 模板管理能力，[了解详情](raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-prompt-engineering.md)

### 2026-04-01

新增

#### 应用发布与分享-UI 设计器：UI 设计器上线

百炼 UI 设计器上线，集成魔笔低代码能力，可视化拖放构建网页 UI 应用，[了解详情](https://help.aliyun.com/zh/model-studio/ui-designer#845c1f4aba43y)

### 2026-03-20

新增

#### 记忆库：记忆库 Memory 2.0 上线

新增长期记忆能力：自动从对话提取记忆片段与用户画像，支持多应用共享同一记忆库，[了解详情](raw/application-user-guide/agent-context/memory-library-overview/memory-library.md)

### 2026-03-19

新增

#### 官方应用-千问联网检索 Agent：联网检索 Agent 官方应用上线

应用广场新增联网检索 Agent 官方应用，提供产品简介、API 参考与说明，[了解详情](raw/application-user-guide/agent-development/application-gallery/web-search-agent.md)

#### 全妙-PPT 生成：全妙 PPT 生成 API 模块上线

全妙解决方案-PPT 生成模块开放完整 API：模板、文档、作品等接口，[了解详情](raw/_short/api-aimiaobi-2023-08-01-dir-ppt-generation-18c4c777ec0a34e6.md)

### 2026-02-28

新增

#### 多模态交互开发套件：多模态交互开发套件新增 Linux C++ SDK

多模态交互开发套件新增 Linux C++ SDK 文档，含下载安装与关键接口示例，[了解详情](https://help.aliyun.com/zh/model-studio/multimodal-sdk-linux#985cb1a0a4zdz)

### 2026-02-10

新增计费

#### 知识库：知识库支持订阅计费资源包

知识库提供后付费（按量付费）和[资源包](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#a06c023507qq3)两种计费方式。资源包可前往控制台[RAG标准版资源包](https://common-buy.aliyun.com/?commodityCode=sfm_ragservicestandard_dp_cn)或[RAG旗舰版资源包](https://common-buy.aliyun.com/?commodityCode=sfm_ragserviceenterprise_dp_cn)开通。详情请参见[知识库计费说明](raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。

### 2026-02-06

新增

#### 应用评测：新版应用评测

支持智能体、工作流和自定义三种类型的评测集，构建适合业务需求的评测体系。详情请参见[新版评测集](raw/_short/agenteval-evaluation-set-946c810bda606877.md)。

#### 应用 - 通义多模态翻译：通义多模态翻译网页翻译 JSSDK 上线

新增网页翻译 JSSDK，通过插入脚本一键完成网站多语言改造，[了解详情](https://help.aliyun.com/zh/model-studio/web-page-translation-jssdk#32940c468bp2y)

#### 插件：国际站官方插件新增 Image Generation

国际站官方插件列表新增 text\_to\_image (Image Generation)，[了解详情](https://help.aliyun.com/zh/model-studio/plugins#00edef12dc50q)

#### MCP：新增官方 MCP 服务

上线官方 MCP 服务，支持平台内集成与外部第三方接入（如 Amap Maps），[了解详情](raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)

#### 多模态交互开发套件：多模态交互开发套件新增 Android/iOS Lite SDK

新增多模态交互开发套件 Android/iOS Lite SDK 与音色列表，[了解详情](https://help.aliyun.com/zh/model-studio/multimodal-sdk-android-lite#d2dba24286nyf)

### 2026-02-05

新增

#### 应用 - 知识库：知识库检索新增排序模型与指令干预模式

Retrieve 接口新增排序模型选项与指令干预模式，平台检索能力扩展，[了解详情](https://help.aliyun.com/zh/model-studio/api-bailian-2023-12-29-retrieve#api-detail-51)

### 2026-01-31

新增

#### 长期记忆：上线新版 长期记忆&用户画像管理 API

[长期记忆 API](raw/application-user-guide/agent-context/memory-library-overview/long-term-memory-2-0.md)相比[长期记忆（旧）](raw/application-api-reference/flow-agent-api/api-bailian-2023-12-29-dir-long-term-memory.md)的改进：

-   通过开放的 API 接口，可接入任意应用，也支持多应用共享同一记忆库。
    
-   速度与效率高：拥有更低的延迟，更高的记忆检索召回效果。
    
-   自动提取能力：支持从对话中自动提取关键信息，自动去重，无需手动输入。
    
-   检索算法优化：新增语义检索能力，检索准确性显著提升，响应速度更快。
    
-   用户画像能力：新增完整的用户画像提取和管理能力。
    

### 2026-01-30

新增

#### 知识库：支持通过API创建音视频知识库

使用此API可创建两类知识库：基于文档或音视频的非结构化知识库，以及用于数据查询或图片问答的结构化知识库。详情请参见[创建知识库](raw/_short/api-bailian-2023-12-29-createindex-8bc613c75f8af371.md)。

### 2026-01-23

新增

#### 工作流应用：新增多模态生成节点

多模态生成节点用于调用阿里云多模态模型，根据配置的提示词和参数生成图像、视频或音频内容。

### 2026-01-21

新增

#### 应用 - 多模态交互开发套件：多模态交互开发套件应用配置上线

应用配置页面支持语音交互、理解与生成、技能、Agent 四大模块配置，[了解详情](https://help.aliyun.com/zh/model-studio/multimodal-app-configuration#a45151c0cfuyw)

### 2026-01-19

新增

#### 知识库：增加知识库监控API

查询指定知识库在特定时间范围内的监控数据。详情请参见[获取知识库监控数据](raw/_short/api-bailian-2023-12-29-getindexmonitor-3a609181d5c9c034.md)。

#### 知识库：增加更新知识库API

更新指定知识库的部分配置。详情请参见[更新知识库](raw/_short/api-bailian-2023-12-29-updateindex-551997e1d335e340.md)。

### 2026-01-15

新增

#### 工作流应用：新增异步运行模式

-   文本生成模式下，新增异步运行模式。
    
-   异步运行模式下，工作流会在后台执行。系统会立即返回Task ID，可通过Task ID查询任务执行结果。在[任务中心](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/app-task-center)中可以查看历史异步任务。
    

### 2026-01-10

新增

#### 知识库：支持子账号开通知识库，支持分账管理

如需将费用归属到不同的部门或项目，可以使用“标签”功能对业务空间进行标记进行分账管理。详情请参见[分账管理](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#60dc157f979as)。

### 2026-01-06

新增改进

#### 知识库：支持调整知识库检索过程初步召回参数

通过降低**初步向量检索TopK**和**初步关键词检索TopK**的数值，可减少送入排序模型的 Token 量，从而显著降低成本。详情请参见[模型调用费用](https://help.aliyun.com/zh/model-studio/billing-for-knowledge-base#e58a3fee888x8)。

### 2026-01-04

计费

#### 知识库：知识库商业化计费

阿里云百炼知识库服务自 2026 年 1 月 4 日起正式开始计费。总费用构成为规格费用和模型调用费用两部分。详情请参见[知识库计费说明](raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。

### 2025-12-26

新增

#### 智能体应用：上线新版智能体应用（Agent 2.0）

-   [新版智能体应用（Agent 2.0）](raw/application-user-guide/agent-development/llm-application/new-single-agent-application.md)将知识库、MCP 统一为工具，由智能体自主规划在何时、以何种顺序进行调用。能完整展示模型思考和工具调用的全过程。
    

### 2025-12-25

新增

#### 知识库：支持音视频知识库

-   支持上传音视频文件创建知识库，可实现：
    
    -   基于音视频内容的智能检索与问答，如直播回放问答、课程助教、客服质检等；
        
    -   对音视频素材进行二次创作，如生成脚本和字幕、给出剪辑建议等。
        
    
    详情请参见[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

### 2025-12-17

新增

#### 工作流应用：知识库节点支持不同调用方式

-   知识库节点支持必定调用、智能调用和旧版调用三种调用方式，支持解析文档、图片、表格类型的知识库。
    

### 2025-11-28

新增

#### 工作流应用：新增多模态数据节点，开始节点新增 file 类型参数

-   新增文档解析、图片解析、视频解析和音频解析四个节点，用于提取对应输入文件的结构化参数。
    
-   开始节点新增 file 类型参数，用于上传文件
    

### 2025-11-03

新增

#### 应用调用：支持通过Responses API 调用阿里云百炼应用

-   同步调用 API：适用于需要即时获取结果的实时交互场景，可轻松复用现有的 OpenAI 代码库，或快速集成来自 OpenAI 生态的各类工具。详情请参见[同步调用 API 参考](raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/synchronous-call-api-reference.md)。
    
-   异步调用 API：对于耗时较长的任务，只需在请求中设置 background 为 true，API 便会立即返回一个任务 ID，用于后续的查询与管理。详情请参见[异步调用 API 参考](raw/application-api-reference/flow-agent-api/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
    

### 2025-09-24

新增

#### 高代码应用：新的应用类型

-   支持基于Python项目结构部署AI后端服务，内置自动化运维、可观测性及日志服务等企业级能力。使用方法请参见[高代码应用](raw/application-user-guide/agent-development/sandbox/rich-code-application.md)。
    

### 2025-09-23

新增改进

#### 工作流应用：新增 Dify 工作流一键导入

-   支持 Dify 工作流一键导入，导入后自动映射节点类型与参数。使用方法请参见[工作流导入/导出](https://help.aliyun.com/zh/model-studio/workflow/introduction#c055d2211fwrp)。
    

#### 智能体应用：文件问答升级

-   支持全文引用、切片检索和自定义处理三种模式，对文档、图片、音视频等多种文件进行深度分析和自动化任务处理。使用方法请参见[文件问答](raw/application-user-guide/agent-development/llm-application/file-q-a.md)。
    

#### 智能体应用：回复功能升级

-   当主模型在特定场景下表现受限时，将自动切换至更优模型。详情请参见[智能体应用（Agent 1.0）](raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。
    

#### 知识库：数据导入流程简化

-   创建知识库时，可直接导入文件或数据，无需预先在应用数据页面导入。
    

#### 知识库：数据源支持DMS

-   创建知识库时，可直接从 DMS 指定数据表同步数据，详情请参见[知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

#### 知识库：创建流程优化

-   根据应用场景，将知识库类型分为**文档**、**数据**和**图片**三类，以简化创建过程，详情请参见[知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

#### 知识库：新增调试面板

-   编辑智能体应用时，可直接在线调整知识库参数，并实时验证检索召回效果。使用方法请参见[知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

### 2025-08-13

新增

#### MCP：新增外部调用功能

-   集成至第三方应用：支持一键自动配置到第三方应用，快速实现外部调用。
    
-   集成至个人项目：通过 MCP SDK 调用，实现灵活编码和深度定制。
    

### 2025-08-12

改进

#### 工作流应用：界面升级

-   智能体编排应用下线。
    
-   工作流应用界面升级。
    

### 2025-07-28

新增

#### 知识库：知识库数据源支持自建MySQL

-   结构化知识库支持从自建MySQL给定数据表同步数据。配置方法详见[集成MySQL数据至知识库](https://help.aliyun.com/zh/model-studio/connect-to-rds-for-knowledge-base)。
    

#### 知识库：知识库支持text-embedding-v4模型

-   text-embedding-v4模型在语种支持、代码片段向量化效果和向量维度选择等方面，相比v3模型进行了全面升级，适用于大部分场景。
    

### 2025-07-02

新增

#### 知识检索问答：知识检索与问答 API 上线

新增知识检索与问答 API，SSE 流式返回三阶段，[了解详情](raw/application-api-reference/rag-api/knowledge.md)

### 2025-05-22

新增

#### 知识库：知识库支持text-embedding-v3模型

-   text-embedding-v3模型在语种支持、输入长度和向量维度自定义等方面，相比v2模型进行了全面升级，适用于大部分场景。
    

### 2025-05-12

新增

#### 知识库：导入图片可选择Qwen VL进行解析

-   可选择qwen-vl-max或qwen-vl-plus模型，通过传入Prompt指引需识别的版面、元素和内容，适用于解析复杂图片或图表，详情请参见[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

### 2025-05-08

新增

#### 知识库：非结构化知识库支持导入离线HTML文件

-   支持基于离线HTML文件构建非结构化知识库，详情请参见[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

### 2025-04-10

新增

#### 知识库：新增权重设置功能

-   当智能体应用同时关联多个知识库时，可按信息源的重要性为每个知识库设置权重。系统将优先召回权重更高的知识库中的相关信息。使用方法请参见[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。

### 2025-04-09

新增

#### MCP：新增MCP市场与MCP管理功能

-   可开通阿里云百炼预置的MCP服务或部署自定义MCP服务，并在智能体应用和工作流应用中引用这些 MCP 服务，使应用具备更强大的能力。使用方法请参见[官方 MCP 服务](raw/application-user-guide/agent-store/model-context-protocol/official-and-third-party-mcp.md)和[自定义MCP服务](raw/application-user-guide/agent-store/model-context-protocol/custom-mcp.md)。

### 2025-04-01

新增

#### 智能体应用：[智能体应用（Agent 1.0）](raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)支持QwQ系列模型

不包括插件、流程、音视频交互能力。

-   [QwQ](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)模型具有强大的推理能力，模型会先输出思考过程，再输出回答内容。数学/代码能力（AIME 24/25、LiveCodeBench）及通用指标（IFEval等）达DeepSeek-R1满血版水平，显著优于同源精简版DeepSeek-R1-Distill。

#### 智能体应用：[智能体应用（Agent 1.0）](raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)支持QwQ系列模型

> 不包括插件、流程、音视频交互能力

-   [QwQ](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)模型具有强大的推理能力，模型会先输出思考过程，再输出回答内容。数学/代码能力（AIME 24/25、LiveCodeBench）及通用指标（IFEval等）达DeepSeek-R1满血版水平，显著优于同源精简版DeepSeek-R1-Distill。

### 2025-03-25

新增

#### 工作流应用：[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)大模型节点支持qwq-plus、qwq-32b模型

-   [QwQ](raw/model-user-guide/model-experience/text-generation-model/deep-thinking.md)模型具有强大的推理能力，模型会先输出思考过程，再输出回答内容。数学/代码能力（AIME 24/25、LiveCodeBench）及通用指标（IFEval等）达DeepSeek-R1满血版水平，显著优于同源精简版DeepSeek-R1-Distill。
    

### 2025-03-24

新增改进

#### 智能体应用：[智能体应用（Agent 1.0）](raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)检索配置新增 “多模态回复增强”开关

-   开启多模态识别能力，使智能体应用能够解析知识库中的图表与图像内容，提供结合视觉信息的精准回答。
    

### 2025-03-18

新增

#### 智能体应用：[智能体应用（Agent 1.0）](raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)支持qwen-vl-plus-latest、qwen-vl-plus-2025-01-25

-   qwen-vl-plus-latest始终等同最新快照版。
    
-   qwen-vl-plus-2025-01-25，又称qwen-vl-plus-0125。此版本属于[Qwen2.5-VL](https://qwenlm.github.io/blog/qwen2.5-vl/)系列模型，扩展上下文至128k，显著增强图像和视频的理解能力。
    

### 2025-02-24

新增

#### 工作流应用：工作流应用支持批量节点

-   批量节点是[工作流](raw/application-user-guide/agent-development/llm-application/workflow-application.md)中用于处理批量任务的功能节点，详情请参见[批处理](raw/application-user-guide/agent-development/llm-application/workflow-application.md)。
    

### 2025-02-18

新增

#### 工作流应用：工作流应用支持 DeepSeek 系列模型

-   [工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)可使用 DeepSeek 系列模型构建任务型和对话型工作流。
    

#### 智能体应用：智能体应用支持 DeepSeek 系列模型

-   [智能体应用（Agent 1.0）](raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)可集成 DeepSeek 系列模型，并结合知识库、长期记忆和 Prompt 模板，构建私有知识问答应用。
    

### 2024-12-16

新增改进

#### 工作流应用：工作流画布功能优化

-   意图分类节点支持选择意图模式：
    
    -   单选模式：大模型将从现有的意图配置中挑选最合适的意图作为输出。
        
    -   多选模式：大模型将从现有的意图配置中挑选全部匹配的意图作为输出。
        
    
-   文本转换节点支持JSON格式输出。
    

详情请参见[工作流应用](raw/application-user-guide/agent-development/llm-application/workflow-application.md)。

#### 智能体编排应用：智能体编排应用支持条件判断节点

-   智能体编排应用支持条件判断节点。详情请参见[智能体编排应用](https://help.aliyun.com/zh/model-studio/multi-agent-application)。
    

### 2024-12-10

新增

#### 工作流应用：新增“音视频实时互动”

-   可将图文对话类应用轻松转为音视频实时互动应用。
    
-   提供 H5/APP 调试窗口，可通过音视频 SDK 发布到用户的 WEB/iOS/Android 应用中。
    

#### 智能体应用：新增“音视频实时互动”

-   可将图文对话类应用轻松转为音视频实时互动应用。
    
-   提供 H5/APP 调试窗口，可通过音视频 SDK 发布到用户的 WEB/iOS/Android 应用中。
    

### 2024-12-03

新增改进

#### 应用组件：新增Prompt样例优化文档

-   大量实践表明，FewShot方法在提升大模型的推理效果和性能方面具有显著的助益。Prompt样例库功能作为阿里云百炼的FewShot能力，通过录入用户输入（Query）和期望的模型回复（Answer）作为样例信息源，在模型调用时根据用户输入，检索召回相关样例信息，以此作为输出参考，从而提高大模型的回答准确性，适用于客服及问答等场景。详情请参见[Prompt样例库](raw/application-user-guide/agent-development/llm-application/prompt/prompt-sample-optimization.md)。
    

### 2024-11-27

新增

#### 应用分享：新增微信、钉钉分享渠道

-   支持创建钉钉AI机器人和微信公众号AI机器人，创建完成后，可按需将AI机器人回调地址或二维码分享给目标用户。详情请参见[应用分享](https://help.aliyun.com/zh/model-studio/share-an-application#8778cb4490l2i)。
    

### 2024-11-01

新增

#### 知识库：非结构化知识库支持导入Excel文档

-   除了结构化知识库，非结构化知识库也支持导入Excel文档，适用于：
    
    -   导入的文档可能包括非Excel格式（例如pdf、doc等）；
        
    -   导入多个具有不同表结构的Excel文档。
        
    
    详情请参见[知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

### 2024-10-24

新增

#### 应用观测：新增应用观测能力

-   新增的[应用观测](https://bailian.console.aliyun.com/knowledge-base#/app-observe)支持端到端查看阿里云百炼应用的处理流程，详情请参见[用量监控与性能分析](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
    

#### SFM服务关联角色：新增AliyunServiceRoleForSFMTelemetry角色

-   用于阿里云百炼应用观测的服务关联角色，应用观测使用此角色来访问OpenTelemetry实例。点击[SFM服务关联角色](https://help.aliyun.com/zh/model-studio/bailian-service-linked-role#31e88eb412d6c)查看。
    

### 2024-09-29

新增

#### SFM服务关联角色：新增AliyunServiceRoleForSFMAccessingMNS角色

-   用于OSS变更自动同步的服务关联角色，阿里云百炼数据中心使用此角色来访问MNS队列中的OSS变更消息。点击[服务关联角色](raw/application-api-reference/more/bailian-service-linked-role.md)查看。
    

### 2024-09-25

新增

#### 知识库：结构化知识库数据源支持云上数据库

-   结构化知识库的数据源支持云数据库RDS。具体说明请参见[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

#### 知识库：非结构化知识库支持自定义metadata

-   支持为非结构化知识库中的文档附加metadata，以提升知识库检索的效率和精准度。具体说明请参见[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

#### 知识库：支持图文检索

-   知识库支持解析文档中的图片，结构化文档中的图片将被转为向量，非结构化文档中的图片将被提取文字然后再转为向量。具体说明请参见[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    
-   如果智能体应用关联的结构化知识库包含图片索引，可以在提问时上传图片，与输入图片相关的数据记录会与提问一起提供给大模型。具体说明请参见[智能体应用（Agent 1.0）](raw/application-user-guide/agent-legacy/legacy-flow-agent/single-agent-application.md)。
    
-   测试知识库页面同样支持了图文输入，便于评估知识库的图文检索能力。具体说明请参见[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)。
    

### 2024-09-17

新增

#### 数据管理：非结构化数据文件支持标签分类

-   非结构化数据支持标签分类，点击[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)查看详情。
    

### 2024-09-04

新增

#### 应用中心：智能体应用新增“检索配置”功能

-   智能体应用中，打开“知识检索增强”开关后，增加“检索配置”功能，用于设置大模型的回答范围、是否展示回答来源等。点击[创建和使用知识库](raw/application-user-guide/agent-context/knowledge-base/data-connection-overview/rag-knowledge-base.md)查看完整信息。
    

### 2024-08-27

改进

#### 数据管理：结构化数据能力更新

-   结构化数据支持增量导入、支持设置表头数据类型，请点击[数据管理](https://bailian.console.aliyun.com/#/data-center)进行体验。
    

### 2024-08-26

新增

#### 应用中心：新增自定义参数的调用说明

-   调用工作流应用和智能体编排应用时，需要传入自定义参数，详情请参见[应用调用](https://help.aliyun.com/zh/model-studio/application-calling-guide)。
    

#### 应用中心：新增自定义参数的透传示例

-   调用工作流应用和智能体编排应用时，需要传入自定义参数。点击，查看“请求参数（工作流和智能体编排应用的参数透传）”中内容。
    

### 2024-08-24

新增

#### 应用中心：新增自定义参数的传入说明

-   调用工作流应用和智能体编排应用时，需要传入自定义参数。点击[自定义节点参数传递](https://help.aliyun.com/zh/model-studio/pass-through-of-application-parameters#uPwcs)查看完整信息。
    

### 2024-08-23

新增

#### 应用中心：新增应用类型

-   新增应用-**流程编排应用**，点击[应用流程编排应用](https://bailian.console.aliyun.com/?accounttraceid=04966e8c43324e508d4aa5e02268236ccabs#/app-center)进行体验。
    

### 2024-08-22

新增

#### 应用广场：新增传媒/零售文章风格与格式学习、电商零售推广文案写作应用

-   点击[应用广场](https://bailian.console.aliyun.com/#/app-market)进行体验，点击[传媒/零售文章风格与格式学习](raw/_short/media-retail-article-style-and-format-learning-8c4530ece55cc26f.md)、[电商文案智能可控生成](raw/_short/intelligent-and-controllable-generation-of-e-com-2b318e596c72856a.md)查看完整信息。
    

#### 应用中心：应用模型展示更新

-   ​我的应用中选择模型后，**展示最大长度数据**。
    

#### 应用中心：智能体应用能力更新

-   智能体应用**支持多函数调用**，**支持循环调用的打断**。
    

### 2024-08-14

新增

#### 应用中心：应用测试窗新增测试能力

-   应用测试窗**支持长期记忆用户洞察和用户画像**，点击[我的应用](https://help.aliyun.com/zh/model-studio/my-application)查看完整信息。
    

### 2024-08-12

新增

#### 插件管理：新增内置插件类型

-   新增生成二维码、GitHub搜索插件内容。
    

### 2024-07-30

新增

#### 应用中心：创建自定义应用支持qwen2模型

-   创建自定义应用支持​**qwen2-72b-instruct**​，​**qwen2-57b-a14b-instruct模型。**​

### 2024-07-24

改进

#### 数据中心：知识索引更新

-   知识索引支持召回命中测试，点击[知识索引](https://help.aliyun.com/zh/model-studio/knowledge-index)查看详情。

### 2024-07-23

新增

#### 应用广场：自定义应用支持分享

-   已发布的应用支持分享Web端（PC/h5）。
-   **API调用**：即现有的API调用方式，无论应用是否配置，API 调用都会发布。
-   **Web(PC/h5)**：基于阿里云百炼现有的页面及魔笔的模板内容进行搭建。
-   **官方分享渠道**：提供应用的测试 Web 页面，仅支持小范围分享体验。
-   **魔笔分享渠道**：魔笔是一个低代码开发平台，提供多种模板，灵活选用，支持定制用户交互界面和自定义域名，轻松发布生产级 Web 应用。

#### 应用广场：自定义应用支持分享

-   已发布的应用支持分享Web端（PC/h5）。

> **API调用**：即现有的API调用方式，无论应用是否配置，API 调用都会发布。>

> **Web(PC/h5)**：基于阿里云百炼现有的页面及魔笔的模板内容进行搭建。

> **官方分享渠道**：提供应用的测试 Web 页面，仅支持小范围分享体验。

**魔笔分享渠道**：魔笔是一个低代码开发平台，提供多种模板，灵活选用，支持定制用户交互界面和自定义域名，轻松发布生产级 Web 应用。 >"

### 2024-07-19

改进

#### 数据管理：OSS授权方式更新

-   数据管理中的文档数据支持本地上传和OSS导入两种模式，**在关联OSS文件存储Bucket后**，**可实现OSS授权及跨域访问。**点击[从OSS导入数据](https://help.aliyun.com/zh/model-studio/oss-data-import-guide)查看详情。

### 2024-07-18

新增

#### 应用中心：插件服务

-   应用中心支持**自定义参数**透传点击[应用的参数传递](raw/_short/pass-through-of-application-parameters-1967bbe8cc08ce9f.md)查看详情。

### 2024-07-08

新增

#### 开发指南：知识索引新增权限控制

-   阿里云主账号或RAM管理员给RAM用户授权后，RAM用户才能使用阿里云百炼知识索引能力。点击[知识索引自定义权限策略](https://help.aliyun.com/zh/model-studio/use-and-authorize-ram-user)查看完整信息。

### 2024-07-03

新增

#### 数据管理：支持上传 Excel格式文件

-   支持结构化数据导入，并且支持自定义设置结构列信息。点击[数据导入](https://help.aliyun.com/zh/model-studio/data-import-instructions)查看详情。

#### 应用中心：支持结构化数据构建知识库及RAG在线推理

-   支持结构化和非结构化数据构建及关联知识库并进行知识检索。点击[知识索引](https://help.aliyun.com/zh/model-studio/knowledge-index)查看详情。

### 2024-06-20

新增

#### 应用广场：应用中心

-   新建的应用支持测试版本，编辑应用后默认保存为测试版本。
    

#### 应用广场：流程管理

-   流程画布支持业务参数透传，点击[流程编排（旧版待下线）](https://help.aliyun.com/zh/model-studio/manage-processes-old)查看详情。
    

### 2024-06-13

新增改进

#### 数据中心：新增数据增强能力

-   数据增强支持通过参数配置及prompt配置对数据进行增强处理，提升处理数据效果。
    

### 2024-06-05

新增

#### 数据中心：数据管理支持多种格式上传

-   数据管理新增支持md、txt、ppt、pptx文件的导入和解析，以及页面预览。
    

#### 数据应用：知识索引支持切片管理

-   支持切片的管理（开关、内容编辑）。
    

### 2024-05-03

新增

#### 我的应用：新增多模型创建应用

-   全新应用创建流程，基于Assistant API机制的RAG、工作流、插件调度机制。
    
-   max、plus、turbo多模型选择，多维效果/成本配置。
    
-   全新Memory长期记忆机制，支持长期记忆存储，个性化Assistant效果。点击[我的应用](https://help.aliyun.com/zh/model-studio/application-building-instructions)查看详情。
    

#### 数据管理：新增平台统一的数据管理模块

-   全新统一数据管理能力，支持本地数据上传、OSS数据导入，支持大批量非结构化文档导入。
    
-   一键IDP解析为可应用数据，支持多类目管理。
    

#### 知识索引：创建和管理用于RAG应用的知识库索引，基于对数据中心的统一引用

-   基于LLamaindex提供完整知识索引配置，包括Chunk切分、向量配置。
    
-   支持多种召回索引配置，满足不同粒度的RAG效果。
    

### 2024-03-31

新增

#### 应用工具：新增官方插件能力

-   上线新版插件中心，新增“**图片生成**”、“**夸克搜索**”、“**Python代码解释器**”和“**计算器**”四款官方插件，点击[插件中心](raw/application-user-guide/agent-development/llm-application/plug-in/plug-in-overview.md)查看详情。
    

#### 应用广场：智能体API应用支持API调用

-   新增[Assistant API](https://help.aliyun.com/zh/model-studio/api-agent)及[Python SDK](https://help.aliyun.com/zh/model-studio/sdk-agent)接口；点击[最佳实践](raw/model-user-guide/use-cases/prompt-engineering-guide.md)查看详情。
    

### 2024-02-22

新增

#### 企业知识库：新增企业检索链路

-   新增ES向量存储数据库，知识库名称为**默认知识库**，检索效果增强。详情查看。
    

#### 企业知识库：支持上传FAQ形式文件

-   新增上传Excel格式的文件，详情查看[配置企业知识库](https://help.aliyun.com/zh/model-studio/configure-enterprise-knowledge-base)。
    

### 2024-02-05

新增

#### 企业知识库：新增上传格式

-   支持OSS上传文档，详情查看[配置企业知识库](https://help.aliyun.com/zh/model-studio/configure-enterprise-knowledge-base)。
    

#### Prompt工程：新增Prompt模板类型

-   新增**110个**Prompt模板。
    

### 2024-02-01

新增

#### 流程编排：新增流程编排版本

-   流程编排支持一键调整布局，优化流程画布交互体验。
    

### 2024-01-30

新增

#### 应用管理：新增会话记录备份

-   通过ADB-PG备份会话记录，支持手动关闭/开启。
    

### 2024-01-24

新增

#### 流程编排：新增流程画布版本

-   脚本节点是面向开发者提供简单的代码开发能力，新增Python语言。
    

#### 流程编排：流程画布增加大模型节点

-   大模型节点，用于关联包括但不限于官方模型、SFT模型，旨在使用大模型能力详情查看[LLM节点说明](https://help.aliyun.com/zh/model-studio/llm-node)。
    

### 2024-01-15

修复

#### API相关：修复文档上传字段缺失

-   相关字段已更新，详情查看[应用调用SDK参考（旧）](https://help.aliyun.com/zh/model-studio/call-alibaba-cloud-model-studio-v1-through-sdk)。
