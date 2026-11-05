# Token

Token 是百炼平台中用于计量模型输入与输出内容的基本单位，是模型调用成本核算、性能监控与资源调度的核心度量基准。一个 Token 通常对应一个子词（subword）或标点符号，在文本场景下近似为中文字符（1–2 字/Token）或英文单词（1 单词 ≈ 1–3 Token）；在多模态场景中，Token 还涵盖图像 patch、音频帧、向量维度等经模型编码后的离散语义单元。

## 在百炼平台的不同场景中，这个概念如何使用

- **计费计量**：所有模型调用（含智能体 Flow、Managed Agents、知识库 RAG 中的向量/排序/路由/问答模型、ParseX 字段抽取所触发的模型）均按 `input_tokens + output_tokens` 精确计费。例如，一次知识库问答若输入 500 Token、生成回答消耗 300 Token，则计费总量为 800 Token。
- **监控告警**：`TotalToken 数` 是模型监控的核心指标，支持分钟级聚合与阈值告警，常用于成本异常检测（如“1 分钟总 Token 超过 10,000”触发告警）。
- **评测成本控制**：模型评测任务中，每条样本的单次推理即产生对应 Token 消耗；启用 `单样本推理次数 > 1`（如 Pass@K）时，Token 总用量线性增长，需在效果验证与成本间权衡。
- **高速推理参数控制**：在 Batch 推理中，`thinking_budget` 以 Token 为单位限制思考过程长度；在 Prime 模式响应中，`usage.completion_tokens_details.reasoning_tokens` 明确分离思考 Token 与最终输出 Token，便于精细化归因。
- **异步任务与安全防护**：异步模型（如文生图）虽不直接暴露 Token，但其底层调度与配额仍基于等效 Token 换算；Agent 安全高级防护中的 `Credit` 单位也按被检内容的 Token 数换算（1 Credit ≈ 1 Token），每日免费额度 300 Credit/席位。

## 关键参数和配置

- **`input_tokens` / `output_tokens`**：API 响应 `usage` 字段中返回的标准字段，开发者应始终解析并记录，用于成本复盘与预算控制。
- **`reasoning_tokens`**（仅 Prime 模式）：位于 `usage.completion_tokens_details` 下，标识思维链（CoT）生成消耗，不计入最终 `completion_tokens`，但参与计费。
- **`thinking_budget`**（Batch & Smart Routing）：整数型请求参数，单位为 Token，用于约束模型内部推理步骤长度，超限将截断并返回 `finish_reason: "length"`。
- **`max_tokens`**（同步接口）：最大输出 Token 数上限，影响响应长度与费用上限；注意：在 Smart Routing 模式下，该参数会自动转为 `max_completion_tokens` 并用于模型筛选。

## 面向开发者，简洁实用

- ✅ **必做**：所有生产环境模型调用，应在日志或监控中持久化记录 `usage.input_tokens` 和 `usage.output_tokens`，避免仅依赖账单延迟数据（约 10 分钟滞后）。
- ✅ **推荐**：对高并发 Agent 或知识库应用，通过 `TopK`（如向量召回设为 20 而非默认 50）主动压缩输入 Token，可显著降低排序与生成环节费用。
- ⚠️ **注意**：Token 计量不含 Prompt 中的系统指令（system [prompt](../guides/prompt.md)）以外的元信息，但含用户输入、历史对话（messages）、工具调用参数（tool_calls）及 JSON Schema 描述；多模态输入（如 base64 图片）按实际编码后长度折算 Token。
- ⚠️ **避坑**：`temperature=0` 不减少 Token 消耗；`n > 1`（并行生成多条结果）会使 `output_tokens` 成倍增加；流式响应中 `usage` 仅在末尾返回，勿在中间 chunk 解析。

## 关联主题页

- [agent billing](../guides/agent-billing.md)
- [model monitoring](../guides/model-monitoring.md)
- [model evaluation introduction](../guides/model-evaluation-introduction.md)
- [model high speed inference](../guides/model-high-speed-inference.md)
- [more about models](../api/more-about-models.md)


