# managed agents

Managed Agents 是百炼提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境和工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件历史实现可追溯、可干预的执行过程。其核心价值在于将基础设施编排（沙箱、工具执行、状态管理）从应用侧剥离，使开发者聚焦于 Agent 逻辑本身。

## 支持的模型与功能

Managed Agents 支持百炼全系列大模型（如 `qwen3-max`、`qwen3.8-plus` 等），模型选择在智能体定义时指定，变更即生成新版本。功能上覆盖完整的智能体能力栈：

- **内置工具**：共 9 个开箱即用工具，包括 `bash`（shell 命令）、`read`/`write`/`edit`（文件操作）、`glob`/`grep`（文件搜索）、`web_search`/`web_fetch`（联网检索）及 `mark_artifacts`（产出物标记）。其中 `web_search` 与 `web_fetch` 自 2026-09-18 起正式上线并按次计费 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **MCP 服务**：通过 Model Context Protocol 接入官方市场或自定义 MCP 服务（如联网搜索、文档处理、图像服务等），挂载后其下工具默认启用，支持独立审批策略。
- **Skill（技能）**：以 ZIP 包形式上传的端到端任务流程封装，需包含符合规范的 `SKILL.md` 文件，描述触发条件与适用场景，直接影响调用准确性 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
- **多智能体协作**：支持 `coordinator` 编队模式，协调者智能体可编排自身（`self`）及其他成员智能体（`agent`）协同完成复杂任务 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
- **记忆库（Memory Store）**：跨会话持久化的文件树资源，挂载后智能体可通过文件工具读写，内容自动保留历史版本，适用于项目知识沉淀与上下文复用 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

> **注意**：文档 6 明确列出 `web_search` 和 `web_fetch` 为内置工具，但文档 23 的更新日志将其标注为“新增”功能。该差异表明这两个工具是后续迭代加入的，当前所有文档均以文档 6 的工具列表为准，其功能与计费规则应以 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md) 为准。

## 关键参数

创建与配置各资源时需关注以下关键参数：

- **Agent**：`name`（工作空间内唯一）、`model.id`（必填，如 `"qwen3-max"`）、`system`（系统提示词）、`tools`（内置工具启用状态与审批策略）、`mcp_servers`（MCP 服务引用）、`skills`（技能 ID 与版本）、`multiagent`（编队配置）。每次保存产生新 `version`，会话创建时锁定该版本。
- **Environment**：`name`（唯一标识）、`config.type`（固定为 `"cloud"`）、`config.packages`（预装包，支持 `apt`/`pip`/`npm`）、`config.networking.type`（`"unrestricted"` 启用出站访问）。
- **Session**：`agent`（Agent ID）、`environment_id`（环境 ID）、`resources`（挂载的文件、记忆库等，路径需以 `/mnt/` 开头）、`title`（会话标题）。会话启动后快照 Agent 配置，后续 Agent 变更不影响已存在会话。
- **Deployment（定时任务）**：`schedule.type`（`"cron"`）、`schedule.expression`（标准五位 cron 表达式）、`initial_events`（触发时发送的初始消息）、`agent.version`（锁定智能体版本）。
- **审批策略**：对 `builtin_toolkit` 或 `mcp_toolkit` 中的单个工具，通过 `permission_policy: {"type": "always_allow" | "always_ask"}` 配置。`always_ask` 工具调用时会暂停会话并等待人工裁决，该策略仅对主智能体生效，且新建会话才生效 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。

## 使用方式

典型工作流分为四步，可通过控制台、API 或 CLI 完成：

1. **创建 Agent**：配置模型、系统提示词、工具（含审批策略）、MCP、Skill 等。例如使用 Python SDK：
   ```python
   agent = client.agents.create(
       name="data-analyst",
       model="qwen3-max",
       system_prompt="你是数据分析专家。",
       tools=[{"type": "builtin_toolkit", "configs": [{"name": "bash", "enabled": True, "permission_policy": {"type": "always_ask"}}]}]
   )
   ```

2. **创建 Environment**：定义沙箱，预装所需依赖。例如：
   ```python
   env = client.environments.create(
       name="data-sandbox",
       config={"type": "cloud", "packages": {"pip": ["pandas", "numpy"]}}
   )
   ```

3. **发起 Session**：绑定 Agent 与 Environment，挂载文件或记忆库。例如：
   ```python
   session = client.sessions.create(
       agent=agent.id,
       environment_id=env.id,
       resources=[{"type": "file", "file_id": "file_xxx", "mount_path": "/workspace/data.csv"}]
   )
   ```

4. **交互与管理**：
   - 通过 `POST /sessions/{id}/events` 发送 `message` 事件驱动智能体；
   - 订阅 `GET /sessions/{id}/events/stream` SSE 流实时接收 `message`、`tool_call`、`tool_approval_request` 等事件；
   - 对 `requires_action` 状态的会话，需发送 `tool_approval_response` 事件完成裁决；
   - 使用 CLI 可实现 IaC 管理：`bl managed-agent init` 初始化项目，`bl managed-agent apply` 创建资源，`bl managed-agent playground` 调试会话 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **配额与生命周期**：单个文件 ≤ 50 MB，工作空间总容量 ≤ 100 GB，文件保存时效 30 天；单个记忆文件 ≤ 102400 UTF-8 bytes，单会话最多挂载 8 个记忆库；Agent 和 Environment 支持归档，Skill 和 File 支持删除，会话支持归档（保留历史）或删除（彻底清除）。
- **安全约束**：云端沙箱禁止安装盗版软件，用户对自行安装的软件及操作结果承担全部责任 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)；密钥库仅支持 `Authorization` 请求头中的 Bearer 占位符替换，请求体与查询参数中的密钥占位符不会被替换，且仅对配置的生效域名生效。
- **状态与交互**：会话状态机严格依赖 `stop_reason` 字段判断可交互性——仅当 `stop_reason` 为 `requires_action` 时禁止发送普通消息，必须先提交审批或中断；其他 `idle` 状态（`null`/`end_turn`/`retries_exhausted`）均可直接发送新消息。客户端切勿仅凭 `idle` 状态做判断 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **计费**：费用由三部分组成：会话运行时费（0.5 元/小时，按实际运行时长计）、模型调用费（按所用模型 token 消耗计）、工具/MCP 调用费（如 `web_search` 0.03 元/次）。免费额度仅抵扣运行时费，不抵扣其余两项 [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


