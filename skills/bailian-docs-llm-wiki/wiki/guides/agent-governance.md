# agent governance

Agent Governance 是百炼平台面向 AI Agent 全生命周期提供的治理能力集合，涵盖可观测性、可评测性、可优化性与安全性四大支柱。它通过统一的数据标准（OpenTelemetry GenAI）、原生集成的运行时支持和开箱即用的分析工具，帮助开发者在开发、测试、上线与运维各阶段实现质量量化、问题定位与风险防控。核心能力围绕 Evolution（观测/评测/优化）与 Security（资产/防护/审计）两大子系统展开。

## 支持的模型/功能

- **Evolution 全链路治理**：支持 Agent 1.0、Agent 2.0 和工作流应用；**不支持**通过 Assistant API 创建的智能体应用 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测对象类型**：覆盖文本、轨迹（Trajectory）、多模态（图片/音频/视频混排）三类核心输出形态。轨迹评测需评测集包含 `trajectory` 字段，多模态评测需字段类型为 `多模态` [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)、[添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)。
- **Security 内生防护**：默认覆盖 Flow Agent（输入输出内容安全）、Managed Agent（沙箱隔离、工具调用拦截）、RAG（知识库内容安全）、Memory（记忆读写安全）、Store（MCP/Skill 组件静态扫描）五大模块 [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)。

> **注意**：文档中关于“应用观测目前暂无 API”的表述（见 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)）与 Security 模块明确提供 7 个 RESTful API（如 `/api/v1/agentstudio/security/overview`）存在功能范围差异，此处特指 Evolution 的观测数据面暂未开放写入或 Trace 查询类 API，而 Security 的读取类 API 已完备。

## 关键参数

- **观测配置参数**：首次使用需完成三项初始化：OpenTelemetry 服务角色授权、OpenTelemetry 服务开通、LogStore 初始化；所有操作需主账号执行，子账号需额外配置权限 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集字段映射**：评估器变量与评测集字段/应用输出字段**必须类型一致**（如 `trajectory` 变量只能映射到 `trajectory` 类型列），否则无法保存配置；单个评测任务最多支持 10 个评估器 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全策略作用域**：所有高级防护策略（如提示词攻击、敏感数据外泄）配置后对**当前阿里云账号下全部 Agent 全局生效**，不区分业务空间 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 使用方式

- **观测**：在应用列表点击“开启观测” → 输入测试问题触发 Trace 上报 → 进入详情页查看 Trace 列表、监控统计（QPM/Token/延时）、限流统计；Trace 数据可一键导出为 JSONL/EXCEL 或直接回流至评测集 [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)。
- **评测**：先创建并**发布**评测集（草稿不可用）→ 选择预置或自定义评估器 → 创建评测任务并严格完成变量映射 → 批量运行后分析得分分布、回归对比及异常样本 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **优化**：支持三条路径：① 多版本 Prompt 对比调试；② 基于单条/多条调试结果 + 人工反馈生成优化建议；③ 基于已发布的评测集或已完成的评测任务（尤其低分样本）发起智能优化；所有“采纳”操作仅更新当前编辑中的 Prompt，**不会自动发布应用** [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全**：默认防护随 Agent 使用对应模块（如启用 RAG 即自动激活知识库扫描）自动生效；高级防护需手动开通服务授权，并在安全策略页启用具体项；风险与审计数据按账号聚合，不区分业务空间 [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)。

## 限制和注意事项

- **观测限制**：Trace 数据同步延迟为分钟级；关闭观测后历史数据停止同步，重新开启仅同步新增数据；Trace 导出最大时间范围为 30 天 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测限制**：评测集最多保存 10 个版本，超出后自动覆盖旧版本；轨迹数据单条大小上限为 1 MB；多模态文件上传限制：图片 ≤20 MB（JPG/JPEG/PNG），音频 ≤100 MB（MP3），视频 ≤100 MB（MP4/MOV） [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)、[添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)、[添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)。
- **安全限制**：高级防护当前**暂不支持自动阻断或拦截风险**，仅提供监测与告警；CLI 命令 `bl agents security overview` 固定查询最近 24 小时数据，不支持自定义时间范围 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。
- **通用注意事项**：标签管理中，分类标签最多支持 20 个筛选项；评测任务创建后配置不可修改，如需调整需新建任务；Security 模块所有页面（除 CLI 外）均不区分业务空间，数据按账号全局展示 [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)、[风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
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
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)


