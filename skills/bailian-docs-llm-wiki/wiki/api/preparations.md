# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需按顺序完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档的流程指引。

## 支持的模型/功能

当前 `preparations` 流程适用于全部支持 API 调用的百炼模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接调试或 Web UI 交互场景**。模型能力边界由具体模型文档定义，本准备流程仅提供通用接入支撑。如需确认某模型是否支持 API 调用，请参考其对应模型页中的“API 支持”标识，或查阅 [使用 API](../../raw/model-api-reference/preparations.md) 中的兼容性说明。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储；
- `base_url`（可选）：当使用私有部署或代理服务时，需显式指定，否则默认指向百炼公有云 API 端点；
- `timeout`（推荐设置）：建议设为 60s 以上，避免因大模型响应延迟导致 SDK 抛出 `TimeoutError`；该参数在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有详细行为说明。

> **注意**：部分旧版 SDK 示例中将 `api_key` 写入环境变量 `DASHSCOPE_API_KEY` 后未显式传参，而新版 SDK（v1.20.0+）已要求显式传入或通过 `dashscope.api_key = ...` 设置；请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的最新说明为准，避免因版本差异导致 `AuthenticationError`。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)，在百炼控制台「API 密钥」页面创建并复制密钥；
2. 执行 `pip install dashscope`（Python）或对应语言 SDK（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）；
3. 初始化客户端时传入 `api_key`，例如：  
   ```python
   import dashscope
   dashscope.api_key = "sk-xxx"  # 或作为参数传入具体方法
   ```

## 限制和注意事项

- 单个 API Key 默认配额为 1000 QPM（每分钟请求数），超出将返回 `429 Too Many Requests`；配额调整需提交工单申请；
- API Key 不可跨地域使用（如杭州 region 的 Key 无法调用上海 region 模型），region 必须与模型部署地一致；
- 错误响应统一遵循标准 HTTP 状态码与 JSON body 结构，完整错误码列表见 [错误码](../../raw/model-api-reference/preparations/error-code.md)；
- **严禁**在前端代码（如浏览器 JS）中硬编码 `api_key`，否则存在密钥泄露风险——该安全要求在 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 中明确强调。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


