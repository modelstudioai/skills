# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心评测与分析模块，提供可观测性、自动化评测、智能 Prompt 优化三大能力。它支持开发者对智能体/工作流应用进行端到端质量量化、问题归因与持续迭代，覆盖从线上 Trace 沉淀、评测集构建、多维评估器配置，到基于反馈的 Prompt 优化闭环。

## 支持的模型/功能

- **观测能力**：支持智能体应用（Agent 1.0 / Agent 2.0）和工作流应用的全链路可视化追踪，包括 Prompt 解析、模型调用、工具执行、记忆读写等环节，并捕获延时、[Token](../concepts/token.md) 消耗、错误等指标；但**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置评估器模板（通用质量、智能体、文本匹配、文本相似度、格式校验）及自定义能力，支持 LLM 评估器（语义理解）、Code 评估器（规则判断）和基于历史评测任务自动提炼的 LLM 评估器 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持多版本 Prompt 对比调试、基于调试对话与人工反馈的 Prompt 智能优化，以及基于优质评测集数据的定向优化 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

> **注意**：文档 13 明确指出“应用优化 - Prompt 优化功能”于 2026-09-18 上线，而文档 1 和文档 2 中“优化”章节描述较笼统，未体现版本对比、调试反馈等具体机制，应以文档 9 的详细操作流程为准。

## 关键参数

- **评估器配置**：
  - `评分范围`：决定打分尺度（如 0–100 或 1–5），需与系统提示词中的要求严格一致；
  - `通过阈值`：用于判定 Pass/Fail（默认建议设为范围中值）；
  - `字段映射`：必须为评估器所有引用参数（如 `query`, `response`, `reference`）完成映射，否则无法创建评测任务。
- **告警规则**：
  - `持续时间`：以分钟为单位，表示指标连续异常的最短时长；
  - `告警检查周期`：默认 60 秒，最小值为 0 秒；
  - `统计周期`（告警模板）：合法范围为 1–10080 分钟（即 1 周）。
- **评测集**：
  - 必须**发布后**才可用于评测任务，草稿状态不可用；
  - 表结构需提前规划，尤其当使用预置评估器时，须确保包含其必选字段（如「问答相关性」评估器要求 `query` 和 `response`）[评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。

## 使用方式

1. **观测接入**：需主账号完成三步授权——开通 OpenTelemetry 服务、授权服务角色、初始化 LogStore；之后在应用观测页面开启对应应用的观测 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
2. **评测执行**：
   - 创建已发布的评测集（支持 xls/xlsx 导入）；
   - 配置评估器（预置或自定义），并在评测任务中完成参数映射；
   - 发起评测任务，结果支持导出 JSONL/EXCEL，且可叠加人工标签进行多维分析。
3. **Prompt 优化**：
   - 在应用优化页面选择目标应用；
   - 可选两种路径：① 多版本对比调试（基准组 vs 对照组）；② 基于调试结果 + 人工反馈生成优化建议；
   - 采纳优化结果仅更新当前 Prompt 草稿，**不会自动发布**，需手动验证后点击“发布”。

## 限制和注意事项

- **API 限制**：应用观测目前**无开放 API**，所有操作均需通过控制台完成 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **权限要求**：开通可观测链路需主账号操作；子账号需被授予相应 RAM 权限。
- **数据时效性**：观测数据同步频率为分钟级，Trace 最长保留 30 天；监控与限流指标聚合粒度支持按分钟/小时/天。
- **依赖约束**：
  - 评估器删除前，必须确保无评测任务正在使用它；
  - 基于评测任务创建的评估器**不支持试运行**，需在真实评测中验证效果；
  - “不关联应用”的评测任务仅支持纯人工标注，不触发任何模型调用。
- **成本提示**：LLM 评估器调用及评测任务中模型推理产生的 [Token](../concepts/token.md) 按实际消耗计费。

## 来源文档

- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)


