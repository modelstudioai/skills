# preparations

在调用百炼模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、地域与 Base URL 选择等基础准备。这些步骤直接影响鉴权、路由、性能与功能可用性，是所有模型调用的前提。本文档结构化梳理关键环节，聚焦可执行要点，避免常见配置陷阱。

## 支持的模型/功能

百炼支持文本生成、[多模态](../concepts/multi-modal.md)对话、图像/视频生成、语音识别与合成、[向量嵌入](../concepts/vector-embedding.md)、重排序及智能体应用等多种模型类型。**模型可用性严格按地域隔离**：每个地域（如华北2北京、新加坡、美国弗吉尼亚）有独立的模型列表，API Key 和 Base URL 均不可跨地域混用 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。例如，`qwen3.7-plus` 在北京地域可用，不代表其在德国法兰克福地域自动可用。实时推理功能全地域支持，但批量推理仅限华北2（北京）和新加坡 [选择地域、服务部署范围和接入域名](../../raw/model-api-reference/preparations/regions.md)。部分模型（如 `qwen3.7-plus`）强制启用思考模式（`enable_thinking=true`），而另一些（如 `qwen-plus`）则需显式关闭该参数才能使用结构化输出或非流式调用，具体约束详见[错误码文档](../../raw/model-api-reference/preparations/error-code.md)中各参数校验规则。

## 关键参数

核心参数包括 `model`、`api_key`、`base_url`（即 `DASHSCOPE_HTTP_BASE_URL`）、`workspace` 和 `region`。其中：
- `model` 必须使用百炼官方模型 ID（如 `qwen-plus`），**不可混用开源社区名称**（如 `Qwen/Qwen3.7-Plus`）；
- `api_key` 需与 `base_url` 所属地域匹配，否则触发 `401 InvalidApiKey` 错误；
- `base_url` 类型决定服务保障等级：**业务空间专属域名**（如 `llm-xxx.cn-beijing.maas.aliyuncs.com`）推荐用于生产，提供更高并发、3600秒超时及 SLA 99.9%；DashScope 域名（如 `dashscope.aliyuncs.com`）为兼容方案，但自2026年9月30日起将停用新特性 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)；
- `workspace` 和 `region` 是 DashScope SDK 2.0 客户端构造的必需参数，取代了 1.x 的全局变量配置方式 [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。

> **注意**：文档 5 与文档 6 对“DashScope 域名”的描述存在不一致。文档 5 称 DashScope 域名“自2026年9月30日起不再支持新特性”，而文档 6 未提及此时间点，仅说明“建议迁移”。此处以文档 5 的明确时间戳为准，开发者应规划迁移路径。

## 使用方式

1. **获取并配置 API Key**：在控制台对应地域页面创建 API Key，**务必选择正确的归属业务空间**（权限由业务空间决定，而非单个 API Key）；配置时优先使用环境变量 `DASHSCOPE_API_KEY`，避免硬编码 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
2. **安装 SDK**：Python 项目推荐安装 `dashscope>=2.0.1`（含 SDK Expert 智能助手）或 OpenAI SDK（`openai>=1.0.0`）；Java/Node.js/Go 等语言请按需引入对应 SDK [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)；
3. **选择 Base URL**：根据场景选用域名——生产用业务空间专属域名，试用用 `trial.*` 域名，并确保 `base_url` 中的 `{WorkspaceId}` 和 `{region}` 与实际一致；
4. **初始化客户端**：SDK 2.0 使用 `dashscope.Client(api_key=..., workspace=..., region=...)` 构造；1.x 存量项目可继续运行，但新代码应避免使用已下线的 Assistants/Threads API [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。

## 限制和注意事项

- **地域与密钥绑定**：API Key、Base URL、模型列表三者严格按地域绑定，跨地域调用必报 `401` 或 `404`；
- **额度与限流**：免费额度耗尽或触发 RPM/TPM 限制时，返回 `429 Throttling.RateQuota` 或 `Throttling.AllocationQuota`，需降频或申请配额 [错误码](../../raw/model-api-reference/preparations/error-code.md)；
- **安全实践**：**禁止在客户端（浏览器/移动端）或不可信环境硬编码长期 API Key**；敏感场景应使用临时 API Key（最长 1800 秒） [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)；
- **SDK 版本兼容性**：DashScope SDK 2.0 默认抛异常（`DashScopeError`），而 1.x 需手动检查 `response.status_code`；[流式输出](../concepts/streaming-output.md)行为也不同（2.0 默认增量，1.x 需设 `incremental_output=True`） [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)；
- **错误诊断**：遇到 `InvalidParameter` 等错误，可直接使用 DashScope SDK Expert 的 `/skill error-code` 命令快速定位修复，它会结合当前 SDK 版本给出可执行建议 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-api-reference/preparations/regions.md)
- [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)


