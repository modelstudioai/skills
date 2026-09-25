# Token

Token 是百炼平台中用于计量模型调用资源消耗的核心单位，代表模型处理文本、图像、音频等内容时所消耗的最小语义或计算粒度。在百炼的计费、配额控制、性能监控与模型服务治理中，Token 是统一的计量基准，直接关联成本、限流、用量统计与服务等级保障。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用与计费**：所有按 token 计费的模型（如 Qwen 系列、Qwen-VL、Qwen-Audio 及兼容 OpenAI 格式的第三方模型）均以实际消耗的 Token 数为计费依据。Token 数由输入（[prompt](../guides/prompt.md)）和输出（completion）共同构成，具体计算遵循各模型的 tokenizer 规则（如 Qwen 使用 `qwen-tokenizer`，按子词切分）。

- **Token Plan 配额管理**：Token Plan 通过 `quota`（日 token 总配额）和 `max_tokens`（单次请求最大 token 数）实现细粒度资源管控。配额按 UTC 每日 00:00 重置，超限请求返回 HTTP 429；单次超 `max_tokens` 则截断并返回 400 错误。Token Plan 绑定到具体模型 ID，不同模型间 quota 不共享。

- **模型监控与可观测性**：在「模型用量」和「实时监控」中，“TotalToken 数”是核心成本指标，支持按模型、API Key、时间维度聚合分析；告警可基于该指标配置（如“单日 TotalToken 超过阈值”），但注意：监控数据仅作参考，**不作为计费依据**，最终账单以费用中心为准。

- **TPM（Tokens Per Minute）预留**：吞吐能力预留以 token 为单位（非请求数），例如设置 `tpm=6000` 表示每分钟最多处理 6000 tokens 的请求流量，适用于高并发、低延迟生产场景。

- **数据处理与日志回流**：SFT 训练集清洗/增强等数据处理任务本身不直接消耗推理 Token，但其产出的数据集若用于模型训练或评测，后续训练/推理过程仍按实际 token 消耗计费；日志回流生成的 JSONL 数据集内容（如 [prompt](../guides/prompt.md)/response）在导入后，其 token 统计可用于效果分析，但不触发计费。

> ⚠️ 注意：Token 是计量单位，**不是认证凭证**。百炼平台中用于身份认证的是 API Key（`Authorization: Bearer <api_key>`）或阿里云 AccessKey（用于 Token Plan API），二者与 Token 概念正交，不可混淆。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 单位 | 约束 |
|------|----------|------|------|------|
| `max_tokens` | 模型 API 请求头 / SDK 参数 | 单次请求允许生成的最大 token 数（不含 [prompt](../guides/prompt.md)） | token（整数） | ≤ 模型上下文长度 × 0.8；超出返回 400 |
| `quota` | Token Plan 控制台 / API | 每日可用 token 总配额（含 prompt + completion） | token（整数，v2.3.0+ 已取消“千 token”单位） | 需在控制台显式设置；超限返回 429 |
| `X-Task-Plan-ID` | 模型 API 请求头 | 指定生效的 Token Plan | string（plan_id） | 必填（若启用 Token Plan）；SDK 中通过 `task_plan_id` 传入 |
| `X-RateLimit-Remaining` / `X-RateLimit-Limit` | 模型 API 响应头 | 实时剩余配额与总配额 | token | 用于客户端自主限流，值与所设 `quota` 一致 |
| `tpm` | 服务实例创建参数 | 吞吐预留能力，即每分钟最大 token 处理量 | tokens/minute | 创建服务实例时指定，影响资源调度与计费 |

## 面向开发者，简洁实用

- ✅ **务必校验响应头**：调用带 Token Plan 的接口后，检查 `X-RateLimit-Remaining` 是否递减，确认配额已生效。
- ✅ **Token 计算可预估**：使用百炼提供的 [Tokenizer 工具](https://bailian.console.aliyun.com/cn-beijing/model/tokenizer) 或 `dashscope` SDK 的 `count_tokens()` 方法，提前估算 prompt + expected completion 的 token 数，避免 400 截断。
- ✅ **监控与计费分离**：用量统计（监控页）有约 1 小时延迟，且不用于计费；真实账单请以「费用中心」为准；若需精确对账，建议开启 SLS 日志投递并解析 `usage.total_tokens` 字段。
- ❌ **不要混淆认证与计量**：`Authorization: Bearer <api_key>` 用于身份认证；`X-Task-Plan-ID` 用于配额绑定；二者需同时携带才能既鉴权又控量。
- ⚠️ **免费额度独立**：新用户赠送的免费 quota 与 Token Plan 的 `quota` 互不影响，也不计入其统计，无需额外配置即可叠加使用。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [model data overview](../guides/model-data-overview.md)
- [model monitoring](../guides/model-monitoring.md)


