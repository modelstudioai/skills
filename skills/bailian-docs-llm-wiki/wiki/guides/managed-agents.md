# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时、有状态任务设计。平台统一托管会话状态、沙箱环境、工具执行与事件历史，开发者只需聚焦智能体逻辑配置，无需自行构建代理循环、沙箱编排或持久化基础设施。其核心价值在于将智能体从无状态函数升级为具备自主执行能力、跨轮次上下文保持和资源隔离的“工作单元”。

## 支持的模型/功能

Managed Agents 支持 Qwen3 系列模型，当前可用模型 ID 严格限定为 `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus` 和 `qwen3.6-flash`；旧版 DashScope 模型 ID（如 `qwen3-max`）将被拒绝并返回 `400 AGENT_010 模型不存在` 错误 [入门：搭一个数据分析 Agent](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-data-analysis.md)。

核心功能包括：
- **多步自主执行**：智能体在独立沙箱中按需调用工具链（命令、文件、网络、MCP、Skill），支持中断与续接；
- **状态持久化**：会话级事件流（SSE）实时推送，服务端完整持久化事件历史；
- **扩展能力体系**：内置 9 个工具（`bash`、`read`、`write`、`edit`、`glob`、`grep`、`web_search`、`web_fetch`、`mark_artifacts`）、MCP 服务（市场/自定义）、Skill（预置流程包）及多智能体协调（coordinator 编队）；
- **上下文管理**：支持文件挂载、跨会话记忆库（Memory Store）及密钥库（Vault）安全注入；
- **生产就绪能力**：定时任务（Deployment）、Webhook 事件通知、CLI 基础设施即代码管理。

> **注意**：文档中多次强调 `default_config.enabled: true` 并不会将工具实际暴露给模型；必须在 `tools.configs[]` 中**逐个显式声明**每个需启用的工具并设 `enabled: true`，否则模型仅能调用平台自动注入的 `mark_artifacts`，导致 `TOOL_NOT_FOUND` 错误 [入门：搭一个数据分析 Agent](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-data-analysis.md)。

## 关键参数

创建与配置资源时需关注以下关键参数：

- **Agent**：`name`（工作空间内唯一）、`model.id`（必须为 Qwen3 系列有效 ID）、`system`（系统提示词）、`tools`（`builtin_toolkit` 下 `configs[]` 显式启用工具）、`mcp_servers`（挂载 MCP 服务）、`skills`（挂载 Skill 版本）、`multiagent`（coordinator 编队配置）；
- **Environment**：`config.type`（固定为 `cloud`）、`config.packages`（`apt`/`pip`/`npm` 预装包列表）、`config.networking.type`（`unrestricted`）；
- **Session**：`agent`（Agent ID）、`environment_id`（环境 ID）、`resources`（挂载文件/记忆库，路径前缀为 `/mnt/session/uploads` 或 `/mnt/memory/<名称>`）、`initial_events`（Deployment 的初始消息）；
- **审批策略**：通过 `tools[].configs[].permission_policy` 设置，仅接受 `{"type": "always_allow"}` 或 `{"type": "always_ask"}` 对象，字符串值将导致参数错误 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)；
- **密钥库**：`allowed_hosts`（域名白名单，支持 `*` 和 `*.example.com`），真实密钥仅在匹配该列表的出网请求 `Authorization` 头中被替换，其余位置均为占位符 [进阶：密钥库安全注入与出网网关](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-credential-security.md)。

## 使用方式

1. **配置资源**：  
   - 创建 Agent（控制台或 API），指定模型、提示词与工具；  
   - 创建 Environment（云端托管沙箱），声明预装包与网络策略；  
   - （可选）上传文件、创建记忆库、配置密钥库、注册 MCP 服务或上传 Skill。

2. **发起会话**：  
   - 控制台：在 Agent 详情页点击「新建会话」，绑定环境并挂载资源；  
   - API：调用 `POST /sessions`，传入 `agent`、`environment_id` 及 `resources`；  
   - CLI：使用 `bl managed-agent playground` 调试，或 `bl managed-agent apply` 批量部署 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

3. **驱动交互**：  
   - 发送用户消息：`POST /sessions/{session_id}/events`，`type=message`；  
   - 订阅事件流：`GET /sessions/{session_id}/events/stream`（SSE），监听 `message`、`tool_call_output`、`session_status` 等事件；  
   - 处理审批：收到 `tool_approval_request` 后，发送 `tool_approval_response`（`allow`/`deny`）；  
   - 运行时挂载：`POST /sessions/{session_id}/resources` 动态追加文件。

4. **生产化部署**：  
   - 定时任务：创建 Deployment，配置 cron 表达式与 `initial_events`；  
   - 事件通知：创建 Webhook endpoint，订阅 `session.status_terminated`、`deployment_run.succeeded` 等具名事件 [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)。

## 限制和注意事项

- **环境预热**：配置了预装包的 Environment 创建后需数分钟预热，期间处于“准备中”状态，无法绑定会话，否则返回 `invalid_parameter` 错误 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **会话状态机**：客户端必须依据 `session_status` 事件中的 `stop_reason` 判断交互状态——仅当 `stop_reason=requires_action` 时禁止发送普通消息，须提交审批或中断；`retries_exhausted` 等其他 `idle` 状态仍允许发送新消息 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **计费项分离**：费用由三部分独立计算：会话运行时费（0.5 元/小时）、模型调用费（按 token）、工具/MCP 调用费（如 `web_search` 0.03 元/次）；免费额度仅抵扣运行时费 [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。
- **密钥安全边界**：Vault 凭证在沙箱内始终为占位符，真实密钥仅在出网网关命中 `allowed_hosts` 时注入 `Authorization` 头；`X-Api-Key` 等其他头不被替换，且非白名单域名请求仅透出占位符，不拦截网络 [进阶：密钥库安全注入与出网网关](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-credential-security.md)。
- **Deployment 限制**：定时任务（Deployment）不支持 `environment_variables`，凭证注入必须通过 `vault_ids`；若需明文环境变量，应使用应用侧主动创建 Session 的方式 [进阶：生产化定时晨报机器人](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-production.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [最佳实践](../../raw/application-user-guide/managed-agents/managed-agents-best-practices.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [入门：搭一个数据分析 Agent](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-data-analysis.md)
- [进阶：生产化定时晨报机器人](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-production.md)
- [进阶：提示词版本管理与回滚](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-prompt-versioning.md)
- [进阶：Webhook 事件通知](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-webhook-notifications.md)
- [进阶：多智能体定制复杂提案](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-multiagent-proposal.md)
- [进阶：自定义 MCP 与 Skills](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-custom-mcp-skills.md)
- [进阶：密钥库安全注入与出网网关](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-credential-security.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


