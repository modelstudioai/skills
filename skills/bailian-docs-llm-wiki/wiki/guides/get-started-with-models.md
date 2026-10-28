# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API，无需安装额外 SDK 即可开始。

## 支持的模型与核心功能

百炼平台提供多种开源及自研大语言模型（如 Qwen 系列）、多模态模型及推理优化版本（如 Qwen-VL、Qwen2-Audio），支持文本生成、对话理解、代码补全、结构化输出（JSON Schema）等能力。模型列表及适用场景详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型还支持流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）和系统提示词（system [prompt](prompt.md)）定制，具体能力以各模型文档为准。

## 关键参数

调用模型 API 时，必需参数包括：`model`（模型 ID，如 `qwen-max`）、`input.messages`（消息数组，含 `role` 和 `content` 字段）。推荐显式指定 `parameters.temperature`（默认 0.85）和 `parameters.max_tokens`（默认 1024，最大 8192）。`stream` 参数控制是否启用流式响应（布尔值）。注意：`top_p`、`repetition_penalty` 等高级参数在 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中有完整示例说明。

> **注意**：[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档中描述的每分钟请求数（RPM）限制已过时；当前统一采用动态配额机制，实际可用额度由账户等级与 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 策略共同决定，请以控制台实时配额为准。

## 使用方式

1. 获取 API Key（在百炼控制台「API 密钥管理」中创建）  
2. 构造请求：使用 `POST /v1/chat/completions` 接口，Header 中设置 `Authorization: Bearer <your_api_key>`  
3. Base URL 需根据部署地域选择，例如华东 1（杭州）为 `https://dashscope.aliyuncs.com/api/v1`；完整域名列表见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)  
4. 地域与服务范围必须匹配，否则返回 403；详细配置规则参见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限为 32768（不同模型可能更低，以 `/models/{model_id}` 接口返回的 `max_context_length` 为准）  
- 流式响应下，`max_tokens` 实际生效值可能受服务端缓冲策略影响，建议预留 10% 余量  
- 不支持跨地域调用：若 API Key 在华北 2 创建，则不可用于调用华东 1 的 `qwen-plus` 实例  
- 所有模型调用均需通过 HTTPS，HTTP 请求将被拒绝  
- 模型输入中禁止包含恶意指令、越权操作提示或绕过安全过滤器的内容，违反者将触发风控拦截

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


