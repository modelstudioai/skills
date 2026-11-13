# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力体系，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大核心支柱，并与内生安全防护深度集成。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现即插即用，支持从开发调试、线上运行到效果迭代的闭环管理。

## 支持的模型/功能

- **Agent 类型**：完整支持 Agent 1.0、Agent 2.0 和工作流应用；**不支持**通过 Assistant API 创建的智能体应用 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **核心功能模块**：
  - **观测（Observability）**：全链路 Trace 可视化（Prompt 解析、模型调用、工具执行、记忆读写），支持延时、Token、QPM、错误率等分钟级监控与限流统计。
  - **评测（Evaluation）**：支持多维自动化评测，包括文本输出质量（准确性、合规性、简洁性）、执行轨迹（步骤逻辑、工具调用成功率、回答忠实度）、多模态内容（图片美学、指令遵循、幻觉检测）[评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
  - **优化（Optimization）**：支持基于调试结果、评测集数据或线上 Trace 的 Prompt 智能优化，提供多版本对比、人工反馈引导与一键采纳能力 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
  - **安全（Security）**：默认启用内生防护（内容安全 I/O、RAG 文件预扫描、凭证隔离等），高级防护（提示词攻击检测、敏感数据外泄检测等）需授权开通 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

> **注意**：文档中“应用观测目前暂无 API”（见 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)）与 Security 模块明确提供 7 个 RESTful API（见 [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)）存在功能边界差异——前者指观测数据上报无开放 API，后者指安全状态查询有 API；二者不矛盾，但需区分使用场景。

## 关键参数

- **观测配置**：首次使用需通过“应用观测配置”完成三步授权：① 授权 OpenTelemetry 服务角色；② 开通 OpenTelemetry 服务；③ 初始化 LogStore 存储 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集字段映射**：创建评测任务时，评估器变量必须与评测集字段或应用输出字段**类型严格一致**（如 `trajectory` 变量只能映射到 `trajectory` 类型列），否则无法保存配置 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全策略生效范围**：所有安全策略配置对**账号下全部 Agent 全局生效**，不区分业务空间，修改前需评估影响范围 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 使用方式

1. **接入观测**：在控制台「应用观测」页面对目标应用点击「开启观测」，随后发送测试问题生成 Trace，即可在 Trace 列表、监控统计、限流统计页签中查看数据。
2. **发起评测**：
   - 创建评测集（支持空建、文件导入，场景可选“智能体”“轨迹”“多模态”等）；
   - 创建评估器（复用预置模板或自定义 LLM/Code 评估器）；
   - 组合评测集、应用、评估器创建评测任务，任务完成后查看数据明细与指标统计。
3. **执行优化**：
   - 在「应用优化」页面选择应用；
   - 可选路径：① 多版本 Prompt 对比调试；② 基于单条/多条调试结果 + 人工反馈生成优化；③ 基于已发布评测集或已完成评测任务的样本进行智能优化。
4. **启用安全**：
   - 默认防护自动生效（无需操作）；
   - 高级防护需进入「Security > 高级防护 > 安全策略」完成服务授权并手动开启策略；
   - 风险事件与审计日志统一在「Security > 高级防护 > 风险与审计」查看。

## 限制和注意事项

- **观测限制**：Trace 数据同步延迟为分钟级；关闭观测后历史数据停止同步，重新开启仅同步新增数据；子账号需主账号预先配置权限方可操作 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测限制**：评测集必须**发布后**才能用于评测任务，草稿状态不可用；单条轨迹数据大小不能超过 1 MB；多模态文件上传有格式与大小限制（图片≤20 MB，音频/视频≤100 MB）[添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **安全限制**：高级防护当前**仅支持风险监测与告警，不支持自动阻断**；内容安全策略需在开通高级防护后**手动开启**；Agent 资产盘点仅覆盖百炼纳管的 Flow Agent 和 Managed Agent，外部 Agent 不计入 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


