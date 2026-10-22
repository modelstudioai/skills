# agent governance

Agent Governance 是百炼平台面向 AI Agent 全生命周期提供的核心治理能力体系，涵盖可观测性、可评测性、可优化性与安全性四大支柱。它通过统一的数据标准（OpenTelemetry GenAI）、开箱即用的分析工具和策略化防护机制，帮助开发者在开发、测试、上线与运维各阶段实现对 Agent 行为、质量与风险的精细化管控。

## 支持的模型/功能

Agent Governance 当前覆盖两类核心能力模块：

- **Evolution（智能体治理平台）**：提供全链路观测、多维自动化评测、Prompt 智能优化三大能力，支持智能体应用（Agent 1.0 / 2.0）和工作流应用；[应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)支持 Trace 数据分钟级同步，[评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)支持 LLM/Code 双引擎评估器组合使用；轨迹（Trajectory）作为一级数据类型，被深度集成于观测、评测集构建与轨迹评估器中，详见[添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
  
- **Security（内生安全防护）**：提供默认防护（自动生效）与高级防护（按需开通）双层机制，覆盖 Flow Agent、Managed Agent、RAG、Memory、Store 五大模块，支持资产盘点、风险拦截与审计留痕闭环。默认防护无需配置，高级防护当前处于限时免费阶段，计费规则见[计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)。

> **注意**：文档中提及“应用观测目前暂无 API”（见[应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)），但 Security 模块明确提供 7 个 RESTful API（如 `/api/v1/agentstudio/security/overview`），且 Evolution 的评测、标签等能力虽未在原始文档中声明 API，但其控制台操作已具备完整 CLI 支持（如 `bl agents security overview`）。因此，“暂无 API”仅特指应用观测模块的**数据导出与查询接口**，不表示整个 Agent Governance 体系缺乏程序化接入能力。

## 关键参数

| 功能域 | 参数/配置项 | 说明 | 约束/默认值 |
|--------|-------------|------|-------------|
| **观测** | Trace 保留时长 | 应用观测中 Trace 数据可查询的最大时间范围 | 最长 30 天（见[应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)） |
| **评测** | 评测集版本上限 | 单个评测集最多保存的历史版本数 | 10 个（见[创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)） |
| **评测** | 评估器数量上限 | 单个评测任务最多可配置的评估器数量 | 10 个（见[评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)） |
| **安全** | Credit 额度 | 每个高级防护席位每日默认配额 | 300 Credits/席位/日（见[计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)） |
| **安全** | 安全策略生效范围 | 高级防护策略的配置作用域 | 全局生效（账号级），不区分业务空间（见[安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)） |

## 使用方式

- **接入准备**：Evolution 依赖 OpenTelemetry GenAI 标准，任意框架均可快速接入；Security 默认防护随 Agent 使用自动生效（如启用 RAG 则知识库内容安全自动开启），高级防护需主账号完成服务授权（角色 `AliyunServiceRoleForSFMSecurity` 等）。
- **核心流程**：
  1. **观测**：在控制台开启应用观测 → 查看 Trace 列表与监控统计 → 基于 Trace 导出数据或一键添加至评测集；
  2. **评测**：创建评测集（支持空建、文件上传、Trace 回流）→ 配置评估器（预置或自定义 LLM/Code）→ 发起评测任务 → 分析得分分布与回归对比；
  3. **优化**：通过多版本 Prompt 对比调试、基于调试反馈生成优化建议、或基于优质评测集/评测任务结果发起智能优化任务；
  4. **安全**：在 Security 控制台查看防护总览与 Agent 资产 → 按需开通高级防护并启用策略（如提示词攻击检测）→ 在风险与审计页排查高风险事件。
- **CLI 支持**：Security 提供 `bl agents security overview` 和 `bl agents security alerts` 等命令，便于自动化集成与巡检（见[使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)）。

## 限制和注意事项

- **功能限制**：应用观测**暂不支持通过 Assistant API 创建的智能体应用**（见[应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)）；评测集字段映射要求严格匹配数据类型，类型不一致将导致导入失败（同上文档及[评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)）；单条轨迹 JSON 大小不可超过 1 MB（见[添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)）。
- **权限与范围**：Security 高级防护策略配置为**账号全局生效**，修改前须评估对全部 Agent 的影响；应用观测配置（如 OpenTelemetry 角色授权）需主账号操作，子账号需被授予必要权限（见[应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)）。
- **数据时效性**：应用观测的监控指标更新频率为**分钟级**；防护总览页面数据约每 2 分钟刷新一次（见[防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)）。
- **成本提示**：评测任务调用大模型产生的 [Token](../concepts/token.md) 费用正常计费；高级防护正式计费后采用“席位费 + 超额 Credit”模式，当前为限时免费（见[计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)）。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agent-governance/agenteval/agenteval-changelog.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/agent-governance/security-guide/changelog.md)


