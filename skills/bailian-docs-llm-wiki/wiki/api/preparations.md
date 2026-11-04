# preparations

在调用阿里云百炼模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、地域与 Base URL 选择等基础准备。这些步骤直接影响鉴权、路由、限流和功能可用性，是所有模型调用的前置依赖。

## 支持的模型/功能

百炼支持文本生成、多模态对话、图像/视频生成、语音识别与合成、向量嵌入、重排序及智能体应用等多种模型能力。具体支持情况按地域划分，例如华北2（北京）支持全部功能（含模型调优、应用开发、高级监控），而新加坡、美国（弗吉尼亚）等地域暂不支持批量推理或模型调优 [选择地域、服务部署范围和接入域名](../../raw/model-api-reference/preparations/regions.md)。模型列表与上下文长度限制请以各地域控制台实际展示为准，不可跨地域混用模型名或 API Key。

> **注意**：文档 4 中提及的 `Assistants / Threads / Runs` 系列 API 已随 DashScope SDK 1.x 下线，服务端不再支持，新项目严禁使用 [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。

## 关键参数

核心参数包括 `model`（必须为控制台模型市场中开通的精确 ID，如 `qwen3.7-plus`，非开源社区名）、`stream`（[流式输出](../concepts/streaming-output.md)开关）、`enable_thinking`（思考模式，部分模型强制为 `true` 或仅支持流式）、`result_format`（思考模式下必须为 `"message"`）、`response_format`（结构化输出需提示词含 `json` 且 `enable_thinking=false`）等。参数取值范围严格受限：`temperature` ∈ [0.0, 2.0)，`top_p` ∈ (0.0, 1.0]，`max_tokens` 不得超过模型最大输出 Token 数，`messages` 长度须在模型输入 Token 上限内 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 使用方式

1. **获取并配置 API Key**：在百炼控制台对应地域的 [API Key](../../raw/model-api-reference/preparations/get-api-key.md) 页面创建，归属业务空间决定调用权限范围；推荐配置为环境变量 `DASHSCOPE_API_KEY`。
2. **安装 SDK**：生产环境优先使用 DashScope Python SDK 2.0.1+（`pip install -U "dashscope>=2.0.1"`），Java/Node.js/Go 开发者可选 OpenAI 兼容 SDK [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
3. **选择 Base URL**：生产环境**必须使用业务空间专属域名**（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），其提供更高并发、3600 秒超时及 WebSocket/AOQ 协议支持；DashScope 域名（如 `dashscope.aliyuncs.com`）将于 2026 年 9 月 30 日起停止支持新特性 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)。
4. **初始化客户端**：DashScope SDK 2.0 使用 `Client(api_key=..., workspace="...", region="...")` 构造，而非 1.x 的全局变量配置 [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。

## 限制和注意事项

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，跨地域调用必报 401 或 404 错误。
- **限流策略**：业务空间专属域名 RPM/TPM 按模型区分、主账号维度合并计算；试用域名 RPM 仅 1000（主账号维度），且不提供 SLA 保障 [选择地域、服务部署范围和接入域名](../../raw/model-api-reference/preparations/regions.md)。
- **安全实践**：禁止在客户端代码或不可信环境硬编码长期 API Key；敏感操作（如删除 RAM 用户）可能导致关联 API Key 级联失效（2026年3月25日前创建的 Key）[获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **错误处理**：429（限流）需降频重试；400（参数错误）须校验 `messages` 结构、`content` 类型、`stop` 参数格式等；5xx 错误建议稍后重试 [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 来源文档

- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)
- [选择地域、服务部署范围和接入域名](../../raw/model-api-reference/preparations/regions.md)


