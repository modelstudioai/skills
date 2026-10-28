# application call

`application call` 是阿里云百炼平台提供的核心能力，用于通过 API 同步或异步调用已发布的智能体（Agent）或工作流（Workflow）应用。它支持 OpenAI 兼容的 Responses API 和原生 DashScope API 两种调用范式，覆盖文本、图像、文件等多模态输入，并提供[流式输出](../concepts/streaming-output.md)、[长期记忆](../concepts/long-term-memory.md)、RAG 检索等高级功能。开发者需结合应用类型（新版智能体、旧版智能体或工作流）、部署地域及业务空间配置，选择合适的接口与参数组合。

## 支持的模型/功能

- **应用类型适配**：  
  - 新版智能体（Agent 2.0）：使用 [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)，支持 `session_id` 对话状态管理、`memory_id` [长期记忆](../concepts/long-term-memory.md)、`enable_thinking` 深度思考模式等专属能力。  
  - 旧版智能体与工作流：统一使用 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)，支持 `messages` 多轮上下文、`biz_params` 自定义参数传递、`rag_options` 知识库检索及 `flow_stream_mode` 工作流节点级流式控制。  
  - OpenAI 兼容模式：通过 [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md) 提供 `input`（含 `messages` 数组）、`stream`、`background` 等标准字段，便于迁移现有 OpenAI 生态代码。

- **多模态能力**：  
  - 图像理解：需选用通义千问 VL 系列模型，并在应用中正确配置（如工作流节点入参设为 `imageList`，智能体设为“自定义处理”）；API 层通过 `image_list`（DashScope）或 `content` 中 `input_image`（Responses）传入 URL 或 Data URL。  
  - 文件问答：仅智能体应用支持，需在应用内启用“全文引用”或“切片检索”，API 层通过 `file_list`（DashScope）或 `input_file`（Responses）传入文件 URL。  
  > **注意**：文档 4 与文档 7 对图像/文件支持范围的描述存在不一致——文档 4 明确限定“仅智能体应用支持文件传入”，而文档 7 在 `file_list` 参数说明中同样标注“仅智能体应用支持”，但其 `image_list` 描述未排除工作流；实际以文档 7 的 [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md) 为准：工作流支持图像（需 VL 模型 + `imageList` 配置），但**不支持文件输入**。

## 关键参数

| 参数名 | 所属 API | 必选 | 说明 | 注意事项 |
|--------|----------|------|------|----------|
| `app_id` | 全部 | 是 | 应用唯一标识，在[应用管理](https://bailian.console.aliyun.com/#/app-center)页面获取。 | 通过 HTTP 调用时需嵌入 URL 路径（如 `/apps/{APP_ID}/completion`），SDK 调用则作为独立参数传入。 |
| `workspace` / `X-DashScope-WorkSpace` | DashScope API | 否（子空间必需） | 业务空间 ID，调用子业务空间或德国（法兰克福）、华北2（北京）、新加坡、中国香港、日本（东京）地域模型时必须提供。 | 获取方式详见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)。 |
| `prompt` | DashScope API | 是（旧版/工作流） | 单轮文本指令。 | 与 `messages` 互斥；若同时提供，`messages` 优先级更高。 |
| `messages` | DashScope API | 否（替代 [prompt](../guides/prompt.md)） | 多轮对话消息数组，含 `system`/`user`/`assistant` 角色。 | 使用该参数要求 Python SDK ≥2.0.1，Java SDK ≥2.17.0。 |
| `input` | Responses API | 是 | OpenAI 兼容输入，可为字符串或 `messages` 数组。 | 当前不支持基于 `pre_response_id` 或 `conversation_id` 的上下文续写，需每次传递完整历史。 |
| `stream` | 全部 | 否 | 是否启用[流式输出](../concepts/streaming-output.md)。DashScope 默认 `false`，Responses 默认 `false`。 | 工作流应用需在控制台目标节点（结束/流程输出）开启“[流式输出](../concepts/streaming-output.md)”开关并重新发布；异步调用（`background=true`）**不支持流式**。 |
| `background` | Responses API | 否 | 是否异步执行（返回任务 ID）。 | 仅 Responses API 支持，DashScope API 无此参数；设置为 `true` 时 `stream` 必须为 `false`。 |
| `biz_params` | DashScope API | 否 | 传递自定义变量、插件参数或用户鉴权信息。 | 工作流应用直接传 `{"city": "杭州"}`；智能体应用需按 `user_prompt_params`/`user_defined_params` 结构组织。 |

## 使用方式

- **API 终端选择**：  
  - **DashScope API**（推荐用于新项目）：Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v1/apps/{APP_ID}/completion`，功能最全，性能更优，支持深度思考、RAG、[长期记忆](../concepts/long-term-memory.md)等高级特性。  
  - **Responses API**（OpenAI 兼容）：Endpoint 为 `POST https://dashscope.aliyuncs.com/api/v2/apps/agent/{APP_ID}/compatible-mode/v1/responses`，适用于快速集成或已有 OpenAI 代码库迁移。  

- **认证与环境**：  
  - 必须配置有效的 `DASHSCOPE_API_KEY`（通过[密钥管理](https://bailian.console.aliyun.com/?tab=app#/api-key)获取），建议通过环境变量而非硬编码传递。  
  - 地域限制：所有文档均明确标注“仅适用于华北2（北京）地域”，其他地域（如德国、新加坡）调用需额外提供 `Workspace ID` 并确认 Base URL 正确性（参见 [Regions](../../raw/model-user-guide/get-started-with-models/regions.md)）。  

- **典型调用流程**：  
  1. **同步调用**（实时响应）：构造请求体，设置 `prompt` 或 `input`，可选 `stream=true` 实现流式渲染。  
  2. **异步调用**（长任务）：在 Responses API 中设置 `background=true`，获取 `task_id` 后调用 `GET /responses/{task_id}` 轮询状态，直至 `status` 为 `completed`/`failed`/`cancelled`。  
  3. **调试验证**：通过控制台“应用卡片 → 发布 → API 调试”页面进行免代码测试，快速验证参数与配置。

## 限制和注意事项

- **地域与 Workspace 强约束**：调用子业务空间应用或非华北2地域模型时，`Workspace ID` 为必填项，且必须与 Base URL 中的地域标识一致；遗漏将导致 `403 Forbidden` 或 `404 Not Found` 错误。  
- **SDK 版本依赖**：多项功能有严格版本要求，例如 `messages` 参数需 Python SDK ≥2.0.1，`flow_stream_mode` 需 Java SDK ≥2.22.23，`enable_thinking` 需 Java SDK ≥2.20.0 —— 低版本 SDK 将忽略参数或报错。  
- **参数冲突与互斥**：  
  > **注意**：`prompt` 与 `messages` 在 DashScope API 中互斥；`stream` 与 `background` 在 Responses API 中互斥（`background=true` 时 `stream` 会被强制忽略）；`session_id` 与 `messages` 同时存在时，`messages` 优先级更高，`session_id` 被忽略。  
- **凭证获取限制**：APP ID 和 Workspace ID **仅支持控制台手动获取**，不提供 API 或 CLI 查询接口（参见 [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)）。  
- **异步任务管理**：Responses API 的异步任务不支持取消操作，仅能通过轮询等待终态；任务结果默认保留 24 小时，超时后无法查询。

## 来源文档

- [获取APP ID和Workspace ID](../../raw/application-api-reference/application-call/obtain-the-app-id-and-workspace-id.md)
- [DashScope API](../../raw/application-api-reference/application-call/application-dashscope-api-reference.md)
- [Responses API](../../raw/application-api-reference/application-call/openai-responses-api.md)
- [同步调用 API 参考](../../raw/application-api-reference/application-call/openai-responses-api/synchronous-call-api-reference.md)
- [异步调用API参考](../../raw/application-api-reference/application-call/openai-responses-api/asynchronous-call-api-reference.md)
- [新版智能体应用 API 参考](../../raw/_short/new-agent-application-api-reference-d745b325d97fcf2e.md)
- [工作流与旧版智能体应用 API](../../raw/_short/agent-and-workflow-application-api-reference-81f0d3ecfd878b1f.md)


