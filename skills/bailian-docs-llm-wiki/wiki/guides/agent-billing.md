# agent billing

Agent 相关计费覆盖 Managed Agents、Flow Agent（智能体/工作流应用）、Sandbox、记忆库、知识库、ParseX 及安全高级防护等多个组件，各组件独立计费、额度不互通。费用主要由运行时长、模型 Token 消耗、工具/MCP 调用、数据存储与处理量等维度构成，所有计费均按实际用量精确计量（支持秒级或小时级出账），最终以控制台账单为准。开发者需结合具体使用形态（如是否开启沙箱持久化、是否启用 Rerank、是否复用解析结果等）精细化评估成本。

## 支持的模型/功能

- **Managed Agents**：支持 Qwen 系列等大模型调用（按 Input/Output Token 计费）、内置工具（如 `web_search` ¥0.03/次）、MCP 服务及沙箱持久化快照（¥0.003/个/小时）[原文标题](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **Flow Agent**：智能体应用计费来源包括模型调用、知识库、MCP；工作流应用按执行路径上各**计费节点**（如大模型节点、图片解析节点）分别计费；文件上传、Prompt 自动优化、UI 设计器本身不计费 [原文标题](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)  
- **Sandbox**：提供基础款（¥0.156/小时）、进阶款（¥0.312/小时）、旗舰款（¥0.624/小时）三档运行时费，以及数据保留费（¥0.0021/GiB·小时）[原文标题](../../raw/application-user-guide/agent-billing/sandbox-billing.md)  
- **记忆库**：按写入（Add）、检索（Search）、存储三类计费，区分 Pro/Lite 策略版本（Rerank 开启与否影响单价与质量）[原文标题](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)  
- **知识库**：规格费用（标准版 ¥0.03/库/小时，旗舰版 ¥0.2/RCU/小时）与模型调用费用（向量、排序、路由、问答模型）完全分离；多个知识库并行检索时，Token 消耗量按知识库数量倍增 [原文标题](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
- **ParseX**：图文按页（¥0.02/页）、音视频按秒（音频 ¥0.00035/秒，视频 ¥0.002/秒）计量；字段抽取分“新文档直接抽取”（¥0.06/页，含解析）和“复用解析结果抽取”（¥0.04/页）两种计价模式 [原文标题](../../raw/application-user-guide/agent-billing/pricing.md)  
- **安全高级防护**：防御席位费（¥0.42/席位·小时） + 超额 Credits（¥0.0015/Credit），默认额度为 300 Credits/席位/日，过期不结转  

> **注意**：文档 2 中称“智能模式各档位的缓存费用见[智能模式计费明细](https://help.aliyun.com/zh/model-studio/new-single-agent-application#66b7273195ors)”，但该外部链接未在原始文档集中提供，且文档 1、6 均未提及缓存费用对 Managed Agents 或知识库的适用性；实际开发中应以控制台实时价格及对应模型的 [选择模型](../../raw/model-user-guide/get-started-with-models/models.md) 文档为准。

## 关键参数

| 参数 | 说明 | 示例值/范围 |
|------|------|-----------|
| `plan_version`（记忆库） | 控制 Add/Search 的策略版本（Pro/Lite），Pro 含 Rerank，Lite 不含 | Add 默认 Pro；Search 请求可显式传 `plan_version=Lite` |
| `top_k`（知识库） | 初步向量/关键词检索 TopK，默认各 50；直接影响 Rerank 阶段 Token 消耗量 | 调整为 10–100，降低可显著节省排序费用 |
| `rcu`（知识库旗舰版） | 检索计算单元，1 RCU ≈ 50 QPS；变配按小时分段计费 | 80 QPS 需至少 2 RCU |
| `snapshot_retention_hours`（Managed Agents） | 沙箱快照保留时长，按存在小时数计费（不足 1 小时按 1 小时） | 快照保留 72 小时 → 72 × ¥0.003 = ¥0.216 |
| `credits_used`（安全高级防护） | 按被检测内容 Token 量换算，每个席位每日 300 Credits 免费 | 10,000 Credits 总消耗 → 超额 9,700 × ¥0.0015 = ¥14.55 |

## 使用方式

- **查看用量**：统一通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看运行时长、Token、工具调用等明细；也可调用 `POST /usage/summary` 和 `POST /usage/trend` API 获取结构化数据 [原文标题](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **开通服务**：知识库、记忆库、安全高级防护等需主动开通；Sandbox、Managed Agents 创建即启用计费；Flow Agent 编排本身免费，仅所依赖组件计费  
- **配置优化**：  
  - 知识库：关闭 Rerank、调低 `top_k`、复用解析结果可降低模型费用  
  - 记忆库：检索时显式指定 `plan_version=Lite` 适用于高频低成本场景  
  - Sandbox：暂停后及时删除无用 Snapshot 可避免数据保留费累积  
- **额度管理**：免费额度自动抵扣（顺序：免费额度 > 资源包 > 按量付费）；资源包需在控制台购买并关注有效期与预警阈值  

## 限制和注意事项

- **额度隔离**：各组件免费额度**不可跨类型抵扣**（如知识库免费时长不能抵扣模型 Token 费，记忆库额度不能抵扣 ParseX 页数）  
- **计费起点**：Managed Agents 自 2026-08-17 09:00（UTC+8）起计费；知识库自 2026-01-04 起计费；记忆库自 2026-08-20 10:00（北京时间）起计费；安全高级防护当前限时免费，正式收费前将提前通知  
- **运行状态定义**：会话/Agent/Sandbox 处于“运行中”状态即开始计费（空闲不计费）；知识库创建成功即开始计时；记忆库写入/检索调用即触发计费  
- **模型费用叠加**：知识库多库并行检索、智能体应用挂载多个知识库、记忆检索注入 Prompt 等场景，均会导致模型 Token 消耗量成倍增加，需特别关注  
- **删除即停计费**：删除知识库、终止 Managed Agents 会话、销毁 Sandbox 实例后，对应规格费用立即停止；但已生成的快照、已写入的记忆、已解析的文档仍可能产生后续费用（如快照保留、记忆存储、解析结果复用）  
- **账单核对**：规格费用在账单中归类为“阿里云百炼知识库（RAG）- 后付费”等商品名；模型 Token 费用统一归类为“阿里云百炼大模型推理”，需通过实例 ID 后缀（如 `...-embedding-...`）识别具体模型类型 [原文标题](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)


