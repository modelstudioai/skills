# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、开发环境搭建及客户端初始化。开发者需按顺序完成 API Key 获取、SDK 安装与配置，方可发起合法请求。所有操作均需遵循 [使用 API](../../raw/model-api-reference/preparations.md) 文档的流程指引。

## 支持的模型/功能

当前 `preparations` 流程适用于全部支持 API 调用的百炼模型（包括 Qwen 系列、Qwen-VL、Qwen-Audio 等），但**不适用于控制台直接试用或 Playground 交互式调用**。模型能力边界由实际调用的 endpoint 决定，`preparations` 本身不绑定特定模型，仅提供通用接入基础。详细模型支持列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的 SDK 兼容性说明。

## 关键参数

- `api_key`：必填，用于身份鉴权，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储  
- `base_url`（可选）：用于私有化部署场景，覆盖默认百炼服务地址；若未设置，SDK 自动使用 `https://dashscope.aliyuncs.com/api/v1`  
- `max_retries`（可选）：SDK 默认重试 2 次，建议生产环境显式设为 `3` 以提升容错性；该行为在 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 中有详细说明  

> **注意**：部分旧版文档示例中将 `api_key` 作为请求头 `Authorization: Bearer <key>` 直接传递，但当前主流 SDK（v4.0+）已强制要求通过初始化 Client 传入，不再支持 header 方式——请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 的最新初始化方式为准。

## 使用方式

1. 访问 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面，创建并复制有效 API Key  
2. 执行 `pip install dashscope`（Python）或对应语言 SDK（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
3. 初始化 Client 并调用模型接口，例如：
   ```python
   import dashscope
   dashscope.api_key = "YOUR_API_KEY"  # 或传入 dashscope.Client(api_key=...)
   ```

## 限制和注意事项

- 单个 API Key 默认限流 5 QPS（每秒查询数），超出将返回 `429 Too Many Requests` 错误，具体策略详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)  
- API Key 不可跨阿里云账号共享，且不支持子账号独立生成（需主账号操作）  
- 本地调试时禁止硬编码 API Key，应使用环境变量（如 `DASHSCOPE_API_KEY`）或密钥管理服务  
- 若使用代理或内网环境，需确保 `base_url` 可达且 TLS 证书有效；否则初始化 Client 会静默失败——该问题在 [使用 API](../../raw/model-api-reference/preparations.md) 的“常见故障”章节有复现路径说明

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


