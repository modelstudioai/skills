# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议，完全遵循 OpenAI RESTful 接口规范（包括请求结构、响应格式、错误码体系及流式传输机制），使开发者能复用现有 OpenAI 生态工具（如 `openai` SDK、LangChain、LlamaIndex 等）无缝接入百炼模型服务，无需修改业务逻辑代码。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口是百炼面向主流开发者的**首选集成方式**，覆盖全栈能力与多样化部署形态：

- **通用模型调用**：支持文本生成（`qwen3.8-max`、`qwen3.7-plus`）、多模态理解（`qwen3-vl-plus`、`qwen3.8-omni-flash`）、向量嵌入（`text-embedding-v4`、`qwen3.7-text-embedding`）、重排序（`qwen3-rerank`）等，统一通过 `/compatible-mode/v1/...` 路径接入。
- **智能体与工具调用**：
  - `chat/completions` 支持标准 `functions` + `function_call` 协议；
  - `responses` 接口（`/responses`）内置联网搜索、网页抓取、代码解释器等原生工具，支持 `previous_response_id` 实现多轮上下文延续。
- **高性能推理场景**：
  - Prime 模式（如 `glm-5.2-fast-preview`）、吞吐预留（TPM）、PTU/DTU 专属部署、智能路由（`auto-model-xxxx`）均通过 OpenAI 兼容接口调用，仅需替换 `model` 参数即可启用加速能力。
- **批量与异步任务**：
  - 批量推理（Batch）支持 JSONL 文件上传，兼容 OpenAI 风格的 `input` 字段；
  - 向量嵌入支持同步（`/embeddings`）与异步（需额外 Header）两种模式。
- **会话管理**：`conversations` 接口提供跨设备上下文同步能力，与 `responses` 配合实现无状态长对话。

> ⚠️ 注意：部分专用模型**不支持** OpenAI 兼容接口，例如 `qwen-deep-research`（仅 DashScope Python SDK）、`Qwen-Audio`（仅 DashScope 原生协议）。调用前请确认模型文档中的协议支持说明。

## 关键参数和配置

| 参数 | 类型 | 必填 | 说明 | 示例值 |
|------|------|------|------|--------|
| `base_url` | string | ✅ | **必须匹配 API Key 所属地域**，推荐使用业务空间专属域名：<br>`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>（如 `https://abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`） | `https://abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | string | ✅ | 使用环境变量 `DASHSCOPE_API_KEY` 配置，**不可硬编码**；Key 与 `base_url` 地域必须一致 | `sk-xxx` |
| `model` | string | ✅ | 严格匹配控制台模型市场名称（区分大小写），不可使用开源 ID（如 `Qwen/Qwen3.7-Plus`） | `"qwen3.8-max"`, `"text-embedding-v4"`, `"qwen3-rerank"` |
| `messages` | array | ✅（Chat） | 标准 OpenAI 消息数组，`role` 为 `"system"`/`"user"`/`"assistant"`，`content` 类型依模型而异：<br>- 纯文本模型：字符串<br>- 多模态模型：对象数组（含 `text`/`image_url`/`video_url`） | `[{"role":"user","content":"你好"}]` |
| `input` | string/array | ✅（Embedding/Rerank/Responses） | 向量/重排序/Responses 接口专用输入字段，支持字符串、字符串数组或结构化对象 | `"hello world"` 或 `["doc1", "doc2"]` |
| `stream` | boolean | ❌（默认 `false`） | 启用流式响应；部分模型（如思考模式模型）要求 `true` | `true` |
| `temperature` / `top_p` | number | ❌（默认 `0.7` / `1.0`） | 采样参数，范围：`temperature ∈ [0.0, 2.0)`，`top_p ∈ (0.0, 1.0]` | `0.5`, `0.9` |
| `enable_thinking` | boolean | ⚠️按模型要求 | 控制深度思考模式（影响 token 计费与输出结构），部分模型（如 `qwen3.7-plus`）强制为 `true`；**必须置于请求 body 顶层** | `true` |
| `previous_response_id` | string | ❌（Responses） | 多轮对话关联 ID，传入上一轮响应的 `id` 字段（UUID 格式） | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |
| `dimensions` | integer | ❌（Embedding） | 指定向量维度（仅 `text-embedding-v4`/`qwen3.7-text-embedding` 等支持），常见值：`1024`, `2048` | `1024` |

> 💡 提示：  
> - 所有 OpenAI 兼容接口均返回标准 OpenAI 格式响应（含 `id`, `object`, `created`, `choices`, `usage`），便于日志解析与监控。  
> - 错误响应严格遵循 OpenAI 错误结构（`error.type`, `error.message`, `error.code`），如 `invalid_api_key`、`invalid_parameter`、`rate_limit_exceeded`。  
> - 流式响应使用 `text/event-stream` MIME type，每行以 `data:` 开头，末尾空行分隔；最终数据块含 `{"object":"chat.completion.chunk","choices":[{"delta":{},"finish_reason":"stop"}]}`。

## 面向开发者，简洁实用

- ✅ **快速上手**：只需 3 步  
  1. 控制台获取 `WorkspaceId` 和 `DASHSCOPE_API_KEY`；  
  2. 设置 `base_url = https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；  
  3. 用 `openai` SDK 调用（Python 示例）：
  ```python
  from openai import OpenAI
  client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url=base_url)
  response = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[{"role": "user", "content": "你好"}],
      stream=True
  )
  ```

- ✅ **平滑迁移**：  
  - 替换 `openai.base_url` 和 `openai.api_key` 即可从 OpenAI 切换至百炼；  
  - LangChain 中只需修改 `ChatOpenAI(base_url=..., api_key=...)`；  
  - 不依赖百炼特有参数时，零代码改造。

- ⚠️ **避坑指南**：  
  - `base_url` 地域 ≠ `api_key` 地域 → `401 invalid_api_key`；  
  - `model` 名称大小写错误或使用开源 ID → `404 model_not_found`；  
  - 多模态模型传入字符串 `content`（非数组）→ `400 invalid_request_error`；  
  - 思考模式模型未设 `stream=true` → `400 invalid_parameter`；  
  - 向量/重排序接口误用 `messages` 字段 → `400 invalid_request_error`。

- 📦 **SDK 推荐**：  
  - Python：`openai>=1.0.0`（官方 SDK）或 `dashscope>=2.0.1`（同时支持 OpenAI/DashScope 协议）；  
  - Java/Node.js/Go：使用对应语言的 `openai` 官方 SDK，无需百炼定制版。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [vector and sort](../api/vector-and-sort.md)
- [more models](../api/more-models.md)


