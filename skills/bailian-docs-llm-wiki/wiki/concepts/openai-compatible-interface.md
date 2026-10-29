# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，完全遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/chat/completions`、`/embeddings`、`/files` 等端点），使开发者可复用现有 OpenAI SDK（Python/Node.js/Java/Go 等）和业务代码，仅需替换 `base_url`、`api_key` 和 `model` 即可无缝接入百炼全栈模型能力。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移与多模型统一调用**：无需重写逻辑，同一套 OpenAI SDK 代码可同时调用文本（`qwen3.8-max`）、多模态（`qwen3-vl-plus`）、向量（`text-embedding-v4`）、重排（`qwen3-rerank`）、图像生成（`qwen-image-3.0-pro`）等不同能力模型，仅需切换 `model` 参数。
- **框架集成**：LlamaIndex、Spring AI Alibaba 等主流框架通过配置 `api_base` 指向百炼兼容地址，即可原生支持百炼模型，无需定制适配器。
- **开发工具链对接**：Cursor、WorkBuddy、Hermes Agent、Qwen Code 等 CLI/IDE/桌面客户端，只需填入百炼的 `base_url`（含 `{WorkspaceId}`）和对应 API Key，即可直接使用 OpenAI 协议完成对话、编码、RAG 等任务。
- **高性能推理加速**：Prime 模式、吞吐预留（PTU/DTU）、智能路由、批量推理（Batch Chat）等加速能力均基于 OpenAI 兼容接口暴露，调用方式与标准 API 完全一致，仅需指定专用 `model` ID（如 `glm-5.3-prime` 或 `auto-model-xxxxxx`）。
- **垂直场景扩展**：意图识别（`tongyi-intent-detect-v3`）、机器翻译（`qwen-mt-plus`）、GUI 自动化（`gui-plus`）等专用模型，只要支持 OpenAI 协议，即统一走 `/chat/completions` 流程，保持接口一致性；但需注意：`qwen-deep-research`、`qwen-audio` 等模型**明确不支持**该协议，必须使用 DashScope 原生 SDK。

## 关键参数和配置

- **`base_url`（必需）**  
  格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`（推荐）或旧版 `https://dashscope.aliyuncs.com/compatible-mode/v1`（不推荐）。  
  ✅ 正确示例（北京地域）：`https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`  
  ❌ 错误：跨地域混用（如北京 Key 调用新加坡域名）、遗漏 `{WorkspaceId}` 占位符、使用未启用兼容模式的域名。

- **`api_key`（必需）**  
  必须为与 `base_url` 同地域、同业务空间创建的专属 Key。各地域 Key 独立，不可复用；生产环境建议使用临时 Key（最长 1800 秒）。

- **`model`（必需）**  
  严格匹配模型市场中的 ID（区分大小写，无前后缀），例如：  
  - 文本：`qwen3.7-plus`、`glm-5.3-prime`  
  - 多模态：`qwen3-vl-plus`  
  - 向量：`text-embedding-v4`  
  - 重排：`qwen3-rerank`  
  - 图像：`qwen-image-3.0-pro`  
  ⚠️ 不支持开源社区命名（如 `Qwen/Qwen3.7-Plus`）或自定义别名。

- **协议级关键参数（按接口类型）**  
  - `/chat/completions`：`messages`（数组，支持 `text`/`image_url`/`video_url`）、`stream`（流式必开）、`enable_thinking`（Qwen3.7+ 思考模式开关）、`response_format={"type": "json_object"}`（结构化输出时需禁用思考）。  
  - `/embeddings`：`input`（字符串或字符串数组）、`dimensions`（可选，指定向量维度）、`encoding_format`（`float` 或 `base64`）。  
  - `/files`：`purpose`（必填，取值 `file-extract`/`batch`/`fine-tune`）。  
  - `/responses`（增强型 Agent 接口）：`input`（支持 string/array）、`previous_response_id`（多轮续写）、`stream_options={"include_usage": true}`（返回 token 统计）。

## 面向开发者，简洁实用

- ✅ **立即上手**：安装任一 OpenAI SDK（如 `pip install openai`），初始化 client 时传入百炼 `base_url` 和 `api_key`，其余代码零修改。  
- ✅ **调试优先**：所有兼容接口均返回标准 OpenAI 格式响应（含 `id`, `object`, `created`, `choices[0].message.content` 等字段），日志、监控、错误处理可复用原有逻辑。  
- ✅ **流式友好**：`stream=True` 时，`delta.content` 逐块返回，与 OpenAI 行为完全一致；思考模式下还会返回 `delta.reasoning_content`（需显式启用）。  
- ⚠️ **避坑提示**：  
  - 不要混用地域——Key、`base_url`、Workspace ID 必须同属一个地域（北京/新加坡/弗吉尼亚等）；  
  - 不要硬编码 Key——务必通过环境变量 `DASHSCOPE_API_KEY` 配置；  
  - 不要忽略模型限制——`qwen-audio`、`qwen-deep-research` 等模型不支持此协议，查文档确认再调用；  
  - 优先使用业务空间专属域名（`{WorkspaceId}.xxx.maas.aliyuncs.com`），性能与稳定性显著优于旧域名。

## 关联主题页

- [preparations](../api/preparations.md)
- [frameworks](../api/frameworks.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [image generation](../api/image-generation.md)
- [video generation api](../api/video-generation-api.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [vector and sort](../api/vector-and-sort.md)
- [more models](../api/more-models.md)


