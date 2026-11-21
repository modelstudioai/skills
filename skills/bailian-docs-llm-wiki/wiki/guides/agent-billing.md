# agent billing

Agent 计费采用按需、分项、独立计费模式，费用来源取决于实际使用的组件与服务类型（如 Sandbox、Flow Agent、Managed Agents、知识库、ParseX、安全防护等），各模块计费规则相互隔离，免费额度仅限抵扣其对应计费项。所有费用均以控制台账单为准，支持按小时出账与用量明细查询。

## 支持的模型/功能

Agent 相关计费覆盖以下核心能力模块：

- **Sandbox**：提供基础款、进阶款、旗舰款三种规格，按运行时长计费；支持暂停与 Snapshot 保留，产生数据保留费 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **Flow Agent**（含智能体应用与工作流应用）：本身不单独收费，费用来自所调用的模型（Token 计费）、知识库、MCP 工具及内置节点（如图片解析、联网搜索）[计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **Managed Agents**：自 2026-08-17 起商业化，费用由会话运行时费、模型调用费、工具/MCP 调用费、沙箱持久化费四部分组成 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **知识库（RAG）**：按规格（标准版/旗舰版）收取运行时长费，并额外收取向量模型、排序模型、路由模型、问答模型等调用产生的 Token 费用 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **ParseX**：按输入类型分项计量（图文按页、音视频按秒），支持一次性免费额度与按量付费 [计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Agent 安全高级防护**：按“防御席位 × 小时” + “超额 Credits”组合计费，当前仍处于限时免费阶段（截至 2026 年 9 月）。

> **注意**：文档 5 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md` 的两份副本，以该路径最新版本为准，无需重复引用。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `运行时长` | Sandbox / Managed Agents / 知识库等按实际占用小时（不足 1 小时按比例折算）计费 | Sandbox 进阶款：0.312 元/小时；Managed Agents：0.5 元/小时；标准版知识库：0.03 元/(个×小时) |
| `Token 数量` | 模型调用（含向量、排序、问答、路由等）按输入/输出 Token 总量计费，单位为千 Token | text-embedding-v4：0.0005 元/千 Token；qwen-plus Input：0.004 元/千 Token |
| `RCU（Retrieval Compute Unit）` | 仅旗舰版知识库使用，1 RCU ≈ 支撑 50 QPS，按 RCU × 小时计费 | 0.2 元/RCU/小时 |
| `Credits` | Agent 安全高级防护中用于度量检测内容量的虚拟单位，按自然日重置 | 默认 300 Credits/席位/日，超额部分 0.0015 元/Credit |
| `页数 / 秒数` | ParseX 计量单位：图文按处理页数，音视频按处理秒数 | 图文解析：0.02 元/页；视频解析：0.002 元/秒 |

## 使用方式

- **费用触发条件**：仅当资源处于**实际运行状态**（如 Sandbox 启动、Managed Agents 会话启用、知识库创建后未删除、ParseX 任务执行、安全防护开启并检测）时开始计费；空闲、暂停、未开通状态不产生费用。
- **免费额度使用逻辑**：严格遵循「免费额度 > 资源包 > 按量付费」三级扣减顺序，且额度不可跨计费项通用（例如知识库免费时长不能抵扣模型 Token 费）。
- **用量查询**：
  - Sandbox：控制台用量页或调用 [Usage API](raw/application-api-reference/managed-agents-api/usage-api.md)；
  - Managed Agents：`POST /usage/summary` 或 `POST /usage/trend`；
  - 知识库：账单详情页筛选「阿里云百炼知识库（RAG）- 后付费」或「阿里云百炼大模型推理」；
  - ParseX：[任务记录](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/tasks.md) 与 [用量](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/usage.md) 页面；
- **账单管理**：所有费用统一归集至「大模型服务平台阿里云百炼」产品下，支持按小时粒度导出明细账单，实例 ID 可标识具体资源（如知识库 ID、模型类型标识符）。

## 限制和注意事项

- **Sandbox 数据保留费**：暂停或保存 Snapshot 均按实际占用 GiB × 小时计费；默认 15 GiB 系统盘不收费，但用户写入数据超出部分计入统计 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **知识库 Rerank 费用陷阱**：排序模型费用取决于**初步召回总切片数 × 平均切片 Token 数**，而非最终返回数量；关闭重排策略可显著降本，但影响检索精度。
- **多知识库叠加成本**：同一 Query 在 N 个挂载的知识库中分别执行完整检索流程（Query 向量化 + Rerank），模型 Token 消耗量呈线性增长（×N）。
- **Managed Agents 沙箱持久化计费**：快照按“存在时长”计费（非生成次数），旧快照在新快照成功生成后才释放，累计时长需手动在会话用量页核对。
- **安全防护 Credit 隔离性**：每个 Agent 席位的 300 Credits 独立计算、不共享、不结转，超时自动清零。
- **模型缓存费用归属**：智能模式下 AUTO 路由的缓存费用按统一刊例价计费；显式选择模型时，缓存费用遵循该模型自身规则，详见 [上下文缓存](raw/model-user-guide/model-experience/text-generation-model/context-cache.md)。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


