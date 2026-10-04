# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/chat/completions`、`messages` 数组、`tools` 工具调用等），使开发者可直接复用现有 OpenAI SDK（Python/Node.js/Java/Go）、LangChain、LlamaIndex 等生态工具，零代码改造即可接入百炼的 Qwen 系列及第三方直供模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与原型验证**：已有基于 OpenAI SDK 的应用（如聊天机器人、Agent 工作流）可仅通过修改 `base_url` 和 `model` 参数，立即调用百炼的 `qwen3.8-max`、`qwen3-vl-plus` 等模型，无需重写业务逻辑。
- **多模态开发**：通过 OpenAI Vision 兼容接口（`messages` 中含 `image_url` 或 `video_url`），调用 `qwen3-vl-plus` 实现图像理解、OCR；视频理解需配合 `fps` 和 `max_frames` 参数（注意：`max_frames` 在 OpenAI 兼容 API 中不可自定义，由服务端固定）。
- **增强型智能体（Agent）构建**：使用 `/v1/responses` 端点（非标准 `/chat/completions`），启用内置工具（`web_search`、`code_interpreter`）或自定义 function 工具，并通过 `previous_response_id` 自动管理多轮上下文，显著简化 Agent 状态维护。
- **批量与长文档处理**：利用 OpenAI 兼容的 Batch 接口（文件批量 / Batch Chat）执行高吞吐评测；结合 OpenAI 文件接口（`/files` + `purpose=file-extract`）上传 PDF/DOCX，交由 `Qwen-Doc-Turbo` 自动解析与问答。
- **嵌入与检索集成**：调用 `/embeddings` 端点，使用 `text-embedding-v4` 等模型生成向量，无缝对接 LangChain 的 `OpenAIEmbeddings` 或 LlamaIndex 的 `OpenAIEmbedding` 类，用于 RAG 场景。

> ⚠️ 注意：`qwen-audio`、`qwen-ocr` 等专用模型**不支持 OpenAI 兼容协议**，必须使用 DashScope 原生接口；第三方模型（如 `deepseek-v4-pro`）仅在华北2（北京）地域可用，且需在控制台开通权限。

## 关键参数和配置

| 参数 | 说明 | 必填 | 示例值 | 注意事项 |
|------|------|------|--------|----------|
| `base_url` | OpenAI 兼容接口根地址，**必须使用业务空间专属域名** | 是 | `https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 旧域名 `dashscope.aliyuncs.com` 已不推荐；[Token](token.md) Plan/Coding Plan 有独立 Base URL（见计费方案文档） |
| `model` | 模型 ID，**必须为百炼控制台模型市场中的官方名称** | 是 | `"qwen3.7-plus"`, `"qwen3-vl-plus"`, `"text-embedding-v4"` | 不支持 Hugging Face 格式（如 `Qwen/Qwen3-7B`）；第三方模型名需与控制台开通一致（如 `"deepseek-v4-pro"`） |
| `messages` | 对话消息数组，格式为 `[{"role": "user", "content": "..."}]` | `/chat/completions` 是；`/responses` 可选（支持更灵活 `input`） | `[{"role":"user","content":"解释量子纠缠"}]` | 纯文本模型（如 `qwen3-max`）的 `content` **必须为字符串**，禁止传数组；多模态模型支持 `image_url`/`video_url` 等类型 |
| `tools` | 启用工具调用（仅 `/responses` 支持） | 否 | `[{"type": "web_search"}]` | 支持内置工具（`web_search`, `code_interpreter`）和自定义 function 工具 |
| `previous_response_id` | 多轮对话状态 ID（仅 `/responses`） | 否（多轮时必填） | `"resp_abc123..."` | 必须传入上一轮响应的顶层 `id` 字段（UUID），**不是 `output` 内消息的 `id`** |
| `enable_thinking` | 控制是否启用模型深度思考模式 | 否（`qwen3.5+` 默认开启） | `true` / `false` | 开启时需同时设 `stream=true`, `incremental_output=true`, `result_format="message"`；与 `response_format={"type": "json_object"}` 互斥 |
| `response_format` | 强制 JSON 结构化输出 | 否 | `{"type": "json_object"}` | 需关闭 `enable_thinking`；OpenAI Java SDK <4.0.0 不原生支持，建议用 DashScope SDK 或升级 SDK |

## 面向开发者，简洁实用

- ✅ **立刻上手**：安装 `openai` SDK（Python）或对应语言客户端，设置 `OPENAI_API_KEY`（实际为百炼 API Key）和 `OPENAI_BASE_URL`（业务空间专属地址），一行代码调用：
  ```python
  from openai import OpenAI
  client = OpenAI(api_key="sk-xxx", base_url="https://your-workspace.cn-beijing.maas.aliyuncs.com/compatible-mode/v1")
  response = client.chat.completions.create(model="qwen3.7-plus", messages=[{"role":"user","content":"你好"}])
  ```
- ✅ **调试优先**：遇到报错（如 `401 Unauthorized`、`429 RateLimited`），先检查 `base_url` 与 API Key 是否同属一个计费方案（[Token](token.md) Plan/Coding Plan/按量）且地域一致；粘贴错误码至 DashScope SDK CLI（`dashscope` 命令）自动诊断。
- ✅ **避坑指南**：
  - 不要硬编码 API Key —— 使用环境变量 `DASHSCOPE_API_KEY`；
  - 流式响应务必设 `stream=True`，并按 SSE 格式解析（非普通 JSON）；
  - 图像输入优先用 `image_url`（公网可访问 URL），避免 Base64 导致请求过大；
  - 第三方模型仅限华北2，且需控制台手动开通；
  - `qwen-audio`、`wan2.6-t2i` 等非文本模型**不在此兼容范围内**，请查对应原生接口文档。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [frameworks](../api/frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


