# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的治理能力集合，涵盖可观测性、可评测性与可优化性三大核心维度。它通过统一的数据标准（如 OpenTelemetry GenAI）、结构化反馈闭环（Trace → 评测集 → 优化）和安全内生防护，帮助开发者系统性地“看清链路、量化质量、持续改进、守住边界”。该能力不依赖特定框架，支持 Agent 1.0/2.0、工作流应用，但暂不支持 Assistant API 创建的智能体。

## 支持的模型/功能

- **观测能力**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路追踪（Trace），完整捕获 Prompt 解析、模型调用（含 TTFT、[Token](../concepts/token.md) 消耗）、工具执行、记忆读写等 Span 级事件；提供分钟级监控统计（QPM、错误率、调用时长）与限流指标（QPM 限流次数）[原文标题](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持文本输出评测（准确性、简洁性、合规性）与轨迹（Trajectory）评测（动作循环、回答忠实度、[工具调用](../concepts/tool-calling.md)成功率等），预置 LLM/Code 双类型评估器，并支持自定义 LLM 评估器（含评分范围与通过阈值配置）和 Code 评估器（Python 脚本）[原文标题](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持基于调试对话、线上 Trace、评测集或评测任务结果的 Prompt 智能优化；提供多版本对比调试、人工反馈引导生成、字段映射驱动的结构化优化路径[原文标题](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全能力**：提供默认防护（自动生效）与高级防护（需授权开通）双层机制。默认防护覆盖 Flow Agent（I/O 内容安全）、Managed Agent（沙箱隔离、凭证隔离）、RAG（知识库文件预扫描）、Memory（记忆内容检测）、Store（MCP/Skill 静态扫描）；高级防护包含提示词攻击、敏感数据外泄、RAG 数据投毒等 7 项可选策略[原文标题](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 关键参数

- **观测配置**：`OpenTelemetry 服务角色授权`、`LogStore 初始化`为前置必要步骤；告警规则中 `持续时间`（分钟）、`告警检查周期`（秒）、`统计周期`（分钟）为关键时效参数；限流指标仅支持分钟级聚合粒度。
- **评测集字段**：轨迹评测集必须包含 `trajectory`（类型为“轨迹”）列；LLM 评估器对输入字段有强约束（如「问答相关性」要求 `query` 和 `response` 字段），字段类型与映射关系必须严格一致，否则无法保存配置或导致评分异常。
- **评估器配置**：
  - LLM 评估器：`评分范围`（如 0–100）决定区分粒度，`通过阈值`（如 ≥80）决定 Pass/Fail 判定；系统提示词中需显式包含评分范围。
  - Code 评估器：入参须与评测集字段类型匹配，脚本返回 `{"score": number, "reason": string}` 结构。
- **安全策略**：所有策略配置对账号下全部 Agent **全局生效**，不区分业务空间；`内容安全`策略需在开通高级防护后手动启用，其余 6 项默认开通。

## 使用方式

1. **观测接入**：在应用列表点击「开启观测」→ 完成 [应用观测配置](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)（主账号授权 OpenTelemetry 角色、开通服务、初始化 LogStore）→ 输入测试问题触发 Trace 上报 → 在 Trace 列表查看节点详情。
2. **评测执行**：创建并[发布评测集](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)（草稿不可用）→ 选择预置或自定义评估器 → 配置变量映射（确保字段类型一致）→ 创建评测任务 → 查看数据明细与指标统计。
3. **优化启动**：在「应用优化」页面选择目标应用 → 选择路径（调试反馈 / 评测集 / 评测任务）→ 按向导完成数据选择、字段映射、人工反馈输入 → 点击「开始优化」→ 在弹窗中对比并「采纳」结果（仅更新草稿 Prompt，不自动发布）。
4. **安全防护**：默认防护随 Agent 使用模块（如 RAG、Memory）自动生效；高级防护需在 Security 控制台完成服务授权 → 进入「安全策略」页面启用所需策略 → 风险事件与审计日志在「风险与审计」页面统一查看（跨业务空间）。

## 限制和注意事项

- **模型/应用限制**：应用观测、评测、优化均**不支持通过 Assistant API 创建的智能体**；仅支持已发布的 Agent 1.0/2.0 和工作流应用[原文标题](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **数据一致性风险**：评测集字段类型与评估器变量类型、Trace 字段与评测集字段映射类型**必须严格一致**，否则导入失败或评分逻辑失效；轨迹 JSON 单条大小不得超过 1 MB。
- **权限与范围**：应用观测配置需使用**主账号**操作，子账号需主账号预先配置 OpenTelemetry 权限；安全策略配置对账号下所有 Agent 全局生效，修改前须评估影响范围。
- > **注意**：文档 22（防护总览）指出“默认防护随 Agent 使用自动生效”，而文档 19（概述）强调“防护在 Agent 使用对应模块后自动生效”，二者一致；但文档 26（安全策略）明确说明“当前高级防护主要支持策略配置与风险监测，**暂不支持自动阻断或拦截风险**”，这与部分用户预期的“防护=实时拦截”存在差异，需特别注意其当前能力边界。
- > **注意**：文档 6 明确声明“应用观测目前暂无 API”，而文档 28 列出了 `/api/v1/agentstudio/security` 下的多个 Security API。这意味着 agent governance 中的 **Observability（观测）模块无公开 API**，但 Security（安全）模块提供完整 API 支持，二者能力开放程度不同，不可混用。
- **计费说明**：评测任务调用大模型产生的 [Token](../concepts/token.md) 按常规计费；安全能力当前处于限时免费阶段，但高级防护未来可能计费，具体规则参见[计费说明](../../raw/application-user-guide/agent-billing/billing.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


