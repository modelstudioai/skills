# managed agents

Managed Agents 是百炼提供的智能体托管运行时，适用于多步工具调用、代码执行、文件处理等长时运行任务。平台统一托管会话状态、[沙箱](../concepts/sandbox.md)环境和工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖并处理数据，所有事件历史在服务端持久化。与无状态的智能体应用不同，Managed Agents 天然支持中断续接、跨轮上下文保持和资源状态复用。

## 支持的模型与功能

- **模型支持**：支持百炼全系列大模型（如 `qwen3-max`、`qwen3.7-plus`、`qwen3.8-max`），模型通过 `model.id` 字段指定，变更即生成新版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **核心工具**：9 个内置工具覆盖全栈操作能力，包括 `bash`（shell 命令）、`read`/`write`/`edit`/`glob`/`grep`（文件操作）、`web_search`/`web_fetch`（网络访问）和 `mark_artifacts`（产出物标记）[Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **扩展能力**：
  - **MCP 服务**：通过标准协议接入官方市场或自定义 MCP 服务（如联网搜索、文档处理），挂载后默认启用全部工具，可按需关闭单个工具 [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
  - **Skills**：以 ZIP 包形式上传的端到端任务封装，含 `SKILL.md` 前置声明（含 name/description），触发逻辑由模型根据 description 自动判断 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
  - **多智能体协作**：通过 `multiagent.type=coordinator` 配置编队，支持 `self` 和 `agent` 类型成员，最多 20 个成员 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
- **上下文资源**：支持挂载独立管理的资源，包括：
  - **文件**：单文件 ≤50 MB，挂载后在[沙箱](../concepts/sandbox.md)内为只读副本，路径前缀为 `/mnt/session/uploads/` [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。
  - **记忆库（Memory Store）**：跨会话持久化的文件树，挂载路径为 `/mnt/memory/<名称>`，支持读写、版本追踪与历史回溯 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

> **注意**：文档 22 明确 `web_search` 与 `web_fetch` 于 2026-09-18 新增，但文档 5 中已将其列为 9 个内置工具之一且未标注时效性。实际使用应以文档 22 的发布日期为准，确认当前环境是否已启用该功能。

## 关键参数

| 参数 | 位置 | 说明 | 可变性 |
|------|------|------|--------|
| `model.id` | Agent 创建/更新 | 指定基础大模型，如 `"qwen3-max"` | ✅ 变更即生成新版本 |
| `system` / `system_prompt` | Agent 创建/更新 | 定义角色、行为与约束的系统提示词 | ✅ 变更即生成新版本 |
| `tools` | Agent 创建/更新 | 内置工具包（`builtin_toolkit`）及 MCP 工具包（`mcp_toolkit`）配置，含 `enabled` 和 `permission_policy`（`always_allow`/`always_ask`） | ✅ 变更即生成新版本 |
| `multiagent` | Agent 创建/更新 | 协作拓扑配置，仅支持 `coordinator` 类型，`agents` 数组定义成员 | ✅ 变更即生成新版本 |
| `skills` | Agent 创建/更新 | 技能引用列表，必须指定 `skill_id` 和 `version` | ✅ 变更即生成新版本 |
| `environment_id` | Session 创建 | 绑定的运行环境 ID，决定[沙箱](../concepts/sandbox.md)类型、预装包和网络策略 | ❌ 会话创建后不可变更 |
| `resources` | Session 创建/运行时追加 | 挂载资源列表，支持 `file`（含 `mount_path`）和 `memory_store`（含 `access` 权限） | ✅ 运行时可追加文件；记忆库仅支持创建时挂载 |

## 使用方式

1. **创建智能体（Agent）**：  
   通过控制台向导或 API 指定 `name`、`model.id`、`system` 和 `tools`。每次保存生成新 `version`，会话创建时锁定该版本 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)。

2. **配置运行环境（Environment）**：  
   创建云端沙箱，声明 `config.type="cloud"` 及预装包（`apt`/`pip`/`npm`）。环境独立于 Agent 管理，可被多个会话复用 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。

3. **发起会话（Session）**：  
   调用 `POST /sessions`，传入 `agent`（ID 或 `{id, version}`）、`environment_id` 和 `resources`。会话启动后，通过 `POST /sessions/{id}/events` 发送 `message` 事件触发处理，并通过 `GET /sessions/{id}/events/stream` 订阅 SSE 事件流接收 `message`、`tool_call`、`tool_approval_request` 等实时反馈 [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。

4. **审批与干预**：  
   当工具设为 `always_ask` 时，事件流推送 `tool_approval_request`，会话进入 `idle` 状态且 `stop_reason=requires_action`。此时必须发送 `tool_approval_response`（含 `batch_id` 和 `call_id`）或 `interrupt`，不可直接发送普通消息 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。

5. **CLI 管理（基础设施即代码）**：  
   使用 `bl managed-agent` 命令集管理全生命周期：`init` 生成 YAML 模板，`apply` 同步资源配置，`playground` 启动调试界面，`deployment create/run` 管理定时任务 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **配额限制**：  
  - 文件单个 ≤50 MB，工作空间总容量 ≤100 GB，保存时效 30 天；  
  - 记忆库单个记忆文件 ≤102400 UTF-8 bytes，单会话最多挂载 8 个；  
  - 多智能体编队最多 20 个成员 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)、[记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)、[多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。

- **安全与权限**：  
  - 密钥库（Vault）密钥以占位符 `${VAR}` 形式注入，**仅在 Authorization 请求头中、且目标域名匹配 `生效域名` 列表时**由网关替换为真实值；请求体/查询参数中的占位符永不替换 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。  
  - 记忆库中严禁存储密钥、[Token](../concepts/token.md) 等凭证，因其内容可被智能体直接读写 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

- **计费说明**：  
  - 费用分三部分：**会话运行时费**（0.5 元/小时，按实际运行时长计）、**模型调用费**（按所用模型 token 实际消耗）、**工具/MCP 调用费**（如 `web_search` 0.03 元/次）[计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。  
  - 免费额度仅抵扣运行时费，不覆盖模型或工具费用。

- **关键行为约束**：  
  - 会话创建后，`environment_id` 不可变更；记忆库仅支持创建时挂载，运行时不可新增/卸载；  
  - 工具审批策略（`always_ask`）仅对主智能体生效，子智能体不支持；  
  - `web_search` 与 `web_fetch` 单独计费，且 `web_fetch` 当前为限时免费，后续收费计划以控制台展示为准 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)


