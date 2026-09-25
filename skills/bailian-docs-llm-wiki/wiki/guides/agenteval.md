# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 智能优化（Optimization）三位一体的能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路接入，支持智能体（Agent 1.0/2.0）和工作流应用的端到端质量量化与持续改进。

## 支持的模型/功能

- **观测能力**：支持全链路 Trace 可视化，覆盖 Prompt 解析、大模型调用（含 TTFT、耗时、[Token](../concepts/token.md) 消耗）、工具执行（MCP）、向量检索、[记忆](../concepts/memory.md)读写等环节；支持分钟级监控统计（QPM、错误率、[Token](../concepts/token.md) 分析）与限流统计 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置评估器（通用质量、智能体、文本匹配、相似度、格式校验）与自定义评估器（LLM 评估器、Code 评估器、基于评测任务生成的 LLM 评估器），支持多维度自动评分与人工标签协同分析 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持基于调试结果的 Prompt 多版本对比、人工反馈驱动的智能优化，以及基于优质评测集/线上 Trace 的闭环迭代 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。
- **标注体系**：通过标签管理支持分类、布尔值、数字、文本四类标签，用于评测数据与观测 Span 的人工标注与多维筛选 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，而其他模块（如评测任务、评估器）均未提及 API 支持状态；当前所有功能均需通过控制台交互使用，无公开 SDK 或 RESTful API 接口。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | 评分范围、通过阈值 | 决定打分尺度与 Pass/Fail 判定逻辑；建议精细评估用 0–100，快速分类用 0–1 或 1–5；阈值通常设为范围中值 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md) |
| **评测任务** | 字段映射 | 所有评估器变量（如 `query`, `response`, `reference`）必须完成到评测集字段或模型输出的准确映射，否则评估失败 |
| **告警规则** | 持续时间、检查周期、阈值 | 告警触发需满足指标在“持续时间”内连续违反阈值，检查周期默认 60 秒；预置模板覆盖 QPM、错误率、TTFT 等核心指标 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md) |
| **标签类型** | 类型（分类/布尔/数字/文本）、筛选条件 | 不同类型对应不同筛选语法（如分类标签用“属于”，数字标签用“大于”），影响后续数据筛选与统计准确性 |

## 使用方式

1. **前置准备**：使用阿里云主账号登录百炼控制台，完成可观测链路 OpenTelemetry 服务授权、开通与 LogStore 初始化（子账号需主账号授权）。
2. **观测启用**：在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)页面开启目标应用观测，Trace 数据分钟级同步；支持导出 JSONL/EXCEL 并一键添加至评测集。
3. **评测构建**：
   - 创建评测集（选择智能体/工作流类型 → 编辑表结构 → 导入数据 → 发布）；
   - 创建评估器（选用预置模板或自定义 LLM/Code 逻辑）；
   - 创建评测任务（绑定评测集、应用、评估器及参数映射）。
4. **优化实施**：
   - 进入应用优化页，发起多版本 Prompt 对比调试；
   - 或基于调试对话+人工反馈（明确描述问题现象与期望行为）生成优化建议；
   - 采纳后需手动发布才生效。

## 限制和注意事项

- **应用兼容性**：应用观测**不支持通过 Assistant API 创建的智能体应用**；仅支持智能体 1.0/2.0 和工作流应用 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集状态**：评测集必须**发布后才能用于评测任务**，草稿状态不可选；版本管理仅保留最近 10 个历史版本。
- **评估器依赖**：基于评测任务创建的评估器**不支持试运行**，且仅允许选择“已完成评估”的任务；若评估器被任一评测任务引用，则无法删除。
- **告警与限流**：限流统计仅展示 QPM 相关指标（如 QPM 限流次数），告警规则配置需关联具体应用，且通知对象依赖云监控联系人配置。
- **成本提示**：LLM 评估器调用产生 [Token](../concepts/token.md) 费用，Code 评估器无额外费用；评测任务消耗的 Token 量可在任务列表查看。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)


