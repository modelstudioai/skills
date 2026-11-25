# Token

Token 是百炼平台中用于计量大模型输入与输出文本单元的最小语义单位，是模型推理、计费、监控与评测等核心能力的基础度量标准。一个 Token 通常对应一个词、子词（subword）或标点符号，其实际切分由模型自身的 tokenizer 决定；开发者无需手动分词，但需理解其数量直接影响成本、延迟与资源配额消耗。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用与计费**：所有 SaaS 模型（如 Qwen 系列、Qwen-VL、Qwen-Audio）及自定义部署模型的推理费用，均按 `(input_tokens + output_tokens)` 精确计量，单位为「千 Token」（即每 1000 Token 计为 1 千 Token）。知识库检索中的 Rerank 阶段也按召回切片的总 Token 数计费，而非最终返回结果数。
- **Token Plan 套餐**：Token 本身**不直接计费**，而是作为 Credits 消耗的底层依据。一次调用消耗的 Credits 由输入 Token、输出 Token、缓存命中率、模型单价及[工具调用](tool-calling.md)次数共同加权计算，例如 `qwen3.6-plus` 单次请求可能消耗约 3.18 Credits，但对应的实际 Token 数需通过响应头或用量 API 查看。
- **模型监控**：控制台「模型监控」页面提供 `模型消耗 TotalToken 数` 指标（支持告警），用于追踪成本趋势与异常突增；审计日志中记录每次调用的精确 `input_tokens` 和 `output_tokens`，但不含原始 Prompt/Response 内容。
- **智能体（Agent）与工作流**：Managed Agents、Flow Agent 中的模型节点、知识库问答、ParseX 解析等环节，均独立按 Token 消耗计费；其中知识库 Rerank 费用取决于「初步召回总切片数 × 平均切片 Token 数」，易被低估。
- **模型评测**：评测任务执行时，裁判模型（如 Qwen-Max）对样本的自动评分过程本身也产生 Token 消耗，计入评测总成本；单样本多次推理（Pass@K）会线性增加 Token 开销。

## 关键参数和配置

- **`input_tokens` / `output_tokens`**：API 响应头（如 `x-dashscope-input-tokens`、`x-dashscope-output-tokens`）及用量接口（`/v1/usage`）中返回的整数字段，精度为 1 Token，是计费与监控的唯一权威依据。
- **Token 缓存影响**：启用上下文缓存后，重复输入可提升缓存命中率，降低有效 `input_tokens` 消耗；监控中 `缓存命中率` = `缓存命中 Token 数 / 输入 Token 数`，该指标不可告警，仅用于性能分析。
- **多模态 Token 计算**：Qwen-VL、Qwen-Audio 等多模态模型的 Token 数包含图像 patch、音频帧等编码后 token，非纯文本长度；文生图/视频类模型暂不返回结构化 Token 字段，其用量以 Credits 或调用次数计量。
- **无显式配置项**：Token 切分由模型 tokenizer 自动完成，开发者不可干预；但可通过精简 Prompt、限制 `max_output_tokens`、启用流式响应（减少首 Token 延迟感知）等方式主动优化 Token 效率。

## 面向开发者，简洁实用

- ✅ **必查响应头**：调试时优先检查 `x-dashscope-input-tokens` 和 `x-dashscope-output-tokens`，而非估算字符数或词数。
- ✅ **用量溯源**：在控制台「用量分析」或调用 `/v1/usage/summary` API，按模型、API Key、时间范围下钻查看 Token 消耗明细。
- ✅ **成本预估公式**：`费用 ≈ (input_tokens + output_tokens) / 1000 × 单价（元/千 Token）`；单价见[模型定价页](https://help.aliyun.com/zh/dashscope/developer-reference/pricing)，注意区分地域与模型版本。
- ⚠️ **避免误区**：Token ≠ 字符 ≠ 词；中文平均约 1.5–2 字符/Token，英文约 0.75 词/Token；切勿用 `len(prompt)` 代替 `input_tokens`。
- ⚠️ **Token Plan 注意**：`sk-sp-` Key 调用只抵扣 Credits，不暴露原始 Token 数；如需精确 Token 分析，请改用 `sk-` Key 调用同一模型并开启监控。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [agent billing](../guides/agent-billing.md)
- [model monitoring](../guides/model-monitoring.md)
- [test 1](../guides/test-1.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)


