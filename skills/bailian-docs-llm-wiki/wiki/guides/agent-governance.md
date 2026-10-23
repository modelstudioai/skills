# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的核心治理能力体系，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大支柱，并与内生安全防护深度集成。它通过 OpenTelemetry GenAI 标准实现框架中立接入，支持从开发调试、线上监控、质量量化到 Prompt 持续迭代的闭环治理，帮助开发者系统性提升 Agent 的可靠性、合规性与业务效果。

## 支持的模型/功能

- **观测能力**：支持智能体应用（Agent 1.0 / 2.0）和工作流应用的端到端链路追踪，完整捕获 Prompt 解析、模型调用（含百炼托管模型及外部模型）、工具执行（MCP/Skill）、知识库检索、记忆读写等环节的 Span 数据，同步记录耗时、Token 消耗、状态与异常信息 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置与自定义双模评估器，覆盖文本、Agent 输出、执行轨迹三类评估对象；支持 LLM 评估器（基于大模型语义评分）与 Code 评估器（基于规则/正则/逻辑校验），并内置 9 类轨迹评估器（如轨迹准确性、动作循环检测、回答忠实度等）[评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持多版本 Prompt 对比调试、基于单条/多条调试对话的反馈式优化、以及基于评测集或评测任务结果的智能优化，所有采纳操作仅更新草稿态 Prompt，不自动发布 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全能力**：默认启用内生防护（内容安全 I/O、供应链扫描、凭证隔离等），高级防护提供 7 项可配置策略（提示词攻击、敏感数据外泄、RAG 数据投毒等），全局生效且当前限时免费 [Security](../../raw/application-user-guide/agent-governance/security-guide.md)。

> **注意**：文档 30 明确指出“应用观测目前暂不支持通过 Assistant API 创建的智能体应用”，而文档 4 和文档 2 均未提及此限制，该约束为关键兼容性限制，需在接入前确认 Agent 创建方式。

## 关键参数

| 参数类别 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **观测** | `QPM`、`TTFT`、`duration_ms`、`total_tokens` | 核心监控指标，用于限流统计与性能分析；其中 QPM 限流阈值默认为 6000，可在告警模板中配置 [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md) | 文档 6、30 |
| **评测** | `评分范围`、`通过阈值`、`字段映射` | LLM 评估器必需配置评分尺度（如 0–100）与 Pass/Fail 判定线；所有评估器变量必须完成类型一致的字段映射（如轨迹变量 → 评测集 trajectory 列） | 文档 8、9 |
| **优化** | `基准组/对照组`、`人工反馈描述`、`评测集字段映射` | 多版本对比需明确定义基准；调试反馈需具体描述问题与期望改进；基于评测集优化时，`应用输入`为必填映射字段，`轨迹`为可选但类型强校验字段 | 文档 10、28 |
| **安全** | `防御席位费`、`Credit 额度`、`风险等级` | 高级防护计费核心参数：0.42 元/席位·小时 + 超额 Credit（0.0015 元/Credit）；风险按高/中/低三级分级，影响审计优先级 | 文档 25、23 |

## 使用方式

1. **接入与初始化**：  
   - 观测：首次使用需在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)页面完成 OpenTelemetry 服务角色授权、服务开通与 LogStore 初始化（主账号操作）[应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。  
   - 安全：默认防护随 Agent 使用自动生效；高级防护需在 Security > 高级防护 > 安全策略 页面完成服务授权并开通 [Security](../../raw/application-user-guide/agent-governance/security-guide.md)。

2. **核心流程**：  
   - **观测 → 评测 → 优化**：在应用观测中定位异常 Trace → 导出为评测集 → 创建评测任务（关联轨迹评估器）→ 分析低分样本 → 发起基于评测集的 Prompt 优化任务。  
   - **评测集构建**：创建评测集时选择「轨迹」场景，系统自动生成 `input`/`reference_output`/`trajectory` 三列结构；轨迹数据须为合法 JSON，单条 ≤ 1 MB [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。  
   - **告警配置**：基于预置模板（如“QPM 限流大于 6000”）快速创建规则，或自定义复合条件；告警通知支持邮箱等渠道，重复策略需明确设置 [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)。

3. **CLI 与 API**：  
   - 安全模块提供 CLI 命令（如 `bl agents security overview`）和 RESTful API（路径前缀 `/api/v1/agentstudio/security`），用于自动化查询防护总览、资产、策略与风险日志 [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)。

## 限制和注意事项

- **功能限制**：应用观测不支持 Assistant API 创建的智能体；轨迹评测功能于 2026-10-21 上线，旧版评测集需手动升级表结构以支持 `trajectory` 字段 [更新日志](../../raw/application-user-guide/agent-governance/agenteval/agenteval-changelog.md)。
- **数据约束**：评测任务中，评估器变量与评测集字段的数据类型必须严格一致（如轨迹变量不可映射至 String 列），否则无法保存配置；评测集单文件上传上限 20 MB，单条轨迹 JSON 上限 1 MB [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **权限与范围**：安全策略配置对账号下全部 Agent 全局生效，不区分业务空间；应用观测数据按业务空间隔离，跨空间 Trace 不可见 [Security](../../raw/application-user-guide/agent-governance/security-guide.md)、[应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **计费提醒**：高级防护当前限时免费，正式计费后将按席位小时 + 超额 Credit 计费；评测任务调用大模型产生的 Token 按常规模型计费，不包含在安全额度内 [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)、[评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

## 来源文档

- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
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
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/agent-governance/security-guide/changelog.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)


