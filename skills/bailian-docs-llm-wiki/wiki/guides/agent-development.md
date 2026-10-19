# agent development

Managed Agents 是阿里云百炼提供的智能体托管运行时，适用于多步工具调用、代码执行、文件处理等长时运行任务。平台托管会话状态、沙箱环境和工具执行，智能体在独立沙箱中自主执行命令、读写文件、安装依赖并处理数据，事件历史在服务端持久化。与无状态的智能体应用不同，Managed Agents 专为有状态、可中断续接、需沙箱隔离的复杂任务设计。

## 支持的模型/功能

- **模型支持**：当前支持 `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus` 等 Qwen 系列模型；`qwen3.8-max` 已验证支持多模态图片输入，而 `performance` 档位明确不支持 [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)。
- **核心能力**：
  - 多步工具调用（内置 `bash`/`read`/`write`/`edit`/`glob`/`grep`/`web_search`/`web_fetch`/`mark_artifacts`）
  - MCP 服务接入（官方市场或自定义服务）[Agent MCP](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-mcp.md)
  - 技能（Skill）封装端到端流程，支持版本管理与复用 [Agent Skills](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-skill.md)
  - 多智能体协作（coordinator 编队）[多智能体协作](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
  - 跨会话记忆库（Memory Store），支持读写挂载与版本控制 [记忆库](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- **沙箱环境**：除 Managed Agents 自带的云端沙箱外，还提供独立的 Sandbox 服务，支持三种基础镜像：`code-interpreter-v1`（代码执行）、`browser`（浏览器操作）、`all-in-one`（全能型），兼容 E2B SDK 协议 [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

> **注意**：文档中存在模型能力描述矛盾。`qwen3.7-plus` 在[进阶：多智能体定制复杂提案](../../raw/_short/managed-agents-multiagent-proposal-c42cf9fd6aca491d.md)中被推荐用于多智能体成员，但在[进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)中仅确认 `qwen3.8-max` 和 `auto` 支持图片识别，未明确 `qwen3.7-plus` 的多模态能力。实际使用应以控制台最新支持列表为准。

## 关键参数

- **Agent 配置**：`name`（必填）、`model.id`（必填）、`system`（系统提示词）、`tools`（必须在 `configs[]` 中显式启用每个工具，仅设 `default_config.enabled: true` 会导致工具不可用）[入门：搭一个数据分析 Agent](../../raw/_short/managed-agents-data-analysis-2249e7a887786f0b.md)。
- **Environment 配置**：`config.type: "cloud"`、`config.packages`（支持 `apt`/`pip`/`npm`）、`config.networking.type: "unrestricted"`（出站放行）[云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **Session 创建**：`agent.id`（必填）、`environment_id`（必填）、`resources`（挂载文件或记忆库）、`mcp_configs`（会话级 MCP 请求头注入）[发起会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md)。
- **工具审批策略**：通过 `tools[].configs[].permission_policy.type` 设置，支持 `"always_allow"` 或 `"always_ask"`；审批仅对主智能体生效，子智能体不支持 [Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 使用方式

1. **创建资源**：
   - 通过控制台或 API 创建 Agent（含模型、提示词、工具）、Environment（沙箱配置）和可选 Skill/MCP。
   - 使用 CLI 可实现基础设施即代码管理：`bl managed-agent init` 生成模板，`bl managed-agent apply` 一键部署 [使用 CLI](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)。
2. **发起会话**：
   - 创建 Session 时绑定 Agent 和 Environment，并可挂载文件（`type: "file"`）或记忆库（`type: "memory_store"`）。
   - 向 Session 发送 `message` 事件触发执行，通过 SSE 订阅 `message`/`tool_call`/`tool_approval_request` 等事件流 [会话事件流（SSE）](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)。
3. **交互与控制**：
   - 当 `session_status` 事件中 `stop_reason = "requires_action"` 时，只能发送 `tool_approval_response` 或 `interrupt`，禁止直接发新 `message` [管理会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
   - 运行时可动态挂载/卸载文件资源，但记忆库仅支持创建时挂载。
4. **生产化集成**：
   - 定时任务（Deployment）支持 cron 触发，适合无人值守场景 [定时任务](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-deployment.md)。
   - Webhook 可订阅 Session/Agent/Deployment 等 32 种事件，实现主动通知 [Webhook 通知](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-webhook.md)。
   - 密钥库（Vault）通过占位符 `${MY_API_KEY}` 注入，网关按 `allowed_hosts` 白名单替换 Authorization 头，保障密钥安全 [密钥库认证](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-credential.md)。

## 限制和注意事项

- **配额与容量**：单个文件 ≤ 50 MB，工作空间总文件容量 ≤ 100 GB；单个记忆文件 ≤ 102400 UTF-8 bytes，单会话最多挂载 8 个记忆库；文件保存时效为 30 天 [文件上传与挂载](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)。
- **环境预热**：配置了预装包的 Environment 创建后需等待预热完成，期间无法创建 Session [云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **计费**：Managed Agents 计费分三部分——会话运行时费（0.5 元/小时）、模型调用费（按 token）、工具/MCP 调用费（如 `web_search` 0.03 元/次）；Sandbox 则按秒计费，分运行费与数据保留费 [计费说明](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-billing.md)。
- **安全约束**：沙箱容器需遵守《阿里云产品服务协议》第 6 条；密钥库凭据仅在匹配 `allowed_hosts` 的请求中由网关替换，其他请求透出占位符；沙箱公网 URL 应视为访问凭证，严禁公开分享 [云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。

## 来源文档

- [开始使用](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using.md)
- [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md)
- [概述](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)
- [快速开始](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [Agent MCP](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [多智能体协作](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [配置 Agent 环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-credential.md)
- [Webhook 通知](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [定时任务](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Agent 上下文管理](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context.md)
- [文件上传与挂载](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)
- [最佳实践](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices.md)
- [记忆库](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [计费说明](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-billing.md)
- [入门：搭一个数据分析 Agent](../../raw/_short/managed-agents-data-analysis-2249e7a887786f0b.md)
- [进阶：生产化定时晨报机器人](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices/managed-agents-production.md)
- [进阶：提示词版本管理与回滚](../../raw/_short/managed-agents-prompt-versioning-b2a756840e400199.md)
- [进阶：多智能体定制复杂提案](../../raw/_short/managed-agents-multiagent-proposal-c42cf9fd6aca491d.md)
- [进阶：联网研究与模型成本分层](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices/managed-agents-cost-tiering.md)
- [进阶：Webhook 事件通知](../../raw/_short/managed-agents-webhook-notifications-508b7232092b6608.md)
- [进阶：自定义 MCP 与 Skills](../../raw/_short/managed-agents-custom-mcp-skills-bb2b03130058d257.md)
- [进阶：密钥库安全注入与出网网关](../../raw/_short/managed-agents-credential-security-b5df5e4f8be278e5.md)
- [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)
- [进阶：跨会话工作记忆交接](../../raw/_short/managed-agents-memory-handoff-090f3657c5cd11c0.md)
- [进阶：构建对话客户端](../../raw/_short/managed-agents-client-streaming-8369920f0c45ea8c.md)
- [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)
- [更新日志](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-changelog.md)
- [开始使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using.md)
- [概述](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/agent-development/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-aio.md)
- [计费说明](../../raw/application-user-guide/agent-development/sandbox/sandbox-billing.md)
- [更新日志](../../raw/application-user-guide/agent-development/sandbox/sandbox-changelog.md)


