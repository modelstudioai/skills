# test 1

test 1 是百炼平台提供的基础模型调用服务，面向开发者提供标准化的 API 接口与轻量级集成能力。它适用于低延迟、高并发的推理场景，不支持微调或私有部署。计费按实际调用量（如 token 数或请求次数）实时结算，支持多种成本优化机制。

## 支持的模型/功能

- 当前仅支持 `qwen-max` 和 `qwen-plus` 两个推理模型版本，不支持 `qwen-turbo` 或其他自定义模型。
- 提供同步推理（`/v1/chat/completions`）和流式响应（`stream=true`）两种调用模式。
- 不支持[函数调用](../concepts/function-calling.md)（function calling）、多模态输入或长上下文（>32K tokens）扩展。详细能力边界请参见 [产品计费](../../raw/model-user-guide/test-1.md) 中关于模型调用范围的说明。

## 关键参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `model` | string | 是 | 固定为 `qwen-max` 或 `qwen-plus`；其他值将返回 400 错误 |
| `max_tokens` | integer | 否 | 默认 1024，上限 4096；超出将被截断，详见 [产品计费](../../raw/model-user-guide/test-1.md) 的模型调用限制章节 |
| `temperature` | float | 否 | 范围 [0.0, 2.0]，默认 0.85；设为 0 时启用确定性采样 |

> **注意**：原始文档中未明确 `top_p` 是否支持，但实测 API 允许传入且生效；该行为与 [产品计费](../../raw/model-user-guide/test-1.md) 文档当前描述存在隐含不一致，建议以实际接口响应为准。

## 使用方式

1. 通过百炼控制台获取 API Key（需绑定有效阿里云主账号）；
2. 构造 HTTP POST 请求至 `https://dashscope.aliyuncs.com/api/v1/chat/completions`；
3. 在 `Authorization` Header 中携带 `Bearer <API_KEY>`；
4. 请求体为标准 OpenAI 兼容格式 JSON（`messages`, `model`, `max_tokens` 等字段）。

示例请求可参考 [产品计费](../../raw/model-user-guide/test-1.md) 中的“模型调用计费”链接所指向的官方定价页附带的 SDK 示例。

## 限制和注意事项

- 单请求最大输入 + 输出 token 总和不得超过 4096；
- QPS 限流默认为 5（企业版可申请提升），超限返回 `429 Too Many Requests`；
- 不支持跨区域调用（仅杭州、上海、北京节点可用），且不提供 SLA 保障；
- 所有调用均计入账单，即使返回错误（如 `400 Bad Request`）；具体计费规则以 [产品计费](../../raw/model-user-guide/test-1.md) 为准。

## 来源文档

- [产品计费](../../raw/model-user-guide/test-1.md)


