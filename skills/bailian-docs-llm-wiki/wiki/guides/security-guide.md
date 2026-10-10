# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、托管与数据使用全生命周期。默认防护随 Agent 使用对应模块（如 RAG、Memory）自动生效，无需额外接入；高级防护则提供可配置的策略与风险监测能力，当前处于限时免费阶段。安全体系围绕「量 → 挡 → 记」闭环设计，即资产盘点、风险拦截与审计留痕。

## 支持的模型/功能

- **默认防护**：面向所有百炼 Agent 自动启用，覆盖 Flow Agent（输入输出内容安全）、Managed Agent（沙箱隔离、工具调用拦截、凭证隔离）、RAG（知识库内容安全）、Memory（记忆读写安全）、Store（MCP/Skill 供应链静态扫描）等模块 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)。
- **高级防护**：需完成服务授权后开通，提供 7 项可按需启用的安全策略：提示词攻击、敏感数据外泄、工具调用安全、RAG 数据投毒、知识库与记忆窃取、身份与安全凭证、内容安全 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)。
- **Agent 类型支持**：当前纳管 Flow Agent（草稿态 + 发布态，仅统计发布态）和 Managed Agent（发布态 + 归档态），不支持外部未接入百炼纳管的 Agent [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)。

> **注意**：文档 7 明确说明“当前高级防护主要支持策略配置与风险监测，暂不支持自动阻断或拦截风险”，而文档 2 描述高级防护为“拦截与防护”，存在表述矛盾。实际能力以文档 7 为准：高级防护不执行实时阻断，仅检测与告警。

## 关键参数

- **防御席位**：每个处于运行中且启用高级防护的 Agent 即计为一个席位，按小时计费（正式计费后单价 0.42 元/席位·小时）[计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)。
- **Credit 额度**：每个席位每日默认 300 Credits，有效期 24 小时，不可结转；Credit 消耗与被检测内容 [Token](../concepts/token.md) 数量正相关。
- **风险等级**：分为高、中、低三档，由风险置信度与危害程度联合研判得出，影响风险列表筛选与优先级判断 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)。

## 使用方式

- **控制台操作**：
  - 默认防护：无需操作，Agent 使用 RAG、Memory 等模块后自动启用。
  - 高级防护开通：导航至 **Security > 高级防护 > 安全策略**，点击“立即开通”，完成服务授权（需创建 `AliyunServiceRoleForSFMSecurity` 等角色）。
  - 查看资产：**Security > 默认防护 > Agent 资产**，查看当前业务空间内 Agent 及其关联模型、工具、知识库等资源。
- **CLI 工具**：
  - `bl agents security overview`：查询防护统计与资产分布；
  - `bl agents security alerts --risk-level high`：筛选高风险告警；
  - 所有命令支持 `--help` 查看完整参数 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。
- **API 接入**：
  - 接口前缀 `/api/v1/agentstudio/security`，共 7 个接口，包括 `/overview`（防护总览）、`/asset_summary`（资产摘要）、`/policies`（策略状态）、`/agent_logs`（告警列表）等，全部返回统一结构 `{"success": true, "data": {...}}` [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)。

## 限制和注意事项

- **作用域限制**：安全策略配置对账号下全部 Agent **全局生效**，不区分业务空间；风险与审计页面也展示该账号下全部 Agent 的数据，无业务空间隔离 [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)。
- **功能限制**：
  - 当前版本不支持从 Agent 资产页面下钻查看具体 Agent 列表与节点详情；
  - 风险与审计模块仅提供查看、分析与证据导出能力，**不支持自动处置风险**；
  - 高级防护暂不支持自动阻断，仅提供检测与告警（见前述注意）。
- **开通前提**：开通高级防护需同意《百炼 Agent 安全（按量付费）服务协议》及《百炼安全服务关联角色授权》，系统将自动创建多个服务关联角色（如 `AliyunServiceRoleForSasAI`）。
- **数据时效性**：防护总览页面数据约每 2 分钟刷新一次；风险事件统计基于最近一年数据，Credit 有效期严格按自然日 24 小时计算，到期清零。

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)


