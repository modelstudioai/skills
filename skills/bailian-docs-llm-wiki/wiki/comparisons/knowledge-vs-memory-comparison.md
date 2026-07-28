# 知识库与记忆体系对比

在构建百炼平台上的智能体应用时，开发者常常需要为大模型补充"模型本身不知道的信息"。这类信息大致分为两类：一类是**企业级共享知识**（产品手册、FAQ、业务文档等），对应**知识库（RAG）**；另一类是**用户级个性化上下文**（用户偏好、历史事件、画像属性等），对应**记忆体系**——包括控制台侧的**记忆库（Memory Library）**与开放接口侧的**长期记忆（新）API**。三者都通过"提取/切片 → 向量化 → 语义检索 → 注入 Prompt"的模式增强生成效果，但定位、数据粒度和接入方式差异显著。本文从技术选型角度对三者进行对比。

## 关键维度对比

| 维度 | 知识库（RAG） | 记忆库（控制台/插件） | 长期记忆（新）API |
| --- | --- | --- | --- |
| 核心定位 | 企业私有知识增强，回答前检索文档切片 | 跨会话个性化记忆的可视化管理与零侵入接入 | 记忆片段/用户画像的 RESTful 增删改查 |
| 数据来源 | PDF、DOCX、Markdown、Excel、图片、音视频等文档 | 用户与智能体的对话内容（自动提取）或 `custom_content` 直写 | 对话 `messages`（自动提取）或 `custom_content`（≤512 字符） |
| 数据粒度 | 文档解析后的切片（chunk） | 记忆片段 + 结构化用户画像 | 记忆片段（memory node）+ 画像模板/用户画像 |
| 数据隔离维度 | 知识库 / [业务空间](../concepts/workspace.md)（Workspace） | `userId` 记忆空间隔离 | `user_id`（最大 64 字符），不同 ID 完全隔离 |
| 输入格式 | 多格式文件（本地上传 / OSS / 数据连接器） | 对话 messages、custom_content、画像模板 | JSON 请求体：`messages` 与 `custom_content` 互斥 |
| 输出格式 | 检索切片（知识检索服务）或生成式回答（知识问答服务） | 召回的记忆条目（自动注入 Prompt） | `memory_nodes` 数组（含 `content`、`event`、`old_content`） |
| 检索方式 | 向量 + 关键词双路召回，可加排序模型精排 | 语义检索（服务端向量化），`topK`/`minScore` 控制 | 语义检索，支持 `top_k`（1~100）、`min_score`、`enable_rerank`、query 重写 |
| 向量/排序模型 | `text-embedding-v4/v3`、`multimodal-embedding-v1`、`qwen3-rerank` 等，可选可配 | 由百炼服务端托管，不可自选 | 由百炼服务端托管，不可自选 |
| API 端点 | 阿里云百炼 SDK / 签名 HTTP（租约上传 → 建索引 → 检索） | OpenClaw 插件或同长期记忆 API | `https://dashscope.aliyuncs.com/api/v2/apps/memory/*` |
| 认证方式 | AccessKey + `WORKSPACE_ID`（签名请求） | DashScope API Key（`sk-` 开头） | `Authorization: Bearer $DASHSCOPE_API_KEY` |
| 挂载/接入方式 | 智能体应用、工作流节点、知识检索/知识问答服务、API 集成 | 控制台可视化管理、HTTP API、OpenClaw 插件（自动捕获/召回） | 纯 HTTP API，Python 可用 `agentscope-runtime` 封装类 |
| 数据有效期 | 长期保存，随文档管理更新 | 规则可配 7/30/180 天或永不过期（默认规则 180 天） | 文档描述"暂无失效日期"（不指定 `project_id` 时走默认规则） |
| 主要限制 | 仅中国站华北2（北京）地域；单次控制台导入 ≤50 文件；检索/问答服务最多绑 15 个知识库 | 所有 OpenClaw Agent 共享同一记忆；不支持 Coding Plan API Key | 总[限流](../concepts/rate-limit.md) 3000 QPM；add 120 QPM；search 300 QPM；messages ≤50 条 |
| 计费关注点 | 规格（标准版/旗舰版）、向量化与排序模型调用、召回切片带来的 Token 消耗 | 记忆读写走长期记忆 API 计量 | 按 API 调用计量，受 QPM [限流](../concepts/rate-limit.md)约束 |
| 典型场景 | 企业文档问答、产品手册检索、FAQ、参数表查询 | 个人助理记住用户偏好、跨会话延续上下文 | 自研应用精细控制记忆的写入、检索、更新与删除 |

## 能力侧重差异

- **知识库**面向"多人共享、以文档为中心"的知识：具备完整的数据处理流水线（解析 → 切片 → 向量化 → 索引），并提供命中测试、Meta 信息抽取、标签/元数据过滤、相似度阈值等丰富的调优手段，还支持 SLS 日志审计。它回答的是"这个问题在企业资料里怎么说"。
- **记忆库**面向"单人专属、以对话为中心"的信息：自动从对话中提取记忆片段并去重、动态更新，配合用户画像模板持久化结构化属性。它回答的是"这个用户是谁、喜欢什么、之前说过什么"。
- **长期记忆（新）API** 是记忆库能力的开放接口层：提供 AddMemory / SearchMemory / ListMemory / DeleteMemory / UpdateMemory 及画像模板系列接口，适合需要把记忆能力嵌入自有系统、并对读写时机做精细编排的开发者。

## 适用场景与选型建议

1. **企业知识问答、文档检索类需求 → 选知识库。** 数据是文档而非对话，需要多格式解析、多知识库联合检索、召回调优和引用溯源时，知识库是唯一合适的方案。若已有生成链路只需要检索切片，用知识检索服务；想要端到端问答，用知识问答服务。
2. **智能体需要"记住用户" → 选记忆体系。** 用户偏好、历史约定、画像属性等以用户为维度的碎片信息，不适合建成文档知识库；用记忆库自动提取 + 语义召回更贴合。
3. **使用 OpenClaw 或希望零改造接入 → 记忆库 + OpenClaw 插件。** `autoCapture` / `autoRecall` 钩子无需改动 Agent 代码即可获得跨会话记忆，注意所有 Agent 共享同一记忆空间。
4. **自研应用需要完全掌控记忆生命周期 → 直接调长期记忆（新）API。** 可自行决定何时写入（`messages` 提炼或 `custom_content` 直写）、何时检索（`top_k`、`min_score`、重排序、query 重写）、何时更新或删除，并通过 `user_id` 做多租户隔离。设计时需预留 QPM [限流](../concepts/rate-limit.md)余量。
5. **两者组合是常态。** 成熟的智能体通常同时挂载知识库（回答业务问题）与记忆体系（保持个性化上下文）：检索企业知识用 RAG，召回用户记忆用长期记忆 API，再一并注入 Prompt。

## 选型速判

| 问题 | 是 → 建议 |
| --- | --- |
| 数据是文档/手册/FAQ 等静态资料？ | 知识库 |
| 信息以单个用户为维度、来自对话？ | 记忆库 / 长期记忆 API |
| 需要控制台可视化管理与有效期规则？ | 记忆库 |
| 需要在自有后端精细控制记忆增删改查？ | 长期记忆（新）API |
| 用 OpenClaw 且不想写代码？ | 记忆库 OpenClaw 插件 |
| 既要答业务问题又要记住用户？ | 知识库 + 记忆体系组合 |

## 被对比主题页

- [knowledge base](../guides/knowledge-base.md)
- [memory library overview](../guides/memory-library-overview.md)
- [long term memory new](../api/long-term-memory-new.md)


