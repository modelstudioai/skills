# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及必须注意的服务限制与兼容性事项。所有操作均基于 RESTful API 接口，无需额外 SDK 即可集成。

## 支持的模型与功能

百炼平台提供多种开源与自研大语言模型，覆盖文本生成、代码补全、多模态理解等场景。模型按能力、尺寸和部署形态分类，包括 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、通义万相（图像生成）及部分第三方模型镜像。完整可用模型列表请参阅 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)。模型能力差异直接影响输入长度、输出格式及计费粒度，建议首次使用前结合 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档比对适用场景。

## 关键参数

调用模型 API 时，必需参数包括 `model`（模型标识符，严格区分大小写）、`input.messages`（对话历史数组，至少含一条 user 角色消息）和 `parameters`（可选，用于控制 temperature、top_p、max_tokens 等）。`model` 值必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中公布的名称完全一致；例如 `qwen-max` 不可写作 `Qwen-Max` 或 `qwen_max`。部分模型不支持 `stream=true` 流式响应，具体以各模型文档说明为准。

## 使用方式

推荐通过 HTTPS POST 请求调用 `/v1/services/aigc/text-generation/generation` 接口。需在 Header 中携带 `Authorization: Bearer <api_key>` 和 `Content-Type: application/json`。请求体结构遵循 OpenAI 兼容格式（但非完全等价），详见 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的完整示例。注意：地域（Region）影响 endpoint 地址和延迟，务必确认所选区域已开通对应模型服务——参考 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限因模型而异（qwen-turbo 为 8K，qwen-max 为 32K），超出将返回 `400 Bad Request` 及错误码 `InvalidParameter.InputLengthExceeded`（见 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)）。
- 默认限流策略为每秒 5 次请求（QPS），突发流量可能触发 `429 Too Many Requests`；如需提升配额，须提交工单申请，不可自行修改 header 中的 `X-RateLimit-Limit`。
> **注意**：[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档中提及的“按账号全局限流”与当前实际生效的“按模型+Region 维度限流”存在表述偏差，以控制台实时配额页显示为准。  
> **注意**：[模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中描述的“统一推理网关”架构已于 2024 年 Q2 迁移至分模型独立网关，旧版 gateway URL 已停用。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


