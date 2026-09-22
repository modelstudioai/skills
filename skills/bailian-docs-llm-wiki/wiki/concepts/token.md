# Token

Token 是百炼平台中用于计量模型调用资源消耗的最小计费与配额单位，表示模型处理文本、图像、音频等内容时实际解析或生成的基本语义单元（如子词、视觉 patch 或音频帧）。一个请求的总 Token 数 = 输入 Token（[prompt](../guides/prompt.md) + history + system message 等） + 输出 Token（模型生成内容），该数值直接决定计费金额、配额扣减和限流判断。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有按量付费模型（LLM、Embedding、多模态、语音等）均以实际消耗的 Token 数为计费基础。输入/输出 Token 分开计价，部分功能（如上下文缓存命中）支持折扣计费。
- **Token Plan 配额控制**：通过 `X-Token-Plan-ID` 绑定 Token Plan 后，每次 API 调用（`/v1/chat/completions`、`/v1/embeddings` 等）的总 Token 消耗将实时扣减对应 Plan 的 `max_tokens_per_day` 配额，并受 `max_qps` 速率限制约束。
- **监控与可观测性**：模型监控系统自动采集并聚合 `token_usage_input` 和 `token_usage_output` 指标，支持按小时/分钟粒度分析用量趋势、识别异常 Token 暴增或低效 [prompt](../guides/prompt.md)。
- **异步任务与文件处理**：图像/视频生成等异步任务在结果返回时一次性上报总 Token 消耗；上传文件（如图片、音频）用于多模态推理时，其编码后产生的 Token 也计入本次请求总量。
- **免费额度与成本优化**：新人免费额度、节省计划抵扣、吞吐预留（TPM）等均以 Token 为核算基准；额度优先级为「免费额度 > 资源包 > 节省计划 > 按量付费」。

> ⚠️ 注意：Token 统计不含硬编码的系统提示词（system [prompt](../guides/prompt.md)）模板部分；流式响应（`stream=true`）的 Token 在整个响应结束时一次性扣减，非逐 chunk 扣减；Token Plan 不适用于模型微调训练、异步批量（`/v1/batch`）及 Coding Plan 独立通道。

## 关键参数和配置

| 参数 | 说明 | 典型值/范围 | 使用位置 |
|------|------|-------------|----------|
| `input_tokens` / `output_tokens` | 响应体中返回的实际消耗 Token 数（只读） | 整数，≥0 | API 响应字段（如 `/v1/chat/completions`） |
| `max_tokens` | 控制模型最大输出长度，直接影响 `output_tokens` 上限 | 1–8192（依模型而异） | 请求 body 参数 |
| `token_plan_id` | Token Plan 唯一标识符 | 字符串（如 `tp-abc123`） | 请求 Header：`X-Token-Plan-ID` |
| `max_tokens_per_day` | 每日 Token 总量上限（单位：千 Token） | 1–100000 → 实际为 1,000–100,000,000 tokens/天 | Token Plan 创建参数 |
| `X-RateLimit-Remaining-Tokens` | 当前 Plan 剩余可用 Token 数（Header 返回） | 整数，单位：千 Token | 响应 Header（启用 Token Plan 时） |

## 面向开发者，简洁实用

- ✅ **务必校验响应 Header**：若看到 `X-RateLimit-Remaining-Tokens`，说明 Token Plan 已生效；若返回 `429 Too Many Requests` 且错误码为 `"TOKEN_EXHAUSTED"`，即当日配额已用尽。
- ✅ **流式调用需预估总量**：`stream=true` 不降低 Token 消耗，仅改变传输方式；请用 `max_tokens` 合理约束输出长度，避免意外超支。
- ✅ **监控排查首选 Token 维度**：在控制台「模型监控」中筛选 `token_usage_input` 和 `token_usage_output`，快速定位高 Token 消耗请求（如过长 history、重复 prompt、未截断的文档输入）。
- ✅ **跨地域/子空间独立计费**：同一 `token_plan_id` 在不同 project 或地域下不共享配额；子业务空间调用需单独绑定 Plan。
- ✅ **调试建议**：首次集成 Token Plan 时，在沙箱环境用小配额（如 `max_tokens_per_day=10` → 10,000 tokens/天）验证扣减逻辑，再逐步放大。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


