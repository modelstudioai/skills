# get started with models

本文档介绍如何快速开始使用百炼平台的模型服务，涵盖模型选择、调用方式、关键参数配置及常见限制。开发者可基于自身业务场景选择合适的模型，并通过 API 或控制台完成集成。所有模型均需通过百炼平台统一鉴权和路由。

## 支持的模型与功能

百炼平台提供多类大语言模型（LLM）、多模态模型及专用小模型，覆盖文本生成、代码补全、图像理解等能力。最新模型如 `qwen4-max-preview` 已开放试用，其能力与性能详见 [qwen4-max-preview（最新模型）](../../raw/model-user-guide/get-started-with-models/qwen4-max-preview.md)。完整模型列表可通过控制台或 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 文档查阅。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）和自定义 system prompt。

## 关键参数

调用模型时需指定以下必选参数：  
- `model`: 模型 ID（如 `qwen3`、`qwen4-max-preview`），必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中所列一致；  
- `input.messages`: 非空消息数组，至少包含一个 `user` 角色消息；  
- `parameters.temperature`、`top_p` 等采样参数为可选，但建议显式设置以保障结果稳定性。  
所有参数命名与语义严格遵循 [OpenAI 兼容接口](../concepts/openai-compatible-interface.md)规范，兼容性细节见 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md)。

## 使用方式

1. **API 调用**：使用 HTTPS POST 请求至 `/v1/chat/completions`，携带 `Authorization: Bearer <api_key>` 头；  
2. **控制台调试**：登录百炼控制台 → 进入「模型 Studio」→ 选择目标模型 → 在「在线调试」页填写输入并执行；  
3. **SDK 集成**：推荐使用官方 Python SDK（`dashscope` v1.20.0+），初始化时传入 `api_key` 即可自动处理重试与限流适配。

## 限制和注意事项

- 单次请求最大 token 数受模型本身限制（如 `qwen4-max-preview` 上限为 32768），超出将返回 `400 Bad Request`；  
- 默认 QPS 限流为 5，如需提升请提交工单申请，具体策略详见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；  
- 所有模型仅在杭州、上海、北京、深圳等[地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md)内可用，跨地域调用将失败；  
> **注意**：文档中提及的 `qwen4-max-preview` 当前仅支持 `chat` 类型调用，不支持 `embedding` 或 `rerank` 接口——该限制未在 [qwen4-max-preview（最新模型）](../../raw/model-user-guide/get-started-with-models/qwen4-max-preview.md) 中明确说明，以实际 API 响应为准。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


