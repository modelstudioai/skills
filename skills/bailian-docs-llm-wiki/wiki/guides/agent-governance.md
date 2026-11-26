# agent governance

agent governance 是百炼平台面向 AI Agent 全生命周期提供的治理能力集合，涵盖可观测性（Observability）、可评测性（Evaluation）与可优化性（Optimization）三大支柱，支撑开发者从开发、上线到持续迭代的闭环管理。其核心目标是将 Agent 的“黑盒”行为转化为可追踪、可量化、可改进的工程化对象，覆盖执行链路、输出质量、安全防护与 Prompt 治理等关键维度。

## 支持的模型/功能

agent governance 当前支持以下三类核心应用形态：
- **智能体应用**：Agent 1.0 与 Agent 2.0（含 Managed Agent），支持全链路 Trace、轨迹评测与 Prompt 优化；
- **工作流应用**（Flow Agent）：支持节点级监控、多模态评测及基于评测集的 Prompt 迭代；
- **RAG / Memory / MCP 组件集成应用**：在安全治理层面支持知识库内容安全、记忆读写检测与工具调用拦截。

> **注意**：应用观测明确不支持通过 Assistant API 创建的智能体应用 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)；而安全策略配置对账号下全部 Agent **全局生效，不区分业务空间** [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)，这与观测、评测等功能按业务空间隔离的设计存在治理粒度差异。

功能模块按能力域划分：
- **观测域**：Trace 可视化、分钟级监控统计（QPM、[Token](../concepts/token.md)、延时）、限流统计、告警规则与历史；
- **评测域**：支持文本、轨迹、多模态三类评测数据；提供 LLM 与 Code 双类型预置评估器（如[轨迹准确性](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)、[图片指令遵循](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)）；支持人工标签体系（分类/布尔/数字/文本）；
- **安全域**：默认防护（自动生效）覆盖输入输出内容安全、RAG 文件预扫描、Memory 内容检测；高级防护（需授权开通）提供提示词攻击、敏感数据外泄等 7 类策略。

## 关键参数

| 参数类别 | 关键参数 | 说明 |
|----------|----------|------|
| **观测配置** | `OpenTelemetry 服务角色授权`、`LogStore 初始化` | 首次使用应用观测的强制前置条件，主账号操作，子账号需额外赋权 [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md) |
| **评测集结构** | `schema_version`（轨迹）、`type`（多模态） | 轨迹数据必须符合 ATIF-v1.8 等指定 schema；多模态字段为 `Array<Object>`，`type` 字段声明元素类型（`text`/`image_url`/`audio_url`/`video_url`） [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md) |
| **评估器映射** | `变量与字段类型一致性` | 评估器变量（如 `trajectory` 或 `multimodal_input`）必须映射到同类型评测集列，类型不匹配则无法保存配置 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md) |
| **安全策略** | `risk-level`（high/medium/low） | CLI 与 API 查询告警时的关键筛选参数，用于聚焦高风险事件 [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md) |

## 使用方式

1. **观测接入**：  
   - 访问 [应用观测](https://bailian.console.aliyun.com/loop/app-observe)，完成[应用观测配置](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md#h-agenteval-obs-prereq)（授权角色、开通服务、初始化 LogStore）；  
   - 在应用列表点击 **开启观测**，输入测试问题触发 Trace 上报；  
   - 进入详情页查看 **Trace 列表**、**监控统计**、**限流统计**，或通过 **添加到评测集** 将线上数据回流至评测场景。

2. **评测执行**：  
   - 创建评测集（选择场景：智能体/工作流/轨迹/自定义），发布后方可使用；  
   - 基于预置模板创建评估器（如“轨迹准确性”或“图片美学质量”），确保评测集字段满足评估器必填参数要求；  
   - 创建评测任务，关联已发布评测集版本与目标应用，配置评估器变量映射（支持映射至评测集字段或应用实时输出）；  
   - 查看 **数据明细**（含轨迹预览）与 **指标统计**，支持人工标签补充标注。

3. **优化实施**：  
   - 通过 **多版本对比** 模式调试不同 Prompt 的回复差异；  
   - 或基于 **调试反馈**：发送问题 → 选择问题样本 → 输入具体人工反馈（如“回答遗漏边界条件”）→ 生成并采纳优化 Prompt；  
   - 或基于 **评测集**：选择优质评测任务结果，驱动 Prompt 智能优化。

4. **安全防护**：  
   - 默认防护自动启用，无需操作；  
   - 高级防护需前往 [安全策略](https://bailian.console.aliyun.com/loop/security/policy) 完成服务授权并开通；  
   - 使用 CLI 快速查询：`bl agents security overview`（防护总览）、`bl agents security alerts --risk-level high`（高风险告警）。

## 限制和注意事项

- **观测限制**：应用观测暂无开放 API；Trace 数据最长保留 30 天；关闭观测后仅停止新增数据同步，历史数据仍可查；导出格式仅支持 JSONL 或 EXCEL。
- **评测限制**：评测集最多保存 10 个版本，超出后自动覆盖旧版本；单条轨迹数据大小不可超过 1 MB；评测任务创建后配置不可修改（应用、评测集、评估器映射均锁定），仅支持追加人工标签 [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
- **安全限制**：高级防护当前处于限时免费阶段，计费规则参见[计费说明](../../raw/application-user-guide/agent-billing/billing-a923eaad372554c6.md)；风险与审计页面展示账号下**全部 Agent** 的数据，**不区分业务空间** [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)，与观测/评测的业务空间隔离设计不一致，需注意权限与数据范围边界。
- **通用注意事项**：所有评测集必须**发布后**才能用于评测任务，草稿状态不可用；轨迹评测集必须包含 `trajectory` 类型列，且评估器映射必须指向该列；多模态文件上传有格式与大小限制（图片 ≤20 MB，音频/视频 ≤100 MB）。

## 来源文档

- [Evolution](../../raw/application-user-guide/agent-governance/agenteval.md)
- [开始使用](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using.md)
- [快速开始](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-set-index.md)
- [应用评测](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation.md)
- [创建与管理](../../raw/_short/agenteval-evaluation-set-946c810bda606877.md)
- [添加轨迹评测数据](../../raw/_short/agenteval-evaluation-set-trajectory-data-7bbfb9904b121823.md)
- [评估器](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-grader.md)
- [添加多模态评测数据](../../raw/_short/agenteval-evaluation-set-multimodal-data-660c12b477900b3c.md)
- [评测任务](../../raw/application-user-guide/agent-governance/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agent-governance/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agent-governance/agenteval/agenteval-tags/agenteval-tag-management.md)
- [开始使用](../../raw/application-user-guide/agent-governance/security-guide/section-gs.md)
- [Security](../../raw/application-user-guide/agent-governance/security-guide.md)
- [概述](../../raw/application-user-guide/agent-governance/security-guide/section-gs/introduction.md)
- [使用 CLI](../../raw/application-user-guide/agent-governance/security-guide/section-gs/cli.md)
- [防护总览](../../raw/application-user-guide/agent-governance/security-guide/section-assets/overview.md)
- [资产盘点](../../raw/application-user-guide/agent-governance/security-guide/section-assets.md)
- [高级防护](../../raw/application-user-guide/agent-governance/security-guide/section-adv.md)
- [Agent 资产](../../raw/application-user-guide/agent-governance/security-guide/section-assets/assets.md)
- [安全策略](../../raw/application-user-guide/agent-governance/security-guide/section-adv/policy.md)
- [风险与审计](../../raw/application-user-guide/agent-governance/security-guide/section-adv/audit.md)
- [参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref.md)
- [API 参考](../../raw/application-user-guide/agent-governance/security-guide/section-ref/api.md)
- [概览](../../raw/application-user-guide/agent-governance/agenteval/agenteval-start-using/agenteval-introduction.md)


