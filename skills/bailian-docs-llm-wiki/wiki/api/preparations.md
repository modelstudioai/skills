# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖身份认证、环境配置与依赖安装。开发者需按顺序完成 API Key 获取、SDK 安装及基础配置，方可发起有效请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档中的流程指引。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼平台开放的模型 API，包括但不限于 Qwen 系列大语言模型、多模态模型（如 Qwen-VL）及 Embedding 模型。SDK 封装统一了鉴权与请求结构，因此无需为不同模型重复配置；具体支持模型列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK 兼容性说明。

## 关键参数

- `api_key`：必填，用于身份校验，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储  
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼服务地址  
- `timeout`（可选）：SDK 默认超时为 60 秒，建议在高延迟网络中显式设置  
> **注意**：部分旧版 SDK 文档中提及 `secret_key` 参数，该字段已废弃；当前仅需 `api_key`，详见 [使用 API](../../raw/model-api-reference/preparations.md) 的最新说明。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，登录阿里云账号并开通百炼服务，创建并复制 API Key  
2. 根据语言选择对应 SDK：Python 用户执行 `pip install dashscope`；其他语言参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)  
3. 初始化客户端（以 Python 为例）：
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   ```
   如需高级调试能力，可启用 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 模式。

## 限制和注意事项

- 单个 API Key 默认调用频率限制为 10 QPS，超出将返回 `429 Too Many Requests` 错误（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）  
- API Key 不可硬编码于前端代码或公开仓库中，必须通过环境变量或密钥管理服务注入  
- 首次调用前务必确认网络可访问 `dashscope.aliyuncs.com`（国内）或 `dashscope.aliyuncs.com`（国际），防火墙策略需放行 HTTPS 流量  
- 若遇到 `AuthenticationFailed` 错误，请优先核查 API Key 是否过期或权限不足，并复核 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中的权限绑定步骤

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


