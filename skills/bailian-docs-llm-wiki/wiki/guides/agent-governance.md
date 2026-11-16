# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力集合，涵盖可观测性、可评测性与可优化性三大核心维度，并与内生安全防护深度集成。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现即插即用，支持从开发调试、线上运行到效果迭代的闭环管理。

## 支持的模型/功能

- **观测能力**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路追踪（Trace），完整记录 Prompt 解析、模型调用（含百炼内置及外部模型）、工具执行（MCP/Connector/Skill）、向量检索、记忆读写等环节；暂不支持通过 Assistant API 创建的智能体 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持多维自动化评测，包括：
  - **文本输出**（准确性、简洁性、合规性、格式校验等）；
  - **执行轨迹**（步骤逻辑、工具调用成功率、错误定位、观察信息增益等），需评测集包含 `trajectory` 类型字段 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)；
  - **多模态内容**（图文音视频理解与生成质量），需评测集字段类型为 `多模态` [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)。
- **优化能力**：支持基于调试结果、评测任务低分样本、线上 Trace 数据或评测集进行 Prompt 智能优化，并提供多版本对比与一键采纳功能。
- **安全治理**：提供“量·挡·记”闭环能力——自动盘点 Agent 关联资产（模型、工具、知识库、记忆等）；默认启用输入输出内容安全、RAG 文件预扫描、Managed Agent 沙箱隔离等原生防护；高级防护支持提示词攻击检测、敏感数据外泄识别等 7 类策略 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

> **注意**：文档中多次提及“应用观测目前暂无 API”，但 Security 模块明确提供了 `/api/v1/agentstudio/security` 下的 7 个 RESTful 接口（如 `/overview`, `/asset_summary`, `/policies`），说明可观测性能力虽无专用 API，但安全治理能力已开放 API 支持。

## 关键参数

- **观测配置**：首次使用需主账号完成三项前置操作——授权 OpenTelemetry 服务角色、开通 OpenTelemetry 服务、初始化 LogStore；子账号需主账号预先配置权限 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集字段映射**：评估器变量必须与评测集字段或应用输出字段**数据类型严格一致**（如 `trajectory` 变量只能映射到 `trajectory` 类型列，`多模态` 变量只能映射到 `多模态` 类型列），否则无法保存配置 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全策略作用域**：所有安全策略配置对当前阿里云账号下**全部 Agent 全局生效**，不区分业务空间，修改前需评估影响范围 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。
- **标签类型约束**：分类标签最多支持 20 个筛选项；数字标签支持 Double 类型；文本标签单条内容最多 10000 字符；所有标签均支持在评测任务和应用观测中复用 [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)。

## 使用方式

1. **观测接入**：在控制台「应用观测」页面开启目标应用观测 → 输入测试问题触发 Trace → 在 Trace 列表中验证节点、模型/工具事件、耗时与 Token 消耗 → 进入「监控统计」页查看 QPM、错误率、TTFT 等分钟级指标 → 配置告警规则（基于预置模板或自定义）实现异常主动发现 [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)。
2. **评测构建**：创建评测集（支持空建或文件上传）→ 发布评测集（草稿不可用于评测）→ 创建评估器（选用预置模板或自定义 LLM/Code 评估器）→ 创建评测任务（关联评测集版本、应用、评估器并完成变量映射）→ 查看数据明细与指标统计，支持人工标签补充标注 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
3. **优化执行**：在「应用优化」页面选择目标应用 → 可选路径包括：① 多版本 Prompt 对比调试；② 基于单条/多条调试结果 + 人工反馈生成优化建议；③ 基于已发布评测集或已完成评测任务的低分样本定向优化 → 查看对比结果后点击「采纳」更新当前编辑中的 Prompt（**不自动发布应用**） [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
4. **安全防护**：默认防护随 Agent 使用模块（如 RAG、Memory）自动生效；高级防护需在「Security > 高级防护 > 安全策略」页面完成服务授权后开通（限时免费），策略全局生效；风险事件与审计日志在「风险与审计」页面集中查看，支持按等级、节点类型筛选 [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)。

## 限制和注意事项

- **观测限制**：应用观测不支持 Assistant API 创建的智能体；Trace 数据同步延迟为分钟级；导出数据最大支持 30 天范围；单条轨迹 JSON 大小不能超过 1 MB [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **评测限制**：评测集最多保存 10 个版本；单个评测任务最多添加 10 个评估器；评测任务创建后**不可修改**应用、评测集等核心配置，仅支持追加人工标签；多模态文件上传有大小限制（图片 ≤20 MB，音频/视频 ≤100 MB） [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **优化限制**：采纳优化结果仅更新当前编辑中的 Prompt，**不会自动发布应用**，需开发者手动发布；基于评测集优化时，若评测集字段映射错误，将直接影响系统对问题模式的判断 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全限制**：高级防护当前**暂不支持自动阻断或拦截风险**，仅提供监测与告警能力；风险与审计页面展示该账号下**全部 Agent 的数据，不区分业务空间**；CLI 命令 `bl agents security overview` 固定查询最近 24 小时数据，不支持自定义时间范围 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
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


