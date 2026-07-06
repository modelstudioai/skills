# 知识库与记忆库对比

百炼平台同时提供「知识库」与「记忆库」两类持久化数据能力，二者定位不同：知识库面向 **静态/半静态的私有领域知识**，通过 RAG 检索增强生成补充模型的事实性背景；记忆库面向 **跨会话的动态对话上下文**，自动从对话中提取并召回用户偏好与历史信息。本页从输入、输出、模型支持、API、计费、典型场景等维度做技术选型对比，供开发者在 RAG 与长期记忆之间做架构决策参考。

## 关键维度对比

| 维度 | 知识库 | 记忆库 |
| --- | --- | --- |
| 定位 | RAG 检索增强生成，补充私有/最新领域知识 | 长期记忆 API，解决跨会话上下文丢失 |
| 数据来源 | 用户主动导入的文档（PDF/Word/Markdown/Excel/CSV/图片/音视频等） | 从对话中自动提取关键事件与画像，或通过 `custom_content` 直写 |
| 内容形态 | 非结构化文档切片、结构化表格（NL2SQL）、图片向量、音视频时间轴 | 记忆片段（自动去重/动态更新）+ 用户画像（结构化属性） |
| 输入格式 | 文件上传，支持电子文档/文档智能/大模型/Qwen VL/音视频等多种解析 | HTTPS JSON（`messages` 或 `custom_content`），或 OpenClaw 插件零侵入 |
| 输出格式 | 检索返回切片（含 `score`/`text`/`metadata`）；问答返回生成回答 | `SearchMemory` 返回记忆条数（建议 top_k 3–10）注入 Prompt |
| 检索方式 | Query 改写 → 向量+关键词混合检索 → Rerank → 加权返回 | 语义检索召回相关记忆 |
| 支持模型 | 千问 QwQ/Long/Max/Plus/Turbo/Coder/Deep-Research、千问 VL 系列、千问开源版、DeepSeek-R1/V3.1、abab6.5s、Llama3.1、Yi-Large 等，及自定义千问调优版 | 任意模型（记忆能力与生成模型解耦）；OpenClaw Agent 共享同一记忆 |
| 地域限制 | 仅中国站 **华北2（北京）** | DashScope 全球接入（`dashscope.aliyuncs.com`） |
| API 端点 | `bailian.cn-beijing.aliyuncs.com`（ApplyFileUploadLease/AddFile/CreateIndex/SubmitIndexJob/Retrieve 等） | `https://dashscope.aliyuncs.com/api/v2/apps/memory/*`（AddMemory/SearchMemory/ListMemory 等） |
| 鉴权 | AK/SK + `WORKSPACE_ID`，需 `AliyunBailianDataFullAccess` 策略 | `DASHSCOPE_API_KEY`（`sk-` 开头） |
| 绑定数量 | 单服务最多绑定 15 个知识库 | 单账号一个默认记忆库（不可删），可创建多个记忆库 ID |
| 计费方式 | 标准版 0.03 元/小时、1 QPS、≤100 GB；旗舰版 0.2 元/RCU/小时、50–10,000 QPS、≤9,999 GB；SLS 日志按存储/流量另计 | 按记忆写入与检索调用计费（DashScope 体系）；具体以控制台规则为准 |
| 数据生命周期 | 持久存储，可手动删除文件/重建索引 | 默认 180 天（控制台规则可配 7/30/180 天或永不过期）；API 直写且不指定 `project_id` 用默认规则 |
| 接入方式 | 控制台 + 开放 API（仅文档搜索类有完整 API 指南） | API 直连（curl/Python `agentscope-runtime`）+ OpenClaw 插件（`before_agent_start`/`agent_end` 钩子） |
| 典型场景 | 企业文档问答、产品手册、图片问答、音视频搜索、结构化数据 NL2SQL | 用户偏好持久化、跨会话上下文连续、个性化助手、Agent 长期状态 |

## 适用场景建议

**选知识库**：
- 需要让模型回答**特定领域事实**（产品手册、规章制度、技术文档）。
- 数据是**文件形态**，体量大、更新不频繁，需要切片+索引+Rerank 全流程。
- 需要 **多模态**（图片问答、音视频搜索、富文本图文）。
- 需要 NL2SQL 查询结构化业务数据。
- 对检索质量有可控调参需求（TopK、相似度阈值、Rerank 模式、Meta 过滤）。

**选记忆库**：
- 需要**跨会话记住用户**（偏好、习惯、历史事件），而非查询外部文档。
- 数据**从对话中动态产生**，无法预先导入。
- Agent 需要"自动捕获/自动召回"零侵入集成（OpenClaw 插件）。
- 个性化场景，每个 `user_id` 记忆空间相互隔离。

**组合使用**：
- 同一智能体可同时挂载知识库与记忆库：知识库提供领域事实底座，记忆库维护用户上下文，二者在 Prompt 层叠加注入。
- 典型架构：用户提问 → 记忆库召回用户偏好 → 知识库召回领域切片 → 一并拼装到 Prompt → 模型生成个性化且准确的回答。

## 技术选型参考

| 决策点 | 倾向知识库 | 倾向记忆库 |
| --- | --- | --- |
| 数据是否预先存在 | 是，文档/表格文件 | 否，需从对话提炼 |
| 内容更新频率 | 低，批量导入 | 高，每次对话增量 |
| 是否需要文件解析/切片 | 是 | 否 |
| 是否按用户隔离 | 不强（按知识库/服务隔离） | 是（按 `user_id`） |
| 是否需要 Rerank 调优 | 是 | 否（语义召回即可） |
| 是否多模态 | 是（图/音视频） | 否（文本为主） |
| 接入是否零侵入 | 否，需走文件上传+索引流程 | 是（OpenClaw 插件） |

简单判断：**事实性问答应答用知识库，用户上下文延续用记忆库**；若两者都需要，组合使用效果最佳。

## 被对比主题页

- [knowledge base](../guides/knowledge-base.md)
- [memory library overview](../guides/memory-library-overview.md)


