# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的治理能力集合，涵盖可观测性、可评测性、可优化性与安全性四大支柱。它通过统一的数据标准（如 OpenTelemetry GenAI）、开箱即用的分析工具和策略化防护机制，帮助开发者在开发、上线与运维阶段系统性地保障 Agent 的质量、稳定性与合规性。核心能力围绕 Evolution（观测/评测/优化）与 Security（资产/策略/审计）两大子系统展开。

## 支持的模型/功能

- **Evolution**：提供全链路可观测性（Trace、监控、限流）、多维自动化评测（含轨迹评测）、基于调试/评测/线上反馈的 Prompt 智能优化闭环。支持 Agent 1.0、Agent 2.0 和工作流应用，但[暂不支持通过 Assistant API 创建的智能体](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **Security**：提供内生安全防护，覆盖内容安全（I/O 检测）、运行时行为安全（沙箱隔离、工具调用拦截）、知识库与记忆安全、Skill 供应链扫描等。默认防护随模块使用自动生效；高级防护（如提示词攻击检测、敏感数据外泄检测）需开通服务并全局配置，当前处于限时免费阶段 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

> **注意**：文档中多次提及“应用观测目前暂无 API”，但 Security 模块明确提供了 7 个 RESTful API（如 `/api/v1/agentstudio/security/overview`），用于查询防护总览、资产、策略与告警 [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)。二者能力边界需区分：Evolution 当前仅提供控制台交互能力，Security 则同时支持控制台与 API。

## 关键参数

- **观测类**：`QPM`（每分钟请求数）、`TTFT`（首 Token 延迟）、`total_prompt_tokens`/`total_completion_tokens`、`duration_ms`（Span 耗时）、`status`（Span 状态码）。
- **评测类**：
  - 评测集字段映射：必须保证 `评测集字段` 与 `评估器变量` 的数据类型一致（如 `trajectory` 类型变量须映射到 `trajectory` 类型列）[评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)；
  - 评估器参数：LLM 评估器需配置 `评分范围`（如 0–100）与 `通过阈值`；Code 评估器需确保入参类型与评测集字段严格匹配。
- **安全类**：风险等级（高/中/低）、防护节点类型（Agent/模型/工具/知识库/记忆等）、策略启用状态（如 `提示词攻击`、`RAG 数据投毒`）。

## 使用方式

1. **接入观测**：在应用观测页面点击**应用观测配置**，授权 OpenTelemetry 服务角色、开通服务、初始化 LogStore（主账号操作）；对已发布应用点击**开启观测**，输入测试问题触发 Trace 上报 [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)。
2. **发起评测**：先创建并[发布评测集](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)（草稿不可用），再创建评测任务，关联已发布版本与评估器，并完成变量映射。
3. **执行优化**：支持三种路径——多版本 Prompt 对比调试、基于单条/多条调试结果+人工反馈生成优化建议、基于评测集或已完成的评测任务（优选低分样本）定向优化。
4. **配置安全**：默认防护无需操作；高级防护需在 **Security > 高级防护 > 安全策略** 页面开通服务并启用具体策略；风险与审计数据在开通后自动汇聚，支持按等级、节点类型筛选分析。

## 限制和注意事项

- **观测限制**：仅支持 Agent 1.0、Agent 2.0 和工作流应用；不支持 Assistant API 创建的智能体；Trace 数据同步延迟为分钟级；导出数据最大支持 30 天范围。
- **评测限制**：评测集最多保存 10 个版本；单个评测任务最多添加 10 个评估器；轨迹数据单条大小不能超过 1 MB；评测任务创建后配置不可修改（应用、评测集、评估器映射均锁定）。
- **安全限制**：安全策略配置对账号下**全部 Agent 全局生效**，不区分业务空间 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)；风险与审计页面展示该账号下**全部 Agent** 的数据，暂不区分业务空间 [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)；CLI 查询（如 `bl agents security overview`）固定返回最近 24 小时数据，且结果为空不等于资产安全 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。
- **通用注意事项**：所有字段映射（评测集→评估器、Trace→评测集、评测集→优化任务）均要求数据类型严格一致，否则导入/配置失败；采纳优化结果仅更新当前编辑中的 Prompt，**不会自动发布应用**。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)


