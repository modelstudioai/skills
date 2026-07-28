# managed agents

Managed Agents 是百炼提供的智能体托管运行时，面向多步工具调用、代码执行、文件处理等长时运行任务。平台托管会话状态、沙箱环境和工具执行，智能体在独立的云端容器沙箱中自主运行命令、读写文件、安装依赖并处理数据，事件历史在服务端持久化。开发者只需专注 Agent 逻辑，无需自建代理循环、沙箱编排或工具执行基础设施。

## 与智能体应用的区别

| 维度 | 智能体应用 | Managed Agents |
| --- | --- | --- |
| 运行模式 | 无状态调用，应用侧维护上下文 | 服务端维护会话状态，支持中断与续接 |
| 执行环境 | 共享运行时 | 独立沙箱，云端容器 |
| 事件模型 | 响应级[流式输出](../concepts/streaming.md) | 会话级 SSE 事件流，事件历史持久化 |
| 典型场景 | 问答、对话、轻量任务 | 多步工具调用、代码执行、文件处理等长时运行任务 |

## 核心概念

详见[概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)：

- **智能体（Agent）**：模型、系统提示词、工具、MCP 服务和 Skill 的组合配置。创建后通过 ID 引用，可在多个会话中复用。
- **运行环境（Environment）**：会话运行的沙箱配置，由百炼托管的云端容器，独立于智能体管理，可被多个会话复用。
- **会话（Session）**：智能体在指定环境中的一次运行实例，执行任务并生成输出。
- **事件（Event）**：应用与智能体之间交换的消息，包括用户消息、工具调用结果和状态变更。

## 支持的模型与工具

- **模型**：创建智能体时从下拉列表选择或在 API 中指定，如 `qwen3-max`。
- **内置工具**：共 7 个，默认全选——`bash`（命令执行）、`read`、`write`、`edit`、`glob`、`grep`（文件操作与搜索）、`download_file`（从 URL 下载）。可按需取消勾选。
- **MCP 服务**：接入外部工具服务。
- **Skill（技能）**：挂载预置的工具组合，封装端到端任务流程。

> **注意**：[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)控制台示例中的模型名 `qwen3.7-plus` 与其 API 示例中的 `qwen3-max` 不一致，前者疑似笔误，实际以控制台下拉列表可选模型为准。

## 使用方式（4 步工作流程）

按[快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)，可通过控制台向导或 API 完成：

1. **创建智能体**：`POST /api/v1/agentstudio/agents`，指定 `name`、`model`、`system`（系统提示词）和 `tools`（`builtin_toolkit` 配置各工具的 `enabled`）。返回 `agent_xxx` ID 与版本号。
2. **配置运行环境**：`POST /api/v1/agentstudio/environments`，`config.type` 为 `cloud`（云端托管），可通过 `packages.apt` / `packages.pip` 预装依赖（如 `ffmpeg`、`pandas`），`networking.type` 可设为 `unrestricted`。
3. **创建会话**：`POST /api/v1/agentstudio/sessions`，用 `agent` 和 `environment_id` 绑定智能体与环境，可选 `title`。
4. **发送事件并接收响应**：向 `sessions/{id}/events` 写入 `role: user` 的 message 事件触发处理；通过 `sessions/{id}/events/stream` 以 SSE（`Accept: text/event-stream`）实时接收工具调用过程与输出，直到会话状态变为 `idle` 或 `terminated`。

所有接口以 `https://{workspace_id}.cn-beijing.maas.aliyuncs.com` 为 endpoint，使用 `Authorization: Bearer $DASHSCOPE_API_KEY` 认证；同时提供 Python / Java SDK。执行过程中可发送新事件引导方向，或中断当前任务；会话操作还支持状态机管理与审批工具调用（详见[委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)）。

## 上下文与文件挂载

根据 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)：

- 挂载资源是上下文中唯一独立于会话管理的部分，通过控制台或 API 创建后可挂载到一个或多个会话，生命周期与会话解耦。
- **挂载时机**：创建会话时在 `resources` 字段指定资源列表和挂载路径。
- **路径约定**：统一位于 `/mnt/session/uploads` 前缀下，可在系统提示词中直接引用完整路径。
- **会话隔离**：挂载时平台做内部拷贝放入会话沙箱；会话内修改不影响原始资源，也不影响挂载同一资源的其他会话；卸载后仅清理会话内副本。

环境层面还可管理外部服务的**凭证**（详见[配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)）。

## 限制与注意事项

- 单个挂载文件不超过 **10 MB**。
- 需已开通阿里云百炼，且当前账号在目标工作空间内具备 Managed Agents 操作权限。
- 会话有状态：跨多轮交互保持上下文和文件系统状态，适合持续数分钟到数小时的任务；轻量问答场景应使用普通智能体应用。
- 控制台"预览调试"页可按事件类型筛选（User、Agent、Tool、Tool_output、Error、Model、System），便于排查工具调用过程。
- 智能体的完整配置项（模型、提示词、内置工具、MCP、技能）入口见[构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)


