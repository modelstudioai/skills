# OpenAI 兼容接口

OpenAI 兼容接口是阿里云百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI REST API 的路径、请求/响应结构、参数命名与语义规范（如 `/chat/completions`、`messages` 数组、`stream` 流式开关等），使开发者能复用现有 OpenAI SDK（如 `openai>=1.0`）、工具链（LangChain、LlamaIndex）及客户端（Cursor、Dify、Postman），仅需替换 `base_url` 和 `api_key` 即可快速接入千问（Qwen）全系列模型及主流第三方模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型直调**：通过 `chat/completions`（标准对话）、`completions`（代码补全）、`embeddings`（向量生成）、`vision`（图文理解）等端点，调用 `qwen3.8-plus`、`qwen3-vl-plus`、`text-embedding-v4` 等模型，适用于简单 [prompt](../guides/prompt.md) 工程、RAG 基础服务或轻量 Agent。
- **智能体（Agent）开发**：使用增强型 `responses` 接口（路径为 `/responses`），支持内置工具调用（`web_search`、`code_interpreter`、`knowledge_retrieval`）、多轮上下文锚定（`previous_response_id`）和结构化输出，是构建生产级 AI 应用的推荐入口。
- **框架集成**：零改造接入 LangChain（`langchain_openai.ChatOpenAI`）、LlamaIndex、Hermes、Kilo CLI 等生态工具；支持 Dify、OpenClaw 等低代码平台——只需配置兼容模式 Base URL，无需修改业务逻辑。
- **客户端适配**：终端 CLI（如 Qwen Code）、IDE 插件（Cursor、Qoder）、桌面应用（Cherry Studio）均原生支持该协议，开发者可直接在开发环境中切换百炼模型，享受本地编码体验。
- **批量与流式处理**：支持单请求多条 [prompt](../guides/prompt.md) 的 batch 调用（需使用专用 batch 域名），以及 `stream=true` 的 SSE 流式响应，满足高吞吐、低延迟、实时渲染等生产需求。

> ⚠️ 注意：`qwen-audio`、部分旧版模型及特定功能（如 `Qwen2.5-VL` 的视频帧率精细控制）不支持 OpenAI 兼容协议，必须使用 DashScope 原生 API。

## 关键参数和配置

| 参数 | 说明 | 必填 | 示例值 | 注意事项 |
|------|------|------|--------|----------|
| `base_url` | OpenAI 兼容服务入口，**必须使用业务空间专属域名** | 是 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` | 替换 `{WorkspaceId}`；旧域名 `dashscope.aliyuncs.com` 已不推荐，性能与稳定性较低 |
| `api_key` | 百炼 API Key（环境变量推荐 `DASHSCOPE_API_KEY`） | 是 | `sk-xxx` | **必须与 Base URL 所属地域、计费方案（[Token](token.md) Plan / Coding Plan / 按量）严格匹配**，跨方案混用将返回 `401` |
| `model` | 模型 ID，区分大小写与版本后缀 | 是 | `"qwen3.8-plus"`, `"qwen3-vl-flash"`, `"text-embedding-v4"` | 查看[模型广场](https://bailian.console.aliyun.com/cn-beijing/model/market)确认可用性；`qwen-coder-turbo` 仅支持 `/completions`，不支持 `/chat/completions` |
| `messages` | 对话历史数组（role/content 结构） | 是（`/chat/completions`） | `[{"role":"user","content":"你好"}]` | 不支持字符串输入；系统消息（`system`）建议置于首位 |
| `stream` | 启用流式响应（SSE） | 否（默认 `false`） | `true` | 需客户端支持解析 `data:` chunk；流式下 `response.choices[0].delta.content` 为增量内容 |
| `enable_thinking` | 控制深度思考过程是否启用（影响 token 计费与响应结构） | 否（默认 `true`） | `false` | **必须作为顶层 JSON 字段传入请求体**，不可放在 `extra_body` 或 `headers` 中 |
| `previous_response_id` | `responses` 接口多轮对话必需，用于关联上下文 | 是（`/responses` 多轮） | `"resp_abc123..."` | 取上一轮响应的顶层 `id` 字段（UUID 格式），非 `output` 内消息的 `id` |

## 面向开发者，简洁实用

- ✅ **快速起步**：安装 `openai` SDK → 设置 `DASHSCOPE_API_KEY` 环境变量 → 初始化 `OpenAI(base_url=..., api_key=...)` → 调用 `client.chat.completions.create(model="qwen3.8-plus", messages=[...])`。
- ✅ **调试技巧**：用 `curl` 直接测试：
  ```bash
  curl -X POST "$BASE_URL/chat/completions" \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen3.8-plus","messages":[{"role":"user","content":"你好"}]}'
  ```
- ✅ **避坑指南**：
  - 地域、计费方案、API Key、Base URL 四者必须完全一致，否则报 `404`（地域不匹配）或 `401`（Key 无效）；
  - `workspace_id` 是 Base URL 的一部分，不是请求头或请求体参数；
  - `temperature` 取值范围为 `[0, 2)`，非 OpenAI 官方的 `[0, 2]` 或 `[0, 1]`；
  - 使用 `responses` 接口时，首次调用无 `previous_response_id`，后续必须携带上一轮响应的 `id`。

如需高级能力（JSON Schema 输出、显式缓存、[多模态](multimodal.md)细粒度控制），请参考 Anthropic 兼容接口或 DashScope 原生 API。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [application call](../api/application-call.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


