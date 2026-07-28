# 托管 Agent 与自建应用调用对比

阿里云百炼平台针对不同复杂度的智能体场景提供了两条主要落地路径：一是由平台托管运行时的 **Managed Agents**，二是通过 **DashScope / Responses API 调用**已在控制台配置好的**智能体应用**或**工作流应用**。二者定位不同、编排位置不同、状态管理方式不同，直接决定了适用场景与工程成本。本文横向对比二者的关键维度，帮助开发者在技术选型时做出判断。

## 背景与定位

- **Managed Agents（托管智能体）**：面向多步工具调用、代码执行、文件处理等长时任务，平台在服务端托管**会话状态**、**独立沙箱**与**工具执行器**。智能体在云端容器中自主运行 shell、读写文件、安装依赖，事件历史持久化，支持中断与续接。
- **自建应用调用（智能体应用 / 工作流应用）**：开发者在控制台编排应用（模型、提示词、知识库、插件、工作流节点等），再通过 API 从业务系统调用。运行时**无状态**，上下文由调用方或平台的 `session_id` 维护，适合问答、对话及可编排的工作流任务。
- **调用协议**：自建应用可选 **DashScope API**（`Application.call` / `POST /apps/{APP_ID}/completion`）或 **OpenAI 兼容的 Responses API**（`POST /api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`）。Managed Agents 走独立的 AgentStudio API（`/api/v1/agentstudio/*`）。

## 关键维度对比

| 维度 | Managed Agents（托管） | 智能体/工作流应用（DashScope API） | 智能体应用（Responses API，OpenAI 兼容） |
| --- | --- | --- | --- |
| 运行模式 | 服务端托管会话，长时任务，支持中断/续接 | 单次同步或流式调用，无状态 | 单次同步 / 流式 / 异步（`background=true`） |
| 状态管理 | 会话（Session）在服务端持久化，事件历史可回溯 | `session_id` 云端保存 1 小时、最多 50 轮；或客户端自维护 `messages` | 客户端在 `input` 数组中传完整消息历史 |
| 执行环境 | 独立云端沙箱容器，可预装 apt/pip 依赖、可配网络策略 | 平台共享运行时 | 平台共享运行时 |
| 输入格式 | 通过 `POST /sessions/{id}/events` 发送用户消息、工具结果、系统事件 | `{"input":{"prompt":"..."}, "parameters":{}, "biz_params":{...}}` | `input`：字符串或消息数组，支持 `input_image` / `input_file` [多模态](../concepts/multimodal.md) 类型 |
| 输出格式 | 会话级 SSE 事件流（User / Agent / Tool / Tool_output / Error / Model / System） | `{"output":{"text","finish_reason","session_id"}, "usage":{...}, "request_id":"..."}` | OpenAI Responses 标准结构（`response.output` 数组） |
| API 端点 | `/api/v1/agentstudio/agents`、`/environments`、`/sessions`、`/sessions/{id}/events`、`/sessions/{id}/events/stream` | `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion` | `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses` |
| SDK 支持 | AgentStudio HTTP API（可搭配任意 HTTP 客户端） | [DashScope SDK](../concepts/dashscope-sdk.md)（Python / Java），或 HTTP（Node.js / curl 等） | OpenAI 官方 SDK（Python / Java 等） |
| 内置工具 | `bash`、`read`、`write`、`edit`、`glob`、`grep`、`download_file`，可挂载 MCP 服务与 Skill | 由应用编排决定（知识库检索、插件、工作流节点等） | 同 DashScope 侧，取决于应用配置 |
| [多模态](../concepts/multimodal.md) | 通过文件挂载到 `/mnt/session/uploads` 参与工具处理 | 依赖应用内模型能力 | 原生支持 `input_image`（VL 模型 + 自定义处理）与 `input_file`（全文引用 / 切片检索） |
| 多轮对话 | 天然多轮：会话即上下文，事件历史持久化 | `session_id`（1 小时、≤ 50 轮）或自维护 `messages` | `input` 数组显式携带完整对话历史 |
| [流式输出](../concepts/streaming.md) | 默认 SSE 事件流 | 支持流式（工作流需在结束/输出节点开启开关） | `stream=true`；异步任务暂不支持流式 |
| 异步执行 | 天然长时任务，会话可中断/续接 | 暂不支持（需自行轮询业务状态） | `background=true` 提交任务，通过 `responses.retrieve(task_id)` 轮询 |
| 自定义参数透传 | 通过 Agent/Environment/Session 配置及事件负载 | `biz_params.user_defined_params` 面向自定义插件 / 工作流插件节点 | 同 DashScope 应用侧的插件透传 |
| 支持模型 | 由 Agent 配置选择（示例：`qwen3-max`；以控制台可选模型为准） | 由应用编排决定 | 由智能体应用编排决定，[多模态](../concepts/multimodal.md) 场景需选通义千问 VL 系列 |
| 资源挂载 | `resources` 字段或运行时 `POST /sessions/{id}/resources` 挂载，路径统一在 `/mnt/session/uploads`，单文件 ≤ 10 MB，会话隔离 | 通过知识库 / 附件 / 插件参数传递 | 通过 `input_file` URL 或应用知识库 |
| 计费与配额 | 计费与沙箱运行时、模型调用相关；单文件 ≤ 10 MB | 按模型调用量计费；`session_id` 缓存 1 小时 | 按模型调用量计费；异步/流式受限见文档 |
| 可用地域 | 见 AgentStudio 文档 | 仅华北 2（北京） | 仅华北 2（北京） |
| 典型场景 | 代码执行、批量文件处理、多步工具编排、长时任务 | 客服问答、RAG 检索、工作流驱动的业务自动化 | 需要 OpenAI 生态兼容、多模态输入或异步长任务的交互 |

## 各方案的适用场景建议

### 优先选 Managed Agents

- 任务需要**执行 shell 命令**、**读写文件**、**运行/调试代码**、**安装依赖**等真实计算操作。
- 单轮响应无法覆盖，需要**长时运行**、**中断续接**或**人工审批**工具调用。
- 需要**独立沙箱**（例如运行不受信代码、隔离网络策略、需要预装的运行环境）。
- 事件级可观测性要求高，需按 User / Agent / Tool / Model / Error 等类型审计执行过程。
- 会话内文件产物需被隔离拷贝管理，避免污染原始资源。

### 优先选 DashScope 应用调用

- 已经在控制台完成**智能体应用**或**工作流**编排，业务系统只需一次调用即可拿到结果。
- 需要使用**自定义插件**并通过 `biz_params.user_defined_params` 透传业务参数（如用户级鉴权、上下文字段）。
- 多轮对话强度中等，愿意使用平台 `session_id` 或客户端自维护 `messages`。
- 语言栈以 Python / Java 为主，倾向使用 [DashScope SDK](../concepts/dashscope-sdk.md) 的成熟示例。

### 优先选 Responses API（OpenAI 兼容）

- 现有代码或团队约定使用 **OpenAI SDK/生态**，希望以最小改动接入百炼。
- 需要**多模态输入**（`input_image` / `input_file`）或严格 OpenAI 输出结构。
- 需要**异步长任务**（`background=true`）并轮询结果，避免请求超时。
- 需要显式控制**完整对话历史**（在 `input` 中传消息数组）而不依赖 `session_id`。

## 技术选型参考

- **要不要托管运行时？** 若任务本质是"让 Agent 在容器里自己干活"，选 Managed Agents；若任务本质是"调一次已配置好的应用拿结果"，选自建应用调用。
- **要不要 OpenAI 兼容？** 是则 Responses API；否，且要用工作流/自定义插件，则 DashScope API；两者都不满足（需沙箱/工具执行）则 Managed Agents。
- **多轮对话怎么管？** 短会话选 `session_id`；需要精细控制或跨端同步选自维护 `messages` / Responses `input` 数组；长时有状态任务选 Managed Agents 会话。
- **要不要异步？** 长时任务但希望"提交-轮询"模式选 Responses API `background=true`；真正需要 Agent 自主推进的长任务选 Managed Agents（会话持久化 + 中断续接）。
- **模型与地域约束**：自建应用调用（两套 API）当前均限华北 2（北京）；模型 ID 需以控制台下拉列表为准，注意文档中 `qwen3-max` 与 `qwen3.7-plus` 等示例不一致的情况。
- **迁移路径**：可以先用自建应用调用跑通业务闭环，当出现需要"沙箱执行 + 长时状态"的诉求时再迁移到 Managed Agents；两者可在同一账号 / [业务空间](../concepts/workspace.md) 内共存，通过应用 ID / Agent ID 区分。

## 被对比主题页

- [managed agents](../guides/managed-agents.md)
- [bailian application calling](../guides/bailian-application-calling.md)
- [application call](../api/application-call.md)


