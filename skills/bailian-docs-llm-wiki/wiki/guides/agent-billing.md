# agent billing

Agent 计费采用多维度、按需付费模式，费用由运行时资源、模型调用、工具/MCP 服务、知识库、解析组件及安全防护等独立计费项构成。各组件遵循“谁使用、谁付费”原则，免费额度仅限抵扣指定计费项，不跨类型通用。实际费用以控制台账单为准，开发者需结合用量监控与配置优化主动控本。

## 支持的模型/功能

Agent 相关计费覆盖以下核心能力模块：

- **Managed Agents**：提供会话运行时费（0.5 元/小时）、模型调用费（按所选模型 Token 实际消耗）、工具及 MCP 调用费（如 `web_search` 0.03 元/次）[计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **Flow Agent**（含智能体应用与工作流应用）：编排本身不收费，费用源自实际执行的模型节点、知识库、MCP 及内置解析能力；智能模式下 AUTO 路由按统一刊例价计费，非 AUTO 模式按所选性能档位计费 [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)  
- **Sandbox**：按秒计量，分“会话运行费”（基础/进阶/旗舰款分别为 0.156/0.312/0.624 元/小时）与“数据保留费”（0.0021 元/GiB·小时）[计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)  
- **知识库（RAG）**：规格费用（标准版 0.03 元/库/小时，旗舰版 0.2 元/RCU/小时）与模型调用费用（向量、排序、路由、问答模型均独立计费）分离，且支持资源包与免费额度抵扣 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
- **ParseX**：图文按页、音视频按秒计量；提供一次性免费额度（图文/字段抽取各 3,000 页，音视频各 100 小时），超出后按量计费 [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)  
- **Agent 安全高级防护**：限时免费中，正式计费后按“防御席位费（0.42 元/席位·小时）+ 超额 Credits（0.0015 元/Credit）”组合计费，Credit 按自然日清零、不可结转 [计费说明](../../raw/application-user-guide/agent-billing/billing.md)  

> **注意**：文档 5 与文档 7 内容完全重复，均为同一份 Agent 安全高级防护计费说明，以最新版本为准（二者无实质差异，无需版本仲裁）。

## 关键参数

| 参数 | 说明 | 示例/取值范围 |
|------|------|----------------|
| `session_runtime_hours` | Managed Agents / Sandbox 运行时长，精确到秒，不足 1 小时按比例计费 | 0.15 小时（9 分钟） |
| `input_tokens`, `output_tokens` | 模型调用（含 LLM、Embedding、Rerank、Routing）的输入/输出 Token 数，按千 Token 计费 | `text-embedding-v4`: 0.0005 元/千 Token |
| `rcu` | 知识库旗舰版并发能力单位，1 RCU ≈ 支撑 50 QPS；变配按小时分段计费 | 1–200 RCU，需向上取整估算 |
| `topk_vector` / `topk_keyword` | 知识库检索中初步召回切片数，直接影响 Rerank 模型 Token 消耗量 | 默认各 50，可调至 10–100 |
| `snapshot_size_gb` | Sandbox Snapshot 或暂停状态数据占用 GiB 数，用于计算数据保留费 | 实际平台统计值，非声明值 |
| `credit_consumption` | 安全高级防护中按内容 Token 换算的 Credit 消耗量，每日重置 | 每席位默认 300 Credits/天 |

## 使用方式

- **用量查询**：统一通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看运行时长、Token、工具调用、知识库规格、ParseX 页数等明细；也可调用 `POST /usage/summary` 和 `POST /usage/trend` API 获取结构化数据 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **账单核对**：在 [账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail) 导出按小时聚合的明细，通过实例 ID 前缀（如 `llm-xxx;xxx-embedding-xxx`）识别模型类型，通过商品名称筛选“阿里云百炼知识库（RAG）- 后付费”或“阿里云百炼大模型推理”定位费用归属 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
- **免费额度管理**：知识库免费额度（720 小时）与 ParseX 免费额度（一次性）均在开通时自动发放，额度余量可在对应服务页面直接查看；额度按实际用量实时扣减，不支持手动分配 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
- **成本优化操作**：关闭知识库重排策略、降低 `topk_vector`/`topk_keyword`、停用未使用的 Managed Agent 会话、删除闲置知识库、及时清理 Sandbox Snapshot，均可显著降低对应计费项 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  

## 限制和注意事项

- **运行时费触发条件**：Managed Agents 与 Sandbox 的运行时费仅在“实际运行中”产生，空闲/暂停状态不计费；但 Sandbox 暂停后仍产生数据保留费 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **免费额度不可叠加与转移**：10 小时 Managed Agents 运行时免费额度仅抵扣运行时费，不抵扣模型或工具费；知识库免费额度仅适用于标准版，不适用于旗舰版；所有免费额度均不跨账号、不跨服务、不结转 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **模型调用费双重叠加风险**：当 Flow Agent 应用挂载 N 个知识库时，Query 向量化与 Rerank 排序费用将 ×N；同理，知识库路由调用 `qwen-plus` 也会在多库场景下重复发生 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
- **安全防护计费隔离性**：Agent 安全高级防护的 Credit 额度严格按席位隔离，3 个 Agent 各享 300 Credits/天，不可共享或调剂；且 Credit 仅用于安全检测，不参与任何其他计费项抵扣 [计费说明](../../raw/application-user-guide/agent-billing/billing.md)  
- **资源包有效期硬约束**：知识库资源包（标准版/旗舰版）购买后一年内有效，过期未用完部分自动作废；退订仅支持未使用额度退款，已消耗部分不可退 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


