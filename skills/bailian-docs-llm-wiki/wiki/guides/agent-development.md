# agent development

Managed Agents 是阿里云百炼提供的智能体托管运行时，适用于多步工具调用、代码执行、文件处理等长时运行任务。平台托管会话状态、沙箱环境和工具执行，智能体在独立沙箱中自主执行命令、读写文件、安装依赖并处理数据，事件历史在服务端持久化。与无状态的智能体应用不同，Managed Agents 专为有状态、可中断续接、需沙箱隔离的复杂任务设计。

## 支持的模型/功能

- **模型支持**：当前支持 `qwen3.7-plus`、`qwen3.8-max`、`deepseek-v4.1-flash`、`glm-5.3` 等模型；新增智能模式路由（`auto`、`performance`、`balanced`、`economy`）[定义 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。注意：`performance` 模型不支持多模态输入，图片问答需选用 `qwen3.8-max` 或 `auto` 等明确支持的模型 [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)。
- **核心能力**：
  - 多步工具调用（内置 `bash`、`read`、`write`、`edit`、`glob`、`grep`、`web_search`、`web_fetch`、`todo_write`、`mark_artifacts`）
  - MCP 协议集成（官方市场服务与自定义 MCP Server）
  - 技能（Skill）封装端到端流程
  - 多智能体协作（coordinator 编队）
  - 跨会话记忆库（Memory Store）
  - 定时任务（Scheduled Task / Deployment）
  - Webhook 事件通知与密钥库（Vault）安全注入

> **注意**：文档 24（入门：搭一个数据分析 Agent）明确指出，`default_config.enabled: true` 不会将工具实际注入模型；必须在 `configs[]` 中逐个显式声明 `enabled: true`，否则模型仅能访问平台自动注入的 `mark_artifacts`，导致 `TOOL_NOT_FOUND` 错误。该规则同样适用于多智能体成员 [进阶：多智能体定制复杂提案](../../raw/_short/managed-agents-multiagent-proposal-c42cf9fd6aca491d.md)。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `model.id` | 必填，指定基础大模型 | `"qwen3.8-max"` | [定义 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md) |
| `system` | 可选，定义角色与行为约束 | `"你是数据分析专家..."` | [快速开始](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-quick-start.md) |
| `tools` | 工具配置，`builtin_toolkit` 下需显式启用每个工具 | `{"name": "bash", "enabled": true}` | [Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md) |
| `multiagent` | 多智能体编队配置 | `{"type": "coordinator", "agents": [...]}` | [多智能体协作](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-multiagent.md) |
| `environment_id` | 会话必填，绑定云端沙箱环境 | `"env_xxx"` | [发起会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md) |
| `resources` | 会话挂载资源（文件、记忆库） | `[{"type": "file", "file_id": "..."}]` | [文件上传与挂载](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md) |

## 使用方式

1. **创建 Agent**：通过控制台或 API 配置模型、系统提示词、工具集、MCP 服务及技能。每次更新生成新版本，会话创建时锁定快照 [定义 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
2. **配置 Environment**：创建云端沙箱，声明预装包（`apt`/`pip`/`npm`）与网络策略（`unrestricted`）。注意：配置预装包后需等待环境预热完成，否则无法创建会话 [云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
3. **发起 Session**：
   - 创建会话时绑定 Agent 和 Environment，并可挂载文件或记忆库；
   - 通过 `POST /sessions/{id}/events` 发送 `message` 事件触发执行；
   - 订阅 SSE 事件流（`/sessions/{id}/events/stream`）接收 `message`、`tool_call`、`tool_approval_request` 等实时事件 [会话事件流（SSE）](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)。
4. **CLI 管理**：使用 `bl managed-agent` 命令以基础设施即代码方式管理全生命周期（`init` → `plan` → `apply` → `destroy`），支持项目化构建与版本发布 [使用 CLI](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)。

## 限制和注意事项

- **配额限制**：
  - 单个文件最大 50 MB，工作空间总容量上限 100 GB [文件上传与挂载](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)；
  - 单个记忆文件最大 102400 UTF-8 bytes，单会话最多挂载 8 个记忆库 [记忆库](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md)；
  - Sandbox 实例最长存活 7 天（由模版生命周期配置）[概述](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-introduction.md)。

- **关键注意事项**：
  - **工具审批仅作用于主智能体**：子智能体（multiagent 成员）不支持工具审批策略 [Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)；
  - **会话级覆盖仅限 API**：通过 `agent` 对象覆盖系统提示词、工具等配置的功能，目前控制台不支持，仅 API 可用 [发起会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md)；
  - **密钥注入路径选择**：Deployment（定时任务）不支持 `environment_variables`，凭证注入必须使用 `vault_ids`；而普通会话可二者兼用，但 Vault 提供更严格的安全边界 [进阶：密钥库安全注入与出网网关](../../raw/_short/managed-agents-credential-security-b5df5e4f8be278e5.md)；
  - **图片输入必须用 `file_id`**：Base64 方式发送图片已被证实不可靠，必须先上传获取 `file_id` 并轮询至 `available` 状态后，再通过 `content` 数组中 `type: "image"` 引用 [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)。

## 来源文档

- [开始使用](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using.md)
- [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md)
- [快速开始](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent.md)
- [使用 CLI](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)
- [Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [定义 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent MCP](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [多智能体协作](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [Agent Skills](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [配置 Agent 环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [定时任务](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [密钥库认证](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-credential.md)
- [Webhook 通知](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [记忆库](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [计费说明](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-billing.md)
- [最佳实践](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices.md)
- [入门：搭一个数据分析 Agent](../../raw/_short/managed-agents-data-analysis-2249e7a887786f0b.md)
- [进阶：生产化定时晨报机器人](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices/managed-agents-production.md)
- [进阶：提示词版本管理与回滚](../../raw/_short/managed-agents-prompt-versioning-b2a756840e400199.md)
- [进阶：多智能体定制复杂提案](../../raw/_short/managed-agents-multiagent-proposal-c42cf9fd6aca491d.md)
- [进阶：联网研究与模型成本分层](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices/managed-agents-cost-tiering.md)
- [进阶：Webhook 事件通知](../../raw/_short/managed-agents-webhook-notifications-508b7232092b6608.md)
- [进阶：自定义 MCP 与 Skills](../../raw/_short/managed-agents-custom-mcp-skills-bb2b03130058d257.md)
- [进阶：密钥库安全注入与出网网关](../../raw/_short/managed-agents-credential-security-b5df5e4f8be278e5.md)
- [进阶：跨会话工作记忆交接](../../raw/_short/managed-agents-memory-handoff-090f3657c5cd11c0.md)
- [Agent 上下文管理](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context.md)
- [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)
- [文件上传与挂载](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)
- [更新日志](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-changelog.md)
- [进阶：构建对话客户端](../../raw/_short/managed-agents-client-streaming-8369920f0c45ea8c.md)
- [开始使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using.md)
- [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)
- [快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)
- [概述](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-introduction.md)
- [模版管理](../../raw/application-user-guide/agent-development/sandbox/sandbox-templates.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-code-interpreter.md)
- [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-aio.md)
- [高代码应用](../../raw/application-user-guide/agent-development/sandbox/rich-code-application.md)
- [计费说明](../../raw/application-user-guide/agent-development/sandbox/sandbox-billing.md)
- [工具接入](../../raw/application-user-guide/agent-development/sandbox/rich-code-application/rich-code-application-mcp.md)
- [更新日志](../../raw/application-user-guide/agent-development/sandbox/sandbox-changelog.md)
- [API 开发指南](../../raw/application-user-guide/agent-development/sandbox/rich-code-application/rich-code-app-develop-guide.md)


