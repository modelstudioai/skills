# agent billing

Agent 相关服务的计费采用按需计量、分项结算模式，费用由运行时、模型调用、工具/MCP 调用、知识库、解析与安全等组件独立产生。各组件免费额度仅限抵扣其对应计费项，不跨服务通用。详细计费规则和地域差异请参考 [Agent 计费](../../raw/application-user-guide/agent-billing.md)。

## 支持的模型/功能

- **Managed Agents**：支持全托管式 Agent 运行，计费涵盖会话运行时、所选模型调用、集成工具及 MCP 服务调用。  
- **Flow Agent**：基于可视化编排的轻量级 Agent，仅对模型调用计费；所依赖的知识库与工具费用另计（见 [Flow Agent](../../raw/application-user-guide/agent-billing/flow-agent-billing.md)）。  
- **Sandbox**：提供隔离调试环境，按会话运行时长与数据保留周期计费。  
- **RAG**：知识库按规格（如文档容量、QPS）与关联模型调用分别计费，详见 [RAG](../../raw/application-user-guide/agent-billing/billing-for-knowledge-base.md)。  
- **ParseX**：图文解析按页、音视频按秒计费，与模型无关。  
- **Memory** 和 **Security**：按策略版本或防护等级分项计量，具体规则参见 [Memory](../../raw/application-user-guide/agent-billing/billing.md) 和 [Security](../../raw/application-user-guide/agent-billing/billing.md)。

> **注意**：原始文档中 Memory 和 Security 的计费说明均指向同一路径 `billing.md`，但该文件实际内容未明确区分二者逻辑；建议以控制台最新计费页为准，并关注 [Agent 计费](../../raw/application-user-guide/agent-billing.md) 中的“计费与免费额度”章节更新。

## 关键参数

| 参数 | 说明 | 示例值 |
|------|------|--------|
| `agent_type` | 指定 Agent 类型，影响计费维度 | `"managed"`, `"flow"` |
| `model_id` | 显式声明调用模型，决定模型调用单价 | `"qwen-max"`, `"qwen-plus"` |
| `tool_ids` | 列出启用的工具 ID，每个工具按次/时长单独计费 | `["tavily_search", "calculator"]` |
| `knowledge_base_id` | 若启用 RAG，知识库 ID 触发对应规格费用 | `"kb-xxx"` |
| `session_ttl_seconds` | Sandbox 或 Managed Agent 会话存活时长，影响运行时计费 | `3600` |

## 使用方式

1. 创建 Agent 时，在配置中显式指定 `model_id` 和所需 `tool_ids`；未指定则使用平台默认模型（按默认单价计费）。  
2. Flow Agent 中若引用知识库节点，系统自动关联 `knowledge_base_id` 并触发 RAG 计费项。  
3. Sandbox 启动后即开始计算运行时，关闭或超时自动终止计费。  
4. 所有调用均通过 `/v1/agents/{id}/run` 接口发起，账单按实际请求上下文拆分至对应计费项——此行为在 [Agent 计费](../../raw/application-user-guide/agent-billing.md) 中明确定义。

## 限制和注意事项

- 免费额度不可跨服务转移：例如 Flow Agent 的模型调用免费额度不能用于抵扣 Managed Agents 的运行时费用。  
- 组合使用多个组件（如 Flow + RAG + Tool）时，各组件费用独立生成账单，不合并折扣。  
- ParseX 解析结果若被后续模型调用复用，不重复计费解析费用，但模型调用仍单独计费。  
- 地域价格差异生效于资源创建时所在 Region，跨 Region 调用不触发额外传输费，但可能因模型部署地不同导致延迟与计费归属变化（参见 [模型计费](../../raw/model-user-guide/test-1/model-pricing.md)）。

## 来源文档

- [Agent 计费](../../raw/application-user-guide/agent-billing.md)


