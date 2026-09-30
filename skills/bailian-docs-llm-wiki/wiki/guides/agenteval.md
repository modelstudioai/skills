# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 智能优化（Optimization）三位一体的闭环能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路接入，支持智能体（Agent 1.0/2.0）和工作流应用，帮助开发者量化输出质量、定位性能瓶颈并持续提升业务效果。

## 支持的模型/功能

- **可观测性**：支持端到端 Trace 可视化，完整捕获 Prompt 解析、大模型调用（含 TTFT、Token 消耗）、工具执行（MCP）、记忆读写等环节；支持监控统计（QPM、错误率、延时）、限流分析及告警配置。> **注意**：当前应用观测暂不支持通过 Assistant API 创建的智能体应用，详见[应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置与自定义评估器，覆盖通用质量、智能体专项、文本匹配、格式校验等场景；支持 LLM 评估器（语义理解型）与 Code 评估器（规则确定型）混合使用；支持多评估器组合（如「相关性（LLM）+ 格式校验（Code）」），单任务最多 10 个评估器。
- **优化能力**：支持 Prompt 多版本对比调试、基于调试对话与人工反馈的智能优化、以及基于优质评测集数据的迭代优化；所有优化操作仅更新草稿态 Prompt，需手动发布生效。

## 关键参数

- **评估器配置**：
  - `评分范围`：决定打分尺度（如 `0-100` 或 `1-5`），影响评估粒度；
  - `通过阈值`：用于自动判定 Pass/Fail（如 `≥80` 为通过）；
  - `参数映射`：必须为评估器中所有引用变量（如 `query`, `response`, `reference`）指定来源字段，映射错误将导致评估失败。
- **告警规则**：
  - `持续时间`：触发告警需连续满足条件的分钟数；
  - `告警检查周期`：默认 60 秒，单位为秒；
  - `重复策略`：控制未恢复状态下的通知频率（如“每 30 分钟重复”）。
- **评测集**：字段结构需与所选评估器的必选参数严格对齐（例如「问答相关性」评估器强制要求 `query` 和 `response` 字段），否则无法完成映射。

## 使用方式

1. **接入观测**：在[应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)页面完成 OpenTelemetry 权限授权与存储初始化后，开启目标应用观测，即可自动同步 Trace 数据（分钟级延迟）。
2. **构建评测**：先创建并**发布**评测集（草稿不可用），再创建评测任务，关联已发布评测集与应用，并添加至少一个评估器（需完成全部参数映射）；支持“不关联应用”模式用于纯人工标注。
3. **执行优化**：在[应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)页面发起任务，可选择「版本对比」或「调试反馈」模式；生成优化结果后需**手动采纳至编辑区**，并通过重新调试验证效果，最终点击**发布**才生效。
4. **标签协同**：通过[标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)创建分类/布尔/数字/文本标签，既可用于评测任务的人工标注，也可用于应用观测 Span 的线上质量标注，实现跨模块数据对齐。

## 限制和注意事项

- **观测限制**：应用观测无公开 API，且不支持 Assistant API 创建的智能体；Trace 数据最长保留 30 天，导出支持 JSONL/EXCEL 格式。
- **评测限制**：评测任务创建后不可修改应用、评测集或评估器配置；LLM 评估器调用产生的 Token 按实际用量计费；基于评测任务创建的评估器**不支持试运行**，需在真实评测中验证效果。
- **优化限制**：一次优化建议聚焦单一问题（如仅修复格式问题），避免多目标冲突；采纳优化结果后必须重新调试验证回归风险（原问题、正常流程、边界输入），否则可能引入新缺陷。
- > **注意**：文档 13（更新日志）显示告警管理于 2026-09-17 上线，但文档 5 中明确说明其功能已完备并提供详细配置指南；而文档 3 提到“应用观测目前暂无 API”，该表述与平台当前能力一致，无需修正。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)


