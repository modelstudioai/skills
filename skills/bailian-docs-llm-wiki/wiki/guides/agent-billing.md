# agent billing

Agent 计费采用按需、分项、独立计费模式，费用来源于实际调用的模型、组件及运行资源，而非 Agent 抽象形态本身。各模块（如模型、知识库、Sandbox、MCP、ParseX、安全防护）均按自身计量单位单独计费，免费额度与资源包仅限抵扣其指定计费项。实际费用以控制台账单为准，开发者需关注各环节的用量来源与叠加关系。

## 支持的模型/功能

- **大语言模型（LLM）**：所有显式或隐式调用的百炼平台模型（含 `qwen-plus`、`qwen3.7-plus`、`text-embedding-v4`、`qwen3-rerank` 等）均按输入/输出 [Token](../concepts/token.md) 计费，标准见[选择模型](raw/model-user-guide/get-started-with-models/models.md)；智能模式下 AUTO 路由按统一刊例价计费，档位模式（性能/均衡/经济）按所选档位计费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **知识库（RAG）**：包含规格费用（标准版 0.03 元/知识库/小时，旗舰版按 RCU 计费）和模型调用费用（向量化、排序、路由、问答生成），二者完全分离 [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。
- **Sandbox**：按会话运行时长（基础款 0.156 元/小时）和数据保留量（0.0021 元/GiB·小时）计费，系统盘 15 GiB 免费 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。
- **Managed Agents**：费用由四部分组成：会话运行时费（0.5 元/小时）、模型调用费（按所调模型标准）、工具/MCP 调用费（如 `web_search` 0.03 元/次）、沙箱持久化（0.003 元/个/小时） [计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。
- **ParseX**：图文按页、音视频按秒计量；解析与字段抽取分项计费，新文档直接抽取已含解析成本 [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)。
- **Agent 安全高级防护**：按“防御席位费（0.42 元/席位·小时）+ 超额 Credits（0.0015 元/Credit）”组合计费，当前处于限时免费阶段 [计费说明 (raw/application-user-guide/agent-billing/billing.md)](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：文档 5 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md` 的副本，以该路径唯一文档为准；文档 4 中明确指出知识库路由调用 `qwen-plus` 产生模型费用，而文档 1 中“智能体应用”章节未提及此场景，存在覆盖遗漏，开发者在多知识库配置中需主动计入此项成本。

## 关键参数

| 参数 | 说明 | 示例值/范围 |
|------|------|-----------|
| `RCU` | 知识库检索计算单元，1 RCU ≈ 支持 50 QPS | 旗舰版支持 1–200 RCU，按需配置 |
| `TopK`（初步向量/关键词召回） | 影响排序模型 [Token](../concepts/token.md) 消耗的核心参数 | 默认各 50，取值范围 10–100；降低可显著减少 rerank 费用 |
| `最终召回数量` | 仅控制返回结果数，**不影响**排序费用 | 与排序费用无关，仅影响下游处理 |
| `Credit` | 安全检测计量单位，按被检内容 [Token](../concepts/token.md) 换算 | 每席位每日默认 300 Credits，24 小时清零 |
| `Snapshot 保留时长` | Sandbox 持久化与 Managed Agents 沙箱持久化共同计量维度 | 不足 1 小时按 1 小时计费 |

## 使用方式

- **费用归属**：所有通过分享链接触发的调用，费用均由应用创建者 UID 承担 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **用量查询**：
  - Flow Agent / 工作流：通过[账单与成本管理](raw/model-user-guide/test-1/bill-query-and-cost-management.md)按执行路径核对节点用量；
  - Managed Agents：控制台 [用量](https://bailian.console.aliyun.com/managed-agent/usage) 页面或调用 `POST /usage/summary` 和 `POST /usage/trend` API；
  - 知识库：账单详情页筛选“阿里云百炼知识库（RAG）- 后付费”查看规格费用，筛选“阿里云百炼大模型推理”查看向量/排序模型 Token 用量；
  - ParseX：通过[任务记录](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/tasks.md)和[用量](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/usage.md)页面核对。
- **免费额度使用**：遵循“免费额度 > 资源包 > 按量付费”扣费顺序；知识库免费额度仅限标准版规格费用，不覆盖模型调用；新人模型免费额度可抵扣所有模型调用 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。

## 限制和注意事项

- **不计费项**：文件上传、Prompt 自动优化、UI 设计器功能本身不收费；但 AI 对话、文件存储、数据库超出免费额度后按量计费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。
- **缓存行为**：智能体应用暂不支持配置显式缓存；支持隐式缓存的模型自动生效且无法关闭；缓存费用按对应模型规则单独计费。
- **知识库费用叠加风险**：挂载 N 个知识库时，Query 向量化与 Rerank 排序费用按 N 倍增加，且路由调用 `qwen-plus` 额外产生一次模型费用。
- **Sandbox 数据保留**：暂停状态仍产生数据保留费；Snapshot 创建后，上一快照不会立即释放，仅在新快照成功生成后释放，需注意累计保留时长。
- **资源包退订**：预付费资源包未使用部分可申请退款，已使用部分不可退；退订后知识库转为按量付费，删除知识库是唯一停止规格费用的方式。
- **安全防护时效性**：高级防护当前限时免费，正式计费前将提前至少一个月通知；默认防护能力（身份签发、内容安全等）始终免费且自动生效。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


