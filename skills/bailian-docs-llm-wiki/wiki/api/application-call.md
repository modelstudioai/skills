# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需自行部署模型与编排逻辑，只需传入业务输入、会话上下文及可选的运行时参数，即可获得结构化输出或流式响应。该能力统一支持 DashScope 原生协议与 OpenAI 兼容协议，适配不同技术栈的集成需求。

## 支持的模型/功能

- **应用类型**：支持新版智能体（Agent 2.0）、旧版智能体（Agent 1.0）和工作流（Workflow）三类应用，对应不同的 API 行为与参数集。
- **协议兼容性**：
  - `DashScope API`：原生协议，功能最全，推荐用于新项目。详见 [工作流与旧版智能体应用 API](raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 和 [新版智能体应用 API 参考](raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)。
  - `Responses API`：OpenAI 兼容模式，分为同步（`/responses`）与异步（`background=true`）两种调用方式，便于复用现有 OpenAI 生态代码。详见 [同步调用 API 参考](raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) 和 [异步调用API参考](raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)。
- **多模态能力**：支持图像（`image_list` / `input_image`）与文件（`file_list` / `input_file`）输入，需在应用中配置对应模型（如通义千问 VL 系列）并发布。
- **高级功能**：包括[长期记忆](../concepts/long-term-memory.md)（`memory_id`）、RAG 检索（`rag_options`）、插件调用（`biz_params.user_defined_params`）、思考过程输出（`enable_thinking` + `has_thoughts`）等。

> **注意**：新版智能体 API 文档明确声明“仅适用于华北2（北京）地域”，而工作流与旧版智能体 API 同样标注“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 中指出 Workspace ID 在德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）等地域为必需——这表明跨地域调用能力实际存在，但部分 API 文档未同步更新地域支持范围，开发时请以控制台实际可用地域为准。

## 关键参数

| 参数名 | 类型 | 必选 | 说明 | 所属协议 |
|--------|------|------|------|----------|
| `app_id` | string | ✅ | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。URL 路径中亦需填入。 | 全部 |
| `prompt` | string | ✅（DashScope 单轮） | 用户指令文本。DashScope API 中为必填；Responses API 中由 `input` 替代。 | DashScope |
| `input` | string / array | ✅（Responses） | Responses API 的核心输入：单字符串（单轮）或消息数组（多轮/多模态）。消息支持 `system`/`user`/`assistant` 角色及 `input_text`/`input_image`/`input_file` 类型。 | Responses |
| `session_id` | string | ❌（可选） | 用于恢复对话历史。仅 DashScope API 支持；Responses API 需显式传递完整 `messages` 数组。 | DashScope |
| `messages` | array | ❌（可选，DashScope 多轮） | 替代 `prompt` + `session_id` 的多轮对话方式，含 `role` 与 `content`。 | DashScope |
| `stream` | boolean | ❌（可选） | 是否启用[流式输出](../concepts/streaming-output.md)。DashScope 需设 Header `X-DashScope-SSE: enable`；Responses 直接传 `stream=true`。 | 全部 |
| `workspace` | string | ❌（条件必选） | 子业务空间 ID。仅当应用位于子空间或调用特定地域模型时必需，通过 Header `X-DashScope-WorkSpace` 传递。详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 | DashScope |
| `biz_params` | object | ❌（可选） | 传递自定义变量、插件参数、用户级鉴权信息（`user_defined_tokens`）等。结构复杂，需严格匹配应用内配置。 | DashScope / Responses（via `extra_body`） |
| `rag_options` | object | ❌（可选） | RAG 检索配置，指定知识库（`pipeline_ids`）、文档（`file_ids`）、元数据过滤（`metadata_filter`）等。仅智能体应用支持。 | DashScope |

## 使用方式

### 1. 准备工作
- 在控制台 [应用管理](https://bailian.console.aliyun.com/#/app-center) 获取 `APP ID`；若应用在子业务空间，还需按 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 获取 `Workspace ID`。
- 通过 [密钥管理](https://bailian.console.aliyun.com/#/api-key) 获取 `DASHSCOPE_API_KEY` 并配置至环境变量。
- （可选）安装 SDK：DashScope SDK（Python/Java）或 OpenAI SDK（Python/Java），版本需满足各参数要求（如 `enable_thinking` 要求 Java SDK ≥2.20.0）。

### 2. 调用示例
- **DashScope 同步调用（新版智能体）**  
  Endpoint: `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  请求体需包含 `"input": {"prompt": "..."}`，`workspace` 通过 Header 传入。

- **Responses 同步调用（OpenAI 兼容）**  
  Endpoint: `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  请求体直接传 `"input": "..."` 或 `"input": [{"role":"user","content":"..."}]`。

- **Responses 异步调用**  
  在同步请求体中增加 `"background": true`，立即返回 `task_id`；再通过 `GET /responses/{task_id}` 轮询状态直至 `completed`。

### 3. 流式处理
- DashScope：Header 加 `X-DashScope-SSE: enable`，响应为 Server-Sent Events（SSE），需逐块解析 `data:` 字段。
- Responses：`stream=true`，响应格式与 OpenAI 一致，客户端需按 chunk 解析 `delta` 或 `content`。

## 限制和注意事项

- **地域限制**：所有文档均强调“仅适用于华北2（北京）地域”，但 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) 明确列出德国（法兰克福）等多地需 `Workspace ID`，表明实际支持跨地域。开发前务必在目标地域控制台验证应用可用性。
- **会话时效**：`session_id` 在连续 1 小时无请求后自动失效，不可复用。
- **异步约束**：Responses 异步模式不支持 `stream=true`，且 `background=true` 时 `stream` 参数会被忽略。
- **参数冲突**：DashScope API 中，若同时传 `session_id` 和 `messages`，则 `messages` 优先，`session_id` 和 `prompt` 被忽略。
- **SDK 版本强依赖**：多个参数（如 `incremental_output`, `flow_stream_mode`, `rag_options`）对 SDK 版本有最低要求（如 Python ≥2.0.1, Java ≥2.22.23），低版本将导致参数无效或报错。
- **凭证安全**：`DASHSCOPE_API_KEY` 绝不可硬编码，必须通过环境变量或密钥管理服务注入。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


