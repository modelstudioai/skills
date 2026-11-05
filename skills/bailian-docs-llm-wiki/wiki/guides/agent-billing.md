# agent billing

百炼平台的 Agent 计费体系采用多维度、按需计量模式，覆盖 Sandbox 运行、智能体/工作流执行、Managed Agents、知识库、ParseX、安全高级防护等核心能力。费用由运行时长、模型 [Token](../concepts/token.md)、组件调用次数、存储占用、安全席位等多种计费项独立构成，支持免费额度、资源包与节省计划抵扣。所有计费均以实际用量为准，按小时出账。

## 支持的模型/功能

Agent 相关计费覆盖以下主要能力模块：

- **Sandbox**：提供基础款、进阶款、旗舰款三种规格，按实际运行秒级计费；暂停或保存 Snapshot 时产生数据保留费 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **Flow Agent（智能体/工作流应用）**：编排本身不收费，费用来自所调用的模型（如 Qwen 系列）、知识库、MCP（如文生图、语音合成）及内置工具（如 `web_search`）。模型调用按输入/输出 [Token](../concepts/token.md) 计费；知识库和 MCP 按各自标准独立计费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **Managed Agents**：自 2026-08-17 起商业化，费用含三部分：会话运行时费（0.5 元/小时）、模型调用费（按所选模型 [Token](../concepts/token.md) 标准）、工具/MCP 调用费（如 `web_search` 0.03 元/次） [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **知识库（RAG）**：规格费用（标准版 0.03 元/知识库/小时，旗舰版 0.2 元/RCU/小时） + 模型调用费用（向量、排序、路由、问答模型均按 Token 计费），二者完全独立 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **ParseX**：图文按页、音视频按秒计量，支持解析与字段抽取分项计费，新文档直接抽取单价已含解析成本 [计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Agent 安全高级防护**：限时免费中，正式计费后按“防御席位费（0.42 元/席位·小时）+ 超额 Credits（0.0015 元/Credit）”组合计费，Credit 按自然日重置且不可跨席位共享 [计费说明 (raw/application-user-guide/agent-billing/billing.md)](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：文档 4 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md` 的副本，以该路径唯一文档为准，避免引用歧义。

## 关键参数

| 参数 | 说明 | 示例值/范围 |
|--------|------|-------------|
| `RCU`（知识库） | 检索计算单元，1 RCU ≈ 支撑 50 QPS；旗舰版按 RCU 数量计费 | 1–200 RCU 可调 |
| `TopK`（知识库检索） | 初步召回切片数，直接影响排序模型 Token 消耗量 | 向量 TopK（默认 50）、关键词 TopK（默认 50） |
| `席位`（安全防护） | 一个处于运行中且启用高级防护的 Agent 实例 | 席位数 = 启用高级防护的 Agent 数量 |
| `Credit`（安全防护） | 安全检测消耗单位，按被检内容 Token 换算；每个席位每日 300 Credit 免费 | 有效期 24 小时，不结转 |
| `GiB·小时`（Sandbox 数据保留） | 暂停状态下的内存/磁盘快照占用量与时长乘积 | 单价 0.0021 元/GiB·小时 |

## 使用方式

- **Sandbox**：创建即开始计费；暂停后仅产生数据保留费；删除实例立即停止所有计费。
- **Flow Agent**：发布应用后，每次调用按执行路径上实际触发的计费节点汇总计费（如模型节点、知识库节点、MCP 节点）；未进入执行路径的节点不计费。
- **Managed Agents**：调用 `CreateSession` 后即开始计收运行时费；需主动调用 `TerminateSession` 终止会话以停止计费。
- **知识库**：创建成功即开始计收规格费用；模型调用费在知识管理（上传/更新）、检索（Query 向量化、Rerank 排序、路由判断）、问答（生成回答）等环节实时产生。
- **ParseX**：调用 `ParseDocument` 或 `ExtractFields` API 即触发计量；复用已有解析结果可降低抽取成本（¥0.04/页 vs ¥0.06/页）。
- **安全高级防护**：需在控制台 Security > 高级防护 > 安全策略页面完成服务授权开通；仅对启用该功能的运行中 Agent 计费。

## 限制和注意事项

- **免费额度不可叠加或转移**：新人免费额度、知识库 720 小时额度、ParseX 一次性赠送额度均按账户/实例独立发放，不跨产品、不跨账号、不结转。老用户知识库免费额度统一于 2026-02-03 失效 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **模型调用费始终独立于组件规格费**：例如知识库的规格费用（0.03 元/小时）与其中使用的 `text-embedding-v4` 向量模型费用（0.0005 元/千 Token）分别计费、分别抵扣，节省计划仅适用于后者。
- **Rerank 排序费用取决于初步召回总量，而非最终返回数量**：若初步召回 100 个切片（平均 500 Token/切片），则排序 Token 消耗为 50,000，即使最终只返回 5 个切片，费用仍按 50,000 Token 计算。
- **Sandbox 系统盘不计费，但超出部分需付费**：每个 Sandbox 默认含 15 GiB 免费系统盘；额外挂载的云盘或 Snapshot 占用空间按 `GiB·小时` 单独计费。
- **高级防护 Credit 按自然日清零**：每日 00:00 重置各席位额度，未用完的 Credit 不累计至次日。
- **工作流中“图片解析”节点存在计费差异**：选择 Qwen-VL 解析会产生模型调用费；选择内置大模型文档解析则暂不计费 —— 开发者需在节点配置中明确选择 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


