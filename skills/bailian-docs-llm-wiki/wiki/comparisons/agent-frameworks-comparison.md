# 智能体开发框架对比：Flow Agent、Managed Agents 与 Agent Context

本文旨在帮助百炼平台开发者清晰理解三种核心智能体能力模块的技术定位、能力边界与适用边界，避免因概念混淆导致架构误选或集成返工。三者并非并列的“同类框架”，而是面向不同抽象层级和工程目标的设计产物：  
- **Flow Agent** 是面向 *已发布应用* 的调用与记忆管理接口层，强调“复用”与“状态持久化”；  
- **Managed Agents** 是面向 *可编程智能体实例* 的全生命周期编排平台，强调“可控性”与“运行时灵活性”；  
- **Agent Context** 并非独立框架，而是 *模型推理阶段的上下文注入机制*，属于底层能力增强组件，强调“信息增强”与“响应精准性”。  

正确选型需回归业务本质：是快速接入一个现成智能体？还是需要从零构建可调试、可扩展、带会话状态与技能编排的智能体服务？抑或仅需在现有模型调用中动态注入知识片段提升回答质量？

---

## 关键维度对比

| 维度 | Flow Agent | Managed Agents | Agent Context |
|------|------------|----------------|----------------|
| **本质定位** | 应用调用 + [长期记忆](../concepts/long-term-memory.md)管理 API 集合 | 可编程智能体（Agent）的基础设施编排平台 | 模型推理时的动态上下文注入机制（非独立服务） |
| **输入格式** | • 应用调用：`POST /v1/agents/{agentId}/invoke`，请求体含 `input`（字符串或对象）、`memoryId`（可选）<br>• 记忆管理：标准 OpenAPI 请求（如 `CreateMemory` 含 `description`, `workspaceId`） | `POST /v1/agents` 创建 Agent；`POST /v1/sessions` 启动会话；消息通过 `POST /v1/sessions/{id}/messages` 提交，支持结构化 `content` + `tool_calls` | 作为 `system` 角色消息嵌入 `/v1/chat/completions` 请求体：`{"role": "system", "content": "{...}"}`，其中 `content` 是序列化后的 `context` 对象 |
| **输出格式** | • 应用调用：标准流式或非流式 JSON 响应（含 `output`, `request_id`, `trace_id`）<br>• 记忆操作：标准 OpenAPI 响应（如 `CreateMemory` 返回 `memoryId`, `createdAt`） | • 同步响应：Agent/Session 元数据（ID、状态、配置）<br>• 异步事件流：通过 SSE 或 Webhook 推送 `agent_step`、`agent_finish` 等事件，含 `step_type`, `tool_name`, `output` 等字段 | 与基础 `/v1/chat/completions` 输出一致（`choices[0].message.content`），无额外 context 字段；上下文效果体现于模型输出质量提升，不可见于响应结构 |
| **支持模型** | 不直接暴露模型选择；所调用的智能体/工作流应用由平台配置决定（底层多为 Qwen 系列），开发者无权在调用时切换 | 显式指定：`agent.runtime.model` 字段支持 `qwen-plus`、`qwen-max` 等（以 [Managed Agent API 概览](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) `supported_models` 为准） | 仅 `qwen-max`、`qwen-plus`、`qwen-turbo` 原生支持完整 context 解析；其他模型（如 `qwen2.5-7b`、`qwen1.5-14b-chat`）可能忽略或错误解析 |
| **API 端点** | • 应用调用：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com`（Bearer [Token](../concepts/token.md)）<br>• 记忆管理：`https://bailian.cn-beijing.aliyuncs.com`（ACS3 签名） | 统一端点：`https://dashscope.aliyuncs.com/api/v1`（Bearer [Token](../concepts/token.md)） | 复用标准大模型推理端点：`https://dashscope.aliyuncs.com/api/v1/chat/completions`（Bearer [Token](../concepts/token.md)） |
| **鉴权方式** | • 应用调用：百炼 API Key（`Authorization: Bearer <key>`）<br>• 记忆管理：阿里云 AccessKey 签名（ACS3-HMAC-SHA256），**不支持 Bearer Token** | 百炼 API Key（`Authorization: Bearer <access_token>`） | 百炼 API Key（`Authorization: Bearer <access_token>`） |
| **计费方式** | • 应用调用：按调用次数 + 模型 token 消耗计费（归属被调用应用所属 workspace）<br>• 记忆管理：[长期记忆](../concepts/long-term-memory.md)存储按容量（GB/月）+ API 调用次数计费（独立计量） | 按 Agent 实例运行时长（秒）、Session 消息数、Memory Store 容量、文件解析等多维度计费（详见 [计费说明](../../raw/application-api-reference/managed-agents-api/managed-agents-api-pricing.md)） | 无独立计费；计入底层 `/v1/chat/completions` 调用的 token 消耗（context 内容占用 input tokens） |
| **典型场景** | • 快速集成已上线的客服机器人、数据分析工作流<br>• 为多个用户维护独立的[长期记忆](../concepts/long-term-memory.md)库（如用户画像、偏好设置）<br>• 需要跨应用共享记忆体的轻量级协作 | • 构建具备复杂工具调用、多步骤决策、状态保持的定制 Agent（如自动化运维助手、销售陪练系统）<br>• 需要灰度发布、A/B 测试、事件审计的生产级智能体服务<br>• 多租户隔离、环境分级（dev/staging/prod）管理 | • 在标准模型调用中注入 RAG 检索结果，提升问答准确性<br>• 将对话历史片段作为 context 传入，增强回复连贯性<br>• 动态拼接第三方系统数据（如 CRM 客户信息）辅助决策 |

---

## 适用场景建议

### ✅ 优先选择 **Flow Agent** 当：
- 你已有在百炼控制台发布好的智能体或工作流应用，只需在自有系统中调用它；
- 你需要为每个终端用户独立维护一份结构化长期记忆（如“张三的订单偏好”、“李四的健康档案”），且该记忆需跨多次调用复用；
- 你接受记忆管理使用独立鉴权（AccessKey）和限流策略（≥1 秒间隔），并愿意自行持久化 `memoryId`/`memoryNodeId`。

### ✅ 优先选择 **Managed Agents** 当：
- 你需要从零开始定义 Agent 行为逻辑（如“先查知识库 → 若无结果则调用天气 API → 最后生成摘要”），而非复用预置应用；
- 你要求完整的会话状态管理（自动过期、最大步数限制、事件流监听）和技能热插拔能力；
- 你需要生产环境级保障：环境隔离、蓝绿部署、凭证安全 Vault、并发 Session 控制；
- 你希望 Agent 具备可观测性（通过事件流捕获每一步工具调用与中间结果）。

### ✅ 优先选择 **Agent Context** 当：
- 你已在使用 `/v1/chat/completions` 直接调用模型，仅需小幅增强单次响应质量；
- 你已有 RAG 知识库、Memory 库或 Connector 数据源，希望在不重构 Agent 架构的前提下注入上下文；
- 你追求极简集成——无需创建新资源、无需管理会话 ID 或 memory ID，只需在请求中添加一条 system 消息；
- 你确认所用模型在支持列表内（`qwen-max`/`qwen-plus`/`qwen-turbo`），且能接受 context 单次生效、不持久化、静默失败等约束。

---

## 技术选型参考（面向开发者）

| 你的需求 | 推荐方案 | 关键原因 |
|----------|----------|----------|
| “我有一个做合同审核的智能体，已在控制台发布，现在要嵌入到客户 CRM 中调用” | **Flow Agent（应用调用接口）** | 复用现有资产，最小改造；通过 `memoryId` 绑定客户专属记忆即可实现个性化审核 |
| “我要做一个支持多轮会议纪要整理 + 自动生成待办事项 + 同步钉钉的 Agent，需支持调试、灰度、审计” | **Managed Agents** | 唯一支持 `Session` 状态管理、`Skill` 动态绑定、`Webhook` 事件订阅的方案；`Environment` 隔离保障测试安全 |
| “我用 SDK 调用 `qwen-plus` 做客服问答，但常答不准，已有知识库，想让模型看到最新 FAQ” | **Agent Context（type="rag"）** | 无需改动 Agent 架构，只需将检索结果塞进 system 消息；成本最低、见效最快 |
| “我需要为 10 万用户每人维护一份‘产品使用习惯’记忆，并在每次调用推荐 Agent 时自动加载” | **Flow Agent（长期记忆） + Managed Agents（Agent 调用）组合** | 用 Flow Agent 的 `CreateMemory`/`UpdateMemoryNode` 管理海量用户记忆；用 Managed Agents 的 `Session` 调用推荐 Agent 并传入 `memoryId` |
| “我想用 `qwen2.5-7b` 自托管模型，同时注入 context” | **不适用 Agent Context** | 该模型不支持 context 解析；建议改用 `qwen-plus`，或自行在 [prompt](../guides/prompt.md) 中拼接上下文（非平台 context 机制） |

> ⚠️ **重要提醒**：  
> - **不要混用概念**：`Agent Context` 不是 Agent，不能被“创建”或“部署”；`Flow Agent` 的 `memoryId` 不能直接用于 `Managed Agents` 的 `Memory Store`；三者数据存储相互隔离。  
> - **鉴权是第一道关卡**：`Flow Agent` 记忆接口强制要求 AccessKey 签名，若只配置了 API Key 将 403；务必按文档区分 Base URL 与鉴权方式。  
> - **调试建议**：对 `Agent Context`，开启 `verbose=true` 参数（若 SDK 支持）或检查 `request_id` 日志；对 `Managed Agents`，务必订阅 `agent_step` 事件以观察真实执行流；对 `Flow Agent` 记忆操作，善用 `ListMemories` 验证数据写入。  

如需进一步评估具体业务场景的架构适配性，建议结合 [百炼智能体架构决策树](guides/agent-architecture-decision-tree.md) 进行逐项匹配。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent context](../guides/agent-context.md)


