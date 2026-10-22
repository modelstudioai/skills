# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议，完全遵循 OpenAI REST API 的路径、请求/响应格式、参数命名与语义规范（如 `/v1/chat/completions`），使开发者无需修改业务代码即可将现有 OpenAI 应用无缝迁移至百炼，调用 Qwen 及其他主流大模型。

## 在百炼平台的不同场景中如何使用

- **标准对话交互**：通过 `POST /compatible-mode/v1/chat/completions` 调用文本生成模型（如 `qwen3.8-max`、`glm-5.3`、`deepseek-v4-pro`），支持 `messages` 数组、`stream` 流式、`function_call` 工具调用及 `stream_options={"include_usage": true}` 等完整 OpenAI 语义。适用于 Cursor、Qwen Code、Dify、LangChain 等所有兼容 OpenAI SDK 的工具链。

- **智能体（Agent）开发**：通过 `POST /compatible-mode/v1/responses` 使用百炼增强型 Agent 接口。除兼容基础对话外，原生支持联网搜索、网页抓取、代码解释器、文搜图、图搜图、知识库检索等内置工具；通过 `previous_response_id` 实现多轮上下文自动串联，配合 `Conversations` 接口可跨设备持久化管理长周期会话。

- **多模态理解与生成**：通过 `POST /compatible-mode/v1/chat/completions` 调用视觉模型（如 `qwen3-vl-plus`、`QVQ`），输入格式严格兼容 OpenAI 多模态消息结构（`{"type": "text", "text": "..."}` + `{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}`）。注意：`QVQ` 仅支持[流式输出](streaming-output.md)。

- **向量化与排序**：通过 `POST /compatible-mode/v1/embeddings`（文本嵌入）和 `POST /compatible-mode/v1/rerank`（重排序）调用对应能力，支持 `text-embedding-v4`、`qwen3.7-text-embedding`、`qwen3-rerank` 等模型。注意：多模态嵌入（如 `qwen3-vl-embedding`）和部分高级 rerank 模型（如 `qwen3-vl-rerank`）**不支持 OpenAI 兼容接口**，需使用 DashScope 原生协议。

- **批量处理**：通过 `POST /compatible-mode/v1/batch` 提交 JSONL 文件进行异步批量推理，支持文本、多模态（`qwen3-vl-plus`）及向量（`text-embedding-v4`）任务；`Batch Chat` 则提供同步阻塞式批量调用，单请求最大上下文达 256K tokens。

> ⚠️ 不支持场景：`Qwen-Audio`、`qwen3-vl-embedding`、`tongyi-embedding-vision-plus-2026-03-06` 等非文本生成类模型**不可通过 OpenAI 兼容接口调用**，必须使用 DashScope 原生 API。

## 关键参数和配置

- **必配认证与路由**：
  - `Authorization: Bearer <API_KEY>` 或 `x-api-key` 请求头（API Key 严格按计费方案与地域绑定，北京 Key 不可用于弗吉尼亚 endpoint）。
  - `base_url` 必须设为业务空间专属域名：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（如 `https://my-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）。旧域名 `dashscope.aliyuncs.com` 已不推荐，性能与稳定性较低。

- **核心参数**：
  - `model`：必填，精确匹配文档所列模型 ID（区分大小写，如 `qwen3.8-max`，不可写作 `qwen38max`）。
  - `messages`：标准对话必需，数组格式；`responses` 接口也支持更灵活的 `input` 字符串或结构化对象。
  - `stream`：布尔值，启用流式响应（默认 `false`）。

- **协议特有参数**：
  - `responses` 接口：`previous_response_id`（传上一轮响应顶层 `id`，UUID 格式）、`tools`（内置或自定义工具列表）、`reasoning.effort`（控制思考强度）、`store`（是否持久化该响应供后续引用）。
  - `chat/completions`：`enable_thinking`（Qwen3 系列模型需显式开启 R1 深度推理，否则返回 400）。
  - `batch` 接口：`enable_thinking` 必须置于 JSONL `body` 顶层，不可嵌套在 `extra_body` 中。
  - `embeddings` / `rerank`：`dimensions`（指定向量维度）、`instruct`（rerank 任务指令）、`encoding_format`（`"float"` 或 `"base64"`）。

## 面向开发者提示

- ✅ 优先使用 `compatible-mode/v1` 路径 + 业务空间专属域名，这是百炼 OpenAI 兼容接口的唯一稳定入口。
- ✅ SDK 调用推荐 `openai>=1.0.0`：初始化时设置 `api_key` 和 `base_url`，直接调用 `client.chat.completions.create()` 等方法；LangChain 用户建议选用 `ChatTongyi`（全模型兼容）而非 `ChatOpenAI`（部分模型受限）。
- ✅ 模型选型前务必查阅各接口支持的模型列表——Vision 接口不能用 `qwen3.8-max`，Embedding 接口不能用 `qwen3-vl-plus`。
- ❌ 避免混用计费方案 Key：[Token](token.md) Plan、Coding Plan、按量计费的 API Key 互不通用，且必须与 `base_url` 地域一致。
- ❌ 不要尝试用 OpenAI 兼容接口调用 `Qwen-Audio`、`qwen3-vl-embedding` 等模型，会返回明确错误（如 `model_not_supported_for_openai_compatible_protocol`）。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)


