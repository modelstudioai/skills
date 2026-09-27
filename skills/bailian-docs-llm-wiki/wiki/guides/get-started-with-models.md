# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API，无需安装额外 SDK 即可开始。

## 支持的模型与功能

百炼平台提供多种开源与自研大模型，包括 Qwen 系列（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）、多模态模型（如 `qwen-vl`）及嵌入模型（如 `text-embedding-v1`）。模型能力覆盖文本生成、代码补全、多轮对话、图像理解与[向量化](../concepts/embedding.md)等场景。具体模型列表及适用场景详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）和工具集成，相关能力说明见 [产品简介](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型 ID（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：非空消息数组，首条消息 `role` 应为 `"user"`；
- `parameters.temperature`：控制输出随机性（0.0–2.0，默认 1.0）；
- `parameters.top_p`：核采样阈值（0.0–1.0，默认 0.8）；
- `parameters.max_tokens`：最大生成 token 数（硬上限，超出将被截断）。

> **注意**：`parameters.stop` 字段在部分旧文档中被描述为支持字符串数组，但实际 API 仅接受字符串（单个终止符）或省略；请以 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的示例为准。

## 使用方式

1. **获取认证凭证**：在百炼控制台创建 API Key（`Authorization: Bearer <api_key>`）；
2. **确定接入地址**：根据部署地域选择 Base URL，例如华东 1（杭州）使用 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；完整域名映射见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
3. **构造请求**：发送 `POST` 请求，`Content-Type: application/json`，Body 包含 `model` 和 `input` 字段；
4. **处理响应**：成功响应包含 `output.text` 或 `output.choices[0].message.content`，流式响应需按 SSE 格式解析。

## 限制和注意事项

- 每个 API Key 默认享有动态配额，受账户等级与资源包影响；配额策略与实时调整机制参见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)；
- 同步调用单次请求最大 `input` 长度为 32768 tokens，`max_tokens` 上限为 8192（部分模型更低，以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 标注为准）；
- 限流规则按分钟级窗口统计，超限返回 `429 Too Many Requests`；详细规则见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- 跨地域调用可能导致延迟升高或不可用，请务必通过 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 确认服务可用性。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


