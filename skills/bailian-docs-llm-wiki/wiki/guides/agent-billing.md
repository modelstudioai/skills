# agent billing

Agent 计费采用多维度、按需付费模式，费用由运行时资源、模型调用、组件服务（如知识库、ParseX、MCP、安全防护等）三类独立计费项构成。各模块遵循“免费额度优先抵扣 → 资源包次之 → 后付费兜底”的扣费顺序，实际账单以控制台台账为准。开发者需根据应用形态（Managed Agents / Sandbox / Flow Agent）和所用组件明确对应计费边界。

## 支持的模型/功能

Agent 相关计费覆盖以下核心能力模块：

- **Managed Agents**：提供会话运行时费（0.5 元/小时）、模型调用费（按所选模型 Token 实际消耗计费）、工具及 MCP 调用费（如 `web_search` 0.03 元/次）[计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)  
- **Sandbox**：按款型（基础/进阶/旗舰）收取会话运行费（0.156–0.624 元/小时），并单独计收数据保留费（0.0021 元/GiB·小时）[计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)  
- **Flow Agent**（含智能体应用与工作流应用）：编排本身不收费，费用源自实际执行的模型节点、知识库、MCP、联网搜索等组件；其中工作流按执行路径上各计费节点（如大模型、图片解析、知识库）分别计量 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)  
- **知识库（RAG）**：规格费用（标准版 0.03 元/知识库/小时，旗舰版 0.2 元/RCU/小时）与模型调用费用（向量、排序、路由、问答模型均按 Token 单独计费）分离 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
- **ParseX**：图文按页、音视频按秒计量，支持解析与字段抽取分项计费（如新文档直接抽取 ¥0.06/页，复用解析结果抽取 ¥0.04/页）[计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)  
- **Agent 安全高级防护**：防御席位费（0.42 元/席位·小时） + 超额 Credits（0.0015 元/Credit），当前处于限时免费阶段 [计费说明 (raw/application-user-guide/agent-billing/billing.md)](../../raw/application-user-guide/agent-billing/billing.md)  

> **注意**：文档 5 和文档 7 内容完全重复，均为 `raw/application-user-guide/agent-billing/billing.md` 的冗余副本，以该路径唯一文档为准；其描述的“限时免费”状态与文档 1 中 Managed Agents 已于 2026-08-17 商业化计费形成明确阶段差异，开发者需按具体服务开通时间判断是否计费。

## 关键参数

| 参数 | 说明 | 示例值/范围 |
|--------|------|-------------|
| `会话运行时长` | Managed Agents/Sandbox 按秒计量，不足 1 小时精确到秒 | 5 小时 23 分 = 5.38 小时 |
| `RCU` | 知识库旗舰版并发能力单位，1 RCU ≈ 50 QPS；变配后分段计费 | 2 RCU → 规格费用 = 2 × 0.2 元/小时 |
| `TopK 参数` | 知识库检索中 `初步向量检索 TopK` 与 `初步关键词检索 TopK` 直接影响排序模型 Token 消耗量 | 默认各 50，调整为 10 可显著降低 rerank 费用 |
| `Credit` | Agent 安全高级防护用量单位，按检测内容 Token 换算，每日重置 | 每席位默认 300 Credits/天，不可结转 |
| `页数` | ParseX 文档解析计量单位：PDF/PPT/图片按页，文本类按每 2000 字符折算 1 页 | 10,000 字 Word → 5 页 |

## 使用方式

- **开通即用型服务**（如 Managed Agents、Flow Agent）：创建并启用后自动开始计费，无需额外开通；终止会话或删除知识库可立即停止对应规格费用。
- **显式开通型服务**（如 Sandbox、知识库、安全高级防护、ParseX）：需在控制台完成开通操作（如点击“立即开通”、购买资源包、授权服务角色），开通后按实际使用量计费。
- **免费额度抵扣**：所有服务均默认启用额度抵扣逻辑（如 Managed Agents 10 小时运行时、知识库 720 小时标准版、ParseX 3000 页图文），额度耗尽后自动切换至后付费。
- **资源包采购**：知识库与 ParseX 支持预付费资源包（如标准版知识库 1 个/年 239 元），购买后按实际用量抵扣，优先于后付费。

## 限制和注意事项

- **会话状态敏感性**：Managed Agents 仅在“运行中”状态产生运行时费，空闲/暂停不计费；Sandbox 暂停后仍产生数据保留费 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)  
- **知识库多实例放大效应**：挂载 N 个知识库时，Query 向量化与 Rerank 排序的 Token 消耗量按 N 倍增加，且无法关闭单库检索 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)  
- **模型缓存不减免费用**：智能体应用中启用上下文缓存（如 qwen-plus 缓存）仍按完整 Token 量计费，缓存仅降低延迟，不改变计费逻辑 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)  
- **文件上传本身免费**：文件问答中的上传操作不计费，但基于文件内容的解析、向量化、问答生成等后续环节均产生对应费用 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)  
- **删除即不可逆**：知识库删除后数据永久清除且无法恢复，删除是唯一停止规格费用的方式；Sandbox 删除后亦停止所有计费 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


