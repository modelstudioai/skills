# preparations

`preparations` 是调用百炼平台模型 API 前必需完成的基础配置步骤，涵盖身份认证、环境准备和请求基础设施设置。开发者需正确获取并管理 API Key，选择适配的 SDK 版本，并确认 Base URL 等网络参数。所有操作均以安全、可复现和符合当前版本规范为前提。

## 支持的模型/功能

本阶段不直接涉及模型选型，但所完成的准备工作（如 API Key 权限配置、SDK 初始化）决定了后续可调用的模型范围。例如，部分模型（如 `qwen-max` 或 `qwen-plus`）要求 API Key 具备对应服务权限；若未开通相应模型配额，即使请求参数合法也会返回 `403 Forbidden` 错误。具体模型支持列表请参考 [使用 API](../../raw/model-api-reference/preparations.md) 中的权限说明章节。

## 关键参数

- `api_key`：必填，用于身份鉴权，须通过 [获取与配置 API Key](../../raw/preparations/get-api-key.md) 流程生成并妥善保管  
- `base_url`：可选，用于指定请求入口，国内默认为 `https://dashscope.aliyuncs.com/api/v1`；国际用户或私有化部署场景需按 [Base URL总览](../../raw/preparations/base-url.md) 配置  
- `timeout`：建议显式设置（如 60s），避免因网络波动导致连接挂起；SDK 默认超时值在不同版本中不一致，请以 [SDK Expert](../../raw/preparations/dashscope-sdk-expert.md) 文档为准  

> **注意**：`dashscope` Python SDK 2.x 起已废弃 `dashscope.api_key` 全局赋值方式，改用 `DashScopeClient(api_key=...)` 实例化；而 [SDK 1.x 历史用法参考](../../raw/preparations/dashscope-1x-legacy-reference.md) 中的写法不再兼容，切勿混用。

## 使用方式

1. 通过 [获取与配置 API Key](../../raw/preparations/get-api-key.md) 获取有效密钥  
2. 安装对应语言 SDK（推荐最新稳定版）：`pip install dashscope`（Python）或参见 [安装SDK](../../raw/preparations/install-sdk.md)  
3. 初始化客户端并发起首次健康检查请求（如 `/status` 或空 payload 的 `/chat/completions`）验证连通性  

## 限制和注意事项

- 单个 API Key 默认有 QPS 和日调用量限制，超出将触发 `429 Too Many Requests`；配额调整需提交工单，不可自行修改  
- API Key 严禁硬编码在前端代码或公开仓库中；应通过环境变量（如 `DASHSCOPE_API_KEY`）注入  
- 错误响应解析必须依赖 [错误码](../../raw/preparations/error-code.md) 文档，不同错误类型（如 `InvalidAPIKey` vs `ResourceNotFound`）需差异化处理  
- 所有 preparatory 操作均需在调用任何模型接口前完成；跳过任一环节可能导致 `401 Unauthorized` 或 `503 Service Unavailable`

## 来源文档

- [使用 API](../../raw/model-api-reference/preparations.md)


