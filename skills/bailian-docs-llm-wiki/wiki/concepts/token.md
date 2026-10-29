# Token

Token 是百炼平台中用于计量模型输入与输出内容长度的基本单位，也是资源配额、计费、限流与监控的核心度量基准。它并非原始字符或字节，而是由百炼平台统一 tokenizer 对文本、图像描述、音频转录等内容进行语义化切分后得到的离散单元，其数量直接反映模型处理的计算负载。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用与推理**：每次 API 请求的 `prompt`（输入）和 `completion`（输出）均被转换为 Token 序列；`max_tokens` 参数限制单次响应最大生成 Token 数，而模型上下文窗口（如 `qwen-max` 为 32768 tokens）则约束总输入+输出长度上限。
- **Token Plan 配额管理**：Token 是 Token Plan 的计量基础——`quota`（日配额）、`burst`（突发容量）、`max_tokens`（单次硬截断）均以 Token 为单位；配额校验仅在请求经百炼标准路由（如 `/v1/services/aigc/text-generation/generation`）转发时生效。
- **费用与用量统计**：所有按 Token 计费的模型调用（含文本生成、多模态理解、向量嵌入等），其账单与监控指标（如「调用量（Token 总量）」）均基于百炼内部 tokenizer 统计，不依赖客户端估算。
- **模型评测**：在「大模型评估」维度中，裁判模型的评分过程本身会产生额外 Token 消耗，该部分费用独立于被评测模型，需在评测配置中明确选择裁判模型（如 `qwen-max`）并纳入成本考量。
- **模型监控与告警**：`调用量（Token 总量）` 是核心可观测指标，支持配置实时告警（如“Token 成本突增”）；失败率、限流次数（429）等健康指标也隐式关联 Token 使用强度。
- **SDK 与 API 集成**：DashScope SDK 2.0 及 [OpenAI 兼容接口](openai-compatible-interface.md)中，`max_tokens`、`stream` 等关键参数均围绕 Token 行为设计；流式响应中每个 `delta.content` 片段对应若干 Token，开发者需按 Token 粒度处理增量输出。

## 关键参数和配置

- `max_tokens`：单次请求允许生成的最大 Token 数（不含 [prompt](../guides/prompt.md)），超限将被服务端强制截断。不同模型有各自上限（如 `qwen-turbo` ≤4096，`qwen-max` ≤8192），须查阅对应模型文档。
- Token 计算一致性：所有 Token 数均以百炼平台内部 tokenizer 为准，与 HuggingFace tokenizer 或本地估算可能存在 ±5% 偏差；实际计数不开放调试接口，建议通过监控数据反向验证。
- 地域隔离性：Token Plan 配额、监控数据、推理日志均按地域隔离（如华东1 创建的 Plan 不在华北2 生效），Token 消耗不跨 region 累计。
- 安全与合规约束：含敏感词或违法内容的请求会被内容安全策略拦截，返回 400 错误且**不计入 Token 配额**，但会记录在监控的「内容安全拦截次数」中。

## 面向开发者，简洁实用

- ✅ **务必校验实际 Token 消耗**：使用控制台「模型监控 → 用量统计」查看真实 Token 数，而非依赖本地 tokenizer 估算；尤其在多模态（图片 URL、视频描述）场景下偏差更明显。
- ✅ **配额调试技巧**：若遇 `429 Too Many Requests`，优先检查 `X-DashScope-Token-Plan-ID` Header 是否正确传递，再确认 `quota`/`burst` 设置及是否已过期（自然日重置）。
- ✅ **流式开发注意**：启用 `stream=true` 时，`max_tokens` 仍作用于整次响应；每个 `chunk` 的 `delta.content` 长度不可预测，应以 Token 累计逻辑（非字符串长度）做缓冲控制。
- ❌ **避免常见错误**：
  - 不要混用各地域 API Key 或 Base URL，会导致 Token 计费归属错乱；
  - 不要将 `max_tokens` 设为超过模型上下文窗口（context window）的值，否则触发 `400 InvalidParameter`；
  - 不要通过 DashScope 原生 SDK 直接调用 `dashscope` 裸 API（如 `/api/v1/chat/completions`），Token Plan 将失效——必须走百炼网关路由（`/v1/services/...`）。
- 📌 **生产建议**：高并发场景下，结合 `burst` + `burst_window_seconds` 缓冲瞬时峰值，同时用监控告警盯住 `TPM`（Tokens Per Minute）趋势，提前扩容或优化 [prompt](../guides/prompt.md) 长度。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [preparations](../api/preparations.md)
- [get started with models](../guides/get-started-with-models.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [model monitoring](../guides/model-monitoring.md)


