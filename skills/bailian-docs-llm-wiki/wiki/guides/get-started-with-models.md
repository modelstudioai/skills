# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、基础调用方式，以及生产环境中需关注的限制与注意事项。所有内容均基于最新稳定版本的模型服务接口规范。

## 支持的模型与功能

百炼平台提供多种预训练大语言模型（如 Qwen 系列）及多模态模型，覆盖文本生成、代码补全、对话理解、图像描述等场景。模型能力通过 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 统一呈现，具体可用模型列表详见 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）和自定义系统提示词，但并非全部模型均支持这些扩展功能——请以 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中标注的能力矩阵为准。

## 关键参数

调用模型 API 时，必需参数包括 `model`（模型 ID）、`input.messages`（消息数组，至少含一条 user 角色消息）和 `api_key`（通过 Header 传递）。推荐显式指定 `parameters.temperature`（默认 1.0）和 `parameters.max_tokens`（默认 1024），避免因模型默认行为差异导致输出不稳定。`model` 值必须严格匹配 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中公布的 ID，大小写敏感，且不支持别名或模糊匹配。

## 使用方式

推荐从 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 入手，该文档提供了完整的 cURL 示例、Python SDK 初始化代码及调试技巧。所有模型统一使用 `/v1/services/aigc/text-generation/generation` 接口（POST），认证方式为 Bearer [Token](../concepts/token.md)。注意：SDK 版本 ≥ 3.2.0 才完整支持 Qwen2-VL 等新模型的多模态输入格式；旧版 SDK 可能静默忽略 `input.images` 字段 —— > **注意**：此行为与 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中描述的“自动降级”逻辑存在不一致，建议强制升级至最新 SDK 并校验响应中的 `usage` 字段确认是否实际处理了图像输入。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（字符数）上限为 32768，超出将返回 `400 Bad Request`（错误码 `InvalidParameter.InputMessagesTooLong`，见 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)）；
- 默认调用频次限制为 5 QPS / 账号，突发流量需提前申请配额，详情参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- 模型服务部署在特定地域（如 `cn-beijing`、`cn-shanghai`），跨地域调用将增加延迟并可能触发路由失败，部署前务必核对 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)；
- 流式响应（`stream=true`）下，`max_tokens` 实际生效值可能略低于设定值，这是由于 token 分片边界与流式 chunk 切分策略共同导致，属正常行为，无需重试。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


