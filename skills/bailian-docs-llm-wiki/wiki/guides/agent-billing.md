# agent billing

Agent billing 涵盖百炼平台中各类 Agent 形态（Managed Agents、Flow Agent、Sandbox）及关联组件（知识库、ParseX、安全高级防护）的计费模型。费用按实际使用量独立计量，支持免费额度、资源包与按量付费混合抵扣，所有计费以控制台账单为准。开发者需重点关注运行时长、Token 消耗、调用次数等核心计量维度，并合理配置以优化成本。

## 支持的模型/功能

不同 Agent 类型及其依赖组件的计费范围如下：

- **Managed Agents**：计费项包括会话运行时费（0.5 元/小时）、模型调用费（按所选模型如 `qwen-plus` 的 Input/Output Token 计费）、工具及 MCP 调用费（如 `web_search` 0.03 元/次）[计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **Flow Agent**（含智能体应用与工作流应用）：本身不单独收费，费用源自实际调用的模型、知识库、MCP 及解析节点；例如图片解析若选用 Qwen-VL 则产生对应模型调用费，而内置文档解析暂不计费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **Sandbox**：按秒计量，分为会话运行费（基础款 0.156 元/小时，进阶款 0.312 元/小时，旗舰款 0.624 元/小时）与数据保留费（0.0021 元/GiB·小时）[计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **知识库**：费用由规格费用（标准版 0.03 元/知识库/小时，旗舰版 0.2 元/RCU/小时）和模型调用费用（向量模型、排序模型、路由模型、问答模型）两部分构成，后者按实际 Token 消耗独立计费 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **ParseX**：按处理量计量，图文按页（¥0.02/页），音视频按秒（音频 ¥0.00035/秒，视频 ¥0.002/秒），字段抽取分“新文档直接抽取”（¥0.06/页）与“复用解析结果抽取”（¥0.04/页）两种单价 [计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Agent 安全高级防护**：正式计费后按“防御席位费 + 超额 Credits”组合计费（席位费 0.42 元/席位·小时，超额 Credit 0.0015 元/Credit），当前仍处于限时免费阶段 [计费说明 (raw/application-user-guide/agent-billing/billing.md)](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：文档 6 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md`，属同一份原始文档被重复收录，以单次引用为准。

## 关键参数

- **运行时长**：Managed Agents 和 Sandbox 均按实际启用/运行时长精确到秒或小时计费；知识库规格费用亦按小时累计，不足 1 小时按比例折算（如 9 分钟 = 0.15 小时）。
- **Token 消耗**：模型调用费（含大模型、向量模型、排序模型、路由模型）统一按输入 Token 总数计算，单位为“千 Token”，价格见各模型在模型广场的公开刊例价。
- **RCU（Retrieval Compute Unit）**：知识库旗舰版并发能力度量单位，1 RCU ≈ 支撑 50 QPS；变配按发生时间分段计费。
- **Credits**：Agent 安全高级防护中用于量化检测负载的虚拟单位，每个席位每日默认 300 Credits，有效期 24 小时，不结转。
- **TopK 参数**：知识库检索中，“初步向量检索 TopK”与“初步关键词检索 TopK”直接影响送入 Rerank 模型的切片总数，从而显著影响排序模型费用。

## 使用方式

- **用量查询**：统一通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看运行时长、Token、工具调用等明细；也可调用 `POST /usage/summary` 和 `POST /usage/trend` API 获取结构化数据 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **账单核对**：知识库规格费用在账单中商品名称为“阿里云百炼知识库（RAG）- 后付费”；模型调用费用（向量/排序）在商品名称为“阿里云百炼大模型推理”的明细中，通过实例 ID 后缀（如 `...-embedding-...` 或 `...-rerank-...`）识别 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **免费额度抵扣**：遵循固定顺序：**免费额度 > 资源包 > 按量付费**；多个知识库或席位共享额度时，按数量线性扣除（如 4 个标准版知识库每小时消耗 4 小时免费额度）。
- **成本优化操作**：
  - 知识库：关闭重排策略、降低 TopK 值、选用更低价向量模型；
  - Flow Agent：避免非必要启用联网搜索、MCP 或高 Token 消耗模型；
  - Managed Agents：及时终止空闲会话以停止运行时费。

## 限制和注意事项

- **免费额度时效性**：Managed Agents 赠送 10 小时运行时免费额度，自生效日起 30 天内有效；知识库新用户免费额度仅 30 天，老用户统一截止至 2026 年 2 月 3 日；逾期未用完自动作废。
- **模型调用费用不可抵扣规格费用**：知识库的模型调用费（如 `text-embedding-v4`）与规格费（如 0.03 元/小时）完全独立，免费额度和资源包均不覆盖模型费用 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **Sandbox 数据保留费易被忽略**：暂停状态或 Snapshot 会产生 `0.0021 元/GiB·小时` 的数据保留费，即使未运行也会持续计费。
- **多知识库检索费用倍增**：当一个应用挂载 N 个知识库并执行单次检索时，Query 向量化和 Rerank 排序的 Token 消耗量将 ×N，需谨慎评估挂载数量。
- **安全高级防护尚未正式计费**：截至 2026 年 9 月仍为限时免费，正式收费前将提前一个月通知，当前无需配置预算或预留额度 [计费说明 (raw/application-user-guide/agent-billing/billing.md)](../../raw/application-user-guide/agent-billing/billing.md)。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


