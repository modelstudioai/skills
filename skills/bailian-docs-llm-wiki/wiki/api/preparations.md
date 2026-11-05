# preparations

在调用百炼平台模型 API 前，需完成身份认证、环境配置与网络接入等基础准备。这些步骤直接影响请求的可达性、鉴权成功率及地域合规性。所有操作均围绕 `preparations` 模块展开，核心依赖于 [使用 API](../../raw/model-api-reference/preparations.md) 文档所定义的规范。

## 支持的模型/功能

`preparations` 本身不提供模型能力，而是为所有模型 API（如 `qwen-max`、`qwen-plus`、`qwen-turbo` 等）提供统一的前置支撑能力，包括：API Key 鉴权、SDK 封装调用、错误码统一处理、多地域接入路由。SDK 层已封装对异步任务、流式响应、[Token](../concepts/token.md) 计费等高级功能的支持，详见 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 关键参数

- `api_key`：必填，用于身份认证，需通过 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md) 获取；
- `base_url`：可选，用于覆盖默认接入地址，适用于私有化部署或调试场景，参考 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)；
- `region`：可选但推荐显式指定，影响服务延迟与数据驻留策略，详见 [选择地域、服务部署范围和接入域名](../../raw/model-api-reference/preparations/regions.md)；
- `timeout`：SDK 默认 60 秒，建议根据模型响应特征调整（如长文本生成需延长）。

> **注意**：`dashscope 1.x SDK` 中 `api_key` 可通过环境变量 `DASHSCOPE_API_KEY` 或构造函数传入；而 `2.x+` 版本强制要求显式传参或使用 `DashScopeAPIKeyAuth` 类，[SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md) 中的部分示例已过时，实际开发请以 [SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md) 为准。

## 使用方式

1. 安装最新版 SDK：`pip install dashscope>=2.0.0`（旧版 `dashscope<2.0.0` 已停止维护）；
2. 配置 API Key（推荐代码内显式传入，避免环境变量泄露风险）；
3. 初始化客户端时指定 `region` 和 `base_url`（如需）；
4. 调用任意模型接口前，SDK 自动完成鉴权头注入与重试逻辑。

完整流程示例见 [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)，其中包含 Python、Java、Go 多语言初始化片段。

## 限制和注意事项

- 单个 API Key 默认 QPS 限流为 5，可通过控制台申请提升；
- 免费额度仅适用于公有云 `cn-shanghai` 地域，跨地域调用不享受免费配额；
- 错误响应统一遵循 [错误码](../../raw/model-api-reference/preparations/error-code.md) 规范，开发者应解析 `code` 字段而非仅依赖 HTTP 状态码；
- 所有预签名 URL（如文件上传回调）有效期默认 15 分钟，不可配置。

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


