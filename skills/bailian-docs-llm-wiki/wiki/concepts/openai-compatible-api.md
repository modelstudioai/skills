# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI RESTful 接口规范（包括路径、请求/响应结构、错误码、流式响应格式等），使开发者无需修改业务逻辑代码，仅通过切换 `base_url`、`api_key` 和 `model` 参数，即可将现有 OpenAI 应用无缝迁移至百炼平台。

## 在百炼平台的不同场景中如何使用

- **快速迁移已有应用**：适用于已集成 OpenAI SDK（如 `openai>=1.0.0`）的 Python/Node.js/Java/Go 等项目。只需将 `client = OpenAI(base_url="https://api.openai.com/v1", ...)` 替换为百炼专属域名（如 `base_url="https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"`），其余调用方式完全一致。
  
- **文本生成与多轮对话**：使用 `/v1/chat/completions` 接口，支持全部主流 Qwen 文本模型（如 `qwen3.8-max`、`qwen3.5-flash`）、视觉语言模型（`qwen3-vl-plus`）及第三方直供模型（DeepSeek、Kimi 等）。图像/视频输入需按 OpenAI Vision 规范组织 `messages`（含 `image_url` 或 `image_url.data` 字段）。

- **智能体（Agent）构建**：使用 `/v1/responses` 接口，专为工具调用、联网搜索、代码执行等复杂推理场景优化。支持 `previous_response_id` 自动继承上下文，并内置 `tool_choice`、`reasoning.effort` 等 Agent 专用参数。当前仅 `qwen3.8-max`、`qwen3.7-plus`、`deepseek-v4.1-flash-1017` 等直供模型完整支持全量 Agent 能力。

- **向量嵌入与语义排序**：  
  - 向量服务（`/v1/embeddings`）支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型，兼容 `input`（字符串或数组）、`dimensions`、`encoding_format` 等标准参数；**注意：不支持稀疏向量输出（`output_type=sparse` 将返回空 embedding）**。  
  - 排序服务（`/v1/rerank`）仅 `qwen3-rerank` 和 `qwen3.7-text-rerank` 提供 OpenAI 兼容接口，接受扁平化 `query` + `documents` 结构，无需嵌套 `input`。

- **专业翻译任务**：`qwen-mt-plus`（纯文本翻译）可通过 `/v1/chat/completions` 调用，使用 `extra_body={"translation_options": {...}}` 传入 `source_lang`、`target_lang`、`terms` 等参数；而图像/文档/音视频等多模态翻译需使用 DashScope 原生接口，**不走 OpenAI 兼容路径**。

> ⚠️ 重要限制：`Qwen-Audio`、`Qwen-Omni`（部分能力）、`Qwen-MT-Image`、`Qwen-MT-Uni` 及所有排序/向量的异步批处理接口均**不支持 OpenAI 兼容协议**，必须使用 DashScope 原生 API。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填，必须使用业务空间专属域名：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>（推荐地域：`cn-beijing`、`ap-southeast-1`、`ap-hongkong`） | ❌ 禁用旧域名 `https://dashscope.aliyuncs.com`（性能与稳定性无保障） |
| `model` | 必填，模型 ID 需严格匹配支持列表：<br>• Chat：`qwen3.8-omni-flash`, `qwen3-vl-plus`, `text-embedding-v4`<br>• Responses：仅限直供 Agent 模型（如 `qwen3.7-plus`）<br>• Embeddings：`qwen3.7-text-embedding`, `qwen3-rerank` | 模型能力因协议而异，例如 `qwen3.8-omni-flash` 支持音视频输入（Chat），但 `qwen3.7-plus` 在 Responses 中才启用 Agent 工具链 |
| `messages`（Chat） / `input`（Responses） | Chat 要求标准 `[{role, content}]` 数组；Responses 支持字符串或扩展 `EasyInputMessage` 结构 | 图像/视频需在 `content` 中按 OpenAI Vision 格式嵌入 `image_url` 或 `image_url.data`（Base64） |
| `previous_response_id`（Responses） | 多轮 Agent 对话必需，值为上一轮响应顶层 `id` 字段（UUID 格式） | ✅ 不是 `output[0].id`，而是响应 JSON 的根级 `"id": "xxx"` |
| `tool_choice`（Responses） | 控制工具调用策略：`"auto"`（默认）、`"none"`、`"required"` 或 `{"type": "tool", "name": "web_search"}` | Anthropic 协议使用对象形式，此处为字符串或对象，语义一致 |
| `reasoning.effort`（Responses） | 思考强度控制：`"none"` / `"low"` / `"high"` | Anthropic 协议对应 `output_config.effort`（`low`/`medium`/`high`/`max`），二者不可混用 |
| `min_pixels` / `max_pixels`（Chat & DashScope） | 图像/视频帧缩放阈值，影响分辨率与 Token 消耗 | `qwen3.8-omni-flash` 默认 `24576`；`qwen3.5/3.6/3.7` 默认 `65536`；Responses API 不暴露此参数 |
| `extra_body`（通用） | 用于传递 OpenAI 标准字段外的百炼扩展参数，如：<br>• `qwen-mt-plus`: `{"translation_options": {"source_lang":"zh","target_lang":"en","terms":[...]}}`<br>• Batch 场景: `{"enable_thinking": false}`（必须为 body 顶层字段） | ❌ `enable_thinking` 若置于 `extra_body` 内将被忽略 |

## 面向开发者的实用提示

- ✅ **首选 SDK 方式**：直接使用官方 OpenAI SDK（v1.x），无需引入额外依赖。LangChain 用户可优先尝试 `langchain_openai`，若遇模型不兼容再切换至 `langchain-community` + `dashscope`。
- ✅ **调试建议**：开启 `stream=True` 查看流式响应格式是否符合预期；检查响应头 `x-request-id` 便于问题定位；使用 `curl -v` 验证 `base_url` 和认证头。
- ✅ **错误处理**：百炼复用 OpenAI 错误码（如 `400 Bad Request`, `429 Rate Limit Exceeded`, `500 Internal Server Error`），但 `error.message` 中会包含百炼特有提示（如“模型不支持该协议”）。
- ❌ **避坑清单**：
  - 不要对 `qwen-mt-image-*` 或 `qwen3.8-audio` 使用 OpenAI 兼容接口；
  - `previous_response_id` 必须取自上一轮响应的根级 `id`，而非 `output` 内消息的 `id`；
  - `enable_thinking`、`purpose` 等扩展参数必须作为 `body` 顶层字段，不可包裹在 `extra_body` 中；
  - `fps`（视频抽帧频率）和 `min_pixels` 等媒体参数仅在 Chat/DashScope 协议生效，Responses 不支持。

如需完整支持列表、各模型能力矩阵或 HTTP 请求示例，请参考对应模型的 API 参考文档。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)
- [vector and sort](../api/vector-and-sort.md)


