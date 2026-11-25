# Agent 计费

<a id="费用构成"></a>

## 费用构成

Agent 的费用取决于实际使用的运行时、模型和组件。模型调用费用与组件费用分别核对，免费额度只抵扣其指定的计费项。

| 服务 | 计费对象 | 计费详情 |
| --- | --- | --- |
| Managed Agents | 会话运行时、模型调用、工具及 MCP 调用 | [Managed Agents](agent-billing/managed-agents-billing.md) |
| Flow Agent | 模型调用费用；所调用的知识库及工具按对应服务另计 | [Flow Agent](agent-billing/flow-agent-billing.md) |
| Sandbox | 会话运行时及数据保留 | [Sandbox](agent-billing/sandbox-billing.md) |
| RAG | 知识库规格与模型调用 | [RAG](agent-billing/billing-for-knowledge-base.md) |
| Memory | 按记忆策略版本及计费项计量 | [Memory](agent-billing/billing-f23f20af1adb6c6b.md) |
| ParseX | 解析与抽取分项；图文按页、音视频按秒 | [ParseX](agent-billing/pricing.md) |
| Security | 按安全防护服务的计费规则 | [Security](agent-billing/billing-a923eaad372554c6.md) |

<a id="计费与免费额度"></a>

## 计费与免费额度

各服务的价格、地域、免费额度有效期、抵扣顺序和超出额度后的行为见上表详情。组合多个组件时，分别核对实际调用和规格费用。

[模型计费](../model-user-guide/test-1/model-pricing.md) · [账单与成本管理](../model-user-guide/test-1/bill-query-and-cost-management.md)
