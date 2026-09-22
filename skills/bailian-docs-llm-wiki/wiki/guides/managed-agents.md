# managed agents

Managed Agents 是百炼平台提供的智能体托管运行时，专为多步工具调用、代码执行、文件处理等长时运行任务设计。平台统一托管会话状态、沙箱环境与工具执行生命周期，智能体在隔离的云端容器中自主执行命令、读写文件、安装依赖，并通过持久化的事件历史实现可追溯、可干预的执行过程。其核心价值在于将开发者从代理循环编排、沙箱运维和工具调度等基础设施负担中解放出来，聚焦于 Agent 逻辑本身。

## 支持的模型与功能

Managed Agents 支持百炼全量大模型（如 `qwen3-max`、`qwen3.8-plus` 等），模型选择在智能体定义阶段指定，变更即生成新版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。功能能力由以下组件协同提供：

- **内置工具**：共 9 个开箱即用工具，覆盖命令执行（`bash`）、文件操作（`read`/`write`/`edit`/`glob`/`grep`）、网络访问（`web_search`/`web_fetch`）及产出物标记（`mark_artifacts`）。其中 `web_search` 按 0.03 元/次计费，`web_fetch` 当前限时免费 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **MCP 服务**：通过 Model Context Protocol 接入官方市场（如联网搜索、文档处理）或自定义 MCP 服务（插件、AI 网关、OpenAPI 等），挂载后其下工具默认启用，可单独开关 [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)。
- **Skill（技能）**：以 ZIP 包形式上传的端到端任务封装，需包含 `SKILL.md`（含 `name` 和 `description`），`description` 质量直接影响调用准确性；挂载时必须指定版本号 [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)。
- **多智能体协作**：支持 `coordinator` 编队模式，协调者智能体可编排自身（`self`）及最多 20 个成员智能体（`agent`），成员版本可显式锁定 [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)。

> **注意**：文档 22 明确 `web_search` 与 `web_fetch` 为 2026-09-18 新增工具，而文档 6 的工具列表描述为“9 个内置工具”，二者一致；但文档 2 的快速开始示例中仅列出 7 个工具（`bash`/`read`/`write`/`edit`/`glob`/`grep`/`mark_artifacts`），未包含新增的 `web_search` 和 `web_fetch`，该示例已过时，应以文档 6 的完整列表为准。

## 关键参数

创建与管理资源时需关注以下关键参数：

- **智能体（Agent）**：`name`（工作空间内唯一）、`model.id`（必填）、`system`（系统提示词）、`tools`（内置工具包配置，支持 `permission_policy` 审批策略）、`multiagent`（编队配置）、`skills`（技能引用）、`mcp_servers`（MCP 服务引用）[定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
- **运行环境（Environment）**：`name`（唯一标识）、`config.type`（固定为 `"cloud"`）、`config.packages`（预装包，支持 `apt`/`pip`/`npm`）、`config.networking.type`（`"unrestricted"` 放行出站）[云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **会话（Session）**：`agent`（智能体 ID）、`environment_id`（环境 ID）、`resources`（挂载资源，含 `file` 和 `memory_store` 类型）、`title`（会话标题）[发起会话](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-session-event.md)。
- **记忆库（Memory Store）**：`name`（唯一）、`access`（挂载权限，`read_write` 或 `read_only`）、`instructions`（挂载说明，供智能体理解用途）[记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)。

## 使用方式

标准使用流程为三步：**定义智能体 → 配置环境 → 发起会话**。

1. **定义智能体**：在控制台或通过 API 创建智能体，配置模型、系统提示词、工具（含审批策略）、MCP、Skill 及多智能体编队。每次保存生成新 `version`，会话创建时锁定该版本 [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)。
2. **配置运行环境**：创建独立的云端沙箱，声明预装包（如 `pip: ["pandas", "numpy"]`）和网络策略。环境可被多个会话复用 [云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
3. **发起会话**：
   - 控制台：在智能体详情页点击“新建会话”，绑定环境并挂载资源（文件、记忆库）。
   - API：调用 `POST /sessions`，传入 `agent`、`environment_id` 和 `resources`。
   - CLI：使用 `bl managed-agent session run --prompt "..."` 快速启动 [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)。
   - 交互：通过 `POST /sessions/{id}/events` 发送 `message` 事件触发执行；通过 `GET /sessions/{id}/events/stream` 订阅 SSE 事件流接收实时反馈（`message`、`tool_call`、`tool_approval_request` 等）[会话事件流（SSE）](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-event-stream.md)。

## 限制和注意事项

- **资源生命周期**：智能体与环境仅支持归档（`archive`），不支持删除；文件与 Skill 支持硬删除；会话支持归档（保留事件历史）与删除（彻底清除）[定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)、[云端托管环境](../../raw/application-user-guide/managed-agents/managed-agents-environment/managed-agents-cloud-hosting.md)。
- **挂载限制**：单个会话最多挂载 8 个记忆库；单个记忆文件最大 102400 UTF-8 字节；单个文件最大 50 MB，工作空间总容量上限 100 GB [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)、[文件上传与挂载](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-file.md)。
- **审批机制**：工具审批（`always_ask`）仅对主智能体生效，子智能体不支持；审批策略变更不影响已存在的会话，需新建会话生效；客户端工具（`function`/`custom`）不参与此审批链路 [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)。
- **密钥安全**：密钥库密钥以占位符（如 `${MY_API_KEY}`）注入，仅在请求发往配置的“生效域名”且目标为 `Authorization: Bearer ...` 头时，由网关替换为真实值；其他位置（请求体、查询参数）或未匹配域名均只传递占位符 [密钥库认证](../../raw/application-user-guide/managed-agents/managed-agents-session/managed-agents-credential.md)。
- **计费提醒**：自 2026-08-17 起正式计费，费用分为三部分：会话运行时费（0.5 元/小时）、模型调用费（按所用模型标准）、工具/MCP 调用费（如 `web_search` 0.03 元/次）；赠送 10 小时运行时免费额度，有效期 30 天 [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [使用 CLI](../../raw/application-user-guide/managed-agents/managed-agents-cli.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [定义 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-agent-definition.md)
- [Agent 工具配置](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-builtin-tools.md)
- [多智能体协作](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-multiagent.md)
- [Agent Skills](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-skill.md)
- [Agent MCP](../../raw/application-user-guide/managed-agents/managed-agents-agent/managed-agents-mcp.md)
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
- [记忆库](../../raw/application-user-guide/managed-agents/managed-agents-context/managed-agents-memory-store.md)
- [更新日志](../../raw/application-user-guide/managed-agents/managed-agents-changelog.md)
- [计费说明](../../raw/application-user-guide/managed-agents/managed-agents-billing.md)


