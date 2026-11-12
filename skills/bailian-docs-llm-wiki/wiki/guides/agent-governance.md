# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的核心治理能力集合，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大支柱，并通过内生安全防护（Security）保障运行合规。它不依赖特定框架，基于 OpenTelemetry GenAI 标准实现即插即用，支持从开发调试、线上监控、质量量化到 Prompt 持续迭代的闭环管理。

## 支持的模型/功能

- **观测能力**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路追踪，完整记录 Prompt 解析、模型调用（含百炼内置及外部模型）、工具执行（MCP/Skill）、向量检索、记忆读写等环节；支持 Trace 数据导出（JSONL/EXCEL）及回流至评测集 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持多维自动化评测，包括文本输出（准确性、简洁性、合规性）、执行轨迹（工具调用成功率、动作循环检测、回答忠实度）、多模态内容（图片美学/指令遵循/幻觉检测、语音一致性、视频理解）等；预置 LLM 与 Code 双类型评估器，覆盖通用质量、任务执行、格式校验等标签维度 [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持基于调试结果、评测任务低分样本、线上 Trace 数据三种路径驱动 Prompt 智能优化；提供多版本对比调试、人工反馈引导、字段映射配置等能力，优化结果可一键采纳至编辑区（不自动发布） [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全防护**：提供“量·挡·记”三层内生安全能力——默认防护自动盘点 Agent 资产（Flow/Managed Agent、模型、工具、知识库、记忆等），实时拦截内容安全 I/O、Skill 静态扫描、文件预扫描等风险；高级防护支持提示词攻击、敏感数据外泄、RAG 数据投毒等 7 项可选策略 [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)。

> **注意**：文档明确指出“应用观测目前暂无 API”，而 Security 模块则提供了完整的 API 接口（如 `/api/v1/agentstudio/security/overview`），二者在可编程性上存在显著差异，开发者需按场景选择合适接入方式。

## 关键参数

- **观测配置**：首次使用需主账号完成 OpenTelemetry 服务角色授权、服务开通及 LogStore 初始化；子账号需主账号预先配置必要权限。
- **评测集字段**：创建时需严格匹配评估器要求的数据类型。例如轨迹评估器必须映射至 `trajectory` 类型列，多模态评估器必须映射至 `多模态` 类型列；类型不匹配将导致配置无法保存或评分失败 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全策略作用域**：所有安全策略配置对账号下全部 Agent **全局生效**，不区分业务空间；修改前须评估跨空间影响 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。
- **轨迹数据结构**：必须为合法 JSON，单条大小 ≤ 1 MB；核心字段包括 `schema_version`、`session_id`、`trajectory_id`、`steps`（含 `source`、`message`、`step_id`）及 `final_metrics`；`steps` 中 `source` 值仅支持 `"user"` 或 `"agent"` [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。

## 使用方式

1. **观测接入**：在控制台「应用观测」页面，对目标应用点击「开启观测」→ 输入测试问题触发 Trace → 进入详情页查看 Trace 列表、监控统计（QPM、[Token](../concepts/token.md)、延时）、限流统计；可配置告警规则（基于预置模板如“QPM 限流大于 6000”）并查看告警历史 [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)。
2. **评测构建**：先创建并**发布**评测集（草稿不可用）→ 选择预置或自定义评估器 → 创建评测任务，映射评估器变量至评测集字段或应用输出 → 批量运行后分析数据明细（含轨迹详情）与指标统计（得分分布、回归对比）。
3. **优化执行**：在「应用优化」页面选择应用 → 任选路径（调试反馈 / 评测集 / 评测任务）→ 配置输入（如测试问题、评测集版本、低分样本）与映射关系 → 点击「开始优化」→ 查看对比报告并「采纳」至 Prompt 编辑区。
4. **安全启用**：默认防护随 Agent 使用对应模块（如 RAG、Memory）自动生效；高级防护需在「Security > 高级防护 > 安全策略」完成服务授权后开通，默认启用前 6 项策略，`内容安全` 需手动开启。

## 限制和注意事项

- **应用兼容性**：应用观测**不支持**通过 Assistant API 创建的智能体；安全防护当前仅纳管 Flow Agent 和 Managed Agent，外部 Agent 不自动识别为资产 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)、[Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)。
- **数据时效性**：观测数据同步频率为分钟级；告警检查周期最小单位为秒（默认 60 秒）；防护总览数据约每 2 分钟刷新一次。
- **评测集约束**：单个评测集最多支持 50 个字段映射；评测集最多保存 10 个版本，超出后自动覆盖旧版本；多模态文件上传有格式与大小限制（图片≤20MB，音频/视频≤100MB） [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)、[添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)。
- **CLI 与 API 差异**：CLI 命令（如 `bl agents security overview`）仅查询最近 24 小时数据，且不触发防护配置；API 接口（如 `/overview`）无时间范围限制，但需注意其响应中单项数据不可用时返回 `null` 而非报错 [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)。
- **优化结果生效**：所有优化路径生成的 Prompt 采纳操作**仅更新当前编辑中的 Prompt**，不会自动发布应用，发布需手动操作。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
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
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)


