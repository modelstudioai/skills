# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力集合，涵盖可观测性、可评测性、可优化性与安全性四大支柱。它通过标准化数据采集（基于 OpenTelemetry GenAI）、结构化评估体系与内生安全防护，帮助开发者在开发、上线与运维各阶段实现质量量化、问题定位与风险防控，无需框架改造即可快速接入。

## 支持的模型/功能

- **观测能力**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路 Trace 可视化，覆盖 Prompt 解析、模型调用（含百炼内置及外部模型）、工具执行（MCP/Connector）、向量检索、记忆读写等节点；支持延时、[Token](../concepts/token.md)、QPM、错误率等分钟级监控与限流统计 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持三类评测对象：
  - **输出评测**：基于文本、[多模态](../concepts/multi-modal.md)（图片/音频/视频混排）输入与期望输出的端到端质量评估；
  - **轨迹评测**：基于结构化 JSON 轨迹（`ATIF-v1.8` 格式）评估执行过程可靠性，如步骤逻辑、工具调用成功率、观察信息增益等 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)；
  - **[多模态](../concepts/multi-modal.md)评测**：支持图文音视频理解与生成效果评估，字段类型为 `Array<Object>`，含 `text`/`image_url`/`audio_url`/`video_url` 等元素 [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)。
- **优化能力**：支持基于调试对话、评测任务结果、线上 Trace 数据三种路径驱动 Prompt 智能优化，并提供多版本对比与一键采纳功能。
- **安全能力**：提供“量·挡·记”闭环防护：默认防护自动覆盖 Flow Agent（I/O 内容安全）、Managed Agent（沙箱/凭证隔离）、RAG（知识库预扫描）、Memory（内容检测）、Store（Skill 静态扫描）；高级防护支持提示词攻击、敏感数据外泄等 7 类可配置策略 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

> **注意**：文档 5 明确指出“应用观测目前暂无 API”，但文档 28 列出了 `/api/v1/agentstudio/security` 下的 7 个 Security 模块 API。二者所属模块不同（agenteval vs security），不构成矛盾；但需注意 agenteval 观测能力当前仅限控制台使用，无对应开放 API。

## 关键参数

- **观测配置**：首次启用需主账号完成三项前置操作——授权 OpenTelemetry 服务角色、开通 OpenTelemetry 服务、初始化 LogStore；子账号需主账号额外授权 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集字段映射**：评估器变量必须与评测集字段或应用输出字段**类型严格一致**（如轨迹变量 → 轨迹类型列，[多模态](../concepts/multi-modal.md)变量 → 多模态类型列），否则无法保存配置 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全策略作用域**：所有安全策略配置对账号下全部 Agent **全局生效**，不区分业务空间，修改前需评估影响范围 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。
- **标签类型约束**：分类/布尔值标签支持筛选条件“属于/不属于”；数字标签支持“等于/大于/小于”等数值比较；文本标签仅支持“包含/不包含” [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)。

## 使用方式

1. **观测接入**：在控制台「应用观测」页面开启目标应用观测 → 发送测试请求生成 Trace → 在 Trace 列表中按 `Request ID`/`Trace ID` 搜索并查看详情 → 可导出 JSONL/EXCEL 或一键回流至评测集。
2. **评测执行**：
   - 创建评测集（选择场景：智能体/工作流/轨迹/多模态/自定义）→ 发布版本；
   - 创建评测任务 → 关联已发布评测集与目标应用 → 配置评估器（必填变量映射）→ 启动批量评测；
   - 在「数据明细」页查看自动评分与轨迹详情，在「指标统计」页分析得分分布与回归对比。
3. **Prompt 优化**：
   - **调试反馈路径**：发送测试问题 → 选择调试结果 → 输入具体问题与改进方向 → 生成并对比优化版 Prompt → 采纳至编辑区；
   - **评测集路径**：选择已发布评测集版本 → 勾选代表性样本 → 配置字段映射（应用输入/输出/轨迹）→ 启动优化；
   - **评测任务路径**：选择已完成的评测任务 → 筛选低分/失败样本 → 启动定向优化。
4. **安全管理**：
   - 默认防护自动生效，无需操作；
   - 高级防护需先完成服务授权 → 进入「安全策略」页面启用所需策略（如提示词攻击、敏感数据外泄）→ 在「风险与审计」查看告警与日志。

## 限制和注意事项

- **观测限制**：不支持通过 Assistant API 创建的智能体；Trace 数据最长保留 30 天；监控/限流指标更新频率为分钟级；告警规则最多添加 50 个应用 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测限制**：评测集草稿不可用于评测任务，必须发布后才能选用；单条轨迹数据大小 ≤ 1 MB；多模态文件单个限制：图片 ≤ 20 MB、音频 ≤ 100 MB、视频 ≤ 100 MB [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **优化限制**：采纳优化结果仅更新当前编辑中的 Prompt，**不会自动发布应用**；多模态评测集字段映射需确保 URL 可访问，否则评估器可能失败。
- **安全限制**：高级防护当前**不支持自动阻断风险**，仅提供监测与告警；CLI 命令 `bl agents security overview` 固定查询最近 24 小时数据，不支持自定义时间范围 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。
- **通用限制**：评测任务创建后，其关联的应用、评测集、评估器配置均不可修改；如需调整，须新建任务。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
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
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)


