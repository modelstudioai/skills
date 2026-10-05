# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组遵循 OpenAI REST API 规范（包括路径、请求体结构、响应格式、流式事件协议等）的标准 HTTP 接口，使开发者能直接复用现有 OpenAI SDK（如 `openai==1.0+`）或工具链，无需修改核心调用逻辑，即可快速接入千问（Qwen）全系列及主流第三方大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速原型开发与迁移**：开发者只需替换 `base_url` 和 `api_key`，即可将原有 OpenAI 项目（如基于 `gpt-4o` 的对话应用）无缝切换至百炼的 `qwen3.8-plus` 等模型，5 分钟内完成首次调用。
- **多模态任务集成**：通过 OpenAI 兼容的 `/chat/completions` 接口，传入含 `image_url` 或 `video_url` 的 `messages`，即可调用 `qwen3.8-omni-flash`、`qwen3-vl-plus` 等模型实现图文/音视频理解；注意 `qwen-audio` 不支持该协议，需改用 DashScope 原生接口。
- **智能体（Agent）构建**：使用 `/responses` 接口（OpenAI 兼容 Responses 协议），可直接启用内置工具链（`web_search`、`code_interpreter`、`file_search`），自动触发工具调用与思考链（reasoning），无需自行解析 `tool_calls` 并轮询结果。
- **向量与批量处理**：`/embeddings` 和 `/batch/chat` 等兼容端点支持标准 OpenAI 请求格式，适用于 RAG 向量化、评测数据批量打标等场景；其中 Batch 接口支持异步提交与回调，成本降低 50%。
- **跨工具链统一接入**：Cursor、Cherry Studio、QwenPaw、Dify（按量计费方案）等主流开发工具均原生支持 OpenAI 兼容协议，配置 `Base URL` + `API Key` + `Model ID` 即可直连百炼，无需适配层。

> ⚠️ 注意：  
> - `qwen-audio`、部分 OCR/法律专用模型明确不支持 OpenAI 兼容协议；  
> - `completions` 接口仅限华北2（北京）地域，且仅支持 `qwen-coder-turbo`；  
> - 所有兼容接口必须使用**业务空间专属域名**（`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`），旧 DashScope 域名（`dashscope.aliyuncs.com`）已停用新特性支持。

## 关键参数和配置

| 参数 | 必填 | 说明 | 典型值示例 |
|------|------|------|------------|
| `base_url` | ✅ | 业务空间专属域名，**必须与地域、计费方案严格匹配** | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | ✅ | 百炼控制台生成的 API Key，**按地域隔离，不可跨地域复用** | `sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`（按量计费）<br>`tp-xxxxxxxx`（Token Plan） |
| `model` | ✅ | 模型标识符，需从各接口支持列表中选择 | `qwen3.8-plus`、`qwen3.8-omni-flash`、`text-embedding-v4`、`deepseek-v4-pro-0813` |
| `messages` | ✅（Chat/Responses） | 标准 OpenAI 消息数组，支持 `system`/`user`/`assistant` 角色；多模态输入通过 `content` 中的 `image_url`、`video_url` 字段传递 | `[{"role":"user","content":[{"type":"text","text":"描述这张图"},{"type":"image_url","image_url":{"url":"https://..."}}]}]` |
| `stream` | ❌（默认 `false`） | 启用流式响应，返回 `data: {...}` 事件流 | `true` |
| `stream_options` | ❌ | 控制流式行为，如是否在末尾 chunk 返回 token 统计 | `{"include_usage": true}` |
| `temperature` / `top_p` | ❌（默认值生效） | 采样控制参数；OpenAI 兼容接口取值范围为 `[0, 2)`，非 `[0,1]` | `0.7`, `0.95` |
| `reasoning.effort` | ❌（Responses API 特有） | 控制思考强度（`"low"`/`"medium"`/`"high"`），影响推理深度与 token 消耗 | `"high"` |
| `total_pixels` | ❌（Responses API 视频场景） | 限制视频总像素量，防止超限 | `10485760`（10MP） |

> 💡 提示：  
> - 使用 Python 时推荐 `openai>=1.0.0` SDK，初始化方式统一为 `OpenAI(api_key=..., base_url=...)`；  
> - 流式响应需按 OpenAI 标准解析 `data:` 行，末尾以 `data: [DONE]` 结束；  
> - 错误响应格式与 OpenAI 一致（`{"error": {"message": "...", "type": "...", "code": "..."}}`），便于统一错误处理。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [get started with models](../guides/get-started-with-models.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)


