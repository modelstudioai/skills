# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API（包括 DashScope 原生接口和 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)）调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持同步与异步两种执行模式，覆盖单轮/多轮对话、[流式输出](../concepts/streaming-output.md)、多模态输入（图像/文件）、自定义参数传递及[长期记忆](../concepts/memory.md)等关键场景，是集成百炼应用到自有系统的主要技术路径。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）及工作流（Workflow）三类应用。新版智能体 API 与工作流/旧版智能体 API 在参数设计上存在差异，需按应用类型选用对应文档 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 或 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **多模态能力**：支持图像理解（需选用通义千问 VL 系列模型）和文件问答（仅智能体应用），通过 `image_list`（DashScope）或 `input_image`/`input_file`（Responses API）传入 URL 或 Data URL。
- **高级功能**：
  - [流式输出](../concepts/streaming-output.md)（`stream=true`）与增量输出（`incremental_output=true`）；
  - 深度思考模式（`enable_thinking=true` + `has_thoughts=true`）；
  - RAG 检索控制（`rag_options`，仅智能体）；
  - [长期记忆](../concepts/memory.md)（`memory_id`，仅智能体）；
  - 插件与自定义变量参数传递（`biz_params`）。

> **注意**：新版智能体 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API 文档同样标注“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 文档指出 Workspace ID 在德国（法兰克福）、新加坡等多地为必需项——这表明实际服务地域支持范围可能更广，API 地域限制描述存在不一致，建议以控制台可用地域及 Base URL 实际配置为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属接口 |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需填入 URL 路径。 | DashScope & Responses |
| `prompt` / `input` | string/array | 是 | 用户指令或完整消息数组（含 `system`/`user`/`assistant`）。`prompt` 用于单轮，`input`（数组）用于多轮或多模态。 | DashScope (`prompt`) / Responses (`input`) |
| `session_id` | string | 否 | 对话历史标识（仅 DashScope）。超时失效（1 小时无请求）。 | DashScope |
| `messages` | array | 否 | 替代 `prompt` 的多轮消息数组（仅工作流/旧版智能体 DashScope API）。若与 `session_id` 同时存在，优先使用 `messages`。 | DashScope（工作流/旧版） |
| `workspace` | string | 否 | 业务空间 ID，调用子业务空间应用或特定地域模型时必需。HTTP 调用需通过 `X-DashScope-WorkSpace` Header 传递。 | DashScope & Responses |
| `stream` | boolean | 否 | 是否[流式输出](../concepts/streaming-output.md)。`true` 时需按 SSE 协议解析 chunk。Responses API 中 `background=true` 时不可用。 | DashScope & Responses |
| `background` | boolean | 否 | Responses API 专用。设为 `true` 启动异步任务，立即返回 `task_id`。 | Responses |
| `biz_params` | object | 否 | 传递自定义变量、插件参数等。结构因应用类型而异（如 `user_prompt_params`, `user_defined_params`）。 | DashScope & Responses |

## 使用方式

- **DashScope 原生 API**  
  Endpoint: `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  认证：Header `Authorization: Bearer {DASHSCOPE_API_KEY}`  
  请求体结构：`input`（含 `prompt`/`messages`/`image_list` 等） + `parameters`（含 `stream`, `incremental_output`, `enable_thinking` 等）  
  SDK 支持：Python/Java 官方 SDK 提供 `Application.call()` 方法（示例见 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)）。

- **OpenAI 兼容 Responses API**  
  Endpoint: `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  认证：Header `Authorization: Bearer {DASHSCOPE_API_KEY}`  
  核心区别：  
  - `input` 字段直接承载字符串或标准 OpenAI `messages` 数组；  
  - 多模态通过 `content` 数组内嵌 `input_text`/`input_image`/`input_file` 对象；  
  - 异步通过 `background=true` 控制，同步则省略该字段或设为 `false`。  
  示例代码详见 [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 和 [异步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。

- **在线调试**：所有应用均支持在控制台“应用卡片 → 发布 → API 调试”中零代码验证参数与响应。

## 限制和注意事项

- **地域限制**：所有文档均标注“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 明确要求在德国（法兰克福）等多地调用时必须提供 `Workspace ID`，且其 Base URL 构成依赖地域。实际部署前务必确认目标地域的服务可用性与凭证要求。
- **异步限制**：Responses API 的异步模式（`background=true`）**不支持流式输出**（`stream=true` 会被忽略），且需自行实现轮询逻辑查询任务状态。
- **SDK 版本要求**：关键功能依赖特定 SDK 版本，例如 `incremental_output` 要求 Python SDK ≥1.24.7、Java SDK ≥2.21.13；`flow_stream_mode` 要求 Java SDK ≥2.22.23。低版本可能导致参数无效或报错。
- **凭证获取**：APP ID 和 Workspace ID **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口，自动化部署需预先配置。
- **参数冲突**：当 `messages` 与 `session_id` 同时传入 DashScope 工作流/旧版 API 时，`messages` 优先级更高，`session_id` 将被忽略。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)


