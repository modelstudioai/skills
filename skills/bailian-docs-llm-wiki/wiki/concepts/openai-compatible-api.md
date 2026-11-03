# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 HTTP API 协议，完全遵循 OpenAI 的 RESTful 设计规范（如 `/v1/chat/completions`、`/v1/embeddings` 等路径）与请求/响应结构（`messages`、`model`、`stream` 等字段），使开发者能直接复用 OpenAI SDK（Python/Node.js/Java/Go/C#）或现有代码逻辑，零改造接入百炼托管的[多模态](multi-modal.md)大模型与第三方模型。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一 API，而是一组按能力分层的协议族，在不同业务场景中承担明确角色：

- **基础文本生成与对话**：通过 `chat.completions.create()` 调用 `qwen3.8-max`、`deepseek-v4-pro-0813` 等文本模型，支持 `system`/`user`/`assistant` 多轮消息、[流式输出](streaming-output.md)、结构化 JSON 输出（`response_format={"type": "json_object"}`）等标准能力。  
- **智能体（Agent）任务**：使用 `responses.create()` 接口，自动集成联网搜索、网页抓取、代码解释器等内置工具，当前仅支持 `qwen3.8-max`、`qwen3.7-plus` 及部分 DeepSeek/GLM/Kimi 模型。  
- **[多模态](multi-modal.md)理解**：在 `chat.completions.create()` 中传入含 `image_url` 或 `video_url` 的 `content` 数组，调用 `qwen3-vl-plus`、`qwen3.8-omni-flash` 等模型实现图文/音视频联合推理。  
- **[向量嵌入](vector-embedding.md)与重排序**：通过 `embeddings.create()` 和 `rerank.create()` 调用 `qwen3.7-text-embedding-flash`、`qwen3.7-text-rerank`，参数 `dimensions` 可选，语种覆盖 201 种。  
- **批量处理与文件分析**：使用 `batches.create()` 提交 JSONL 文件进行异步批量推理；或通过 `files.create(purpose="file-extract")` 上传 PDF/Word 等文档，再由 Responses API 自动解析内容。  
- **对话生命周期管理**：通过 `conversations.create()` / `conversations.messages.append()` 统一管理长期会话状态，配合 Responses API 实现跨设备上下文延续。  

> ⚠️ 注意：Qwen-Audio 系列语音模型（ASR/TTS/S2S）**不支持 OpenAI 兼容协议**，必须使用 DashScope 原生 API；所有 OpenAI 兼容接口均需通过业务空间专属域名调用，旧版 `dashscope.aliyuncs.com` 不推荐使用。

## 关键参数和配置

| 参数 | 类型 | 说明 | 示例值 | 生效范围 |
|------|------|------|--------|----------|
| `base_url` | string | **必须配置**，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`，地域需与 API Key 严格匹配 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 全局（客户端初始化时） |
| `model` | string | **必填**，模型 ID 必须与[官方模型列表](../../raw/model-user-guide/get-started-with-models/models.md)完全一致（大小写敏感、无空格） | `qwen3.7-plus`, `qwen3-vl-plus`, `text-embedding-v4` | 所有接口 |
| `messages` | array | Chat Completions 标准输入，每项含 `role`（`user`/`system`/`assistant`）和 `content`（字符串或含 `type: "image_url"` 的数组） | `[{"role":"user","content":[{"type":"image_url","image_url":{"url":"https://..."}},{"type":"text","text":"描述这张图"}]}]` | `chat.completions` |
| `input` | string/array | Responses API 输入，支持纯文本或结构化数组（含 `input_text`/`input_image`/`input_file`） | `"总结这份财报"` 或 `[{"role":"user","content":"分析图表","input_image":"https://..." }]` | `responses.create` |
| `stream` | boolean | 启用流式响应（SSE），多数模型支持；`qwen-audio-3.1-realtime-plus` 等实时模型**强制要求 `true`** | `true` | 全局 |
| `enable_thinking` | boolean | 开启深度思考链，需配合 `stream=true` 和 `incremental_output=true`；Batch 场景下必须置于 JSONL `body` 顶层 | `true` | Qwen3.5+、DeepSeek v4 等支持模型 |
| `response_format` | object | 结构化输出，仅支持 `{"type": "json_object"}`，且提示词中需含 `json` 关键词 | `{"type": "json_object"}` | `chat.completions` |
| `dimensions` | integer | [向量嵌入](vector-embedding.md)维度（Embeddings API 专用），可选 `256`/`1024`/`2048` 等 | `1024` | `embeddings.create` |

## 面向开发者，简洁实用

- ✅ **快速上手**：只需两行代码初始化 OpenAI 客户端，替换 `base_url` 和环境变量 `DASHSCOPE_API_KEY` 即可调用：
  ```python
  from openai import OpenAI
  client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://ws-xxx.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  )
  ```
- ✅ **平滑迁移**：99% 的 OpenAI SDK 调用方式（如 `client.chat.completions.create`）可直接复用，仅需检查 `model` 名称是否在[百炼支持列表](../../raw/model-user-guide/get-started-with-models/models.md)中。
- ✅ **错误排查优先看三点**：  
  ① `base_url` 地域是否与 API Key 所属地域一致（北京 Key ≠ 弗吉尼亚 URL）；  
  ② `model` 字符串是否完全匹配（`qwen3.7-plus` ≠ `Qwen3.7-Plus`）；  
  ③ 非文本模型（如 Audio）是否误用了 OpenAI 接口——请改用 DashScope 原生 API。
- ✅ **性能优化建议**：高吞吐场景优先选用 `qwen3.8-flash` 或 Prime 模式模型（如 `glm-5.3-prime`）；长上下文任务确保 `max_tokens` 不超模型上限（如 `qwen3.7-plus` 为 256K）。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [application call](../api/application-call.md)


