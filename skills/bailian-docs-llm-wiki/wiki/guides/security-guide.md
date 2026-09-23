# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory、Managed Agent）自动生效，无需额外接入；高级防护需完成服务授权后开通，当前处于限时免费阶段。安全能力通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」闭环实现资产可视、风险可控、行为可溯。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景深度集成，支持以下模块的原生防护：

- **Flow Agent**：输入/输出内容安全检测（含提示词、模型响应）  
- **Managed Agent**：运行时沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：上传文件预扫描、知识库内容安全检测（含数据投毒识别）  
- **Memory**：记忆读写内容安全检测  
- **Store（MCP/Skill）**：Skill 组件供应链静态扫描（恶意代码、风险依赖检测）  

> **注意**：文档 4 中明确说明“如已发起并完成自建内容安全审批，内容安全项将显示为‘关闭’”，而文档 14 的策略列表仍将“内容安全”列为可手动开启的高级策略之一。二者逻辑存在冲突——默认防护已包含基础内容安全，但高级策略中又将其作为独立可选能力。实际使用中应以控制台实时状态为准，建议优先参考 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md) 页面的启用状态。

## 关键参数

- **防护粒度**：默认防护按模块（Flow/RAG/Memory 等）自动激活；高级防护策略全局生效，作用于账号下全部 Agent，不区分业务空间（见 [概述](../../raw/application-user-guide/security-guide/section-gs/security.md)）。  
- **Credit 消耗**：高级防护中内容检测按 [Token](../concepts/token.md) 换算 Credit，每席位每日默认 300 Credits，超量部分按 0.0015 元/Credit 计费（见 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）。  
- **风险等级**：风险事件分为高、中、低三级，由置信度与危害程度联合研判生成，用于 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 页面筛选与处置优先级判断。

## 使用方式

- **控制台操作**：  
  - 默认防护：无需配置，Agent 接入对应模块（如绑定知识库）后自动启用。  
  - 高级防护：进入 **Security > 高级防护 > 安全策略**，点击「立即开通」完成服务授权（自动创建 AliyunServiceRoleForSFMSecurity 等角色），默认启用前 6 项策略，“内容安全”需手动开启。  
- **CLI 工具**：安装百炼 CLI 后，执行 `bl agents security overview` 查询防护统计，`bl agents security alerts --risk-level high` 获取高风险告警（见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)）。  
- **API 集成**：调用 `/api/v1/agentstudio/security` 下的 7 个接口，如 `GET /overview`（防护总览）、`GET /agent_logs`（分页告警列表）、`POST /export_agent_logs`（导出告警）等（见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)）。

## 限制和注意事项

- **资产统计范围**：仅纳管百炼原生或托管的 Flow Agent 与 Managed Agent；外部 Agent 不被自动识别为资产（见 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）。  
- **审计数据范围**：[风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 页面展示账号级全部 Agent 数据，**不区分业务空间**；而 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md) 和 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md) 均按业务空间维度组织。  
- **处置能力限制**：当前高级防护仅提供风险监测与告警，**不支持自动阻断或拦截**（见 [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)），所有风险需人工确认处理或忽略。  
- **时效性**：防护总览页面数据约每 2 分钟刷新一次；Credit 额度按自然日重置，有效期 24 小时，不结转。

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/security.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)


