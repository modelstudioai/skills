# preparations

`preparations` 是调用百炼模型 API 前必需完成的初始化步骤，涵盖身份认证、开发环境配置及基础依赖安装。开发者需按顺序完成 API Key 获取、SDK 安装与初始化，方可发起合法请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档中定义的流程规范。

## 支持的模型/功能

当前 `preparations` 流程适用于全部百炼平台公开模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及配套能力（如流式响应、异步任务、文件上传解析）。不支持私有化部署模型的免鉴权调用；私有化场景需参考 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中的内网鉴权说明。

## 关键参数

- `api_key`：必填，通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取，建议通过环境变量 `DASHSCOPE_API_KEY` 注入，避免硬编码  
- `base_url`（可选）：用于私有化或代理场景，覆盖默认 endpoint；需与 SDK 版本兼容，详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)  
- `timeout`（可选）：推荐设为 60s 以上，尤其对多模态大文件处理场景  

> **注意**：部分旧版 SDK 示例中将 `api_key` 作为方法参数传入，但自 dashscope v1.18.0 起已强制要求全局初始化时设置，否则触发 `AuthenticationError` —— 请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的最新初始化示例为准。

## 使用方式

1. **获取 API Key**：登录百炼控制台 →「API 密钥管理」→ 创建并复制密钥  
2. **安装 SDK**：执行 `pip install dashscope`（Python）或对应语言包（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. **初始化客户端**：
   ```python
   import dashscope
   dashscope.api_key = "sk-..."  # 或 os.environ["DASHSCOPE_API_KEY"]
   ```

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS（具体配额以控制台显示为准），超限返回 `429 Too Many Requests`，错误详情参见 [错误码](../../raw/model-api-reference/preparations/error-code.md)  
- API Key 不可跨地域使用（如杭州 region 的 key 无法调用上海 region 模型），region 需在初始化时显式指定或通过 endpoint 推导  
- 严禁在前端代码（如浏览器 JS）中暴露 `api_key`；Web 应用必须通过后端代理转发请求  
- 临时 Token（如 STS 临时凭证）暂不支持 `preparations` 流程，仅限长期 API Key

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


