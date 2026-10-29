# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的核心治理能力体系，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大支柱，并集成原生安全防护（Security）。它基于 OpenTelemetry GenAI 标准实现框架中立接入，支持从开发调试、线上运行到持续迭代的闭环治理，帮助开发者系统性提升 Agent 的稳定性、质量与安全性。

## 支持的模型/功能

- **观测能力**：支持智能体应用（Agent 1.0 和 Agent 2.0）及工作流应用的全链路追踪，覆盖 Prompt 解析、大模型调用（含 TTFT、[Token](../concepts/token.md) 消耗）、工具执行（MCP/自定义 API）、向量检索、记忆读写等环节；但**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持文本级（如准确性、合规性）、轨迹级（Trajectory）和多模态（暂未上线）评测。预置评估器覆盖 LLM 与 Code 类型，包括「轨迹准确性」「动作循环检测（ATIF）」「回答忠实度（ATIF）」等 9+ 种轨迹评估器 [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：提供 Prompt 多版本对比调试、基于调试反馈的智能优化、以及基于评测集/评测任务的定向优化三种路径，所有优化结果均需人工审核后手动采纳至编辑区，**不会自动发布应用** [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全能力**：默认防护随 Agent 使用自动生效（免费），覆盖输入输出内容安全、RAG 知识库扫描、Memory 内容检测等；高级防护含 7 项可配置策略（如提示词攻击、敏感数据外泄），当前处于限时免费阶段，需服务授权开通 [Security](../../raw/application-user-guide/agent-governance/security-guide.md)。

> **注意**：文档中关于“应用观测目前暂无 API”的表述与 Security 模块明确提供 `/api/v1/agentstudio/security` 系列 API 形成事实矛盾。实际观测能力虽暂未开放 REST API，但可通过 CLI（如 `bl agents security overview`）和控制台完成关键数据查询 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

## 关键参数

| 参数类别 | 关键参数 | 说明 |
|----------|----------|------|
| **观测** | `Trace ID` / `Span ID` / `Request ID` | 用于精准检索单条调用链；Trace 数据导出支持 JSONL 或 EXCEL 格式 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md) |
| **评测** | `trajectory` 字段（数据类型为 `轨迹`） | 轨迹评测集必需字段，结构需符合 ATIF-v1.8 规范，单条大小 ≤ 1 MB [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md) |
| **安全** | `Credit` 额度 | 高级防护计费单元，每个席位每日默认 300 Credits，超量部分按 0.0015 元/Credit 计费；额度按自然日重置，不结转 [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md) |

## 使用方式

1. **接入准备**：主账号需授权 OpenTelemetry 服务角色并开通可观测链路服务（分钟级生效）；安全能力无需额外开通，默认防护自动启用。
2. **观测启用**：在控制台「应用观测」页面选择目标应用 → 点击「开启观测」→ 所有后续调用将自动追踪（分钟级同步）。
3. **评测构建**：
   - 创建评测集（支持空建或文件上传），场景选「轨迹」时系统自动生成 `input`/`reference_output`/`trajectory` 三列；
   - 选用预置评估器（如「轨迹准确性」）或自定义 LLM 评估器，确保变量映射与评测集字段类型一致；
   - 发起评测任务，关联已发布评测集与应用，最多支持 10 个评估器组合 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
4. **优化执行**：在「应用优化」页面选择调试模式（对比/反馈/评测集），输入问题或选择 Trace 数据 → 系统生成优化建议 → **人工确认后点击「采纳」写入 Prompt 编辑区**（不自动发布）。
5. **安全配置**：高级防护需在「Security > 高级防护 > 安全策略」完成服务授权；策略全局生效，修改前须评估对账号下全部 Agent 的影响。

## 限制和注意事项

- **观测限制**：应用观测数据最长保留 30 天；关闭观测后历史数据停止同步，重新开启仅同步新增数据；限流统计更新频率为分钟级。
- **评测限制**：评测任务创建后不可修改应用、评测集等核心配置；轨迹字段必须为合法 JSON 对象；单个评测集文件上传最大 20 MB；草稿状态评测集不可用于评测任务 [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)。
- **安全限制**：高级防护风险事件需开通后才产生数据；当前风险与审计模块仅支持查看与导出，**不支持自动处置**；安全策略配置对账号下全部 Agent 全局生效，不区分业务空间 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。
- **通用注意事项**：所有优化操作（含版本对比、调试反馈、评测集优化）均**仅更新当前编辑中的 Prompt，不会触发自动发布**；标签类型（分类/布尔/数字/文本）需在创建时明确定义，后续不可修改数据类型；轨迹评测依赖严格的数据结构，字段映射错误将导致评估失败。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agent-governance/agenteval/agenteval-changelog.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/agent-governance/security-guide/changelog.md)


