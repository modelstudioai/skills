# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的主流模型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有内容均基于最新稳定版 API 和控制台能力。

## 支持的模型与功能

百炼平台提供多类大语言模型（LLM）、多模态模型及推理优化版本，覆盖文本生成、代码补全、长上下文理解、图像理解等场景。当前主力模型包括 `qwen2.5-7b`、`qwen2.5-72b`、`qwen-vl-plus` 和 `qwen4-max`（详见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md)）。完整模型列表可通过控制台或 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 页面实时查看。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）和自定义 system [prompt](prompt.md)。

> **注意**：[选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档中提及的 `qwen1.5-110b-chat` 已于 2024 年 Q3 下线，实际可用模型请以 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 为准。

## 关键参数

调用模型 API 时，必需参数包括 `model`（模型 ID，如 `"qwen2.5-7b"`）、`input.messages`（消息数组，至少含一个 user 角色消息）。推荐设置 `parameters.temperature`（默认 0.8）和 `parameters.max_tokens`（默认 1024，最大 32768）。对于 `qwen4-max` 等高阶模型，需显式指定 `parameters.top_p` 和 `parameters.repetition_penalty` 以保障输出稳定性（参见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md)）。

## 使用方式

1. 在百炼控制台开通模型服务并获取 API Key；
2. 构造 HTTP POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；
3. 设置 `Authorization: Bearer <API_KEY>` 和 `Content-Type: application/json`；
4. 提交 JSON payload（结构参考 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)）；
5. 解析响应中的 `output.text` 或流式 `output.choices[].delta.content`。

## 限制和注意事项

- 免费试用额度为 1000 次调用/月，超出后按量计费；
- 单次请求 `input.messages` 总 token 数上限为 32768（`qwen4-max` 支持 1M 上下文，但需使用专用 endpoint）；
- 限流策略为 10 QPS / 账号（突发允许 20 QPS），详情见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- 错误响应统一遵循标准格式，常见错误码含义请查阅 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)；
- 模型服务部署地域影响延迟与合规性，支持地域列表见 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


