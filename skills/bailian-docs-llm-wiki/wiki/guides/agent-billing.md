# agent billing

Agent 计费覆盖 Managed Agents、Flow Agent（含智能体/工作流应用）、Sandbox、知识库、安全高级防护及 ParseX 等核心能力，采用按量付费为主、多维度独立计费的模式。各组件费用不互相抵扣，免费额度仅限指定计费项且严格按使用规则生效。实际费用以控制台账单为准，开发者需结合用量监控与成本优化策略进行精细化管理。

## 支持的模型/功能

- **Managed Agents**：支持会话运行时、模型调用（如 Qwen 系列）、工具/MCP 调用（如 `web_search`）、沙箱持久化四类计费项，其中模型调用费按实际 Token 消耗计费，不含在运行时费中 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。  
- **Flow Agent**：智能体应用计费来源为模型调用、知识库、MCP；工作流应用按执行路径上各**计费节点**（如大模型节点、图片解析节点）的实际调用量计费；文件上传、Prompt 自动优化、UI 设计器本身不计费 [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。  
- **Sandbox**：按运行时长（基础/进阶/旗舰款不同单价）和数据保留量（GiB·小时）计费，暂停或保存 Snapshot 均产生数据保留费 [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。  
- **知识库**：费用由**规格费用**（标准版 0.03 元/知识库/小时，旗舰版按 RCU 计费）和**模型调用费用**（向量、排序、路由、问答模型等独立计费）构成，二者不可混用免费额度 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **ParseX**：图文按页、音视频按秒计量，提供一次性免费额度（图文/字段抽取各 3,000 页，音视频各 100 小时），新文档直接抽取已含解析费用 [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)。  
- **Agent 安全高级防护**：限时免费中，正式计费后按“防御席位费 + 超额 Credits”组合计费，席位费 0.42 元/席位·小时，超额 Credit 单价 0.0015 元/Credit [计费说明](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：文档 5 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md` 的副本，以单一权威版本为准，避免引用歧义。

## 关键参数

| 参数 | 说明 | 示例值/范围 |
|------|------|-----------|
| `session_runtime_hour` | Managed Agents 会话运行时长，不足 1 小时按实际时长精确计算 | 0.5 小时 → 0.25 元（0.5 元/小时） |
| `token_input/output` | 模型调用费用核心参数，按千 Token 计费，价格依模型而异 | `qwen-plus`: Input 0.004 元/千 Token，Output 0.012 元/千 Token |
| `snapshot_hours` | 沙箱持久化按快照存在时长计费，不足 1 小时按 1 小时 | 3 天 = 72 小时 × 0.003 元 = 0.216 元 |
| `rcu` | 知识库旗舰版并发能力单位，1 RCU ≈ 50 QPS，规格费用 = RCU × 小时 × 0.2 元 | 2 RCU × 24h × 0.2 = 9.6 元 |
| `credits_per_session_per_day` | 安全高级防护默认额度，每个席位每日 300 Credits，24 小时有效期，不结转 | 超出 900 Credits（3 席位）后开始计费 |
| `pages/seconds` | ParseX 计量单位，图文按页、音视频按秒，复用解析结果可降低抽取单价 | 直接抽取新文档：¥0.06/页；复用解析结果：¥0.04/页 |

## 使用方式

- **用量查询**：统一通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看运行时长、Token、工具调用等明细；也可调用 `POST /usage/summary` 和 `POST /usage/trend` API 获取结构化数据 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。  
- **账单核对**：知识库规格费用在[账单详情](https://usercenter2.aliyun.com/finance/expense-report/expense-detail)中筛选“阿里云百炼知识库（RAG）- 后付费”；模型 Token 消耗需筛选“阿里云百炼大模型推理”，通过实例 ID 后缀（如 `...-embedding-...`）识别具体模型 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **免费额度抵扣**：系统自动按 **免费额度 > 资源包 > 按量付费** 顺序扣减，无需手动操作；但知识库免费额度仅适用于标准版，不抵扣旗舰版或模型调用费 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **成本优化**：知识库可通过关闭 Rerank、调低 TopK 参数减少排序 Token 消耗；Flow Agent 工作流中未进入执行路径的节点不计费；及时终止闲置 Managed Agents 会话可避免运行时费累积。

## 限制和注意事项

- **免费额度时效性**：Managed Agents 运行时免费额度为 10 小时，自生效日起 30 天内有效；知识库新用户免费额度仅 30 天，老用户统一截止至 2026 年 2 月 3 日；ParseX 一次性赠送，不按周期重置 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)、[知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)、[计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)。  
- **沙箱与快照释放逻辑**：Sandbox 暂停后数据保留计费；Managed Agents 沙箱持久化中，旧快照在新快照生成后才释放，因此快照保留时长可能跨多次运行 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。  
- **模型调用叠加风险**：知识库检索时，若挂载 N 个知识库，Query 向量化和 Rerank 排序的 Token 消耗量将 ×N；工作流中模型内置联网搜索同时产生模型调用费和搜索策略费 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)、[计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。  
- **服务依赖与额外成本**：选用自购 ADB-PG 作为知识库向量存储时，需单独支付 ADB-PG 费用；MCP 若调用第三方 API，其费用由第三方收取，百炼不参与计费 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)、[计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。  
- **安全防护开通前提**：高级防护需完成服务授权并创建多个 AliyunServiceRoleFor* 角色，开通即表示同意《百炼 Agent 安全（按量付费）服务协议》，默认开通 6 项策略，内容安全需手动启用 [计费说明](../../raw/application-user-guide/agent-billing/billing.md)。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


