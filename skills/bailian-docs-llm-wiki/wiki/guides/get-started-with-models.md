# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API 或 SDK 实现，无需部署模型本身。

## 支持的模型与核心功能

百炼平台提供多类预训练大语言模型（LLM）、多模态模型及专用小模型，覆盖文本生成、代码补全、对话理解、图像描述等场景。模型列表持续更新，具体支持情况请参考 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。除基础推理外，平台还支持流式响应、系统提示词（system prompt）、工具调用（function calling）等高级能力，详见 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

> **注意**：部分文档中提及的“默认启用 long-context 模式”与当前 v3.2 API 行为不一致——实际需显式传入 `max_tokens` 且 `top_p=1.0` 才能稳定触发长上下文处理逻辑；该差异已在 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 的示例中修正。

## 关键参数

调用模型 API 时，以下参数为必需或强推荐：

- `model`: 模型标识符（如 `qwen-max`, `qwen-plus`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中列出的名称严格一致；
- `input.messages`: 非空消息数组，格式为 `[{ "role": "user", "content": "..." }]`；
- `parameters.temperature`: 控制输出随机性，建议生产环境设为 `0.1–0.8`；
- `parameters.top_p`: 推荐设为 `0.95` 或 `1.0`，避免与 `temperature` 同时高值导致不稳定；
- `parameters.max_tokens`: 显式指定最大生成长度，否则可能因模型默认截断引发意外交互中断。

## 使用方式

1. **获取 API Key**：在控制台「API 密钥管理」中创建并复制密钥；
2. **构造请求**：使用 `POST /v1/services/aigc/text-generation/generation` 端点，Header 中携带 `Authorization: Bearer <api_key>`；
3. **发送调用**：参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供的 cURL 和 Python 示例；
4. **处理响应**：检查 `output.text` 字段，同时务必解析 `usage.input_tokens` 和 `usage.output_tokens` 用于配额监控。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含角色标记）不得超过模型 context window 的 90%，超限将返回 `400 Bad Request`（错误码 `InvalidParameter.InputLengthExceeded`，见 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)）；
- 免费试用额度按自然日重置，超出后请求将被 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 拦截，而非直接拒绝；
- 同一 API Key 下并发请求超过 10 QPS 将触发 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)，建议客户端实现指数退避；
- 不支持跨区域调用（例如华东 region 的 key 不能调用华北 endpoint），region 必须与控制台项目所在地域一致。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


