# get started with models

百炼平台提供统一的模型调用入口，支持通过 API 快速接入多种大语言模型、[多模态](../concepts/multi-modal.md)模型及推理优化模型。本文档指导开发者完成模型选择、参数配置与首次调用，涵盖基础能力、关键约束及常见问题排查路径。所有模型均需通过 Model Studio 管理和授权，调用前请确保已开通对应模型服务。

## 支持的模型与核心功能

- 当前支持的模型包括 `qwen2.5-7b`、`qwen2.5-72b`、`qwen-vl-plus`、`qwen-audio` 及最新发布的 `qwen4-max`（详见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md)）。
- 模型能力覆盖文本生成、结构化输出（JSON Schema）、[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应、多轮对话状态管理等。
- 完整可用模型列表以 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 为准；该页面实时同步 Model Studio 中已启用且授权成功的模型。

## 关键参数

- `model`: 必填，值必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中显示的模型 ID 完全一致（区分大小写，如 `qwen4-max` 不可写作 `Qwen4-Max`）。
- `input.messages`: 至少包含一条 `role: "user"` 的消息；系统提示词（`role: "system"`）仅在部分模型中生效，具体支持情况见各模型文档。
- `parameters.temperature`、`top_p`、`max_tokens` 等控制生成行为的参数，其有效范围因模型而异，请参考对应模型的参数说明页。

## 使用方式

1. 登录百炼控制台 → 进入 **Model Studio** → 选择目标模型 → 点击「部署」并完成授权；
2. 获取 API Key（需在「API 密钥管理」中创建）；
3. 发送 POST 请求至 `/v1/services/aigc/text-generation/generation`（文本类）或 `/v1/services/aigc/multimodal-generation/generation`（[多模态](../concepts/multi-modal.md)类），请求体为标准 OpenAI 兼容格式；
4. 示例调用可参考 [开始使用](../../raw/model-user-guide/get-started-with-models.md) 文档中的 curl 片段。

> **注意**：原始文档中 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 提到“所有模型默认在 cn-beijing 可用”，但实际 `qwen4-max` 目前仅在 `cn-shanghai` 和 `cn-hangzhou` 上线（见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md)）。请以具体模型文档的 region 支持列表为准。

## 限制和注意事项

- 所有模型均受统一限流策略约束，单位时间内调用次数和总 tokens 数分别受限，详情参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；
- 输入内容长度、上下文窗口、输出最大 token 数等硬性限制由模型本身决定，超出将返回 `400 Bad Request` 或触发截断，错误码含义请查阅 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)；
- 模型调用日志默认保留 7 天，如需审计或调试，建议客户端自行记录 request_id 与输入输出。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


