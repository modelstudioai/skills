# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需按顺序完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档的流程指引。

## 支持的模型/功能

当前 `preparations` 流程适用于全部支持 API 调用的百炼模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接试用或 Playground 交互式调用**。模型能力边界由实际调用的 endpoint 决定，准备阶段本身无模型特异性。如需确认某模型是否支持 API 方式，请查阅对应模型的 [使用 API](../../raw/model-api-reference/preparations.md) 文档说明。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储  
- `base_url`（可选）：当使用私有部署或代理时需显式指定；默认指向百炼公有云服务地址  
- `timeout`（推荐设置）：建议设为 60s 以上，避免因大模型响应延迟导致客户端超时中断  
- `max_retries`（SDK v3.12+）：自动重试次数，默认为 2；该行为在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有详细说明  

> **注意**：部分旧版文档中将 `api_key` 描述为“可选”（见早期 `install-sdk.md` 示例），此为过时信息；自 v3.10 起，所有生产环境调用均强制要求 `api_key`，请以 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 为准。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，在百炼控制台创建并复制密钥  
2. 执行 `pip install dashscope>=3.10`（Python）或对应语言 SDK（参见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. 初始化客户端时传入 `api_key`，例如：  
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"
   ```  
   或使用 `DashScopeClient(api_key=...)` 实例化（推荐，见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)）

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS（每秒查询数），超出将返回 `429 Too Many Requests`；具体配额请在控制台「API Key 管理」页查看  
- `api_key` 不得硬编码于前端代码或公开仓库中，否则将触发安全告警并可能被自动禁用  
- 错误响应统一遵循 [错误码](../../raw/model-api-reference/preparations/error-code.md) 规范，开发者应解析 `code` 字段（如 `InvalidArgument`、`Unauthorized`）而非仅依赖 HTTP 状态码  
- 企业版用户若启用 VPC 内网访问，需额外配置 `base_url` 并确保网络策略放行，该细节未在 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md) 中体现，须参考私有化部署附录

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


