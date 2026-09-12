# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需确保 API Key 有效、SDK 版本兼容，并正确设置请求上下文。所有操作均以安全、可复现为前提，不涉及模型训练或数据上传。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 Model API 提供的在线推理服务，包括 `qwen-max`、`qwen-plus`、`qwen-turbo` 等通义千问系列模型，以及 `lingji-vl` 等[多模态](../concepts/multi-modal.md)模型。语音、向量、Embedding 类模型亦适用同一套认证与 SDK 初始化机制。具体支持列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的官方说明。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过 [获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 获取；
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼 API 地址；
- `timeout`（推荐设置）：建议显式指定 `timeout=60`，避免长尾请求阻塞；
- `max_retries`（推荐设置）：SDK 默认重试策略可能不满足高可用需求，建议在初始化时显式配置，详见 [SDK Expert](../../raw/model-api-reference/preparations.md)。

> **注意**：部分旧版文档中提及 `secret_key` 作为备用鉴权方式，但自 v3.12.0 起 SDK 已移除对该字段的支持，仅保留 `api_key`；请以 [使用 API](../../raw/model-api-reference/preparations.md) 的最新说明为准。

## 使用方式

1. 访问 [获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 创建并复制密钥；
2. 执行 `pip install dashscope` 安装最新稳定版 SDK（≥3.15.0）；
3. 在代码中初始化客户端：
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"  # 或通过环境变量 DASHSCOPE_API_KEY 设置
   ```
   更高级的配置（如异步客户端、自定义 session）请参阅 [SDK Expert](../../raw/model-api-reference/preparations.md)。

## 限制和注意事项

- 单个 API Key 默认 QPS 限制为 5，可通过控制台申请提升；
- API Key 不可跨 Region 使用，华东 1（杭州）密钥无法调用华北 2（北京）Endpoint；
- 本地调试时禁止硬编码 `api_key`，应使用环境变量或密钥管理服务；
- 错误响应统一遵循标准 HTTP 状态码与 JSON 格式，详细含义见 [错误码](../../raw/model-api-reference/preparations.md)。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)



