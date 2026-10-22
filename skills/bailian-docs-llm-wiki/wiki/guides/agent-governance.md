# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的核心治理能力体系，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大支柱，并与内生安全防护深度集成。它通过 OpenTelemetry 标准实现框架中立的链路采集，支持从开发调试、线上监控、质量评测到 Prompt 智能优化的闭环迭代，同时提供默认生效的安全防护与按需启用的高级策略，保障 Agent 在业务落地过程中的稳定性、质量与合规性。

## 支持的模型/功能

- **观测能力**：支持智能体应用（Agent 1.0 和 Agent 2.0）及工作流应用的全链路追踪，覆盖 Prompt 解析、大模型调用（含 TTFT、耗时、Token 消耗）、MCP 工具执行、向量检索、记忆读写等环节；但[应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)明确指出暂不支持通过 Assistant API 创建的智能体应用。
- **评测能力**：支持基于预置评估器（通用质量、智能体、文本匹配、文本相似度、格式校验）和自定义评估器（LLM 或 Code 方式）对输出进行多维自动化评分；支持将线上 Trace 数据直接导入评测集，构建真实业务场景的评测样本 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **优化能力**：支持三类 Prompt 优化路径：① 多版本对比调试；② 基于单条或多条调试结果 + 人工反馈的智能优化；③ 基于已发布评测集或已完成评测任务的低分样本定向优化 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全能力**：提供默认防护（随 Agent 使用自动生效，免费）与高级防护（限时免费，需服务授权）。默认防护覆盖 Flow Agent、Managed Agent、RAG、Memory、Store 五大模块的内容安全、沙箱隔离、知识库预扫描等；高级防护提供 7 项可配置策略，包括提示词攻击检测、敏感数据外泄、RAG 数据投毒等 [Security](../../raw/application-user-guide/agent-governance/security-guide.md)。

> **注意**：文档中存在功能归属矛盾。`agenteval` 系列文档将“观测、评测、优化”统称为 Evolution 平台能力；而 `security-guide` 文档将安全能力独立为 Security 模块。二者在控制台为并列导航项（Evolution 与 Security），但 Wiki 主题 `agent governance` 需统一涵盖。此处以功能实质为准，将安全视为 governance 的关键子域，而非 Evolution 的子功能。

## 关键参数

- **观测参数**：Trace ID、Span ID、Request ID、QPM、TTFT（首 Token 耗时）、总耗时、输入/输出 Token 量、错误码；限流指标仅支持分钟级聚合。
- **评测参数**：
  - 评测集：字段映射需严格匹配评估器要求（如「问答相关性」评估器必需 `query` 和 `response` 字段）[评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)；
  - 评估器：`评分范围`（如 0–100）与 `通过阈值`（如 ≥80 为 Pass）必须一致且在系统提示词中显式体现；
  - 评测任务：最多支持 10 个评估器，建议组合使用 LLM（语义）与 Code（规则）评估器。
- **安全参数**：
  - 默认防护：无显式配置参数，依赖 Agent 使用的模块自动激活；
  - 高级防护：7 项策略（提示词攻击、敏感数据外泄等）全局生效，`内容安全` 策略需手动开启，其余 6 项默认开通 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 使用方式

- **观测**：在控制台 Evolution > 应用观测页面，点击目标应用的**开启观测**；需主账号完成 OpenTelemetry 服务角色授权、服务开通及 LogStore 初始化；开启后数据分钟级同步，支持按 Trace ID 搜索、导出 JSONL/EXCEL、添加至评测集。
- **评测**：
  1. 创建评测集（选择智能体/工作流类型 → 编辑表结构 → 导入数据 → 发布）；
  2. 创建评估器（基于预置模板或自定义 LLM/Code）；
  3. 创建评测任务（关联评测集 + 应用 + 评估器 + 参数映射）。
- **优化**：
  - 版本对比：在应用优化页开启**对比模式**，配置基准组与对照组 Prompt，输入问题发起调试，采纳最优组配置；
  - 调试反馈：在调试窗口输入问题 → 选择代表性调试结果 → 输入具体人工反馈 → 点击**开始优化** → 采纳结果；
  - 评测集/任务优化：选择已发布评测集或已完成评测任务 → 映射字段（必需 `应用输入`）→ 开始优化 → 查看报告并采纳。
- **安全**：
  - 默认防护：无需操作，Agent 使用对应模块（如 RAG）即自动启用；
  - 高级防护：进入 Security > 高级防护 > 安全策略 → 点击**立即开通** → 同意协议 → 手动开启 `内容安全` 策略；
  - CLI 查询：`bl agents security overview`（防护统计）、`bl agents security alerts`（风险告警）[使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

## 限制和注意事项

- **观测限制**：当前无公开 API；仅支持 30 天内 Trace 数据查询；关闭观测后历史数据停止同步，重启仅同步新增数据；不支持 Assistant API 创建的智能体。
- **评测限制**：评测集文件最大 20 MB（xls/xlsx）；草稿状态评测集不可用于评测任务；评测任务创建后配置不可修改（应用、评测集、评估器映射均锁定）；LLM 评估器调用产生的 Token 正常计费。
- **优化限制**：采纳优化结果仅更新当前编辑区 Prompt，**不会自动发布应用**；基于评测集优化时，需确保字段映射准确，否则影响优化效果；多条调试结果应围绕同一优化目标，避免冲突反馈。
- **安全限制**：高级防护策略当前**仅支持风险监测与告警，不支持自动阻断**；安全策略配置对账号下全部 Agent 全局生效，不区分业务空间；风险与审计页面数据不分业务空间，展示账号级汇总 [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)。
- **通用注意事项**：所有治理能力均基于业务空间（Business Space）隔离，但安全策略与风险审计为账号级；Evolution 与 Security 为两个独立服务，需分别开通权限与服务角色。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [更新日志](../../raw/application-user-guide/agent-governance/agenteval/agenteval-changelog.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [更新日志](../../raw/application-user-guide/agent-governance/security-guide/changelog.md)


