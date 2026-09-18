# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需按顺序完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档的流程指引。

## 支持的模型/功能

当前 `preparations` 流程适用于全部支持 API 调用的百炼模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接试用或 Playground 交互式调用**。模型能力边界由实际调用的 endpoint 决定，`preparations` 本身不绑定特定模型，仅提供通用接入基础。详细模型支持列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK 兼容性说明。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储  
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼服务地址；若未设置，SDK 自动使用 `https://dashscope.aliyuncs.com/api/v1`  
- `max_retries`（可选）：SDK 默认重试 2 次，建议生产环境显式设为 `3` 以提升容错性；该行为在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有详细说明  

> **注意**：部分旧版文档中提及 `secret_key` 参数，该字段已于 v3.0.0 SDK 起废弃，仅保留 `api_key`；请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的最新参数定义为准。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，登录阿里云账号，在「API 密钥管理」中创建并复制密钥  
2. 执行 `pip install dashscope`（Python）或对应语言 SDK（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. 初始化客户端（示例）：
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"  # 或通过环境变量 DASHSCOPE_API_KEY 设置
   ```
4. 后续调用任意模型 API（如 `dashscope.Generation.call`）即可自动复用该准备状态

## 限制和注意事项

- 单个 API Key 默认限流 10 QPS（每秒查询数），超出将返回 `429 Too Many Requests`；具体配额请查阅 [错误码](../../raw/model-api-reference/preparations/error-code.md) 文档中的限流说明  
- API Key 不可跨地域使用（例如华东1 区生成的 Key 无法调用华北2 区 endpoint），此限制在 [使用 API](../../raw/model-api-reference/preparations.md) 中明确标注  
- 严禁在前端代码、Git 仓库或日志中硬编码 `api_key`；推荐使用环境变量或密钥管理服务注入  
- 若使用代理或内网环境，需确保 `base_url` 对应域名可访问，且 TLS 证书有效（SDK 默认校验证书）

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


