# 智能体开发框架：通用框架、流程型Agent与托管Agent对比

为帮助开发者在阿里云百炼平台上高效选型，本文对三类主流智能体开发路径进行系统性对比：**通用框架（LlamaIndex/Spring AI Alibaba 集成）**、**流程型 Agent（Flow Agent API）** 与 **托管型 Agent（Managed Agents API）**。三者定位不同——通用框架聚焦 *AI 原语封装与知识增强应用构建*，流程型 Agent 强调 *可视化编排与确定性任务执行*，托管型 Agent 则提供 *全生命周期托管的生产级智能体运行时*。本对比旨在厘清能力边界、明确适用约束，降低技术决策成本，避免因方案错配导致重复开发或运维负担。

## 关键维度对比

| 维度 | 通用框架（LlamaIndex / Spring AI Alibaba） | 流程型 Agent（Flow Agent API） | 托管型 Agent（Managed Agents API） |
|------|------------------------------------------|--------------------------------|-------------------------------------|
| **核心定位** | AI 开发工具链集成层，用于快速构建 RAG、检索增强、模型调用等基础能力 | 预定义多步骤工作流的可编程封装，强调结构化任务编排与状态保持 | 全托管、可配置、带[长期记忆](../concepts/long-term-memory.md)与工具生态的生产级 Agent 运行时服务 |
| **输入格式** | 灵活：支持原始文本、`Document` 对象、结构化 `input_schema`（Spring）、`Prompt` 实例等；无强 schema 约束（除 Flow 调用外） | **强约束**：必须严格匹配 Flow 编辑器中定义的首个节点 `input_schema`（JSON Schema），字段缺失/类型错误返回 400 | 灵活但结构化：支持 `text` 字符串、`files` 数组（上传后引用）、`tool_choice` 控制策略；`input` 为 JSON 对象，含 `content` + 可选 `metadata` |
| **输出格式** | 多样：可返回 `Response` 对象、`QueryBundle`、`List[Node]`、`StreamEvent`（流式）等，由上层框架逻辑决定 | **固定结构化 JSON**：`{ "status": "success" \| "failed", "output": { ... }, "trace_id": "...", "session_id": "..." }`；流式响应为 SSE 格式事件流 | **标准化消息流**：非流式返回 `Message` 对象（含 `role`, `content`, `tool_calls`）；流式为 SSE 事件（`message`, `tool_call`, `tool_result`, `done`） |
| **支持模型** | 全量百炼文本生成模型（`qwen-max`/`qwen-plus`/`qwen-turbo` 等）+ Embedding（`text-embedding-v1/v2/v3`）+ Rerank（`gte-rerank`） | **仅 `flow-agent-v1`（百炼自研专用模型）**，不兼容通用大模型直接调用 | 仅百炼托管模型：`qwen-max`、`qwen-plus`、`qwen-turbo`；**不支持自定义模型或 HuggingFace 模型** |
| **API 端点** | 分散式组件调用：<br>• LlamaIndex：`index.as_query_engine()` / `retriever.retrieve()`<br>• Spring AI：`DashScopeAgent.call()` / `DashScopeDocumentRetriever.retrieve()` | 统一端点：<br>`POST https://dashscope.aliyuncs.com/api/v1/agents/{app_id}/invoke` | RESTful 资源化端点：<br>• 创建 Agent：`POST /agents`<br>• 启动会话：`POST /sessions`<br>• 发送消息：`POST /sessions/{id}/messages` |
| **计费方式** | **按调用粒度计费**：<br>• LLM 调用：按 token 计费（输入+输出）<br>• Embedding/Rerank/Parse：按调用次数或文档页数计费<br>• 云端知识库（`DashScopeCloudIndex`）：按索引容量 + 检索次数计费 | **按 Flow 执行计费**：<br>• 按成功完成的 Flow 实例计费（含所有内部节点消耗）<br>• 流式调用不额外计费，但计入总执行时长 | **按资源实例 + 使用量混合计费**：<br>• Agent/Environment/Memory Store：按月订阅或按小时计费（资源占用）<br>• Session 消息处理：按 token 计费（输入+输出+工具调用上下文）<br>• 文件解析/工具调用：按次计费 |
| **[长期记忆](../concepts/long-term-memory.md)支持** | ❌ 无原生支持；需自行集成向量数据库（如 `VectorStoreIndex`）或使用 `DashScopeCloudIndex`（仅限云端知识库检索） | ✅ 支持（新版）：通过 `memory_context` 字段注入历史片段，**无持久化存储**，依赖 `session_id` 生命周期（默认 24h） | ✅ 原生支持：`Memory Store` 提供持久化向量记忆（TTL 默认 7 天，企业版可延长），自动关联 Session 与 Agent |
| **工具调用能力** | ⚠️ 有限：LlamaIndex 需手动集成 `Tool` 类并编写 `ToolOutputParser`；Spring AI `DashScopeAgent` 仅支持调用百炼已发布应用（App ID） | ✅ 内置：在 Flow 编辑器中预配置 HTTP/DB/API 工具，节点内自动触发，**不可动态选择** | ✅ 动态可控：支持 `tool_choice: "auto"` / `"none"` / `"skill_id"`；Skill 可独立管理、版本化、权限控制 |
| **定制化能力** | ✅ 高：可替换任意组件（LLM、Embedding、NodeParser、Reranker、Retriever），支持本地部署与私有模型接入 | ❌ 低：逻辑完全在 Flow 编辑器中可视化编排，无法修改底层模型推理、切分、嵌入逻辑 | ⚠️ 中：支持配置 Prompt 模板、Memory Store 类型、Tool 绑定、Webhook 回调；**不支持替换核心模型或自定义推理逻辑** |
| **典型场景** | • 快速搭建 RAG 应用<br>• 构建企业知识库问答系统<br>• 数据分析报告生成（结合本地代码解释器）<br>• 多模型协同实验（如 v2 Embedding + v3 Rerank） | • 客服工单自动分派与闭环<br>• 合同关键条款提取与合规校验流水线<br>• 多步骤数据清洗与报表生成（ETL-like）<br>• 标准化业务审批流程（申请→初审→复核→归档） | • 个人智能助理（跨会话记忆、文件理解、日程管理）<br>• 销售顾问 Agent（记住客户历史、调用 CRM、生成提案）<br>• DevOps 自动化助手（读取日志、调用监控 API、生成修复建议）<br>• 合规审计 Agent（持续记忆审计规则、扫描文档、生成报告） |

## 各方案适用场景建议

- **选择通用框架（LlamaIndex / Spring AI Alibaba）当且仅当**：  
  ✅ 项目处于原型验证或 MVP 阶段，需快速验证 RAG、检索、模型调用等基础能力；  
  ✅ 对数据敏感性要求高，需将 Embedding、切分、索引等环节完全本地化部署；  
  ✅ 需要灵活组合多种模型（如 `qwen-plus` 生成 + `text-embedding-v3` 向量化 + `gte-rerank-hybrid` 重排）；  
  ❌ 不适合需要开箱即用的[长期记忆](../concepts/long-term-memory.md)、复杂多轮对话状态管理或生产级环境隔离的场景。

- **选择流程型 Agent（Flow Agent API）当且仅当**：  
  ✅ 业务逻辑高度结构化、步骤明确且变更频率低（如金融风控审批、物流状态追踪）；  
  ✅ 团队具备低代码/无代码协作能力，希望产品、运营人员参与流程设计；  
  ✅ 需要强输入校验、确定性执行路径与清晰的节点级可观测性（Trace）；  
  ❌ 不适合需要动态决策（如“根据用户情绪切换回复策略”）、实时学习反馈或接入大量异构外部系统的场景。

- **选择托管型 Agent（Managed Agents API）当且仅当**：  
  ✅ 构建面向终端用户的生产级 Agent 产品（如 SaaS 客服助手、智能办公插件）；  
  ✅ 要求开箱即用的长期记忆、安全凭证管理（Credential Vault）、文件多模态理解（PDF/CSV 解析）、事件驱动（Webhook）；  
  ✅ 需要细粒度资源治理（Environment 隔离测试/生产环境）、会话级 SLA 保障与企业级审计日志；  
  ❌ 不适合超轻量级需求（如单次问答）、预算受限且无需记忆/工具的简单场景，或需深度定制模型推理内核的科研项目。

## 技术选型参考指南（面向开发者）

| 你的关键诉求 | 推荐方案 | 理由说明 |
|--------------|----------|----------|
| “我只想快速试一个知识库问答，明天就要给老板演示” | **通用框架（LlamaIndex）** | 5 行代码初始化 `DashScopeCloudIndex` + `as_query_engine()`，无需创建任何平台资源，零配置启动。 |
| “我们的报销流程有 7 个固定环节，法务、财务、HR 都要介入，必须留痕可追溯” | **流程型 Agent** | 在 Flow 编辑器中拖拽配置审批节点、设置角色审批条件、绑定电子签章工具，自动生成可审计的 Trace 日志。 |
| “我们要上线‘智能销售助手’SaaS 服务，每位客户拥有独立记忆空间，能上传合同 PDF 并调用 CRM API” | **托管型 Agent** | 直接使用 `Memory Store` 隔离客户数据，`File` 接口解析 PDF，`Skill` 绑定 CRM SDK，`Webhook` 推送商机更新，全部免运维。 |
| “我们需要在私有云部署，所有数据不出内网，且要用自研的 Embedding 模型” | **通用框架（LlamaIndex 本地模式）** | 替换 `DashScopeEmbedding` 为 `HuggingFaceEmbedding`，使用 `SimpleDirectoryReader` 本地加载文档，`VectorStoreIndex` 接入私有 Milvus。 |
| “Agent 需要根据用户历史行为动态调整工具调用策略（例如老客户跳过身份验证）” | **托管型 Agent** | 利用 `Memory Store` 查询用户画像，通过 `tool_choice` 字段在请求时动态指定是否启用 `verify_identity_skill`。 |
| “我们已有 Spring Boot 微服务架构，希望最小改造接入 AI 能力” | **通用框架（Spring AI Alibaba）** | 仅需引入 `spring-ai-alibaba-starter-dashscope`，配置 `application.yml`，即可用 `@Autowired DashScopeAgent` 注入调用，无缝融入现有 Bean 生命周期。 |

> **重要提醒**：三者并非互斥，而是可分层组合。典型实践是——**用通用框架构建知识底座（RAG）**，**将其封装为 Skill 或云端知识库（`DashScopeCloudRetriever`）**，**再注入到托管型 Agent 的 Memory 或 Flow Agent 的工具节点中**，实现能力复用与架构解耦。

## 被对比主题页

- [frameworks](../api/frameworks.md)
- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)


