# agent billing

Agent 相关服务的计费采用多维度、按需付费模式，费用由运行时长、模型调用、工具/MCP 调用、数据存储与安全防护等独立计费项构成。各组件遵循“谁使用、谁付费”原则，免费额度仅限抵扣其指定计费项，不跨项目通用。实际费用以控制台账单为准，所有计费均支持按小时出账与用量明细查询。

## 支持的模型/功能

Agent 生态中涉及计费的核心能力包括：

- **Managed Agents**：提供会话运行时、模型调用、工具/MCP 调用及沙箱持久化四类计费项，其中模型调用费严格按所选模型（如 `qwen-plus`）的 Token 实际消耗计费 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **Flow Agent**（含智能体应用与工作流应用）：编排逻辑本身不收费，费用源自下游调用的模型、知识库、MCP 及解析节点；例如工作流中图片解析节点若选用 Qwen-VL，则产生对应模型调用费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **Sandbox**：按运行款型（基础/进阶/旗舰）收取会话运行费，并对暂停或 Snapshot 占用的磁盘空间按 GiB·小时计收数据保留费 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **知识库（RAG）**：费用由规格费（标准版 0.03 元/库/小时，旗舰版 0.2 元/RCU/小时）与模型调用费（向量、排序、路由、问答模型）两部分组成，后者按实际 Token 消耗独立计费 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **记忆库（Memory Library）**：按写入（Add）、检索（Search）和存储三类操作计费，Pro/Lite 版本区分是否启用 Rerank，影响单价与质量 [计费说明 (raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)。
- **ParseX**：图文按页、音视频按秒计量，字段抽取分“新文档直抽”与“复用解析结果”两种计价路径 [计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Agent 安全高级防护**：正式计费后按防御席位（0.42 元/席位·小时）+ 超额 Credits（0.0015 元/Credit）组合计费，当前仍限时免费 [计费说明 (raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)。

> **注意**：文档 3 中称“工作流应用按执行路径上各计费节点调用量计费”，而文档 1 明确 Managed Agents 的会话运行时费与模型调用费“分别独立计费”。二者逻辑一致，但需注意：**Managed Agents 的会话运行时费是固定开销，无论是否触发模型调用均产生；而 Flow Agent 工作流中若某节点未被执行（如条件分支未命中），则该节点不产生任何费用**。

## 关键参数

| 参数 | 所属服务 | 含义 | 示例值/范围 |
|--------|-----------|------|-------------|
| `session_runtime_hours` | Managed Agents | 会话处于“运行中”状态的累计时长（小时） | 不足 1 小时按秒级精度折算 |
| `token_input` / `token_output` | 所有模型调用 | 模型输入/输出 Token 数量 | `qwen-plus`: 0.004 元/千 Input Token, 0.012 元/千 Output Token |
| `snapshot_count` × `snapshot_duration_hours` | Managed Agents（沙箱持久化） | 快照数量 × 单个快照保留时长 | 单价 0.003 元/个/小时 |
| `rcu` | 知识库（旗舰版） | 检索计算单元，1 RCU ≈ 支撑 50 QPS | 可配置 1–200 RCU，按小时计费 |
| `plan_version` | 记忆库 | Pro（启用 Rerank）或 Lite（跳过 Rerank）策略版本 | 写入与检索可独立指定 |
| `credits_consumed` | Agent 安全高级防护 | 每日检测内容换算所得 Credit 总量 | 默认 300 Credits/席位/天，超量部分计费 |

## 使用方式

- **查看用量**：统一通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看运行时长、Token、工具调用、知识库检索次数等明细；也可调用 `POST /usage/summary` 或 `POST /usage/trend` API 获取结构化数据 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **开通与配置**：
  - 知识库规格、RCU、TopK 参数在创建/编辑知识库时设置；
  - 记忆库 `plan_version` 在规则创建或 Search 请求中传参指定；
  - Sandbox 款型在创建时选择；
  - 安全高级防护需在 Security > 高级防护 > 安全策略页面完成服务授权后开通。
- **成本优化**：
  - 关闭知识库重排策略、降低 TopK 值可显著减少排序模型费用；
  - 对高频低精度场景，选用记忆库 Lite 版本或 ParseX 复用解析结果；
  - 及时终止闲置会话、删除不用的知识库/记忆库以停止对应运行时与存储计费。

## 限制和注意事项

- **免费额度不可叠加与跨项抵扣**：Managed Agents 的 10 小时运行时免费额度仅抵扣运行时费，不覆盖模型、工具或沙箱费用；知识库 720 小时免费额度仅适用于标准版规格费；记忆库写入/检索额度分规格发放，互不通用 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **计费起点明确**：
  - Managed Agents：自会话创建并启用（状态为“运行中”）起计运行时费；
  - 知识库：自成功创建起计规格费；
  - 记忆库：自 2026 年 8 月 20 日 10:00 起正式计费；
  - Sandbox：按秒计量，启动即开始计费。
- **存储与快照生命周期**：Managed Agents 沙箱持久化中，旧快照在新快照生成后才释放，因此快照保留时长可能大于单次会话运行时长；知识库平台存储费用已包含在规格费中，但若选用自购 ADB-PG 则需额外付费 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **模型调用费用的双重影响**：知识库检索产生的向量/排序模型调用费独立于规格费；同时，召回的记忆内容注入 Prompt 后，会增加大模型问答阶段的 Input Token，从而推高模型调用总费用 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **安全防护时效性**：Agent 安全高级防护的 Credit 按自然日重置，不结转；席位费仅对“运行中且启用高级防护”的 Agent 计费，Agent 停止后立即停计 [计费说明 (raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)


