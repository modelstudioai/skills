# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 端点，严格遵循 OpenAI REST API 的路径、请求/响应格式、参数语义与错误码规范，使开发者能直接复用现有 OpenAI SDK、LangChain 集成或业务代码，实现零代码迁移至 Qwen 系列模型及其他百炼支持能力（如 Embedding、File、Batch、Vision）。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有项目**：若你已使用 `openai` Python SDK 或其他 OpenAI 客户端，只需将 `base_url` 替换为 `https://dashscope.aliyuncs.com/api/v1/`，并传入百炼的 API Key（`sk-xxx`），即可调用 `chat/completions`、`embeddings`、`files`、`batches` 等全部兼容端点，无需修改业务逻辑。
- **[多模态](multi-modal.md)与向量能力统一接入**：除文本生成外，OpenAI 兼容接口还支持 `qwen-vl`（视觉语言）、`text-embedding-v1` 等模型，通过 `/v1/chat/completions`（带 `image_url`）或 `/v1/embeddings` 端点调用，保持协议一致性。
- **批量任务与文件协同**：通过 `/v1/files` 上传文件后，可直接在 `/v1/batches` 中引用 `file_id` 创建 Batch Chat 任务；该流程与 OpenAI 原生 Batch 接口完全一致，适合离线批量推理场景。
- **LangChain 等框架原生集成**：`langchain-community` 提供 `DashScopeChatModel` 和 `DashScopeEmbeddings` 封装类，自动适配 OpenAI 兼容协议，开箱即用，无需自定义适配器。

> ⚠️ 注意：  
> - `qwen-vl` 和 `qwen-audio` 模型**仅支持 OpenAI 兼容接口调用**（不支持 DashScope 原生接口）；  
> - OpenAI 兼容接口**不支持流式响应（`stream=true`）**，所有请求强制返回完整 JSON 响应；  
> - `functions` 字段已废弃，请统一使用 `tools` + `tool_choice`（符合 OpenAI v1.0+ 规范）。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `model` | string | 是 | 百炼平台启用的模型 ID，非 OpenAI 原生名 | `"qwen-max"`, `"qwen-plus"`, `"text-embedding-v1"` |
| `messages` | array | 是（仅 `/chat/completions`） | 对话历史，格式为 `[{ "role": "user", "content": "..." }]` | `[{"role":"user","content":"你好"}]` |
| `temperature` / `top_p` / `max_tokens` | number / integer | 否 | 语义与 OpenAI 一致，但受模型上下文限制（如 `qwen-plus` 最高 `8192`） | `0.7`, `0.9`, `1024` |
| `tools` / `tool_choice` | array / object | 否 | 工具定义与调用策略，支持[函数调用](function-calling.md)（Function Calling）语义 | `[{"type":"function","function":{"name":"get_weather","parameters":{...}}}]` |
| `response_format` | object | 否 | 仅 `qwen-max`/`qwen-plus` 支持 `{"type": "json_object"}`，需配合 system [prompt](../guides/prompt.md) 使用 | `{"type": "json_object"}` |
| `file_id` / `batch_id` | string | 是（对应端点） | 由 `/v1/files` 或 `/v1/batches` 创建后返回，用于关联资源 | `"file-abc123"`, `"batch-def456"` |

- **认证方式**：`Authorization: Bearer <your_dashscope_api_key>`（注意：不是 `sk-xxx` 开头的 OpenAI Key，而是百炼控制台生成的 DashScope API Key）  
- **Endpoint 基地址**：`https://dashscope.aliyuncs.com/api/v1/`  
- **常用端点示例**：
  - `POST /v1/chat/completions`
  - `POST /v1/embeddings`
  - `POST /v1/files`
  - `POST /v1/batches`

## 面向开发者，简洁实用

✅ **推荐做法**：  
- 使用 `dashscope` Python SDK（≥1.20.0），它自动处理多协议路由、错误重试与配额监控；  
- 若坚持用 `openai` SDK，请确保 `base_url` 正确，并检查 `model` 是否在 [模型列表](https://help.aliyun.com/zh/model-studio/list-models) 中可用；  
- 所有请求必须携带 `Content-Type: application/json`；  
- 超长 `messages`（总 token > 模型上下文）会被静默截断，建议客户端自行做长度预估（如用 `tiktoken` 计算）。

❌ **避免踩坑**：  
- 不要传 `gpt-4`、`gpt-3.5-turbo` 等 OpenAI 模型名——会返回 `404 Not Found`；  
- 不要设置 `stream=true`——服务端将忽略该参数并返回完整响应；  
- 不要混用 `functions` 和 `tools`——`functions` 已废弃，使用即报 `400 Bad Request`；  
- 文件上传请优先使用 OpenAI 兼容 `/v1/files`（而非 DashScope 原生 `/api/v1/files`），路径更统一、权限更清晰。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [file management api](../api/file-management-api.md)
- [more about models](../api/more-about-models.md)


