# agent development

Managed Agents 是阿里云百炼提供的智能体托管运行时，适用于多步工具调用、代码执行、文件处理等长时运行任务。平台托管会话状态、沙箱环境和工具执行，智能体在独立沙箱中自主执行命令、读写文件、安装依赖并处理数据，事件历史在服务端持久化。与无状态的智能体应用不同，Managed Agents 专为有状态、长周期、需环境隔离的任务设计。

## 支持的模型/功能

- **核心模型支持**：当前支持 `qwen3.8-max`、`qwen3.7-plus`、`qwen3.7-max` 等 Qwen 系列模型（见 [概述](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-introduction.md)）。`performance` 模型明确不支持多模态输入 [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)。
- **内置能力**：命令执行（`bash`）、文件操作（`read`/`write`/`edit`/`glob`/`grep`）、联网搜索（`web_search`/`web_fetch`）、待办管理（`todo_write`）、产出物标记（`mark_artifacts`）等 [Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **扩展能力**：
  - **MCP 服务**：接入官方市场或自定义 MCP 服务（如 `WebSearch`），支持插件、脚本部署、AI 网关等多种接入方式 [Agent MCP](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
  - **Skills**：上传 ZIP 包封装端到端流程，通过 `SKILL.md` 定义触发条件与执行指令 [Agent Skills](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：通过 `coordinator` 编队协调多个成员 Agent，支持混用不同模型实现成本分层 [进阶：联网研究与模型成本分层](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices/managed-agents-cost-tiering.md)。
- **沙箱环境**：除 Managed Agents 自带的云端沙箱外，还可独立使用 Sandbox 服务，提供代码解释器、浏览器、全能型三种基础镜像，兼容 E2B SDK [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)。

> **注意**：文档 46 和 47 提到的“高代码应用”属于另一套技术栈（基于 Serverless/K8s 部署 Python 后端），其 MCP 工具接入逻辑需在用户代码中手动实现，与 Managed Agents 的声明式工具挂载机制不同，二者不可混用。

## 关键参数

- **Agent 创建参数**：`name`（必填）、`model.id`（必填）、`system`（系统提示词）、`tools`（必须在 `configs[]` 中显式启用每个工具，仅设 `default_config.enabled: true` 无效）[入门：搭一个数据分析 Agent](../../raw/_short/managed-agents-data-analysis-2249e7a887786f0b.md)。
- **Environment 参数**：`config.type: "cloud"`（固定）、`config.packages`（按 `apt`/`pip`/`npm` 声明预装包）、`config.networking.type: "unrestricted"`（出站放行）[云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **Session 创建参数**：`agent`（可传 `id` 或覆盖配置）、`environment_id`（必选）、`resources`（挂载文件或记忆库）、`mcp_configs`（为 MCP 请求注入 Header）[发起会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md)。
- **审批策略参数**：在 `tools.configs[]` 中为单个工具设置 `permission_policy.type`（`always_allow` / `always_ask`）[Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 使用方式

1. **快速启动**：通过控制台「Managed Agents > 快速开始」向导，4 步完成 Agent 创建、环境配置、会话发起与调试 [快速开始](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-quick-start.md)。
2. **基础设施即代码（IaC）**：使用阿里云百炼 CLI (`bl managed-agent`) 管理全生命周期，支持 `init` 生成模板、`plan` 预览变更、`apply` 一键部署 [使用 CLI](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)。
3. **API 集成**：
   - 创建 Agent/Environment/Session 均需 `POST` 对应资源端点，携带 `Authorization: Bearer $DASHSCOPE_API_KEY`。
   - 会话交互采用 SSE 事件流：先建立 `/sessions/{id}/events/stream` 连接，再 `POST /sessions/{id}/events` 发送 `message` 或 `tool_approval_response` [会话事件流（SSE）](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)。
4. **生产化部署**：
   - **定时任务**：通过 Deployment 资源配置 Cron 表达式，自动触发会话 [定时任务](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-deployment.md)。
   - **事件通知**：配置 Webhook 订阅 `session.status_terminated` 等事件，实现任务完成后的主动回调 [Webhook 通知](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-webhook.md)。
   - **密钥安全**：通过 Vault 密钥库注入凭证，以 `${VAR_NAME}` 占位符形式在工具代码中引用，由网关按域名白名单动态替换 [密钥库认证](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-credential.md)。

## 限制和注意事项

- **配额限制**：单个文件 ≤ 50 MB；工作空间总文件容量 ≤ 100 GB；记忆库单文件 ≤ 102400 UTF-8 bytes；单会话最多挂载 8 个记忆库 [文件上传与挂载](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)。
- **环境预热**：配置了预装包的 Environment 创建后需等待预热完成，期间无法创建会话 [云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **会话状态机**：客户端必须依据 `stop_reason` 字段（而非仅 `idle` 状态）判断交互能力：`requires_action` 时禁止发送普通消息，只能提交审批或中断 [管理会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **版本锁定**：会话创建时快照 Agent 当前版本，后续修改 Agent 不影响已存在会话；若需更新，必须新建会话 [概述](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-introduction.md)。
- **多模态输入**：图片必须通过 `file_id` 方式上传并审核为 `available` 状态后，才能在 `content` 数组中以 `type: "image"` 发送；`base64` 方式不支持 [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)。

## 来源文档

- [Managed Agent](../../raw/application-user-guide/agent-development/managed-agents.md)
- [开始使用](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using.md)
- [概述](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-start-using/managed-agents-cli.md)
- [Agent 工具配置](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [构建 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent Skills](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [Agent MCP](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [多智能体协作](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [配置 Agent 环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-credential.md)
- [定时任务](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [文件上传与挂载](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-file.md)
- [Agent 上下文管理](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context.md)
- [Webhook 通知](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [记忆库](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [最佳实践](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices.md)
- [计费说明](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-billing.md)
- [进阶：提示词版本管理与回滚](../../raw/_short/managed-agents-prompt-versioning-b2a756840e400199.md)
- [进阶：生产化定时晨报机器人](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices/managed-agents-production.md)
- [入门：搭一个数据分析 Agent](../../raw/_short/managed-agents-data-analysis-2249e7a887786f0b.md)
- [进阶：联网研究与模型成本分层](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-best-practices/managed-agents-cost-tiering.md)
- [进阶：多智能体定制复杂提案](../../raw/_short/managed-agents-multiagent-proposal-c42cf9fd6aca491d.md)
- [进阶：Webhook 事件通知](../../raw/_short/managed-agents-webhook-notifications-508b7232092b6608.md)
- [进阶：自定义 MCP 与 Skills](../../raw/_short/managed-agents-custom-mcp-skills-bb2b03130058d257.md)
- [进阶：跨会话工作记忆交接](../../raw/_short/managed-agents-memory-handoff-090f3657c5cd11c0.md)
- [进阶：多模态输入与图片问答](../../raw/_short/managed-agents-multimodal-image-f8a5567fd5beea47.md)
- [进阶：构建对话客户端](../../raw/_short/managed-agents-client-streaming-8369920f0c45ea8c.md)
- [Sandbox](../../raw/application-user-guide/agent-development/sandbox.md)
- [开始使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using.md)
- [概述](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-development/sandbox/sandbox-start-using/sandbox-quick-start.md)
- [模版管理](../../raw/application-user-guide/agent-development/sandbox/sandbox-templates.md)
- [实例管理与使用](../../raw/application-user-guide/agent-development/sandbox/sandbox-sdk.md)
- [使用 Code Interpreter Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-code-interpreter.md)
- [使用 Browser Use Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-browser-use.md)
- [使用 AIO Sandbox](../../raw/application-user-guide/agent-development/sandbox/sandbox-best-practice-aio.md)
- [计费说明](../../raw/application-user-guide/agent-development/sandbox/sandbox-billing.md)
- [高代码应用](../../raw/application-user-guide/agent-development/sandbox/rich-code-application.md)
- [工具接入](../../raw/application-user-guide/agent-development/sandbox/rich-code-application/rich-code-application-mcp.md)
- [更新日志](../../raw/application-user-guide/agent-development/managed-agents/managed-agents-changelog.md)
- [API 开发指南](../../raw/application-user-guide/agent-development/sandbox/rich-code-application/rich-code-app-develop-guide.md)
- [进阶：密钥库安全注入与出网网关](../../raw/_short/managed-agents-credential-security-b5df5e4f8be278e5.md)
- [更新日志](../../raw/application-user-guide/agent-development/sandbox/sandbox-changelog.md)


