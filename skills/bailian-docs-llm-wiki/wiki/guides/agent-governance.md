# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的治理能力集合，涵盖可观测性、自动化评测、智能优化与内生安全四大支柱。它通过统一的数据标准（如 OpenTelemetry GenAI）、预置评估器与策略引擎，帮助开发者在开发、测试、上线及运维阶段持续验证、诊断和提升 Agent 的可靠性、合规性与业务效果。

## 支持的模型/功能

- **可观测性**：支持 Agent 1.0、Agent 2.0 和工作流应用的全链路 Trace 上报与可视化，覆盖 Prompt 解析、模型调用（含 TTFT、[Token](../concepts/token.md) 消耗）、工具执行（MCP/自定义 API）、向量检索、记忆读写等节点；不支持通过 Assistant API 创建的智能体 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持三类评测对象：
  - **输出评测**：基于文本、多模态（图片/音频/视频混排）输入与期望输出的端到端质量评估；
  - **轨迹评测**：以 ATIF 标准结构化 JSON 为输入，评估步骤逻辑、[工具调用](../concepts/tool-calling.md)成功率、观察信息增益等执行过程可靠性 [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)；
  - **多模态评测**：支持图片美学、指令遵循、画质、文字渲染正确性等维度，要求评测集字段类型为“多模态” [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)。
- **优化路径**：支持三种 Prompt 优化触发方式：基于单条/多条调试结果的人工反馈、基于已发布评测任务结果、基于线上 Trace 数据回流生成的评测集。
- **安全防护**：提供默认防护（自动生效）与高级防护（需授权开通）双层机制，覆盖内容安全（I/O 检测）、提示词攻击、敏感数据外泄、RAG 数据投毒、[工具调用](../concepts/tool-calling.md)安全、身份凭证滥用等 7 类风险策略。

> **注意**：文档中关于“应用观测目前暂无 API”的表述（见 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)）与 Security 模块明确提供 `/api/v1/agentstudio/security` 系列接口（含 `/overview`、`/asset_summary` 等）存在功能边界矛盾。实际可观测数据需通过控制台或 CLI 获取，Security 相关指标可通过 API 查询，二者能力范围不同，非同一 API 体系。

## 关键参数

- **Trace 上报粒度**：监控与限流指标更新频率为分钟级；Trace 数据同步延迟通常为分钟级，高峰期可能延长。
- **评测集版本管理**：单个评测集最多保存 10 个发布版本，超出后自动覆盖旧版本；草稿状态不可用于评测任务 [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)。
- **轨迹数据约束**：单条轨迹 JSON 大小上限为 1 MB；必须为合法 JSON 对象，且 `schema_version` 需符合 ATIF 规范（如 `"ATIF-v1.8"`）。
- **多模态字段校验**：图片（JPG/JPEG/PNG，≤20 MB）、音频（MP3，≤100 MB）、视频（MP4/MOV，≤100 MB）；文本字段 ≤10000 字符。
- **安全策略作用域**：所有高级防护策略配置对账号下全部 Agent **全局生效**，不区分业务空间 [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)。

## 使用方式

1. **接入观测**：主账号进入[应用观测配置](https://bailian.console.aliyun.com/loop/app-observe)，完成 OpenTelemetry 服务角色授权、服务开通与 LogStore 初始化；在应用列表点击“开启观测”，输入测试问题触发 Trace 上报。
2. **构建评测集**：
   - 场景选择“轨迹”或“多模态”，配置对应字段类型（`trajectory` 或 `多模态`）；
   - 通过“单条新增”粘贴 JSON 轨迹或上传媒体文件，或通过“批量导入”上传 CSV/XLSX；
   - 发布评测集后方可用于评测任务。
3. **创建评测任务**：
   - 选择已发布评测集版本与目标应用；
   - 为每个评估器变量配置映射：轨迹变量 → 评测集 `trajectory` 列，多模态变量 → 评测集 `多模态` 列，类型必须严格一致；
   - 最多添加 10 个评估器，建议组合 LLM（如相关性）与 Code（如格式校验）评估器。
4. **启动优化**：
   - 在“调试&反馈优化”中发送问题，选择代表性调试结果，填写具体问题描述（如“未按 JSON 格式输出”）；
   - 在“基于评测集优化”中选择已发布的高质量评测集版本；
   - 生成对比后，点击“采纳”仅更新当前编辑区 Prompt，**不会自动发布应用**。
5. **配置安全告警**：在[告警管理](https://bailian.console.aliyun.com/loop/alert-manage)中基于预置模板（如“QPM 限流大于 6000”）快速创建规则，设置通知时段与重复策略。

## 限制和注意事项

- **权限要求**：应用观测首次开通必须使用主账号；子账号需主账号预先配置 OpenTelemetry 相关权限。
- **数据时效性**：Trace 列表最长可查 30 天历史数据；监控统计聚合粒度支持分钟/小时/天，但原始数据点非实时。
- **评测集字段强约束**：评估器变量映射时，若类型不匹配（如将字符串字段映射给轨迹变量），配置无法保存；务必在创建评测集前确认所选评估器的必填参数（如“问答相关性”需 `query` 和 `response` 字段）。
- **安全策略开通前提**：高级防护处于限时免费阶段，但需先完成服务授权；开通后策略全局生效，修改前须评估对全部 Agent 的影响。
- **CLI 与 API 差异**：`bl agents security overview` 命令固定查询最近 24 小时数据，而 `/api/v1/agentstudio/security/overview` 接口无时间窗口硬编码，实际行为以接口文档为准；两者均不触发新扫描或防护动作。

## 来源文档

- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
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
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)


