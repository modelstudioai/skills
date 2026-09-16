# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件历史实现中断续接。相比无状态的智能体应用，Managed Agents 更适合需要跨轮次保持上下文、文件系统状态和复杂执行流的场景。

## 支持的模型与功能

- **模型支持**：支持百炼全系列大模型（如 `qwen3-max`、`qwen3.8-max`、`qwen3.7-plus`），模型在创建智能体时指定，变更即生成新版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **核心能力**：
  - **内置工具**：共 7 个开箱即用工具，覆盖 shell 命令执行（`bash`）、文件读写（`read`/`write`/`edit`）、文件查找（`glob`）、文本搜索（`grep`）及 URL 下载（`download_file`）[Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
  - **MCP 服务**：通过 Model Context Protocol 接入官方市场（如联网搜索、文档处理）或自定义 MCP 服务（插件、脚本部署、AI 网关、阿里云 OpenAPI）[Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
  - **Skills**：以 ZIP 包形式上传的预置能力包，含 `SKILL.md`（YAML front matter + Markdown 指令），支持版本化挂载与复用 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：支持 `coordinator` 编队，协调一个 `self` 智能体与最多 19 个成员智能体协同完成任务 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
- **上下文扩展**：支持挂载文件资源（单文件 ≤10 MB，路径前缀统一为 `/mnt/session/uploads`），挂载后副本独立于原始文件，支持创建时或运行时动态追加 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。

> **注意**：文档 20 中提到 `POST /sessions/{session_id}/events` 已支持多模态内容块（`image`/`video`/`file`），但文档 15 的 SSE 事件类型列表未更新该能力，实际使用应以 API 文档 [发送 Event](../../raw/application-api-reference/managed-agents-api/session-api/event-post.md) 为准。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `agent` | 智能体 ID（必填），会话创建时锁定其当前版本 | `"agent_xxx"` | [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md) |
| `environment_id` | 运行环境 ID（必填），决定工具执行的沙箱配置 | `"env_xxx"` | [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) |
| `resources` | 挂载资源列表，支持 `file` 类型，需指定 `file_id` 和 `mount_path` | `[{"type":"file","file_id":"file_xxx","mount_path":"/workspace/data.csv"}]` | [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md) |
| `tools[].permission_policy` | 工具审批策略，仅接受对象 `{"type": "always_allow"}` 或 `{"type": "always_ask"}`，字符串值将导致参数错误 | `{"type": "always_ask"}` | [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md) |
| `multiagent` | 多智能体编队配置，`type` 固定为 `"coordinator"`，`agents` 列表中 `type="self"` 表示 coordinator 自身 | `{"type":"coordinator","agents":[{"type":"self"},{"type":"agent","id":"agent_researcher"}]}` | [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md) |

## 使用方式

1. **创建智能体**：配置名称、模型、系统提示词、工具（内置/MCP/Skills）、多智能体编队等。每次保存生成新版本，会话创建时锁定版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
2. **配置运行环境**：创建云端沙箱，声明预装包（`apt`/`pip`/`npm`）与网络策略（`unrestricted`）。环境可被多个会话复用 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
3. **发起会话**：
   - 控制台：在智能体详情页点击「新建会话」，绑定环境并挂载文件。
   - API：调用 `POST /sessions`，传入 `agent`、`environment_id`、`resources` 等字段 [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。
4. **驱动交互**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，`type=message`。
   - 处理审批：收到 `tool_approval_request` 后，用相同 `batch_id` + `call_id` 发送 `type=tool_approval_response`（`allow`/`deny`）。
   - 中断执行：发送 `type=interrupt` 可终止当前处理流程 [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。
5. **CLI 管理**：使用 `bl managed-agent apply` 声明式创建资源，`bl managed-agent session run --prompt "..."` 快速启动调试 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **会话状态机**：会话处于 `idle` 状态且 `stop_reason=requires_action` 时，**禁止发送普通 `message`**，必须先提交 `tool_approval_response` 或发送 `interrupt`；否则返回 `pending_tool_approval_unresolved` 错误 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **资源生命周期**：
  - 文件：单文件 ≤10 MB，工作空间总容量 ≤100 GB，保存时效 30 天，超期可能被自动清理 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。
  - 技能：上传 ZIP 包需含 `SKILL.md`（YAML front matter 必须用 `---` 包裹），`description` 字段影响调用准确率，建议包含触发条件、适用输入、操作范围与不适用场景 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
- **计费与配额**：
  - 自 2026-08-17 起商业化计费，费用分三部分：会话运行时费（0.5 元/小时）、模型调用费（按所用模型 token 计）、工具/MCP 调用费（按服务标准）[计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。
  - 赠送 10 小时运行时免费额度，仅抵扣运行时费，30 天内有效。
- **安全与合规**：云端沙箱容器需遵守《阿里云产品服务协议》第 6 条关于网络和数据安全的约定，不得安装盗版软件，用户对自行安装的软件及操作结果承担全部责任 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [Webhook 事件订阅](../../raw/application-user-guide/managed-agents/managed-agents-webhook.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)


