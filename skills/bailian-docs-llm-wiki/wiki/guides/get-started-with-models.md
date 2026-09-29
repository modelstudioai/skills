# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解平台当前支持的主流模型类型、关键请求参数含义、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API 接口，无需安装额外 SDK（但 SDK 可简化开发）。

## 支持的模型与核心功能

百炼平台提供多类预训练大语言模型（LLM），包括 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、多模态模型（如 qwen-vl）及推理优化版本（如 qwen-14b-chat-int4）。模型能力覆盖文本生成、代码补全、多轮对话、结构化输出（JSON Schema）、工具调用（Function Calling）等。详细模型列表与适用场景请参阅 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。

> **注意**：[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 文档中描述的 quota 优先级策略与 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 中定义的固定 QPS 限制存在表述差异——实际生效规则以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 为准，后者内容已过时，建议忽略。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `"qwen-turbo"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中列出的名称严格一致；
- `input.messages`：非空消息数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `parameters`（可选）：控制生成行为，常用字段有 `temperature`（0.0–2.0）、`top_p`、`max_tokens`、`stop`、`response_format`（支持 `"text"` 或 `{"type": "json_object"}`）。

Base URL 和地域配置影响请求路由与延迟，详见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md) 与 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（AccessKey ID/Secret）；
2. **构造请求**：使用 `POST /v1/chat/completions`（或 `/v1/completions`）端点，设置 `Authorization: Bearer <API_KEY>`；
3. **发送调用**：参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供的 cURL 示例完成首调验证；
4. （可选）集成官方 Python SDK（`dashscope` >= 1.20.0），自动处理重试、流式响应解析等。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限为 32768（具体依模型而异，qwen-max 支持更高）；
- 免费额度仅适用于部分模型（如 qwen-turbo），qwen-max 等高性能模型默认按量计费；
- 流式响应（`stream=true`）需正确处理 `data:` 分块与 `event: done` 终止信号；
- 所有模型均不支持自定义 LoRA 微调权重在线加载，微调后需部署为独立服务实例；
- 地域选择必须与 API Key 所属项目地域一致，否则返回 `403 Forbidden` ——该约束在 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中有明确说明。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


