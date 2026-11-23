# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、调用方式、关键参数配置及常见限制。所有模型均通过统一 API 接口调用，支持同步推理与流式响应。建议首次使用前通读 [开始使用](../../raw/model-user-guide/get-started-with-models.md) 全文，并重点关注地域可用性与限流策略。

## 支持的模型与核心功能

- 当前平台提供多类大语言模型（如 `qwen4-max`、`qwen2.5-72b`、`qwen-audio` 等）及多模态模型，完整列表见 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)  
- 模型能力覆盖文本生成、代码补全、结构化输出（JSON Schema）、工具调用（Function Calling）、长上下文（最高 1M tokens）及音视频理解等  
- 所有模型均集成在 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 定义的统一抽象层中，无需为不同模型适配独立 SDK

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 模型 ID，必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中一致（如 `qwen4-max`） |
| `input.messages` | array | 是 | 对话消息数组，格式为 `[{ "role": "user", "content": "..." }]`；`content` 可为字符串或含 `image_url`/`audio_url` 的对象 |
| `parameters.temperature` | number | 否 | 采样温度，默认 `0.8`；设为 `0` 启用确定性解码（推荐用于结构化输出） |
| `parameters.max_tokens` | integer | 否 | 最大输出 token 数，上限取决于模型（如 `qwen4-max` 为 8192） |

> **注意**：`qwen4-max` 的实际最大输出长度在 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md) 中标注为 32768，但当前 API 实际限制仍为 8192 —— 请以 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md) 中 `InvalidParameter.MaxTokensExceeded` 的触发阈值为准。

## 使用方式

1. **认证**：使用 `X-DashScope-Access-Token` 请求头传入 API Key（需在控制台开通模型权限）  
2. **端点**：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`（文本模型）或 `/services/aigc/multimodal-generation/generation`（多模态）  
3. **示例请求体**：
   ```json
   {
     "model": "qwen4-max",
     "input": {
       "messages": [{"role": "user", "content": "用 Python 写一个快速排序"}]
     },
     "parameters": {"temperature": 0.1, "max_tokens": 1024}
   }
   ```
4. 响应结构统一，结果位于 `output.text`（文本）或 `output.choices[0].message.content`（兼容 OpenAI 格式）

## 限制和注意事项

- **地域限制**：模型服务仅在 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 列出的 Region 可用（如 `cn-beijing`, `ap-southeast-1`），跨 Region 调用将返回 `RegionNotSupported` 错误  
- **限流策略**：默认 QPS 为 5，TPM（Token Per Minute）为 10000，具体配额见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；超出后返回 `RateLimitExceeded` 错误码  
- **输入长度**：单次请求总 token（prompt + completion）不得超过模型 context window；超长输入将被截断且不报错，建议客户端预估并分片处理  
- **调试建议**：首次调用失败时，优先检查 `X-DashScope-Access-Token` 权限、`model` 字符串拼写、以及是否在支持地域内 —— 这些是 [开始使用](../../raw/model-user-guide/get-started-with-models.md) 中强调的三大高频问题

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


