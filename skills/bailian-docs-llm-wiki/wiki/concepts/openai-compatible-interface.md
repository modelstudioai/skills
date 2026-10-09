# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/v1/chat/completions`），使开发者可直接复用现有 OpenAI SDK（Python/Node.js/Java/Go 等）和代码逻辑，零改造接入百炼的 Qwen 系列及第三方模型服务。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与多模型切换**：已有基于 OpenAI SDK 的应用（如 LangChain、LlamaIndex、Dify、Cursor、Hermes Agent 等），只需替换 `base_url` 和 `model` 参数，即可调用百炼的 `qwen3.8-max`、`glm-5.3`、`deepseek-v4-pro` 等数十种文本模型，无需重写业务代码。  
- **多模态统一接入**：通过 `chat/completions` 接口，支持图像（`image_url`）、视频（`video_url`）、文档（`file_id`）等多模态输入（需模型支持，如 `qwen3.8-omni-flash`），保持与 OpenAI Vision API 一致的 content 数组结构。  
- **向量与排序能力集成**：`/embeddings` 和 `/rerank` 端点完全兼容 OpenAI 格式，可直接用于 RAG 流程中的向量化与重排环节，支持 `qwen3.7-text-embedding`、`qwen3-rerank` 等模型。  
- **翻译与专业任务**：`qwen-mt-plus` 文本翻译模型通过 `chat/completions` 调用，将翻译控制参数（如 `source_lang`、`target_lang`、术语表）置于 `extra_body.translation_options` 中，复用 OpenAI 请求体结构。  
- **批量与异步处理**：`batch` 接口（文件式/同步式）和 `responses`（智能体原生接口）均挂载在 `/compatible-mode/v1/` 下，支持标准 OpenAI SDK 的 batch 提交与流式响应解析。  
- **限制说明**：不支持 OpenAI 兼容协议的模型（如 `qwen-audio`、`qwen-ocr`、实时语音 `Realtime API`）需使用 DashScope 原生 SDK 或 AOQ SDK；部分高级能力（如 `enable_thinking`）在 `chat/completions` 中无效，仅对 `batch` 或 `responses` 接口生效。

## 关键参数和配置

- **Base URL（必需）**：  
  推荐使用业务空间专属域名：  
  `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`  
  （`{WorkspaceId}` 从控制台「业务空间详情」获取，`{region}` 如 `cn-beijing`）  
  旧域名 `https://dashscope.aliyuncs.com/compatible-mode/v1` 仍可用，但性能与稳定性较低。

- **API Key（必需）**：  
  必须使用与计费方案和地域匹配的密钥：  
  - 按量计费：`sk-xxx`（支持全部能力）  
  - [Token](token.md) Plan：`tp-xxx`（仅限文本生成，不支持多模态）  
  - Coding Plan：`cp-xxx`（不支持思考模式与 R1 格式）  
  配置为环境变量 `DASHSCOPE_API_KEY`，禁止硬编码。

- **Model（必需）**：  
  使用百炼控制台开通的**精确模型 ID**（如 `qwen3.8-max`、`qwen3.7-text-embedding`），区分大小写；不可使用开源命名（如 `Qwen/Qwen3-8B`）。不同接口支持范围不同：  
  - `chat/completions`：支持 Qwen、DeepSeek、Kimi、GLM 等主流文本/多模态模型  
  - `completions`：仅限 `qwen-coder-turbo`  
  - `responses`：仅限 `qwen3.x-*`、`deepseek-v4-*` 等指定型号  

- **Stream（推荐启用）**：  
  多数视觉/音频/思考模型强制要求 `stream=true`（如 `qwen-vl-plus`、`qwen3.8-omni-flash`），否则返回错误。流式响应末尾可通过 `stream_options={"include_usage": true}` 获取 token 统计。

- **扩展参数（按需传入）**：  
  - `extra_body`：用于传递 OpenAI 协议未定义但百炼特有参数，如：  
    - `translation_options`（`qwen-mt-plus`）  
    - `enable_thinking`（仅 `batch` / `responses` 接口有效）  
    - `fps` / `total_pixels`（视频理解）  
    - `instruct`（Rerank 任务指令）  
  - 所有数值参数需满足约束：`temperature ∈ [0.0, 2.0)`，`top_p ∈ (0.0, 1.0]`，`max_tokens ∈ [1, 模型上限]`。

> ⚠️ 注意：`system` 消息在 `QwQ` 模型中无效；`qwen-audio` 明确不支持 OpenAI 兼容协议；`Realtime API` 必须使用 AOQ SDK。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [vector and sort](../api/vector-and-sort.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


