# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、调用方式、关键参数配置及常见限制。所有模型均通过统一 API 接口调用，支持同步推理与流式响应。建议首次使用前通读 [开始使用](../../raw/model-user-guide/get-started-with-models.md) 全文，并重点关注地域可用性与限流策略。

## 支持的模型与核心功能

- 当前平台提供多类大语言模型（如 `qwen4-max`、`qwen2.5-72b`、`qwen-audio` 等）及多模态模型，完整列表见 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)  
- 模型能力覆盖文本生成、代码补全、多轮对话、语音转写、图像理解等场景；部分模型支持[函数调用](../concepts/function-calling.md)（Function Calling）和 JSON Schema 输出约束  
- 所有模型均集成于 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 所述的 Model Studio 架构中，统一纳管权限、配额与可观测性

## 关键参数

调用时必需指定以下参数（以 REST API 为例）：

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中一致（如 `qwen4-max`） |
| `input.messages` | array | 是 | 对话历史，格式为 `[{ "role": "user", "content": "..." }]`；`content` 支持纯文本或含 `image_url` 的多模态输入 |
| `parameters.temperature` | number | 否 | 采样温度，默认 `0.8`；设为 `0` 可启用确定性解码（注意：[qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md) 文档明确要求该值 ≥ 0.01） |
| `parameters.max_tokens` | integer | 否 | 最大输出 token 数，默认 `1024`，上限依模型而异 |

> **注意**：`top_p` 与 `temperature` 同时设置时，部分旧版 SDK 可能忽略 `top_p`；请以 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 文档中 `INVALID_PARAMETER` 的校验逻辑为准。

## 使用方式

1. **认证**：在请求 Header 中携带 `Authorization: Bearer <api_key>`，API Key 从控制台「API 密钥管理」获取  
2. **端点**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（文本类）或对应多模态路径  
3. **示例请求体**：
   ```json
   {
     "model": "qwen4-max",
     "input": { "messages": [{ "role": "user", "content": "你好" }] },
     "parameters": { "temperature": 0.5, "max_tokens": 512 }
   }
   ```
4. 响应结构统一包含 `output.text`（主输出）、`usage.input_tokens` / `output_tokens`，流式响应需监听 `event: message` SSE 事件

## 限制和注意事项

- **地域限制**：模型服务仅在 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 列出的 Region 可用（如 `cn-beijing`、`ap-southeast-1`），跨 Region 调用将返回 `REGION_NOT_SUPPORTED` 错误  
- **限流策略**：默认 QPS 为 5，TPM（[Token](../concepts/token.md)s Per Minute）为 10000，具体阈值受账号等级与模型类型影响；详细规则见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)  
- **输入长度**：单次请求 `input.messages` 总 token 数不得超过模型上下文窗口（例如 `qwen4-max` 为 32768），超长将触发 `CONTEXT_LENGTH_EXCEEDED` 错误  
- **安全合规**：禁止输入含 PII、违法或高风险内容；平台会主动拦截并记录违规调用，详情参见 [开始使用](../../raw/model-user-guide/get-started-with-models.md) 中的安全章节

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


