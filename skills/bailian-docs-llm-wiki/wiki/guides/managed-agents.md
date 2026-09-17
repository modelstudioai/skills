# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，面向多步工具调用、代码执行、文件处理等长时运行任务。平台统一托管会话状态、[沙箱环境](../concepts/sandbox.md)与工具执行生命周期，智能体在独立云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件历史实现可中断、可续接的有状态交互。开发者只需专注 Agent 逻辑设计，无需自行编排代理循环、沙箱或工具执行基础设施。

## 支持的模型与功能

- **模型支持**：支持 Qwen 系列大模型（如 `qwen3-max`、`qwen3.7-plus`、`qwen3.8-max`），模型通过 `model.id` 字段指定，变更即生成新版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **核心能力组件**：
  - **内置工具**：7 个开箱即用工具，覆盖 `bash`（命令执行）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`download_file`（URL 下载）[Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
  - **MCP 服务**：通过 Model Context Protocol 接入官方市场（如 `web_search`）或自定义 MCP 服务（插件、AI 网关、OpenAPI 等）[Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
  - **Skills**：以 ZIP 包形式上传的端到端任务封装，需包含 `SKILL.md`（含 `name` 和 `description`），挂载时必须指定版本号 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：支持 `coordinator` 编队，协调者可引用自身（`self`）及最多 20 个成员智能体（`agent` 类型），编队配置不可变 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。

> **注意**：文档 1 中 Python 示例使用 `qwen3.8-max`，而文档 5 的 API 示例和文档 9 的多智能体示例均使用 `qwen3-max`；当前平台实际支持的模型 ID 以控制台下拉列表或 [模型服务目录](https://help.aliyun.com/zh/model-studio/model-service-catalog) 为准，`qwen3.8-max` 尚未在所有区域开放，建议优先选用 `qwen3-max` 或 `qwen3.7-plus`。

## 关键参数

| 参数 | 说明 | 可变更性 | 备注 |
|------|------|----------|------|
| `name` | 智能体/环境/会话唯一标识符（工作空间内） | 智能体/环境：是；会话：否 | 必填，长度限制见各文档 |
| `model.id` | 指定基础大模型 | 是（触发新版本） | 仅支持百炼已开通的模型 ID |
| `system_prompt` | 定义角色、行为与约束 | 是（触发新版本） | 影响工具调用决策质量 |
| `tools` | 内置工具启用状态与审批策略 | 是（触发新版本） | `permission_policy.type` 必须为对象 `{"type": "always_allow"}` 或 `{"type": "always_ask"}`，传字符串将报错 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md) |
| `mcp_servers` | 挂载的 MCP 服务列表 | 是（触发新版本） | 在 `tools` 字段中配置审批策略，**不在** `mcp_servers` 中设置 |
| `skills` | 挂载的 Skill ID 与版本 | 是（触发新版本） | 版本锁定，后续上传新版本不影响已挂载的智能体 |
| `multiagent` | 协作编队配置 | 是（触发新版本） | `agents` 为空数组表示清空编队，回退为单智能体 |
| `environment_id` | 会话绑定的[沙箱环境](../concepts/sandbox.md) | 会话创建时固定，不可变更 | 创建会话时快照智能体配置，后续编辑不影响已有会话 |

## 使用方式

1. **创建智能体**：通过控制台向导或 API 指定 `name`、`model.id`、`system_prompt` 和 `tools`。工具审批策略需在 `tools` 字段的 `default_config` 或 `configs[]` 中显式声明 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。
2. **创建运行环境**：配置 `cloud` 类型沙箱，声明 `apt`/`pip`/`npm` 预装包及 `networking.type: unrestricted`（出站放行）[云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
3. **发起会话**：调用 `POST /sessions` 绑定 `agent` 和 `environment_id`，可选挂载 `resources`（如文件）和 `vault_id`（密钥库）[发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。
4. **驱动交互**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，`type=message`
   - 订阅实时事件：`GET /sessions/{session_id}/events/stream`（SSE）
   - 处理审批：收到 `tool_approval_request` 后，用相同 `batch_id` + `call_id` 发送 `type=tool_approval_response` [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
5. **CLI 管理（中国站专属）**：使用 `bl managed-agent apply` 声明式部署，`bl managed-agent session run --prompt "..."` 快速调试 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **资源配额**：单个文件 ≤ 10 MB，工作空间总文件容量 ≤ 100 GB，文件保存时效 30 天 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。
- **审批机制限制**：工具审批仅对主智能体生效，子智能体不支持；`function`/`custom` 等客户端工具不参与该审批流 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **状态机关键规则**：会话处于 `idle` 且 `stop_reason=requires_action` 时，**禁止发送普通 `message`**，否则返回 `pending_tool_approval_unresolved` 错误；此时仅允许 `tool_approval_response` 或 `interrupt` [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **计费要点**：会话运行中（`running` 或 `idle` 但未终止）即产生运行时费（0.5 元/小时），空闲不计费；模型 token 费与工具/MCP 调用费单独计算 [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。
- **Webhook 注意事项**：Signing Secret 仅创建/重置时返回一次，遗失需重置；事件投递为“至少一次”，客户端必须按 `event.id` 幂等去重 [Webhook 事件订阅](../../raw/application-user-guide/managed-agents/managed-agents-webhook.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [Webhook 事件订阅](../../raw/application-user-guide/managed-agents/managed-agents-webhook.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


