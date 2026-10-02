# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory）自动生效，无需额外接入；高级防护则需服务授权后开通，提供可配置的策略与风险监测能力。整体形成「量 → 挡 → 记」的安全闭环：通过资产盘点发现攻击面、默认与高级策略实现风险拦截、审计日志支持回溯分析。

## 支持的模型/功能

- **默认防护**：面向所有百炼 Agent 自动启用，覆盖 Flow Agent（输入输出内容安全）、Managed Agent（[沙箱](../concepts/sandbox.md)隔离、工具调用拦截、凭证隔离）、RAG（知识库内容预扫描与检测）、Memory（记忆读写内容安全）、Store（MCP/Skill 供应链静态扫描）等模块。详见 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)。
- **高级防护**：提供 7 项可按需启用的策略，包括提示词攻击、敏感数据外泄、工具调用安全、RAG 数据投毒、知识库与记忆窃取、身份与安全凭证、内容安全。其中前 6 项默认开通，**内容安全策略需手动开启**；当前高级防护仅支持风险监测与告警，**不支持自动阻断**（见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）。
- **Agent 类型支持**：Flow Agent（草稿态+发布态，仅统计发布态）与 Managed Agent（发布态+归档态）均被纳管；外部未接入百炼纳管的 Agent 不在资产盘点与防护范围内（见 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）。

> **注意**：文档 7 明确说明“当前高级防护主要支持策略配置与风险监测，暂不支持自动阻断或拦截风险”，但文档 2 中“挡 · 拦截与防护”描述为“默认防护实时拦截风险；高级防护提供策略配置与风险监测”，二者对高级防护是否具备拦截能力表述存在隐含矛盾。实际能力以文档 7 为准——高级防护目前仅监测告警，拦截动作由默认防护承担。

## 关键参数

- **Credit 消耗规则**：高级防护按内容 [Token](../concepts/token.md) 数量换算 Credit，每席位每日默认额度 300 Credits，有效期 24 小时（自然日），不结转；超额部分按 0.0015 元/Credit 计费（见 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）。
- **防御席位**：指“处于运行中且使用了高级防护的 Agent”，仅运行时计费（0.42 元/席位·小时），停用即停止计费。
- **风险等级**：分为高、中、低三档，由风险置信度与危害程度联合研判确定，影响风险列表筛选与优先级排序（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）。

## 使用方式

- **控制台操作**：
  - 默认防护：无需开通，Agent 使用对应模块（如接入知识库）后自动生效。
  - 高级防护：在控制台 **Security > 高级防护 > 安全策略** 页面点击“立即开通”，完成服务授权（自动创建 `AliyunServiceRoleForSFMSecurity` 等角色）后启用。
- **CLI 工具**：
  - `bl agents security overview`：查询防护统计与资产分布；
  - `bl agents security alerts --risk-level high`：按风险等级筛选告警（见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)）。
- **API 接入**：
  - 所有 Security API 均以 `/api/v1/agentstudio/security` 为前缀，共 7 个接口，包括 `/overview`（防护总览）、`/asset_summary`（资产摘要）、`/policies`（策略状态）、`/agent_logs`（告警列表）等（见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)）。

## 限制和注意事项

- **全局生效范围**：安全策略配置对账号下全部 Agent 全局生效，**不区分业务空间**；修改前须评估影响范围（见 [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)）。
- **数据隔离限制**：风险与审计页面展示该账号下**全部 Agent 的风险及日志详情，暂不区分业务空间**；Agent 资产页面也仅按业务空间维度展示，但不支持下钻查看具体 Agent 列表与节点详情（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 和 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）。
- **免费阶段与计费**：高级防护当前处于**限时免费阶段（截至 2026 年 9 月）**，正式计费后将按席位+Credit 超额用量组合计费；默认防护始终免费（见 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）。
- **能力边界**：高级防护不提供自动处置能力，风险事件需人工处理或忽略；审计日志仅支持查看、搜索与导出，不支持自动响应（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）。

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
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


