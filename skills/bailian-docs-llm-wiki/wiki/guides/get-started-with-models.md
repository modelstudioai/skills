# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的主流模型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有内容均基于最新稳定版 API 和控制台能力。

## 支持的模型与功能

百炼平台提供多类大语言模型（LLM）、多模态模型及推理优化模型，覆盖文本生成、代码补全、长上下文理解、图像理解等场景。当前主力模型包括 `qwen-plus`、`qwen-max`、`qwen-turbo` 及最新发布的 `qwen4-max` —— 后者支持 1000K 上下文与增强的工具调用能力，详见 [qwen4-max](../../raw/model-user-guide/get-started-with-models/qwen4-max.md)。完整模型列表及能力对比可查阅 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md)。

> **注意**：文档 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中提及的 `qwen-vl-plus` 已于 v2.3.0 版本起标记为 deprecated，新项目请优先选用 `qwen-vl-max`；该变更未在 [模型服务概览](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中同步说明。

## 关键参数

调用模型 API 时，以下参数为必需或强推荐：

- `model`: 模型标识符（如 `qwen-max`），必须与 [模型列表](../../raw/model-user-guide/get-started-with-models/model-studio-model-list.md) 中公布的名称严格一致；
- `input.messages`: 标准 ChatML 格式消息数组，首条 `role=system` 消息建议不超过 4096 token；
- `parameters.temperature`: 浮点数（0.0–1.0），默认 `0.8`；设为 `0` 时启用确定性采样；
- `parameters.top_p`: 建议保持默认 `0.8`，避免与 `temperature` 同时大幅调整；
- `parameters.max_tokens`: 显式指定响应长度上限，防止超限截断。

## 使用方式

1. **认证**：使用 `Authorization: Bearer <api_key>` 请求头，API Key 从控制台「API 密钥管理」获取；  
2. **端点**：统一调用 `POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；  
3. **示例请求体**：
   ```json
   {
     "model": "qwen-max",
     "input": { "messages": [{"role": "user", "content": "你好"}] },
     "parameters": { "max_tokens": 512 }
   }
   ```
   更多调用示例见 [开始使用](../../raw/model-user-guide/get-started-with-models.md) 文档中的代码片段。

## 限制和注意事项

- 单次请求 `input.messages` 总 token 数上限为模型 context length 的 90%（例如 `qwen4-max` 为 900K），超出将返回 `400 Bad Request`；  
- 默认 QPS 限流为 5，可通过提交工单申请提升，具体策略参见 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md)；  
- 错误响应统一遵循标准结构，含 `code` 与 `message` 字段，常见错误码含义见 [错误码](../../raw/model-user-guide/get-started-with-models/error-code-start.md)；  
- 所有模型仅支持指定地域部署（如 `cn-beijing`, `ap-southeast-1`），跨地域调用将失败，请确认服务端点与 [地域和服务部署范围](../../raw/model-user-guide/get-started-with-models/regions.md) 一致。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


