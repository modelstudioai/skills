# agent governance

Agent Governance 是百炼平台面向 AI Agent 全生命周期提供的治理能力集合，涵盖可观测性、可评测性、可优化性与安全性四大支柱。它通过统一的数据标准（如 OpenTelemetry GenAI）、开箱即用的分析工具和策略化防护机制，帮助开发者在开发、上线与运维阶段系统性地保障 Agent 的质量、性能与合规性。核心能力不依赖特定框架，支持 Agent 1.0/2.0、工作流应用等主流形态。

## 支持的模型/功能

- **可观测性**：支持全链路 Trace 可视化（Prompt 解析、模型调用、工具执行、记忆读写），自动捕获耗时、[Token](../concepts/token.md) 消耗、状态与异常；覆盖调用统计、模型分析、工具调用分析、限流统计等维度 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **可评测性**：提供多维自动化评测能力，包括输出质量（准确性、简洁性、合规性）与执行过程（轨迹准确性、工具调用成功率、观察信息增益等）；支持预置评估器（LLM/Code）与自定义评估器 [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **可优化性**：支持基于调试结果、评测任务低分样本或线上 Trace 数据的 Prompt 智能优化，并提供多版本对比与一键采纳功能 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全性**：提供内生安全防护，分为默认防护（自动生效，覆盖输入输出内容安全、RAG 知识库扫描、记忆内容检测等）与高级防护（需开通，含提示词攻击检测、敏感数据外泄检测等 7 类策略）[概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

> **注意**：文档 5 明确指出“应用观测目前暂无 API”，但文档 27 列出了 `/api/v1/agentstudio/security` 下的多个 Security 接口（如 `/overview`, `/asset_summary`）。二者所属模块不同（agenteval vs security），不构成矛盾；但需注意 `agenteval` 观测能力当前仅限控制台使用，无对应 API。

## 关键参数

- **观测配置**：首次使用需授权 OpenTelemetry 服务角色、开通服务并初始化 LogStore（主账号操作）；子账号需主账号预先配置权限 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集字段映射**：创建评测任务时，评估器变量必须与评测集字段或应用输出字段完成映射，且**数据类型必须严格一致**（如轨迹变量须映射到轨迹类型列）；不匹配将导致配置无法保存 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全策略作用域**：所有安全策略配置对**账号下全部 Agent 全局生效**，不区分业务空间；修改前需评估影响范围 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。
- **轨迹数据格式**：轨迹（Trajectory）为 JSON 结构，必须包含 `schema_version`、`session_id`、`trajectory_id`、`steps` 和 `final_metrics` 等核心字段，单条大小 ≤ 1 MB [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。

## 使用方式

- **观测接入**：在控制台「应用观测」页面对已发布应用点击「开启观测」，随后输入测试问题即可生成 Trace；支持按 Request ID/Trace ID 搜索、导出 JSONL/EXCEL、配置告警规则 [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)。
- **评测执行**：先创建并**发布**评测集（草稿不可用），再创建评测任务，关联已发布评测集版本与目标应用，配置评估器及字段映射后发起批量评测 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **Prompt 优化**：在「应用优化」页面选择应用后，可任选路径：
  - *调试反馈*：发送测试问题 → 选择调试结果 → 输入人工反馈 → 生成并采纳优化 Prompt；
  - *评测集/评测任务*：选择已发布的评测集版本或已完成的评测任务 → 勾选样本 → 配置字段映射 → 生成优化 Prompt [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全防护**：默认防护随 Agent 使用对应模块（如 RAG、Memory）自动启用；高级防护需在「Security > 高级防护 > 安全策略」页面完成服务授权后开通，并手动启用所需策略 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

## 限制和注意事项

- **应用支持范围**：应用观测**暂不支持通过 Assistant API 创建的智能体**，仅支持 Agent 1.0、Agent 2.0 和工作流应用 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集版本管理**：评测集最多保存 10 个历史版本，超出后自动覆盖最旧版本；草稿状态的评测集不能用于评测任务 [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)。
- **CLI 与 API 能力边界**：Security CLI（如 `bl agents security overview`）仅支持查询最近 24 小时防护统计与风险告警，**不支持开通/配置防护或发起扫描**；API 同样仅提供查询能力，无写操作接口 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。
- **优化采纳行为**：所有优化路径（调试、评测集、评测任务）的「采纳」操作**仅更新当前编辑中的 Prompt，不会自动发布应用**；发布需在应用管理页面单独操作 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)


