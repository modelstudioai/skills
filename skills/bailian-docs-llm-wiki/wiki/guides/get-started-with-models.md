# get started with models

本文档面向开发者，介绍如何快速开始调用百炼平台提供的大模型服务。核心包括模型选择、API 调用方式、关键参数配置及基础限制说明。所有操作均基于标准 RESTful API 接口，无需额外 SDK 即可集成。

## 支持的模型与功能

百炼平台提供多类预训练与微调模型，覆盖文本生成、代码补全、多模态理解等场景。模型列表及能力概览详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（function calling）和系统提示词（system prompt）设置；具体支持情况需以各模型文档为准。动态限流策略也按模型维度独立配置，参考 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。

## 关键参数

调用模型 API 时，必需参数包括 `model`（模型 ID）、`input.messages`（消息数组）和认证头 `Authorization: Bearer <api_key>`。推荐显式指定 `parameters.temperature`（默认为 1.0）和 `parameters.max_tokens`（默认为 1024），避免因平台默认值变更导致行为不一致。地域与接入域名需匹配所选服务部署范围，详见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)。

## 使用方式

1. 获取 API Key：在百炼控制台「API 密钥管理」中创建；
2. 确定 Base URL：根据目标地域和服务类型选择，完整列表见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
3. 构造请求：使用 `POST /v1/chat/completions`（或对应接口路径），JSON body 示例：
   ```json
   {
     "model": "qwen-max",
     "input": { "messages": [{"role": "user", "content": "你好"}] },
     "parameters": { "temperature": 0.7, "max_tokens": 512 }
   }
   ```
4. 首次调用验证：建议从 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的最小可行示例入手，确认网络连通性与鉴权有效性。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（token 数）受模型上下文窗口限制，超长将返回 400 错误；
- 默认 QPS 限制为 5，可通过控制台申请提升，但实际生效值以 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档中当前配额为准；
- > **注意**：[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 与 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 两篇文档对配额继承逻辑描述存在差异——前者强调按模型组聚合限流，后者未提及分组机制。请以控制台实时显示的「模型级 QPS 配额」为准，API 响应头 `X-RateLimit-Remaining` 为最终依据。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


