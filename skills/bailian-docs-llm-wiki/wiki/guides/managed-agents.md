# managed agents

Managed Agents 是百炼提供的智能体托管运行时，适用于多步工具调用、代码执行、文件处理等长时运行任务。平台统一托管会话状态、沙箱环境和工具执行生命周期，智能体在独立云端容器中自主执行命令、读写文件、安装依赖并处理数据，所有事件历史在服务端持久化。与无状态的智能体应用相比，Managed Agents 更适合需要跨轮次保持上下文、文件系统状态和中断续接能力的复杂任务。

## 支持的模型与功能

- **模型支持**：支持百炼全系列大模型（如 `qwen3-max`、`qwen3.8-plus` 等），模型通过 `model.id` 字段指定，变更即生成新版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **核心工具集**：提供 9 个内置工具，覆盖命令执行（`bash`）、文件操作（`read`/`write`/`edit`/`glob`/`grep`）、网络访问（`web_search`/`web_fetch`）及产出物标记（`mark_artifacts`）。其中 `web_search` 按 0.03 元/次计费，`web_fetch` 当前限时免费 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **扩展能力**：
  - **MCP 服务**：通过标准 Model Context Protocol 接入官方市场或自定义 MCP 服务（如联网搜索、文档处理），挂载后默认启用其全部工具 [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
  - **Skill（技能）**：以 ZIP 包形式上传，包含 `SKILL.md`（声明触发条件与执行逻辑），支持版本管理与多智能体复用 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：通过 `coordinator` 编队配置，协调者智能体可编排自身（`self`）与最多 19 个成员智能体（`agent`）协同工作 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
- **上下文资源**：支持挂载独立管理的资源，包括：
  - **文件**：单个 ≤50 MB，挂载后在沙箱内为只读副本，路径前缀为 `/mnt/session/uploads/` [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。
  - **[记忆](../concepts/memory.md)库（Memory Store）**：跨会话持久化的文件树，挂载后智能体可通过文件工具读写，内容实时同步；支持版本历史与只读/读写权限控制 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

> **注意**：文档 23 明确记录 `web_search` 和 `web_fetch` 于 2026-09-18 新增，但文档 7 中已将其列为内置工具列表并说明计费规则。该信息一致，无需修正；但需注意 `web_fetch` 的“限时免费”状态可能随时间变化，实际计费请以控制台最新说明为准。

## 关键参数

- **智能体（Agent）参数**：
  - `name`（必填）：工作空间内唯一标识。
  - `model.id`（必填）：指定模型 ID，变更即生成新版本。
  - `system`（可选）：系统提示词，定义角色与行为约束。
  - `tools`：以 `builtin_toolkit` 形式声明，支持 `default_config.permission_policy`（`always_allow`/`always_ask`）控制审批策略；单个工具可在 `configs[]` 中覆盖 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
  - `mcp_servers`：数组，每个元素含 `type`（`official`/`custom`）和 `name`。
  - `skills`：数组，每个元素含 `type`（`customer`）、`skill_id` 和 `version`。
  - `multiagent`：对象，`type="coordinator"`，`agents` 数组含 `type`（`self`/`agent`）、`id`（`agent` 类型必填）和 `version`（`agent` 类型可选）。

- **运行环境（Environment）参数**：
  - `config.type`：固定为 `"cloud"`（云端托管）。
  - `config.packages`：按包管理器声明预装依赖，如 `"apt": ["ffmpeg"]`, `"pip": ["pandas"]`。
  - `config.networking.type`：`"unrestricted"`（放行全部出站）。

- **会话（Session）参数**：
  - `agent`（必填）：智能体 ID，创建时快照其当前版本。
  - `environment_id`（必填）：运行环境 ID。
  - `resources`：数组，支持 `type="file"`（含 `file_id`, `mount_path`）和 `type="memory_store"`（含 `memory_store_id`, `access`, `instructions`）。
  - `initial_events`（定时任务专用）：触发时自动发送的初始消息事件。

## 使用方式

1. **创建智能体**：通过控制台向导或 API 配置模型、系统提示词、工具（含审批策略）、MCP、Skill 和多智能体编队 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。
2. **创建运行环境**：配置云端沙箱，声明预装包（`apt`/`pip`/`npm`）和网络策略 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)。
3. **发起会话**：
   - 控制台：在智能体详情页点击“新建会话”，绑定环境并挂载文件/[记忆](../concepts/memory.md)库。
   - API：`POST /sessions`，传入 `agent`、`environment_id` 和 `resources` [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。
4. **交互与控制**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，`type="message"`。
   - 处理审批：收到 `tool_approval_request` 事件后，`POST /sessions/{session_id}/events` 发送 `type="tool_approval_response"`（`allow`/`deny`）。
   - 中断执行：`POST /sessions/{session_id}/events` 发送 `type="interrupt"`。
   - 订阅事件流：`GET /sessions/{session_id}/events/stream`（SSE），监听 `message`、`tool_call_output`、`session_status` 等事件 [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。
5. **定时任务（Deployment）**：绑定智能体与环境，配置 Cron 表达式或手动触发，每次触发创建一个新会话并发送 `initial_events` [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)。
6. **CLI 管理**：使用 `bl managed-agent` 命令集进行基础设施即代码（IaC）式管理，支持 `init`/`apply`/`playground` 等全生命周期操作 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **资源配额**：
  - 文件：单个 ≤50 MB，工作空间总容量 ≤100 GB，保存时效 30 天 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。
  - [记忆](../concepts/memory.md)库：单个记忆文件 ≤102400 UTF-8 bytes，单会话最多挂载 8 个 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。
  - 技能包：ZIP 文件 ≤10 MB [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。

- **生命周期管理**：
  - 智能体与环境支持**归档**（保留历史，不可新建会话/绑定），不支持删除；技能与文件支持**硬删除**（不可恢复）。
  - 会话支持**归档**（状态变 `terminated`，事件历史保留）和**删除**（元数据、事件、资源副本全部清除）[发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。

- **安全与隔离**：
  - 密钥库（Vault）通过占位符 `${VAR}` + 网关替换机制注入密钥，仅对匹配域名的 Authorization 请求头生效，真实密钥不出现在容器内 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。
  - 文件挂载为会话内副本，修改不影响原始文件；记忆库挂载为直接读写，内容跨会话共享 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)。
  - `bash` 等高风险工具建议设为 `always_ask` 审批策略，且审批仅对主智能体生效，子智能体不支持 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

- **计费**：费用由三部分独立构成——会话运行时费（0.5 元/小时）、模型调用费（按 token 计）、工具/MCP 调用费（如 `web_search` 0.03 元/次）[计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


