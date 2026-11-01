# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的统一治理能力集合，涵盖可观测性、质量评测、智能优化与安全防护四大核心维度。它基于 OpenTelemetry GenAI 标准构建，支持框架中立接入，帮助开发者从“黑盒运行”走向“透明决策”，实现对 Agent 行为、输出、风险与演进的系统化管控。

## 支持的模型/功能

agent governance 由两大子系统构成：**Evolution（智能体治理平台）** 和 **Security（内生安全防护）**，二者协同覆盖开发、测试、上线与运维各阶段。

- **Evolution** 提供全链路观测、多维自动化评测与 Prompt 智能优化能力：
  - 支持智能体应用（Agent 1.0 / 2.0）与工作流应用的 Trace 采集与可视化，但[目前暂不支持通过 Assistant API 创建的智能体应用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)；
  - 支持轨迹（Trajectory）数据结构的完整建模与评测，可用于评估执行过程可靠性，相关能力在[2026-10-21版本正式上线](../../raw/application-user-guide/agent-governance/agenteval/agenteval-changelog.md)；
  - 提供预置 LLM/Code 类评估器（如轨迹准确性、动作循环检测、回答忠实度等），也支持自定义 LLM 评估器，其 Prompt 编辑与评分规则配置需严格匹配数据类型要求。

- **Security** 提供默认防护与高级防护双层安全能力：
  - 默认防护自动生效，覆盖 Flow Agent（输入输出内容安全）、Managed Agent（沙箱隔离、凭证隔离）、RAG（知识库内容检测）、Memory（记忆读写检测）及 Store（MCP/Skill 组件扫描）五大模块；
  - 高级防护提供 7 项可按需启用的策略（如提示词攻击、敏感数据外泄、RAG 数据投毒等），当前处于[限时免费阶段](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)，配置后对账号下全部 Agent 全局生效。

> **注意**：文档中关于“应用观测目前暂无 API”的说明（见 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)）与 Security 模块明确提供的 7 个 RESTful API（如 `/api/v1/agentstudio/security/overview`）存在能力边界差异——前者特指 Evolution 的观测数据导出无开放 API，后者是 Security 独立提供的治理接口，二者不矛盾。

## 关键参数

| 功能模块 | 参数名 | 说明 | 来源依据 |
|----------|--------|------|----------|
| **观测告警** | `告警检查周期` | 单位为秒，必须为 ≥0 的整数，默认 60 秒；影响告警触发频率 | [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md) |
| **评测集** | `schema_version` | 轨迹数据必需字段，标识轨迹结构版本（如 `"ATIF-v1.8"`）；类型不匹配将导致导入失败 | [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md) |
| **LLM 评估器** | `评分范围` | 决定评估器打分尺度（如 `0-100` 或 `1-5`），该值会注入系统提示词，必须与 Prompt 中的评分指令严格一致 | [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md) |
| **安全高级防护** | `Credit 额度` | 每个运行中 Agent 席位每日默认 300 Credits，超量部分按 `0.0015 元/Credit` 计费；有效期 24 小时，不结转 | [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md) |

## 使用方式

1. **接入与开通**  
   - Evolution：首次使用需在[应用观测页面](https://bailian.console.aliyun.com/loop/app-observe)完成三步配置——授权 OpenTelemetry 服务角色、开通 OpenTelemetry 服务、初始化 LogStore 存储（主账号操作，分钟级生效）；  
   - Security：默认防护随 Agent 使用自动启用；高级防护需在[安全策略页面](https://bailian.console.aliyun.com/loop/security/policy)点击「立即开通」，完成服务关联角色授权。

2. **核心流程**  
   - **观测 → 评测 → 优化闭环**：在应用观测中开启追踪 → 将典型 Trace 批量导入评测集 → 关联轨迹评估器发起评测任务 → 基于低分样本在应用优化中发起「基于评测任务优化」，一键采纳优化后 Prompt；  
   - **安全治理闭环**：通过[防护总览](https://bailian.console.aliyun.com/loop/security/overview)掌握拦截统计 → 在[Agent 资产](https://bailian.console.aliyun.com/loop/security/assets)盘点攻击面 → 启用[安全策略](https://bailian.console.aliyun.com/loop/security/policy)增强防护 → 在[风险与审计](https://bailian.console.aliyun.com/loop/security/audit)中定位与追溯事件。

3. **CLI 与 API 快速操作**  
   - 使用百炼 CLI 查询安全状态：`bl agents security overview`（防护总览）、`bl agents security alerts --risk-level high`（高风险告警）；  
   - Security 模块提供标准 RESTful API（前缀 `/api/v1/agentstudio/security`），支持程序化获取资产摘要、策略状态与告警日志。

## 限制和注意事项

- **功能限制**：  
  - 应用观测数据同步延迟为分钟级，Trace 最长保留 30 天；导出仅支持 JSONL/EXCEL 格式；  
  - 评测集最多保存 10 个版本，超出后自动覆盖；单条轨迹数据大小不可超过 1 MB；  
  - 安全高级防护的「内容安全」策略需在开通后手动启用，其余 6 项默认开通；  
  - CLI 命令 `bl agents security alerts` 展示的是**账号下全部 Agent** 的风险，不区分业务空间（见 [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)）。

- **关键注意事项**：  
  - 评测任务创建后，应用、评测集、评估器映射等配置**不可修改**，仅支持新增人工标签；需变更配置请新建任务；  
  - 字段映射是评测与优化的核心前提：评估器变量类型必须与评测集列类型严格一致（如轨迹变量须映射到 `trajectory` 类型列），否则无法保存配置；  
  - 安全策略配置全局生效，修改前务必评估对所有 Agent 的影响；高级防护当前**不支持自动阻断风险**，仅提供监测与告警能力。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agent-governance/agenteval/agenteval-changelog.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)
- [更新日志](../../raw/application-user-guide/agent-governance/security-guide/changelog.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)


