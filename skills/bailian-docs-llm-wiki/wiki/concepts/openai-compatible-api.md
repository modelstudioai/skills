# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一组标准化 RESTful API，严格遵循 OpenAI 官方 API 的路径、请求/响应结构、参数命名与错误码规范（如 `/v1/chat/completions`），使开发者无需修改业务逻辑即可将现有基于 OpenAI SDK 的代码（Python、Node.js、cURL 等）快速迁入百炼，调用千问系列及第三方直供大模型。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有项目**：只需替换 `base_url`（指向百炼专属域名）、`api_key`（使用 DashScope API Key）和 `model`（如 `qwen3.8-max`），即可复用 OpenAI SDK（如 `openai==1.45.0+`）或主流工具链（Cursor、Dify、Postman、LangChain）。
- **多模态开发**：通过标准 `messages` 数组传入 `image_url`（支持 Base64 或公网 URL），调用 `qwen3-vl-plus`、`qwen3.8-omni-flash` 等视觉/音视频模型，完全兼容 OpenAI Vision 规范。
- **智能体（Agent）构建**：使用 `OpenAI兼容-Responses` 接口（路径 `/compatible-mode/v1/responses`），获得内置联网搜索、网页抓取、代码解释器等工具能力，并通过 `previous_response_id` 实现多轮上下文自动关联，显著降低 Agent 工程复杂度。
- **批量与文件处理**：结合 OpenAI 文件接口兼容能力，上传 PDF/DOCX/图像等文件（`purpose=file-extract`），直接用于文档问答、结构化提取等场景。
- **向量检索集成**：调用 `text-embedding-v4` 等模型时，使用标准 `/v1/embeddings` 路径与 `input` 字段，无缝接入 RAG 流水线；注意不支持稀疏向量输出（`output_type=sparse` 将返回空 embedding）。

> ⚠️ 限制说明：`Qwen-Audio` 模型**不支持** OpenAI 兼容协议，必须使用 DashScope 原生 API；`completions` 接口仅限 `qwen-coder-turbo` 等特定模型；`qwen3.5-omni-plus` 在 Batch 场景下不支持语音输出。

## 关键参数和配置

| 参数 | 类型 | 说明 | 注意事项 |
|------|------|------|----------|
| `base_url` | `string` | 必填。服务端点，格式为：<br>• 按量计费：`https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`<br>• [Token](token.md) Plan：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`<br>• Coding Plan：`https://coding.dashscope.aliyuncs.com/v1` | 地域（如 `cn-beijing`）必须与 API Key 所属地域严格一致，否则返回 `invalid_api_key`；推荐使用业务空间专属域名以保障稳定性与性能。 |
| `model` | `string` | 必填。模型 ID，例如 `qwen3.8-max`、`qwen3-vl-plus`、`deepseek-v4-pro`、`text-embedding-v4` | 不同子接口支持范围不同：<br>• `chat/completions`：支持全系列文本/多模态模型<br>• `embeddings`：仅限向量模型<br>• `responses`：仅限明确标注支持的模型（见控制台或文档列表） |
| `messages` | `array` | 对话输入，格式为 `[{"role": "user", "content": "..."}, ...]`；支持 `role="system"`（部分模型生效）和 `content` 中嵌入图像（`{"type": "image_url", "image_url": {"url": "..."}}`） | `qwen-vl-plus` 等视觉模型**仅支持[流式输出](streaming.md)**（`stream=true`）；图像分辨率由平台自动缩放，不支持 `min_pixels`/`max_pixels` 等 DashScope 特有参数。 |
| `stream` / `stream_options` | `boolean` / `object` | 是否启用流式响应；`stream_options={"include_usage": true}` 可在流末尾返回 token 统计 | 默认 `false`；流式响应需按 SSE 格式解析，末行含 `data: [DONE]`。 |
| `enable_thinking` | `boolean` | 控制是否启用模型内部思考（reasoning）流程 | 仅对 `qwen3.5+` 系列模型有效；必须作为请求 body 顶层字段传入（不可放在 `extra_body` 内）；默认 `true`，关闭可降低 token 成本。 |
| `previous_response_id` | `string` | 用于 `responses` 接口的多轮对话上下文关联 | 必须传入上一轮响应的顶层 `id` 字段值（如 `"resp_abc123"`），而非 `response_id` 或其他字段。 |

## 面向开发者，简洁实用

- ✅ **即插即用**：`pip install openai` 后，仅需 3 行代码切换：
  ```python
  from openai import OpenAI
  client = OpenAI(base_url="https://your-workspace-id.cn-beijing.maas.aliyuncs.com/compatible-mode/v1", 
                  api_key="sk-xxx")
  response = client.chat.completions.create(model="qwen3.8-max", messages=[{"role": "user", "content": "你好"}])
  ```
- ✅ **调试友好**：所有错误均返回标准 OpenAI 错误格式（`{"error": {"message": "...", "type": "invalid_request_error", "code": "model_not_found"}}`），便于统一捕获与日志。
- ✅ **生产就绪**：支持业务空间专属域名、[Token](token.md) Plan/Coding Plan 多套餐隔离、PTU/DTU/智能路由等部署模式，满足高并发、低延迟、成本可控等企业级需求。
- ❌ **避坑提示**：
  - 不要混用 Key 与 Base URL 方案（如 [Token](token.md) Plan Key + 按量 Base URL）；
  - 图像模型务必设 `stream=True`；
  - `qwen-mt-plus` 翻译需通过 `extra_body={"translation_options": {...}}` 传参，非直接平铺字段；
  - `responses` 接口旧路径 `/api/v2/apps/protocols/compatible-mode/v1/responses` 已废弃，请立即迁移至 `/compatible-mode/v1/responses`。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [use chat client or development tool](../guides/use-chat-client-or-development-tool.md)
- [model deployment index](../guides/model-deployment-index.md)
- [qwen mt translation models](../api/qwen-mt-translation-models.md)


