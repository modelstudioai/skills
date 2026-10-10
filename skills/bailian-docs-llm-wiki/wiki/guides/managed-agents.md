# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件历史实现可追溯、可中断、可续接的交互流程。

## 支持的模型与功能

Managed Agents 支持 `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.6-flash` 等 Qwen3 系列模型，同时支持智能路由模式（如 `auto`、`performance`）[原文标题](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。核心能力覆盖：

- **多模态输入**：自 2026-09-07 起，`POST /sessions/{session_id}/events` 支持 `image`、`video` 和 `file` 类型内容块，图片/视频进入模型视觉通道，文件自动物化至沙箱文件系统 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)；
- **工具生态**：内置 9 个工具（`bash`、`read`、`write`、`edit`、`glob`、`grep`、`web_search`、`web_fetch`、`mark_artifacts`），支持 MCP 服务（官方市场或自定义 HTTP/AI 网关）、Skill 技能包及多智能体协调编队 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)；
- **上下文扩展**：支持挂载独立管理的资源，包括文件（单文件 ≤50 MB）、记忆库（跨会话持久化文件树，单记忆 ≤102400 字节）和密钥库（Vault）[原文标题](../../raw/application-user-guide/managed-agents/managed-agents-context.md)。

> **注意**：文档 24 明确指出 `download_file` 工具已下线，不应再配置；而文档 31 的更新日志未提及该工具，说明其移除是既定事实，非过时信息遗漏。

## 关键参数

| 参数类别 | 字段/配置项 | 说明 |
|----------|-------------|------|
| **Agent 配置** | `model.id`, `system`, `tools`, `multiagent`, `skills`, `mcp_servers` | `tools` 必须在 `configs[]` 中逐项显式启用（`enabled: true`），仅设 `default_config.enabled: true` 会导致工具不可用 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-data-analysis.md)；`multiagent` 仅支持 `coordinator` 类型，成员数 1–20；`skills` 需指定版本号，新版本上传不影响已挂载实例。 |
| **Environment 配置** | `config.type`, `config.packages`, `config.networking` | `type` 固定为 `cloud`（不可变）；`packages` 支持 `apt`/`pip`/`npm`；`networking.type` 仅支持 `unrestricted`（控制台不显示，API 设置）。预装包环境需等待预热完成才可绑定会话 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。 |
| **Session 创建** | `agent`, `environment_id`, `resources`, `vault_ids`, `initial_events` | `resources` 支持 `file`（挂载路径前缀为 `/mnt/session/uploads`）和 `memory_store`（路径由服务端生成）；`vault_ids` 是 Deployment 唯一支持的凭证注入方式（`environment_variables` 在 Deployment 中被静默忽略）[原文标题](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-production.md)。 |

## 使用方式

1. **创建资源**：  
   - 通过控制台或 API 创建 Agent（含模型、提示词、工具）、Environment（沙箱配置）和可选 Skill/MCP；  
   - 使用 CLI 可声明式管理：`bl managed-agent init` 生成模板，`bl managed-agent apply` 一键部署 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

2. **发起会话**：  
   - 调用 `POST /sessions` 绑定 Agent 与 Environment，传入 `resources` 挂载文件或记忆库；  
   - 通过 `POST /sessions/{id}/events` 发送 `message` 事件触发执行；  
   - 订阅 `GET /sessions/{id}/events/stream` SSE 流接收 `message`、`tool_call_output`、`session_status` 等事件。

3. **生产化集成**：  
   - 定时任务：使用 Deployment（API/CLI/控制台），配置 cron 表达式与 `initial_events`；  
   - 安全凭证：高敏密钥存 Vault，会话通过 `vault_ids` 引用，出网时由网关按 `allowed_hosts` 白名单替换 `Authorization` 头；非敏感配置用 `environment_variables`；  
   - 事件通知：创建 Webhook endpoint 订阅 `session.status_terminated` 或 `deployment_run.succeeded` 等具名事件 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)。

## 限制和注意事项

- **环境预热**：配置了 `packages` 的 Environment 创建后处于“准备中”状态，此时创建会话将返回 `invalid_parameter` 错误，需等待预热完成 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **审批机制**：工具审批（`always_ask`）仅对主智能体生效，子智能体不支持；已存在会话不会继承 Agent 新增的审批策略，必须新建会话 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **计费规则**：会话运行时费（0.5 元/小时）按实际运行时长精确计算，空闲状态不计费；模型 token 消耗与工具调用（如 `web_search` 0.03 元/次）单独计费；免费额度仅抵扣运行时费，有效期 30 天 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。
- **安全边界**：Vault 密钥在沙箱内始终为占位符（`BMA_SECRET_PLACEHOLDER_*`），真实值仅在出网网关命中 `allowed_hosts` 时注入 `Authorization` 头；其他请求头（如 `X-Api-Key`）或请求体中的占位符均不被替换 [原文标题](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-credential-security.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [最佳实践](../../raw/application-user-guide/managed-agents/managed-agents-best-practices.md)
- [入门：搭一个数据分析 Agent](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-data-analysis.md)
- [进阶：生产化定时晨报机器人](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-production.md)
- [进阶：提示词版本管理与回滚](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-prompt-versioning.md)
- [进阶：多智能体定制复杂提案](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-multiagent-proposal.md)
- [进阶：自定义 MCP 与 Skills](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-custom-mcp-skills.md)
- [进阶：Webhook 事件通知](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-webhook-notifications.md)
- [进阶：密钥库安全注入与出网网关](../../raw/application-user-guide/managed-agents/managed-agents-best-practices/managed-agents-credential-security.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


