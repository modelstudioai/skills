# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及必须注意的服务限制与兼容性事项。所有操作均基于 RESTful API 接口，无需安装额外 SDK 即可开始。

## 支持的模型与核心功能

百炼平台提供多种开源与自研大语言模型（如 Qwen 系列）、多模态模型及推理优化版本（如 `qwen-max`、`qwen-plus`、`qwen-turbo`），覆盖通用对话、长文本理解、代码生成等场景。模型能力与部署状态可通过 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 实时查询。部分模型还支持流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）和系统提示词（system prompt）定制，具体能力以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档为准。

> **注意**：[模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中提及的“本地模型沙箱调试”功能已在 v2.3 版本中移除，当前仅支持云上托管模型调用，请以 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 的流程为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型 ID（如 `qwen-turbo`），必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中公布的 ID 完全一致；
- `input.messages`：非空消息数组，至少包含一个 `user` 角色消息；
- `parameters.temperature`：控制输出随机性（0.0–2.0），默认为 1.0；  
其他常用参数包括 `top_p`、`max_tokens`、`stream`（布尔值）等，完整定义见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md)。

## 使用方式

1. 在百炼控制台开通模型服务并获取 API Key；
2. 构造 HTTP POST 请求，目标 URL 为 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；
3. 设置请求头：`Authorization: Bearer <your_api_key>`，`Content-Type: application/json`；
4. 发送 JSON payload（参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的示例）；
5. 解析响应体中的 `output.text` 或流式 chunk 数据。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限因模型而异（例如 `qwen-turbo` 为 8K，`qwen-max` 为 32K），超出将返回 `400 Bad Request` 错误；
- 默认调用频次限制为 10 QPS / 账号，突发流量需提前申请配额，详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- 模型服务按地域部署，调用时需确保 API Endpoint 与所选 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 一致，否则可能返回 `404 Not Found`；
- 所有错误码含义请查阅 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)，其中 `InvalidParameter.ModelNotFound` 表示模型 ID 不存在或未授权。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


