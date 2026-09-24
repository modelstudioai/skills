# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需依次完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循平台安全规范与配额策略。

## 支持的模型/功能

当前 `preparations` 流程适用于全部公开可调用的百炼模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于私有化部署或离线 SDK 场景**。模型能力边界由实际调用的 endpoint 决定，而非准备阶段本身。具体支持列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的链接导航。

## 关键参数

- `api_key`：必填，用于身份鉴权，须通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储  
- `base_url`（可选）：仅在自定义 endpoint 时设置，例如私有网关地址；默认值由 SDK 自动指定  
- `timeout`（推荐显式设置）：建议设为 60s 以上，避免因大模型响应延迟导致连接中断  

> **注意**：`model` 参数不属于 `preparations` 阶段配置项，而是在实际请求 payload 中指定；混淆该归属可能导致初始化失败——详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的参数分层说明。

## 使用方式

1. 访问控制台，按指引完成 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)  
2. 根据语言选择对应 SDK，执行 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 步骤（如 `pip install dashscope`）  
3. 初始化客户端时传入 `api_key`，示例（Python）：
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"
   ```
   更高级用法（如多 key 轮询、自定义 session）见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS，超出将返回 `429 Too Many Requests`（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）  
- API Key 不可跨地域复用（如杭州 region 的 key 无法调用深圳 region 的服务），region 必须与初始化时 `base_url` 或 SDK 默认 region 一致  
- 严禁在前端代码（如浏览器 JS）中硬编码 `api_key`，否则存在密钥泄露风险；应通过后端代理转发请求  
- 若使用旧版 `dashscope<1.18.0`，部分错误码解析逻辑不兼容最新平台响应格式，请升级至最新 SDK 版本以确保 [错误码](../../raw/model-api-reference/preparations/error-code.md) 处理准确性

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


