# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory、Managed Agent）自动生效，无需额外接入；高级防护需完成服务授权后开通，当前处于限时免费阶段。安全能力通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」形成闭环，持续保护提示词、内容、工具调用、知识与记忆等关键资产。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景深度集成，支持以下模块的原生防护：

- **Flow Agent**：输入/输出内容安全检测（含提示词攻击识别）  
- **Managed Agent**：运行时行为安全，包括沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：知识库内容安全，含上传文件预扫描、数据投毒检测  
- **Memory**：记忆读写内容安全检测  
- **Store（MCP/Skill）**：供应链静态扫描、组件恶意代码与风险依赖检测  

> **注意**：文档 5（[防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)）明确说明“如已发起并完成自建内容安全审批，内容安全项将显示为‘关闭’”，但文档 13（[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）指出内容安全是高级防护中需手动开启的第 7 项策略。二者逻辑存在不一致：前者暗示内容安全可被外部审批绕过，后者将其列为可开关的策略项。实际行为以控制台策略配置为准，建议优先通过[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)页面统一管理。

## 关键参数

- **防御席位（Seat）**：指一个处于运行状态且启用高级防护的 Agent，按小时计费（0.42 元/席位·小时）  
- **Credit 额度**：每个席位每日默认 300 Credits，有效期 24 小时，不可结转；超额部分按 0.0015 元/Credit 计费  
- **风险等级**：高/中/低三级，由风险置信度与危害程度联合研判生成，用于[风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)筛选与处置优先级判断  
- **Agent 身份标识**：由平台自动签发，是资产盘点、权限管控与审计溯源的基础标识  

## 使用方式

- **默认防护**：无需操作，Agent Studio 中创建或接入 Flow/Managed Agent、RAG、Memory、Store 等模块后自动启用  
- **高级防护开通**：进入控制台 **Security > 高级防护 > 安全策略**，点击「立即开通」，完成服务授权（需创建 `AliyunServiceRoleForSFMSecurity` 等角色）并同意协议  
- **CLI 查询**：使用 `bl agents security overview` 查看防护统计，`bl agents security alerts --risk-level high` 获取高风险告警列表（详见[使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)）  
- **API 集成**：调用 `/api/v1/agentstudio/security/` 下 7 个 REST 接口，如 `GET /overview`、`GET /agent_logs`，支持分页与导出（详见[API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)）  

## 限制和注意事项

- 安全策略配置对账号下**全部 Agent 全局生效**，不区分业务空间；修改前须评估跨业务影响  
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) 页面展示该账号下**所有 Agent 的风险事件**，不按业务空间隔离  
- 默认防护能力（如内容安全、凭证隔离）**免费且自动启用**；高级防护（含 7 项策略与风险监测）当前限时免费，正式计费后按席位+Credit 模式后付费  
- Agent 资产统计仅包含百炼纳管的 **Flow Agent（发布态）与 Managed Agent（发布态/归档态）**，草稿态 Flow Agent 不计入；外部未纳管 Agent 不被识别为资产  
- 所有安全检测均为**异步执行**，防护总览数据约每 2 分钟刷新一次；风险与审计数据延迟通常小于 5 分钟  
- 当前高级防护**不支持自动阻断或拦截风险**，仅提供检测、告警与审计能力，处置需人工介入

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)


