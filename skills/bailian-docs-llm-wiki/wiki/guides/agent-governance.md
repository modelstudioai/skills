# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力集合，涵盖可观测性、自动化评测、智能优化与内生安全四大支柱。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现即插即用，支持从开发调试、线上运行到效果迭代的闭环管理，同时提供默认生效的安全防护与可配置的高级策略。

## 支持的模型/功能

- **观测能力**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路 Trace 可视化，覆盖 Prompt 解析、大模型调用（含 TTFT、Token 消耗）、工具执行（MCP/Skill）、向量检索、记忆读写等节点；暂不支持通过 Assistant API 创建的智能体应用 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持多维自动化评测，包括文本质量（准确性、简洁性、合规性）、轨迹可靠性（步骤逻辑、工具调用成功率、回答忠实度）、多模态内容（图片美学/指令遵循/画质、语音一致性、视频理解）等；预置 LLM 与 Code 类评估器超 20 种，均需按字段类型严格映射 [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持基于调试结果、评测任务低分样本、线上 Trace 数据或评测集的 Prompt 智能优化；所有优化路径均生成对比版本，采纳后仅更新草稿态 Prompt，**不会自动发布应用** [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全能力**：提供“量·挡·记”闭环防护：默认防护自动盘点 Agent 资产（Flow/Managed Agent、模型、工具、知识库、记忆等），并拦截输入输出内容安全、Skill 静态扫描、RAG 文件预扫描等风险；高级防护含 7 项可选策略（如提示词攻击、敏感数据外泄、RAG 数据投毒），全局生效且当前限时免费 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

> **注意**：文档中关于“应用观测目前暂无 API”的表述（见 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)）与 Security 模块明确提供 `/api/v1/agentstudio/security` 下 7 个治理相关 API 的事实矛盾。实际可观测性能力虽无独立 OpenTelemetry 上报 API，但 Security 模块已开放资产、策略、告警等治理接口，开发者可通过 API 实现部分治理自动化。

## 关键参数

- **观测配置**：首次使用需主账号完成三项前置操作——授权 OpenTelemetry 服务角色、开通 OpenTelemetry 服务、初始化 LogStore；子账号需主账号预先授予 `AliyunBailianFullAccess` 或最小权限策略 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集字段**：轨迹评测集必须包含 `trajectory`（数据类型为“轨迹”）列；多模态评测集需将对应列设为“多模态”类型，且单条数据中图片/音频/视频 URL 必须有效且符合格式（JPG/PNG/MP3/MP4/MOV，大小限制分别为 20MB/100MB/100MB） [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **评估器映射**：创建评测任务时，所有评估器变量必须完成映射，且映射字段的数据类型须严格一致（如轨迹变量只能映射到轨迹类型列，多模态变量只能映射到多模态类型列），否则无法保存配置 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全策略作用域**：所有安全策略配置对当前阿里云账号下全部 Agent **全局生效**，不区分业务空间；修改前需评估影响范围 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 使用方式

- **观测**：在控制台进入「应用观测」→「开启观测」目标应用 → 输入测试问题触发 Trace → 在 Trace 列表中按 Request ID/Trace ID 搜索 → 查看节点详情、监控统计（QPM、Token、延时）、限流统计，并可导出 JSONL/EXCEL；支持将 Trace 批量导入评测集 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测**：先创建并**发布**评测集（草稿不可用）→ 选择预置或自定义评估器 → 创建评测任务，绑定评测集版本、目标应用及评估器 → 配置变量映射 → 运行后查看数据明细（含轨迹渲染视图）与指标统计（得分分布、回归对比） [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **优化**：在「应用优化」页面选择目标应用 → 可选三类路径：① 多版本 Prompt 对比调试；② 基于单条/多条调试结果 + 人工反馈生成新 Prompt；③ 基于已发布评测集或已完成评测任务的低分样本定向优化；所有路径均支持一键采纳至当前 Prompt 编辑区 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全**：默认防护自动启用；高级防护需在「Security > 高级防护 > 安全策略」完成服务授权并开通；风险事件与审计日志在「Security > 高级防护 > 风险与审计」集中查看，支持按风险等级、节点类型筛选及 Trace 下钻 [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)。

## 限制和注意事项

- **观测限制**：Trace 数据同步延迟约 1 分钟；监控与限流指标聚合粒度最小为分钟级；Trace 最长保留 30 天；关闭观测后历史数据仍保留，但新增数据停止上报。
- **评测限制**：单个评测任务最多添加 10 个评估器；评测集最多保存 10 个版本（超出自动覆盖）；轨迹数据单条大小 ≤ 1 MB；多模态数据单文件上传上限为 20 MB（图片）或 100 MB（音视频）。
- **优化限制**：采纳优化结果仅更新当前编辑中的 Prompt，**必须手动发布应用才能生效**；基于评测任务优化时，仅支持状态为“已完成”的任务；调试优化中若选择多条调试结果，应确保其反映同一优化目标，避免冲突反馈导致 Prompt 约束混乱。
- **安全限制**：高级防护当前**不支持自动阻断或拦截风险**，仅提供监测、告警与审计能力；风险与审计页面展示账号下全部 Agent 数据，**不区分业务空间**；自建内容安全审批通过后，“内容安全”项将显示为“关闭”，需重新配置 [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)。

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
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


