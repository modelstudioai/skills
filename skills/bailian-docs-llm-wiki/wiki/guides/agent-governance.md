# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力体系，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大支柱，并内嵌原生安全防护（Security）。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现即插即用，帮助开发者从“黑盒运行”走向“透明决策”，支撑 Agent 的稳定交付与持续迭代。

## 支持的模型/功能

- **观测能力**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路 Trace 可视化，覆盖 Prompt 解析、模型调用（含百炼内置及外部模型）、工具执行（MCP/Connector）、向量检索、记忆读写等环节；支持延时、Token 消耗、QPM、错误率等分钟级监控指标。> **注意**：目前暂不支持通过 Assistant API 创建的智能体应用，详见[应用观测](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持多维自动化评测，包括：
  - **文本维度**：准确性、简洁性、合规性、格式校验等；
  - **轨迹维度**：动作循环检测、回答忠实度、执行成功性、工具调用成功率等（需评测集含 `trajectory` 字段），参考[添加轨迹评测数据](raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)；
  - **多模态维度**：图片美学/指令遵循/画质、语音内容一致性、多模态幻觉检测等（需评测集含 `多模态` 字段），参考[添加多模态评测数据](raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)。
- **优化能力**：支持基于调试结果、评测任务低分样本、线上 Trace 数据或评测集的 Prompt 多版本对比与智能优化，生成可审查、可采纳的 Prompt 候选方案。
- **安全能力**：提供默认防护（自动生效）与高级防护（按需开通）双层机制，覆盖 Flow Agent、Managed Agent、RAG、Memory、Store 五大模块，实现“量·挡·记”闭环，详见[概述](raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

## 关键参数

| 参数类别 | 关键参数 | 说明 |
|----------|----------|------|
| **观测配置** | `OpenTelemetry 服务角色授权`、`LogStore 初始化` | 首次使用前必需完成，主账号操作；子账号需主账号授权权限。 |
| **评测集字段** | `input`（String）、`reference_output`（String）、`trajectory`（轨迹）、`multimodal`（多模态） | 字段类型必须与评估器变量映射严格一致，否则无法保存配置或导致评分异常。 |
| **评估器映射** | `query` ↔ `input`、`response` ↔ `output`、`trajectory` ↔ `trajectory` | 映射错误将直接导致评估器失效；预置评估器对字段有明确要求，建议先查阅其详情页。 |
| **安全策略** | `提示词攻击`、`敏感数据外泄`、`RAG 数据投毒` 等共 7 项 | 全局生效，影响账号下所有 Agent；`内容安全`需手动开启，其余 6 项默认开通。 |

## 使用方式

1. **观测接入**：在[应用观测配置](https://bailian.console.aliyun.com/loop/app-observe)中完成 OpenTelemetry 授权与 LogStore 初始化 → 在应用列表点击**开启观测** → 输入测试问题触发 Trace 上报 → 进入详情页查看 Trace 列表、监控统计、限流统计。
2. **评测执行**：创建并**发布**评测集（草稿不可用）→ 选择预置或自定义评估器 → 创建评测任务，严格完成变量映射 → 启动任务，查看数据明细与指标统计。
3. **Prompt 优化**：在应用优化页面选择路径（调试反馈 / 评测集 / 评测任务）→ 提供问题样本与人工反馈（如适用）→ 查看生成 Prompt 与当前 Prompt 的对比 → 点击**采纳**更新编辑区（**不自动发布**）。
4. **安全启用**：默认防护随 Agent 使用对应模块（如 RAG、Memory）自动生效；高级防护需在[安全策略](https://bailian.console.aliyun.com/loop/security/policy)页面完成服务授权后开通，并可按需启停具体策略。

## 限制和注意事项

- **观测限制**：应用观测目前**无公开 API**，仅支持控制台操作；Trace 数据最长保留 30 天；关闭观测后历史数据停止同步，重启仅同步新增数据。
- **评测限制**：单条轨迹数据大小 ≤ 1 MB；单个评测集最多支持 50 个字段映射；每个评测任务最多支持 10 个评估器；评测任务创建后**不可修改**应用、评测集或评估器配置。
- **优化限制**：采纳操作仅更新当前编辑中的 Prompt，**不会自动发布应用**；多条调试结果用于优化时，应聚焦同一问题，避免反馈冲突导致优化方向模糊。
- **安全限制**：高级防护策略配置对账号下**全部 Agent 全局生效**，不区分业务空间；风险与审计页面展示该账号下**全部 Agent** 的数据，**不区分业务空间**；`内容安全`策略需手动开启，且若已发起自建内容安全审批，则该项显示为“关闭”。
- > **注意**：文档 4 与文档 5 均指出“应用观测暂不支持通过 Assistant API 创建的智能体”，但文档 2 的概览中未明确此限制，以文档 4 和文档 5 的表述为准。

## 来源文档

- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
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
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


