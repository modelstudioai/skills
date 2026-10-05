# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory）自动生效，无需额外开通；高级防护需完成服务授权后启用，当前处于限时免费阶段。安全能力通过「量·发现与盘点—挡·拦截与防护—记·审计与留痕」形成闭环，持续保护提示词、内容、工具调用、知识与记忆等关键资产。

## 支持的模型/功能

百炼安全能力按 Agent 类型与使用场景深度集成，支持以下模块的原生防护：

- **Flow Agent**：输入/输出内容安全检测（含提示词与模型响应）  
- **Managed Agent**：运行时行为安全，包括沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：知识库内容安全，含上传文件预扫描与知识库内容检测  
- **Memory**：记忆读写内容安全检测  
- **Store（MCP/Skill）**：供应链静态扫描、组件依赖风险检测  

> **注意**：文档 5（[防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)）明确说明“如已发起并完成自建内容安全审批，内容安全项将显示为‘关闭’”，但文档 7（[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）和文档 12（[计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）均指出默认防护中的“内容安全”是免费且自动生效的基础能力。该矛盾表明：自建内容安全审批仅影响**界面展示状态**，不实际关闭底层检测逻辑；实际拦截仍由平台默认防护执行。

## 关键参数

| 参数类别 | 说明 | 来源 |
|----------|------|------|
| **防护范围标识** | `Agent 身份签发`为资产盘点与权限管控基础；`防护中 X`/`已自动防护 X 个 Agent`反映模块实际启用状态（见[防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)） | [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md) |
| **高级防护配额** | 每个 Agent 席位每日默认 300 Credits，有效期 24 小时，不可结转；超额部分按 0.0015 元/Credit 计费 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |
| **风险等级** | 高/中/低三级，基于风险置信度与危害程度联合研判；仅开通高级防护后，[风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)页面才产生数据 | [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) |

## 使用方式

- **控制台操作**：  
  - 默认防护：无需配置，Agent 使用 RAG、Memory 等模块后自动启用。入口见 **Security > 默认防护 > 防护总览** 或 **Agent 资产**。  
  - 高级防护：在 **Security > 高级防护 > 安全策略** 页面点击「立即开通」，完成服务授权（自动创建 `AliyunServiceRoleForSFMSecurity` 等角色），默认启用前 6 项策略；`内容安全`策略需手动开启。  

- **CLI 工具**：  
  使用 `bl agents security overview` 查询防护统计与资产分布，`bl agents security alerts --risk-level high` 获取高风险告警列表。所有命令支持 `--help` 查看参数详情（见[使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)）。  

- **API 集成**：  
  Security 模块提供 7 个 RESTful 接口，路径前缀 `/api/v1/agentstudio/security`，覆盖防护总览（`/overview`）、资产摘要（`/asset_summary`）、策略状态（`/policies`）、告警查询（`/agent_logs`）等能力，全部接口返回统一结构 `{"success": true, "data": {...}}`（见[API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)）。

## 限制和注意事项

- **全局策略作用域**：安全策略配置对账号下**全部 Agent 全局生效**，不区分业务空间；修改前须评估跨业务影响（见[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）。  
- **高级防护能力边界**：当前高级防护**仅提供风险监测与告警，不支持自动阻断或拦截**（见[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）；风险处置需人工介入。  
- **资产统计规则**：Flow Agent 仅统计发布态（草稿态不计入），Managed Agent 统计发布态与归档态；外部未纳管 Agent 不出现在资产清单中（见[Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）。  
- **审计日志范围**：风险与审计页面展示**账号下全部 Agent 的数据，不区分业务空间**，且仅在开通高级防护后才有风险事件数据（见[风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）。

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)


