# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，完全遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/v1/chat/completions`），使开发者能直接复用现有 OpenAI SDK（如 `openai>=1.0`）和生态工具（LangChain、LlamaIndex、Cursor、Dify 等），无需修改业务逻辑即可调用百炼托管的千问（Qwen）全系模型及主流第三方模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速接入与原型验证**：开发者只需替换 `base_url` 和 `model` 参数，即可将本地 OpenAI 代码迁移至百炼，5 分钟内完成首次调用，适用于 PoC、A/B 测试和轻量应用开发。  
- **多模态推理统一入口**：通过标准 `messages` 数组支持 `text`、`image_url`（含 Base64）、`video_url` 等内容类型，兼容 Qwen-VL、Qwen-Audio（部分型号）、Qwen-OCR 等视觉/语音模型（注意：Qwen-Audio 当前不支持 OpenAI 协议，需用 DashScope 原生接口）。  
- **智能体（Agent）增强能力**：`/v1/responses` 是百炼特有扩展端点，在 OpenAI 兼容框架下原生支持 `tools`（如 `web_search`、`code_interpreter`）、`previous_response_id`（自动上下文关联）和 Session 缓存，无需额外编排即可构建具备联网、计算、文档理解能力的生产级 Agent。  
- **第三方工具链集成**：Postman、Kilo CLI、OpenClaw、Cherry Studio、Qoder CN 等客户端可直接配置百炼 `base_url` 和 API Key，开箱即用；LangChain 用户仅需初始化 `ChatOpenAI` 并传入百炼域名，即可无缝接入 RAG、Workflow 等高级模式。  
- **垂直场景模型调用**：意图识别（`tongyi-intent-detect-v3`）、法律（`farui-plus`）、GUI 自动化（`gui-plus-*`）等专用模型均支持 OpenAI 兼容接口，通过标准 `messages` + 领域特定 `system` 提示或 `extra_body` 扩展参数启用专业能力。

> ⚠️ 注意：并非所有模型和能力都 100% 兼容 OpenAI 官方行为。例如：`qwen-deep-research` 仅支持 DashScope Python SDK，不开放 OpenAI 接口；`temperature` 范围为 `[0, 2)`（非 OpenAI 的 `[0, 2]`）；部分非标参数（如 `enable_thinking`、`vl_high_resolution_images`）需置于 `extra_body` 中传递。

## 关键参数和配置

| 参数 | 是否必填 | 说明 | 示例值 |
|------|----------|------|--------|
| `base_url` | ✅ | **必须使用业务空间专属域名**，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。旧域名 `dashscope.aliyuncs.com` 已进入迁移期，2026 年 9 月 30 日起停止支持新特性。 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | ✅ | 百炼控制台生成的 API Key（非阿里云 AK/SK），按地域独立管理，不可跨地域复用。推荐设为环境变量 `DASHSCOPE_API_KEY`。 | `sk-xxx` |
| `model` | ✅ | 模型标识符，严格区分大小写，需与所选地域支持列表一致。支持 Qwen 全系（`qwen3.8-max`）、第三方（`deepseek-v4-pro-0813`）、嵌入（`text-embedding-v4`）、意图（`tongyi-intent-detect-v3`）等。 | `"qwen3.8-max"`, `"text-embedding-v4"` |
| `messages` | ✅（chat/responses） | 标准 OpenAI 消息数组，`content` 支持 `text` / `image_url` / `video_url`；视觉模型需确保 `image_url.url` 可公开访问或为 Base64 编码。 | `[{"role": "user", "content": [{"type": "text", "text": "描述这张图"}, {"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}]}]` |
| `extra_body` | ❌（可选） | 传递 OpenAI 规范外的百炼扩展参数，如 `{"enable_thinking": true}`、`{"vl_high_resolution_images": true}`。**不可放在 `messages` 或顶层 body 内**。 | `{"enable_thinking": false}` |
| `previous_response_id` | ⚠️（仅 `/responses`） | 用于多轮上下文延续，值为上一轮响应的顶层 `id`（UUID 字符串），非 `output[0].id`。 | `"0c842a11-c7d1-45da-b7ec-4e668c389xxx"` |

## 面向开发者，简洁实用

- ✅ **立即上手**：安装 `pip install -U openai`，复制 OpenAI 示例代码，仅改 `base_url` 和 `model` 即可运行。  
- ✅ **调试友好**：所有请求/响应结构与 OpenAI 官方一致，可直接用 Postman 或 `curl` 测试，错误码（如 `429` 限流、`400` 参数错误）语义清晰。  
- ✅ **平滑演进**：同一套代码可同时对接百炼（OpenAI 兼容）、Anthropic 兼容、DashScope 原生接口，通过切换 `base_url` 和参数适配不同协议。  
- ⚠️ **避坑提示**：  
  - 不要硬编码 `api_key`，务必使用环境变量；  
  - `enable_thinking` 必须放 `extra_body`，否则无效；  
  - 文件类操作（上传、批量处理）需用 `client.files.create()` 等专用方法，非 `chat.completions`；  
  - 流式响应（`stream: true`）在部分 GUI 工具中可能渲染异常，建议先测试 `stream: false`。  

如需完整参数列表、各模型支持详情及错误码说明，请查阅 [OpenAI 兼容 API 参考](../../raw/model-api-reference/qwen-api-reference/qwen-api-via-openai-chat-completions.md)。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [more models](../api/more-models.md)


