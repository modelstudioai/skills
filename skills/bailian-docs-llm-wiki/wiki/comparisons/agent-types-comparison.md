# 流程型智能体、托管智能体与传统智能体架构对比

本文旨在帮助开发者清晰理解百炼平台当前三大主流智能体技术路径的核心差异，明确其定位、能力边界与适用阶段，从而在实际项目中做出高效、可持续的技术选型决策。随着百炼平台从早期低代码编排（Agent 1.0）向结构化工作流（Flow Agent）与全托管运行时（Managed Agents）演进，不同架构在模型支持、状态管理、工程可控性及运维成本上呈现显著分化。本对比基于官方最新文档（截至2024年Q3），聚焦可落地的工程事实，不涉及概念性推测。

## 关键维度对比

| 维度 | 流程型智能体（Flow Agent） | 托管智能体（Managed Agents） | 传统智能体（Agent Legacy / Agent 1.0） |
|------|---------------------------|------------------------------|----------------------------------------|
| **定位与本质** | **应用级工作流编排平台**：面向已发布的智能体/工作流应用提供标准化调用与组件管理能力，强调“发布即服务”（API-First） | **运行时托管平台**：提供带状态生命周期管理的 AI Agent 运行环境，强调“开箱即用的生产就绪能力”（Environment + Session + Memory Store） | **低代码提示词驱动引擎**：基于预置模板与插件的零代码/少代码智能体构建方式，强调“快速验证与垂直场景交付” |
| **输入格式** | • DashScope API：`prompt`（单轮）或 `messages`（多轮数组）<br>• Responses API：`input`（兼容 OpenAI `messages` 结构）<br>• 组件接口：`content`（Prompt 模板文本）、`memoryNode.content`（记忆片段） | • `/sessions/{id}/messages`：严格要求 `role`（user/assistant/tool）、`content`、`tool_calls` 等字段<br>• 支持结构化工具调用参数（JSON Schema 定义）<br>• `session_id` 必须显式创建并绑定 `environment_id` | • 控制台配置：`系统提示词` + `用户输入文本`<br>• API 调用：仅支持纯文本 `prompt` 字段（无原生 `messages` 多轮支持）<br>• 上下文轮数由 `携带的上下文轮数` 参数控制（非消息数组） |
| **输出格式** | • 同步：标准 JSON 响应（含 `output.text`、`usage`、`request_id`）<br>• 流式：SSE 协议，支持 `incremental_output` 分 token 返回<br>• Responses API：完全兼容 OpenAI `/v1/chat/completions` 响应结构 | • 强结构化响应：包含 `message.role`、`message.content`、`message.tool_calls`、`message.tool_call_id`<br>• 自动注入 `memory_store_id` 与 `session_id` 元信息<br>• Webhook 回调支持事件类型区分（`agent_started` / `tool_executed` / `session_completed`） | • 简单 JSON：仅含 `output`（字符串）、`usage`（token 统计）<br>• 不返回工具调用中间结果，仅最终回复文本<br>• 无原生流式支持（需自行轮询异步任务） |
| **支持模型** | • **不直接暴露模型**，仅调用已部署的应用实例<br>• 底层可基于 `qwen-max`/`qwen-plus`/`qwen-turbo` 等任意百炼托管模型构建应用 | • **严格限定**：仅支持 `qwen-max`、`qwen-plus`、`qwen-turbo`（Qwen 系列专属托管模型）<br>• **不支持**用户自定义模型、外部模型接入或多模型路由 | • 支持千问系列公开模型（`qwen-plus`/`qwen-max`）及**用户自定义部署模型**<br>• 不支持新版[函数调用](../concepts/function-calling.md)原生模型（如 `qwen2.5-72b-instruct` 的 tool calling 模式） |
| **API 端点** | • 应用调用：`https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`（DashScope）<br>• 组件管理：`/{workspaceId}/promptTemplates`（OpenAPI，需 AccessKey 签名） | • 全 RESTful：`https://bailian.aliyuncs.com/api/v1/agents`、`/environments`、`/sessions` 等<br>• **统一鉴权**：所有接口均使用 `Authorization: Bearer <api_key>` | • 仅通过旧版控制台生成应用后获得调用地址（无独立 API 文档端点）<br>• 实际调用仍走 DashScope 应用网关（同 Flow Agent 应用调用路径），但参数结构受限 |
| **计费方式** | • **按模型调用计费**：以输入/输出 token 为单位（知识库检索文本计入输入 token）<br>• Prompt 模板、Memory（旧）等组件操作**不单独计费**<br>• 插件调用按 MCP 类型单独计费 | • **按 Agent 实例+会话时长+Token 三重计费**：<br>  - Agent 实例固定月费（含基础 vCPU/RAM）<br>  - Session 持有时间（分钟级）<br>  - 模型推理 Token（输入/输出）<br>• Memory Store、Skill、Vault 等托管资源**包含在实例费用内** | • **纯 Token 计费**：输入（含知识库文本、历史对话、[长期记忆](../concepts/long-term-memory.md)内容）+ 输出 token<br>• 插件调用按次计费（MCP 类型）<br>• **[长期记忆](../concepts/long-term-memory.md)内容本身不计费**（但占用上下文窗口，间接影响 token 成本） |
| **状态与记忆管理** | • `session_id`：云端会话标识，1 小时无请求自动失效<br>• `messages` 数组：显式传递多轮上下文（替代 session_id）<br>• **[长期记忆](../concepts/long-term-memory.md)（旧）组件已标记为遗留**，推荐使用新版智能体内置机制 | • **强状态绑定**：`session_id` → `environment_id` → `memory_store_id` 三级关联<br>• Memory Store 默认 TTL=7 天（不可配置）<br>• 支持跨会话共享 Memory Store（需显式指定） | • 依赖 `session_id` + `携带的上下文轮数` 模拟状态<br>• “长期记忆”为 Prompt 注入文本，无独立存储实体<br>• 记忆内容随每次请求合并入 Prompt，无持久化能力 |
| **工具/插件能力** | • 支持工作流节点调用工具（如 RAG 检索、HTTP 请求）<br>• 工具调用日志需通过 DashScope SDK 解析 | • **原生 MCP 协议支持**：`tool_calls` 字段直出，支持复杂参数校验与错误重试<br>• Skill 封装标准 Webhook 或内部服务，支持并发调用与超时控制（默认 30s） | • 插件调用为黑盒流程，超时强制设为 **5 秒**，超时即失败<br>• 无中间状态反馈，仅返回最终结果或错误 |
| **典型场景** | • 对接已有智能体/工作流应用的业务系统（如客服后台调用知识问答 Agent）<br>• 需复用 OpenAI 生态代码（通过 Responses API）<br>• 需精细管理 Prompt 模板与历史记忆片段（组件类接口） | • 构建需长期会话、多步骤协作、环境隔离的生产级 Agent（如企业级 IT 助手、合规审批机器人）<br>• 要求开箱即用的状态管理、安全凭证（Vault）、文件处理（File）能力<br>• 需要完整执行链路可观测性（Webhook + Debug 日志） | • 快速上线垂直领域轻量应用（如内部 FAQ 机器人、销售话术生成器）<br>• 无开发资源，依赖业务人员通过控制台配置<br>• 需复用大量历史 Prompt 模板与样例数据（支持自动优化） |

## 各方案的适用场景建议

- **选择流程型智能体（Flow Agent）当**：  
  ✅ 你已拥有在百炼控制台发布好的智能体或工作流应用，只需将其集成到现有业务系统；  
  ✅ 你的团队熟悉 OpenAI API 生态，希望最小改造迁移现有代码；  
  ✅ 你需要对 Prompt 模板进行集中化、版本化管理，并支持变量插值；  
  ❌ 不适合需要自定义模型、强会话状态持久化或复杂工具编排的场景。

- **选择托管智能体（Managed Agents）当**：  
  ✅ 你正在构建企业级、高可靠性的 AI 应用，要求环境隔离、会话状态强一致性、内置安全凭证管理；  
  ✅ 你需要原生支持 MCP 协议的工具调用，且对调用超时、重试、错误分类有明确要求；  
  ✅ 你接受统一的托管资源模型（固定规格实例 + Session 时长计费），并愿意为运维简化支付溢价；  
  ❌ 不适合预算敏感型项目、需灵活切换底层模型、或仅需简单问答功能的场景。

- **选择传统智能体（Agent Legacy）当**：  
  ✅ 你追求极致交付速度，业务方可在控制台 10 分钟内完成一个知识库问答机器人；  
  ✅ 你有大量历史 Prompt 样例数据，需利用平台自动优化能力提升效果；  
  ✅ 你依赖特定旧版特性（如某款插件的兼容性、历史版本回滚机制）；  
  ❌ **强烈不建议新项目选用**：该体系已归档，不再接收功能更新，长期维护风险高；华北2（北京）地域强绑定，扩展性差。

## 面向开发者的选型参考

| 你的核心诉求 | 推荐方案 | 关键理由 |
|--------------|----------|----------|
| **“已有应用，快速集成”** | 流程型智能体 | DashScope API 与 Responses API 提供最平滑的对接路径，无需重构应用逻辑；组件接口满足模板与记忆管理需求。 |
| **“从零构建，追求生产就绪”** | 托管智能体 | 内置 Environment/Sessions/Memory Store/Secret Vault 等企业级能力，避免自研状态管理与安全模块；Webhook 提供完整可观测性。 |
| **“零代码验证，业务主导”** | 传统智能体（仅限存量/过渡） | 控制台拖拽式配置、Prompt 自动优化、一键发布，大幅降低技术门槛；但务必规划向 Flow Agent 或 Managed Agents 的迁移路径。 |
| **“需自定义模型或混合模型路由”** | 流程型智能体（通过自定义应用） | Flow Agent 允许将任意百炼托管模型（包括用户部署模型）封装为应用，再通过统一 API 调用；Managed Agents 与 Agent Legacy 均不支持。 |
| **“严格成本敏感，按 token 精确计量”** | 流程型智能体 或 传统智能体 | 二者均采用纯 Token 计费模式，无固定资源租用成本；Managed Agents 的实例月费在低频场景下性价比偏低。 |
| **“需长期（>7天）记忆与自定义 TTL”** | 流程型智能体（结合外部数据库） 或 自研方案 | Managed Agents Memory Store TTL 不可调；传统智能体无真正长期记忆；Flow Agent 可通过组件接口管理记忆片段，并同步至自有数据库。 |

> **重要提醒**：  
> - **地域一致性**：Flow Agent（应用调用类）与传统智能体均**仅支持华北2（北京）地域**，跨地域调用必然失败。托管智能体虽未明文限制，但控制台与文档均默认指向北京，生产环境请务必确认地域可用性。  
> - **认证分离**：Flow Agent 的应用调用（Bearer）与组件管理（AccessKey）使用两套认证体系，集成时需分别处理；托管智能体与传统智能体均统一使用 Bearer Token。  
> - **演进路线**：百炼平台明确以 **Managed Agents 为未来主干**，Flow Agent 作为兼容与扩展层持续存在，传统智能体进入维护期。新项目应优先评估 Managed Agents，次选 Flow Agent；传统智能体仅用于历史系统兼容或超短期 PoC。

## 被对比主题页

- [flow agent api](../api/flow-agent-api.md)
- [managed agents api](../api/managed-agents-api.md)
- [agent legacy](../guides/agent-legacy.md)


