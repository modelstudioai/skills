# 流程型智能体、OpenAI 兼容智能体与托管智能体对比

为帮助开发者在百炼平台中高效选型，本文系统对比三类主流智能体能力方案：**流程型智能体（Flow Agent）**、**OpenAI 兼容智能体（OpenAI-Compatible Agents）** 与 **托管智能体（Managed Agents）**。三者均面向生产级 AI 应用构建，但在设计哲学、抽象层级、集成方式和适用边界上存在显著差异。本对比基于当前（2024年Q3）百炼平台正式发布的 API 规范与行为约束，聚焦可落地的技术决策维度，不涉及概念性或未来规划内容。

---

## 关键维度对比

| 维度 | 流程型智能体（Flow Agent） | OpenAI 兼容智能体（OpenAI-Compatible Agents） | 托管智能体（Managed Agents） |
|------|---------------------------|-----------------------------------------------|------------------------------|
| **核心定位** | 面向**已发布应用/工作流的调用与编排**，强调“运行时即服务” | 面向**标准协议兼容与快速迁移**，提供 OpenAI 风格 Agent 运行时 | 面向**全生命周期自主管理**，提供细粒度资源控制与扩展能力 |
| **输入格式** | 支持 `prompt`（单轮文本）或标准 `messages` 数组（含 `system`/`user`/`assistant`），支持多模态结构；需显式传 `app_id` | 完全兼容 OpenAI `chat.completions` 输入格式（`messages` + `tools` + `tool_choice`），首条 `system` 消息为最佳实践 | 使用自定义 RESTful 结构：`POST /v1/sessions/{id}/chat`，`messages` 格式同 OpenAI，但需先创建 `session_id` 和（推荐）`environment_id` |
| **输出格式** | 同步返回 JSON 或 SSE 流式响应；含 `output.text` / `output.choices[0].message.content`；异步模式返回 `task_id` | 基本兼容 OpenAI 响应结构（`choices[0].message` + `tool_calls`），**额外返回 `session_id` 字段**用于续聊 | 返回标准化 JSON，含 `response.message.content` 及 `tool_calls`；支持 `stream=true`，但**不返回 `session_id`（由客户端维护）**；状态变更需主动调用 `/sessions/{id}/extend` |
| **支持模型** | 不直接绑定模型，底层由应用/工作流配置决定（可含 Qwen 系列、多模态、插件增强等） | **仅限 Agent 专用模型**：`qwen-plus-agent-v1`（推荐）、`qwen-max-agent-v1`（已弃用） | **仅限百炼托管 Qwen 模型**：`qwen-max`、`qwen-plus`、`qwen-turbo`；**不支持外部或自定义模型** |
| **API 端点** | • 应用调用：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（DashScope）<br>• 组件管理：`https://bailian.{region}.aliyuncs.com/{workspaceId}/...`（OpenAPI） | `https://dashscope.aliyuncs.com/compatible-mode/v1/agents/chat/completions`（统一入口） | `https://dashscope.aliyuncs.com/v1/sessions/{session_id}/chat`（所有操作以 `/v1/` 为根路径） |
| **鉴权方式** | **双体系并存**：<br>• 应用调用：`Bearer <百炼 API Key>`<br>• Prompt/Memory 等组件：阿里云 `AccessKey` 签名（ACS3-HMAC-SHA256） | **统一 Bearer Token**：<br>`Authorization: Bearer <API Key>`（需含 `agents:run` 权限） | **统一 Bearer Token**：<br>`Authorization: Bearer <API Key>`（平台颁发，非 AccessKey） |
| **[长期记忆](../concepts/long-term-memory.md)支持** | ✅ 提供 `Memory`（记忆体）与 `MemoryNode`（片段）两级 API，支持 CRUD 与分页；<br>⚠️ **不支持用户画像存储**（需控制台操作）；<br>⚠️ **1 秒限频** | ✅ Session 级上下文自动持久化（TTL=24h）；<br>✅ Vault 支持安全凭证存储（需显式占位符引用）；<br>❌ 无独立 Memory 存储 API | ✅ 内置 `Memory Store`（TTL=7天，默认不可调）；<br>✅ 支持导出（`/memory_store/{id}/export`）；<br>✅ 与 Session 强绑定，自动加载 |
| **工具调用能力** | ⚠️ 依赖工作流内嵌节点或插件配置，**无原生 `tools` 参数接口**；需通过 Prompt 工程或组件编排实现 | ✅ 原生支持 OpenAI 风格 `tools` + `tool_choice`；自动选择、调用、返回 `tool_calls`；需客户端执行工具并回传 `tool_result` | ✅ 支持 Skill 封装（类 `tools`），通过 `tool_choice` 控制；<br>⚠️ 单次最多调用 5 个工具（含嵌套）；<br>⚠️ 若设 `tool_choice=auto` 但未注册 Skill，请求直接失败 |
| **环境隔离** | ❌ 无运行环境抽象；依赖工作流内部沙箱或外部服务集成 | ✅ 支持 `environment_id` 绑定预配置环境（如 Python 沙箱、DB 连接池） | ✅ 强环境模型：`POST /v1/environments` 可定制依赖、超时、资源限制；<br>⚠️ **未指定 environment_id 时使用 `default`，易引发冲突** |
| **计费方式** | 按**调用量计费**：<br>• 应用调用：按 token（输入+输出）计费<br>• Prompt/Memory 等组件：按 API 调用次数计费（低频） | 按**Agent 模型调用 token 计费**（同百炼通用模型计费规则），与 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)一致 | 按**托管资源消耗计费**：<br>• Agent 实例、Session、Environment、Memory Store 均为独立计费单元<br>• 文件上传、Webhook 等扩展能力单独计费 |
| **典型场景** | • 快速上线已配置好的客服机器人、审批工作流<br>• 需要复用控制台 Prompt 模板与[长期记忆](../concepts/long-term-memory.md)的轻量级应用<br>• 多地域子业务空间（需 workspaceId）的合规部署 | • 将现有 OpenAI Agent 代码零改造迁入百炼<br>• 需要标准协议保障、便于多平台切换的中台能力<br>• 重视工具链生态（如已有大量 function tools） | • 构建高可靠、可审计、需长期状态保持的企业级自动化系统<br>• 要求环境强隔离、技能模块化、凭证集中管控<br>• 需深度定制运行时行为（如自定义 Webhook 事件、Skill 编排） |

---

## 适用场景建议

### ✅ 选择 **流程型智能体（Flow Agent）** 当：
- 你已在百炼控制台完成智能体或工作流的可视化搭建，**只需调用而非开发**；
- 项目对交付速度要求极高，且功能边界明确（如表单填写助手、FAQ 问答流）；
- 需要利用百炼内置的 Prompt 模板管理、会话上下文（`session_id`）或基础[长期记忆](../concepts/long-term-memory.md)（`Memory`）；
- 团队熟悉 DashScope 应用网关模式，且接受“应用 ID + Workspace ID”双标识管理。

### ✅ 选择 **OpenAI 兼容智能体（OpenAI-Compatible Agents）** 当：
- 你已有基于 OpenAI `chat.completions` + `tools` 的 Agent 代码，希望**最小成本迁移至百炼**；
- 团队技术栈偏好标准协议（如 LangChain、LlamaIndex），需保证跨平台可移植性；
- 场景以**工具驱动型任务**为主（如天气查询、数据库检索），且对 Session 生命周期（24h）可接受；
- 需要快速验证 Agent 能力，无需深度定制运行环境或内存策略。

### ✅ 选择 **托管智能体（Managed Agents）** 当：
- 你需要构建**生产级、可运维、可扩展的 AI 自动化系统**，例如合同审核流水线、多步骤数据治理 Agent；
- 对**安全性、隔离性、可观测性**有严格要求（如金融、政务场景），需 Environment/Vault/Skill 分层管控；
- 必须支持**长期状态保持**（>24h）且需自主控制 Memory TTL 与导出策略；
- 愿意承担稍高的学习成本与 API 调用复杂度，以换取最大控制权与企业级 SLA 保障。

---

## 技术选型参考（致开发者）

| 你的需求 | 推荐方案 | 关键理由 |
|----------|----------|----------|
| “我有一个现成的 OpenAI Agent，想今天就跑起来” | OpenAI 兼容智能体 | 仅需替换 endpoint 和 API Key，`messages`/`tools` 代码 0 修改；`session_id` 自动注入降低客户端逻辑负担。 |
| “我在控制台拖拽了一个审批工作流，现在要嵌入 App” | 流程型智能体 | 直接调用 `apps/{APP_ID}/completion`，无需重新定义模型、工具或环境；Prompt 模板、记忆体均可在控制台统一维护。 |
| “我要做一个银行风控 Agent，需连接内部数据库、加密存储密钥、记录每步决策日志” | 托管智能体 | Environment 隔离 DB 连接、Vault 安全注入凭证、Webhook 推送审计事件、Memory Store 持久化决策链——全部原生支持。 |
| “我需要同时支持北京、法兰克福、东京三地用户，且各区域数据不出域” | 流程型智能体（子空间） + 托管智能体（多 region 部署） | Flow Agent 支持 `workspaceId` 显式指定地域；Managed Agents 可分别在各 region 创建独立 `environment` 和 `agent` 实例；[OpenAI 兼容接口](../concepts/openai-compatible-interface.md)暂未明确标注多地域支持。 |
| “我团队没有后端工程师，只有前端和产品，想快速试错” | 流程型智能体 | 控制台完成全部配置，前端仅需调用一个 REST 接口；无需理解 Session、Environment、Vault 等概念。 |

> **重要提醒**：  
> - **不要混用认证体系**：Flow Agent 的组件类接口（Prompt/Memory）必须用 AccessKey 签名，而其他两类方案均只认 Bearer API Key；误用将导致 `401 Unauthorized`。  
> - **地域不是可选项**：Flow Agent 应用调用默认仅限华北2（北京）；若需其他地域，请确认文档是否明确支持，并严格使用对应 `workspaceId` 构造 URL。  
> - **模型 ≠ 万能**：`qwen-max-agent-v1` 已弃用，请勿用于新项目；`qwen-plus-agent-v1` 是当前 OpenAI 兼容方案唯一推荐模型；托管智能体不支持任何 `-agent` 后缀模型。  

---  
*本文档依据百炼平台 2024 年 9 月 API 文档快照编写，具体行为请以控制台最新文档及 OpenAPI Explorer 实际响应为准。*

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [managed agents api](../api/managed-agents-api.md)


