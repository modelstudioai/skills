# get started with models

本文档面向开发者，介绍如何快速开始调用百炼平台提供的大模型服务。核心包括模型选择、API 调用方式、关键参数配置及基础限制说明。所有操作均基于标准 RESTful API 接口，无需额外 SDK 即可集成。

## 支持的模型与功能

百炼平台提供多类预训练与微调模型，覆盖文本生成、代码补全、多模态理解等场景。模型列表及能力概览详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（function calling）和系统提示词（system prompt）设置，具体以各模型文档为准。注意：[产品简介](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 中提及的“实时语音转写模型”当前尚未开放公测，实际可用模型请以控制台或 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 页面为准。

## 关键参数

调用模型 API 时，必需参数包括 `model`（模型 ID）、`input.messages`（消息数组）和认证头 `Authorization: Bearer <api_key>`。推荐显式指定 `parameters.temperature`（默认 1.0）和 `parameters.max_tokens`（默认 1024），避免因平台默认值变更导致行为不一致。地域相关参数（如 `region`）影响接入域名和延迟，需与 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中声明的可用区域匹配。

## 使用方式

1. 在百炼控制台开通模型服务并获取 API Key；  
2. 根据目标模型确定 Base URL —— 全部可用地址汇总见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；  
3. 构造 POST 请求，例如首次调用千问系列模型可参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的 cURL 示例；  
4. 建议在生产环境启用重试逻辑（指数退避）并监控 HTTP 状态码（如 429 表示限流）。

## 限制和注意事项

- 单次请求 `input.messages` 总长度不得超过 32768 token（按模型 tokenizer 计算）；  
- 默认 QPS 限制为 5，可通过 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 提交配额申请；  
- > **注意**：[限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档中描述的“按账户全局限流”已下线，现为“按模型 + 地域维度独立限流”，以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 中的最新规则为准；  
- 所有模型调用均需通过 HTTPS，HTTP 请求将被拒绝；  
- 模型输出内容受内容安全策略过滤，敏感结果可能被截断或返回空响应，不可绕过。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


