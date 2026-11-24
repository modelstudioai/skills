# agent billing

Agent 计费采用多维度、按需付费模式，费用由运行时资源、模型调用、组件服务（如知识库、记忆库、ParseX）及安全防护等独立计费项构成。各模块按实际用量精确计量（小时、[Token](../concepts/token.md)、次、页、秒等），支持免费额度抵扣、资源包预购和节省计划优化。开发者需结合具体 Agent 类型（Sandbox、Managed Agents、Flow Agent）和所用能力组合，分项核算成本。

## 支持的模型/功能

Agent 计费覆盖以下核心能力模块，均按实际调用独立计费：

- **Sandbox 运行与数据保留**：按款型（基础/进阶/旗舰）收取会话运行费（0.156–0.624 元/小时），以及暂停或 Snapshot 产生的数据保留费（0.0021 元/GiB·小时）[计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **Managed Agents**：包含会话运行时费（0.5 元/小时）、模型调用费（按所选模型 [Token](../concepts/token.md) 计费）、工具/MCP 调用费（如 `web_search` 0.03 元/次）及沙箱持久化费（0.003 元/个/小时）[计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **Flow Agent**：编排本身不收费，费用来自下游调用的模型、知识库、MCP、记忆库及 ParseX 等组件，各组件按自身标准计费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **知识库（RAG）**：规格费用（标准版 0.03 元/库/小时，旗舰版 0.2 元/RCU/小时） + 模型调用费用（向量、排序、路由、问答模型按 [Token](../concepts/token.md) 计费）[知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **记忆库**：按写入（Add）、检索（Search）次数及存储时长（0.002 元/万条/小时）计费，Pro/Lite 版本影响单价与 Rerank 能力 [计费说明 (raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)。
- **ParseX**：图文按页（¥0.02/页）、音视频按秒（¥0.002/秒视频，¥0.00035/秒音频）、字段抽取分场景计价（新文档 ¥0.06/页，复用解析结果 ¥0.04/页）[计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Agent 安全高级防护**：防御席位费（0.42 元/席位·小时） + 超额 Credits（0.0015 元/Credit），默认防护免费 [计费说明 (raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)。

> **注意**：文档 2 与文档 1 对“沙箱”计费口径存在差异——文档 1 中 Sandbox 是独立运行环境（含系统盘），而文档 2 的“沙箱持久化”特指 Managed Agents 启用快照功能后的附加费用，二者属不同产品形态，不可混用单价。开发者应严格依据所用 Agent 类型选择对应计费文档。

## 关键参数

- **运行时长**：以秒为粒度计量，不足 1 小时按实际时长折算（如 40 分钟 = 2/3 小时）。Sandbox 和 Managed Agents 均按此规则，但计费对象不同（前者为 Sandbox 实例，后者为会话 Session）。
- **Token 计量**：模型调用费用统一按输入/输出 Token 数量计算，单位为“千 Token”。知识库向量化、Rerank、问答生成等环节均独立计量；检索阶段费用取决于**初步召回切片总数 × 平均切片 Token 数**，而非最终返回数量。
- **RCU（Retrieval Compute Unit）**：知识库旗舰版并发能力单位，1 RCU ≈ 支撑 50 QPS；变配后按小时分段计费。
- **Credit**：Agent 安全高级防护计量单位，每个席位每日默认 300 Credits，有效期 24 小时，不结转。
- **页/秒计量**：ParseX 中图文按处理页数、音视频按处理秒数计量；文本类文件按文本量/2000 折算为页。

## 使用方式

- **查看用量**：通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看 Managed Agents 的运行时长、Token、工具调用明细；知识库用量在账单详情中按“实例 ID”筛选；ParseX 用量见 [任务记录](../../raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/tasks.md) 和 [用量](../../raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/usage.md)。
- **调用 API**：使用 [Usage API](../../raw/application-api-reference/managed-agents-api/usage-api.md)（`POST /usage/summary` 和 `POST /usage/trend`）获取工作空间、Agent 或 Session 级别的用量汇总与趋势。
- **配置优化**：知识库可通过关闭 Rerank、降低 TopK 值减少排序模型费用；Managed Agents 应及时终止空闲会话以避免运行时费；记忆库可按场景选用 Lite 版本降低检索成本。
- **额度管理**：免费额度按“先到先得”顺序抵扣（免费额度 > 资源包 > 按量付费）；知识库资源包、AI 节省计划等需在控制台单独购买并绑定。

## 限制和注意事项

- **计费起点明确**：Sandbox 自创建即开始计费；知识库自成功创建起计费；记忆库自商业化生效日（2026-08-20）起计费；ParseX 自首次开通起赠送一次性额度。
- **删除即停费**：删除知识库、Sandbox 或 Agent 会立即停止对应规格费用，但已产生的模型调用、Credits 消耗等仍计入当期账单。
- **额度不通用**：各组件免费额度仅抵扣其指定计费项（如知识库额度不抵扣模型费，记忆库额度不抵扣 Search Pro 费用），且不可跨账号、跨工作空间共享。
- **模型费用叠加风险**：挂载多个知识库时，Query 向量化与 Rerank 费用按知识库数量线性倍增；智能体应用中记忆检索内容注入 Prompt 后，将额外产生大模型 Token 费用。
- **版本兼容性**：记忆库 Pro/Lite 版本由 `plan_version` 参数控制，Add 与 Search 的版本可独立设置；未传参时默认 Pro，需显式指定 Lite 以降低成本。
- **安全防护时效性**：Agent 安全高级防护当前限时免费，正式计费前将提前一个月通知；开通需完成服务角色授权，且默认策略需手动启用。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)


