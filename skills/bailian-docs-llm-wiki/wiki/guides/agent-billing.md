# agent billing

Agent 计费采用多维度、按需付费模式，费用由运行时资源、模型调用、组件服务（如知识库、ParseX、Sandbox）及安全防护等独立计费项构成。所有费用均以控制台账单为准，支持免费额度抵扣、资源包预购和节省计划优化。开发者需根据实际使用路径（如会话运行、知识检索、工作流执行）分别核算成本。

## 支持的模型/功能

Agent 相关计费覆盖以下核心能力模块：

- **Managed Agents**：按会话运行时长（0.5 元/小时）+ 模型 [Token](../concepts/token.md) 调用 + 工具/MCP 调用三部分独立计费，空闲状态不计运行时费 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **Flow Agent（智能体/工作流应用）**：编排本身不收费，费用源自实际执行的模型节点、知识库、MCP、联网搜索等组件；工作流按执行路径上各计费节点累加费用 [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)  
- **知识库（RAG）**：含规格费用（标准版 0.03 元/库/小时，旗舰版 0.2 元/RCU/小时）与模型调用费用（向量、排序、路由、问答模型 [Token](../concepts/token.md) 计费），二者完全分离 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
- **Sandbox**：按秒计量，分“会话运行费”（基础/进阶/旗舰款：0.156–0.624 元/小时）和“数据保留费”（0.0021 元/GiB·小时） [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)  
- **ParseX**：图文按页、音视频按秒计量，支持一次性免费额度（图文/字段抽取各 3,000 页，音视频各 100 小时） [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)  
- **Agent 安全高级防护**：限时免费中；正式计费后按“防御席位费（0.42 元/席位·小时）+ 超额 Credits（0.0015 元/Credit）”组合计费 [计费说明](../../raw/application-user-guide/agent-billing/billing.md)  

> **注意**：文档 6 和文档 7 内容完全重复，为同一份 `billing.md` 的重复收录，以首次出现为准，无需额外处理。

## 关键参数

| 参数 | 说明 | 示例值/范围 |
|------|------|-----------|
| `会话运行时长` | Managed Agents / Sandbox 的计费基础，精确到秒，不足 1 小时按比例折算 | 0.15 小时 = 9 分钟 |
| `Token 数量` | 模型调用（含大模型、向量、排序、路由模型）的核心计量单位，按输入/输出分别计费 | `text-embedding-v4`: 0.0005 元/千 [Token](../concepts/token.md) |
| `RCU（Retrieval Compute Unit）` | 知识库旗舰版并发能力单位，1 RCU ≈ 50 QPS；变配按小时分段计费 | 2 RCU 支撑最高 100 QPS |
| `初步召回 TopK` | 知识库检索中影响排序费用的关键参数，费用与初步召回总切片数 × 平均切片 Token 数正相关 | 向量 TopK=50 + 关键词 TopK=50 → 最多 100 切片送入 Rerank |
| `Credit` | Agent 安全高级防护的检测额度单位，每个席位每日默认 300 Credits，24 小时过期不结转 | 10,000 Credits 消耗 → 超额 9,100 Credits 计费 |

## 使用方式

- **开通即用，自动计费**：除高级防护需手动授权外，Managed Agents、Flow Agent、知识库、Sandbox、ParseX 均在创建/启用后立即开始计量，无需额外开通计费开关。  
- **免费额度自动抵扣**：所有免费额度均按“免费额度 > 资源包 > 按量付费”顺序优先抵扣，且仅限指定计费项（如知识库免费额度仅抵扣标准版规格费，不抵扣模型调用费）。  
- **资源包与节省计划叠加**：知识库可购买标准版/旗舰版资源包；向量及排序模型调用支持 AI 通用型节省计划抵扣（仅限模型费用，不抵扣规格费） [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **账单明细可追溯**：通过[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)页面，按小时粒度导出账单，结合实例 ID 前缀（如 `llm-xxx;xxx-rerank;...`）精准定位模型调用来源。  

## 限制和注意事项

- **会话与席位状态强耦合**：Managed Agents 的运行时费、Sandbox 的会话运行费、安全高级防护的席位费，均**仅在 Agent/Sandbox 实际处于“运行中”且启用对应能力时产生**；暂停、停止、空闲状态不计费。及时终止闲置资源是成本控制关键。  
- **知识库多库调用费用倍增**：当一个智能体应用挂载 N 个知识库并执行检索时，Query 向量化和 Rerank 排序的 Token 消耗量将按 N 倍增加，此行为不可关闭或配置跳过 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **Rerank 费用取决于初步召回量，而非最终返回量**：即使将“最终召回数量”设为 5，只要初步召回了 150 个切片，Rerank 模型即对全部 150 个切片计费。关闭重排策略或降低 TopK 是主要优化手段。  
- **模型调用费与应用形态无关**：无论通过 Managed Agents、Flow Agent 还是 API 直接调用，同一模型（如 `qwen-plus`）的 Token 计费单价一致，遵循模型广场刊例价。  
- **文件上传本身免费，但后续处理均计费**：文件问答中的上传操作不收费；但基于该文件的解析（ParseX）、向量化（知识库）、问答生成（模型）均独立计费 [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


