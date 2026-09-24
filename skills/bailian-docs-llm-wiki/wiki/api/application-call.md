# application call

`application call` 是阿里云百炼平台提供的核心能力，允许开发者通过标准 API 接口调用已发布的智能体（Agent）或工作流（Workflow）应用。该机制屏蔽底层模型调度与编排细节，统一暴露为 `app_id` 驱动的语义化服务调用，支持同步、异步及流式响应模式，并兼容 DashScope 原生协议与 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）和工作流（Workflow）三类应用，但不同 API 路径对类型的支持存在差异：
  - DashScope 原生 API（`/api/v1/apps/{APP_ID}/completion`）同时支持全部三类，是功能最完整的入口；
  - Responses API（`/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`）名义上支持智能体与工作流，但其[同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)明确指出“适用于需要即时获取结果的实时交互场景”，且文档中所有工作流示例均依赖控制台节点配置（如“流程输出节点”流式开关），实际能力受限于应用发布时的配置。
- **多模态能力**：当应用内选用通义千问 VL 系列模型时，可通过 `image_list`（DashScope API）或 `input_image`（Responses API）传入图像 URL 或 Data URL；文件输入（PDF/DOCX/MP3 等）仅限智能体应用，通过 `file_list`（DashScope）或 `input_file`（Responses）传递。
- **长期[记忆](../concepts/memory.md)**：仅新版智能体应用支持 `memory_id` 参数，用于关联用户级长期[记忆](../concepts/memory.md)体，需在应用中开启开关并发布后生效。
- **RAG 检索**：仅智能体应用支持 `rag_options` 参数，可指定知识库 ID（`pipeline_ids`）、文档 ID（`file_ids`）及元数据过滤条件（`metadata_filter`, `structured_filter`）。

> **注意**：[新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 和 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 均声明“仅适用于华北2（北京）地域”，但[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需项，且是 Base URL 的组成部分。这表明跨地域调用能力实际存在，但官方 API 文档未完整覆盖，开发者需以控制台显示的 Base URL 为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属 API |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，从控制台应用卡片复制获得。HTTP 调用时需填入 URL 路径；SDK 调用时作为独立参数。 | 全部 |
| `prompt` / `input` | string / array | 是 | 单轮文本输入为字符串；多轮或含多媒体时为消息数组（`messages`）。DashScope API 中 `prompt` 属于 `input` 对象；Responses API 中 `input` 直接承载内容。 | 全部 |
| `workspace` | string | 否 | 子业务空间 ID，仅当应用部署于子空间或特定地域（如法兰克福）时必需。HTTP 调用需通过 Header `X-DashScope-WorkSpace` 传递。 | 全部 |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)。DashScope 默认 `false`，Responses 默认 `false`；推荐设为 `true` 以降低超时风险。 | 全部 |
| `incremental_output` | boolean | 否 | 仅 DashScope API 支持，控制[流式输出](../concepts/streaming-output.md)是否为增量 delta（`true`）或全量追加（`false`）。 | DashScope |
| `flow_stream_mode` | string | 否 | 仅工作流应用在 DashScope API 中有效，指定流式推送格式（`message_format_plus` 推荐）。 | DashScope |
| `biz_params` | object | 否 | 传递自定义变量、插件参数或用户鉴权信息。Responses API 中需通过 `extra_body` 透传。 | 全部 |
| `has_thoughts` | boolean | 否 | 控制是否返回思考过程（`thoughts` 字段），需与 `enable_thinking`（新版智能体）或 `flow_stream_mode=full_thoughts`（工作流）配合使用。 | DashScope |

## 使用方式

- **HTTP 调用**：
  - DashScope 原生：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，Header 需含 `Authorization: Bearer {API_KEY}` 和可选的 `X-DashScope-WorkSpace`。
  - Responses（OpenAI 兼容）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，Header 同上，请求体结构遵循 OpenAI `responses.create` 规范。
- **SDK 调用**：
  - DashScope SDK（Python/Java）：使用 `Application.call()` 方法，自动处理 endpoint 和参数映射。
  - OpenAI SDK（Python/Java/Node.js 等）：初始化客户端时设置 `base_url` 为 Responses API 地址，调用 `client.responses.create()`。
- **在线调试**：所有应用在控制台“应用卡片 → 发布 → API 调试”中提供可视化界面，支持参数填写与实时运行。

## 限制和注意事项

- **地域限制**：所有官方文档均标注“仅适用于华北2（北京）地域”，但实际调用需依据控制台显示的 Base URL（如 `https://dashscope.aliyuncs.com/api/v1/apps/...`）——该 URL 已隐含地域信息，开发者无需手动拼接地域前缀。
- **会话管理**：`session_id` 有效期为 1 小时无请求即失效；`messages` 参数优先级高于 `session_id`，若同时传入则忽略历史会话。
- **异步限制**：Responses API 的异步模式（`background=true`）不支持 `stream=true`，且暂不支持基于 `pre_response_id` 的上下文续写，每次请求必须携带完整对话历史。
- **参数版本兼容性**：`flow_stream_mode` 要求 Python SDK ≥1.24.0、Java SDK ≥2.22.23；`image_list` 要求 Python SDK ≥1.24.7、Java SDK ≥2.21.13；`enable_thinking` 要求 Java SDK ≥2.20.0。低版本 SDK 可能忽略这些参数。
- **凭证获取**：APP ID 和 Workspace ID **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口，详见[获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


