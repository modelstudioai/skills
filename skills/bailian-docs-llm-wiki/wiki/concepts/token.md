# Token

Token 是百炼平台中用于计量模型输入、输出及中间计算过程的最小语义单元，是计费、配额控制、限流与资源调度的核心基础单位。它不直接对应字符或字节，而是由模型 tokenizer 根据语言结构（如子词、标点、空格）动态切分生成，同一文本在不同模型下产生的 Token 数量可能不同。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用**：每次 API 请求（同步 `/v1/chat/completions`、异步 `/v1/async/task`、批量 `/v1/batch/invoke`、流式响应）均按实际消耗的 `input_tokens + output_tokens` 计量，计入 Token Plan 配额与账单。流式响应以最终 `usage.total_tokens` 为准，非预估。
- **模型训练与调优**：文本类模型训练按训练数据总 Token 数计费；图像/视频/语音类任务则按等效 Token（如音频时长×采样率折算）统一归一化计量。
- **吞吐预留（TPM）**：TPM（Tokens Per Minute）是吞吐容量单位，1 kTPM = 1000 tokens/分钟，用于购买预置推理吞吐能力，输入/输出 Token 分别按不同单价结算。
- **模型评测**：被评测模型的每次推理产生 `input_tokens + output_tokens`；若启用「大模型评估」维度，裁判模型（如 `qwen-max`）对每条样本的评分过程也独立产生 Token 消耗，按实际用量计费。
- **Token Plan 管理**：`token_quota`（日额度）、`token_rate_limit`（TPS）、`burst_capacity`（突发缓冲）等参数均以千 Token（kToken）为单位配置，构成细粒度用量隔离与成本管控的基础。

> ⚠️ 注意：Token 不用于模型微调训练任务的配额控制（该场景由独立训练配额管理），也不作用于向量检索、PAI-DSW 或 OSS 存储等非模型服务。

## 关键参数和配置

| 参数名 | 单位 | 说明 | 典型值范围 |
|--------|------|------|-------------|
| `input_tokens` | 个 | 模型接收到的 prompt、system message、历史对话等输入内容经 tokenizer 切分后的总 Token 数 | 取决于输入长度，如 `qwen3.7-plus` 最高支持 1M 输入 Token |
| `output_tokens` | 个 | 模型实际生成的 completion 内容的 Token 数（不含 stop token） | 通常 ≤ `max_tokens` 参数设定值 |
| `total_tokens` | 个 | `input_tokens + output_tokens`，见于 API 响应 `usage` 字段 | 用于计费与配额校验的唯一依据 |
| `token_quota` | 千 Token（kToken） | Token Plan 日额度，自然日重置 | 10–100000 kToken（即 10,000–100,000,000 tokens/天） |
| `token_rate_limit` | Tokens/秒（TPS） | 每秒最大允许消耗 Token 数 | 1–5000 TPS |
| `burst_capacity` | 千 Token（kToken） | 突发流量缓冲池，平滑瞬时高峰 | 建议设为 `token_quota × 0.1`，最小 5 kToken（个人版固定值） |

- 所有 Token 计量均以模型实际 tokenizer 输出为准，开发者可通过 `GET /v1/models/{model_id}` 接口查询模型支持的最大输入 Token 数及 tokenizer 特性。
- 缓存命中场景（如上下文缓存）按特定折算系数（0.1–0.25）计费，不改变原始 Token 数，仅影响费用结算。

## 面向开发者，简洁实用

- ✅ **必查**：调用前用 `GET /v1/models/{model}` 确认目标模型的 `max_input_tokens` 和 tokenizer 行为，避免因超限返回 `400 Bad Request`。
- ✅ **必看响应**：每次成功请求的 `usage` 字段（含 `prompt_tokens`, `completion_tokens`, `total_tokens`）是唯一可信的 Token 消耗依据，不可依赖客户端预估。
- ✅ **配额调试**：测试 Token Plan 时，在请求 Header 中添加 `x-token-plan-id: <plan_id>` 并观察返回状态码——超配额返回 `429 Too Many Requests`，配额不足但未超速返回 `403 Forbidden`（常因 `model_whitelist` 配置错误）。
- ✅ **成本优化**：
  - 对长文本输入，优先使用支持超长上下文的模型（如 `qwen3.7-flash-2026-07-15` 支持 1M 输入），避免多次切分调用；
  - 评测任务中，若无需高精度打分，优先选用「规则评估」替代「大模型评估」，节省裁判模型 Token 开销；
  - 使用免费额度时，务必使用**通用 API Key**（非 Token Plan 专属 Key），否则不生效。
- ❌ **禁止**：将 Token 数硬编码进业务逻辑（如假设“100 字 ≈ 120 Token”），必须以 API 实际返回 `usage` 为准；Token Plan 配置不支持通配符或正则匹配模型 ID。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [token plan api](../api/token-plan-api.md)
- [test 1](../guides/test-1.md)
- [model data overview](../guides/model-data-overview.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


