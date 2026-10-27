# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖身份认证、环境配置与依赖安装。这些操作直接影响后续请求的可用性与稳定性，开发者需严格按顺序执行。所有步骤均基于 [使用 API](../../raw/model-api-reference/preparations.md) 文档定义。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼托管模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等）及配套能力（如流式响应、异步任务、文件上传等）。SDK 封装已统一适配各模型的通用鉴权与协议规范，无需为不同模型重复配置。具体支持范围详见 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK 版本兼容说明。

## 关键参数

- `api_key`：必填，通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需在请求头 `Authorization: Bearer <api_key>` 或 SDK 初始化时传入  
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼服务地址；若未指定，则自动使用官方 endpoint  
- `timeout`（推荐设置）：建议显式配置连接与读取超时（如 `timeout=60`），避免因网络波动导致阻塞；该参数在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有详细示例  

> **注意**：部分旧版文档中提及 `secret_key` 作为备用凭证，但自 v3.15.0 起 SDK 已移除对该字段的支持，仅接受 `api_key` —— 请以 [使用 API](../../raw/model-api-reference/preparations.md) 的最新描述为准。

## 使用方式

1. **获取 API Key**：登录百炼控制台，在「API 密钥管理」中创建并复制密钥  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言包（参考 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. **初始化客户端**：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   # 或使用 client 实例化方式（推荐用于多 key 场景）
   ```

## 限制和注意事项

- 单个 API Key 默认限流 10 QPS（每秒查询数），超出将返回 `429 Too Many Requests`；详细策略见 [错误码](../../raw/model-api-reference/preparations/error-code.md)  
- API Key 不可跨地域使用（如杭州 region 的 key 无法调用上海 endpoint），需确保 `base_url` 与控制台分配 region 一致  
- 本地调试时禁用代理或显式配置 `NO_PROXY`，否则可能因证书校验失败中断连接（该问题在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的“常见故障”章节有复现说明）

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


