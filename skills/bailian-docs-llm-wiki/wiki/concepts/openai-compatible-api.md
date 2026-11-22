# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API 协议层，严格遵循 OpenAI 官方 API 的路径、请求/响应格式、参数命名与语义规范，使开发者能复用现有 OpenAI SDK（如 `openai>=1.0.0`）、LangChain 集成、Prompt 工程实践及 Agent 框架，无需重写核心逻辑即可快速接入百炼的千问（Qwen）系列及第三方模型服务。

## 在百炼平台的不同场景中，这个概念如何使用

OpenAI 兼容接口不是单一 API，而是一组按能力分层、协议对齐、模型适配的接口集合，覆盖从基础对话到智能体编排的全栈场景：

- **标准对话（Chat）**：通过 `/compatible-mode/v1/chat/completions` 调用，支持 `messages` 数组、`system` 角色、[多模态](multi-modal.md)输入（图像/视频/音频），适用于通用 LLM 应用、客服机器人、内容生成等。注意：`Qwen-Audio` 不支持此协议，仅限 DashScope 原生调用。

- **智能体原生交互（Responses）**：通过 `/compatible-mode/v1/responses` 提供增强型 Agent 能力，内置联网搜索、代码解释器、知识库检索等工具链，支持 `previous_response_id` 多轮串联与 `x-dashscope-session-cache: enable` 自动会话缓存，适合构建复杂工作流和自主 Agent。

- **专用智能体（Agents API）**：通过 `/api/v1/agents/chat/completions`（独立 endpoint）提供完整生命周期管理，支持 Session 持久化、Environment 隔离执行、Vault 安全凭证注入，专用于生产级 AI Agent 开发；仅兼容 `qwen-plus-agent-v1` 等 Agent 专用模型。

- **向量嵌入（Embeddings）**：通过 `/compatible-mode/v1/embeddings` 支持 `text-embedding-v4`、`qwen3.7-text-embedding` 等模型，与 OpenAI `embeddings.create()` 完全一致，可直接替换 `text-embedding-ada-002` 进行语义检索与 RAG 构建。

- **文件处理（Files）**：通过 `/compatible-mode/v1/files` 支持文档上传与解析（`purpose="file-extract"`），配合 `qwen-long` 或 `qwen-doc-turbo` 实现结构化数据提取，行为与 OpenAI 文件 API 对齐。

- **图像生成（Image Generation）**：千问图像模型（如 `qwen-image-3.0-pro`）支持 OpenAI 兼容模式，只需切换 `base_url` 和 `model` 即可复用 `openai.Image.create()` 调用方式，但万相、可灵、Vidu 等模型仍需使用 DashScope 原生协议。

- **框架集成**：LlamaIndex（`llamaindex-qwen`）、Spring AI Alibaba 等框架通过封装 OpenAI 兼容层实现“零改造”迁移，自动处理 token 续期、重试、错误码映射等运维细节。

## 关键参数和配置

所有 OpenAI 兼容接口共享以下关键配置项，开发者必须显式设置：

- **`base_url`（必需）**：必须使用业务空间专属域名，格式为  
  `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`（华北2）或对应地域域名。  
  ⚠️ 旧域名 `dashscope.aliyuncs.com` 已不推荐，性能与稳定性无保障。

- **`api_key`（必需）**：百炼平台生成的 API Key，**严格按地域绑定**（北京 Key 不能调用弗吉尼亚 endpoint），错误码 `invalid_api_key` 通常表示地域不匹配。

- **`model`（必需）**：模型 ID，不同接口支持范围不同：
  - Chat/Embeddings：支持广泛模型（`qwen4-max`, `deepseek-v4-pro`, `text-embedding-v4` 等）；
  - Responses：仅限明确列出的商业版模型（如 `qwen4-max`, `qwen3.8-flash`）；
  - Agents：仅限 `qwen-plus-agent-v1` 等 Agent 专用模型；
  - Files：仅限 `qwen-long`, `qwen-doc-turbo`。

- **核心请求参数（依接口而异）**：
  - `messages`：Chat/Responses/Agents 接口必填，格式为 OpenAI 标准数组（含 `role`/`content`/`tool_calls`）；
  - `tools` + `tool_choice`：Agents/Responses 中启用工具调用的必需字段；
  - `session_id`：Agents/Responses 中指定会话上下文，用于状态保持；
  - `enable_thinking`：Batch 场景下控制是否开启深度推理（影响 `reasoning_tokens` 成本）；
  - `x-dashscope-session-cache`：Header 字段，设为 `enable` 启用 Responses 接口的自动会话缓存。

- **[多模态](multi-modal.md)特有参数**：
  - 图像：`image_url.url` + `detail`（精度），`detail` 必须嵌套在 `image_url` 对象内；
  - 视频：`video_url.url`，不支持 OpenAI 兼容层自定义 `max_frames`（需用 DashScope 原生）；
  - 注意：`Qwen-Audio` 明确不支持 OpenAI 兼容协议。

## 面向开发者，简洁实用

✅ **快速上手三步走**：  
1. 获取业务空间 ID 和 API Key（控制台 → API 密钥管理）；  
2. 设置 `base_url = "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"`；  
3. 使用标准 OpenAI SDK 调用（示例）：  
```python
from openai import OpenAI
client = OpenAI(
    api_key="sk-xxx",
    base_url="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
)
response = client.chat.completions.create(
    model="qwen4-max",
    messages=[{"role": "user", "content": "你好"}]
)
```

✅ **避坑提示**：  
- 不要混用协议：Qwen-Audio、Qwen-VL 的部分高级能力（如高精度 OCR）需用 DashScope 原生 API；  
- 所有 `model` 参数值必须与接口文档支持列表严格一致，拼写错误或越界将返回 `400 Bad Request`；  
- 流式响应中 `delta.content` 可能为空字符串，请做空值判断；  
- [多模态](multi-modal.md)输入务必校验 `detail` 嵌套位置（应在 `image_url` 内，非同级）；  
- 生产环境请始终使用业务空间专属域名，避免因旧域名限流导致超时失败。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [openai compatible agents api](../api/openai-compatible-agents-api.md)
- [frameworks](../api/frameworks.md)
- [image generation](../api/image-generation.md)


