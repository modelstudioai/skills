# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。这些操作直接影响后续请求的合法性与稳定性，开发者需严格按顺序执行。所有步骤均以 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 为权威依据。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等）及通用推理接口。不区分模型类型，统一采用同一套认证与 SDK 初始化机制。SDK Expert 模式（见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)）支持自动模型路由与参数适配，但底层仍依赖标准 preparations 流程。

## 关键参数

- `api_key`：必填，通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需在请求头或 SDK 初始化时显式传入  
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼服务地址；若未设置，则使用官方 endpoint  
- `max_retries`（SDK 默认为 3）：建议在高并发场景下显式配置，避免因临时网络抖动导致请求失败  

> **注意**：部分旧版文档示例中将 `api_key` 写作环境变量 `DASHSCOPE_API_KEY`，而最新 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 文档明确要求优先通过代码参数传入，以增强多租户隔离安全性——请以该文档为准。

## 使用方式

1. **获取 API Key**：登录百炼控制台 →「API 密钥管理」→ 创建并复制密钥  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言包（参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "your_api_key"  # 或传入 dashscope.Generation(..., api_key=...)
   ```

## 限制和注意事项

- 单个 API Key 默认限流 10 QPS（具体以控制台配额页为准），超限返回 `429 Too Many Requests`（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）  
- API Key 不可跨地域使用（如杭州 region 的 key 无法调用上海 endpoint），且不支持子账号继承主账号密钥权限  
- 本地调试时禁止硬编码 API Key；生产环境必须通过安全凭证管理服务（如 KMS）注入，否则违反 [使用 API (raw/model-api-reference/preparations.md)](../../raw/model-api-reference/preparations.md) 安全规范

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


