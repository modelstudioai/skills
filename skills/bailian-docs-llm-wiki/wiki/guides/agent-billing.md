# agent billing

Agent 计费覆盖 Managed Agents、Flow Agent（含智能体/工作流应用）、Sandbox、知识库、安全高级防护及 ParseX 等核心组件，各模块独立计费、按量结算。费用结构清晰分为运行时资源费、模型/组件调用费、持久化/存储费及安全防护费四类，支持免费额度、资源包与节省计划等成本优化机制。实际费用以控制台账单为准，开发者需结合用量监控与配置调优主动控本。

## 支持的模型/功能

- **Managed Agents**：支持 Qwen 系列模型（如 `qwen-plus`、`qwen3.7-plus`）的 Token 调用计费；内置工具如 `web_search`（0.03 元/次）、`web_fetch`（限时免费）；沙箱持久化快照按 0.003 元/个/小时计费 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **Flow Agent**：智能体应用计费来自模型调用、知识库、MCP 及上下文缓存；工作流应用按执行路径上各计费节点（如大模型、图片解析、联网搜索）分别计费；文件上传、Prompt 自动优化、UI 设计器本身不计费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **Sandbox**：按款型（基础/进阶/旗舰）收取会话运行费（0.156–0.624 元/小时），暂停或 Snapshot 数据保留费为 0.0021 元/GiB·小时 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **知识库**：规格费用（标准版 0.03 元/库/小时，旗舰版 0.2 元/RCU/小时）与模型调用费用（向量/排序/路由/问答模型）分离计费；`text-embedding-v4`、`qwen3-rerank` 等 A 类模型支持 AI 通用型节省计划抵扣 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **ParseX**：图文按页（¥0.02/页）、音视频按秒（音频 ¥0.00035/秒，视频 ¥0.002/秒）计量；字段抽取分“新文档直接抽取”（¥0.06/页）与“复用解析结果抽取”（¥0.04/页）两种单价 [计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)。

> **注意**：文档 5 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md` 的冗余副本，以文档 5 为准；文档 2 中提及“智能模式各档位的缓存费用见[智能模式计费明细]”，但该链接为外部 help.aliyun.com 地址，非平台内原始文档，无法验证一致性，建议以模型广场中对应模型的公开计费标准为准。

## 关键参数

| 参数 | 说明 | 示例值/范围 |
|------|------|-----------|
| `session_runtime_hours` | Managed Agents 运行中会话时长（不足 1 小时按实际秒级折算） | `5.83` 小时（350 分钟） |
| `token_input/output` | 模型调用的输入/输出 Token 数，决定模型费用 | `qwen-plus`: Input 0.004 元/千 Token, Output 0.012 元/千 Token |
| `snapshot_count` & `snapshot_duration_hours` | 沙箱持久化快照数量与每个快照保留时长（不足 1 小时按 1 小时计） | 2 个快照 × 各保留 36 小时 → 72 小时计费 |
| `rcu` | 知识库旗舰版并发能力单位，1 RCU ≈ 50 QPS；变配后分段计费 | 配置 2 RCU，运行 0.5 小时 → `0.5 × 2 × 0.2 = 0.20` 元 |
| `credit_consumption` | 安全高级防护中检测内容换算的 Credits，每日默认 300 Credits/席位，超限部分按 0.0015 元/Credit 计费 | 10,000 Credits 总消耗 → 超额 `(10000−900)×0.0015 = 13.65` 元 |
| `parse_pages` / `audio_seconds` | ParseX 文档页数或音视频处理秒数，为唯一计量维度 | PDF 解析 120 页 → `120 × 0.02 = 2.40` 元 |

## 使用方式

- **查看用量**：统一通过控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面查看运行时长、Token、工具调用等明细；也可调用 [Usage API](raw/application-api-reference/managed-agents-api/usage-api.md) 获取工作空间/Agent/Session 级别汇总与趋势数据。
- **开通服务**：知识库、安全高级防护、ParseX 均需在控制台显式开通；Sandbox 和 Managed Agents 在创建并启用后即开始计费；Flow Agent 编排本身免费，仅其调用的下游组件计费。
- **成本优化**：
  - 知识库：关闭重排策略、降低 `TopK` 值可显著减少排序模型 Token 消耗；
  - Managed Agents：及时终止空闲会话避免运行时费累积；
  - 模型调用：使用 AI 通用型节省计划抵扣向量/排序模型费用；
  - Sandbox：合理规划运行与暂停周期，避免长时间低效保留数据。

## 限制和注意事项

- **免费额度不可叠加或跨模块使用**：Managed Agents 的 10 小时运行时免费额度仅抵扣运行时费，不覆盖模型/工具费；知识库 720 小时免费额度仅适用于标准版规格费；新人模型免费额度仅抵扣模型调用费 [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **计费粒度差异**：Managed Agents 运行时费按秒级精确计算；Sandbox 运行费按秒、数据保留费按 GiB·小时；知识库规格费按小时出账；ParseX 图文按页、音视频按秒；安全 Credits 按自然日清零。
- **共享与归属**：分享链接产生的费用由应用创建者 UID 承担；多知识库/多 Agent 共享同一账号免费额度或资源包，但额度按实例数量线性扣减（如 4 个标准版知识库每小时扣减 4 小时额度）。
- **停用即止费**：删除知识库、终止 Managed Agents 会话、关闭 Sandbox 或卸载安全高级防护后，对应计费项立即停止；但已生成的 Snapshot、已缓存的解析结果等仍可能产生后续保留费用。
- **第三方费用隔离**：MCP 若调用第三方 API（如某些语音合成服务），其费用由第三方收取，百炼不参与计费；ADB-PG 作为知识库向量存储时，其费用单独结算。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


