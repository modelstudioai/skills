# 内容安全过滤

内容安全过滤是百炼平台在模型输入（prompt）与输出（completion）环节自动执行的多模态风险识别与拦截机制，基于关键词匹配、敏感实体识别、图像鉴黄等策略，实时阻断涉政、暴恐、色情、违禁、违法等违规内容的生成与传播。

## 在百炼平台的不同场景中，这个概念如何使用

- **模型 API 调用**：所有百炼托管模型（含 Qwen 系列及第三方接入模型）默认启用内容安全过滤。开发者可通过请求参数 `enable_content_safety=false` 临时关闭（仅限非高危业务场景），但平台级基础策略（如涉政、暴恐类实时拦截）仍强制生效，不可绕过。
- **Agent 应用运行时**：在 Agent 编排链路中，内容安全过滤作用于用户输入、模型生成回复、插件返回结果、知识库检索片段等全部文本/图像输出节点，确保端到端响应合规；相关拦截事件会统一上报至 Security API 的告警系统，`asset_type="agent"` 且 `policy_code="content_safety"`。
- **Security API 管理**：通过 `/api/v1/agentstudio/security/overview` 可查看最近 24 小时内容安全模块的拦截统计（如拦截次数、高危类型分布）；通过 `/api/v1/agentstudio/security/agent_logs?policy_code=content_safety` 可筛选并导出全部内容安全相关告警，用于审计与复盘。
- **合规备案流程**：内容安全过滤日志（含脱敏后的触发上下文与拦截原因）是 AI 应用完成《生成式人工智能服务管理暂行办法》备案的必要佐证材料之一，需配合 `audit_log_enabled=true` 开启完整审计日志。

## 关键参数和配置

| 参数名 | 类型 | 默认值 | 说明 |
|--------|------|--------|------|
| `enable_content_safety` | boolean | `true` | 控制是否启用应用层内容安全过滤（开关粒度为单次 API 请求或 Agent 实例）。设为 `false` 后，仅豁免关键词/实体类策略，不豁免平台强管控策略。 |
| `audit_log_enabled` | boolean | `false` | 开启后，内容安全拦截事件将记录完整审计日志（含 request_id、触发时间、原始输入片段、拦截策略 ID、风险等级），日志保留 90 天。需配合 RAM 权限 `bailian:ListAuditLogs` 使用。 |

> ⚠️ 注意：  
> - `enable_content_safety` 仅支持在模型调用请求体（JSON）或 Agent 配置中传入，**不支持通过 URL Query 或 Header 设置**；  
> - 关闭该开关不降低平台安全责任，因监管要求的强制拦截策略始终在线；  
> - 安全告警中的 `risk_level` 字段取值为 `"low"` / `"medium"` / `"high"` / `"critical"`，对应不同策略严重程度，可用于自动化分级响应。

## 面向开发者，简洁实用

- ✅ **推荐做法**：生产环境保持 `enable_content_safety=true`，结合 Security API 告警接口建立实时监控看板，对 `risk_level=high` 以上告警设置企业微信/钉钉告警；  
- ✅ **调试技巧**：本地测试时若需快速验证 prompt 是否被拦截，可调用 `/api/v1/agentstudio/security/overview` 查看“今日拦截数”突增，并立即查 `/agent_logs?policy_code=content_safety&status=unhandled` 获取详情；  
- ❌ **避免踩坑**：不要依赖关闭 `enable_content_safety` 来“绕过审核”——这既违反服务协议，也无法规避平台级强策略，反而导致审计日志缺失，影响合规验收；  
- 🛠️ **集成提示**：若需自定义响应（如拦截后返回友好提示语而非空响应），应在应用层监听 `error.code === "ContentSafetyBlocked"` 类错误（SDK v2.3+ 已支持），而非修改过滤逻辑。

## 关联主题页

- [security api guide](../api/security-api-guide.md)
- [security and compliance](../guides/security-and-compliance.md)
- [application support](../guides/application-support.md)
- [preparations](../api/preparations.md)


