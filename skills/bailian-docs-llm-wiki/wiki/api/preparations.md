# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需按顺序完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档的流程指引。

## 支持的模型/功能

当前 `preparations` 流程适用于全部支持 API 调用的百炼模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接试用或 Playground 交互式调用**。模型能力边界由实际调用的 endpoint 决定，`preparations` 本身不绑定特定模型，仅提供通用接入基础。详细模型支持列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK 兼容性说明。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼服务地址；
- `timeout`（推荐设置）：建议显式设置 HTTP 超时（如 60s），避免因网络波动导致阻塞；
- `max_retries`（推荐设置）：SDK 默认重试策略可能不满足生产要求，应依据 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 指南定制。

> **注意**：部分旧版文档中提及 `secret_key` 参数，该字段已于 v3.2.0 SDK 起废弃，仅保留 `api_key`；请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的最新说明为准。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，创建并复制有效 API Key；
2. 执行 `pip install dashscope`（Python）或对应语言 SDK（参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；
3. 初始化客户端时传入 `api_key`，例如：
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"
   ```
   或使用 `dashscope.Client(api_key="sk-xxx")` 实例化方式（推荐，便于多 key 隔离）。

## 限制和注意事项

- 单个 API Key 默认限流为 10 QPS（具体值以控制台配额页为准），超限返回 `429 Too Many Requests`，错误详情见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；
- API Key 不可跨区域复用（如 cn-beijing Key 无法调用 us-west-2 endpoint），区域信息需与 endpoint 严格匹配；
- 严禁在前端代码、Git 仓库或日志中硬编码 `api_key`，必须通过环境变量或密钥管理服务注入；
- 若使用代理或内网环境，需确保 SDK 可访问 `https://dashscope.aliyuncs.com`（或对应私有 endpoint），防火墙策略须放行。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


