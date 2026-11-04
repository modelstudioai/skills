# Token 计费与计量

Token 计费与计量是百炼平台最基础、最核心的成本度量单元，指以模型处理的输入（Input）和输出（Output）文本/内容所消耗的 Token 数量为依据，进行精确计费与用量统计的机制。所有语言模型、向量模型、排序模型及部分多模态能力均按实际生成或处理的 Token 量计费，而非按请求次数、时长或文件大小。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用模型调用（实时推理）**：每次 API 调用均返回 `usage.input_tokens` 和 `usage.output_tokens`，二者之和即为本次调用总 Token 消耗。费用 = Input Tokens × 单价 + Output Tokens × 单价（单价按模型广场公示标准执行，如 `qwen3.7-plus`：输入 ¥0.004/千 Token，输出 ¥0.012/千 Token）。

- **RAG 知识库场景**：Token 消耗呈链式叠加——Query 向量化（`text-embedding-v4`）、召回文档向量化（若启用动态向量）、Rerank 排序（`qwen3-rerank`）、最终问答生成（大模型）各环节独立计费。挂载 N 个知识库时，向量+Rerank 的 Token 消耗量默认 ×N，需通过 `topk_vector` / `topk_keyword` 参数主动收敛。

- **向量与排序服务（Embedding / Rerank）**：  
  - 文本向量：按 `input` 中文本总字符数（经分词后）折算 Token，支持批量输入（如 100 行文本 → 按实际 Token 总量计费）；  
  - Rerank：`input.query` + `input.documents` 全部内容参与计费，`top_n` 仅影响返回结果数，不减少 Token 消耗。

- **音频类 API（ASR/TTS/Audio Generation）**：  
  - ASR：按语音时长折算 Token（≈ 1 秒 ≈ 15–25 Tokens，依语速与模型而定），非按音频文件字节；  
  - TTS：按输入文本 Token 数 + 语音合成隐式开销计费（平台自动核算，开发者无需换算）；  
  - Audio Generation：按 `input.prompt` 文本 Token + 生成音频等效 Token（按 duration_seconds 折算）合并计费。

- **Agent 工作流（Flow Agent / Managed Agents）**：Token 不跨节点“汇总”，而是**逐节点计量**——每个模型调用节点（如 LLM 节点、Rerank 节点、ParseX 解析后抽取节点）独立上报 Input/Output Tokens，并分别计费。工作流总费用 = 各节点 Token 费用之和。

- **模型训练与部署**：  
  - 训练：按训练数据总 Token 数 × 循环次数计费（文本模型）；  
  - 部署（PTU/DTU）：按预留的 TPM（Tokens/分钟）容量计费，与实际调用量无关；但实际调用仍额外产生按量 Token 费用（除非已购买足额节省计划覆盖）。

> ✅ 提示：Token 计量由百炼服务端在模型推理完成后精确返回，**不可由客户端预估或截断规避**。缓存命中可减少实际 Token 消耗，但缓存本身不收费。

## 关键参数和配置

| 参数 | 所属场景 | 说明 | 开发者操作建议 |
|--------|-----------|------|----------------|
| `usage.input_tokens` / `usage.output_tokens` | 所有模型 API 响应体 | 标准 OpenAI 兼容字段，真实消耗 Token 数，为计费唯一依据 | 必须在代码中解析并记录，用于成本归因与告警（如监控 `TotalToken 数` 突增） |
| `topk_vector` / `topk_keyword` | 知识库检索 | 控制向量/关键词召回数量，直接影响 Rerank 输入 Token 量 | 多知识库场景下建议设为 `10–30`（非默认 50），可降低 40%+ Rerank 成本 |
| `dimensions` | 向量模型 | 维度越高，Token 消耗略增（因向量序列更长），但不影响计费单价 | 仅在业务确需高维语义时启用（如 `2048`），常规检索 `1024` 足够 |
| `instruct`（Rerank） | Rerank 模型 | 自定义指令文本计入 `input_tokens`，增加 Token 消耗 | 指令应精简（≤ 20 字），避免冗余描述 |
| `enable_fusion`（多模态向量） | 多模态 Embedding | 开启融合向量会合并多模态内容，Token 消耗高于单模态独立向量 | 仅当业务强依赖跨模态对齐时启用，否则建议分模态调用降本 |

- **免费额度抵扣规则**：100 万 Token/模型/地域的免费额度，**仅适用于实时推理 API 调用**，且严格按 `input_tokens + output_tokens` 总和抵扣；Batch 调用、训练、部署、ParseX、MCP 工具调用等均不参与抵扣。

- **账单粒度**：Token 费用按小时聚合出账（单位：千 Tokens），控制台「模型用量」页面延迟约 10 分钟，**是计费唯一可信源**；监控中的 `TotalToken 数` 仅用于告警，不可用于对账。

## 面向开发者，简洁实用

- ✅ **必做**：在所有模型调用的响应解析逻辑中，提取 `usage.input_tokens` 和 `usage.output_tokens`，写入本地日志或监控系统，用于成本分析与异常检测。  
- ✅ **必控**：对知识库、Rerank、多步骤 Agent 流程，通过 `topk`、`max_length`、`temperature=0` 等参数主动约束输出长度，避免无意义 Token 浪费。  
- ✅ **必查**：定期登录控制台 → 「运维管理 > 模型监控」→ 查看「模型消耗 TotalToken 数」指标，配置环比突增告警（如 1 分钟内 > 10,000 Tokens）。  
- ❌ **勿信**：客户端估算 Token（如 `len(text)` 或粗略除法）、忽略 `usage` 字段、依赖文档中“典型值”做预算——Token 消耗受模型、prompt、上下文、温度等多重影响，必须以服务端返回为准。  
- 💡 **技巧**：启用「免费额度用完即停」开关（控制台设置），可防止额度耗尽后意外产生费用；结合 AI 通用型节省计划，用承诺消费换取最高 5.3 折 Token 折扣。

## 关联主题页

- [agent billing](../guides/agent-billing.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [vector and sort](../api/vector-and-sort.md)
- [audio api references](../api/audio-api-references.md)


