# get started with models

本文档面向开发者，介绍如何快速接入和调用百炼平台提供的大模型服务。你将了解当前支持的模型类型、关键请求参数、标准调用方式，以及生产环境需关注的限制与注意事项。所有操作均基于 RESTful API，无需安装额外 SDK 即可开始。

## 支持的模型与核心功能

百炼平台提供多种开源与自研大模型，包括 Qwen 系列（如 qwen-max、qwen-plus、qwen-turbo）、Embedding 模型（如 text-embedding-v1）及多模态模型（如 qwen-vl）。模型能力覆盖文本生成、代码补全、语义检索、图像理解等场景。具体可用模型列表及适用场景详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。动态限流与配额管理能力已集成至统一控制台，支持按 [Token](../concepts/token.md) 或请求数维度配置策略，详情参见 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md)。

## 关键参数

调用模型 API 时，必需参数包括：  
- `model`：模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；  
- `input.messages`：非空消息数组，首条消息 `role` 必须为 `"user"`；  
- `parameters.temperature`：取值范围 `[0.0, 2.0]`，默认 `1.0`；  
- `parameters.top_p`：取值范围 `[0.0, 1.0]`，默认 `1.0`；  
- `parameters.max_tokens`：最大输出 token 数，不同模型有硬性上限（如 qwen-turbo 最高 8192），超出将被截断并返回 `400` 错误。

> **注意**：部分旧文档中 `top_k` 被列为推荐参数，但当前 API 已废弃该字段，实际生效仅以 `temperature` 和 `top_p` 为准；请以 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 中的请求示例为准。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（AccessKey ID / Secret），用于 `Authorization: Bearer <api_key>` 认证；  
2. **确定接入点**：根据部署地域选择 Base URL，例如华东 1（杭州）对应 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`；完整域名映射见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；  
3. **发起 POST 请求**：使用标准 JSON payload 提交，Content-Type 必须为 `application/json`；  
4. **处理响应**：成功响应含 `output.text` 字段，错误码参考 `status_code` 及 `code` 字段（如 `InvalidParameter`、`Throttling`）。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 system prompt）不得超过模型上下文窗口的 95%，否则返回 `400 InvalidParameter`；  
- 免费试用额度仅限新用户首次开通后 30 天内有效，配额耗尽后需手动开通按量付费；  
- 所有模型均不支持跨地域调用：若在华北 2（北京）开通服务，不可使用华东 1 的 Base URL，否则触发鉴权失败；地域与域名绑定关系详见 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md)；  
- `rate-limit` 响应头（如 `X-RateLimit-Limit`, `X-RateLimit-Remaining`）仅在配额未超限时返回，超限后直接返回 `429 Too Many Requests`，无重试建议头；该行为与部分旧版文档描述存在差异，请以实际接口响应为准。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


