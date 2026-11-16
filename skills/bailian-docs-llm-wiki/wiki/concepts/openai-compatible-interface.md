# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 API 协议实现，严格遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与错误码规范，使开发者能复用现有 OpenAI SDK（Python/Node.js/Java/Go）和业务代码，仅需替换 `base_url` 和 `api_key` 即可快速接入百炼的 Qwen 及第三方模型服务，实现零逻辑改造迁移。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一接口，而是覆盖多类能力的协议族，在百炼中按功能分层使用：

- **标准对话生成**：通过 `/chat/completions` 接口调用 `qwen-plus`、`qwen4-max`、`deepseek-v4.1-flash` 等文本模型，支持 `messages` 数组输入、`stream` 流式响应、`tool_choice` 工具调用（部分模型），适用于通用聊天、Agent 编排等场景。  
- **智能体原生响应（Responses API）**：通过 `/responses` 接口调用 `qwen4-max` 等增强型模型，内置联网搜索、代码解释器、网页抓取等工具，并支持 `previous_response_id` 自动关联上下文、`x-dashscope-session-cache` 启用会话级缓存，适合构建免维护状态的 AI 应用。  
- **向量嵌入（Embeddings）**：通过 `/embeddings` 接口调用 `text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3-vl-embedding` 等模型，支持 `dimensions` 指定向量维度、`encoding_format` 控制输出格式（`float` 或 `base64`），用于 RAG、语义检索等场景。  
- **文本翻译（MT）**：仅 `qwen-mt-plus` 支持 OpenAI 兼容调用，通过 `chat.completions.create()` 提交 `messages` + `extra_body={"translation_options": {...}}`，实现术语干预、领域提示等企业级能力；`qwen-mt-uni` 和 `qwen-mt-image-*` 等多模态翻译模型**不支持** OpenAI 兼容协议，须使用 DashScope 原生接口。  
- **排序（Rerank）**：`qwen3-rerank` 和 `qwen3.7-text-rerank` 支持 `/rerank` 接口，接受 `query` 与 `documents` 数组，支持 `instruct` 自定义排序任务；注意 `gte-rerank` 系列模型**已下线且不支持** OpenAI 兼容方式。  

> ⚠️ 关键限制：  
> - `qwen-audio`（语音模型）**完全不支持** OpenAI 兼容协议，必须使用 DashScope 原生 API；  
> - 第三方直供模型（DeepSeek/Kimi/GLM/MiniMax）**仅限华北2（北京）地域可用**，且需在控制台手动开通服务；  
> - 子业务空间中微调部署的专属模型（如 `qwen-plus-finetuned`）**不支持** OpenAI 兼容调用，仅限 DashScope 原生协议。

## 关键参数和配置

| 参数 | 是否必填 | 说明 | 示例值 | 注意事项 |
|------|----------|------|--------|----------|
| `base_url` | ✅ | 业务空间专属域名（推荐）或通用兼容域名 | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>`https://dashscope.aliyuncs.com/compatible-mode/v1` | **必须显式配置**；推荐使用 WorkspaceId 专属域名以保障性能与隔离性；不同地域 endpoint 不互通（北京 Key 不能调用新加坡 endpoint） |
| `api_key` | ✅ | 百炼平台生成的 API Key | `sk-xxx` | **严格按地域绑定**；需从对应地域控制台获取；前端不可硬编码，应通过后端签发临时 Key（`expire_in_seconds ≤ 1800`） |
| `model` | ✅ | 模型 ID，需与所选接口能力严格匹配 | `qwen4-max`, `text-embedding-v4`, `qwen3-vl-plus`, `qwen3-rerank` | 不同接口支持的模型范围不同（如 Responses API 支持 `qwen4-max`，但 Chat Completions 不支持 `qwen-mt-plus`）；拼写错误将返回 `model_not_supported` |
| `stream` | ❌ | 启用流式响应 | `True` | 配合 `stream_options={"include_usage": True}` 可在流式末尾获取 token 统计 |
| `previous_response_id` | ❌（仅 Responses API） | 上一轮响应的顶层 `id`，用于自动注入上下文 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` | 仅 `/responses` 接口有效；无需手动管理 messages 历史 |
| `enable_thinking` | ❌（混合思考模型专用） | 显式开关深度思考（如 `qwen3.8-max`） | `false` | 必须作为 JSONL 请求体中 `body` 的顶层字段（与 `model` 同级），置于 `extra_body` 中将被忽略 |
| `dimensions` | ❌（Embedding 专用） | 指定向量维度 | `1024`, `2048` | `text-embedding-v4` 支持 `512`/`1024`/`2048`；`qwen3-vl-embedding` 支持 `1024`/`2048`；`multimodal-embedding-v1` 固定 1024 维，不支持该参数 |
| `instruct` | ❌（Rerank 专用） | 自定义排序任务指令 | `"Retrieve semantically similar text."` | 影响相关性打分逻辑；未指定则按默认问答检索任务执行 |

## 面向开发者，简洁实用

- ✅ **快速上手**：只需 3 行代码初始化 OpenAI 客户端，其余调用方式与官方 SDK 完全一致：
  ```python
  from openai import OpenAI
  client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                  base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
  # 后续调用无差异：client.chat.completions.create(...), client.embeddings.create(...)
  ```

- ✅ **平滑迁移**：  
  - 所有 OpenAI SDK 方法（`chat.completions`, `embeddings`, `rerank`, `files`, `responses`）均可用；  
  - 错误响应格式（`error.type`, `error.message`, `error.code`）与 OpenAI 一致，便于统一错误处理；  
  - HTTP 状态码语义对齐（如 `429` 表示限流，`400` 表示参数错误）。

- ⚠️ **避坑提醒**：  
  - `temperature` 范围为 `[0, 2)`，非 OpenAI 的 `[0, 1]`，迁移时需校准；  
  - `max_tokens` 含义因模型而异：对 `qwen4-max`，它限制“回复 + 思考过程”总长度；对 `qwen-plus`，仅限制回复内容；  
  - 多模态输入格式需严格匹配协议：Chat Completions 使用 `{"type": "image_url", "image_url": {"url": "...", "detail": "high"}}`，不支持 `video_url` 抽帧控制（`max_frames` 仅 DashScope 支持）；  
  - `qwen-mt-plus` 翻译需将参数封装在 `extra_body={"translation_options": {...}}` 中，不可直接放在 `messages` 或顶层 body。

- 🚀 **生产建议**：  
  - 高并发场景务必复用 `OpenAI` 客户端实例（避免每次新建）；  
  - 对延迟敏感的 Embedding/Rerank 场景，优先选用同步接口（单次 ≤20 条）；  
  - 长耗时任务（如多模态翻译、视频理解）请改用 DashScope 原生异步接口，OpenAI 兼容协议不覆盖此类能力。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [more about models](../api/more-about-models.md)


