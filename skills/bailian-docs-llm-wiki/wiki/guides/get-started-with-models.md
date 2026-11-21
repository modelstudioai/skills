# get started with models

百炼平台提供统一的模型调用入口，支持通过 API 快速接入多种大语言模型、多模态模型及推理优化模型。本文档指导开发者完成模型选择、参数配置与首次调用，涵盖基础能力、关键约束及常见问题排查路径。所有模型均需通过 Model Studio 管理和授权，调用前请确保已开通对应模型服务。

## 支持的模型与核心功能

- 当前支持 Qwen 系列（如 `qwen4-max`、`qwen2.5-plus`）、通义万相、语音合成等模型，具体列表见 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)  
- 模型能力覆盖文本生成、结构化输出（JSON Schema）、流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）及多轮对话状态管理  
- 部分模型支持图像/音频输入（如 `qwen-vl-plus`），详细输入格式要求参见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md) 文档中的 multimodal 输入示例  

> **注意**：[模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中提及的“自动模型路由”功能在 v2.3+ SDK 中已默认启用，但旧版 API（`/v1/chat/completions`）仍需显式指定 `model` 参数；若未指定，将返回 400 错误而非自动降级，该行为与文档中“默认 fallback”的描述存在不一致。

## 关键参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `model` | string | 是 | 模型 ID，必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中完全一致（区分大小写，如 `qwen4-max`） |
| `input.messages` | array | 是 | 至少包含一个 `role: "user"` 的 message，`content` 支持字符串或含 `image_url` 的对象（多模态场景） |
| `parameters.temperature` | number | 否 | 取值范围 0.0–2.0，默认 1.0；部分模型（如 `qwen4-max`）对 >1.2 的值会强制截断，详见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md) |
| `stream` | boolean | 否 | 设为 `true` 启用流式响应，需按 SSE 格式解析 |

## 使用方式

1. 在 Model Studio 中为项目启用目标模型（如 `qwen4-max`），获取 API Key 和 Endpoint  
2. 发送 POST 请求至 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（通用 endpoint）  
3. 设置请求头：`Authorization: Bearer <API_KEY>`，`Content-Type: application/json`  
4. 示例请求体（非流式）：
```json
{
  "model": "qwen4-max",
  "input": {
    "messages": [{"role": "user", "content": "你好"}]
  },
  "parameters": {"temperature": 0.8}
}
```

## 限制和注意事项

- **地域限制**：模型服务仅在杭州、上海、北京、深圳、新加坡等[指定地域](../../raw/model-user-guide/get-started-with-models/regions.md)可用，跨地域调用将失败  
- **限流策略**：默认 QPS 为 5（每秒请求数），TPM（Tokens Per Minute）因模型而异，详情见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；超限返回 `429 Too Many Requests`，错误码定义参考 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)  
- **输入长度**：`qwen4-max` 最大上下文为 32768 tokens，但单次 `input.messages` 总长度（含 system prompt）不得超过 28672 tokens，超出将触发 `InvalidParameter.InputLengthExceeded`  
- **认证要求**：所有调用必须携带有效 API Key；使用 RAM 子账号时，需授予 `dashscope:InvokeModel` 权限，否则返回 `AccessDenied`（该权限项未在 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中明确列出，属必要补充）

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


