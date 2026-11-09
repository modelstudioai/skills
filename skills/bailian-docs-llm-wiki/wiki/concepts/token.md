# Token

Token 是百炼平台中用于衡量模型输入与输出内容长度的基本计量单位，也是计费、限流、性能监控和资源调度的核心依据。它并非简单等同于字符或词，而是由模型 tokenizer 对文本（及图像、音频等多模态内容）进行子词切分后生成的离散单元。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用**：`max_tokens` 参数控制模型生成内容的最大 Token 数（不包含输入部分）；`input.messages` 的总长度以 Token 数（非字符数）为上限（Qwen2 系列默认上限 32768 tokens），超限将直接拒绝请求（HTTP 400）。
- **计费计量**：所有模型服务（包括大语言模型、向量模型、排序模型、路由模型等）均按 **输入 Token 数 + 输出 Token 数** 分别计费。例如 `text-embedding-v4` 按 0.0005 元/千 Token 计费，知识库 Rerank 费用取决于初步召回切片的总 Token 数，而非最终返回数量。
- **监控告警**：`模型消耗 TotalToken 数` 是模型监控的核心指标，支持配置环比突增、阈值越界等告警，是识别异常调用、排查成本飙升的首要依据。
- **限流控制**：配额（如 5 QPS / 账号）和吞吐能力（如独占吞吐单元）均以 Token 处理速率（tokens/s）为底层约束；流式响应中 `max_tokens` 的实际生效值可能略低于设定值，系因 token 分片边界与 chunk 切分策略导致，属正常行为。
- **多模态处理**：图像、音视频等非文本输入经预处理后同样被编码为 Token 序列参与计算（如 `qwen3-vl-plus` 的图像 patch 会被 tokenizer 映射为视觉 token），其 Token 消耗计入总用量并计费。

## 关键参数和配置

| 参数名 | 所在接口 | 类型 | 说明 | 常见取值 |
|--------|----------|------|------|-----------|
| `max_tokens` | 所有模型 API（DashScope 原生、OpenAI 兼容、Anthropic 兼容） | integer | 模型生成内容的最大 Token 数（仅输出侧） | `1024`（默认）、`2048`、`8192` |
| `input.messages` 长度限制 | DashScope 原生接口 | — | 请求体中 `messages` 内容总 Token 数上限（含 system/user/assistant） | `32768`（Qwen2 系列） |
| `TotalToken 数` | 监控系统（`model-telemetry`） | numeric | 单次调用中 `input_tokens + output_tokens` 总和，用于计费与告警 | 由平台自动统计，不可设置 |
| `top_k` / `repetition_penalty` | DashScope 原生接口（高级控制） | integer / number | 影响 token 采样过程的参数，间接调控输出 token 的多样性与重复性 | `top_k=50`, `repetition_penalty=1.1` |

> ⚠️ 注意：`max_tokens` 仅限制生成长度，**不控制输入长度**；输入超限需自行截断或分块；流式响应下该参数仍生效，但首 Token 延迟和 chunk 边界不受其影响。

## 面向开发者，简洁实用

- **必查响应中的 `usage` 字段**：每次成功调用返回的 JSON 中均含 `"usage": {"input_tokens": N, "output_tokens": M, "total_tokens": N+M}`，这是验证实际 Token 消耗、调试截断逻辑、核对账单的唯一可信来源。
- **调试建议**：本地开发时，使用 `dashscope` SDK 的 `get_tokenizer()` 工具（如 `dashscope.Tokenizer.get_instance('qwen-max')`）可精确估算输入文本的 Token 数，避免线上超限。
- **成本优化重点**：
  - 减少冗余 system prompt 和历史消息；
  - 知识库检索时降低 `vector_topk` 和 `keyword_topk`，直接减少送入 Rerank 的切片 Token 总量；
  - 流式场景下，若只需摘要，可设较小 `max_tokens` 并配合 `stop` 参数提前终止。
- **不要混淆**：Token ≠ 字符（中文常 1 字 ≈ 1–2 token，英文单词常拆为 subword）、≠ 词（无空格分隔时仍可切分）、≠ 行数。一切以 `usage` 字段和 tokenizer 实测为准。

## 关联主题页

- [get started with models](../guides/get-started-with-models.md)
- [qwen api reference](../api/qwen-api-reference.md)
- [agent billing](../guides/agent-billing.md)
- [model monitoring](../guides/model-monitoring.md)
- [more about models](../api/more-about-models.md)


