# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，通过复用 OpenAI RESTful 接口规范（如 `/v1/chat/completions`、`/v1/embeddings` 等），使开发者无需修改现有代码即可调用百炼托管的 Qwen 系列模型、Embedding 模型、Rerank 模型及多模态能力。该接口本质是 DashScope 底层能力的语义映射层，不依赖 OpenAI 服务，完全运行于阿里云基础设施。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用**：支持 `chat/completions`（文本对话）、`completions`（补全）、`embeddings`（向量生成）、`reranks`（重排序）、`vision`（图像理解）等核心端点，覆盖 `qwen3.8-max`、`qwen3-vl-plus`、`text-embedding-v4`、`qwen3-rerank` 等主流模型；Qwen-Audio 和 QwQ 模型除外（仅支持 DashScope 原生协议）。
- **工具与框架集成**：可直接用于 LangChain（通过 `BailianLLM` / `BailianEmbeddings`）、LlamaIndex、Hermes Agent、Cursor、Dify 等工具——只需将 `OPENAI_BASE_URL` 指向百炼兼容地址，并传入 DashScope API Key。
- **客户端接入**：支持 Postman、cURL、VS Code 插件等通用开发工具；不同计费方案（[Token](token.md) Plan、Coding Plan、按量计费）对应独立 Base URL，需严格匹配。
- **应用调用**：智能体（Agent）和工作流（Workflow）可通过 OpenAI 兼容的 Responses API（`/compatible-mode/v1/responses`）调用，支持 `input_image`、`input_file`、`previous_response_id` 等扩展字段，实现多轮上下文管理与多模态输入。
- **批量处理**：`batches` 端点支持 JSONL 格式批量请求（如批量 embedding），但暂不支持 `conversations` 类型任务。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必须设置为对应方案的兼容地址：<br>• 按量计费：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>• [Token](token.md) Plan：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>• Coding Plan：`https://coding.dashscope.aliyuncs.com/v1` | `{WorkspaceId}` 和 `{region}` 需从控制台获取并替换；地域必须与[模型部署](model-deployment.md)地一致（如华北2）。 |
| `api_key` | 使用 DashScope API Key（`sk-xxx`），**非 OpenAI Key**；不同计费方案 Key 不互通。 | [Token](token.md) Plan/Coding Plan 的 Key 仅在对应 Base URL 下有效，混用返回 401。 |
| `model` | 必填，值为百炼平台发布的模型 ID，如 `qwen3.8-max`、`text-embedding-v4`、`qwen3-rerank`。不支持 `gpt-3.5-turbo` 等 OpenAI 原生名。 | 模型名中的 `.` 在部分工具（如 Cursor）中需替换为 `-`（如 `glm-5.3` → `glm-5-3`）。 |
| `stream` | 控制是否流式响应，默认 `false`；`chat/completions` 支持，但 `completions` 等非 Chat 端点暂不生效。 | 流式响应默认启用（工具包层面），但实际行为以接口文档为准。 |
| `messages` | OpenAI 标准格式数组，含 `role`（`system`/`user`/`assistant`）和 `content`；`system` 消息在 QwQ/QVQ 模型中无效。 | 多模态输入需在 `content` 中嵌入 `image_url` 或 `input_image` 字段（非 base64 图片需带 `data:image/xxx;base64,` 前缀）。 |
| `input`（Responses API） | 替代 `messages`，支持字符串或结构化数组（含 `input_text`、`input_image`、`input_file`）。 | 与 `previous_response_id` 配合可构建无状态多轮对话。 |

## 面向开发者，简洁实用

- ✅ **开箱即用**：安装 `openai>=1.40.0`，设置环境变量 `OPENAI_API_KEY`（DashScope Key）和 `OPENAI_BASE_URL`，即可复用原有 OpenAI SDK 代码。
- ✅ **功能对齐但有边界**：支持 `temperature`、`top_p`、`max_tokens` 等常用参数，语义一致；但**不支持 `functions` / `tools` [函数调用](function-calling.md)**，也**不返回 OpenAI 的限流 Header**（如 `x-ratelimit-*`），请以 DashScope 控制台配额为准。
- ⚠️ **注意兼容性例外**：
  - Vision 接口仅兼容 Qwen-VL 系列，不支持 `gpt-4o` 图像格式；
  - Embedding 最大输入长度为 8192 tokens，超长自动截断（无警告）；
  - `conversations` 接口需显式传 `session_id`，且 session 生命周期为 24 小时；
  - 所有 OpenAI 兼容接口均**不支持缓存控制头（如 `Cache-Control`）**，上下文管理依赖 `previous_response_id` 或 `session_id`。
- 🔗 **调试建议**：优先使用 `curl -v` 查看完整请求/响应；遇到 401 错误，请核验 Key 与 Base URL 方案是否匹配；遇到 400，请检查模型名、`image_url` 格式、JSONL 文件 schema 是否符合文档要求。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)
- [application call](../api/application-call.md)


