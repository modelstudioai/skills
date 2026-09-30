# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，面向多步工具调用、代码执行、文件处理等长时运行任务。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在独立云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件流反馈全过程。所有交互以结构化事件（SSE）形式实时推送，支持中断、审批与跨会话状态复用。

## 支持的模型与功能

- **模型支持**：当前支持 `qwen3-max`、`qwen3.7-plus`、`qwen3.8-max` 等 Qwen 系列大模型（见[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)），模型选择在创建 Agent 时指定，变更即生成新版本。
- **核心能力**：
  - **内置工具**：共 9 个开箱即用工具，包括 `bash`（shell 命令）、`read`/`write`/`edit`/`glob`/`grep`（文件操作）、`web_search` 与 `web_fetch`（联网检索）、`mark_artifacts`（产出物标记）[Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
  - **MCP 集成**：通过 Model Context Protocol 接入官方市场（如 `web_search`）或自定义 MCP 服务，挂载后其工具默认启用，可按需关闭 [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
  - **Skills 封装**：支持上传 ZIP 包形式的技能（含 `SKILL.md` front matter），封装端到端流程；挂载时必须指定版本号，版本更新不影响已绑定 Agent [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：支持 `coordinator` 编队，协调者可引用自身（`self`）及最多 19 个成员 Agent，编排协同任务 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
  - **上下文扩展**：支持挂载独立管理的资源，包括文件（≤50 MB/个，30 天有效期）和记忆库（跨会话持久化文件树，单文件 ≤102400 UTF-8 bytes）[Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)。

> **注意**：文档 1 中示例代码使用 `qwen3.8-max`，而文档 6 的 API 示例使用 `qwen3-max`，文档 23 更新日志未明确列出 `qwen3.8-max` 是否为正式支持型号。实际开发请以控制台下拉列表或 [API 模型列表](../../raw/application-api-reference/managed-agents-api/managed-agents-api-overview.md) 为准，避免硬编码未验证型号。

## 关键参数

| 参数 | 说明 | 可变性 | 示例值 |
|------|------|--------|--------|
| `model.id` | 必填，指定基础大模型 ID | 创建后变更即生成新版本 | `"qwen3-max"` |
| `system_prompt` | 定义角色、行为与约束的系统提示词 | 变更即生成新版本 | `"你是数据分析专家..."` |
| `tools` | 内置工具包配置，支持 `builtin_toolkit` 类型，含 `default_config`（全局策略）与 `configs`（单工具覆盖） | 可变 | `{"type": "builtin_toolkit", "default_config": {"permission_policy": {"type": "always_allow"}}, "configs": [{"name": "bash", "permission_policy": {"type": "always_ask"}}]}` |
| `mcp_servers` | MCP 服务列表，每个条目含 `type`（`official`/`custom`）与 `name` | 可变 | `[{"type": "official", "name": "web_search"}]` |
| `skills` | 技能列表，每个条目含 `type`（`customer`）、`skill_id` 与 `version` | 可变 | `[{"type": "customer", "skill_id": "skill_xxx", "version": "1.0"}]` |
| `multiagent` | 协作编队配置，`type="coordinator"`，`agents` 列表支持 `self` 和 `agent` 类型 | 可变 | `{"type": "coordinator", "agents": [{"type": "self"}, {"type": "agent", "id": "agent_researcher", "version": 3}]}` |

## 使用方式

1. **创建 Agent**：通过控制台向导或 API 指定名称、模型、`system_prompt` 与 `tools` 等参数。每次保存生成新 `version`，会话创建时锁定该版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
2. **配置 Environment**：创建云端沙箱，声明 `config.type="cloud"` 及预装包（`apt`/`pip`/`npm`）与网络策略（`unrestricted`）。环境可被多个会话复用 [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)。
3. **发起 Session**：绑定 Agent ID 与 Environment ID 创建会话实例。支持创建时挂载文件（`resources.type="file"`）或记忆库（`resources.type="memory_store"`），路径自动映射至 `/mnt/...` 下 [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。
4. **驱动交互**：
   - 发送 `message` 事件触发智能体处理；
   - 订阅 SSE 事件流（`GET /sessions/{id}/events/stream`）接收 `tool_call`、`tool_call_output`、`session_status` 等实时事件；
   - 对 `always_ask` 工具，在 `requires_action` 状态下通过 `tool_approval_response` 事件提交裁决（`allow`/`deny`）[会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。

## 限制和注意事项

- **会话状态机约束**：会话处于 `idle` 且 `stop_reason=requires_action` 时，仅允许发送 `tool_approval_response` 或 `interrupt`，禁止直接发送 `message`，否则返回 `pending_tool_approval_unresolved` 错误 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **资源生命周期解耦**：文件与记忆库作为独立资源管理，挂载到会话时做内部拷贝（文件）或直连（记忆库），会话内修改不影响原始资源；但记忆库内容跨会话共享，需注意并发写入风险 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。
- **密钥安全机制**：密钥库（Vault）中的密钥以占位符（如 `${MY_API_KEY}`）注入，仅当请求目标域名匹配“密钥替换生效域名”且位于 `Authorization: Bearer ...` 头时，网关才替换为真实值；其他位置（请求体、查询参数）或不匹配域名均保留占位符 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。
- **计费关键点**：会话运行时费（0.5 元/小时）按“启用状态”计费，空闲不计费；模型 token 消耗与工具调用（如 `web_search` 0.03 元/次）单独计费；免费额度仅抵扣运行时费 [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。
- **CLI 权限限制**：Managed Agent CLI 功能目前仅对中国站（aliyun.com）账号开放 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


