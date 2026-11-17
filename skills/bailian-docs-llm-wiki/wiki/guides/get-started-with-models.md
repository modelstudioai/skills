# get started with models

百炼平台提供统一的模型调用入口，支持通过 API 快速接入多种大语言模型、多模态模型及推理优化模型。本文档指导开发者完成模型选择、参数配置与首次调用，涵盖基础能力、关键约束及常见问题排查路径。所有模型均通过 Model Studio 统一管理，调用前需确保已开通对应模型服务权限。

## 支持的模型与核心功能

当前平台支持 Qwen 系列（如 `qwen4-max`、`qwen2.5-plus`）、Qwen-VL 多模态模型及部分第三方精调模型，具体以 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 为准。模型能力覆盖文本生成、代码补全、结构化输出（JSON Schema）、工具调用（Function Calling）及图像理解等。部分模型支持流式响应和系统提示词（`system` role），但并非全部兼容——详见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md) 的能力说明。

> **注意**：[选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档中列出的部分旧版模型（如 `qwen1.5-72b-chat`）已在控制台下线，实际可用模型请以 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 实时数据为准。

## 关键参数

必填参数包括 `model`（模型 ID，区分大小写）、`input.messages`（消息数组，至少含 `role` 和 `content` 字段）。推荐显式设置 `parameters.temperature`（默认 0.8）和 `parameters.max_tokens`（默认 2048，不同模型上限不同）。`stream` 参数控制是否启用流式响应（布尔值），启用后需按 SSE 协议解析响应体。所有参数定义与取值范围详见 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 使用方式

1. 在百炼控制台开通目标模型服务（如 `qwen4-max`）；
2. 获取 API Key（位于「API 密钥管理」）；
3. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`，Header 中携带 `Authorization: Bearer <api_key>`；
4. 请求体为 JSON，结构参考 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中的示例。

## 限制和注意事项

- 免费调用量受账号等级限制，超出后触发限流；详细配额与错误码见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 和 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)；
- 模型部署地域影响延迟与可用性，中国大陆用户建议优先选用 `cn-beijing` 或 `cn-hangzhou` 区域，具体支持情况参见 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)；
- 输入内容长度、输出长度及并发请求数均存在硬性限制，单次请求 `input.messages` 总 token 数不得超过模型 context length（如 `qwen4-max` 为 32768），超限将返回 `400 Bad Request`。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


