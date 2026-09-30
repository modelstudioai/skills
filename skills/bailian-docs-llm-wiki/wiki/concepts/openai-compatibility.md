# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 API 协议层，完全遵循 OpenAI REST API 的请求/响应格式（如 `/chat/completions`、`/embeddings`、`/reranks` 等路径）、数据结构（`messages`、`input`、`choices`、`usage`）与认证方式（`Authorization: Bearer <API_KEY>`），使开发者无需修改业务逻辑即可将现有 OpenAI SDK、LangChain 集成、Prompt 工程框架或本地开发工具快速迁移到百炼平台。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用**：支持 Qwen 全系列文本模型（`qwen3.8-max`、`qwen3.7-plus` 等）、多模态模型（`qwen3-vl-plus`、`qwen3-omni-flash`）、嵌入模型（`text-embedding-v4`、`qwen3.7-text-embedding`）及重排序模型（`qwen3-rerank`）。注意：`Qwen-Audio` 不支持 OpenAI 兼容协议，仅限 DashScope 原生接口。
- **智能体与工作流调用**：通过 `application call` 的 OpenAI 兼容 Responses API（`/apps/agent/{APP_ID}/compatible-mode/v1/responses`）同步或异步调用已发布的智能体，复用 `messages` 结构传递多轮对话与多模态输入（如 `content` 数组含 `image_url` 或 `file_list`），并支持 `biz_params` 透传自定义参数。
- **向量与排序服务**：统一使用 `/compatible-mode/v1/embeddings` 和 `/compatible-api/v1/reranks` 等路径，兼容 OpenAI Embedding/Rerank 标准字段（`input`、`model`、`query`、`documents`），便于 RAG 系统无缝集成。
- **开发工具链对接**：支持 CLI（如 ollama、curl）、IDE 插件（Cursor、Cherry Studio）、桌面客户端（Qwen APP 工作助理）及低代码平台（Dify），只需配置正确的 `base_url` 和对应套餐的 API Key 即可启用。
- **批量与异步任务**：提供 `Batch Chat`（单请求多条 [prompt](../guides/prompt.md) 同步处理）、`Batch File`（JSONL 异步批处理）和 `Embedding 批处理` 接口，均保持 OpenAI 请求体结构，仅扩展 `background=true` 或专用 endpoint 路径。

## 关键参数和配置

- **`base_url`**：必须使用地域专属兼容地址，例如  
  `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（按量计费）  
  `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（Token Plan）  
  ❗旧域名 `dashscope.aliyuncs.com` 已不推荐，且部分新功能（如 `qwen3.8-omni-flash` 音视频支持）仅在新域名下可用。
- **`model`**：严格匹配平台模型 ID，如 `qwen3.8-max`、`qwen3-vl-plus`、`text-embedding-v4`、`qwen3-rerank`；第三方模型（如 `deepseek-v4-pro`）需先在控制台开通权限。
- **`messages` / `input`**：  
  - Chat 类接口（`/chat/completions`）使用标准 `messages: [{role, content}]`，支持 `image_url`（含 `detail` 字段）等 OpenAI 多模态字段；  
  - Responses API（`/responses`）和 Application Call 使用 `input` 字段，支持 `string` 或 `array`（含 `system`/`user`/`assistant` 角色及 `content` 数组），更灵活适配多轮与多模态。
- **`stream`**：设为 `true` 启用[流式输出](streaming.md)，返回 `chat.completion.chunk`；Responses API 还支持 `stream_options={"include_usage": true}` 在流结束时返回 token 统计。
- **`previous_response_id`**：Responses API 多轮对话必需，传入上一轮响应的顶层 `id`（非 `output` 内部消息 ID），用于自动上下文管理。
- **`enable_thinking`**：Qwen3.5+ 模型启用思考模式（生成 reasoning tokens），**必须作为请求体顶层参数传入**，不可置于 `extra_body`。
- **多模态控制参数**（仅部分模型支持）：  
  `min_pixels` / `max_pixels` / `max_frames`（图像/视频分辨率与帧数限制）  
  `fps`（视频抽帧率）  
  `enable_fusion`（多模态嵌入融合向量开关）

## 面向开发者，简洁实用

- ✅ **零改造迁移**：用 OpenAI Python SDK 时，仅需替换 `client = OpenAI(base_url="...", api_key="...")`，其余代码（`client.chat.completions.create(...)`）完全不变。
- ✅ **功能增强不破兼容**：内置工具调用（`web_search`, `code_interpreter`）、显式缓存（`x-dashscope-session-cache: enable`）、结构化 JSON 输出（配合提示词或 `response_format={"type": "json_object"}`）均在标准字段内扩展，不影响旧逻辑。
- ⚠️ **注意差异点**：  
  - `temperature` 范围为 `[0, 2)`（非 OpenAI 的 `[0, 1]`），迁移时建议校准；  
  - `completions` 接口仅限华北2（北京）且仅支持 `qwen-coder-turbo`；  
  - `Qwen-Audio`、子空间专属微调模型、部分异步生成模型（如 `wan2.6-t2i`）**不支持** OpenAI 兼容协议，需切回 DashScope 原生接口。
- 📌 **调试建议**：开启 `stream_options={"include_usage": true}` 查看实际 token 消耗；对多模态请求，优先使用 `oss://` 临时 URL + `X-DashScope-OssResourceResolve: enable` 头提升稳定性。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [vector and sort](../api/vector-and-sort.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more about models](../api/more-about-models.md)


