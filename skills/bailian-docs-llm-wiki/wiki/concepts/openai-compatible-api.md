# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 API 协议层，严格遵循 OpenAI v1 RESTful 接口规范（如 `/v1/chat/completions`、`/v1/embeddings`、`/v1/files` 等路径），支持使用标准 OpenAI SDK（Python/Node.js/Java/Go/C#）或原生 HTTP 调用，无需修改业务代码即可快速迁移现有 AI 应用。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用模型调用**：适用于 `qwen-plus`、`qwen3.7-plus`、`qwen4-max`、`qwen3-vl-plus`、`text-embedding-v4` 等主流文本、多模态与嵌入模型，通过 `client.chat.completions.create()` 或 `client.embeddings.create()` 直接调用。
- **智能体开发与工具集成**：配合 `Responses API`（`/compatible-mode/v1/responses`）可自动注入联网搜索、代码解释器等内置工具，并基于 `previous_response_id` 实现多轮上下文延续；广泛兼容 Qoder、Claude Code、Trae、Hermes Agent 等十余种开发工具。
- **文件与批量处理**：支持 OpenAI 兼容的 `files` 接口上传文档用于内容提取（`purpose="file-extract"`）或批量任务（`purpose="batch"`），也支持 `batches` 接口提交异步批处理请求。
- **Token Plan 专属服务**：面向企业级订阅用户，提供 `sk-sp-` 开头的专用 API Key 与隔离式 Base URL（如 `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），实现计费、权限与地域的精准绑定。
- **对话状态管理**：通过 `Conversations API`（`/compatible-mode/v1/conversations`）创建、追加和查询会话，结合 `Responses API` 构建跨设备、长生命周期的对话体验。
- **不适用场景**：`Qwen-Deep-Research`、`paraformer-realtime-v2`（语音识别）、`cosyvoice-v3-flash`（语音合成）、`Qwen-Audio` 等专用模型**不支持** OpenAI 兼容协议，必须使用 DashScope 原生接口。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填，**必须为地域+业务空间专属域名**，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1` | ❌ 禁止使用全局 `dashscope.aliyuncs.com`；`{WorkspaceId}` 需从控制台获取；Token Plan 用户固定为 `token-plan.{region}.maas.aliyuncs.com` |
| `api_key` | 必填，`sk-xxx`（百炼）或 `sk-sp-xxx`（Token Plan）开头的密钥 | ✅ Key 与 `base_url` 地域必须严格一致（如北京 Key 只能配 `cn-beijing` 域名），否则返回 `401 InvalidApiKey` |
| `model` | 必填，模型 ID 必须与 [模型列表](raw/model-user-guide/get-started-with-models/models.md) 中的标准名称完全一致（如 `"qwen3.7-plus"`） | ❌ 不支持开源社区别名（如 `"qwen2.5"`）；多模态模型要求 `messages.content` 为数组（含 `text`/`image_url`），纯文本模型要求为字符串 |
| `enable_thinking` | 可选布尔值，部分模型（如 `qwen3.8-*` 系列）默认开启思考模式；设为 `false` 可降本并启用结构化输出（`response_format={"type": "json_object"}`） | ⚠️ 必须作为顶层参数传入，不可置于 `extra_body`；开启时需同步设置 `incremental_output=true` 和 `result_format="message"` |
| `previous_response_id` | Responses API 多轮对话必需参数，值为上一次响应的顶层 `id` 字段（如 `"resp_xxx"`） | ❌ 不是 `output.messages[0].id`（即 `msg_xxx`），传错将导致上下文丢失 |

## 面向开发者，简洁实用

- ✅ **快速上手**：安装任一 OpenAI SDK（如 `pip install openai`），仅需替换 `base_url` 和 `api_key`，其余代码（包括 `messages` 格式、`stream`、`temperature` 等）零修改。
- ✅ **调试建议**：首次调用推荐用 `curl` 验证基础连通性：
  ```bash
  curl -X POST "https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1/chat/completions" \
    -H "Authorization: Bearer sk-xxx" \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen-plus","messages":[{"role":"user","content":"Hello"}]}'
  ```
- ✅ **错误排查**：常见问题优先检查三项一致性——API Key 所属地域、Base URL 地域、模型开通地域；所有错误均返回标准 HTTP 状态码 + 百炼 `code` 字段（如 `InvalidParameter`、`Throttling.RateQuota`）。
- ✅ **安全实践**：`api_key` 必须通过环境变量（如 `OPENAI_API_KEY`）注入，禁止硬编码；生产环境务必使用业务空间专属域名，避免共享流量与权限风险。
- ⚠️ **限制提醒**：OpenAI 兼容接口**不原生支持工具调用（`tools`）或联网搜索**（除非使用 `/responses` 路径）；`stop`、`top_k`、`repetition_penalty` 等高级参数需切换至 DashScope 原生接口。

## 关联主题页

- [preparations](../api/preparations.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [file management api](../api/file-management-api.md)
- [more models](../api/more-models.md)


