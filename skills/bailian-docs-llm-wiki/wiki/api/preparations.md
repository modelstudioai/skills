# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建和客户端初始化。开发者需按顺序完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循平台安全规范与配额策略。

## 支持的模型/功能

当前 `preparations` 流程适用于所有通过百炼 API 提供的模型服务，包括但不限于 Qwen 系列大语言模型、embedding 模型及多模态模型。该准备流程不区分模型类型，统一采用 DashScope SDK 接入，详见 [使用 API](../../raw/model-api-reference/preparations.md)。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过 [获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 页面申请并妥善保管  
- `base_url`（可选）：仅在私有化部署或调试场景下覆盖默认 endpoint，生产环境通常无需设置  
- `timeout`（推荐显式设置）：建议设为 60 秒以上，避免因网络波动导致连接中断；具体超时行为参见 [错误码](../../raw/model-api-reference/preparations.md) 中 `RequestTimeout` 的说明  

## 使用方式

1. 访问 [获取与配置 API Key](https://help.aliyun.com/zh/model-studio/get-api-key) 获取有效密钥  
2. 执行 `pip install dashscope` 安装官方 SDK（Python），其他语言请参考 [安装SDK](https://help.aliyun.com/zh/model-studio/install-sdk)  
3. 初始化客户端：  
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"
   ```  
   如需高级能力（如异步调用、流式响应处理），应启用 [SDK Expert](https://help.aliyun.com/zh/model-studio/dashscope-sdk-expert)，其配置细节见 [使用 API](../../raw/model-api-reference/preparations.md)。

## 限制和注意事项

- 单个 API Key 默认限速 10 QPS（每秒查询数），超出将返回 `429 Too Many Requests`；企业版用户可通过控制台调整配额  
- API Key 不可硬编码于前端代码或公开仓库中，必须通过环境变量或密钥管理服务注入  
- > **注意**：部分旧版文档提及 `dashscope.init(api_key=...)` 初始化方式，该接口已在 v1.18.0+ 版本中废弃，请统一使用 `dashscope.api_key = ...` 赋值，以确保与 [SDK Expert](https://help.aliyun.com/zh/model-studio/dashscope-sdk-expert) 兼容  
- 首次调用前务必确认网络可访问 `https://dashscope.aliyuncs.com`，国内用户若使用代理需额外配置 `HTTP_PROXY` 环境变量  
- 错误响应解析应依赖 [错误码](../../raw/model-api-reference/preparations.md) 文档中的标准定义，避免自行映射非标准状态码

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


