# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。这些操作直接影响后续请求的合法性与稳定性，开发者需严格按顺序执行。所有配置项均以最小必要原则设计，避免冗余依赖。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼平台 Model API 提供的模型服务（包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 等），但**不适用于控制台直接交互或 Web UI 场景**。SDK 封装已覆盖主流语言（Python、Java、Node.js、Go），各语言能力对齐详见 [使用 API](../../raw/model-api-reference/preparations.md)。注意：部分旧版 SDK（如 v3.0.0 以下 Python SDK）未支持 `dashscope-sdk-expert` 模式，需升级至最新稳定版。

## 关键参数

- `api_key`：必填，用于身份鉴权，须通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `base_url`（可选）：仅在私有化部署场景下需显式指定，公有云默认使用官方 endpoint；
- `max_retries`（可选）：推荐设为 `3`，避免因临时网络抖动导致请求失败；
- `timeout`（可选）：建议设为 `60` 秒，适配长上下文生成类请求。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥；  
2. **安装 SDK**：根据语言选择对应包（如 `pip install dashscope`），参考 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；  
3. **初始化客户端**：推荐使用 `dashscope-sdk-expert` 模式（自动处理重试、超时、鉴权头注入），详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)；  
4. **验证连通性**：调用 `dashscope.models.list()` 或发送空 body 的 `/v1/services/aigc/text-generation` 请求测试。

> **注意**：原始文档中 [错误码](../../raw/model-api-reference/preparations/error-code.md) 列表未包含 `429 Too Many Requests` 的具体限流策略说明，实际限流由百炼网关统一控制，开发者应依据响应头 `X-RateLimit-Remaining` 和 `Retry-After` 字段实现退避逻辑，而非仅依赖文档所列错误码。

## 限制和注意事项

- 单个 API Key 默认 QPS 限制为 5，可通过工单申请提升；
- `api_key` 不得硬编码在前端代码或公开仓库中，必须通过环境变量或密钥管理服务注入；
- Python SDK v4.0+ 已弃用 `dashscope.api_key = ...` 全局赋值方式，必须通过 `dashscope.ApiKeyAuth(api_key=...)` 或构造函数传参；
- 所有 preparatory 步骤均需在首次 API 调用前完成，运行时动态修改 `api_key` 可能导致连接复用异常。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


