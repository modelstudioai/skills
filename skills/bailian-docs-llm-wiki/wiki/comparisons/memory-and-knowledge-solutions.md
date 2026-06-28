# 长期记忆、记忆库与[知识库](../concepts/knowledge-base.md)对比

百炼平台为开发者提供了三类用于"补充模型上下文"的能力：**长期记忆（新）API**、**记忆库（Memory Library）**、**[知识库](../concepts/knowledge-base.md)（Knowledge Base）**。三者定位不同：长期记忆 API 是底层的 RESTful 接口集合；记忆库是建立在长期记忆 API 之上、面向"跨会话用户记忆"的产品化封装（含控制台管理、OpenClaw 插件零侵入接入）；[知识库](../concepts/knowledge-base.md)则基于 RAG 技术，面向"私有文档/数据的语义检索"。本页通过关键维度对比，帮助开发者根据业务诉求（用户画像 vs 文档问答 vs 零侵入记忆）做出技术选型。

## 关键维度对比

| 维度 | 长期记忆（新）API | 记忆库（Memory Library） | 知识库（Knowledge Base） |
| --- | --- | --- | --- |
| 定位 | 底层 RESTful API，存储/检索/更新/删除用户记忆片段与画像 | 长期记忆 API 的产品化封装，含控制台与 OpenClaw 插件 | 基于 RAG 的私有数据语义检索，为模型补充领域知识 |
| 输入格式 | `messages`（对话）或 `custom_content`（自定义文本，≤512 字符） | 同长期记忆 API；OpenClaw 插件自动捕获对话 | 文件（pdf/docx/xlsx/图片/音视频等）、数据表、OSS 导入 |
| 输出格式 | 记忆片段（`memory_nodes`）、用户画像（结构化属性） | 记忆片段 + 用户画像，可注入 Prompt | 召回的文本切片（≤20 个/次），拼装后注入 Prompt |
| API 端点 | `https://dashscope.aliyuncs.com/api/v2/apps/memory/*` | 复用长期记忆 API；OpenClaw 插件通过 Gateway 钩子调用 | 阿里云百炼 SDK / 检索 API（需 AliyunBailianDataFullAccess 权限） |
| 支持模型 | 不直接绑定模型；记忆提取与画像由服务端完成 | 同长期记忆 API；OpenClaw 插件不支持 Coding Plan [API Key](../concepts/api-key.md) | 预置千问系列、DeepSeek-R1/V3.1、abab6.5s、Llama3.1、Yi-Large 及自定义模型 |
| 数据存储 | 记忆片段与画像，按 `user_id` 隔离，按 `memory_library_id` 分库 | 同长期记忆 API；默认库预置"默认有效期 180 天"规则 | 向量索引（text-embedding-v3/v4 512 维；multimodal-embedding-v1 1024 维） |
| 计费方式 | 按 API 调用计费（具体见平台说明） | 同长期记忆 API | 规格费用（按小时）+ 模型调用费用（[Token](../concepts/token.md)）；标准版 0.03 元/小时，旗舰版 0.2 元/RCU/小时 |
| 并发/限流 | 全部接口 ≤3000 QPM；add 120 QPM；search 300 QPM | 同长期记忆 API | 标准版 1 QPS（固定）；旗舰版 50–10,000 QPS（1–200 RCU） |
| 有效期 | API 直写：暂无失效日期 | 控制台规则：7/30/180 天或永不过期（默认 180 天） | 持久存储，无失效概念 |
| 接入方式 | 直接调用 RESTful API；Python 可用 `agentscope-runtime` | API 直连 / 百炼控制台 / OpenClaw 插件（零侵入） | 控制台创建 + SDK 集成；可挂载到[智能体应用](../concepts/agent-application.md)、工作流应用 |
| 典型场景 | 跨会话个性化、用户偏好持久化、自动提取关键事件 | 用户长期记忆、画像维护、Agent 零侵入记忆接入 | 私有文档问答、领域知识检索、图文/音视频内容搜索 |

## 各方案适用场景建议

### 长期记忆（新）API

适合需要**精细控制记忆生命周期**的开发者：自行管理写入（AddMemory）、语义检索（SearchMemory）、更新与删除，并通过画像模板（Profile Schema）维护结构化用户属性。当业务需要将记忆能力嵌入自有应用、对 `user_id` 与 `memory_library_id` 做多租户隔离、或希望用 `custom_content` 直接写入指定记忆（绕过对话提炼）时，优先选择此 API。

### 记忆库（Memory Library）

适合希望**以最低接入成本获得跨会话记忆**的场景：

- **OpenClaw 插件方式**：通过 `before_agent_start`（自动召回）与 `agent_end`（自动捕获）两个 Gateway 钩子实现零侵入记忆，所有提炼、向量化、语义检索由百炼服务端完成。适合基于 OpenClaw 构建的 Agent，无需改动业务代码。
- **控制台方式**：在百炼控制台可视化管理记忆库与规则，支持配置记忆片段有效期（7/30/180 天或永不过期），适合非技术运营人员参与记忆策略管理。
- **API 直连方式**：与长期记忆 API 一致，适合自定义接入。

注意：OpenClaw 记忆插件为统一配置，所有 Agent 共享同一记忆，暂不支持按 Agent 独立配置。

### 知识库（Knowledge Base）

适合需要**让模型基于私有数据回答问题**的 RAG 场景：

- 文档问答（pdf/docx/markdown/图片等，单文件最大 150MB）
- 数据查询（xlsx 数据表，最大 10 万行）
- 图片问答（multimodal-embedding-v1）
- 音视频搜索（最大 512MB）

知识库仅在**中国站华北2（北京）**地域可用，提供标准版（1 QPS、≤100 GB）与旗舰版（50–10,000 QPS、≤9,999 GB）两档规格。创建后知识库类型、metadata 抽取与切片策略不可更改，需一次性规划。适合企业知识库、产品手册问答、领域知识检索等"知识供给"型应用。

## 技术选型参考

| 选型问题 | 推荐方案 |
| --- | --- |
| 需要记住用户偏好、历史事件，实现跨会话个性化 | 长期记忆 API 或记忆库 |
| 基于 OpenClaw 构建 Agent，希望零侵入接入记忆 | 记忆库（OpenClaw 插件） |
| 需要运营人员在控制台管理记忆规则与有效期 | 记忆库（控制台） |
| 需要精细控制记忆的增删改查与画像模板 | 长期记忆（新）API |
| 需要基于私有文档/数据做语义检索问答 | 知识库 |
| 需要处理图片/音视频等多模态内容检索 | 知识库（图片问答/音视频搜索） |
| 高并发检索（>1 QPS） | 知识库旗舰版（最多 10,000 QPS） |
| 同时需要"用户记忆"和"文档知识" | 记忆库 + 知识库组合使用，二者互补 |

**一句话总结**：长期记忆 API 与记忆库解决"记住用户是谁、做过什么"的问题（个性化上下文），知识库解决"模型不知道的领域知识"的问题（RAG 检索）。二者并不互斥，可在同一应用中组合使用——用记忆库维持用户画像与历史，用知识库供给领域文档，共同提升大模型在特定业务中的表现。

## 被对比主题页

- [long term memory new](../api/long-term-memory-new.md)
- [memory library overview](../guides/memory-library-overview.md)
- [knowledge base](../guides/knowledge-base.md)


