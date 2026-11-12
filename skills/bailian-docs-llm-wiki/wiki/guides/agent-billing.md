# agent billing

Agent 计费采用多维度、按需计量的模式，费用由运行时资源、模型调用、工具/MCP 服务、知识库、解析服务及安全防护等独立计费项组成。各组件遵循“谁使用、谁付费”原则，免费额度仅限抵扣其指定计费项，不跨类型通用。实际费用以控制台账单为准，开发者需结合用量监控与成本优化策略进行精细化管理。

## 支持的模型/功能

Agent 相关计费覆盖以下核心能力模块：

- **Managed Agents**：提供会话运行时费（0.5 元/小时）、模型调用费（按所选模型 [Token](../concepts/token.md) 实际消耗计费）、工具及 MCP 调用费（如 `web_search` 0.03 元/次）[计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **Sandbox**：按款型区分计费（基础款 0.156 元/小时，进阶款 0.312 元/小时，旗舰款 0.624 元/小时），另收取数据保留费（0.0021 元/GiB·小时）[计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)  
- **Flow Agent（智能体/工作流应用）**：编排本身不收费，费用源自实际执行的模型调用、知识库、MCP、图片/文档解析等节点；工作流按执行路径上各计费节点累加 [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)  
- **知识库（RAG）**：规格费用（标准版 0.03 元/知识库/小时，旗舰版 0.2 元/RCU/小时） + 模型调用费用（向量、排序、路由、问答模型均按 [Token](../concepts/token.md) 单独计费）[知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
- **ParseX 解析服务**：图文按页（¥0.02/页）、音视频按秒（音频 ¥0.00035/秒，视频 ¥0.002/秒）、字段抽取分场景定价（新文档直接抽取 ¥0.06/页，复用解析结果 ¥0.04/页）[计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)  
- **Agent 安全高级防护**：防御席位费（0.42 元/席位·小时） + 超额 Credits（0.0015 元/Credit），当前处于限时免费阶段，正式计费前将提前通知 [计费说明](../../raw/application-user-guide/agent-billing/billing.md)  

> **注意**：文档 6 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md` 的副本，以该路径唯一文档为准，避免引用歧义。

## 关键参数

| 参数 | 说明 | 示例值/范围 |
|--------|------|-------------|
| `session_runtime_hours` | Managed Agents 运行中会话时长（精确到秒，不足 1 小时按比例计费） | `5.25` 小时 → `5.25 × 0.5 = 2.625` 元 |
| `rcu_count` | 知识库旗舰版并发能力单位，1 RCU ≈ 支撑 50 QPS；变配后分段计费 | `2 RCU` → `0.2 × 2 = 0.4` 元/小时 |
| `topk_vector` / `topk_keyword` | 知识库检索参数，直接影响 Rerank 模型 [Token](../concepts/token.md) 消耗量（费用 ∝ 初步召回总切片数 × 平均切片 Token 数） | 默认 `50`，可调至 `10–100` |
| `credit_quota_per_seat_per_day` | 安全高级防护默认额度，按席位隔离、24 小时清零 | `300 Credits/席位/日` |
| `parse_unit` | ParseX 计量单位：图文按页、音视频按秒；文本容器按 2000 字符折算为 1 页 | `100 页 PDF` → `100 × ¥0.02` |

## 使用方式

- **查看用量**：统一入口为控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面，支持按工作空间、Agent 或 Session 维度查看运行时长、Token、工具调用等明细；也可调用 `POST /usage/summary` 和 `POST /usage/trend` API 获取结构化数据 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **开通服务**：知识库、Sandbox、安全高级防护等需显式开通；开通即开始计费（知识库从创建起计费，Sandbox 从启动起计费，安全防护从启用高级策略起计费）  
- **配置优化**：  
  - 知识库：关闭 Rerank、降低 `topk_vector`/`topk_keyword` 可显著减少模型费用 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
  - Flow Agent：避免在非必要路径配置计费节点（如禁用未使用的联网搜索、图片解析）  
  - Sandbox：及时暂停或删除闲置实例以规避运行费与数据保留费叠加  

## 限制和注意事项

- **免费额度不可跨类抵扣**：Managed Agents 的 10 小时运行时免费额度仅抵扣运行时费，不覆盖模型或工具费用；知识库 720 小时免费额度仅适用于标准版规格费，不适用于旗舰版或任何模型调用 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **模型调用费用双重叠加风险**：  
  - 知识库挂载多个实例时，Query 向量化与 Rerank 费用按知识库数量线性放大（N 个知识库 → N 倍 Token 消耗）  
  - 工作流中若同一模型节点被多路径触发，费用按实际执行次数累加  
- **计费粒度与时效性**：  
  - Sandbox 按秒计量，知识库规格费用按小时出账，模型 Token 费用按千 Token 结算，安全 Credits 按自然日清零  
  - 所有费用以控制台账单为准，API 返回的用量数据可能存在数分钟延迟  
- **资源释放不等于费用终止**：  
  - 删除知识库立即停止规格费用，但已产生的模型调用费用仍计入当期账单  
  - Sandbox 暂停后仍产生数据保留费，需彻底删除或清理 Snapshot 才能终止该费用  
- **第三方依赖费用**：部分 MCP（如调用外部 API 的工具）费用由第三方收取，阿里云百炼不参与计费 [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


