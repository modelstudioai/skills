# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时、有状态任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主运行命令、读写文件、安装依赖，并通过持久化的事件流反馈全过程。开发者可聚焦于 Agent 逻辑本身，无需自行构建代理循环、沙箱编排或工具调度基础设施。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash` 等 Qwen3 系列模型；`model.id` 支持智能路由模式（如 `auto`、`performance`），由平台按任务复杂度自动匹配档位 [可选模型](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **核心能力**：
  - **多步工具调用**：内置 9 个工具（`bash`、`read`、`write`、`edit`、`glob`、`grep`、`web_search`、`web_fetch`、`mark_artifacts`），全部在绑定的运行环境中执行 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)；
  - **MCP 集成**：支持挂载官方市场 MCP 服务（如 `WebSearch`）或自定义 MCP Server（HTTP 注册模式），实现标准化外部能力接入 [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)；
  - **Skills 封装**：支持上传 ZIP 格式技能包（含 `SKILL.md` front matter），封装端到端任务流程，支持版本管理与跨 Agent 复用 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)；
  - **多智能体协作**：通过 `coordinator` 编队模式，协调多个成员 Agent 并行/串行执行，各成员可配置不同模型与工具集 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)；
  - **记忆库（Memory Store）**：提供跨会话持久化的文件树存储，智能体可通过 `read`/`write` 工具直接读写，历史版本自动留存 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

> **注意**：文档 24（入门教程）明确指出，`default_config.enabled: true` 不会将工具实际注入模型；必须在 `tools.configs[]` 中**逐个显式声明并启用**所需工具（如 `{"name": "bash", "enabled": true}`），否则模型仅可见平台自动注入的 `mark_artifacts`，导致 `TOOL_NOT_FOUND` 错误。该行为在多智能体场景（文档 28）中同样适用。

## 关键参数

| 参数类别 | 字段/配置项 | 说明 | 来源依据 |
|----------|-------------|------|----------|
| **Agent 创建** | `model.id` | 必填，指定模型 ID；变更即生成新版本 | [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md) |
| | `system` | 可选，系统提示词；变更即生成新版本；建议聚焦“工作纪律”而非操作步骤 | [入门：搭一个数据分析 Agent](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-data-analysis.md) |
| | `tools` | 内置工具需通过 `builtin_toolkit` 类型配置，`configs[]` 中必须显式启用每个工具 | [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md) |
| | `multiagent` | 可选，配置 `coordinator` 类型及成员列表（`self` 或 `agent` 引用） | [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md) |
| **Environment 创建** | `config.type` | 固定为 `cloud`（云端托管）；创建后不可变更 | [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md) |
| | `config.packages` | 可选，声明预装包（`apt`/`pip`/`npm`），触发环境预热 | [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md) |
| **Session 创建** | `agent` + `environment_id` | 必填；会话创建时快照所引用 Agent 的**当前版本**（非最新版），后续 Agent 更新不影响已存在会话 | [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md) |
| | `resources` | 可选，挂载文件（`type: file`）或记忆库（`type: memory_store`）；文件路径前缀自动补 `/mnt/session/uploads/` | [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md) |
| **审批策略** | `permission_policy.type` | 工具级配置，仅接受 `{"type": "always_allow"}` 或 `{"type": "always_ask"}` 对象；字符串值将报错 | [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md) |

## 使用方式

1. **资源准备**：
   - 创建 Agent：配置模型、系统提示词、工具（含审批策略）、MCP/Skills（可选）；
   - 创建 Environment：选择云端托管，按需配置预装包（注意预热时间）；
   - （可选）创建 Memory Store、Vault、File 等上下文资源。

2. **发起会话**：
   - 调用 `POST /sessions`，传入 `agent` ID、`environment_id` 及 `resources`（如挂载文件或记忆库）；
   - 会话创建后处于 `idle` 状态（`stop_reason=null`），可发送首条用户消息。

3. **交互与控制**：
   - 发送 `message` 事件触发 Agent 处理；
   - 订阅 SSE 事件流（`GET /sessions/{id}/events/stream`）实时接收 `message`、`tool_call`、`tool_approval_request` 等事件；
   - 遇 `requires_action`（`stop_reason=requires_action`）时，仅允许发送 `tool_approval_response` 或 `interrupt`；普通消息将被拒绝 [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)；
   - 运行时可动态追加挂载文件（`POST /sessions/{id}/resources`），但记忆库仅支持创建时挂载。

4. **生产化部署**：
   - 使用 Deployment（定时任务）实现无人值守：配置 cron 表达式与 `initial_events`，每次触发创建新会话；
   - 通过 Webhook 订阅 `deployment_run.succeeded`/`failed` 等事件，替代轮询 [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)；
   - CLI 用户可使用 `bl managed-agent apply` 以 IaC 方式批量管理 Agent、Environment、Deployment 等资源 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **环境预热**：配置了预装包的 Environment 创建后需预热（数分钟），期间状态为“准备中”，无法被会话引用，否则返回 `invalid_parameter` 错误 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **会话状态机**：客户端必须依据 `stop_reason` 判断交互状态——仅 `requires_action` 禁止发送普通消息；`retries_exhausted` 等其他 `idle` 状态仍可发送新消息继续流程 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **密钥安全**：
  - Vault 密钥在沙箱内始终为占位符（`BMA_SECRET_PLACEHOLDER_*`），真实值**仅在出网网关命中 `allowed_hosts` 白名单时，替换 `Authorization` 请求头**；其他请求头（如 `X-Api-Key`）或请求体中的占位符均不替换 [密钥库安全注入与出网网关](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-credential-security.md)；
  - Deployment（定时任务）**不支持 `environment_variables`**，高敏凭证必须通过 `vault_ids` 注入 [进阶：生产化定时晨报机器人](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-production.md)。
- **计费**：费用分三部分独立计算——会话运行时费（0.5 元/小时）、模型调用费（按 token）、工具/MCP 调用费（如 `web_search` 0.03 元/次）；免费额度仅抵扣运行时费 [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。
- **配额**：单文件 ≤50 MB；单工作空间文件总容量 ≤100 GB；单记忆文件 ≤102400 UTF-8 bytes；单会话最多挂载 8 个记忆库 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)、[记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
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


