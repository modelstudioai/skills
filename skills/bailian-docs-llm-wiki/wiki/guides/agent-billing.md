# agent billing

Agent 计费采用多维度、按需付费模式，费用来源取决于所用 Agent 类型（Sandbox、Managed Agents、Flow Agent）、调用的底层组件（模型、知识库、MCP、ParseX 等）及启用的安全能力。各计费项独立计量、独立抵扣，免费额度与资源包仅限指定计费项使用，不跨类型通用。实际费用以控制台账单为准。

## 支持的模型/功能

Agent 计费不绑定单一模型，而是根据实际调用的模型和功能组件分别计费：

- **大模型调用**：所有 Agent 形态均产生模型 Token 费用，包括 `qwen-plus`、`qwen3.7-plus`、`text-embedding-v4`、`qwen3-rerank` 等，单价按模型广场公开标准执行（如 Input 0.004 元/千 Token，Output 0.012 元/千 Token）[计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **知识库（RAG）**：含规格费用（标准版 0.03 元/知识库/小时，旗舰版按 RCU 计费）和模型调用费用（向量、排序、路由、问答生成等），二者完全分离 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **ParseX 文档解析**：按页（图文）、秒（音视频）计量，图文解析 ¥0.02/页，视频解析 ¥0.002/秒，支持一次性免费额度 [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)。
- **MCP 与工具调用**：如 `web_search` 按 0.03 元/次计费，部分 MCP（如文生图）按模型调用计费，第三方 API 调用费用由第三方收取 [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **安全高级防护**：防御席位费（0.42 元/席位·小时）与超额 Credits（0.0015 元/Credit），当前限时免费，正式计费后生效 [计费说明](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：文档 6 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md`，属同一版本，无矛盾；但需注意该文档中“截至 2026 年 9 月仍限时免费”的说明与其他已商业化服务（如 Managed Agents 自 2026-08-17 起计费）存在时间线交叉，开发者应以控制台实时价格与账单为准，勿依赖文档中的未来时间点描述。

## 关键参数

| 参数 | 说明 | 示例值/范围 |
|------|------|-------------|
| `session_runtime_hours` | Sandbox 或 Managed Agents 运行时长（小时），按秒累计，不足 1 小时精确到分钟 | 40 分钟 = 0.6667 小时 |
| `snapshot_size_gb` | Snapshot 占用存储量（GiB），用于计算数据保留费 | 6 GiB |
| `rcu` | 知识库旗舰版检索计算单元，1 RCU ≈ 50 QPS；变配后分段计费 | 1–200 RCU |
| `topk_vector` / `topk_keyword` | 知识库检索参数，直接影响 Rerank 模型 Token 消耗量 | 默认 50，可调至 10–100 |
| `credit_consumption` | 安全高级防护消耗 Credits，按被检测内容 Token 换算，每日重置 | 每席位默认 300 Credits/天 |

## 使用方式

- **Sandbox**：创建时选择基础/进阶/旗舰款，运行即产生会话运行费；暂停或保存 Snapshot 触发数据保留费 [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **Managed Agents**：启用即开始计费会话运行时费（0.5 元/小时）；模型调用与工具调用在运行中自动触发，费用独立叠加。
- **Flow Agent**：智能体应用费用 = 模型调用 + 知识库规格费 + 知识库模型费 + MCP 调用费；工作流应用费用 = 执行路径上各计费节点（模型、解析、知识库等）费用之和。
- **知识库**：开通即开始计费规格费；上传/更新/检索/问答操作触发对应模型调用费；关闭 Rerank 可显著降低检索成本。
- **ParseX**：调用解析或抽取接口即触发计量；新文档直接抽取已含解析费，复用解析结果则仅收抽取费。

## 限制和注意事项

- **免费额度不可跨类抵扣**：Managed Agents 的 10 小时运行时免费额度仅抵扣运行时费，不抵扣模型或工具费；知识库 720 小时免费额度仅适用于标准版规格费，不覆盖旗舰版或任何模型调用费。
- **模型调用费用倍增风险**：当一个智能体应用挂载 N 个知识库时，Query 向量化与 Rerank 排序的 Token 消耗量将 ×N，务必在多知识库场景下监控账单明细 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **暂停 ≠ 停止计费**：Sandbox 暂停后仍产生数据保留费；知识库删除才停止规格费；Managed Agents 需显式终止会话才能停止运行时费。
- **缓存与计费分离**：上下文缓存自动生效且不额外收费，但其节省的 Token 量会影响最终模型调用费用；智能模式下 AUTO 路由按统一刊例价计费，与实际路由模型无关。
- **账单粒度**：知识库规格费按小时出账；模型调用费按小时聚合显示用量（千 Tokens）与金额；Credits 按自然日清零，不结转。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


