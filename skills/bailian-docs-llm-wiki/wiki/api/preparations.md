# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需依次完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循平台安全规范与配额策略。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 API 提供的模型服务（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不直接支持控制台沙箱调试或免密直连模式**。模型能力启用状态以 [使用 API](../../raw/model-api-reference/preparations.md) 文档中列出的 SDK 支持矩阵为准；部分新模型可能需 SDK ≥ 4.12.0 才能正确初始化 client 实例。

## 关键参数

- `api_key`：必填，从 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，不可硬编码于生产代码中  
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼网关地址  
- `timeout`（可选）：建议显式设置（如 `timeout=60`），避免因网络抖动导致连接挂起  
- `max_retries`（可选）：SDK 默认为 2，高并发场景建议设为 0 并由上层统一重试  

## 使用方式

1. **获取 API Key**：登录百炼控制台 →「API 密钥管理」→ 创建并复制密钥  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言包（参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. **初始化 client**：  
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"  # 或通过环境变量 DASHSCOPE_API_KEY 设置
   ```
   > **注意**：[SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中推荐的 `dashscope.Config(...)` 初始化方式在 v4.15.0+ 已废弃，应改用 `dashscope.api_key` 全局赋值或 `dashscope.base_http_api()` 显式传参。

## 限制和注意事项

- 单个 API Key 默认限流 10 QPS，超出将返回 `429 Too Many Requests`（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）  
- API Key 仅对创建者所在工作空间生效，跨工作空间调用需单独申请  
- 不支持在浏览器前端直接使用 API Key（存在泄露风险），必须通过后端代理转发请求  
- 首次调用前务必确认模型服务已开通（控制台「模型服务」页签），否则返回 `403 Forbidden` 而非鉴权失败

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


