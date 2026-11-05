# agent governance

Agent Governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力集合，涵盖可观测性、质量评测、智能优化与内生安全四大支柱。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现即插即用，支持从开发调试、线上运行到持续迭代的闭环管理。核心目标是让 Agent 的行为可追溯、质量可量化、问题可定位、风险可防控。

## 支持的模型/功能

Agent Governance 当前覆盖两类核心能力体系：

- **Evolution（全链路治理平台）**：提供应用观测、应用评测、应用优化三大功能模块，完整支撑 Agent 从调试、评估到优化的闭环。支持 Agent 1.0、Agent 2.0 和工作流应用，但**暂不支持通过 Assistant API 创建的智能体** [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。  
- **Security（内生安全防护）**：提供默认防护与高级防护双层机制，覆盖 Flow Agent、Managed Agent、RAG、Memory、Store 五大模块，实现“量·发现与盘点—挡·拦截与防护—记·审计与留痕”的安全闭环 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

> **注意**：文档中多次提及 Evolution 的“框架中立、即插即用”特性，但实际接入需满足 OpenTelemetry GenAI 标准；部分旧文档未明确强调该前提，开发者应以 [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md) 中的说明为准。

## 关键参数

| 功能模块 | 关键参数/配置项 | 说明 |
|----------|------------------|------|
| **应用观测** | `Request ID` / `Trace ID` / `Span ID` | 用于在 Trace 列表中精确检索调用链；支持按时间范围（最长 30 天）和聚合粒度（分钟/小时/天）筛选监控数据。 |
| **应用评测** | 评测集字段映射、评估器变量映射 | 必须确保评测集字段类型与评估器变量类型严格一致（如轨迹类型变量必须映射到轨迹类型列），否则无法保存配置或导致评分异常 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。 |
| **安全策略** | 风险等级（高/中/低）、风险节点类型（Agent/模型/工具/知识库等） | 用于在风险与审计页面筛选和定位问题；高级防护策略全局生效，不区分业务空间 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。 |

## 使用方式

1. **接入准备**：  
   - Evolution：主账号完成 OpenTelemetry 服务角色授权、开通服务并初始化 LogStore；子账号需主账号配置必要权限 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。  
   - Security：默认防护自动生效；高级防护需完成服务授权（当前限时免费），且策略配置对账号下全部 Agent 全局生效 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。  

2. **核心操作路径**：  
   - **观测**：开启应用观测 → 输入测试问题生成 Trace → 在 Trace 列表查看节点详情、监控统计（调用数/[Token](../concepts/token.md)s/模型分析）及限流统计 → 可导出 JSONL/EXCEL 或一键添加至评测集。  
   - **评测**：创建并**发布**评测集（草稿不可用）→ 选择评估器并完成字段映射 → 创建评测任务 → 查看数据明细（含轨迹预览）与指标统计（得分分布、回归对比）。  
   - **优化**：支持三类路径——多版本 Prompt 对比调试、基于调试反馈人工引导优化、基于评测集或评测任务结果智能优化；所有“采纳”操作仅更新当前编辑中的 Prompt，**不会自动发布应用**。  
   - **安全**：通过控制台 Security > 默认防护/高级防护 页面查看防护总览、资产清单、策略状态与风险事件；CLI 命令 `bl agents security overview` 和 `bl agents security alerts` 可快速查询关键指标 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。  

## 限制和注意事项

- **功能限制**：  
  - 应用观测无开放 API，仅支持控制台操作；  
  - 评测集最多保存 10 个版本，超出后自动覆盖；单条轨迹数据大小不能超过 1 MB；  
  - 安全策略目前**暂不支持自动阻断或拦截风险**，仅提供监测与告警能力 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。  

- **关键注意事项**：  
  - 所有评测任务创建后，其配置（应用、评测集、评估器映射）**不可修改**，需新建任务；  
  - 轨迹评测集必须包含 `trajectory` 类型字段，且评估器需显式映射该字段；  
  - Security 模块的风险与审计页面展示**该账号下全部 Agent 的数据，不区分业务空间**，需注意权限隔离边界。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


