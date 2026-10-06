# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，它严格遵循 OpenAI REST API 的路径、请求/响应结构、字段命名与语义规范（如 `/v1/chat/completions`、`messages` 数组、`choices[0].message.content` 等），使开发者能直接复用主流 OpenAI SDK（Python/Node.js/Java/Go 等）和现有代码逻辑，无需重写调用逻辑即可接入百炼的多模态大模型与专用能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与多模型切换**：开发者只需将 `openai` SDK 的 `base_url` 指向百炼业务空间专属地址（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），并替换 `model` 参数（如 `"qwen3.8-max"`、`"qwen3-vl-plus"`、`"text-embedding-v4"`），即可无缝调用文本生成、视觉理解、向量嵌入、文件解析等能力，大幅降低迁移成本。  
- **统一技术栈管理**：在混合模型架构中（如同时使用 Qwen、DeepSeek、GLM、Kimi），OpenAI 兼容接口提供一致的调用范式，避免因协议差异导致的 SDK 切换与适配开销。  
- **生态工具集成**：LangChain、LlamaIndex、DSPy、Ollama 等主流 AI 工具链可原生对接（通过 `langchain_openai` 或 `openai` 客户端），支持 RAG、Agent、评估流水线等高级模式。  
- **受限场景明确边界**：该协议覆盖绝大多数文本、多模态、嵌入、文件处理类任务，但**不支持 Realtime API（实时语音流）、Qwen-Audio 专用音频模型、以及部分工具类图像模型（如 `wanx-style-repaint-v1`）**；此类能力需通过 DashScope 原生协议或独立 HTTP 接口调用。

## 关键参数和配置

- **必配项**：  
  - `base_url`：必须使用**业务空间专属域名**（格式：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），不可使用公共 `dashscope.aliyuncs.com`；地域（如 `cn-beijing`）须与 API Key 所属地域严格一致。  
  - `api_key`：配置为 `Authorization: Bearer <YOUR_API_KEY>`，推荐通过环境变量 `DASHSCOPE_API_KEY` 注入。  
  - `model`：必须为百炼文档明确列出的 OpenAI 兼容模型 ID（如 `"qwen3.8-omni-flash"`、`"qwen-image-3.0"`、`"kling-v1.0"`），大小写敏感，不支持别名或通配符。  

- **核心请求字段（与 OpenAI 官方一致）**：  
  - `messages`：对话数组，支持 `text` / `image_url` / `video_url` / `input_audio` 等多模态内容对象（具体类型依模型而定）；  
  - `response_format`：设为 `{"type": "json_object"}` 时，提示词中**必须包含 `json` 关键词**，且 `enable_thinking` 必须为 `false`；  
  - `stream`：设为 `true` 时返回 Server-Sent Events（SSE）流式响应，格式为 `data: {...}\n\n`；  
  - `max_tokens`：OpenAI 兼容接口中为**可选参数**（默认由模型自动决策），若显式设置，需确保不超过模型文档标注的最大输出长度。  

- **百炼特有扩展字段（顶层 JSON 字段，非嵌套于 `extra_body`）**：  
  - `enable_thinking`：布尔值，控制是否启用思考模式（仅对支持思考的模型如 `qwen3.8-max` 有效）；与 `response_format="json_object"` 互斥；  
  - `previous_response_id`：用于 `Responses API` 自动注入上下文，值为上一轮响应体顶层 `id` 字段；  
  - `purpose`：文件上传接口必需，取值为 `"file-extract"`（文档解析）、`"batch"`（批量任务）等。

## 面向开发者，简洁实用

- ✅ **即装即用**：`pip install -U openai` + 5 行代码即可发起首次调用（替换 `base_url` 和 `model`）；  
- ✅ **调试友好**：所有响应均含标准 `request_id`（UUID），失败时可直接用于日志查询或提工单；  
- ✅ **安全合规**：支持临时 API Key（最长 1800 秒），生产环境严禁硬编码长期 Key；  
- ⚠️ **注意避坑**：  
  - 图像生成仅 `qwen-image-3.0` 系列支持 OpenAI 兼容接口，`wan2.7-image-pro` 等万相模型需用 DashScope SDK；  
  - 视频生成虽统一走 `/v1/videos/generations`，但其 `prompt` 长度上限为 512 字符，超长将被静默截断；  
  - 多模态输入中 `image_url` 的图片需为公网可访问 URL（不支持本地路径或相对路径）；  
  - 启用 `stream=true` 时，客户端必须正确处理 SSE 流（如 Python 中使用 `response.iter_lines()`）。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)


