# agent billing

Agent 计费覆盖 Sandbox、Flow Agent（智能体/工作流应用）、Managed Agents、知识库、ParseX 及安全高级防护等多个核心能力模块，采用按量付费为主、资源包与免费额度为辅的混合计费模型。各模块计费项相互独立，费用按实际使用量（时长、Token、页数、Credits 等）精确计量，支持分段计费与多级抵扣。开发者需根据具体部署形态和调用路径识别对应计费单元。

## 支持的模型/功能

- **Sandbox**：提供基础款（0.156 元/小时）、进阶款（0.312 元/小时）、旗舰款（0.624 元/小时）三档运行时计费，另收取数据保留费（0.0021 元/GiB·小时）；默认含 15 GiB 免费系统盘 [计费说明 (raw/application-user-guide/agent-billing/sandbox-billing.md)](../../raw/application-user-guide/agent-billing/sandbox-billing.md)。  
- **Flow Agent**：本身不单独收费，费用源自所调用的模型、知识库、MCP 工具及解析节点；例如图片解析若选用 Qwen VL 则产生模型调用费，而内置文档/音频/视频解析暂不计费 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。  
- **Managed Agents**：自 2026-08-17 起商业化，计费项包括会话运行时费（0.5 元/小时）、模型调用费（按所选模型 Token 标准）、工具/MCP 调用费（如 `web_search` 0.03 元/次）[计费说明 (raw/application-user-guide/agent-billing/managed-agents-billing.md)](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)。  
- **知识库**：规格费用（标准版 0.03 元/知识库/小时，旗舰版 0.2 元/RCU/小时）与模型调用费用（向量、排序、路由、问答模型）分离计费；多个知识库并行检索时，Token 消耗量按知识库数量倍增 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **ParseX**：按处理维度计量——图文按页、音视频按秒；新文档直接抽取单价（¥0.06/页）已含解析，复用解析结果抽取单价更低（¥0.04/页）[计量与计费 (raw/application-user-guide/agent-billing/pricing.md)](../../raw/application-user-guide/agent-billing/pricing.md)。  
- **Agent 安全高级防护**：防御席位费（0.42 元/席位·小时）与超额 Credits（0.0015 元/Credit）组合计费；默认防护（身份签发、内容安全等）免费且自动生效 [计费说明 (raw/application-user-guide/agent-billing/billing.md)](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：文档 6 和文档 7 内容完全重复，系同一份原始文档被误收录两次，以单次引用为准；文档 5 中“老用户免费额度有效期截至 2026 年 2 月 3 日”与文档 3 中“Managed Agents 免费额度有效期 30 天”逻辑一致，但文档 2 提到“新人免费额度”未明确时效，开发者应以控制台实时显示的额度有效期为准。

## 关键参数

- **时长类**：Sandbox 运行时长（秒级精度）、Managed Agents 会话运行时长（小时级，不足 1 小时按比例计）、知识库规格运行时长（小时级，支持分段计费）、安全席位运行时长（小时级）。  
- **Token 类**：模型输入/输出 Token（按千 Token 计费）、知识库向量化与排序 Token（按初步召回切片总量计算，非最终返回量）、安全检测 Credit（按 Token 换算，1 Credit ≈ 若干 Token，具体换算比以控制台为准）。  
- **容量/数量类**：Sandbox 数据保留量（GiB）、知识库 RCU 数量（1 RCU ≈ 50 QPS）、ParseX 处理页数/秒数、安全席位数（即启用高级防护的运行中 Agent 实例数）。  
- **免费额度**：Sandbox 无通用免费额度；Flow Agent 可用新人免费额度抵扣模型调用；Managed Agents 赠送 10 小时运行时；知识库赠送 720 小时标准版规格费（新用户 30 天有效）；ParseX 首次开通赠图文/字段抽取各 3,000 页、音视频各 100 小时；安全防护暂无免费额度（限时免费阶段）。

## 使用方式

- **费用归属**：所有费用均由应用创建者 UID 账号承担，包括通过分享链接产生的调用 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。  
- **抵扣顺序**：统一遵循 **免费额度 > 资源包 > 按量付费** 三级抵扣逻辑，适用于知识库规格费、模型调用费等支持该机制的计费项。  
- **账单查询**：  
  - Sandbox/Managed Agents/安全防护费用见 [账单与成本管理](raw/model-user-guide/test-1/bill-query-and-cost-management.md)；  
  - 知识库规格费用在账单中筛选“阿里云百炼知识库（RAG）- 后付费”，模型 Token 费用筛选“阿里云百炼大模型推理”；  
  - ParseX 用量可在 [用量](raw/application-user-guide/agent-context/getting-started-overview/settings-configurations/usage.md) 页面查看。  
- **成本优化**：  
  - 知识库可关闭重排策略或降低 TopK 值减少排序 Token 消耗；  
  - Flow Agent 工作流中未执行路径的节点不计费；  
  - 及时终止闲置 Sandbox 或 Managed Agents 会话以避免运行时费累积。

## 限制和注意事项

- **暂停≠停止计费**：Sandbox 暂停后仍产生数据保留费；知识库删除后费用立即终止，但数据永久清除且不可恢复 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **模型费用叠加风险**：知识库检索时，若挂载 N 个知识库，Query 向量化与排序 Token 消耗量 ×N；工作流中模型节点若被多次执行（如循环），Token 费用累加 [计费说明 (raw/application-user-guide/agent-billing/flow-agent-billing.md)](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)。  
- **资源包有效期刚性**：知识库资源包（如标准版 720 小时/月）购买后一年内有效，过期未用完自动作废；退订仅支持未使用部分退款 [知识库计费说明 (raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **安全防护开通依赖角色授权**：高级防护需显式开通并同意服务协议，系统自动创建 5 个 AliyunServiceRoleFor* 角色；默认防护无需操作 [计费说明 (raw/application-user-guide/agent-billing/billing.md)](../../raw/application-user-guide/agent-billing/billing.md)。  
- **价格时效性**：所有单价均以控制台实时展示及费用账单为准，文档中刊例价可能随促销或版本更新调整；例如文档 1 示例按目录价计算，实际应付金额以账单为准。

## 来源文档

- [计费说明](../../raw/application-user-guide/agent-billing/sandbox-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/managed-agents-billing.md)
- [计量与计费](../../raw/application-user-guide/agent-billing/pricing.md)
- [知识库计费说明](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)
- [计费说明](../../raw/application-user-guide/agent-billing/billing.md)


