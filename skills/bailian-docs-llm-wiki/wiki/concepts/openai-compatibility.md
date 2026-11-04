# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API 协议，完全遵循 OpenAI 官方 v1 接口规范（包括路径、请求/响应结构、字段语义与错误码），使开发者无需修改业务逻辑即可将现有 OpenAI SDK、LangChain 集成、Prompt 工程脚本或 Agent 框架快速迁移至百炼。该接口不是简单代理，而是原生实现——所有模型能力（如多模态理解、工具调用、结构化输出、缓存控制）均通过标准 OpenAI 字段暴露，保障功能一致性与生产可用性。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有项目**：已使用 `openai>=1.0.0` SDK 的用户，只需将 `base_url` 替换为百炼业务空间专属域名（如 `https://ws-abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），更新 `api_key` 和 `model` 参数，即可零代码改动调用 Qwen 系列、DeepSeek、GLM、Kimi 等数十种模型。
- **多模态应用开发**：通过 `/v1/chat/completions` 接口传入 `image_url`、`video_url` 或 `input_audio`（注意：Qwen-Audio 不支持此协议），即可调用 `qwen3-vl-plus`、`qwen3.8-omni-flash` 等模型实现图文/音视频联合理解，无需适配私有协议。
- **向量与排序任务**：调用 `/v1/embeddings`（文本向量）、 `/v1/multimodal-embeddings`（多模态向量）、`/v1/rerank`（文本精排），参数（如 `input`, `dimensions`, `top_n`）与 OpenAI 生态完全对齐，可直接复用 RAG 流水线。
- **批量与文件处理**：使用 `/v1/batch`（同步批量 Chat）、`/v1/files`（文件上传与管理）、`/v1/batches`（异步批量任务）等端点，支持 JSONL 文件上传、文档解析、微调数据集准备等典型工作流。
- **Agent 与高级推理**：通过 `/v1/responses`（增强版 Chat）启用内置工具链（`web_search`, `code_interpreter`, `file_search`）和深度思考控制（`reasoning.effort`），服务端自动调度，客户端保持 OpenAI 标准 `tool_calls` 响应格式。

> ⚠️ 注意：Qwen-Audio 全系列模型（语音合成、识别、对话等）**不支持 OpenAI 兼容接口**，必须使用 DashScope 原生音频 API。

## 关键参数和配置

| 参数 | 说明 | 注意事项 |
|------|------|----------|
| `base_url` | 必填。业务空间专属域名，格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。`{WorkspaceId}` 在控制台「业务空间详情」获取；`{region}` 如 `cn-beijing`、`ap-southeast-1`。旧域名 `dashscope.aliyuncs.com` 已不推荐。 | 强烈建议使用新域名，性能更高、稳定性更强，且支持全部新特性（如显式缓存、多模态融合）。 |
| `api_key` | 必填。API Key **严格按地域绑定**：北京地域 Key 只能调用北京 endpoint，新加坡 Key 只能调用新加坡 endpoint。混用将返回 `invalid_api_key` 错误。 | Key 权限需在控制台开通对应模型调用权限（如 `qwen3.8-max`、`text-embedding-v4`）。 |
| `model` | 必填。模型 ID 必须与所选接口类型匹配：<br>• Chat/Responses：`qwen3.8-max`, `qwen3-vl-plus`, `deepseek-v4.1-flash-1017`<br>• Embeddings：`text-embedding-v4`, `qwen3.7-text-embedding`<br>• Rerank：`qwen3-rerank`, `qwen3-vl-rerank`<br>• Files/Batch：仅支持白名单模型（见各子文档） | 模型名需与百炼控制台实际开通的模型 ID 完全一致，大小写敏感。 |
| `cache_control` | 可选。启用显式缓存，值为 `{ "type": "ephemeral" }`，标记内容块可被服务端复用，降低重复请求成本。 | 所有 OpenAI 兼容接口均支持，是百炼特有增强，OpenAI 官方不支持。 |
| `response_format` / `output_config.format` | 可选。用于结构化输出，如 `{"type": "json_object"}`，配合 `response_format` 触发 JSON Schema 验证（需模型支持）。 | Anthropic 兼容接口使用 `output_config.format`，OpenAI 兼容接口统一使用 `response_format`。 |
| `temperature`, `max_tokens`, `top_p` 等采样参数 | 通用控制参数。`temperature` 范围 `[0, 2)`；`max_tokens` 行为因模型而异（如对 `qwen3.8-max` 控制总长度，对 `glm-5.2` 仅控回复长度）。 | 请以具体模型文档为准，避免跨协议直接迁移参数值。 |

## 面向开发者，简洁实用

- ✅ **即开即用**：安装官方 `openai` Python SDK（`pip install openai`），初始化 client 时指定 `base_url` 和 `api_key`，其余代码 0 修改。
- ✅ **调试友好**：所有接口返回标准 OpenAI 错误格式（`{ "error": { "message": "...", "type": "...", "code": "..." } }`），与本地开发环境一致。
- ✅ **生产就绪**：支持流式响应（`stream: true`）、重试机制、请求 ID（`x-request-id` Header）、审计日志，满足企业级可观测性要求。
- ✅ **平滑演进**：当百炼新增模型或能力（如新 VL 模型、新嵌入维度），只要符合 OpenAI 规范，即可立即通过同一接口调用，无需 SDK 升级。
- ❌ **避坑提示**：
  - 不要将 DashScope 原生 `X-DashScope-Async` Header 用于 OpenAI 兼容接口；
  - 不要对 `/v1/chat/completions` 传入 `previous_response_id`（这是 Responses API 专用）；
  - 视频处理时，OpenAI 兼容接口**不支持 `max_frames` 参数**，仅支持 `total_pixels` 总像素限制；
  - 文件上传请优先使用 `/compatible-mode/v1/files`（OpenAI 兼容），而非旧版 `/api/v1/files`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [audio api references](../api/audio-api-references.md)
- [file management api](../api/file-management-api.md)


