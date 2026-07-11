# managed agents

Managed Agents 是百炼提供的智能体托管运行时，面向多步工具调用、代码执行、文件处理等长时运行任务。与无状态的智能体应用不同，它由平台在服务端托管会话状态、沙箱环境与工具执行，智能体在独立云端容器中自主执行命令、读写文件、安装依赖，事件历史在服务端持久化并支持中断与续接。

## 与智能体应用的区别

| 维度 | 智能体应用 | Managed Agents |
| --- | --- | --- |
| 运行模式 | 无状态调用，应用侧维护上下文 | 服务端维护会话状态，支持中断与续接 |
| 执行环境 | 共享运行时 | 独立沙箱，云端容器 |
| 事件模型 | 响应级[流式输出](../concepts/streaming.md) | 会话级 SSE 事件流，事件历史持久化 |
| 典型场景 | 问答、对话、轻量任务 | 多步工具调用、代码执行、文件处理等长时任务 |

## 核心概念

四个核心对象构成完整的运行链路，详见 [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)：

- **智能体（Agent）**：模型、系统提示词、工具、MCP 服务和 Skill 的组合配置。创建后通过 ID 引用，可在多个会话中复用。
- **运行环境（Environment）**：会话运行的沙箱配置，由百炼托管的云端容器，独立于智能体管理，可被多个会话复用。
- **会话（Session）**：智能体在指定环境中的一次运行实例，承载任务执行与输出。
- **事件（Event）**：应用与智能体之间交换的消息，包括用户消息、工具调用结果和状态变更。

## 支持的工具

智能体通过以下工具与运行环境交互：

- **命令执行**：在沙箱中运行 shell 命令（`bash`）。
- **文件操作**：`read`、`write`、`edit`、`glob`、`grep`，以及从 URL 下载的 `download_file`；也可上传本地文件挂载到沙箱。
- **MCP 服务**：接入外部工具服务，详见 [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)。
- **Skill**：挂载预置的工具组合，封装端到端任务流程。

快速开始阶段默认全选 7 个内置工具（`bash`、`read`、`write`、`edit`、`glob`、`grep`、`download_file`），可按需取消勾选。

## 使用方式

典型流程分为四步（控制台向导或 API 均可完成），参见 [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)：

1. **配置智能体**：指定名称、模型（如 `qwen3-max`）、系统提示词与工具。API 为 `POST /api/v1/agentstudio/agents`。
2. **配置运行环境**：默认云端托管沙箱，可通过 `config.packages` 预装 apt / pip 依赖并设置网络策略。API 为 `POST /api/v1/agentstudio/environments`。
3. **发起会话**：绑定智能体 ID 与环境 ID 创建会话实例。API 为 `POST /api/v1/agentstudio/sessions`。
4. **发送事件并接收响应**：向会话写入用户消息触发处理（`POST /sessions/{id}/events`），通过 SSE 事件流实时接收工具调用过程与输出（`GET /sessions/{id}/events/stream`）。

控制台的**预览调试**标签页可直接对话并按事件类型（User、Agent、Tool、Tool_output、Error、Model、System）筛选查看执行过程。

### 上下文与资源挂载

上下文中的挂载资源独立于会话管理，可被多个会话复用，详见 [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)：

- **挂载时机**：创建会话时在 `resources` 字段指定，或运行时通过 `POST /sessions/{session_id}/resources` 追加，实时生效且无需重启会话。
- **路径约定**：挂载资源统一放在 `/mnt/session/uploads` 前缀下，可在系统提示词中直接引用完整路径。
- **会话隔离**：平台为挂载资源做内部拷贝放入沙箱，会话内的修改不影响原始资源，也不影响挂载同一资源的其他会话；卸载后副本被清理。

## 限制与注意事项

- 单个上传文件不超过 **10 MB**。
- 沙箱内文件路径遵循 `/mnt/session/uploads` 约定，代码中引用文件应使用该完整路径。
- 会话状态、中断续接与工具审批由会话状态机管理，详见 [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)。

> **注意**：文档中出现的模型名称不一致——控制台向导示例填写 `qwen3.7-plus`，而 API 代码示例使用 `qwen3-max`。请以控制台模型下拉列表中实际可选的模型 ID 为准。

## 来源文档

- [概述](../../raw/application-user-guide/managed-agents/managed-agents-introduction.md)
- [快速开始](../../raw/application-user-guide/managed-agents/managed-agents-quick-start.md)
- [构建 Agent](../../raw/application-user-guide/managed-agents/managed-agents-agent.md)
- [配置 Agent 环境](../../raw/application-user-guide/managed-agents/managed-agents-environment.md)
- [Agent 上下文管理](../../raw/application-user-guide/managed-agents/managed-agents-context.md)
- [委派任务给 Agent](../../raw/application-user-guide/managed-agents/managed-agents-session.md)


