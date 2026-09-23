# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 RESTful API 协议，完全遵循 OpenAI 的 `chat/completions`、`completions`、`embeddings`、`files`、`batches` 等核心端点规范与请求/响应格式，使开发者能复用现有 OpenAI SDK（如 `openai==1.0+`）、工具链（Cursor、Dify、Hermes）和代码逻辑，仅需替换基础配置即可无缝接入千问（Qwen）及主流第三方模型。

## 在百炼平台的不同场景中如何使用

- **快速原型开发**：通过 `base_url + api_key + model` 三元组，5 分钟内用标准 OpenAI Python SDK 调通 `qwen3.8-plus` 文本生成，无需修改业务逻辑。
- **多模态应用集成**：对支持的模型（如 `qwen3.8-omni-flash`），在 `messages.content` 中按 OpenAI 格式传入 `image_url`（OSS 或 data URI）或结构化 `input_audio`/`input_video`，实现音视频理解；注意：纯 `chat/completions` 接口不支持音频输入，需改用 Responses API。
- **RAG 与向量检索**：调用 `/embeddings` 端点（如 `qwen3.7-text-embedding-flash`），直接兼容 LangChain、LlamaIndex 的嵌入模块；支持 `input` 为字符串或字符串数组，输出标准 `embedding` 数组。
- **批量任务处理**：使用 `/v1/batches` 提交 JSONL 文件，享受实时调用 50% 的费用折扣；支持 `batch_chat`（同步等待）与 `batch_file`（异步提交）两种模式。
- **智能体（Agent）构建**：启用 `tools` 参数声明 `web_search`、`file_search` 等内置工具，结合 `tool_calls` 响应解析，实现免开发的联网/知识库调用能力。
- **会话状态管理**：配合 `/conversations` CRUD 接口，持久化对话上下文，解决跨设备、长时间中断后的上下文断裂问题，替代手动维护 `messages` 历史。

> ⚠️ 注意：`qwen-audio` 模型、部分高级推理模式（如 `reasoning.effort`）及 `QwQ`/`QVQ` 系列模型不支持 OpenAI 兼容协议，需切换至 DashScope 原生协议或 Anthropic 兼容协议。

## 关键参数和配置

| 参数 | 必填 | 类型 | 说明 | 示例值 |
|------|------|------|------|--------|
| `base_url` | 是 | string | **必须使用业务空间专属域名**，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；旧域名 `dashscope.aliyuncs.com` 已停用，生产环境严禁混用 | `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1` |
| `api_key` | 是 | string | 与 `base_url` 地域和计费方案严格匹配的密钥；[Token](token.md) Plan、Coding Plan、按量计费 Key 互不通用 | `sk-xxxxxxxxxxxxx`（按量计费）或 `tpk-xxxxxxxx`（[Token](token.md) Plan） |
| `model` | 是 | string | 百炼支持的模型 ID，需与所选协议能力匹配；不同接口支持范围不同（如 `completions` 仅支持 `qwen-coder-turbo`） | `"qwen3.8-plus"`, `"qwen3.7-text-embedding-flash"`, `"glm-5-3"`（注意：`.` 需替换为 `-`） |
| `messages` | 是（chat） | array | 标准 OpenAI 消息数组，支持 `system`/`user`/`assistant` 角色；`user` 消息可含 `image_url`、`input_file` 等多模态内容 | `[{"role": "user", "content": [{"type": "image_url", "image_url": {"url": "data:image/png;base64,..."}}]}]` |
| `stream` | 否 | boolean | 启用流式响应（SSE），适用于长文本生成或前端实时渲染 | `true` |
| `tools` | 否 | array | 声明模型可调用的工具列表，支持内置工具（`web_search`）和自定义 function 工具 | `[{"type": "web_search"}, {"type": "function", "function": {"name": "get_weather", ...}}]` |
| `response_format` | 否 | object | 控制输出结构，设 `{"type": "json_schema", "json_schema": {...}}` 可启用强约束 JSON 输出（qwen3.8+/glm-5.x 支持） | `{"type": "json_schema", "json_schema": {"name": "answer", "schema": {"type": "object", "properties": {"text": {"type": "string"}}}}}` |

## 面向开发者的重要提示

- ✅ **立即可用**：安装最新版 `openai` SDK（≥1.40.0），初始化时指定 `base_url` 和 `api_key`，其余代码零修改。
- ✅ **地域与 Key 强绑定**：北京地域 Key 只能配北京 `base_url`，新加坡 Key 不可用于东京域名，否则返回 `401 invalid_api_key`。
- ✅ **WorkspaceId 是必填项**：在控制台「业务空间管理」中获取真实 ID，**不可留 `{WorkspaceId}` 占位符**。
- ❌ **避免踩坑**：
  - 不要使用 `dashscope.aliyuncs.com` 域名——功能缺失且将于 2026 年 9 月 30 日彻底下线；
  - [Token](token.md) Plan / Coding Plan Key **禁止用于 Dify、n8n、Coze 等工作流平台**，仅限个人开发工具（Cursor、Hermes）使用；
  - `qwen3.8-omni-flash-realtime` 为实时语音专用模型，**不兼容 OpenAI `chat/completions`**，须用 Responses API；
  - `embeddings` 接口不支持 `output_type=sparse`，传入将返回空向量。

如需调试，推荐使用 [百炼控制台的 API Playground](https://bailian.console.aliyun.com/cn-beijing/model/playground) 实时验证请求格式与响应。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [application component api reference](../api/application-component-api-reference.md)


