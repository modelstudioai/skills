# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API，无需安装额外 SDK 即可开始。

## 支持的模型与核心功能

百炼平台提供多种开源及自研大语言模型（如 Qwen 系列）、多模态模型及推理优化版本（如 Qwen-VL、Qwen2-Audio），支持文本生成、对话理解、代码补全、结构化输出（JSON Schema）等能力。模型列表及适用场景详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型还支持流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）和系统提示词（system prompt）定制，具体能力以各模型文档为准。

## 关键参数

调用模型 API 时，必需参数包括：`model`（模型 ID，如 `qwen-max`）、`input.messages`（消息数组，含 `role` 和 `content` 字段）。推荐显式指定 `parameters.temperature`（默认 1.0）和 `parameters.max_tokens`（默认 2048）以控制生成行为。`stream` 参数控制是否启用流式响应（布尔值）。所有参数定义与取值范围请参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的请求示例与字段说明。

> **注意**：`top_p` 和 `frequency_penalty` 在 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档中标注为“部分模型支持”，但实际在 v2.3+ API 中已统一支持所有 Qwen 系列模型；旧版文档未及时更新，建议以 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 的参数表为准。

## 使用方式

1. 获取 API Key（通过百炼控制台「API 密钥管理」创建）  
2. 构造请求：使用 `POST /v1/chat/completions` 端点，Header 包含 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`  
3. 设置 Base URL：根据部署地域选择对应域名，例如杭州地域为 `https://dashscope.aliyuncs.com/api/v1`，完整列表见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)  
4. 发送请求并处理响应（含错误码解析，如 `429 Too Many Requests` 表示触发限流）

## 限制和注意事项

- 单次请求 `input.messages` 总长度上限为 32768 token（具体依模型而异），超长输入将被截断或返回 `400 Bad Request`  
- 默认调用频率限制为 10 QPS（每秒查询数），可通过 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 页面申请提升配额  
- 模型服务按地域隔离，跨地域调用将失败；务必确认所选模型在目标地域已发布，并使用对应 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中的接入地址  
- 流式响应中 `delta.content` 可能为空字符串（尤其在[函数调用](../concepts/function-calling.md)场景），客户端需容错处理

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


