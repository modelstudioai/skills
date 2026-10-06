# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件历史实现可追溯、可干预的执行过程。其核心价值在于将基础设施编排（沙箱、工具链、状态管理）下沉至平台层，使开发者聚焦于 Agent 逻辑本身。

## 支持的模型与功能

Managed Agents 支持百炼全系列大模型（如 `qwen3-max`、`qwen3.8-plus`），模型选择在创建 Agent 时指定，变更即生成新版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。Agent 的能力由以下组件共同构成：

- **内置工具**：共 9 个开箱即用工具，覆盖命令执行（`bash`）、文件操作（`read`/`write`/`edit`/`glob`/`grep`）、网络访问（`web_search`/`web_fetch`）及产出物标记（`mark_artifacts`）。其中 `web_search` 按 0.03 元/次计费，`web_fetch` 当前限时免费 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **MCP 服务**：通过 Model Context Protocol 接入官方市场或自定义 MCP 服务（如联网搜索、文档处理），挂载后其下工具默认启用，可单独开关 [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
- **Skill**：以 ZIP 包形式上传的端到端任务封装，需包含 `SKILL.md`（含 `name` 和 `description`），`description` 质量直接影响调用准确率 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
- **多智能体协作**：支持 `coordinator` 编队，协调者智能体可编排自身（`self`）及其他成员智能体（`agent`）协同工作 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。
- **记忆库（Memory Store）**：跨会话持久化的文件树资源，挂载后智能体可通过文件工具读写，所有修改自动产生历史版本，适用于长期知识沉淀 [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

> **注意**：文档 6 列出 9 个内置工具，但文档 1 和文档 2 的快速开始示例中仅提及 7 个（`bash`/`read`/`write`/`edit`/`glob`/`grep`/`mark_artifacts`），未包含 `web_search` 和 `web_fetch`。根据文档 23 的更新日志（2026-09-18 新增），这两个工具为后续迭代加入，因此当前实际支持的内置工具总数为 9 个，快速开始示例属于早期模板，已过时。

## 关键参数

Agent、Environment、Session 等资源均通过 API 或控制台配置关键参数，核心字段如下：

- **Agent**：`name`（工作空间内唯一）、`model.id`（必填，如 `"qwen3-max"`）、`system`（系统提示词）、`tools`（内置工具包配置，支持 `permission_policy` 审批策略）、`mcp_servers`（MCP 服务列表）、`skills`（技能引用）、`multiagent`（编队配置）[定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **Environment**：`name`（唯一标识）、`config.type`（固定为 `"cloud"`）、`config.packages`（预装包，支持 `apt`/`pip`/`npm`）、`config.networking.type`（`"unrestricted"` 放行出站）[云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **Session**：`agent`（Agent ID）、`environment_id`（环境 ID）、`resources`（挂载资源列表，支持 `file` 和 `memory_store` 类型）、`title`（会话标题）[发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。
- **审批策略**：对 `always_ask` 工具，必须通过 `POST /sessions/{session_id}/events` 发送 `tool_approval_response` 事件响应，携带 `batch_id` 和 `call_id`；发送普通 `message` 事件将被拒绝并返回 `pending_tool_approval_unresolved` 错误 [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。

## 使用方式

标准使用流程分为四步：创建 Agent → 创建 Environment → 创建 Session → 驱动交互。

1. **创建 Agent**：通过控制台向导或 API 指定模型、系统提示词和工具集。例如 Python SDK：
   ```python
   agent = client.agents.create(
       name="data-analyst",
       model="qwen3-max",
       system_prompt="你是数据分析专家，使用 pandas 处理 CSV 文件。",
       tools=[{"type": "builtin_toolkit", "configs": [{"name": "bash", "enabled": True}]}]
   )
   ```

2. **创建 Environment**：配置云端沙箱及预装依赖，例如安装 `pandas`：
   ```python
   env = client.environments.create(
       name="data-sandbox",
       config={"type": "cloud", "packages": {"pip": ["pandas"]}}
   )
   ```

3. **创建 Session**：绑定 Agent 和 Environment，并可选挂载文件或记忆库：
   ```python
   session = client.sessions.create(
       agent=agent.id,
       environment_id=env.id,
       resources=[{"type": "file", "file_id": "file_xxx", "mount_path": "/workspace/data.csv"}]
   )
   ```

4. **驱动交互**：通过 SSE 订阅事件流（`GET /sessions/{id}/events/stream`），并用 `POST /sessions/{id}/events` 发送用户消息或审批响应。**必须先建立 SSE 连接再发送事件**，否则可能错过 `tool_approval_request` [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。

此外，CLI 提供基础设施即代码（IaC）管理能力，支持 `bl managed-agent apply` 一键部署完整 Agent 栈 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。

## 限制和注意事项

- **配额限制**：单个文件 ≤ 50 MB，工作空间总文件容量 ≤ 100 GB，文件保存时效 30 天；单个记忆文件 ≤ 102400 UTF-8 字节，单会话最多挂载 8 个记忆库 [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)、[记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。
- **状态机约束**：会话处于 `idle` 且 `stop_reason=requires_action` 时，**禁止发送普通 `message` 事件**，只能提交 `tool_approval_response` 或发送 `interrupt`；其他 `idle` 状态（`null`/`end_turn`/`retries_exhausted`）才允许发送新消息 [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)。
- **资源生命周期**：Agent 和 Environment 支持归档（保留历史，不可新建会话），而 Skill 和 File 仅支持硬删除（不可恢复）；Session 归档后事件历史仍可查，删除则彻底清除 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)、[云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)、[Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)、[文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。
- **安全边界**：密钥库（Vault）的密钥以占位符 `${VAR}` 注入，**仅在 Authorization 请求头中、且目标域名匹配“密钥替换生效域名”时，才由网关替换为真实值**；请求体、查询参数及非匹配域名的请求均只传递占位符 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。
- **计费说明**：费用分三部分独立计算——会话运行时费（0.5 元/小时，按实际启用时长计）、模型调用费（按所用模型 token 计）、工具/MCP 调用费（如 `web_search` 0.03 元/次）[计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)
- [管理会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-operations.md)
- [发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)
- [会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)
- [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)
- [定时任务](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-deployment.md)
- [Webhook 通知](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-webhook.md)
- [文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)


