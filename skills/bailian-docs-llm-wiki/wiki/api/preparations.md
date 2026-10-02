# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需依次完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循平台安全规范与配额约束。

## 支持的模型/功能

当前 `preparations` 流程适用于全部支持 API 调用的百炼模型，包括 Qwen 系列（如 qwen-max、qwen-plus）、embedding 模型（如 text-embedding-v1）及多模态模型（如 qwen-vl-plus）。不适用于仅支持控制台交互或私有化部署离线 SDK 的场景。具体模型兼容性请参考 [使用 API](../../raw/model-api-reference/preparations.md) 文档中列出的接口清单。

## 关键参数

- `api_key`：必填，通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，需在请求 Header 中以 `Authorization: Bearer <api_key>` 方式传递  
- `base_url`（可选）：用于私有化部署或调试，覆盖默认网关地址；若未显式设置，则使用百炼公共 API 域名  
- `timeout`（推荐设置）：建议设为 60s 以上，避免因大模型响应延迟导致 SDK 抛出 `TimeoutError`；该参数在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有详细说明  

> **注意**：部分旧版文档示例中将 `api_key` 写入请求 Body，此方式已废弃；请严格按 [使用 API](../../raw/model-api-reference/preparations.md) 中的 Header 传递规范执行，否则返回 `401 Unauthorized`。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，登录百炼控制台，在「API 密钥管理」中创建并复制密钥  
2. 根据语言选择对应 SDK：Python 用户运行 `pip install dashscope`，Node.js 用户运行 `npm install @dashscope/nodejs-sdk`（详见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. 初始化客户端时传入 `api_key`，例如 Python 示例：  
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"
   ```

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS，超出将返回 `429 Too Many Requests`；如需提升，请提交工单申请配额调整  
- API Key 不可硬编码于前端代码或公开仓库中，必须通过环境变量或密钥管理服务注入  
- 错误响应统一遵循标准 HTTP 状态码与 JSON body 结构，完整错误码列表见 [错误码](../../raw/model-api-reference/preparations/error-code.md)  
- 若使用代理或内网环境，需确保 `dashscope` SDK 可访问 `https://dashscope.aliyuncs.com`（或私有化地址），DNS 解析失败会导致 `ConnectionError`

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


