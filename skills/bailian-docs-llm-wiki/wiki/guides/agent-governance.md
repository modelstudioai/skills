# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力集合，涵盖可观测性、自动化评测、智能优化与内生安全四大支柱。它基于 OpenTelemetry GenAI 标准实现框架中立接入，支持从开发调试、线上运行到持续迭代的闭环管理，帮助开发者快速定位问题、量化效果、优化 Prompt 并保障生产环境安全。

## 支持的模型/功能

- **可观测性**：支持智能体应用（Agent 1.0 和 Agent 2.0）及工作流应用的全链路 Trace 捕获，覆盖 Prompt 解析、大模型调用（含 TTFT、[Token](../concepts/token.md) 消耗）、工具执行（MCP）、向量检索、记忆读写等环节；但**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置 LLM/Code 评估器（如轨迹准确性、动作循环检测、回答忠实度等），支持文本、Agent 输出、执行轨迹三类评估对象；轨迹评测需评测集字段类型为 `trajectory`，且须使用[添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)规范构建。
- **优化能力**：支持多版本 Prompt 对比调试、基于调试反馈的智能优化、以及基于评测集/评测任务低分样本的定向优化；所有采纳操作仅更新当前编辑中的 Prompt，**不会自动发布应用** [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全防护**：默认防护随 Agent 使用模块（如 RAG、Memory、Managed Agent）自动生效，覆盖内容安全 I/O、知识库预扫描、沙箱隔离等；高级防护提供 7 项可配置策略（如提示词攻击、敏感数据外泄），但当前**仅支持风险监测，不支持自动阻断** [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

> **注意**：文档中关于“应用观测目前暂无 API”的表述（见[应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)）与 Security 模块明确提供 `/api/v1/agentstudio/security` 系列 API（含防护总览、资产、告警等）存在功能范围矛盾。此处“暂无 API”特指应用观测模块自身未开放 Trace 数据上报或查询接口，而非整个 agent governance 体系无 API 支持。

## 关键参数

- **Trace 上报粒度**：监控与限流指标更新频率为分钟级，Trace 数据同步延迟通常为分钟级 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集字段映射**：评估器变量必须与评测集字段类型严格一致（如轨迹类型变量须映射至 `trajectory` 类型列），否则无法保存配置 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全 Credit 消耗**：高级防护按席位（运行中 Agent）+ Credits 计费，每个席位每日默认 300 Credits，超量部分按 0.0015 元/Credit 计费；Credit 按自然日重置，不结转 [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)。
- **告警检查周期**：最小支持 60 秒，单位为秒，必须为不小于 0 的整数 [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)。

## 使用方式

- **接入可观测性**：主账号需先授权 OpenTelemetry 服务角色、开通服务并初始化 LogStore；应用需发布后才可在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)页面开启观测。
- **发起评测任务**：需先创建并**发布**评测集（草稿态不可用），再关联已发布的评测集版本与评估器；评估器参数映射必须全部完成才能保存 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **执行安全审计**：风险与审计页面展示**账号下全部 Agent** 的事件（不分业务空间），需先开通高级防护并启用对应策略，否则无数据 [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)。
- **CLI 快速查询**：通过 `bl agents security overview` 和 `bl agents security alerts` 命令可终端查询防护统计与风险详情，需提前安装并鉴权百炼 CLI [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

## 限制和注意事项

- **应用观测限制**：不支持 Assistant API 创建的智能体；关闭观测后历史数据停止同步，重新开启仅同步新增数据；Trace 导出最大时间范围为 30 天 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集约束**：单条轨迹数据大小不能超过 1 MB；评测集最多保存 10 个版本，超出后自动覆盖；本地上传文件最大 20 MB [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)。
- **安全策略全局性**：高级防护策略配置对账号下**全部 Agent 全局生效，不区分业务空间**，修改前需评估影响范围 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。
- **优化结果落地**：所有“采纳”操作仅写入当前 Prompt 编辑区，**必须手动发布应用才能使优化生效**；评测任务创建后配置不可修改，需新建任务调整 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
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


