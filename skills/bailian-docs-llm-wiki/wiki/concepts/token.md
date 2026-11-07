# Token 计量与计费

Token 计量与计费是百炼平台对大模型相关服务（含文本、视觉、语音、向量等）进行资源消耗量化与费用结算的核心机制。平台按实际消耗的输入/输出 Token 数量（以千 Token 为计费单位）精确计量，费用实时生成并纳入统一账单体系，不按请求次数或调用时长计费。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型调用（`model experience`）**：所有同步/异步模型调用（包括文本生成、VL 多模态、ASR、TTS、Embedding、Rerank 等）均按实际 token 消耗计费。`usage` 字段在响应体中明确返回 `input_tokens` 和 `output_tokens`，开发者可据此监控和优化成本。例如：
  - 文本模型：按 prompt + completion 的 token 总数计费；
  - 视觉/语音模型：输入图像/音频经编码后折算为等效 token（具体换算规则见各子文档）；
  - 向量模型（embedding）：按输入文本长度（字符数或分词后 token 数）计费，不依赖输出维度；
  - 全模态模型：多模态输入统一归一化为 token 当量，按总当量计费。

- **知识库（RAG）**：Token 消耗发生在多个环节：
  - **向量化**：文档切片后送入 embedding 模型产生的输入 token；
  - **重排序（rerank）**：对召回结果做精排时的 query + document pair 输入 token；
  - **问答生成**：LLM 基于检索结果生成答案时的 prompt（含上下文）+ output token；
  > 注意：多个知识库并行检索时，token 消耗量按知识库数量线性叠加。

- **Flow Agent / Managed Agents**：Agent 自身不单独计费，但其执行过程中触发的模型调用（如 LLM 路由、工具参数生成、最终回答生成）均计入对应模型的 token 消耗，并体现在账单中“阿里云百炼大模型推理”类目下。

- **ParseX 文档解析**：虽主要按页/秒计量，但若启用“智能字段抽取”等依赖大模型的高级能力，该部分将额外产生 token 费用（归属模型调用类目），与基础解析费用分离。

- **安全高级防护**：内容安全检测（如敏感词、价值观、幻觉识别）按 Credit 计费，而 1 Credit ≈ 固定 token 当量（具体换算比以控制台实时显示为准），本质仍是 token 消耗的抽象计量形式。

## 关键参数和配置

- **计量精度**：Token 数量以整数计，账单按 **千 Token（kToken）四舍五入**，不足 1 kToken 按 1 kToken 计。
- **响应必含字段**：所有模型调用成功响应的 `usage` 对象中均包含：
  ```json
  "usage": {
    "input_tokens": 1234,
    "output_tokens": 567,
    "total_tokens": 1801
  }
  ```
- **计费模型标识**：Token 单价与所选 `model_id` 强绑定，不同模型（如 `qwen-max` vs `qwen-plus`）、不同地域（北京/新加坡等）单价可能不同，需以控制台「计费中心」实时价格为准。
- **免费额度抵扣**：新人/新功能赠送的免费 token 额度（如 Flow Agent 新人额度）自动优先抵扣模型调用费用，无需手动配置；额度有效期以控制台显示为准。
- **用量查询入口**：
  - 实时用量：控制台「用量中心」→「模型调用」页，支持按 `model_id`、`API Key`、时间范围筛选；
  - 历史账单：通过 Billing API 的 `GetBillingTrend` 接口，指定 `groupBy: [{"code": "BASE_MODEL"}]` 可获取各模型 token 费用明细。

## 面向开发者，简洁实用

- ✅ **务必解析响应中的 `usage` 字段**：这是唯一权威的 token 消耗依据，不可依赖请求长度或经验估算。
- ✅ **流式响应同样完整计费**：即使中断流式读取，已生成的 output tokens 仍会计费。
- ✅ **多模态输入需关注编码开销**：一张高分辨率图或一段长音频，其 token 当量可能远超文本，建议在生产环境预估并压测。
- ⚠️ **避免无效 token 浪费**：精简 prompt 中冗余说明、限制 `max_tokens`、启用 `stop` 参数截断无关输出，可显著降本。
- ⚠️ **注意跨模型 token 定义差异**：Embedding 模型按输入字符/分词计，VL 模型按图像 patch 编码后 token 计——务必查阅对应模型子文档的「Token 计算规则」章节。
- 🔍 **排查费用异常？**：先查用量中心确认 token 消耗量，再结合 Billing API 按 `API_KEY_ID` 分组，定位高消耗调用方。

## 关联主题页

- [agent billing](../guides/agent-billing.md)
- [model experience](../guides/model-experience.md)
- [more about models](../api/more-about-models.md)
- [billing api](../api/billing-api.md)


