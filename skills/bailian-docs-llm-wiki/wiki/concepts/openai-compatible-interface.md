# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套遵循 OpenAI REST API 规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/batch` 等路径）的标准化调用方式，支持使用 OpenAI SDK（Python/Node.js 等）或原生 HTTP 请求快速接入千问（Qwen）及多家第三方大模型，实现零代码迁移与技术栈复用。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速原型与工具集成**：开发者可直接在 Postman、Cherry Studio、Cursor、Dify 等主流客户端中配置 `base_url` 和 `api_key`，调用 `/v1/chat/completions` 即可发起对话；图像/视频输入统一走 `/v1/multimodal/chat/completions`，无需修改客户端逻辑。  
- **框架嵌入**：LlamaIndex、LangChain 等生态可通过官方适配器（如 `llama-index-llms-openai`）无缝对接，只需将 `openai_api_base` 指向百炼业务空间专属域名，即可复用现有 RAG 或 Agent 流程。  
- **批量与生产级任务**：通过 `/v1/batch` 接口提交异步批量请求，或使用 `/v1/files` 上传文档供 Qwen-Long/Qwen-Doc-Turbo 推理，显著降低单次调用成本（最高降本 50%）。  
- **智能体（Agent）开发**：`/v1/responses` 是专为 Agent 场景设计的 OpenAI 兼容接口，内置 `web_search`、`web_extractor`、`code_interpreter` 等工具，并支持 `previous_response_id` 自动维护多轮上下文，比标准 Chat API 更适合复杂工作流。  
- **多模态与嵌入服务**：`/v1/chat/completions` 支持图像/视频输入（需 `qwen3-vl-plus` 等模型），`/v1/embeddings` 提供 `text-embedding-v4` 等高性能向量模型，均完全兼容 OpenAI 的请求/响应结构。

> ⚠️ 注意：并非所有百炼模型都支持 OpenAI 兼容协议。例如 `Qwen-Audio`、`qwen-deep-research` 仅支持 DashScope 原生接口；`qwen3.8-omni-flash` 的音视频能力在 Responses API 中明确支持，但在 Chat Completions API 中未声明——请以各接口文档的「支持模型列表」为准。

## 关键参数和配置

| 参数 | 类型 | 说明 | 是否必填 |
|------|------|------|-----------|
| `base_url` | string | **必须使用业务空间专属域名**：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（推荐）；旧域名 `https://dashscope.aliyuncs.com/api/v1` 仍可用但性能较低。 | 是 |
| `api_key` | string | 百炼控制台生成的 API Key，**严格按地域绑定**（如北京地域 Key 无法调用弗吉尼亚 endpoint）。 | 是 |
| `model` | string | 模型 ID，如 `"qwen3.7-plus"`、`"text-embedding-v4"`；不同接口支持范围不同（详见各接口文档）。 | 是 |
| `messages` | array | Chat 类接口核心输入，格式为 `[{"role": "user", "content": "..."}]`；多模态时 `content` 为数组，含 `text` 和 `image_url` 对象。 | 是（Chat/Responses） |
| `tools` | array | 启用[函数调用](function-calling.md)或工具调用，`qwen-max`/`qwen-plus` 支持，`qwen-turbo` 不支持；Responses API 内置工具无需显式定义。 | 否（按需） |
| `stream` | boolean | 设为 `true` 启用 SSE 流式响应，客户端需解析 `data:` 块。 | 否 |
| `temperature` / `top_p` / `max_tokens` | number / integer | 标准采样参数，默认值与 OpenAI 一致（`temperature=0.7`, `top_p=1.0`），取值范围同官方规范。 | 否 |
| `previous_response_id` | string | **仅 Responses API 必需**：传入上一轮响应的顶层 `id`（UUID），用于自动关联上下文与工具执行状态。 | 是（Responses 多轮） |
| `enable_thinking` | boolean | Batch 或 GUI 模型场景下控制是否返回思考链（`reasoning_content`），默认关闭以节省 token。 | 否（按需） |

> ✅ 提示：`min_pixels`/`max_pixels` 等图像控制参数在 OpenAI 兼容接口中完全支持（如 `qwen3.7-plus` 默认 `min_pixels=65536`），但 `max_frames`（视频帧数限制）**仅 DashScope 原生接口支持**，OpenAI 兼容接口不识别该参数。

## 面向开发者，简洁实用

- **三步接入**：① 控制台创建业务空间 → ② 获取对应地域的 API Key → ③ 将 SDK 的 `base_url` 替换为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，其余代码（包括 `messages` 构造、`tools` 声明、流式处理）**一行不用改**。  
- **调试建议**：优先使用百炼控制台「API 调试」页生成带签名的 cURL 示例；遇到 `invalid_api_key` 错误，请检查 Key 所属地域与 endpoint 地域是否一致。  
- **避坑指南**：  
  - 不要混用协议：`Qwen-Audio` 输入音频必须用 DashScope 原生 `/api/v1/asr`，不能塞进 OpenAI `messages`；  
  - 不要忽略 `previous_response_id`：Responses API 多轮对话若缺失该字段，将丢失上下文与工具状态；  
  - 不要依赖未声明能力：`qwen3.8-omni-flash` 的音视频支持仅在 Responses API 文档中列出，Chat Completions API 调用可能失败。  
- **性能提示**：专属域名（`{WorkspaceId}.{region}.maas.aliyuncs.com`）相比通用域名平均延迟降低 30%，QPS 提升 2×，**新项目务必启用**。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [frameworks](../api/frameworks.md)
- [more models](../api/more-models.md)


