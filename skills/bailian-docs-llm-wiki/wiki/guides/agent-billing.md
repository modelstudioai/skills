# agent billing

Agent 计费采用多维度、按需计费模式，费用由运行时资源、模型调用、工具/MCP 服务、知识库、解析组件及安全防护等独立计费项构成。各组件价格与免费额度相互隔离，不跨项抵扣；实际费用以控制台账单为准，支持按小时出账与分段计费。开发者需根据应用形态（Managed Agents / Flow Agent / Sandbox）和启用能力（如高级防护、知识库路由、Rerank 排序等）主动评估成本。

## 支持的模型/功能

Agent 相关计费覆盖以下核心能力模块：

- **Managed Agents**：按会话运行时长（0.5 元/小时）、所调用大模型 [Token](../concepts/token.md)（如 `qwen-plus` 输入 0.004 元/千 [Token](../concepts/token.md)）、工具/MCP 调用（如 `web_search` 0.03 元/次）三类独立计费 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **Flow Agent（智能体/工作流应用）**：编排本身不收费，费用来自实际执行的模型调用、知识库、MCP 及联网搜索等节点；其中知识库召回文本切片会增加模型输入 [Token](../concepts/token.md)，间接推高模型调用费 [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **Sandbox**：按秒计量，分为会话运行费（基础款 0.156 元/小时）与数据保留费（0.0021 元/GiB·小时），暂停或 Snapshot 均产生保留费用 [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **知识库（RAG）**：规格费用（标准版 0.03 元/知识库/小时，旗舰版按 RCU 计费）与模型调用费用（向量、排序、路由、问答模型）分离；排序费用取决于**初步召回总切片数**，而非最终返回数量 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **ParseX 解析服务**：图文按页（¥0.02/页）、音视频按秒（音频 ¥0.00035/秒，视频 ¥0.002/秒）计量；字段抽取分“新文档直接抽取”（¥0.06/页）与“复用解析结果抽取”（¥0.04/页）两种计价 [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Agent 安全高级防护**：限时免费中，正式计费后按“防御席位费（0.42 元/席位·小时）+ 超额 Credits（0.0015 元/Credit）”组合计费；每个席位每日默认 300 Credits，额度不结转、不共享 [计费说明](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：文档 4 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md` 的副本，以该路径最新版本为准；文档 2 中提及“智能模式各档位的缓存费用见[智能模式计费明细](https://help.aliyun.com/zh/model-studio/new-single-agent-application#66b7273195ors)”为外部链接，非百炼平台内原始文档，未纳入本 Wiki 引用范围。

## 关键参数

| 参数 | 说明 | 影响范围 |
|------|------|----------|
| `会话运行时长` | Managed Agents/Sandbox 按实际启用时间计费，空闲状态不计费；Sandbox 暂停后仍产生数据保留费 | 运行时费、数据保留费 |
| `RCU（Retrieval Compute Unit）` | 知识库旗舰版并发能力单位，1 RCU ≈ 支撑 50 QPS；变配按发生时间分段计费 | 知识库规格费用 |
| `初步召回 TopK` | 知识库检索中“向量检索 TopK”与“关键词检索 TopK”之和，决定送入 Rerank 模型的切片总数 | Rerank 模型费用（主要成本项） |
| `Credit` | 安全高级防护中内容检测消耗单位，按 Token 换算；每个席位每日 300 Credits，超限部分按 0.0015 元/Credit 计费 | 超额 Credits 用量 |
| `嵌套调用深度` | Flow Agent 工作流中，若模型节点输出触发下游多个 MCP 或知识库调用，费用叠加计算 | 总费用 = 各执行路径节点费用之和 |

## 使用方式

- **开通与配置**：  
  - Managed Agents、Sandbox、知识库、ParseX 均在控制台对应页面开通，默认启用后付费；知识库可购买资源包（如[标准版资源包](https://common-buy.aliyun.com/?commodityCode=sfm_ragservicestandard_dp_cn)）实现预付费抵扣。  
  - Agent 安全高级防护需在 **Security > 高级防护 > 安全策略** 页面手动开通并授权服务角色 [计费说明](../../raw/application-user-guide/agent-billing/billing.md)。  

- **费用控制操作**：  
  - 终止闲置会话、删除不再使用的知识库或 Sandbox，立即停止对应运行时/规格费用。  
  - 知识库检索阶段可关闭 Rerank 排序或降低 TopK 值以显著降低成本；智能体应用中可禁用知识库路由减少 `qwen-plus` 调用。  
  - ParseX 复用已有解析结果进行字段抽取，单价更低（¥0.04/页 vs ¥0.06/页）。  

- **账单查询**：  
  - 所有费用统一归集至「大模型服务平台阿里云百炼」产品下，按小时聚合出账。  
  - 知识库规格费用查账单中商品名为「阿里云百炼知识库（RAG）- 后付费」；模型 Token 消耗查「阿里云百炼大模型推理」，实例 ID 含 `embedding` 或 `rerank` 可区分用途 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  

## 限制和注意事项

- **免费额度不可跨项、跨资源类型使用**：Managed Agents 的 10 小时运行时免费额度仅抵扣运行时费，不抵扣模型或工具费；知识库 720 小时免费额度仅适用于标准版规格费用，且老用户有效期截至 2026-02-03 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **模型调用费用始终独立于宿主服务**：无论通过 Managed Agents、Flow Agent 还是 Sandbox 调用 `qwen-plus`，均按统一 Token 价格计费；知识库路由、Rerank、问答生成等场景产生的 Token 消耗均计入模型账单，不包含在知识库规格费中。  
- **Sandbox 数据保留费易被忽略**：暂停 Sandbox 或保存 Snapshot 后，即使未运行，只要数据占用磁盘空间，即按 GiB·小时持续计费；系统盘 15 GiB 免费，超出部分及快照均计费 [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。  
- **高级防护 Credit 按自然日重置**：每个席位 Credit 有效期严格为 24 小时（00:00–23:59），不结转；多 Agent 场景下额度不共享，需按席位分别监控 [计费说明](../../raw/application-user-guide/agent-billing/billing.md)。  
- **知识库多实例调用放大效应**：同一 Query 在挂载的 N 个知识库中默认各执行一次完整检索（含向量化 + Rerank），Token 消耗量线性增长；无法通过配置关闭单库检索 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


