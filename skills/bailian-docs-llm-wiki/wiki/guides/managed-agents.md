# managed agents

Managed Agents 是百炼提供的智能体托管运行时，适用于多步工具调用、代码执行、文件处理等长时运行任务。平台统一托管会话状态、沙箱环境和工具执行生命周期，智能体在独立云端容器中自主执行命令、读写文件、安装依赖并处理数据，所有事件历史在服务端持久化。与无状态的智能体应用不同，Managed Agents 天然支持中断续接、跨轮上下文保持和资源复用。

## 支持的模型与功能

- **模型支持**：支持 `qwen3-max`、`qwen3.7-plus`、`qwen3.8-max` 等 Qwen 系列大模型（见[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)）；模型选择在创建 Agent 时指定，变更将生成新版本。
- **核心能力**：
  - **内置工具**：共 9 个开箱即用工具，包括 `bash`（shell 命令）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`web_search`/`web_fetch`（联网检索）和 `mark_artifacts`（产出物标记）[Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
  - **MCP 集成**：通过 Model Context Protocol 接入官方市场或自定义 MCP 服务（如文档处理、地理可视化），挂载后其下工具默认启用，可单独开关 [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
  - **Skills 封装**：支持上传 ZIP 格式技能包（含 `SKILL.md`），封装端到端任务流程，挂载时需指定版本号 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：通过 `coordinator` 编队配置协调者与成员智能体，支持最多 20 个成员 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
  - **记忆库（Memory Store）**：跨会话持久化的文件树资源，支持版本管理与读写挂载，智能体通过文件工具访问 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

> **注意**：文档 5 列出 9 个内置工具，但文档 2 和文档 4 的示例中仅提及 7 个（`bash`/`read`/`write`/`edit`/`glob`/`grep`/`mark_artifacts`）。根据文档 23 的更新日志，`web_search` 和 `web_fetch` 是 2026-09-18 新增，因此当前完整列表为 9 个，旧示例未及时更新。

## 关键参数

- **Agent 配置**：`name`（必填，工作空间内唯一）、`model.id`（必填）、`system`（系统提示词）、`tools`（内置工具启用策略）、`mcp_servers`（MCP 服务列表）、`skills`（技能 ID 与版本）、`multiagent`（编队配置）。
- **Environment 配置**：`name`（必填）、`config.type`（固定为 `"cloud"`）、`config.packages`（预装包，支持 `apt`/`pip`/`npm`）、`config.networking.type`（`"unrestricted"` 或受限网络）。
- **Session 配置**：`agent`（Agent ID）、`environment_id`（环境 ID）、`resources`（挂载资源列表，含 `file`、`memory_store` 等类型及 `mount_path`）、`title`（会话标题）。
- **审批策略**：对 `builtin_toolkit` 或 `mcp_toolkit` 中的单个工具，可通过 `permission_policy: {"type": "always_allow" | "always_ask"}` 控制是否需人工确认 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 使用方式

1. **创建 Agent**：通过控制台向导或 API 指定模型、系统提示词和工具集。每次保存生成新 `version`，会话创建时锁定该版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
2. **配置 Environment**：创建云端沙箱，声明预装包（如 `pip: ["pandas"]`）和网络策略。环境可被多个会话复用 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)。
3. **发起 Session**：
   - 控制台：在 Agent 详情页点击「新建会话」，绑定环境并挂载文件/记忆库。
   - API：`POST /sessions` 传入 `agent`、`environment_id` 和 `resources`，服务端快照 Agent 当前配置 [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。
4. **交互与事件流**：
   - 发送消息：`POST /sessions/{session_id}/events` 提交 `message` 类型事件。
   - 订阅响应：`GET /sessions/{session_id}/events/stream` 获取 SSE 流，监听 `message`、`tool_call`、`tool_approval_request` 等事件 [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。
5. **CLI 管理**：使用 `bl managed-agent apply` 声明式部署 Agent/Environment，`bl managed-agent session run` 快速启动会话 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **资源配额**：单个文件 ≤ 50 MB，工作空间总文件容量 ≤ 100 GB，文件保存时效 30 天；单个记忆文件 ≤ 102400 UTF-8 bytes，单会话最多挂载 8 个记忆库 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)、[记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。
- **状态机约束**：会话处于 `idle` 且 `stop_reason=requires_action` 时，仅允许发送 `tool_approval_response` 或 `interrupt`，禁止直接发送普通 `message`，否则返回 `pending_tool_approval_unresolved` 错误 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **安全限制**：
  - 密钥库密钥仅在 Authorization 请求头中按域名匹配替换，请求体/查询参数中的占位符不替换 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。
  - 记忆库中禁止存储密钥、Token 等凭证，因其内容可能被模型读取并输出 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。
- **计费说明**：费用分三部分——会话运行时费（0.5 元/小时）、模型调用费（按所用模型 token 计费）、工具/MCP 调用费（如 `web_search` 0.03 元/次）[计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。
- **生命周期管理**：Agent 和 Environment 支持归档（保留历史，不可新建会话/绑定），文件和 Skill 支持删除（硬删除，不可恢复）；会话支持归档（`terminated`，保留事件历史）和删除（硬删除）[定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)、[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)、[发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


