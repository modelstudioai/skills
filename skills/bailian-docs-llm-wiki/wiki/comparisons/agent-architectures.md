# 智能体架构方案对比：流程型、托管型与应用调用型

为帮助开发者在百炼平台上高效选型，本文系统对比三种主流智能体集成与部署范式：**流程型（Flow Agent）**、**托管型（Managed Agents）** 与 **应用调用型（Application Call）**。三者定位不同——流程型聚焦底层组件编排与控制平面管理；托管型提供全生命周期可编程 Agent 运行时；应用调用型则面向开箱即用的生产级服务集成。本对比基于当前（2024年Q3）百炼平台公开 API 文档与最佳实践，旨在明确各方案的能力边界、技术约束与适用阶段，避免因误用导致开发返工或运维风险。

---

## 关键维度对比

| 维度 | 流程型（Flow Agent API） | 托管型（Managed Agents API） | 应用调用型（Application Call） |
|------|---------------------------|------------------------------|-------------------------------|
| **核心定位** | 智能体/工作流应用的**调度控制平面 + 底层组件（记忆、Prompt）管理接口** | **可编程、有状态、可扩展的 Agent 运行时基础设施** | **已发布智能体/工作流的标准化服务调用通道** |
| **输入格式** | • 应用调用：`prompt`（单轮）或 `messages`（多轮），需显式传入 `workspaceId`（嵌入 URL）<br>• 组件管理：`CreateMemoryNode` 等需 `memoryId` + `content`（1–200 字符纯文本） | `POST /v1/sessions/{session_id}/messages`，请求体为标准 OpenAI 风格 `messages` 数组；支持 `file_list`、`image_list` 及 `biz_params` 透传 | • DashScope 原生：`input.prompt` 或 `input.messages`，支持 `session_id` 自动续聊<br>• OpenAI 兼容模式：`messages` 数组或 `input_text`/`input_image`，支持 `stream=true` 和 `background=true`（异步） |
| **输出格式** | • 应用调用：结构化 JSON（含 `output.text`、`usage`、`request_id`）<br>• 组件管理：CRUD 操作结果（如 `memoryId`、`node_id`），无模型推理输出 | SSE 流式响应（含 `agent_step`、`agent_finish` 事件）或轮询 `GET /v1/sessions/{id}` 获取完整会话状态；输出含 `steps` 执行轨迹、`final_output` 及 `memory_store` 快照 | • 同步：JSON（`choices[0].message.content`）或 SSE 流式 delta<br>• 异步：立即返回 `task_id`，后续 `GET /responses/{task_id}` 获取结果；支持 OpenAI 格式兼容响应 |
| **支持模型** | **不直接调用模型**；仅调度已发布的智能体/工作流（其内部模型由发布时配置决定） | **用户自主指定模型**（如 `qwen-max`、`qwen-plus`），受平台模型白名单约束；模型能力由 Agent 配置驱动 | **不感知底层模型**；调用对象是已发布的应用，其模型已在控制台配置并固化（如 Qwen-VL、Qwen-Max） |
| **API 端点** | • 应用调用：`https://{workspaceId}.cn-beijing.maas.aliyuncs.com/api/v1/apps/{app_id}/completion`<br>• 组件管理：`https://bailian.{regionId}.aliyuncs.com`（OpenAPI 风格） | 统一 `https://dashscope.aliyuncs.com/api/v1/` 前缀，资源路径如 `/v1/agents`、`/v1/sessions`、`/v1/skills` | • DashScope 原生：`https://dashscope.aliyuncs.com/api/v1/apps/{app_id}/completion`<br>• OpenAI 兼容：`https://dashscope.aliyuncs.com/api/v2/apps/agent/{app_id}/compatible-mode/v1/responses` |
| **鉴权方式** | **严格分离**：<br>• 应用调用：`Authorization: Bearer <API_KEY>`<br>• 组件管理：AccessKey 签名（ACS3-HMAC-SHA256），**不支持 Bearer** | **统一 Bearer [Token](../concepts/token.md)**（通过 `/v1/auth/token` 获取或控制台生成） | **统一 Bearer [Token](../concepts/token.md)**（`DASHSCOPE_API_KEY`），子空间需额外 Header `X-DashScope-WorkSpace` |
| **计费方式** | • 应用调用：按**调用次数 + 输出 token** 计费（归属对应 App 的计费主体）<br>• 组件管理（[长期记忆](../concepts/long-term-memory.md)）：**当前免费**，但属遗留能力，不承诺长期支持 | 按 **Agent 实例运行时长（秒） + 调用次数 + token 消耗** 综合计费；`Memory Store`、`Vault` 存储按量计费 | 按 **调用次数 + 输入/输出 token** 计费；文件/图像处理另计费用；OpenAI 兼容模式计费逻辑与原生一致 |
| **典型场景** | • 在自研系统中集成百炼已发布的工作流，同时需动态管理用户专属[长期记忆](../concepts/long-term-memory.md)（旧版）<br>• 构建低代码平台，需批量创建/更新 Prompt 模板与记忆体 | • 需要细粒度控制 Agent 行为：如拦截中间步骤、注入运行时上下文、绑定动态 Skill、实现会话级状态共享<br>• 多租户 SaaS 应用，要求环境隔离（Environment）、凭证安全（Credential）、技能热插拔 | • 快速将百炼智能体嵌入现有业务系统（如客服对话框、CRM 工单助手）<br>• 使用 OpenAI SDK 生态快速迁移，或需[异步任务](../concepts/asynchronous-task.md)（如长周期报告生成） |

---

## 适用场景建议

| 方案 | 推荐采用场景 | 不推荐场景 |
|------|--------------|-------------|
| **流程型（Flow Agent）** | ✅ 需要**同时调用智能体应用 + 管理用户级[长期记忆](../concepts/long-term-memory.md)（旧版）** 的混合场景（如个性化导购机器人，记忆用户偏好并调用推荐工作流）<br>✅ 构建**轻量级低代码集成平台**，需批量操作 Prompt 模板、记忆体等元数据 | ❌ 新项目单独使用“长期记忆（旧）”——该能力已标记为遗留，新需求应优先选用向量知识库或新版记忆服务<br>❌ 需要实时监控 Agent 内部执行步骤或动态修改运行时行为（如条件跳过某 Skill） |
| **托管型（Managed Agents）** | ✅ 构建**高可控性、可调试、可扩展的智能体产品**：如企业级自动化助理，需对接内部 Webhook Skill、按会话隔离敏感凭证、记录每一步决策日志<br>✅ 需要**强会话状态管理**：如多轮表单填写、复杂问题拆解（需 `agent_step` 事件驱动 UI 更新）<br>✅ 多租户环境，要求 `Environment` 级别配置隔离与灰度发布 | ❌ 简单单轮问答集成（过度设计，增加运维复杂度）<br>❌ 对延迟极度敏感且无法接受 SSE 流式协议的客户端（如部分嵌入式设备） |
| **应用调用型（Application Call）** | ✅ **生产环境快速落地**：已有成熟智能体/工作流，只需标准 API 对接（如嵌入微信小程序、钉钉机器人）<br>✅ **生态兼容优先**：团队已使用 OpenAI SDK，希望零改造接入百炼能力<br>✅ **异步长任务**：如文档分析、视频摘要，需 `background=true` + `retrieve` 模式 | ❌ 需要深度定制 Agent 内部逻辑（如修改 LLM 提示词模板、替换某个[工具调用](../concepts/tool-calling.md)逻辑）<br>❌ 需要跨会话共享结构化状态（如购物车、审批流程状态），因其 `session_id` 仅缓存 1 小时且不开放持久化接口 |

---

## 技术选型参考（面向开发者）

请按以下决策树进行选型：

1. **你的目标是“调用一个现成的智能体”，而非“构建一个智能体”？**  
   → 是 → 选 **应用调用型**（最简路径，SDK 支持完善，生产就绪）  
   → 否 → 进入第 2 步  

2. **你是否需要完全掌控 Agent 的运行时行为（如步骤拦截、动态 Skill 绑定、会话级内存管理）？**  
   → 是 → 选 **托管型**（提供 `Environment`、`Session`、`Memory Store`、`Skill` 全栈能力）  
   → 否 → 进入第 3 步  

3. **你是否必须在调用智能体的同时，管理一批用户专属的、结构简单的文本记忆（且接受该能力为遗留方案）？**  
   → 是 → 选 **流程型**（仅当“应用调用 + 旧版长期记忆”组合不可替代时）  
   → 否 → **强烈建议回归应用调用型**（搭配新版向量知识库或 RAG 配置实现更健壮的记忆能力）  

> **关键提醒**：  
> - **避免混用鉴权**：Flow Agent 的组件类接口（如 `CreateMemory`）**绝不接受 `Bearer` [Token](../concepts/token.md)**，务必使用 AccessKey 签名，否则 403。  
> - **地域注意**：应用调用型与托管型 API 默认支持华北2（北京），但 Workspace ID 在法兰克福、新加坡等地同样有效，请以控制台实际可用区域为准。  
> - **演进趋势**：平台正推动“长期记忆（旧）”向向量知识库迁移，“本地 Python Skill”已下线——新项目应默认采用托管型的 Webhook Skill 或应用调用型的 RAG 配置，确保长期兼容性。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [application call](../api/application-call.md)


