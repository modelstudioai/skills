# Token 计量与管理

Token 计量与管理是百炼平台对大模型及相关 AI 组件（如向量模型、排序模型、路由模型等）资源消耗进行精确度量、实时监控与成本控制的核心机制。所有模型调用的计费均以输入/输出 Token 数量为基本单位，按千 Token（kToken）粒度统计并结算。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型推理调用**：文本生成、[函数调用](function-calling.md)、JSON Schema 输出等所有同步/流式请求，均按 `input_tokens + output_tokens` 精确计量。例如调用 `qwen3-32b` 处理 1200 字 Prompt 并生成 850 字响应，实际消耗 Token 数由模型 tokenizer 精确计算，而非字符或字数估算。

- **RAG 知识库检索**：Token 消耗贯穿全流程：
  - 向量模型（embedding）：按查询文本 Token 数计费；
  - 排序模型（rerank）：按「初步召回切片总数 × 平均切片 Token 数」计费，**与最终返回 TopK 数量无关**；
  - 路由模型（router）：按路由决策输入（如 query + candidate list）Token 数计费；
  - 问答模型（LLM answer）：按最终生成答案的输入上下文（含检索结果拼接）与输出 Token 数双重计费。

- **Agent 工作流（Flow Agent / Managed Agents）**：Token 计量嵌入每个可执行节点：
  - Prompt 编排、工具调用前的参数生成、多步推理中的中间状态构造，均触发模型调用并产生 Token 消耗；
  - 上下文缓存自动生效，其读写操作不额外计费，但缓存内容参与后续模型调用时仍计入输入 Token。

- **ParseX 结构化抽取**：图文解析中，OCR 文本提取、字段识别 Prompt 构造及结构化生成均按实际 Token 计费；音视频转文本后的摘要/关键词生成同样纳入 Token 计量。

- **高速推理能力（Prime / PTU / DTU / 智能路由）**：Token 计量逻辑保持一致，不因加速模式改变——Prime 模式提升 TPS 但不改变单次 Token 消耗；智能路由选择低价模型可直接降低千 Token 单价；DTU/MU 等独占部署按实际 Token 消耗计费，无固定带宽包绑定。

> ⚠️ 注意：监控系统中的 `TotalToken 数` 仅用于可观测性（延迟约 1–2 分钟），**不作为计费依据**；费用核算以账单中心每小时聚合的用量明细为准，延迟约 10 分钟。

## 关键参数和配置

- **`input_tokens` / `output_tokens`**：API 响应体中 `usage` 字段返回的精确值（整数），开发者应主动解析并记录，用于成本归因与预算控制。
- **`max_output_tokens`**（原 `max_tokens`）：硬性限制输出长度，直接影响 `output_tokens` 上限，是控制成本最直接的参数。
- **TopK 类参数**（如知识库 `vector_top_k`, `keyword_top_k`）：虽不直接计费，但显著影响排序模型 Token 消耗量——增大 TopK 将线性增加召回切片数，从而推高 rerank 阶段 Token 成本。
- **`stream: true`**：流式响应不影响总 Token 计量，但需注意部分模型（如 GLM-5.2 Prime）在流式下会额外生成 reasoning content，可能增加 `output_tokens`。
- **模型选型**：不同模型千 Token 单价差异显著（如 `qwen2.5-7b` vs `qwen4-max`），且长上下文支持能力（32K vs 65K）直接影响单次请求最大 Token 消耗上限。

## 面向开发者，简洁实用

- ✅ **必做**：每次模型调用后解析响应中的 `"usage": {"input_tokens": N, "output_tokens": M}`，累加至业务维度（如用户 ID、会话 ID、功能模块）进行成本分摊。
- ✅ **推荐**：在知识库检索中，将 `vector_top_k` 设为满足业务效果的最小值（如从 100 降至 30），可显著降低 rerank Token 成本。
- ✅ **推荐**：对确定性任务（如[函数调用](function-calling.md)、结构化输出），启用 `temperature=0` 并设置合理 `max_output_tokens`，避免无效生成。
- ❌ **避免**：在非必要场景（如简单关键词匹配）调用大模型；优先使用轻量级组件（如 ParseX 内置规则引擎）替代 LLM。
- 🔍 **排查成本异常**：若发现 Token 消耗突增，优先检查：
  - 是否误设过大 `max_output_tokens`；
  - 是否在循环中重复调用同一模型（如未缓存 embedding）；
  - 是否知识库召回 TopK 设置过高，导致 rerank 输入爆炸；
  - 是否启用了未预期的智能路由或 AUTO 模式，调用高价模型。

Token 是百炼平台最细粒度的成本单元。理解其计量逻辑、主动配置关键参数、结合用量统计与账单明细闭环分析，是实现高效、可控 AI 应用落地的基础能力。

## 关联主题页

- [agent billing](../guides/agent-billing.md)
- [get started with models](../guides/get-started-with-models.md)
- [model monitoring](../guides/model-monitoring.md)
- [test 1](../guides/test-1.md)
- [model high speed inference](../guides/model-high-speed-inference.md)


