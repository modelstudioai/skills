# get started with models

本文档指导开发者快速接入百炼平台的模型服务，涵盖模型选择、API 调用基础配置、关键参数设置及常见约束。适用于首次集成千问（Qwen）等大模型的开发场景，无需部署模型即可通过标准 HTTP 接口调用。所有操作均基于百炼统一 API 网关，需提前完成身份认证与配额配置。

## 支持的模型与核心功能

百炼平台当前支持 Qwen 系列（如 `qwen-max`、`qwen-plus`、`qwen-turbo`）、通义万相、通义听悟等多模态模型，具体列表详见 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md)。各模型提供文本生成、结构化输出（JSON Schema）、流式响应、[函数调用](../concepts/function-calling.md)（Function Calling）等能力。部分模型还支持图像理解（如 `qwen-vl-plus`），但需注意输入格式与 token 计费规则差异。

> **注意**：[动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 与 [限流](../../raw/model-user-guide/get-started-with-models/rate-limit.md) 文档中对并发数阈值的描述存在不一致——前者以“每秒请求数（RPS）”为单位，后者以“并发连接数”为单位；实际生效策略以 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 中定义的账户级配额为准。

## 关键参数

调用模型 API 时，必需参数包括：
- `model`：模型标识符（如 `"qwen-max"`），必须与 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 中公布的名称严格一致；
- `input.messages`：消息数组，格式为 `[{ "role": "user", "content": "..." }]`，系统角色（`system`）仅在部分模型中支持；
- `parameters.temperature`：控制输出随机性（0.0–1.0），默认为 0.85；
- `parameters.top_p`：核采样阈值，默认为 0.8；
- `stream`：布尔值，启用流式响应需显式设为 `true`。

所有参数均遵循 [OpenAI 兼容接口](../concepts/openai-compatible-api.md)规范，但 `max_tokens` 实际限制受模型上下文窗口与配额双重约束。

## 使用方式

1. **获取凭证**：在百炼控制台创建 API Key（AK/SK），并确保对应账号已开通模型服务权限；  
2. **确定接入点**：根据部署地域选择 Base URL，例如华东1（杭州）使用 `https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`，完整列表见 [Base URL总览](../../raw/model-user-guide/get-started-with-models/base-url.md)；  
3. **发起请求**：使用 `POST` 方法，`Content-Type: application/json`，携带 `Authorization: Bearer ${API_KEY}` 头；  
4. **验证首调**：推荐从 [首次调用千问API](../../raw/model-user-guide/get-started-with-models/first-api-call-to-qwen.md) 提供的最小示例入手，确认网络连通性与鉴权有效性。

## 限制和注意事项

- 单次请求 `input.messages` 总长度（含 role + content）不得超过模型上下文窗口的 90%，超长将被截断且不报错；  
- 流式响应（`stream=true`）下，`X-RateLimit-Remaining` 响应头不可靠，应依赖 [动态限流](../../raw/model-user-guide/get-started-with-models/quota-management.md) 提供的异步配额查询接口进行节流控制；  
- 模型服务地域隔离：调用域名必须与 [选择地域、服务部署范围和接入域名](../../raw/model-user-guide/get-started-with-models/regions.md) 中指定的 Region 严格匹配，跨地域请求将返回 `403 Forbidden`；  
- 所有模型调用按 token 计费，输入与输出 token 分别计数，具体计费规则以控制台最新公示为准。

## 来源文档

- [开始使用](../../raw/model-user-guide/get-started-with-models.md)


