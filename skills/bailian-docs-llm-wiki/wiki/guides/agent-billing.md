# agent billing

Agent Billing 涵盖 Managed Agents、Flow Agent（智能体/工作流应用）、Sandbox、记忆库、知识库、ParseX 及安全高级防护等核心组件的计费逻辑。所有费用均按实际用量独立计量，支持免费额度抵扣、资源包与后付费混合结算，并以控制台账单为准。开发者需重点关注各组件的计费项粒度（如会话时长、[Token](../concepts/token.md)、调用次数、RCU、Credit 等）及额度适用范围，避免跨组件误抵扣。

## 支持的模型/功能

- **Managed Agents**：按会话运行时长、模型调用（Input/Output [Token](../concepts/token.md)）、工具/MCP 调用（如 `web_search` ¥0.03/次）、沙箱持久化（¥0.003/个/小时）四类独立计费 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **Flow Agent**：智能体应用费用来自模型调用、知识库、MCP；工作流应用按执行路径上各计费节点（如大模型、图片解析、联网搜索）分别计费；编排能力本身不收费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **Sandbox**：分“会话运行费”（基础款 ¥0.156/小时，进阶款 ¥0.312/小时）和“数据保留费”（¥0.0021/GiB·小时），按秒计量 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **记忆库**：按写入（Add）、检索（Search）、存储三类计费，Pro/Lite 版本影响 Rerank 是否启用及单价（如 Search Pro ¥0.001/次，Lite ¥0.00002/次） [计费说明 (raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)。
- **知识库**：规格费用（标准版 ¥0.03/库/小时，旗舰版 ¥0.2/RCU/小时）与模型调用费用（向量、排序、路由、问答模型）分离计费，后者按 [Token](../concepts/token.md) 消耗量计算 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **ParseX**：图文按页（¥0.02/页）、音视频按秒（音频 ¥0.00035/秒，视频 ¥0.002/秒）计量；字段抽取分“新文档直接抽取”（¥0.06/页）与“复用解析结果抽取”（¥0.04/页） [计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)。
- **安全高级防护**：防御席位费（¥0.42/席位·小时） + 超额 Credits（¥0.0015/Credit），每个席位每日默认 300 Credits，过期不结转 [计费说明 (raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)。

> **注意**：文档 2 中提及“工作流应用中图片解析节点选择 Qwen VL 解析产生 Qwen-VL 系列模型调用费用”，但文档 5 在“工作流应用”小节明确说明“图片解析、文档解析、音频解析、视频解析使用内置大模型解析，暂不计费”。该矛盾尚未澄清，建议以控制台实时用量或最新 API 返回的 `usage` 字段为准，避免依赖静态文档描述。

## 关键参数

- **会话运行时长**：仅对处于“运行中”状态的会话计费（空闲不计），不足 1 小时按实际秒数折算（如 Sandbox 按秒，Managed Agents 按小时精确到小数点后多位）。
- **Token 计量**：模型调用费用统一按 `(Input Token + Output Token) / 1000 × 单价（元/千 Token）` 计算；知识库检索阶段的 Rerank 费用取决于**初步召回总切片数 × 平均切片 Token 数**，而非最终返回数量。
- **RCU（知识库）**：1 RCU ≈ 支撑 50 QPS，变配按小时分段计费；旗舰版规格费用 = RCU 数 × 小时数 × ¥0.2。
- **Snapshot/快照**：Managed Agents 沙箱持久化按快照存在时长计费（¥0.003/个/小时，不足 1 小时按 1 小时）；Sandbox 数据保留费按实际 GiB 占用量 × 保留时长 × ¥0.0021/GiB·小时。
- **Credits（安全）**：按自然日重置，每个席位独立 300 Credits，超支部分按 ¥0.0015/Credit 结算。
- **免费额度抵扣顺序**：所有组件均遵循 `免费额度 > 资源包 > 按量付费` 优先级；但额度严格限定用途（如知识库免费额度仅抵扣标准版规格费，不抵扣模型调用费）。

## 使用方式

- **查看用量**：统一通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看各组件汇总与明细；也可调用 `POST /usage/summary` 和 `POST /usage/trend` API 获取结构化数据 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **开通与配置**：
  - 知识库需主动开通服务并选择规格（标准版/旗舰版）；
  - 记忆库写入/检索版本由 `plan_version` 参数控制（Add 由规则决定，Search 由请求参数独立指定）；
  - 安全高级防护需完成服务授权并创建关联角色；
  - Sandbox 款型（基础/进阶/旗舰）在创建时选定。
- **成本优化**：
  - 关闭知识库 Rerank 或降低 TopK 值可显著减少排序模型费用；
  - 及时终止闲置会话、删除不用的知识库/Sandbox 以停止运行时长计费；
  - 复用 ParseX 解析结果进行字段抽取可节省 ¥0.02/页。

## 限制和注意事项

- **免费额度有效期严格受限**：Managed Agents 运行时免费额度为 10 小时、30 天有效；知识库新用户免费额度为 720 小时、30 天内有效，老用户则截至 2026 年 2 月 3 日；记忆库写入/检索额度 3 个月内有效，存储额度长期有效。
- **额度不可跨组件通用**：例如新人模型免费额度不能抵扣知识库规格费，知识库资源包不能抵扣记忆库写入费。
- **模型调用费用始终独立**：无论 Managed Agents、Flow Agent 还是知识库问答，所有模型调用（含 Embedding、Rerank、Qwen-Plus 路由、问答生成）均按对应模型的公开 Token 单价另行计费，且计入模型自身的免费额度与节省计划。
- **沙箱持久化与 Snapshot 生命周期**：Managed Agents 开启沙箱持久化后，上一快照不会立即释放，需待新快照成功生成后才释放旧快照；其保留时长累计计费。
- **安全高级防护限时免费**：截至 2026 年 9 月仍免费，正式计费前将提前一个月通知，开通即视为同意服务协议与角色授权。
- **文件上传本身不计费**：但基于文件内容的问答、解析、抽取等后续操作均产生对应费用。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-f23f20af1adb6c6b.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)


