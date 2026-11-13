# get started with models

百炼平台提供统一的模型调用入口，支持通过 API 快速接入多种大语言模型、多模态模型及推理优化模型。本文档指导开发者完成模型选择、参数配置与首次调用，适用于生产环境集成。所有模型均通过 Model Studio 统一管理与发布，具体能力以 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中定义为准。

## 支持的模型与功能

- 当前支持 Qwen 系列（如 `qwen2.5-72b-instruct`、`qwen2-vl-7b-instruct`）、`qwen4-max-preview`（预览版，详见 [qwen4-max-preview（最新模型）](../../raw/model-user-guide/get-started-with-models/qwen4-max-preview.md)）等主流模型；
- 支持文本生成、结构化输出（JSON Schema）、流式响应、工具调用（Function Calling）及多模态输入（图像+文本）；
- 完整可选模型列表请参考 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)，该列表实时同步 Model Studio 控制台状态。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中一致，例如 `"qwen2.5-72b-instruct"`；不支持别名或旧版命名（如 `qwen-max` 已弃用） |
| `input.messages` | array | 是 | 对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；多模态需按 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 规范传入 base64 图像 |
| `parameters.temperature` | number | 否 | 取值范围 0.0–2.0，默认 1.0；部分模型（如 `qwen4-max-preview`）对温度敏感度更高，建议从 0.7 开始调试 |

> **注意**：`max_tokens` 参数在部分旧文档中被描述为“默认 2048”，但实际行为由模型自身上下文窗口决定，且 `qwen4-max-preview` 默认上限为 32768 —— 请以 [qwen4-max-preview（最新模型）](../../raw/model-user-guide/get-started-with-models/qwen4-max-preview.md) 的说明为准，勿依赖通用默认值。

## 使用方式

1. **获取 API Key**：在百炼控制台「API 密钥」页面创建并复制密钥；
2. **构造请求**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（文本）或 `/services/aigc/multimodal-generation/generation`（多模态）发送 POST 请求；
3. **验证响应**：检查 `output.text` 字段；若返回错误，依据 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 定位问题（如 `InvalidParameter.ModelNotFound` 表示模型 ID 错误）；
4. **限流处理**：默认 QPS 为 5，超出将返回 `429 Too Many Requests`；详细配额规则见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)。

## 限制和注意事项

- 所有模型仅支持指定地域部署，调用前需确认服务端点与 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 一致（例如 `cn-beijing` 不支持 `qwen2-vl-7b-instruct`）；
- 输入内容长度受模型上下文窗口限制，超长将被截断且不报错；建议主动分块或使用 `truncate` 参数（部分模型支持）；
- 流式响应（`stream: true`）需客户端正确处理 SSE 格式，否则可能解析失败；
- 预览模型（如 `qwen4-max-preview`）接口与行为可能变更，上线前务必阅读其专属文档 [qwen4-max-preview（最新模型）](../../raw/model-user-guide/get-started-with-models/qwen4-max-preview.md)。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


