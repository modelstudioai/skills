# get started with models

百炼平台提供统一的模型调用入口，支持通过 API 快速接入多种大语言模型、多模态模型及推理优化模型。本文档梳理了模型使用的起点路径、关键配置项、调用方式及常见约束，适用于首次集成模型服务的开发者。所有模型均需通过 Model Studio 管理和调用，实际可用模型以控制台实时列表为准。

## 支持的模型与核心功能

- 当前支持的模型类型包括：通用大语言模型（如 Qwen 系列）、代码模型、多模态理解/生成模型，以及部分专有推理优化模型。  
- 模型能力覆盖文本生成、结构化输出（JSON Schema）、[函数调用](../concepts/function-calling.md)（Function Calling）、流式响应、长上下文（最高 1M tokens）等。  
- 完整可选模型列表请参考 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)；新发布的预览模型（如 `qwen4-max-preview`）详情见 [qwen4-max-preview](../../raw/model-user-guide/get-started-with-models/qwen4-max-preview.md)。

## 关键参数

调用模型 API 时，以下参数为必需或强推荐设置：

| 参数名 | 类型 | 说明 |
|--------|------|------|
| `model` | string | 模型 ID，必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中一致，区分大小写和版本后缀（如 `qwen3`、`qwen3-32b`） |
| `input.messages` | array | 至少包含一个 `role: user` 的消息对象；系统提示词（system prompt）需显式传入 `role: system` |
| `parameters.temperature` | number | 控制输出随机性，范围 `[0.0, 2.0]`；设为 `0` 表示确定性采样（greedy decoding） |
| `parameters.max_tokens` | integer | 输出最大 token 数，不同模型有硬上限（如 `qwen3` 默认 8192，`qwen4-max-preview` 支持 1M） |

> **注意**：部分旧文档中提及的 `top_p` 默认值为 `1.0`，但当前所有模型默认行为已统一为 `top_p: 1.0` 且不可省略——若未显式传入，API 将返回参数校验错误。请始终在 `parameters` 中完整声明所需采样参数。

## 使用方式

1. **获取凭证**：在百炼控制台「API 密钥」页创建 AccessKey（AK/SK），用于签名认证；  
2. **构造请求**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（文本生成）或对应服务端点发送 POST 请求；  
3. **签名与 Header**：使用 AK/SK 对请求签名（HMAC-SHA256），并设置 `Content-Type: application/json` 和 `Authorization: Bearer <token>`（其中 `<token>` 由 `dashscope` SDK 自动生成，或手动调用 `/tokens` 接口获取）；  
4. **调试建议**：首次调用推荐使用 `curl` 或 Postman 验证基础流程，再集成 SDK；错误排查请对照 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 文档定位原因。

## 限制和注意事项

- **地域限制**：模型服务仅在指定地域部署，调用前需确认所选模型在目标 Region 可用，详见 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)；  
- **限流策略**：按 AccessKey 维度实施 QPS 和 TPS 双重限制，超出将返回 `429 Too Many Requests`；具体配额见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；  
- **输入长度**：单次请求 `input.messages` 总 token 数不得超过模型上下文窗口（如 `qwen3` 为 32768，`qwen4-max-preview` 为 1048576），超长将被截断并触发警告日志；  
- **安全合规**：所有输入内容将经过内容安全过滤，含违规内容的请求将被拒绝并返回 `400 Bad Request`，不计入配额。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


