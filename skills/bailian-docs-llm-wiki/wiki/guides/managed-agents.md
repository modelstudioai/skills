# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件流反馈全过程。与无状态的智能体应用不同，Managed Agents 天然支持中断续接、跨轮上下文保持和沙箱级资源隔离。

## 支持的模型与功能

- **模型支持**：支持 Qwen 系列大模型（如 `qwen3-max`、`qwen3.7-plus`、`qwen3.8-max`），模型在创建智能体时指定，变更将生成新版本并影响后续新建会话 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **核心能力**：
  - **内置工具**：共 9 个开箱即用工具，包括 `bash`（shell 命令）、`read`/`write`/`edit`/`glob`/`grep`（文件操作）、`web_search` 与 `web_fetch`（网络访问）、`mark_artifacts`（产出物标记）[Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
  - **MCP 服务**：通过 Model Context Protocol 接入官方市场（如联网搜索、文档处理）或自定义 MCP 服务（插件、脚本部署、AI 网关、OpenAPI）[Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
  - **Skills（技能）**：以 ZIP 包形式上传，含 `SKILL.md`（YAML front matter + Markdown 指令），支持版本管理与多智能体复用 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：支持 `coordinator` 拓扑，协调者智能体可编排自身（`self`）与其他成员智能体（`agent`）协同工作 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
  - **记忆库（Memory Store）**：跨会话持久化的文件树，挂载后智能体可通过 `read`/`write` 等工具读写，历史版本自动记录 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

> **注意**：文档 1 中 Python 示例使用 `qwen3.8-max`，而文档 5 的示例使用 `qwen3-max`；文档 22 明确 `web_search` 和 `web_fetch` 于 2026-09-18 新增，但文档 8 的工具列表已包含二者且未标注时效性——应以文档 22 的发布时间为准，确认其为当前可用功能。

## 关键参数

| 参数 | 说明 | 可变性 | 示例 |
|------|------|--------|------|
| `model.id` | 必填，指定基础大模型 ID | 创建后变更产生新版本 | `"qwen3-max"` |
| `system_prompt` | 定义角色、行为与约束，影响工具调用决策 | 变更产生新版本 | `"你是数据分析专家，使用 pandas 处理 CSV 文件。"` |
| `tools` | 内置工具包配置，支持 `builtin_toolkit` 和 `mcp_toolkit` 类型 | 可动态更新，影响后续会话 | 含 `configs[]` 控制单个工具启用状态与 `permission_policy`（`always_allow` / `always_ask`） |
| `mcp_servers` | 挂载 MCP 服务列表，`type` 为 `official` 或 `custom` | 可动态更新 | `[{"type": "official", "name": "web_search"}]` |
| `skills` | 技能引用列表，需指定 `skill_id` 与 `version` | 可动态更新 | `[{"type": "customer", "skill_id": "skill_xxx", "version": "1.0"}]` |
| `multiagent` | 编队配置，`type="coordinator"`，`agents` 列表支持 `self` 与 `agent` 类型 | 可动态更新 | `{"type": "coordinator", "agents": [{"type": "self"}, {"type": "agent", "id": "agent_researcher"}]}` |

## 使用方式

1. **创建智能体**：通过控制台或 API 配置模型、系统提示词、工具、MCP、Skills 和多智能体编队。每次保存生成新 `version`，会话创建时锁定该版本 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。
2. **配置运行环境**：创建云端沙箱（`type: "cloud"`），声明预装包（`apt`/`pip`/`npm`）与网络策略（如 `"unrestricted"`）。环境独立于智能体，可被多个会话复用 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
3. **发起会话**：绑定智能体（ID）与环境（ID），可选挂载文件（`resources.type=file`）或记忆库（`resources.type=memory_store`）。会话启动后，服务端快照智能体配置 [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。
4. **交互与事件处理**：
   - 发送用户消息：`POST /sessions/{session_id}/events`，`type=message`。
   - 订阅实时事件：`GET /sessions/{session_id}/events/stream`（SSE），监听 `message`、`tool_call`、`tool_approval_request` 等类型 [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。
   - 处理审批：收到 `tool_approval_request` 后，发送 `tool_approval_response`（`allow`/`deny`）；若仅发 `interrupt`，服务端将为未执行调用补发 `deny` [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
5. **CLI 管理**：使用 `bl managed-agent` 命令以 IaC 方式管理资源，如 `bl managed-agent apply` 应用配置、`bl managed-agent session run --prompt "..."` 启动会话 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **配额限制**：
  - 单个文件 ≤ 10 MB，工作空间总容量 ≤ 100 GB，文件保存时效 30 天 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。
  - 单个记忆文件 ≤ 102400 UTF-8 bytes，单会话最多挂载 8 个记忆库 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。
- **生命周期管理**：
  - 智能体与环境支持**归档**（保留历史，不可用于新会话），不支持删除；技能与文件支持**硬删除**（不可恢复）[定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)、[云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
  - 会话支持归档（`terminated`，事件历史保留）与删除（元数据、事件、资源全清）[发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。
- **安全与合规**：
  - 云端沙箱需遵守《阿里云产品服务协议》第 6 条，禁止安装盗版软件，用户对自行操作结果负全责 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
  - 记忆库中**不得存储密钥、[Token](../concepts/token.md) 等凭证**；密钥应通过密钥库（Vault）集中管理并按域名注入 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)、[记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。
- **计费**：费用分三部分独立计算——会话运行时费（0.5 元/小时）、模型调用费（按 token）、工具/MCP 调用费（如 `web_search` 0.03 元/次）[计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

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
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [Webhook 事件订阅](../../raw/application-user-guide/managed-agents/managed-agents-webhook.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


