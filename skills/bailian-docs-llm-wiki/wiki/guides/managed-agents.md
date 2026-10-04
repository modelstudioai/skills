# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件历史实现可中断、可续接的交互流程。相比无状态的智能体应用，Managed Agents 更适合需要状态保持、环境隔离和复杂编排的生产级场景。

## 支持的模型与功能

- **模型支持**：支持百炼全系列大模型（如 `qwen3-max`、`qwen3.8-plus`），模型在创建智能体时指定，变更即生成新版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **内置工具**：共 9 个开箱即用工具，覆盖核心执行能力：
  - `bash`（shell 命令）、`read`/`write`/`edit`/`glob`/`grep`（文件操作）、`web_search`/`web_fetch`（联网检索）、`mark_artifacts`（产出物标记）。
  - `web_search` 与 `web_fetch` 自 2026-09-18 起上线，按次计费（`web_search` 0.03 元/次，`web_fetch` 限时免费）[Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **扩展能力**：
  - **MCP 服务**：通过 Model Context Protocol 接入官方市场或自定义 MCP 服务（如联网搜索、文档处理、图像服务）。
  - **Skill**：以 ZIP 包形式上传预置技能，封装端到端任务流程；`SKILL.md` 的 `description` 字段直接影响调用准确性 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：支持 `coordinator` 编队，协调者智能体可编排自身（`self`）及最多 20 个成员智能体（`agent`）协同工作 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
- **上下文资源**：
  - **记忆库（Memory Store）**：跨会话持久化的文件树，挂载后智能体可通过 `read`/`write` 等工具读写，历史版本自动记录 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。
  - **文件**：单文件上限 50 MB，挂载后以副本形式进入沙箱，会话内修改不影响原始文件 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。

> **注意**：文档 23 明确指出 `web_search` 和 `web_fetch` 于 2026-09-18 上线，但文档 6 中工具列表描述为“9 个内置工具”，而文档 1 和文档 2 的快速开始示例中仅列出 7 个（`bash`, `read`, `write`, `edit`, `glob`, `grep`, `mark_artifacts`）。实际可用工具应以控制台或最新 API 文档为准，`web_search`/`web_fetch` 需显式启用且单独计费。

## 关键参数

- **智能体（Agent）参数**：
  - `name`（必填）：工作空间内唯一标识。
  - `model.id`（必填）：指定模型 ID。
  - `system`（可选）：系统提示词，定义角色与行为约束。
  - `tools`：`builtin_toolkit` 下声明各工具启用状态及审批策略（`always_allow` 或 `always_ask`）；`mcp_servers` 指定 MCP 服务；`skills` 指定 Skill ID 与版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **运行环境（Environment）参数**：
  - `config.type`：固定为 `cloud`（云端托管）。
  - `config.packages`：按包管理器声明预装依赖，如 `"apt": ["ffmpeg"]`, `"pip": ["pandas"]`。
  - `config.networking.type`：`unrestricted`（放行全部出站）。
- **会话（Session）参数**：
  - `agent`（必填）：智能体 ID。
  - `environment_id`（必填）：运行环境 ID。
  - `resources`：挂载资源列表，支持 `file`（指定 `file_id` 和 `mount_path`）和 `memory_store`（指定 `memory_store_id` 和 `access` 权限）。
- **审批策略**：`permission_policy` 必须为对象形态 `{"type": "always_allow"}` 或 `{"type": "always_ask"}`，传字符串将报错 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 使用方式

1. **创建智能体**：通过控制台向导或 API（`POST /agents`）配置模型、提示词与工具集。每次保存生成新 `version`，会话创建时锁定该版本 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。
2. **配置运行环境**：创建独立的云端沙箱，声明预装包与网络策略。环境可被多个会话复用 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)。
3. **发起会话**：
   - 控制台：在智能体详情页点击“新建会话”，绑定环境并挂载资源。
   - API：`POST /sessions`，传入 `agent`、`environment_id` 及 `resources`。
   - CLI：`bl managed-agent session create` 或 `bl managed-agent playground` 进行调试 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。
4. **交互与事件流**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，`type=message`。
   - 订阅实时事件：`GET /sessions/{session_id}/events/stream`（SSE），监听 `message`、`tool_call`、`tool_approval_request` 等事件 [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。
5. **高级能力集成**：
   - **定时任务**：创建 Deployment，配置 cron 表达式与初始消息，每次触发生成一个会话 [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)。
   - **密钥库**：集中管理 API Key，通过 `${变量名}` 占位符注入，网关在匹配域名的 Authorization 头中自动替换真实值 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。
   - **Webhook**：注册回调地址，订阅 Session、Agent 等资源的状态变更事件，实现事件驱动架构 [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)。

## 限制和注意事项

- **配额限制**：
  - 文件：单个 ≤ 50 MB，工作空间总容量 ≤ 100 GB，保存时效 30 天。
  - 记忆库：单条记忆 ≤ 102400 UTF-8 bytes，单会话最多挂载 8 个。
  - 多智能体编队：最多 20 个成员。
- **生命周期管理**：
  - 智能体与环境支持**归档**（保留历史，不可新建会话/绑定），不支持删除；文件与 Skill 支持**硬删除**（不可恢复）。
  - 会话支持归档（`terminated`，事件历史保留）与删除（元数据、事件、资源全部清除）。
- **安全与合规**：
  - 云端沙箱需遵守《阿里云产品服务协议》第 6 条，禁止安装盗版软件，用户对自行操作结果负全责 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
  - 密钥库密钥仅在 Authorization 头中替换，请求体与查询参数中的占位符**不会被替换**；`*` 域名通配需手动确认风险 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。
- **计费说明**：费用由三部分独立构成——会话运行时费（0.5 元/小时）、模型调用费（按 token 计）、工具/MCP 调用费（如 `web_search` 0.03 元/次）[计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。
- **状态机关键点**：会话处于 `idle` 且 `stop_reason=requires_action` 时，**禁止发送普通 `message`**，否则返回 `pending_tool_approval_unresolved` 错误；此时只能提交 `tool_approval_response` 或发送 `interrupt` [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


