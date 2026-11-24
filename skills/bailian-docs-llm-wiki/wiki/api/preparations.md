# preparations

在调用百炼平台模型服务前，开发者需完成 API Key 获取与配置、SDK 安装、Base URL 选择等基础准备。这些步骤直接影响鉴权、路由、功能可用性及稳定性，是所有模型调用的前提。本文汇总关键配置项、参数约束与常见陷阱，帮助开发者快速建立可运行的调用环境。

## 支持的模型/功能

百炼支持文本生成、多模态对话、图像/视频生成、语音识别与合成、[向量嵌入](../concepts/vector-embedding.md)、重排序、智能体应用等多种能力。各能力对应不同 SDK 接口和模型 ID，例如 `qwen-plus`（文本）、`qwen3-vl-plus`（多模态）、`wanx2.1-t2i-turbo`（图像）、`paraformer-v2`（ASR）等。模型列表详见 [模型列表](raw/model-user-guide/get-started-with-models/models.md)，具体能力支持请参考各模型文档。**注意**：部分模型仅支持[流式输出](../concepts/streaming-output.md)（如思考模式模型），若非流式调用将返回 `InvalidParameter` 错误；另需确认目标模型已在控制台[模型市场](https://bailian.console.aliyun.com/cn-beijing/model/market)开通，否则报错 `The product is not activated` [错误码](../../raw/model-api-reference/preparations/error-code.md)。

## 关键参数

- **API Key**：必须通过控制台创建，且与地域强绑定，**不能跨地域混用**；新版 API Key 仅创建时完整显示一次，关闭后不可恢复 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
- **Base URL**：必须与 API Key 所属地域及计费方案匹配。生产环境推荐使用业务空间专属域名（如 `https://{WorkspaceId}.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`），试用场景可用 `trial.` 域名，中心化 `dashscope.aliyuncs.com` 域名仍可用但建议迁移 [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)。
- **模型名称**：严格区分大小写与格式，必须使用百炼官方模型 ID（如 `qwen3.7-plus`），不可混用开源社区命名（如 `Qwen/Qwen3.7-Plus`），否则报错 `Model not exist` [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **流式开关**：`stream=true` 是思考模式（`enable_thinking=true`）、音频输出、工具调用等场景的强制要求；非流式调用将触发 `InvalidParameter` 错误。

## 使用方式

1. **获取并配置 API Key**：在控制台对应地域页面创建 API Key，推荐归属至业务空间以实现权限隔离与成本核算；配置为环境变量 `DASHSCOPE_API_KEY`（Linux/macOS/Windows 均有详细示例）或直接传入 SDK 构造函数 [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)。
2. **安装 SDK**：推荐使用 DashScope Python SDK 2.0（≥2.0.1）或 OpenAI 兼容 SDK（Python/Node.js/Java/Go）。DashScope SDK 提供原生接口，OpenAI SDK 适配兼容模式；AOQ 实时语音/多模态模型需额外下载 [AOQ SDK](../../raw/model-api-reference/more-about-models/realtime-api-aoq-api/realtime-sdk-download.md) [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)。
3. **初始化客户端**：DashScope SDK 2.0 通过 `Client(api_key=..., workspace=..., region=...)` 构造，优先级为构造参数 > 环境变量 > 配置文件；1.x 版本已冻结维护，新项目请勿使用 [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)。
4. **调用模型**：使用对应能力的接口，如 `client.chat.completions.create()`（文本）、`client.multimodal.chat.create()`（多模态）、`client.images.generate()`（图像）。SDK Expert 可自动生成校验过版本的可运行代码，支持需求描述、错误诊断与代码修复 [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)。

## 限制和注意事项

> **注意**：文档 1 中关于 RAM 用户 API Key 的级联删除规则存在时效性矛盾——其明确指出“2026年3月25日前创建的 API Key 与 RAM 用户绑定，删除用户时同步删除”，但该日期明显为未来时间点，实际应为历史策略变更节点（如 2024 年某月），此为文档笔误，开发者应以控制台当前行为及最新公告为准。

- **地域隔离**：API Key、Base URL、模型列表均按地域独立，跨地域调用必报 `401 InvalidApiKey` [错误码](../../raw/model-api-reference/preparations/error-code.md)。
- **权限继承**：API Key 权限由其归属业务空间决定，同一空间内所有 API Key 权限一致；默认业务空间可调用全部标准模型，子业务空间仅能调用已授权模型。
- **安全实践**：严禁在客户端（浏览器、移动 App）硬编码长期 API Key；敏感环境应使用临时 API Key（最长 1800 秒）或服务端代理。
- **错误处理**：SDK 2.0 默认失败抛 `DashScopeError` 异常（含 `code`/`status_code`/`request_id`），而非检查响应状态码；[流式输出](../concepts/streaming-output.md)一律增量返回，无需手动设置 `incremental_output`（除智能体应用外）。
- **配额与限流**：触发 `Throttling.RateQuota` 或 `Insufficient_quota` 时需降低并发/频率或申请配额；免费额度耗尽后调用将被拒绝，需充值或升级套餐。

## 来源文档

- [获取与配置 API Key](../../raw/model-api-reference/preparations/get-api-key.md)
- [错误码](../../raw/model-api-reference/preparations/error-code.md)
- [安装SDK](../../raw/model-api-reference/preparations/install-sdk.md)
- [DashScope Python SDK 1.x 历史用法参考](../../raw/model-api-reference/preparations/dashscope-1x-legacy-reference.md)
- [DashScope SDK Expert](../../raw/model-api-reference/preparations/dashscope-sdk-expert.md)
- [Base URL总览](../../raw/model-api-reference/preparations/base-url.md)


