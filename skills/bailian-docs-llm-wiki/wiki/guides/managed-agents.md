# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境和工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过服务端持久化的事件历史实现中断与续接。相比无状态的智能体应用，Managed Agents 更适合需要有状态上下文、跨轮文件系统一致性及复杂编排能力的场景。

## 支持的模型与功能

Managed Agents 支持百炼全系列大模型（如 `qwen3-max`、`qwen3.7-plus`、`qwen3.8-max` 等），模型选择在创建智能体时指定，变更即生成新版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。核心功能覆盖：

- **多步工具调用**：内置 9 个开箱即用工具（`bash`、`read`、`write`、`edit`、`glob`、`grep`、`web_search`、`web_fetch`、`mark_artifacts`），全部在绑定的运行环境中执行 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)；
- **外部服务集成**：通过 MCP 协议接入官方市场或自定义 MCP 服务（如联网搜索、文档处理、图像服务等）[Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)；
- **端到端流程封装**：支持挂载 Skill（ZIP 包格式，含 `SKILL.md` 前置声明），复用预置任务逻辑 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)；
- **多智能体协作**：通过 `coordinator` 编队配置协调者与成员智能体，实现任务分发与结果聚合 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)；
- **上下文扩展**：支持挂载独立管理的文件（≤50 MB）和记忆库（跨会话持久化文件树），路径统一映射至 `/mnt/` 下 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)、[记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

> **注意**：文档 23 明确 `web_search` 与 `web_fetch` 于 2026-09-18 新增，但文档 6 中已将其列为内置工具并说明计费规则。二者无矛盾，属功能演进记录，当前所有文档均以该版本为准。

## 关键参数

创建与配置资源时需关注以下关键参数：

- **智能体（Agent）**：`name`（工作空间内唯一）、`model.id`（必填）、`system`（系统提示词）、`tools`（内置工具启用策略）、`mcp_servers`（MCP 服务列表）、`skills`（Skill ID 与版本）、`multiagent`（编队配置）；
- **运行环境（Environment）**：`config.type`（固定为 `"cloud"`）、`config.packages`（预装包，支持 `apt`/`pip`/`npm`）、`config.networking.type`（`"unrestricted"` 开放出站）；
- **会话（Session）**：`agent`（智能体 ID）、`environment_id`（环境 ID）、`resources`（挂载资源列表，含 `file_id`/`memory_store_id` 及 `mount_path`）、`title`（会话标题）；
- **工具审批**：通过 `tools[].configs[].permission_policy` 设置 `{"type": "always_allow"}` 或 `{"type": "always_ask"}`，仅对主智能体生效，且新建会话才继承新策略 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)；
- **密钥库（Vault）**：`variables` 中 `name`（变量名，不可修改）、`value`（密钥值，保存后仅回显末 4 位）、`domains`（密钥替换生效域名，支持 `*` 或 `*.example.com`）；密钥以 `${变量名}` 占位符形式注入，网关仅在匹配域名的 `Authorization: Bearer ${...}` 头中替换真实值 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。

## 使用方式

### 快速上手
1. **控制台向导**：进入「Managed Agents > 快速开始」，按步骤完成智能体（模型+工具）、环境（云端+预装包）、会话（绑定+挂载）三步配置；
2. **API 驱动**：调用 `POST /agents` 创建智能体，`POST /environments` 创建环境，`POST /sessions` 发起会话，再通过 `POST /sessions/{id}/events` 发送消息或审批响应；
3. **CLI 管理**：使用 `bl managed-agent init` 初始化项目，`bl managed-agent apply` 同步 YAML 配置（支持 Agent、Environment、Deployment 等资源声明）[使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

### 事件交互
- 会话通过 SSE（`GET /sessions/{id}/events/stream`）订阅实时事件流，关键事件包括 `message`（助手回复）、`tool_call`/`tool_call_output`（工具调用与结果）、`tool_approval_request`（待审批）、`session_status`（含 `stop_reason` 判断可交互性）；
- 客户端需根据 `session_status.stop_reason` 状态机驱动交互：`null`/`end_turn`/`retries_exhausted` 时可发新消息；`requires_action` 时必须提交 `tool_approval_response` 或 `interrupt`，禁止直接发送普通消息 [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)、[管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。

### 高级能力
- **定时任务**：创建 Deployment 绑定智能体与 cron 表达式，每次触发生成独立会话并执行初始消息 [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)；
- **Webhook 通知**：注册 Workspace 级 Webhook endpoint，订阅 Session/Agent/Deployment 等资源的 32 种事件，实现状态变更实时推送 [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)。

## 限制和注意事项

- **资源生命周期**：智能体与环境仅支持归档（`archive`），不支持删除；文件与 Skill 支持硬删除（`delete`），不可恢复；会话可归档（保留事件历史）或删除（彻底清除）；
- **配额约束**：
  - 文件：单个 ≤50 MB，工作空间总容量 ≤100 GB，保存时效 30 天；
  - 记忆库：单个记忆文件 ≤102400 UTF-8 bytes，单会话最多挂载 8 个；
  - 工具调用：`web_search` 按 0.03 元/次计费，`web_fetch` 当前限时免费 [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)；
- **安全限制**：
  - 密钥库密钥仅在 `Authorization` 请求头中替换，且仅限配置的 `domains`；请求体/查询参数中的占位符不替换；
  - 记忆库内容不应包含密钥、Token 等凭证，因其可能被智能体读取并输出；
  - 沙箱网络策略默认受限，如需外网访问须显式配置 `networking.type: unrestricted`；
- **行为约束**：
  - 工具审批策略不适用于子智能体（多智能体协作中）；
  - 记忆库仅支持创建会话时挂载，运行中不可新增/卸载/修改；
  - `web_search` 与 `web_fetch` 调用需单独开通权限，且受阿里云内容安全策略约束；
- **版本兼容性**：会话创建时锁定智能体版本，后续编辑不影响已有会话；Skill 挂载必须指定版本号，新版本上传不影响已绑定的智能体。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


