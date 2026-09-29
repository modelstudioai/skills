# 概述

Security 为 Agent 提供内生的安全防护能力。

阿里云百炼为 Agent 提供安全内生、开箱即用的原生安全能力。安全能力与平台深度融合，Agent 上线即可获得默认防护，无需额外接入或改造；基础防护默认生效，高级防护可按需启用。

同时覆盖 Agent 开发、运行、托管与数据使用过程，通过资产盘点、风险拦截和审计留痕形成「量 → 挡 → 记」的安全闭环，持续保护提示词、内容、工具调用、知识与记忆等关键环节。

支柱

说明

对应功能

**量 · 发现与盘点**

全面盘点 Agent 关联的全部资产，掌握攻击面

[Agent 资产](raw/application-user-guide/security-guide/section-assets/assets.md)

**挡 · 拦截与防护**

默认防护实时拦截风险；高级防护提供策略配置与风险监测

[安全策略](raw/application-user-guide/security-guide/section-adv/policy.md)

**记 · 审计与留痕**

记录风险事件与操作日志，支持风险回溯

[风险与审计](raw/application-user-guide/security-guide/section-adv/audit.md)

## 使用须知

-   默认防护为百炼原生能力，使用百炼 Agent Studio 即自动获得，无需额外开通。
-   防护在 Agent 使用对应模块后自动生效。例如，Agent 接入 RAG 知识库后，知识库内容安全防护自动启用。
-   高级防护需完成服务授权后开通，当前处于限时免费阶段，计费规则参见[计费说明](raw/application-user-guide/security-guide/section-ref/billing.md)。
-   安全策略配置对账号下全部 Agent 全局生效，不区分业务空间。

## 下一步

-   [防护总览](raw/application-user-guide/security-guide/section-assets/overview.md)：查看防护全景与拦截统计
-   [Agent 资产](raw/application-user-guide/security-guide/section-assets/assets.md)：盘点 Agent 关联的全部资产
-   [安全策略](raw/application-user-guide/security-guide/section-adv/policy.md)：按需启用高级防护策略
-   [风险与审计](raw/application-user-guide/security-guide/section-adv/audit.md)：查看风险事件与审计日志
