# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及 SDK 集成。这些操作直接影响后续请求的合法性与稳定性，开发者需严格按顺序执行。所有前置准备均以 [使用 API](../../raw/model-api-reference/preparations.md) 为统一入口文档。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼平台 HTTP API 或 SDK 调用的模型（包括 Qwen 系列、Baichuan、GLM 等），但**不适用于控制台直接试用或 Playground 交互式调用**。模型能力边界由实际调用的 endpoint 决定，而非 preparation 步骤本身。详见 [使用 API](../../raw/model-api-reference/preparations.md) 中的模型兼容性说明。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `base_url`（可选）：当使用私有部署或代理时需显式指定，否则默认指向百炼公有云地址；
- `timeout`（SDK 推荐设置）：建议设为 ≥10s，避免因网络抖动导致误判失败——该建议在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有明确说明。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 创建并复制 API Key；
2. 根据语言选择对应 SDK，按 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档完成依赖安装；
3. 初始化客户端时传入 `api_key`，推荐复用 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 提供的连接池与重试策略。

> **注意**：部分旧版文档示例中仍使用 `dashscope.api_key = "xxx"` 的全局赋值方式，但自 v1.18.0 起 SDK 已要求显式传入 `api_key` 参数至 Client 构造函数，否则将触发 `AuthenticationError` ——请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的最新初始化示例为准。

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS（每秒查询数），如需提升请提交配额申请；
- API Key 不可跨区域使用（例如杭州 region 的 key 无法调用北京 region 的 endpoint），region 必须与 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中所选一致；
- 错误响应解析应优先参考 [错误码](../../raw/model-api-reference/preparations/error-code.md)，其中 `InvalidAPIKey`（401）与 `RateLimitExceeded`（429）是最常见两类失败原因。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


