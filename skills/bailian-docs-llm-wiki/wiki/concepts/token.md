# Token

Token 是百炼平台中用于计量模型输入与输出文本长度的基本单位，也是资源配额、计费和限流的核心度量基准。一个 token 通常对应一个子词（subword）或标点符号，而非单个字符或字；实际切分由模型底层 tokenizer 决定，例如 `"Hello, world!"` 在 Qwen 系列模型中解析为 3 个 tokens。

## 在百炼平台的不同场景中，这个概念如何使用

- **推理调用（Inference）**：所有 `/v1/chat/completions`、`/v1/completions` 等同步/异步推理接口均按 `input_tokens + output_tokens` 总和计费与限流。Token Plan、高速推理通道、QPM/QPS 限流等机制均以此为计量基础。
- **配额管理（Token Plan）**：Token Plan 是面向推理请求的资源配额体系，其核心约束项（如 `tokens_per_minute`、`max_tokens_per_request`）全部以 token 为单位，不覆盖微调、向量嵌入（`/v1/embeddings`）或知识库索引等非推理类任务。
- **高速推理优化**：`enable_high_speed` 模式对 token 总量有硬性限制（`input_tokens + max_tokens ≤ 8192`），超出即自动降级至普通通道；同时建议将 `max_tokens` 设为 ≤1024 以提升命中率。
- **异步与批量任务**：`/v1/batch/invoke` 批量调用按每个子任务独立计算 tokens；异步任务（`async: true`）同样按最终生成的 tokens 计量，计入发起账号的 Token Plan 配额。
- **用量监控与调试**：通过 `/v1/usage/token-plan` 可查询每小时粒度的 token 消耗明细；SDK 日志或响应头（如 `X-DashScope-Usage`）也常返回本次请求的 `input_tokens` 和 `output_tokens`，便于开发者精准归因。

> ⚠️ 注意：token 数量以服务端 tokenizer 解析结果为准，与客户端字符数、UTF-8 字节数无关；不同模型（如 Qwen-VL、Qwen-Audio）的 tokenization 规则可能不同，不可跨模型直接换算。

## 关键参数和配置

| 参数名 | 所属场景 | 说明 | 典型取值范围 |
|--------|----------|------|--------------|
| `max_tokens` / `max_tokens_per_request` | 推理 API、Token Plan | 单次请求最大输出 token 数，硬性截断阈值 | `1–8192`（默认 `2048`） |
| `tokens_per_minute` | Token Plan | 每分钟总 token 配额（input + output），超限返回 `429` | 按 Plan 版本设定，如 `10k–1M/min` |
| `burst_ratio` + `burst_window_seconds` | Token Plan（进阶） | 突发流量弹性系数（需二者同时配置才生效），支持短时超额消耗 | `burst_ratio`: `1.0–3.0`；`burst_window_seconds`: `10–60` |
| `input_tokens` / `output_tokens` | 响应头或用量 API | 实际消耗的 tokens 数，用于调试与成本分析 | 响应头示例：`X-DashScope-Usage: {"input_tokens": 42, "output_tokens": 17}` |

## 面向开发者，简洁实用

- ✅ **必查响应头**：每次推理请求后检查 `X-DashScope-Usage`，确认实际 token 消耗是否符合预期，避免隐性超限。
- ✅ **合理设 `max_tokens`**：在满足业务需求前提下尽量降低该值——它既影响输出长度，也参与 Token Plan 配额计算和高速推理准入判断。
- ✅ **Token Plan 绑定要显式声明**：调用 API 时务必在 Header 中添加 `X-DashScope-Token-Plan: <plan_id>`，否则走默认配额，可能导致突发流量被限。
- ✅ **调试优先用 `qwen-turbo` 或 `qwen-plus`**：相同 [prompt](../guides/prompt.md) 下 token 数更少、成本更低；生产环境再按质量需求升级至 `qwen-max`。
- ❌ **不要混淆 token 与字符**：中文平均约 1–2 字符/Token，英文单词常为 1 Token，但标点、空格、特殊符号均独立计数；务必以服务端返回的 `input_tokens` 为准做容量规划。
- ❌ **不要在非推理场景误用 Token Plan**：微调、向量嵌入、知识库构建等任务不走 Token Plan，需单独购买资源包或按量计费。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [more about models](../api/more-about-models.md)


