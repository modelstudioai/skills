# agent governance

Agent Governance 是百炼平台面向 AI Agent 全生命周期提供的核心治理能力体系，涵盖可观测性（Observability）、可评测性（Evaluation）、可优化性（Optimization）与安全性（Security）四大支柱。它通过 OpenTelemetry 标准链路接入、结构化轨迹分析、多维自动评估器及内生安全防护，帮助开发者从“黑盒运行”走向“透明决策”，支撑 Agent 的质量闭环迭代与合规稳定交付。

## 支持的模型/功能

- **观测能力**：支持智能体应用（Agent 1.0 / 2.0）和工作流应用的全链路 Trace 可视化，覆盖 Prompt 解析、大模型调用（含 TTFT、[Token](../concepts/token.md) 消耗）、工具执行（MCP）、向量检索、记忆读写等环节；但**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置 LLM/Code 类评估器（如「轨迹准确性」「动作循环检测」「回答忠实度」），支持文本、Agent 输出、执行轨迹三类评估对象；轨迹评测需评测集包含 `trajectory` 类型字段，并映射至评估器变量 [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持三种 Prompt 优化路径：① 多版本对比调试；② 基于单条或多条调试结果 + 人工反馈生成优化建议；③ 基于已发布评测集或评测任务中的低分样本定向优化 [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)。
- **安全能力**：默认防护随 Agent 使用模块（Flow Agent、RAG、Memory 等）自动生效；高级防护提供 7 项策略（如提示词攻击、敏感数据外泄、RAG 数据投毒），需服务授权后开通，当前处于限时免费阶段 [Security](../../raw/application-user-guide/agent-governance/security-guide.md)。

> **注意**：文档中多次提及“应用观测目前暂无 API”，而 Security 模块明确提供了 `/api/v1/agentstudio/security` 下的 7 个 RESTful 接口（如 `/overview`, `/asset_summary`, `/policies`）[API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)。二者能力边界清晰：观测数据仅限控制台查看与导出（JSONL/EXCEL），安全数据则开放完整 API 访问能力。

## 关键参数

| 功能模块 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **告警管理** | `持续时间` / `告警检查周期` | 触发告警需指标连续异常的时长（分钟）；规则轮询频率（秒） | 持续时间必填；检查周期 ≥ 0 整数，默认 60 秒 |
| **评测集** | `数据类型`（列级） | 支持 `String`/`Number`/`Boolean`/`Object`/`Array`/`轨迹` | `轨迹` 类型列必须用于轨迹评估器；类型不匹配将导致导入/映射失败 |
| **评估器** | `评分范围` / `通过阈值` | 决定打分尺度（如 0–100）与 Pass/Fail 判定线 | 阈值须在评分范围内；精细评估推荐大范围（0–100），快速分类推荐小范围（1–5） |
| **安全策略** | `Credit 额度` | 每个运行中 Agent 每日默认 300 Credits，超量按 0.0015 元/Credit 计费 | Credit 有效期 24 小时，不结转；消耗量与检测内容 [Token](../concepts/token.md) 量正相关 |

## 使用方式

1. **接入准备**：  
   - 观测：主账号需授权 OpenTelemetry 服务角色、开通服务并初始化 LogStore [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)；  
   - 安全：默认防护自动生效；高级防护需在 **Security > 高级防护 > 安全策略** 页面完成服务授权并开通 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

2. **核心操作流**：  
   - **观测 → 评测 → 优化**闭环：在应用观测中筛选异常 Trace → 批量添加至评测集 → 关联轨迹评估器发起评测任务 → 基于低分样本创建「基于评测任务优化 Prompt」任务 → 采纳优化结果；  
   - **安全审计**：通过 CLI 快速查询风险（`bl agents security alerts --risk-level high`）或调用 `/agent_logs` 接口获取告警详情 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)。

3. **轨迹专用流程**：  
   - 创建评测集时选择「轨迹」场景，自动生成 `input`/`reference_output`/`trajectory` 表结构；  
   - 单条新增时通过「轨迹样例」插入 JSON 模板，或「通过 TraceID 导入」复用观测数据；  
   - 评测任务中配置评估器时，必须将 `trajectory` 变量映射至评测集的 `trajectory` 列（类型严格一致）。

## 限制和注意事项

- **观测限制**：Trace 数据同步延迟为分钟级；关闭观测后历史数据停止同步，重新开启仅同步新增数据；导出数据最大支持 30 天范围 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。  
- **评测限制**：评测集最多保存 10 个版本，超出后自动覆盖；评测任务创建后不可修改应用、评测集等核心配置，仅支持追加人工标签 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。  
- **安全限制**：高级防护策略配置对**账号下全部 Agent 全局生效**，不区分业务空间；当前高级防护仅提供风险监测与告警，**暂不支持自动阻断或拦截风险行为** [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。  
- **通用限制**：轨迹 JSON 单条大小 ≤ 1 MB；评测集文件上传单个 ≤ 20 MB；标签名称长度 ≤ 50 字符；告警名称 ≤ 50 字符 [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [更新日志](../../raw/application-user-guide/agent-governance/agenteval/agenteval-changelog.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [计费说明](../../raw/application-user-guide/agent-governance/security-guide/section-ref/billing.md)
- [更新日志](../../raw/application-user-guide/agent-governance/security-guide/changelog.md)


