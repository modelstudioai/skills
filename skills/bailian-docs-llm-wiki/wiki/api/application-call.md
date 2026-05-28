# application call

本文档介绍如何通过 API 调用阿里云百炼平台的应用（智能体与工作流）。平台提供原生 DashScope 协议与 OpenAI 兼容的 Responses API 两种接入方式，全面支持同步/异步执行、流式/非[[streaming-output|流式输出]]及多轮会话交互。开发者可基于现有代码库快速集成，或根据实时性与业务复杂度灵活选择调用模式。

## 支持的模型与功能
- **应用类型**：支持调用 [[智能体应用]]（含新版 Agent 2.0）与 [[工作流应用]]。
- **协议体系**：
  - **DashScope 原生 API**：提供完整参数控制，Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`。
  - **OpenAI 兼容 Responses API**：符合 OpenAI 规范，便于生态迁移，Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`。详细同步调用规范请参考 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)。
- **交互模式**：支持单轮查询、多轮上下文保持、SSE [[streaming-output|流式输出]]（适用于对话补全）以及后台异步任务提交。
- **多模态能力**：支持纯文本、图像 URL (`input_image`) 及文件 URL (`input_file`) 输入，满足图文问答与文档分析场景。

## 关键参数说明
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `app_id` | string | 是 | 目标应用唯一标识。需替换 URL 路径或请求体中的 `{APP_ID}`。 |
| `workspace_id` | string | 条件 | 应用归属子业务空间时必须传入。凭证获取步骤详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `input` / `[[prompt|prompt]]` | string/array | 是 | 核心输入。DashScope 协议使用 `input.[[prompt|prompt]]`；OpenAI 协议支持字符串或 `messages` 对象数组。 |
| `session_id` | string | 否 | 用于 DashScope 协议维持会话状态。首次调用后需从响应中提取并缓存。 |
| `stream` | boolean | 否 | 是否开启[[streaming-output|流式输出]]。默认为 `false`。开启后服务端以 SSE 格式逐块返回增量文本。 |
| `background` | boolean | 否 | 是否转为异步任务。默认为 `false`。设为 `true` 时立即返回 `task_id`，需轮询获取结果。 |
| `biz_params` | object | 否 | 透传自定义业务参数至工作流开始节点或智能体插件，键名需与 [[应用参数配置]] 完全一致。 |

## 使用方式
### 1. 凭证与环境准备
调用前需获取 `APP ID`，并配置环境变量 `DASHSCOPE_API_KEY`。建议使用官方 [[DashScope SDK]] 或 [[OpenAI Python SDK]] 进行请求封装，以简化鉴权与重试逻辑。

### 2. 多轮对话实现
- **DashScope 协议**：依赖服务端托管的 `session_id`。客户端在后续请求中透传上一次响应的 `session_id` 即可自动续接上下文。该会话 ID 在最后一次交互后 1 小时内有效。
- **OpenAI 兼容协议**：需客户端自行维护消息历史。每次请求需将包含完整 `system`、`user`、`assistant` 角色的 `input` 数组整体传入。
> **注意**：不同文档对上下文维护机制的说明存在演进差异。基于 OpenAI Responses API 的 `pre_response_id` 或 `conversation_id` 自动托管功能当前**尚未开放**，请务必采用客户端缓存并全量传递消息数组的方式实现多轮对话，避免因服务端未记录历史导致上下文丢失。

### 3. 异步任务与状态轮询
针对耗时较长的报告生成或复杂工作流，推荐启用异步模式。在请求体中设置 `background: true`，获取 `task_id` 后通过 SDK 的 `retrieve()` 方法或 REST API 定期查询任务状态。终态包含 `completed`（成功）、`failed`（失败）或 `cancelled`（已取消）。完整异步调度与轮询示例请参考 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
> **注意**：异步任务 (`background=true`) 与流式输出 (`stream=true`) **互斥**，当前版本不支持在异步模式下开启 `stream`，请勿在请求体中同时设置这两个参数。

## 限制与注意事项
- **地域限制**：当前 API 调用端点仅适用于中国大陆版（北京地域）。调用德国（法兰克福）等地域模型时需严格校验 `workspace_id` 并使用对应 Global Endpoint。
- **配置生效依赖**：若在控制台修改了视觉模型选型（需切换至 [[通义千问VL系列]]）、文件处理策略（需设为全文引用或切片检索）或工作流节点的流式开关，**必须重新发布应用**，否则 API 调用将沿用旧版配置或返回参数不匹配错误。
- **文件输入约束**：`input_file` 参数仅支持 [[智能体应用]]，[[工作流应用]] 暂不支持通过 API 直传文件对象。
- **权限管控**：`Workspace ID` 的查询依赖 RAM 权限体系。子账号默认仅能查看已加入的业务空间，查询全量 ID 需主账号或具备 `AliyunBailianFullAccess` 策略授权的子账号操作。
- **调试建议**：在代码集成前，建议优先使用控制台 **应用卡片 -> 发布 -> API 调试** 路径验证参数组合与业务逻辑，确认响应结构符合预期后再进行生产环境联调。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/agent-and-workflow-application-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/application-api-reference/application-call/application-dashscope-api-reference/new-agent-application-api-reference.md)

