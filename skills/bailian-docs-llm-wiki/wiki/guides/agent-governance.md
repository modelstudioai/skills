# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的核心治理能力体系，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大支柱，并与内生安全防护深度集成。它基于 OpenTelemetry GenAI 标准实现框架中立接入，支持对智能体（Agent 1.0/2.0）、工作流等应用的链路追踪、质量量化、Prompt 智能迭代及风险闭环管控，为开发者提供从开发调试到线上运维的一站式治理基础设施。

## 支持的模型/功能

- **观测能力**：支持全链路 Trace 可视化（Prompt 解析、模型调用、工具执行、记忆读写），覆盖延时、Token 消耗、QPM、首 Token 耗时（TTFT）等指标；支持限流统计与告警规则配置。当前仅支持通过百炼控制台创建的智能体应用和工作流应用，**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持文本级（准确性、合规性、简洁性）与轨迹级（步骤逻辑、工具调用成功率、观察信息增益等）双维度自动化评测；提供预置 LLM/Code 评估器（如「轨迹准确性」「动作循环检测（ATIF）」）及自定义评估器能力 [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持基于调试对话、评测任务结果、线上 Trace 数据三种路径驱动 Prompt 迭代；提供多版本对比调试、人工反馈引导生成、一键采纳等闭环操作 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全治理**：默认启用内容安全 I/O 拦截、RAG 文件预扫描、Skill 静态扫描等原生防护；高级防护提供提示词攻击检测、敏感数据外泄识别等 7 类可选策略，全局生效且当前限时免费 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，但文档 27 列出了 `/api/v1/agentstudio/security` 下的 Security 模块 API（含防护总览、资产、策略、告警等）。二者所属模块不同（agenteval vs security），不构成直接矛盾；但需注意 **应用观测（agenteval-observability）本身无公开 API**，其数据导出仅支持 JSONL/EXCEL 手动下载。

## 关键参数

- **Trace 相关**：`Request ID`、`Trace ID`、`Span ID` 为必选搜索字段；`schema_version`（如 `ATIF-v1.8`）决定轨迹结构兼容性 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **评测集字段**：轨迹评测集必须包含 `input`（String）、`reference_output`（String）、`trajectory`（轨迹类型）三列；字段映射须严格匹配数据类型，否则导入失败 [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)。
- **评估器配置**：LLM 评估器需指定评分范围（如 `0-100`）与通过阈值；Code 评估器需明确定义入参（如 `query`, `response`, `trajectory`）并确保与评测集字段一致 [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **告警规则**：`持续时间`（分钟）、`告警检查周期`（秒，默认 60）、`统计周期`（1–10080 分钟）为关键阈值参数；预置模板（如「QPM 限流大于 6000」）优先推荐使用 [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)。

## 使用方式

1. **接入观测**：主账号完成 OpenTelemetry 服务角色授权、开通服务、初始化 LogStore 后，在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)页面开启目标应用观测；Trace 数据分钟级同步，支持按 ID 搜索与 30 天内筛选。
2. **构建评测**：
   - 创建评测集（支持空建或文件上传），选择「轨迹」场景自动配置表结构；
   - 基于预置模板或自定义创建评估器，注意校验必选参数（如轨迹评估器需 `trajectory` 字段）；
   - 创建评测任务，绑定已发布评测集版本、目标应用，并完成评估器变量到评测集字段/应用输出的**类型一致映射**。
3. **驱动优化**：
   - 在「应用优化」页面选择应用，可发起多版本 Prompt 对比调试；
   - 或基于已选调试结果+人工反馈、已发布评测集、已完成评测任务的低分样本，启动智能优化任务；
   - 生成结果支持与当前 Prompt 并排对比，采纳后仅更新草稿态 Prompt，**不自动发布**。
4. **配置安全**：默认防护自动生效；如需高级策略，进入 **Security > 高级防护 > 安全策略** 开通服务并启用对应项（如「提示词攻击」），策略对账号下所有 Agent 全局生效。

## 限制和注意事项

- **功能限制**：应用观测无 API 接口；Assistant API 创建的智能体不可观测；评测集最多保存 10 个版本，超出后自动覆盖；单条轨迹 JSON 不得超过 1 MB [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **数据一致性**：评测任务中评估器变量与映射字段**数据类型必须严格一致**（如轨迹变量不可映射至 String 列），否则无法保存配置；字段映射错误将导致评分失效 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **权限与范围**：OpenTelemetry 配置需主账号操作；安全策略配置全局生效，不区分业务空间；风险与审计页面展示账号下全部 Agent 数据，不按业务空间隔离 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。
- **成本提示**：评测任务调用大模型产生的 Token 按标准计费；安全模块 CLI 与 API 查询不产生额外费用，但防护本身（如内容安全扫描）可能涉及资源消耗。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)


