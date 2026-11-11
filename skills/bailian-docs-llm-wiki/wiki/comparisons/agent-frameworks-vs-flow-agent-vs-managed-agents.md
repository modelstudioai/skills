# 智能体开发框架、流程型智能体与托管智能体对比

为帮助开发者在百炼平台上高效选型，本文系统对比三类主流智能体构建路径：**智能体开发框架（Frameworks）**、**流程型智能体（Flow Agent）** 和 **托管智能体（Managed Agents）**。三者定位不同——框架面向代码优先的深度定制场景，流程型智能体聚焦低代码/配置化应用集成，托管智能体则提供全生命周期可编程的运行时基础设施。本对比基于当前（2024年Q3）百炼平台正式版 API 与 SDK 能力，旨在为技术决策提供客观、可落地的参考依据。

## 关键维度对比

| 维度 | 智能体开发框架（Frameworks） | 流程型智能体（Flow Agent） | 托管智能体（Managed Agents） |
|------|-----------------------------|---------------------------|------------------------------|
| **核心定位** | 开发者主导的 SDK 集成方案，用于构建 RAG、Agent 等自定义应用逻辑 | 预发布应用的标准化调用接口，强调“即开即用”与组件化能力复用 | 可编程智能体的基础设施层，支持细粒度编排、状态管理与技能扩展 |
| **输入格式** | Python/Java 对象（`Document`, `Node`, `messages` 列表等），需手动构造；支持结构化文档解析（PDF/DOCX）与语义切分 | HTTP 请求体中传入 `prompt`（单轮）或 `messages`（多轮数组，含 `role: "user"/"system"`）；支持 `session_id` 复用上下文 | JSON 请求体，含 `input` 字符串或结构化对象；支持通过 `Memory Store` 注入上下文变量（如 `{{ memory.user_preference }}`） |
| **输出格式** | 同步返回 `Response` 对象（含 `response`, `source_nodes`, `metadata`）；LlamaIndex 支持流式迭代器；Spring AI Alibaba 返回 `ChatResponse` 或 `List<Document>` | 同步响应（JSON）或 Server-Sent Events（SSE）流式响应；`incremental_output=true` 时按 token 分片；`responses` 兼容 OpenAI 格式 | SSE 事件流（`event: agent_step`, `event: agent_finish`）；支持 `include_events=true` 查询完整执行轨迹；输出结构由 `prompt_template` 控制 |
| **支持模型** | ✅ 完整支持：`qwen-max`, `qwen-plus`, `text-embedding-v1/v2/v3`, `gte-rerank-*` 等；可自由组合 LLM + Embedding + Rerank | ❌ 不直接暴露模型选择；模型能力由已发布的智能体/工作流应用预绑定（如某 Agent 固定使用 `qwen-plus`） | ✅ 运行时指定：创建 Agent 时通过 `model` 字段声明（如 `"qwen-max"`），需在项目配额内；支持动态切换模型版本 |
| **API 端点** | 无统一 REST 端点；通过 SDK 调用各组件（如 `DashScopeCloudIndex.as_retriever()` → 内部调用百炼云端索引服务） | ✅ 明确两类端点：<br>• 应用调用：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（DashScope）<br>• 组件管理：`POST /{workspaceId}/promptTemplates`（OpenAPI） | ✅ 统一 RESTful 端点：<br>`POST /v1/agents`（创建）<br>`POST /v1/sessions`（启动会话）<br>`GET /v1/sessions/{id}/events`（查询事件） |
| **认证方式** | SDK 内置 API Key（`DASHSCOPE_API_KEY` 环境变量或显式传参） | ⚠️ 双模式：<br>• 应用调用：`Authorization: Bearer <api-key>`<br>• 组件类（Prompt/Memory）：阿里云 AccessKey 签名（ACS3-HMAC-SHA256） | ✅ 统一 Bearer Token：`Authorization: Bearer <access_token>`（通过百炼 OAuth2 获取） |
| **计费方式** | 按调用次数与资源消耗计费：<br>• LLM/Embedding/Rerank：按 token 计费<br>• 文档解析、云端索引存储：按页/GB/请求量计费 | 按应用调用次数计费（每次 `completion` 请求）；Prompt 模板、Memory 等组件操作免费 | 按 Agent 实例运行时长（秒）+ Session 事件数 + Memory 存储量计费；Skill Webhook 调用不额外计费 |
| **知识库支持** | ✅ 深度集成：<br>• `DashScopeCloudIndex`：一键构建云端向量库（强制使用百炼默认切分+向量化）<br>• `VectorStoreIndex`：本地索引（支持自定义 `NodeParser`/`Embedding`） | ✅ 间接支持：<br>• 通过 `DashScopeDocumentRetriever`（Spring AI）或 RAG API 调用知识库<br>• 仅支持百炼托管知识库，不支持自定义切分/向量模型 | ✅ 原生支持：<br>• 可将 `KnowledgeBase ID` 作为 Skill 注册，动态注入检索能力<br>• 支持混合检索（向量+关键词）与重排 |
| **[长期记忆](../concepts/long-term-memory.md)** | ❌ 无内置能力；需自行实现（如 Redis 存储对话历史） | ✅ 提供 `Memory`（记忆体）与 `MemoryNode`（片段）两级 API（标记为“旧”，建议评估替代方案） | ✅ 内置 `Memory Store`：键值对存储，支持 TTL、结构化访问（`{{ memory.key }}`）、最大 1MB/条、项目级配额管理 |
| **技能/工具扩展** | ✅ 完全自主：可集成任意 Python 函数、HTTP API、数据库驱动；LlamaIndex 支持 `Tool` 接口 | ❌ 不支持动态扩展；功能边界由应用发布者定义（如某工作流内置“查天气”技能） | ✅ 原生支持 `Skill`：注册 Webhook 类型技能（HTTP 回调），支持动态绑定/解绑；不支持本地函数（v2.3+ 已移除） |
| **环境与隔离** | ❌ 无运行时环境概念；依赖开发者代码组织（如多租户需自行实现） | ✅ 通过 `Workspace ID` 实现业务空间隔离（跨地域必需）；子业务空间需显式传递 Header | ✅ 强隔离：`Environment` 抽象（多租户/多版本），`Agent` 实例绑定特定 Environment，配置完全独立 |

## 各方案适用场景建议

- **选择智能体开发框架（Frameworks）当且仅当**：  
  ✅ 需要**深度定制 RAG 流程**（如自定义中文语义切分规则、混合检索策略、私有 Embedding 模型微调）；  
  ✅ 构建**复杂 Agent 逻辑**（如多跳推理、动态工具选择、异步任务编排），且团队具备 Python/Java 工程能力；  
  ✅ 已有 LlamaIndex/Spring AI Alibaba 技术栈，希望**最小成本迁移至百炼**并复用生态能力；  
  ❌ 不推荐用于快速上线简单问答 Bot 或需频繁 A/B 测试 Prompt 的场景。

- **选择流程型智能体（Flow Agent）当且仅当**：  
  ✅ 需要**快速集成已发布的智能体/工作流**（如客服助手、合同审核 Agent），关注业务交付而非底层实现；  
  ✅ 依赖**Prompt 模板管理**与**轻量级[长期记忆](../concepts/long-term-memory.md)**（如用户偏好存储），且接受平台托管的旧版 Memory 方案；  
  ✅ 项目部署在**华北2（北京）地域**，或能接受 Workspace ID 的显式管理；  
  ❌ 不推荐用于需跨地域部署、要求模型热切换、或需对接私有工具链的场景。

- **选择托管智能体（Managed Agents）当且仅当**：  
  ✅ 需要**生产级可运维的智能体服务**：明确的生命周期（启停/销毁）、会话状态持久化（24h）、事件溯源与可观测性；  
  ✅ 要求**强环境隔离与安全管控**（如金融客户多租户 SaaS 场景，需 `Environment` 级配置隔离 + `Vault` 凭证管理）；  
  ✅ 构建**技能中心化平台**：统一注册 Webhook 技能（如支付、CRM、ERP），供多个 Agent 动态复用；  
  ❌ 不推荐用于原型验证或极简单轮问答（此时 Flow Agent 更轻量）。

## 技术选型参考指南（面向开发者）

| 你的需求 | 推荐方案 | 关键理由 | 注意事项 |
|----------|----------|----------|----------|
| “我要用百炼的 PDF 解析 + 向量库，但必须用自己的分词器和 Embedding 模型” | **Frameworks** | `DashScopeJsonNodeParser` 和 `DashScopeEmbedding` 支持完全自定义；`VectorStoreIndex` 可绕过云端强制流程 | 需自行维护向量库更新、检索逻辑；不享受百炼云端索引的高并发优化 |
| “我已有一个训练好的 Qwen 微调模型，想封装成 API 供前端调用” | **Managed Agents** | 创建 Agent 时指定 `model: "my-qwen-finetuned"`（需先开通模型权限），通过 `/v1/sessions` 提供标准接口 | 微调模型需在百炼平台完成部署并获取有效 model_id；不支持直接上传 HuggingFace 模型权重 |
| “运营同学需要每周更换客服 Bot 的回答模板，且要记录用户常见问题” | **Flow Agent** | 使用 Prompt 模板 API 动态更新 `content`；`MemoryNode` 可存用户问题摘要；控制台界面友好 | `Memory` 为遗留方案，新项目应规划迁移到 Managed Agents 的 `Memory Store` 或自建方案 |
| “我们是 ISV，要为 100 家客户部署独立知识库问答 Bot，每家配置不同” | **Managed Agents + Frameworks 结合** | 用 Frameworks 构建通用 RAG 核心（`DashScopeCloudIndex`），用 Managed Agents 封装为多租户 Agent 实例（每个客户一个 `Environment`） | 需双 SDK 集成；`Environment` 配置需自动化脚本管理 |
| “快速验证一个想法：用大模型总结会议纪要并生成待办事项” | **Flow Agent**（首选）或 **Managed Agents**（次选） | Flow Agent 可 5 分钟发布一个工作流并调用；Managed Agents 提供更可控的调试事件流 | 避免从 Frameworks 开始——开发成本过高，偏离验证目标 |

> **重要提醒**：  
> - **地域限制是硬约束**：Flow Agent 的应用调用接口**仅支持华北2（北京）**，跨地域调用必失败；Frameworks 和 Managed Agents 无此限制（模型服务地域以实际开通为准）。  
> - **演进趋势**：百炼正推动能力收敛——`Memory Store`（Managed Agents）已替代旧版 `Memory`；未来 Frameworks 的 `DashScopeCloudIndex` 可能开放自定义切分插件。建议新项目优先采用 Managed Agents 作为智能体底座，Framework 作为能力增强层。  
> - **成本敏感型项目**：若主要负载为高频简单问答，Flow Agent 的按次计费通常低于 Managed Agents 的按秒计费；若需长会话（>10分钟）或复杂技能链，Managed Agents 的综合成本可能更低。

## 被对比主题页

- [frameworks](../api/frameworks.md)
- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)


