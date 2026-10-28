# agent governance

Agent Governance 是百炼平台面向 AI Agent 全生命周期提供的核心治理能力体系，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大支柱，并与内生安全防护深度集成。它基于 OpenTelemetry GenAI 标准实现框架中立接入，支持智能体（Agent 1.0/2.0）与工作流应用，帮助开发者从“黑盒运行”走向“透明决策”，实现质量量化、问题定位、持续迭代与风险防控的一体化闭环。

## 支持的模型/功能

- **观测能力**：支持全链路 Trace 可视化，覆盖 Prompt 解析、大模型调用（含 TTFT、耗时、[Token](../concepts/token.md) 消耗）、MCP 工具执行、向量检索、记忆读写等环节；支持分钟级监控统计（调用数、QPM、[Token](../concepts/token.md) 分析、模型/工具维度趋势）与限流统计 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持端到端输出质量评测（准确性、合规性、简洁性）与轨迹（Trajectory）过程评测（动作循环、回答忠实度、工具调用成功率等），提供预置 LLM/Code 评估器及自定义评估器能力 [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持多版本 Prompt 对比调试、基于调试反馈的智能优化、基于评测集/评测任务结果的定向优化，所有优化操作均作用于草稿态 Prompt，需手动发布生效 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全能力**：提供默认防护（自动生效，免费）与高级防护（限时免费，全局配置）双层安全治理。默认防护覆盖 Flow Agent 输入输出、Managed Agent 运行时沙箱、RAG 知识库、Memory 记忆、Store MCP 组件等内容与行为安全；高级防护提供提示词攻击、敏感数据外泄、RAG 数据投毒等 7 项可选策略 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

> **注意**：文档中提及“应用观测目前暂无 API”，但 Security 模块明确提供了 `/api/v1/agentstudio/security` 下的 7 个 RESTful 接口（如 `/overview`, `/asset_summary`, `/policies`），可用于程序化获取防护与资产数据 [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)。二者能力边界需按模块区分，不可混用。

## 关键参数

- **Trace 相关**：`schema_version`（如 `ATIF-v1.8`）、`session_id`、`trajectory_id`、`steps`（含 `source`, `message`, `step_id`）、`final_metrics`（`total_steps`, `total_prompt_tokens`, `total_completion_tokens`）——用于轨迹结构化存储与评测 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **评测集字段**：创建轨迹评测集时，必填列 `input`（String）、`trajectory`（轨迹类型）；`reference_output` 为可选列。字段类型必须严格匹配，否则导入失败 [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)。
- **评估器配置**：LLM 评估器需指定 `评分范围`（如 0–100）与 `通过阈值`；变量映射必须满足类型一致（如轨迹变量只能映射至评测集中的轨迹类型列）[评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **安全策略参数**：高级防护策略（如“提示词攻击”、“RAG 数据投毒”）全局生效，不支持按业务空间或单个 Agent 配置；内容安全策略需在开通高级防护后手动启用 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 使用方式

1. **接入准备**：主账号完成可观测链路 OpenTelemetry 服务角色授权、服务开通与 LogStore 初始化；Security 默认防护随 Agent 使用自动生效，无需额外操作 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
2. **开启观测**：在控制台 [应用观测](https://bailian.console.aliyun.com/loop/app-observe) 页面为已发布应用开启观测，Trace 数据分钟级同步，支持按 `Request ID`/`Trace ID`/时间范围搜索与导出（JSONL/EXCEL）。
3. **构建评测闭环**：
   - 创建评测集（选择“轨迹”场景以支持过程评测）；
   - 添加评估器（如选用“轨迹准确性”LLM 评估器，需确保评测集含 `trajectory` 列）；
   - 创建评测任务，关联评测集与应用，配置评估器参数映射；
   - 查看数据明细（含轨迹渲染视图）与指标统计 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
4. **执行优化**：在“应用优化”页面选择应用，通过“对比模式”调试多版本 Prompt，或基于已选调试结果/评测集数据发起智能优化，采纳结果后需手动发布应用。
5. **配置安全**：在 [安全策略](https://bailian.console.aliyun.com/loop/security/policy) 页面完成服务授权并开通高级防护；使用 CLI 命令（如 `bl agents security overview`）或 Security API 查询防护状态与风险 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

## 限制和注意事项

- **观测限制**：应用观测暂不支持通过 Assistant API 创建的智能体应用；关闭观测后历史数据停止同步，重新开启仅同步新增数据；Trace 导出最大时间范围为 30 天 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测限制**：单条轨迹 JSON 大小不能超过 1 MB；评测任务创建后配置不可修改（应用、评测集、评估器），仅支持追加人工标签；每个评测任务最多添加 10 个评估器 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **优化限制**：所有“采纳”操作仅更新当前编辑区的 Prompt 草稿，**不会自动发布应用**；发布需在应用管理页面单独操作；基于评测集优化时，字段映射错误将导致系统无法正确识别问题模式，务必提前抽查数据 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全限制**：高级防护策略对账号下全部 Agent 全局生效，不区分业务空间；当前高级防护暂不支持自动阻断风险，仅提供监测与告警；CLI 与 API 查询范围为账号级，不支持按业务空间过滤 [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agent-governance/agenteval/agenteval-changelog.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)
- [更新日志](../../raw/application-user-guide/agent-governance/security-guide/changelog.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)


