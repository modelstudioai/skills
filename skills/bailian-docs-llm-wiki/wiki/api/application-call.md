# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API（包括 DashScope 原生接口和 [OpenAI 兼容接口](../concepts/openai-compatibility.md)）调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需自行部署模型与编排逻辑，只需传入业务输入、凭证及可选上下文，即可获得结构化或流式响应。该机制统一了应用层抽象，支持文本、图像、文件、多轮对话及异步长任务等多种交互范式。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）及工作流（Workflow）三类应用，详见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 和 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **多模态能力**：当应用配置为通义千问 VL 系列模型时，可通过 `image_list`（DashScope）或 `input_image`（Responses API）传入图像 URL 或 Data URL；智能体应用还支持 `file_list` / `input_file` 进行文档、音视频问答。
- **长期记忆与 RAG**：智能体应用支持通过 `memory_id` 启用长期记忆；同时提供 `rag_options` 参数（仅 DashScope API），用于指定知识库 ID（`pipeline_ids`）、文档 ID（`file_ids`）及元数据过滤条件，实现精准检索增强。
- **异步执行**：通过 Responses API 的 `background=true` 模式发起耗时任务，立即返回 `task_id`，后续通过轮询 `retrieve` 接口获取结果，适用于报告生成、批量处理等场景，详见 [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

> **注意**：DashScope API 与 Responses API 在功能覆盖上存在差异。例如，`rag_options` 仅在 DashScope API 中可用；而 Responses API 的 `input` 字段原生支持消息数组（含 `system`/`user`/`assistant` 角色）和多模态 `content` 数组，无需额外封装到 `input` 对象内。开发者应根据需求选择合适接口。

## 关键参数

| 参数名 | 类型 | 是否必选 | 说明 | 所属接口 |
|--------|------|----------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需填入 URL 路径。 | 全部 |
| `prompt` | string | 是（DashScope 单轮） | 用户指令文本。DashScope API 中为顶层字段；Responses API 中需置于 `input` 内。 | DashScope |
| `input` | string/array | 是（Responses） | 核心输入：单字符串（单轮）或消息数组（多轮/多模态）。消息数组支持 `system`/`user`/`assistant` 角色及 `input_text`/`input_image`/`input_file` 类型。 | Responses |
| `session_id` | string | 否 | 用于恢复对话历史的会话标识，1 小时无请求自动失效。仅 DashScope API 支持。 | DashScope |
| `messages` | array | 否（DashScope 多轮） | 替代 `prompt` + `session_id` 的多轮对话方式，按顺序包含 `system`/`user`/`assistant` 消息对象。 | DashScope |
| `workspace` | string | 否 | 业务空间 ID，调用子业务空间或德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）地域模型时必需。HTTP 调用需通过 `X-DashScope-WorkSpace` Header 传递。 | 全部 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming.md)。DashScope 默认 `false`；Responses 默认 `false`，设为 `true` 时需客户端逐 chunk 解析。 | 全部 |
| `biz_params` | object | 否 | 传递自定义变量、插件参数或用户级鉴权信息（如 `user_prompt_params`, `user_defined_params`, `user_defined_tokens`）。DashScope 和 Responses 均支持，但 Responses 需通过 `extra_body` 透传。 | 全部 |
| `rag_options` | object | 否 | 检索增强配置，含 `pipeline_ids`（知识库 ID 列表）、`file_ids`（文档 ID 列表）、`metadata_filter`（元数据过滤）等。**仅 DashScope API 支持**。 | DashScope |

## 使用方式

### 1. 凭证准备
- **APP ID**：在 [应用管理](https://bailian.console.aliyun.com/#/app-center) 页面复制目标应用卡片上的 ID。
- **Workspace ID**：若应用位于子业务空间或上述特定地域，需通过控制台右上角工作空间图标或 [业务空间管理](https://bailian.console.aliyun.com/?tab=globalset#/efm/business_management) 页面获取，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。
- **API Key**：在 [密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key) 创建并配置至环境变量 `DASHSCOPE_API_KEY`。

### 2. 接口选择与调用
- **DashScope 原生 API**（推荐用于高级功能）：
  - 终端：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`
  - SDK：Python/Java SDK 提供 `Application.call()` 方法，自动处理 endpoint 与认证。
- **OpenAI 兼容 Responses API**（推荐用于快速迁移）：
  - 同步：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`
  - 异步：同上 endpoint，请求体中设置 `"background": true`，再通过 `GET /responses/{task_id}` 查询。
- **在线调试**：所有应用均支持在控制台“应用卡片 → 发布 → API 调试”中直接测试参数与响应。

### 3. 流式与增量输出
- 设置 `stream=true` 后，DashScope 需在 Header 中添加 `X-DashScope-SSE: enable`；Responses API 直接在请求体中设置 `"stream": true`。
- 若需增量输出（即后续 chunk 不重复前序内容），DashScope 需额外设置 `incremental_output=true`（放入 `parameters`）；Responses API 无此参数，其流式 `delta` 字段天然为增量。

## 限制和注意事项

- **地域限制**：所有文档均明确标注“本文档仅适用于华北2（北京）地域”。其他地域（如德国、新加坡）调用时，必须显式传入 `Workspace ID`，且 Base URL 可能不同，具体请参考 [Regions 文档](raw/model-user-guide/get-started-with-models/regions.md)。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本。例如，`incremental_output` 要求 Java SDK ≥ 2.20.0；`flow_stream_mode` 要求 Java SDK ≥ 2.22.23；`file_list` 要求 Python SDK ≥ 1.24.7。低版本 SDK 可能导致参数被忽略或报错。
- **异步限制**：Responses API 的异步模式（`background=true`）**不支持[流式输出](../concepts/streaming.md)**（`stream=true` 会被忽略），且暂不支持基于 `pre_response_id` 或 `conversation_id` 的上下文自动续接，每次请求需传入完整 `input`。
- **参数冲突**：当 `messages` 与 `prompt` + `session_id` 同时存在时，DashScope API 优先使用 `messages`，`session_id` 和 `prompt` 将被忽略。Responses API 仅接受 `input` 字段，不存在此冲突。
- **权限约束**：查询所有 Workspace ID 需主账号或具备 `AliyunBailianFullAccess` 权限的 RAM 子账号；普通子账号仅能查看已加入的业务空间，详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


