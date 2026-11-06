# 安全过滤

安全过滤是百炼平台在模型调用与 Agent 执行全链路中，对输入（Prompt、用户消息、知识库内容、工具参数等）和输出（模型回复、工具返回、记忆写入、RAG 检索结果等）实施的实时、多维度内容风险识别与拦截机制。它不是单一功能模块，而是由默认防护层与可配置高级防护层共同构成的内生式安全护栏，覆盖违法信息、敏感词、价值观偏差、提示词攻击、RAG 投毒、敏感数据外泄等典型风险场景。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型 API 调用场景**：  
  通过 `enable_content_safety=true`（默认启用）触发输入/输出双端内容安全过滤；配合 `compliance_mode=strict` 可提升拦截灵敏度（延迟增加 50–200ms）。该过滤自动生效于所有托管模型（Qwen 系列及微调模型），无需额外集成。

- **AI Agent 场景**：  
  - *默认防护*：随 Agent 功能模块自动启用——RAG 知识库扫描（防投毒）、Memory 内容检测（防越权读写）、工具输入参数校验（防命令注入）均内置安全过滤逻辑；  
  - *高级防护*：需在控制台开通「安全高级防护」服务后，手动启用 `prompt_attack`、`rag_poisoning`、`pii_leakage` 等共 11 类策略，策略全局生效于账号下所有 Agent。

- **Security API 数据治理场景**：  
  安全过滤的执行结果（拦截事件、风险类型、原始上下文、拦截话术）统一沉淀为结构化告警数据，可通过 `/api/v1/agentstudio/security/agent_logs` 查询或 `/api/v1/agentstudio/security/export_agent_logs` 导出，用于审计、复盘与策略调优。

- **计费场景**：  
  高级防护产生的安全过滤行为按消耗 Credits 计费（1 Credit ≈ 100 [Token](token.md) 的检测开销），每个防护席位每日含 300 Credits 免费额度；超限后按 0.0015 元/Credit 结算，费用独立于模型、工具等其他计费项。

## 关键参数和配置

| 参数 | 位置 | 类型 | 说明 | 默认值 |
|------|------|------|------|--------|
| `enable_content_safety` | 请求 Body（模型 API） | boolean | 控制是否启用基础内容安全过滤（输入+输出） | `true` |
| `compliance_mode` | 请求 Body（模型 API） | string | 合规模式：`standard`（平衡体验与安全）、`strict`（高敏感场景，增强拦截） | `standard` |
| `risk_level` | Query（Security API） | string | 告警筛选：`high` / `medium` / `low`，用于聚焦高危过滤事件 | — |
| `status_list` | Query（Security API） | array | 告警状态筛选：如 `["intercepted", "unhandled"]`，精准定位被拦截样本 | — |
| `asset_type` | Response（Security API） | string | 标识触发过滤的资产类型：`agent` / `tool` / `skill` / `knowledge_base` / `memory` / `channel` | — |

> ⚠️ 注意：  
> - 安全过滤规则库不可自定义，仅支持通过 `compliance_mode` 调节阈值；  
> - 高级防护策略（如 `prompt_attack`）需先完成服务授权并开通，否则配置不生效；  
> - 所有安全过滤操作均不降低模型 SLA，但 `strict` 模式会引入确定性延迟增量。

## 面向开发者，简洁实用

- ✅ **快速启用**：模型调用时显式传 `{"enable_content_safety": true}`，即可获得基础防护；Agent 开发者无需修改代码，高级防护在控制台一键开通即生效。  
- ✅ **精准排查**：用 Security API 拉取 `risk_level=high&status_list=["intercepted"]` 的告警，结合 `original_prompt` 和 `blocked_response` 字段快速定位误拦/漏拦原因。  
- ✅ **成本可控**：监控 `/security/overview` 中 `credits_used_today` 指标，结合 `current_credits_quota` 判断是否临近额度上限，及时调整策略启用范围或升级席位。  
- ❌ **避免踩坑**：不要尝试绕过过滤（如 Base64 编码敏感内容），平台会对常见混淆手段做二次检测；也不要依赖 `app` 类型字段（已废弃），`asset_type` 仅接受文档明确定义的 6 种值。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [agent governance](../guides/agent-governance.md)
- [agent billing](../guides/agent-billing.md)


