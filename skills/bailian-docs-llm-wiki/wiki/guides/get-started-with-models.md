# get started with models

本文档面向开发者，介绍如何快速开始调用百炼平台提供的大模型服务。核心包括模型选择、API 调用方式、关键参数配置及基础限制说明。所有操作均基于标准 RESTful API 接口，无需额外 SDK 即可集成。

## 支持的模型与功能

百炼平台提供多类预训练与微调模型，覆盖文本生成、代码补全、多模态理解等场景。模型列表及能力概览详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。部分模型支持流式响应、[函数调用](../concepts/function-calling.md)（function calling）和系统提示词（system prompt）注入，具体能力以各模型文档为准。首次使用前，建议先阅读 [产品简介](../../raw/model-user-guide/get-started-with-models/what-is-model-studio.md) 理解 Model Studio 的定位与服务边界。

## 关键参数

调用模型 API 时，必需参数包括 `model`（模型 ID）、`input.messages`（消息数组）和认证头 `Authorization: Bearer <api_key>`。推荐显式指定 `parameters.temperature`（默认 0.85）和 `parameters.max_tokens`（默认 1024），避免因平台默认值变更导致行为不一致。地域相关参数（如 `region`）影响接入域名和延迟，需与 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中声明的可用区域匹配。

## 使用方式

1. 获取 API Key：在百炼控制台「API 密钥管理」中创建；
2. 构造请求：使用 HTTPS POST 向对应地域的 Base URL 发送 JSON 请求，Base URL 格式见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；
3. 示例调用：参考 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的 cURL 和 Python 片段，注意替换 `qwen-max` 等模型 ID 及实际 API Key。

> **注意**：原始文档中 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 与 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 对 QPS 计算逻辑描述存在差异——前者按单次请求计数，后者按 token 数加权统计。当前生产环境以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 规则为准。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system、user、assistant）不得超过模型上下文窗口限制（如 qwen-plus 为 32768 tokens）；
- 免费试用额度仅限新用户首月，过期后需绑定付费账号，配额策略详见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)；
- 非中国内地地域（如 ap-southeast-1）暂不支持部分多模态模型，调用前请确认 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中的模型可用性矩阵。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


