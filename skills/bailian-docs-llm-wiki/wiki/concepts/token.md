# Token 计量与计费

Token 计量与计费是百炼平台统一、精确的资源消耗度量与成本核算机制：所有模型推理类服务（含文本生成、嵌入、重排序、决策判断等）均以 UTF-8 字节级编码统计实际输入与输出 Token 数量，并据此按千 Token（kToken）为单位进行实时扣费或额度抵扣。该机制是平台按量计费体系的核心基础，贯穿免费额度、Token Plan、吞吐预留、Agent 组件化计费等全部成本场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **通用模型调用（/v1/chat/completions 等）**：输入 Prompt（含 system/user/assistant 消息）与输出 response 的所有字符均按 UTF-8 编码逐字节解析为 Token，系统自动四舍五入到整数 Token 后计入用量；例如 `qwen-plus` 调用一次含 1234 输入 + 567 输出，即消耗 1801 Token。
- **Token Plan 场景**：必须显式携带 `x-bailian-token-plan-id` 请求头，系统校验 Plan 绑定模型后，从预购额度中实时扣减本次调用的总 Token 数（输入 + 输出），余额不足返回 `402 Payment Required`。
- **Agent 应用**：模型调用费用独立于 Agent 其他组件（如知识库、沙箱、记忆库），但知识库中的 Rerank 调用、智能体路由时的 `qwen-plus` 判断、记忆检索注入 Prompt 所产生的额外 Token，均按实际 Token 数单独计费。
- **向量与排序服务（/v1/embeddings /v1/rerank）**：`text-embedding-v1` 等嵌入模型按输入文本总 Token 数计费；Rerank 模型则按 `query` + 所有 `documents` 的 Token 总和计费（非仅返回文档数），且 `query` 超 512 Token 将被静默截断——截断前的完整长度仍计入计量。
- **决策模型（decision-model-preview）**：严格按 `state` 字段（无论 string/object/array）序列化后的 UTF-8 字节长度换算 Token，上限 65536 Token；`questions` 结构体本身不参与 Token 计量，仅 `state` 内容计入。
- **监控与用量分析**：控制台「模型用量统计」中 `TotalToken 数` 是唯一可信的计费依据，延迟约 1–10 分钟；该数据与账单出账一致，可用于成本突增告警（如配置“1分钟内 TotalToken 增长 >50万”触发通知）。

## 关键参数和配置

- **Token 计量规则**：
  - 统一采用 UTF-8 字节级编码统计，非词元（token）级分词；
  - 输入与输出 Token 均计入，不可拆分抵扣；
  - 所有场景（含 Batch、缓存命中、长输入）均先按此规则得出原始 Token 数，再应用对应折扣或系数。
- **计费换算公式**：  
  `费用（元） = ⌈总 Token 数 ÷ 1000⌉ × 单价（元/千 Token）`  
  其中单价由模型、地域、计费模式（按量/Token Plan/节省计划）共同决定。
- **特殊系数（需主动启用）**：
  - 上下文缓存：命中部分 Token 按折扣系数（如 0.1）计费，创建缓存 Token 按 1.25× 标准单价计费；
  - 长输入阶梯：对 >32K 输入按区间应用系数（如 3x），直接作用于原始 Token 数；
  - Batch 调用：单价为实时推理的 50%，但不与缓存折扣叠加。
- **用量查询接口**：  
  `GET /api/v1/token-plan/usage`（Token Plan 余额）  
  `GET /api/v1/model/usage`（按模型/业务空间维度查询历史 Token 消耗）

## 面向开发者，简洁实用

- ✅ **务必校验 `model` 字段一致性**：Token Plan 中 `qwen-turbo` 不可用于 `qwen-plus`，否则直接报错；Agent 中知识库路由调用 `qwen-plus` 也需确保其属于已开通计费权限的模型。
- ✅ **警惕隐式 Token 消耗**：记忆库 `Search` 结果注入 Prompt、Rerank 的 `documents` 列表、决策模型中 `state` 的 JSON 序列化，都会显著增加 Token 数——建议在开发期用 `/v1/chat/completions` 的 `tools` 或 `response_format` 模拟结构化输入，预估 Token 开销。
- ✅ **调试技巧**：使用 `curl -v` 或 SDK 日志开启 debug 模式，查看响应头 `x-bailian-input-tokens` 和 `x-bailian-output-tokens` 字段，快速验证计量是否符合预期。
- ❌ **不要依赖客户端估算**：避免用字符数、单词数或第三方 tokenizer 估算 Token；百炼 Token 数以服务端实际编码结果为准，尤其对中文、emoji、多模态 base64 等场景差异显著。
- ⚠️ **注意地域隔离**：华北2（北京）的免费额度、价格、模型支持列表与其他地域完全独立；跨地域调用需重新确认 Token 计量逻辑与计费规则。

## 关联主题页

- [token plan guide](../guides/token-plan-guide.md)
- [agent billing](../guides/agent-billing.md)
- [test 1](../guides/test-1.md)
- [model monitoring](../guides/model-monitoring.md)
- [vector and sort](../api/vector-and-sort.md)
- [decision model](../api/decision-model.md)


