# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台在服务端统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件历史实现中断续接与可追溯性。其核心价值在于将代理循环、沙箱编排与工具基础设施从开发者职责中剥离，聚焦于 Agent 逻辑本身。

## 支持的模型/功能

- **模型支持**：支持百炼全系大模型（如 `qwen3-max`、`qwen3.8-plus`、`qwen3.7-plus`），模型通过 `model.id` 字段指定，变更即生成新版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **内置工具**：提供 7 个开箱即用的沙箱内工具，全部在会话绑定的运行环境中执行：
  - `bash`：执行 shell 命令（含 `apt install`、脚本运行等）
  - `read` / `write` / `edit`：文件读写与安全替换
  - `glob` / `grep`：文件查找与内容搜索
  - `download_file`：从 URL 下载文件到沙箱
- **扩展能力**：
  - **MCP 服务**：通过标准 Model Context Protocol 接入官方市场（如 web_search）或自定义 MCP 服务（插件、AI 网关、OpenAPI）[Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
  - **Skills**：以 ZIP 包形式上传预置技能，包含 `SKILL.md`（声明触发条件与能力）和执行逻辑，挂载时需指定版本号 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：通过 `coordinator` 编队配置协调者与成员智能体，支持 `self` 和 `agent` 类型条目，最多 20 个成员 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。

> **注意**：文档中对 `multiagent` 字段的 Java SDK 示例（文档 9）使用了 `RosterEntry.builder()`，但最新版 SDK 实际要求使用 `MultiAgentRosterEntry.builder()`；请以 [API 参考](../../raw/application-api-reference/managed-agents-api/agent-api.md) 中的字段定义为准，避免构建失败。

## 关键参数

| 参数 | 说明 | 示例值 | 来源 |
|------|------|--------|------|
| `agent` | 智能体 ID（必填），会话创建时快照其当前版本 | `"agent_xxx"` | [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md) |
| `environment_id` | 运行环境 ID（必填），决定沙箱类型与预装包 | `"env_xxx"` | [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md) |
| `resources` | 挂载资源列表，支持 `file` 类型，需指定 `file_id` 与 `mount_path` | `[{"type":"file","file_id":"file_xxx","mount_path":"/workspace/data.csv"}]` | [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md) |
| `tools[].permission_policy` | 工具审批策略，仅接受对象 `{"type": "always_allow"}` 或 `{"type": "always_ask"}`，**不可传字符串** | `{"name":"bash","permission_policy":{"type":"always_ask"}}` | [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md) |
| `networking.type` | 环境网络策略，`unrestricted` 表示放行全部出站访问（控制台不显示，仅 API 可设） | `{"type":"unrestricted"}` | [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md) |

## 使用方式

1. **创建智能体**：配置名称、模型、系统提示词及工具集（内置/MCP/Skills/多智能体）。每次保存生成新 `version`，会话创建时锁定该版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
2. **创建运行环境**：选择 `cloud` 托管类型，声明 `apt`/`pip`/`npm` 预装包及 `networking` 策略。环境可被多个会话复用 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
3. **发起会话**：
   - 控制台：在智能体详情页点击「新建会话」，绑定环境并上传/挂载文件；
   - API：`POST /sessions`，传入 `agent`、`environment_id` 和 `resources`；
   - CLI：`bl managed-agent session run --prompt "..."`（需先 `apply` 配置）[使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。
4. **交互与控制**：
   - 发送消息：`POST /sessions/{id}/events`，`type=message`；
   - 处理审批：收到 `tool_approval_request` 后，`POST` 同接口，`type=tool_approval_response` 并指定 `batch_id`/`call_id`/`result`；
   - 中断执行：`type=interrupt`；
   - 订阅流式事件：`GET /sessions/{id}/events/stream`（SSE）[会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。

## 限制和注意事项

- **配额限制**：
  - 单文件 ≤ 10 MB，工作空间总容量 ≤ 100 GB，文件保存时效 30 天 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)；
  - 技能 ZIP 包 ≤ 10 MB，`SKILL.md` 中 `description` ≤ 1024 字符 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)；
  - 多智能体编队最多 20 个成员 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。

- **关键注意事项**：
  - **审批策略生效时机**：修改 Agent 的工具审批策略**不会影响已存在的会话**，必须新建会话才生效 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)；
  - **路径前缀规则**：挂载文件时填写的 `mount_path`（如 `/workspace/data.csv`）会被自动加上 `/mnt/session/uploads` 前缀，智能体需使用实际路径 `/mnt/session/uploads/workspace/data.csv` 访问 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)；
  - **计费起始点**：会话处于 `running` 状态即开始计收「会话运行时费」（0.5 元/小时），`idle` 状态不计费；模型 token 与工具调用费另行计算 [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)；
  - **Webhook 验签密钥**：`signing_secret` 仅在创建或重置 Webhook 时返回一次，关闭弹窗后无法再次查看，遗失必须重置 [Webhook 事件订阅](../../raw/application-user-guide/managed-agents/managed-agents-webhook.md)。

- **状态机与交互逻辑**：
  - 判断会话是否可发送普通消息，**必须检查 `session_status` 事件中的 `stop_reason`**：仅当 `stop_reason` 为 `requires_action` 时禁止发送 `message`，其余 `idle` 状态（`null`/`end_turn`/`retries_exhausted`）均允许 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)；
  - SSE 订阅与事件发送是两个独立接口：`GET /events/stream` 用于接收，`POST /events` 用于发送；切勿对 `POST` 请求加 `Accept: text/event-stream` 头 [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。

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
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [Webhook 事件订阅](../../raw/application-user-guide/managed-agents/managed-agents-webhook.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)


