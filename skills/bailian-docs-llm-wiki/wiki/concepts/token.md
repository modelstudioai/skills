# Token

Token 是百炼平台中用于度量和计量大模型服务资源消耗的核心计费与配额单位，表示模型处理文本、图像、音频等输入输出内容时所消耗的最小语义单元数量。一个 token 通常对应一个子词（subword）、标点、空格或特殊控制符号；其实际长度取决于模型分词器（tokenizer），而非字符数。

## 在百炼平台的不同场景中，这个概念如何使用

- **配额管理（Token Plan）**：Token 是 Token Plan 的计量基础。平台按小时为单位分配 token 配额（如 `team` 版每小时 100 万 tokens），所有受支持的 API 调用（`chat`、`completion`、`embedding`）均按实际消耗的输入 + 输出 token 总数实时扣减配额。流式响应（streaming）的 token 扣减发生在请求完成时，而非逐块累计。

- **模型调用与推理**：每次 API 请求（标准 REST 或 Realtime API）均需明确指定 `model`，平台自动计算该次请求的输入 token 数（含 system [prompt](../guides/prompt.md)、messages、tools 等上下文）与输出 token 数（实际生成内容）。`max_tokens` 参数仅限制输出长度，不影响输入 token 计算。

- **可观测性与监控**：
  - **应用观测（Application Monitoring）**：自动采集并上报单次请求的 `input_tokens` 和 `output_tokens`，用于链路追踪、延迟归因与成本分析；
  - **模型监控（Model Monitoring）**：在「监控中心」提供按模型、应用、环境维度聚合的 token 消耗趋势（输入/输出分离统计），支持 P99 延迟与 token 效率（tokens/sec）联合分析；
  - **账单系统（Billing API）**：token 消耗是计费核心依据，账单明细中按模型类型、调用次数、总 token 数三者联动呈现，支撑成本分摊与用量审计。

- **组织治理（TokenPlan API）**：TokenPlan API 不直接处理 token 计算，但通过席位（seat）分配、成员管理、订阅配置等方式，将 token 配额以组织为单位进行分发与隔离，实现企业级资源治理。

## 关键参数和配置

- `plan`（必填，字符串）：声明本次调用所归属的 Token Plan 类型（`"personal"` / `"team"` / `"advanced"`），决定配额池与扣减规则；
- `max_tokens`（可选，整数）：硬性限制模型输出 token 上限（默认由模型决定），不参与配额计算，但影响实际 token 消耗；
- `stream: true`（Realtime API 强制）：启用流式响应时，token 统计仍以完整请求为单位，非逐 chunk 扣减；
- 监控相关参数（非调用参数，但影响 token 数据可见性）：
  - `enable_monitoring: true`（应用级开关，开启后才采集 token 指标）；
  - `trace_sampling_rate`（控制 token 级 trace 的采样比例，影响观测粒度与存储开销）。

> ⚠️ 注意：所有 token 计算均基于百炼平台内置 tokenizer（与 Qwen 系列模型一致），开发者无需自行分词；输入内容（如 base64 图像、PCM 音频）经预处理后统一转换为 token 序列计入总量。

## 面向开发者，简洁实用

- **快速验证 token 消耗**：调用任意模型 API 后，检查响应头 `X-DashScope-Token-Usage`（格式为 `input:123,output:456,total:579`），该字段在所有成功响应中稳定返回。
- **避免配额超限**：单次请求消耗不得超过当前 Plan 小时配额的 10%；若频繁触发 `429 Too Many Requests`，请检查 `max_tokens` 是否设置过大，或拆分长上下文。
- **流式调用优化**：虽 token 扣减延迟至请求结束，但 `content_block_delta` 事件中 `delta.token_count` 字段可实时获知已生成 token 数，用于前端进度提示。
- **成本控制建议**：优先使用 `qwen-turbo` 处理简单任务；对 RAG 应用，监控检索阶段 token 占比（应用观测中可下钻），避免冗余上下文注入。
- **调试技巧**：在请求 Header 中添加 `X-Bailian-Trace-ID`，可在「观测」页精准定位某次高 token 消耗请求的完整链路与各阶段耗时。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [realtime api user guide](../api/realtime-api-user-guide.md)
- [application monitoring](../guides/application-monitoring.md)
- [model monitoring](../guides/model-monitoring.md)
- [billing api](../api/billing-api.md)


