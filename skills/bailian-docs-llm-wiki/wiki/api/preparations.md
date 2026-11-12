# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖认证凭证获取、SDK 环境搭建及服务端点配置。这些操作直接影响请求的合法性与连通性，开发者需严格按顺序执行。所有配置项均以最小必要原则设计，避免冗余依赖。

## 支持的模型/功能

当前 `preparations` 流程适用于全部通过百炼平台 HTTP API 提供的模型服务（包括 `qwen-*`、`lingji-*` 等系列），不区分文本生成、多模态或嵌入模型。SDK 封装统一覆盖所有模型能力，无需为不同模型单独准备环境。具体支持范围请参考 [使用 API](../../raw/model-api-reference/preparations.md) 文档中列出的子模块。

## 关键参数

- `api_key`：必填，用于身份认证，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取并安全存储  
- `base_url`：可选，默认指向生产环境；如需对接沙箱或私有部署实例，须显式配置，详见 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)  
- `timeout`：建议显式设置（如 60s），避免因网络波动导致连接挂起  

> **注意**：部分旧版 SDK 1.x 示例中将 `api_key` 作为构造函数参数传入，而新版 SDK（2.x+）推荐通过环境变量 `DASHSCOPE_API_KEY` 注入——该差异已在 [SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 中明确标注，请勿混用。

## 使用方式

1. 安装 SDK：运行 `pip install dashscope`（Python）或对应语言包（见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)）  
2. 配置认证：设置环境变量 `DASHSCOPE_API_KEY` 或在代码中显式传入（不推荐）  
3. 初始化客户端：指定 `base_url`（如需）并验证连通性（例如调用 `models.list()`）  

## 限制和注意事项

- 单个 `api_key` 默认限流 5 QPS，超出将返回 `429 Too Many Requests`（详见 [错误码](../../raw/model-api-reference/preparations/error-code.md)）  
- 不支持在浏览器前端直接使用 `api_key`，必须通过后端代理调用，防止密钥泄露  
- SDK Expert 模式（见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)）提供细粒度控制，但要求开发者自行处理重试、熔断等逻辑，生产环境建议优先使用默认封装

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


