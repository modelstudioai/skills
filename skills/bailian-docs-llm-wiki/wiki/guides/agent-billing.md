# agent billing

Agent 计费采用按需、分项、独立计费模式，费用来源于实际调用的模型、组件及运行资源，而非 Agent 抽象形态本身。各模块（如 Flow Agent、Managed Agents、Sandbox、知识库、ParseX、安全高级防护）均按自身使用量单独计量与计费，免费额度仅限抵扣其指定计费项。实际费用以控制台台账单为准，开发者需结合用量监控与账单明细进行成本管理。

## 支持的模型/功能

Agent 相关计费覆盖以下核心能力模块：

- **Flow Agent**：包含智能体应用与工作流应用两种形态。费用来自模型调用（含输入/输出 Token）、知识库（规格费 + 模型调用费）、MCP（如文生图、语音合成等，部分由第三方收费）、上下文缓存（自动生效，按所选模型规则计费）。文件上传、Prompt 自动优化、UI 设计器功能本身不计费，但其触发的模型调用、存储或数据库操作可能产生费用 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **Managed Agents**：计费项包括会话运行时费（0.5 元/小时）、模型调用费（按实际调用模型标准）、工具/MCP 调用费（如 `web_search` 0.03 元/次）、沙箱持久化费（0.003 元/个/小时）[计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **Sandbox**：按秒计量，分为会话运行费（基础款 0.156 元/小时、进阶款 0.312 元/小时、旗舰款 0.624 元/小时）和数据保留费（0.0021 元/GiB·小时）[计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **知识库（RAG）**：费用由两部分构成——规格费用（标准版 0.03 元/知识库/小时，旗舰版 0.2 元/RCU/小时）和模型调用费用（向量模型、排序模型、路由模型、问答模型等，按实际 Token 消耗计费）[知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **ParseX**：按处理量计量：图文按页、音视频按秒；提供一次性免费额度（图文/字段抽取各 3,000 页，音视频各 100 小时），超出后按量付费 [计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Agent 安全高级防护**：正式计费后按“防御席位费 + 超额 Credits”组合计费（席位费 0.42 元/席位·小时，超额 Credit 0.0015 元/Credit），当前处于限时免费阶段 [计费说明 (raw/application-user-guide/agent-billing/billing.md)](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：文档 5 和文档 7 内容完全重复，均为同一份关于 Agent 安全高级防护的计费说明，已合并引用。另需注意，文档 4 中明确指出知识库路由功能调用 `qwen-plus` 模型产生的费用属于模型调用费，而文档 1 中提及“智能模式下 AUTO 按统一刊例价计费”，二者在路由场景下的计费归属逻辑未明确对齐，建议以实际调用模型的 Token 计费为准。

## 关键参数

- **Token 计量**：模型调用（含大模型、向量模型、排序模型、路由模型）均按输入/输出 Token 数量计费，单位为“千 Token”。知识库检索中，排序费用取决于**初步召回总切片数 × 平均切片 Token 数**，而非最终返回数量。
- **RCU（Retrieval Compute Unit）**：知识库旗舰版并发能力单位，1 RCU ≈ 支撑 50 QPS；变配按时间分段计费。
- **席位（Seat）**：Managed Agents 与安全高级防护中，“席位”指一个处于运行中且启用对应能力的 Agent 实例，按小时计费。
- **Credit**：安全高级防护中用于度量检测内容量的抽象单位，每个席位每日默认 300 Credits，有效期 24 小时，不结转。
- **Snapshot / 快照**：Managed Agents 沙箱持久化与 Sandbox 数据保留均以快照为计费对象，按存在时长与占用资源（个数或 GiB）计费。
- **TopK 参数**：知识库检索中，“初步向量检索 TopK”和“初步关键词检索 TopK”直接影响排序模型 Token 消耗量，是关键成本调控参数。

## 使用方式

- **查看用量**：
  - Managed Agents：通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面或调用 [Usage API](../../raw/application-api-reference/managed-agents-api/usage-api.md)（`POST /usage/summary` 或 `/usage/trend`）获取运行时长、Token、工具调用等明细。
  - 知识库：在账单详情页筛选产品为“大模型服务平台阿里云百炼”，商品为“阿里云百炼知识库（RAG）- 后付费”查规格费；筛选商品为“阿里云百炼大模型推理”并查看实例 ID 前缀（如 `...-embedding-...` 或 `...-rerank-...`）查模型调用费。
  - ParseX：通过 [任务记录](../../raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/tasks.md) 和 [用量](../../raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/usage.md) 页面核对处理量。
- **成本优化**：
  - 知识库：关闭重排策略、降低 TopK 值、复用解析结果、选用资源包或节省计划（AI 通用型节省计划可抵扣向量/排序模型费用）。
  - Flow Agent：避免在非必要路径配置计费节点（如联网搜索、Qwen-VL 图片解析）；合理设置知识库召回参数。
  - Managed Agents：及时终止空闲会话以减少运行时费；评估是否开启沙箱持久化。
- **开通与授权**：安全高级防护需在控制台 Security > 高级防护 > 安全策略中完成服务授权，系统将自动创建关联角色（如 `AliyunServiceRoleForSFMSecurity`）。

## 限制和注意事项

- **免费额度不可跨项抵扣**：模型调用免费额度仅抵扣模型费用，知识库免费额度（720 小时）仅抵扣标准版规格费，ParseX 免费额度仅限对应解析/抽取能力，三者互不通用。
- **计费起点明确**：知识库自创建成功起计费；Sandbox 自启动运行起按秒计费；Managed Agents 会话自启用（运行中）状态起计费；安全高级防护席位费仅在 Agent 运行且启用该能力时产生。
- **删除 ≠ 立即停费**：知识库删除后数据永久清除且停止计费；Sandbox 删除后快照若已生成仍按保留时长计费至释放；Managed Agents 会话终止后快照保留期间仍产生沙箱持久化费。
- **多知识库放大效应**：应用挂载 N 个知识库时，Query 向量化与 Rerank 排序的 Token 消耗量按 N 倍增加，需谨慎评估必要性。
- **价格时效性**：所有单价均以文档发布时点为准，实际价格以控制台最新公示及账单为准；资源包、节省计划等优惠策略需主动购买并配置生效。
- **第三方费用隔离**：部分 MCP（如调用外部 API 的工具）费用由第三方收取，阿里云百炼不参与计费。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


