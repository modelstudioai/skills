# get started with models

百炼平台提供统一的模型调用入口，支持通过 API 快速接入多种大语言模型与多模态模型。本文档指导开发者完成模型选择、参数配置与首次调用，涵盖基础能力、关键约束及常见问题排查路径。所有模型均需通过 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中定义的 Model Studio 统一管理。

## 支持的模型与功能

- 当前支持 Qwen 系列（如 `qwen4-max`、`qwen2.5-plus`）、通义万相、语音合成等模型，完整列表见 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)  
- 多数模型支持文本生成、[函数调用](../concepts/function-calling.md)（tool calling）、流式响应；部分模型（如 `qwen4-max`）额外支持长上下文（最高 1M tokens）与结构化输出（JSON mode）  
- 多模态能力（图像理解、文档解析）需显式指定 `input.files` 参数，并确保文件类型与模型兼容 —— 具体支持范围请参考 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中一致（如 `qwen4-max`） |
| `input.messages` | array | 是 | 对话消息数组，格式为 `[{role: 'user', content: '...'}]`；`system` 角色仅部分模型支持 |
| `parameters.temperature` | number | 否 | 默认 `0.8`，取值范围 `[0, 2]`；设为 `0` 可启用确定性输出（非所有模型均生效） |
| `parameters.top_p` | number | 否 | 默认 `0.95`，建议与 `temperature` 避免同时调整 |

> **注意**：`max_tokens` 在部分旧版文档中被描述为“硬上限”，但实际行为由模型自身实现决定；`qwen4-max` 的 `max_tokens` 仅影响输出长度上限，不控制输入截断 —— 详见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md) 文档说明。

## 使用方式

1. **认证**：使用 `X-DashScope-Access-Token` 请求头传入 API Key（推荐通过环境变量或密钥管理服务注入）  
2. **请求**：向 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation` 发送 POST 请求（其他模型类型路径不同，参见 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)）  
3. **响应解析**：检查 `output.choices[0].message.content`；若含错误，优先对照 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 定位原因  

## 限制和注意事项

- 所有模型受统一 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 策略约束（按 Token 数与 QPS 双维度），突发流量需主动降级或排队  
- 输入内容长度受模型最大上下文限制（如 `qwen2.5-plus` 为 32K，`qwen4-max` 为 1M），超长输入将被静默截断，**不会报错**  
- 跨地域调用可能增加延迟或触发地域白名单校验，请严格遵循 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 中的 endpoint 映射规则  
- 不支持在单次请求中混合调用多个模型；如需链式调用，须由客户端自行编排

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


