# security guide

百炼平台为 Agent 提供内生、开箱即用的原生安全能力，覆盖开发、运行、数据、记忆与生态全链路。默认防护随 Agent 使用对应模块（如 RAG、Memory、Managed Agent）自动生效，无需额外接入；高级防护则需服务授权后开通，提供策略配置与风险监测能力。整体形成「量·发现与盘点—挡·拦截与防护—记·审计与留痕」的安全闭环。

## 支持的模型/功能

百炼安全能力按 Agent 类型和使用场景差异化覆盖：

- **Flow Agent**：输入输出内容安全检测（含提示词攻击识别）  
- **Managed Agent**：运行时行为安全，包括沙箱隔离、工具调用拦截、凭证隔离与 Session 生命周期治理  
- **RAG**：知识库内容安全，支持上传文件预扫描、数据投毒检测  
- **Memory**：记忆读写内容安全检测  
- **Store（MCP/Skill）**：供应链静态扫描、组件恶意代码与风险依赖检测  

所有防护均基于 Agent 身份签发实现资产绑定与权限管控基础。详细防护范围见 [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)。

> **注意**：文档 7（[安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)）称高级防护“暂不支持自动阻断或拦截风险”，但文档 4（[防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)）明确列出“内容安全 I/O 拦截”“上传文件预扫描拦截”等实时拦截能力。此处矛盾源于功能分层：**默认防护具备自动拦截能力，高级防护当前仅提供风险监测与告警，不触发阻断**。开发者应以默认防护作为基础拦截层，高级防护用于深度分析与审计。

## 关键参数

| 参数类别 | 说明 | 来源 |
|----------|------|------|
| **防护粒度** | 默认防护按模块（Flow/Managed/RAG/Memory/Store）自动启用；高级防护策略全局生效，作用于账号下全部 Agent，不区分业务空间（见 [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)） | [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md) |
| **Credit 消耗** | 高级防护按内容 Token 量换算 Credit，每席位每日默认 300 Credits，超额部分按 0.0015 元/Credit 计费；Credit 有效期 24 小时，不结转 | [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md) |
| **风险等级** | 风险事件按置信度与危害程度联合研判，分为高、中、低三档，影响审计优先级与处置策略 | [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md) |

## 使用方式

### 控制台操作
- **默认防护**：无需开通，Agent 接入对应模块（如发布 RAG 知识库、启用 Memory）后自动激活  
- **高级防护**：在控制台 **Security > 高级防护 > 安全策略** 页面点击「立即开通」，完成服务授权（自动创建 `AliyunServiceRoleForSFMSecurity` 等角色），默认启用前 6 项策略，`内容安全` 需手动开启  

### CLI 查询
通过百炼 CLI 快速获取安全数据：
```bash
bl agents security overview          # 查看防护总览与资产分布
bl agents security alerts --risk-level high  # 查询高风险告警
```
完整命令参考见 [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)。

### API 集成
Security 模块提供 7 个 RESTful 接口，路径前缀 `/api/v1/agentstudio/security`，支持程序化查询与告警导出：
- `/overview`（防护总览）、`/asset_summary`（资产摘要）、`/policies`（策略状态）  
- `/agent_logs`（分页告警列表）、`/agent_logs/{alert_id}`（详情）、`/export_agent_logs`（导出）  
详见 [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)。

## 限制和注意事项

- **资产统计范围**：仅纳管百炼原生或托管的 Flow Agent 与 Managed Agent；外部 Agent 不被自动识别为资产（见 [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)）  
- **策略生效范围**：安全策略配置对账号下全部 Agent 全局生效，修改前须评估跨业务空间影响  
- **数据延迟**：防护总览页面数据约每 2 分钟刷新一次，非实时  
- **自建审批影响**：若已发起并完成自建内容安全审批，控制台「内容安全」项将显示为“关闭”，默认防护能力受限  
- **高级防护能力边界**：当前版本仅支持风险监测与审计，**不支持自动处置**（如阻断工具调用、删除记忆），风险处理需人工介入（见 [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)）  
- **免费期提醒**：高级防护目前处于限时免费阶段，正式计费前平台将至少提前一个月通知（见 [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)）

## 来源文档

- [开始使用](../../raw/application-user-guide/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/security-guide/section-gs/cli.md)
- [防护总览](../../raw/application-user-guide/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/security-guide/section-adv/policy.md)
- [参考](../../raw/application-user-guide/security-guide/section-ref.md)
- [风险与审计](../../raw/application-user-guide/security-guide/section-adv/audit.md)
- [API 参考](../../raw/application-user-guide/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl.md)
- [更新日志](../../raw/application-user-guide/security-guide/section-cl/changelog.md)
- [资产盘点](../../raw/application-user-guide/security-guide/section-assets.md)
- [计费说明](../../raw/application-user-guide/security-guide/section-ref/billing.md)


