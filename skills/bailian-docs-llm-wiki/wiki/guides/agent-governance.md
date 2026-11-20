# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力集合，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大核心支柱，并与内生安全防护深度集成。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现即插即用，支持从开发调试、线上运行到效果迭代的闭环管理。

## 支持的模型/功能

- **观测能力**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路追踪，完整记录 Prompt 解析、模型调用（含百炼内置及外部模型）、工具执行（MCP/Skill）、向量检索、记忆读写等环节；支持 Trace 数据导出（JSONL/EXCEL）、监控统计（QPM、Token、延时、错误率）和限流分析。> **注意**：[应用观测](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md) 明确指出“暂不支持通过 Assistant API 创建的智能体”，该限制在多处文档中一致，无矛盾。
- **评测能力**：支持三类评测对象：
  - **输出评测**：对最终文本/多模态输出进行准确性、合规性、格式等维度评估；
  - **轨迹评测（Trajectory）**：基于结构化执行时序数据评估步骤逻辑、工具调用成功率、观察信息增益等，需评测集包含 `trajectory` 类型字段；
  - **多模态评测**：支持图文、音视频混排内容的理解与生成质量评估，需评测集包含 `多模态` 类型字段。
  预置评估器覆盖 LLM 与 Code 两类，如 [轨迹准确性](raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)、图片指令遵循、多模态幻觉检测等。
- **优化能力**：支持基于调试结果、评测任务低分样本或线上 Trace 数据驱动的 Prompt 智能优化，并提供多版本对比调试与一键采纳功能。
- **安全治理**：提供“量·挡·记”闭环能力——自动盘点 Agent 关联资产（模型、工具、知识库、记忆等）、默认启用内容安全/I/O 拦截、RAG 文件预扫描等原生防护，并支持 7 项高级策略（如提示词攻击、敏感数据外泄）按需开启，所有策略对账号下全部 Agent 全局生效 [安全策略](raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 关键参数

- **观测配置**：首次使用需通过“应用观测配置”授权 OpenTelemetry 服务角色、开通服务并初始化 LogStore（主账号操作，子账号需授权）。
- **评测集字段映射**：创建评测任务时，评估器变量必须与评测集字段或应用输出字段完成**类型严格匹配**（如 `trajectory` 变量只能映射到 `trajectory` 类型列），否则无法保存配置 [评测任务](raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全策略作用域**：所有高级防护策略（如 RAG 数据投毒、工具调用安全）配置后对**当前阿里云账号下全部 Agent 全局生效**，不区分业务空间，修改前需评估影响范围 [安全策略](raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。
- **标签类型约束**：用于评测标注的标签分为分类、布尔值、数字、文本四类，其筛选条件（如“属于”、“大于”）与类型强绑定，影响后续数据筛选与指标统计 [标签管理](raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)。

## 使用方式

- **观测**：在应用列表点击“开启观测” → 输入测试问题触发 Trace → 进入详情页查看 Trace 列表、监控统计、限流统计；可将 Trace 批量导入评测集用于回流验证。
- **评测**：先创建并**发布**评测集（草稿不可用）→ 选择已发布版本 → 关联目标应用 → 配置评估器并完成变量映射 → 启动任务 → 查看数据明细（含轨迹预览）与指标统计（得分分布、回归对比）。
- **优化**：支持三条路径：
  - *多版本对比*：在编辑区调整 Prompt，发起多组调试，直观比对回复差异；
  - *基于调试反馈*：发送测试问题 → 选择调试结果 → 输入具体人工反馈 → 生成优化 Prompt；
  - *基于评测数据*：选择已发布的评测集或已完成的评测任务 → 勾选低分/失败样本 → 配置字段映射 → 生成优化 Prompt。
- **安全**：默认防护随 Agent 使用对应模块（如 RAG、Memory）自动生效；高级防护需在 Security 控制台完成服务授权后，于“高级防护 > 安全策略”页面启用具体策略；风险事件与审计日志统一在“风险与审计”页面查看与导出。

## 限制和注意事项

- **API 缺失**：应用观测功能目前**无公开 API**，所有操作需通过控制台完成 [应用观测](raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集状态要求**：评测任务必须关联**已发布**的评测集版本，草稿状态无法选用；评测集最多保留 10 个历史版本，超出后自动覆盖 [创建与管理](raw/_short/agenteval-evaluation-set-946c810bda606877.md)。
- **轨迹数据规范**：单条轨迹 JSON 大小不得超过 1 MB，且必须为合法 JSON 对象；评测集若含 `trajectory` 字段，其数据必须符合 ATIF-v1.8 等指定 schema，否则导入或评测会失败 [添加轨迹评测数据](raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)。
- **安全策略全局性**：高级防护策略（如“提示词攻击”、“工具调用安全”）一旦启用，将对账号下**所有 Agent 生效**，无法按业务空间或单个 Agent 细粒度控制，此设计已在 [安全策略](raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md) 中明确强调。
- **CLI 与 API 范围**：Security 模块 CLI 命令（如 `bl agents security overview`）和 API（如 `/api/v1/agentstudio/security/overview`）仅提供查询能力，**不支持开通、配置或处置防护策略**，相关操作必须通过控制台完成 [API 参考](raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


