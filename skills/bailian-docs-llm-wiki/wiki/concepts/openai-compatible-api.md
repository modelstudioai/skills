# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 RESTful API，严格遵循 OpenAI 的请求格式、路径结构与响应协议（如 `/v1/chat/completions`），使开发者能复用现有 OpenAI SDK、工具链和代码逻辑，零改造调用千问（Qwen）全系列及主流第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速接入与迁移**：已有基于 OpenAI SDK（Python/Node.js）开发的应用，只需替换 `api_key` 和 `base_url`，无需修改业务逻辑即可调用百炼托管的 `qwen3.8-plus`、`deepseek-v4-pro-0813` 等模型，大幅降低迁移成本。  
- **[多模态](multi-modal.md)统一调用**：文本、图像、音频等模型（如 `qwen3.8-omni-flash`、`qwen-audio-3.1-asr-flash-streaming`）均支持同一套 OpenAI 兼容接口，通过 `model` 参数切换，避免为不同模态维护多套客户端。  
- **流式响应与调试友好**：支持标准 `stream=true` 流式传输，返回符合 OpenAI SSE 格式的 `data: {...}` 响应，便于前端实时渲染、日志追踪和本地调试。  
- **与原生接口协同使用**：当需要 JSON Schema 结构化输出、工具调用（function calling）或高级采样控制时，可切换至 DashScope 原生接口；而日常对话、内容生成等通用场景，优先选用 OpenAI 兼容接口以保持简洁性与生态兼容性。

## 关键参数和配置

| 参数 | 说明 | 示例值 | 是否必需 |
|------|------|--------|----------|
| `model` | 模型标识符，必须与所选地域支持的模型一致 | `"qwen3.7-plus"`, `"kimi-k3"` | ✅ |
| `base_url` | 接入域名，**必须与 API Key 所属地域严格匹配**，并填入真实 `WorkspaceId` | `"https://abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"` | ✅（私有化/多地域部署必填） |
| `api_key` | 百炼平台生成的 API Key，建议设为环境变量 `DASHSCOPE_API_KEY` | `"sk-xxx"` | ✅ |
| `messages` | 对话消息数组，格式与 OpenAI 完全一致 | `[{"role":"user","content":"你好"}]` | ✅（`chat/completions`） |
| `temperature` | 控制输出随机性（0.0–2.0），默认 `1.0` | `0.7` | ❌（可选） |
| `max_tokens` | 输出最大 token 数，受模型上下文限制 | `1024` | ❌（可选） |
| `stream` | 启用流式响应（布尔值） | `True` | ❌（可选） |

> ⚠️ 注意：  
> - `base_url` 路径固定为 `/compatible-mode/v1`（不带 `/chat/completions` 后缀），SDK 会自动拼接 endpoint；  
> - `api_key` 不可跨地域复用，北京地域 Key 无法用于新加坡接入点；  
> - 工具调用（`tools` / `tool_choice`）**不被 OpenAI 兼容接口原生支持**，需改用 DashScope 原生接口。

## 面向开发者，简洁实用

- ✅ **推荐起步方式**：用 OpenAI Python SDK（`pip install openai`），初始化时传入 `base_url` 和 `api_key`，直接调用 `client.chat.completions.create()`；  
- ✅ **调试技巧**：用 `curl` 快速验证，注意设置 `Content-Type: application/json` 和 `Authorization: Bearer <api_key>`；  
- ✅ **错误排查**：若返回 `404 Not Found`，检查 `base_url` 路径是否误加了 `/chat/completions`；若返回 `401 Unauthorized`，确认 `api_key` 地域匹配且未过期；  
- ✅ **性能提示**：高并发场景下，建议复用 `OpenAI` client 实例，避免频繁重建连接；  
- ❌ **不推荐场景**：需强约束 JSON 输出、复杂[函数调用](function-calling.md)或自定义 stop token 时，请切换至 DashScope 原生接口。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [preparations](../api/preparations.md)


