# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 协议规范（如 `v1/chat/completions`、`v1/embeddings` 等路径与请求/响应结构）的标准化模型调用入口，使开发者无需修改代码逻辑即可将现有基于 OpenAI SDK 或生态工具（如 LangChain、Postman、Dify、Cursor）的应用快速迁移到百炼平台。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一接口，而是一套按能力分层、按协议对齐的接口族，覆盖从基础推理到智能体编排的全链路场景：

- **Chat 接口**（`/v1/chat/completions`）：最常用入口，支持文本对话、多模态图文理解（如 `qwen3-vl-plus`）、第三方模型（DeepSeek、GLM、Kimi），适用于通用对话、办公助手、客服机器人等场景。
- **Responses 接口**（`/v1/responses`）：Chat 的增强演进版，内置联网搜索、网页抓取、代码解释器、知识库检索等原生工具能力；支持音视频端到端处理（`qwen3.8-omni-flash`）及更灵活的输入格式（纯字符串或消息数组），专为智能体（Agent）和应用级调用设计。
- **Completions 接口**（`/v1/completions`）：面向代码补全与 Fill-in-the-Middle（FIM）任务，当前仅支持 `qwen-coder-turbo` 模型，适用于 IDE 插件、代码生成工具等垂直场景。
- **Vision 接口**（`/v1/chat/completions` + `image_url`）：复用 Chat 路径，通过标准 OpenAI 图像消息格式（`{"type": "image_url", "image_url": {"url": "..."}}`）调用视觉模型（如 `QVQ`、`qwen3-vl-plus`），支持 OCR、图表理解、多图推理。
- **Embedding 接口**（`/v1/embeddings`）：提供文本向量化服务（如 `text-embedding-v4`），输出稠密向量，用于 RAG 召回；注意不支持稀疏向量（`output_type=sparse` 无效）。
- **Batch 接口**（`/v1/batch`）：支持批量[异步处理](asynchronous-processing.md)（JSONL 文件）或同步批量请求（Batch Chat），显著降低数据标注、评测等非实时任务成本。
- **Files 接口**（`/v1/files`）：管理文件资源，支撑文档问答（`file-extract`）、微调数据集上传（`fine-tune`）等场景。
- **Conversations 接口**（`/v1/conversations`）：实现跨设备、长时间对话的状态持久化，自动注入历史上下文，与 Responses API 协同构建有记忆的智能体体验。

> ⚠️ 注意：并非所有模型都支持全部接口。例如 `qwen3.8-omni-flash` 仅在 Responses 接口中可用；`qwen-coder-turbo` 仅支持 Completions；`Qwen-Audio` 不支持任何 OpenAI 兼容协议，必须使用 DashScope 原生接口。

## 关键参数和配置

所有 OpenAI 兼容接口共用以下核心配置项，开发者需严格遵循：

- **`base_url`**（必需）  
  必须使用业务空间专属域名：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`  
  示例：`https://wk-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`  
  ❌ 禁用旧域名（如 `https://dashscope.aliyuncs.com`），否则性能与稳定性下降。

- **`api_key`**（必需）  
  使用百炼控制台生成的 Secret Key（SK），**非 Access Key（AK）**；且严格按地域绑定（北京 AK 无法调用弗吉尼亚 endpoint）。

- **`model`**（必需）  
  值必须为控制台已开通的精确模型 ID（如 `qwen3.8-max`、`qwen3-vl-plus`、`deepseek-v4-pro`），不支持别名或旧版名称；不同接口支持的模型列表不同，请以各接口文档为准。

- **`input` / `messages`**（必需）  
  - Chat & Responses：推荐使用 `messages` 数组（含 `role`/`content`/`image_url` 等字段）；  
  - Responses 还额外支持 `input: string`（单轮纯文本）；  
  - Completions 使用 `prompt: string`；  
  - Embedding 使用 `input: string | string[]`；  
  - Vision 输入需符合 OpenAI 图像消息规范。

- **`stream`**（可选，默认 `false`）  
  设为 `true` 启用流式响应；客户端需健壮处理 `delta.content` 为空字符串的情况（尤其首 chunk）。

- **其他常用参数**  
  - `temperature`: 范围 `[0, 2)`，非 OpenAI 官方 `[0, 1]`，迁移时需校准；  
  - `max_tokens`: 对多数模型限制回复长度，但对 `qwen3.8-max` 等大模型可能包含思考过程总长；  
  - `stream_options`: 如 `{"include_usage": true}` 可在流式结束帧返回 token 统计。

## 面向开发者，简洁实用

- ✅ **开箱即用**：直接使用 OpenAI Python SDK、curl 或 Postman，只需替换 `base_url` 和 `api_key`，无需重写逻辑。  
- ✅ **工具友好**：完美兼容 Dify、LangChain、LlamaIndex、Cursor、Hermes Agent 等主流框架与客户端。  
- ✅ **多模态统一**：同一接口路径（`chat/completions`）支持文本、图像、视频（via `qwen3.8-omni-flash` in Responses）混合输入。  
- ⚠️ **避坑提示**：  
  - 不支持 `function calling`（tools schema），工具调用需通过 [prompt](../guides/prompt.md) 工程或 Responses 内置工具实现；  
  - 单次 `messages` 总 token 上限为 32768，超限返回 `400 Bad Request`；  
  - 多模态请求中 `image_url` 必须公开可访问且响应头含 `Content-Type: image/*`；  
  - 流式响应中 `finish_reason` 可能出现在非最后一 chunk，客户端应以 `delta.content` 是否为空判断内容结束。  

立即开始：开通模型 → 获取 WorkspaceId 和地域 API Key → 配置 `base_url` → 发起标准 OpenAI 格式请求。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [application call](../api/application-call.md)
- [vector and sort](../api/vector-and-sort.md)


