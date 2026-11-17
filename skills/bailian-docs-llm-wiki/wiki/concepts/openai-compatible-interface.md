# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI SDK、LangChain 集成、[Prompt 工程](prompt-engineering.md)工具链和业务代码，仅需替换 `base_url` 和模型名即可快速接入百炼的 Qwen 系列模型及专用模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **文本与多模态生成**：通过 `chat/completions` 接口调用 `qwen4-max`、`qwen3.8-plus`、`qwen3-vl-plus`（需注意：实际仅 Anthropic 或 DashScope 协议支持该模型，OpenAI Chat Completions 不支持）等模型，兼容 `messages` 数组、`image_url` 视觉输入、`function calling` 等核心能力。  
- **智能体（Agent）开发**：通过 `agents/chat/completions` 接口调用专属 Agent 模型（如 `qwen-plus-agents-202409`），完全复用 OpenAI 的 `tools`、`tool_choice`、`session_id` 等字段，实现工具调用、状态持久化与环境隔离。  
- **向量嵌入**：通过 `/v1/embeddings` 接口调用 `text-embedding-v4` 等模型，支持 `input`、`model`、`encoding_format`（仅 `float` 有效，`sparse` 不支持）等标准参数。  
- **文件处理**：通过 `/v1/files`（上传）、`/v1/batches`（异步批量）、`/v1/conversations`（会话管理）等路径，复用 OpenAI 文件生态工作流；`purpose` 字段（如 `file-extract`、`batch`）用于指定用途。  
- **专用模型调用**：意图识别（`tongyi-intent-detect-v3`）、OCR（`qwen3.5-ocr`）、GUI 自动化（`gui-plus-*`）等模型均支持 OpenAI 兼容接口，模型特有参数（如 `translation_options`、`min_pixels`）通过 `extra_body`（Python SDK）或顶层 JSON 字段（curl/Node.js）传入。  
- **框架集成**：原生适配 LangChain 的 `langchain_openai` 模块，零代码修改即可切换后端为百炼；也支持 LlamaIndex、DSPy 等主流框架。

> ⚠️ 注意：`Qwen-Audio`、`qwen-deep-research` 不支持 OpenAI 兼容接口，必须使用 DashScope 原生协议；`qwen3-vl-plus` 在 OpenAI Chat Completions 中不可用（文档已明确排除），请优先选用 Anthropic Messages 或 DashScope 协议。

## 关键参数和配置

| 参数 | 说明 | 示例值 | 注意事项 |
|------|------|--------|----------|
| `base_url` | **必须配置**，使用业务空间专属域名（推荐） | `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 旧域名 `dashscope.aliyuncs.com` 已不推荐，性能与稳定性较低；必须与 `api_key` 地域一致。 |
| `api_key` | 百炼平台生成的密钥，按地域绑定 | `sk-xxx` | 北京 key 无法调用弗吉尼亚 endpoint，否则返回 `invalid_api_key`。 |
| `model` | **必须精确匹配**，区分协议支持范围 | `"qwen4-max"`, `"text-embedding-v4"`, `"qwen-plus-agents-202409"` | `qwen3-vl-plus`、`Qwen-Audio`、`qwen-deep-research` 等不支持；Agent 场景必须用 `-agents-` 后缀专用模型。 |
| `messages` / `input` | 输入结构依接口类型而定 | `[{ "role": "user", "content": "..." }]`（Chat）；`"string"` 或 `[{...}]`（Responses） | Responses API 使用 `input` 字段而非 `messages`；OCR/Vision 场景需在 `content` 数组中使用 `type: "image_url"`。 |
| `extra_body`（Python SDK） | 传递非标准但必需的模型参数 | `{"min_pixels": 1024, "max_pixels": 8388608}` | Python 中必须用此参数传 `translation_options`、`enable_thinking`、`vl_high_resolution_images` 等；Node.js/curl 中直接置于 JSON body 顶层。 |
| `purpose`（File/Batch） | 指定文件或批量任务用途 | `"file-extract"`, `"batch"`, `"fine-tune"` | 必须显式声明，否则文件无法被下游服务识别；不同 purpose 有独立大小限制（如 `file-extract` ≤ 150 MB）。 |
| `session_id`（Agents/Conversations） | 显式管理会话上下文 | `"sess_abc123"` | 不传则自动生成；Agents Session 默认 24 小时过期，需主动续期。 |

## 面向开发者，简洁实用

- ✅ **快速迁移**：只需改三处——`base_url`（用专属域名）、`api_key`（确保地域匹配）、`model`（查文档选支持型号），其余代码（包括 `stream=True`、`functions` 定义、LangChain Chain）无需修改。  
- ✅ **调试建议**：  
  - 首选 `curl` 或 Postman 验证基础调用，确认 `base_url` 和 `model` 正确；  
  - Python 开发者用 `openai==1.45.0+`，传参时善用 `extra_body`；  
  - Node.js 开发者将扩展参数（如 `min_pixels`）直接写入 JSON body 顶层，勿嵌套。  
- ❌ **避坑提醒**：  
  - 不要对 `qwen3-vl-plus` 使用 `/v1/chat/completions` —— 会返回 404 或模型不支持错误；  
  - 不要对 Agents API 设置 `stream=True` —— 直接报 `400 Bad Request`；  
  - 不要混用 `api_key` 地域 —— 错误码是 `invalid_api_key`，不是权限错误。  
- 📦 **生产推荐**：  
  - 所有新项目统一使用 `compatible-mode/v1` 路径；  
  - 文件类场景优先用 OpenAI 兼容 File 接口（支持多地域），弃用原生 `/api/v1/files`；  
  - Agent、Batch、Embedding 等高价值场景，务必启用业务空间专属域名以保障 SLA。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [file management api](../api/file-management-api.md)
- [more models](../api/more-models.md)


