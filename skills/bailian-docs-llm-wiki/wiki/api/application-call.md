# application call

`application call` 是指通过 API 方式调用阿里云百炼平台已发布的智能体（Agent）或工作流（Workflow）应用。开发者无需自行部署模型或编排逻辑，只需提供应用凭证（APP ID、可选 Workspace ID）、输入内容及必要参数，即可获得结构化响应。该能力支持同步、异步与流式三种调用模式，适用于对话交互、多步骤任务执行、文件/图像理解等多种场景。

## 支持的模型/功能

- **应用类型**：支持新版智能体应用（Agent 2.0）、旧版智能体应用及工作流应用三类，对应不同 API 接口与参数集 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) 和 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)。
- **模型能力**：底层可调用通义千问系列大语言模型（如 Qwen-Plus、Qwen-Max）、深度思考模型（需显式启用 `enable_thinking`）及通义千问 VL 系列多模态模型（支持图像理解），具体取决于应用创建时所选模型 [图像与视频理解](../../raw/model-user-guide/model-experience/vision-model/vision.md)。
- **扩展能力**：支持插件调用、RAG 知识库检索（`rag_options`）、长期记忆（`memory_id`）、自定义变量注入（`biz_params`）及多模态输入（`image_list`, `file_list`, `input_image`, `input_file`）。

> **注意**：新版智能体应用 API 与工作流/旧版智能体应用 API 在部分参数命名、默认行为及 SDK 版本要求上存在差异。例如，`messages` 参数在工作流 API 中为一级字段，而在 Responses API 的 OpenAI 兼容模式中需嵌套于 `input` 数组内；且新版智能体 API 明确要求华北2（北京）地域，而工作流 API 同样标注“仅适用于华北2（北京）地域”，但文档 1 指出 Workspace ID 在德国（法兰克福）等多地亦为必需——这表明地域限制可能随功能演进而变化，实际调用前请以控制台提示和最新 API 响应为准。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 | 来源示例 |
|--------|------|------|------|----------|
| `app_id` | string | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)中获取。HTTP 调用时需填入 URL 路径，SDK 调用时作为方法参数传入。 | [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `prompt` | string | 是（单轮） | 用户指令文本。仅用于单轮对话，若使用 `messages` 则此参数被忽略。 | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |
| `messages` | array | 是（多轮） | 消息数组，含 `system`/`user`/`assistant` 角色对象，用于多轮上下文管理。 | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |
| `input` | string/array | 是（Responses API） | OpenAI 兼容模式下的核心输入字段，可为字符串（单轮）或消息数组（多轮/多模态）。 | [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md) |
| `workspace` | string | 否（条件必填） | 业务空间 ID，调用子业务空间或特定地域（如德国、新加坡）应用时必需，通过 Header `X-DashScope-WorkSpace` 传递。 | [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md) |
| `stream` | boolean | 否 | 是否启用[流式输出](../concepts/streaming-output.md)。推荐设为 `true` 以降低超时风险；HTTP 调用需额外设置 Header `X-DashScope-SSE: enable`。 | [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) |
| `incremental_output` | boolean | 否（流式下） | [流式输出](../concepts/streaming-output.md)时是否增量返回（即后续 chunk 不重复之前内容）。仅 DashScope API 支持，Responses API 不提供此参数。 | [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md) |
| `biz_params` | object | 否 | 传递自定义变量、插件参数或用户鉴权信息的容器，结构因应用配置而异。 | [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) |

## 使用方式

- **DashScope API（原生）**  
  Endpoint：`POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`  
  适用场景：需要精细控制（如 `incremental_output`、`enable_thinking`）、调用新版智能体或工作流。支持 Python/Java SDK 及标准 HTTP。SDK 调用更简洁，HTTP 需手动构造 `input` 和 `parameters` 对象，并通过 Header 传 `X-DashScope-WorkSpace` 等元数据。

- **Responses API（OpenAI 兼容）**  
  Endpoint（同步）：`POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`  
  Endpoint（异步）：同上，请求体中添加 `"background": true`  
  适用场景：快速迁移 OpenAI 生态代码、简化多模态输入（`input` 直接支持 `input_image`/`input_file` 数组）。**注意**：异步模式不支持 `stream=true`，且 `messages` 格式与 DashScope API 不完全兼容。

- **调试与开发**  
  所有应用均支持控制台内 **应用卡片 → 发布 → API 调试** 实时测试；建议优先配置 `DASHSCOPE_API_KEY` 环境变量而非硬编码密钥；生产环境务必使用 RAM 子账号并授予最小必要权限（如 `AliyunBailianFullAccess`）。

## 限制和注意事项

- **地域与权限**：APP ID 和 Workspace ID 仅能通过控制台手动获取，不支持 API 查询 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。RAM 子账号需超级管理员权限才能查看全部业务空间列表。
- **会话与状态**：`session_id` 有效期为 1 小时无请求，超时后失效；`messages` 参数替代 `session_id` 实现上下文管理，但需每次请求携带完整历史。
- **版本与兼容性**：  
  - 新版智能体 API 要求 Java SDK ≥ 2.20.0，Python SDK ≥ 2.0.1；  
  - 工作流 API 的 `flow_stream_mode` 默认为 `full_thoughts`，但文档明确标注“**不推荐新业务使用**”，应优先选用 `message_format_plus`；  
  - Responses API 的 `background=true` 异步调用与 `stream=true` 互斥，违反将导致错误。
- **安全与合规**：API Key 严禁硬编码；文件/图片 URL 需确保公网可访问且符合阿里云内容安全策略；涉及用户隐私数据的长期记忆（`memory_id`）需明确告知并获授权。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)


