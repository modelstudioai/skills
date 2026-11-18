# OpenAI 兼容接口

OpenAI 兼容接口是百炼平台提供的一套标准化 REST API 协议，严格遵循 OpenAI v1 API 的路径、请求/响应结构、字段命名与错误码规范，使开发者无需修改核心调用逻辑即可将现有 OpenAI 应用快速迁移至百炼。该接口并非简单代理，而是深度适配百炼模型能力（如多模态、工具链、长上下文）的原生实现，兼顾兼容性与扩展性。

## 在百炼平台的不同场景中，这个概念如何使用

- **快速迁移已有应用**：替换 SDK 初始化时的 `base_url`（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`）和 `api_key`，即可复用 `openai`、`langchain_openai` 等标准 SDK 调用 Qwen、DeepSeek、GLM、Kimi 等模型，零代码改造。
- **构建智能体（Agent）**：通过 `/compatible-mode/v1/responses` 接口启用内置联网搜索、网页抽取、代码解释器等工具链；配合 `previous_response_id` 实现无状态多轮对话，`store=true` 后可查询历史输入与输出。
- **多模态理解与生成**：在 `/compatible-mode/v1/chat/completions` 中使用 `messages` 包含 `image_url` 或 base64 图像数据，支持 `qwen3-vl-plus`、`QVQ` 等模型；注意 `QVQ` 仅支持[流式输出](streaming-output.md)，需显式启用思考模式。
- **向量嵌入与排序**：调用 `/compatible-mode/v1/embeddings`（文本向量）或 `/compatible-mode/v1/rerank`（文本重排），支持 `qwen3.7-text-embedding`、`qwen3-rerank` 等模型；注意多模态向量（`qwen3-vl-embedding`）和稀疏向量暂不兼容此协议。
- **文件与批量处理**：使用 `/compatible-mode/v1/files` 上传、管理文件（用途为 `file-extract`/`batch`），再通过 `/compatible-mode/v1/batches` 提交异步批量推理任务；相比 DashScope 原生文件接口，OpenAI 兼容版支持跨 Region 调用且错误码更规范。

> ⚠️ 注意：Qwen-Audio 音频模型、部分高级参数（如 `vl_high_resolution_images`、`min_pixels`）及稀疏向量输出等能力**仅在 DashScope 原生协议中可用**，不纳入 OpenAI 兼容接口范围。

## 关键参数和配置

| 参数 | 位置 | 必填 | 说明 |
|------|------|------|------|
| `base_url` | SDK 初始化或 HTTP 请求 Host | 是 | 格式为 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`；必须使用业务空间专属域名（如 `abc123.cn-beijing.maas.aliyuncs.com`），旧域名 `dashscope.aliyuncs.com` 已不推荐。 |
| `api_key` | `Authorization: Bearer <API_KEY>` | 是 | **严格按地域绑定**：北京地域 endpoint 必须使用北京创建的 API Key，跨地域调用返回 `401 invalid_api_key`。 |
| `model` | 请求 body | 是 | 模型 ID 必须与控制台发布名称**完全一致、大小写敏感**，如 `qwen3.8-max`（非 `qwen-3.8-max`）、`deepseek-v4.1-flash`；第三方模型需带供应商前缀。 |
| `workspace_id` | URL 路径占位符 | 是 | `{WorkspaceId}` 需替换为真实业务空间 ID，可在百炼控制台「业务空间详情」页获取。 |
| `stream` | 请求 body | 否 | 设为 `true` 启用逐 token 流式响应（所有 Chat/Responses/Vision 接口均支持）。 |
| `enable_thinking` | 请求 body（Batch 场景） | 否 | 显式开关思考模式，默认开启；必须作为顶层参数传入，不可置于 `extra_body`。 |

> ✅ 最佳实践：将 `base_url` 和 `api_key` 从环境变量读取（如 `OPENAI_BASE_URL`, `OPENAI_API_KEY`），避免硬编码；使用 `curl -v` 或 SDK 日志验证实际请求 URL 与 Header 是否符合预期。

## 面向开发者，简洁实用

- **起步最快方式**：
  ```bash
  pip install -U openai
  export OPENAI_BASE_URL="https://abc123.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
  export OPENAI_API_KEY="sk-xxx"
  python -c "from openai import OpenAI; c=OpenAI(); print(c.chat.completions.create(model='qwen3.8-max', messages=[{'role':'user','content':'Hello'}]).choices[0].message.content)"
  ```

- **调试要点**：
  - 404 错误：检查 `model` 名称是否拼写正确、`base_url` 是否含 `/compatible-mode/v1` 路径；
  - 401 错误：确认 `api_key` 与 `base_url` 所在地域一致；
  - 400 错误：检查 `messages` 格式（必须为数组，首条 `system` 消息需 `role: system`）、图像参数（`detail` 仅对 `qwen4-max` 生效）；
  - 流式响应：确保客户端正确处理 `text/event-stream` Content-Type 与 `data:` 前缀。

- **避坑提醒**：
  - 不要混用协议：`/responses` 是 OpenAI 兼容专用路径，勿与 Anthropic 的 `/messages` 或 DashScope 原生 `/api/v1/services/...` 混用；
  - 第三方模型（DeepSeek/Kimi/GLM）仅在华北2（北京）、新加坡、中国香港地域可用，且需在控制台开通对应服务；
  - `max_pixels` 默认值以 OpenAI 兼容文档为准（如 `qwen3.8-max` 为 `2621440`），DashScope 原生协议可能不同。

## 关联主题页

- [qwen api reference](../api/qwen-api-reference.md)
- [toolkits and frameworks](../api/toolkits-and-frameworks.md)
- [frameworks](../api/frameworks.md)
- [vector and sort](../api/vector-and-sort.md)
- [file management api](../api/file-management-api.md)


