# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 持续优化（Optimization）三位一体的闭环能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路接入，支持智能体（Agent 1.0/2.0）和工作流应用，但**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。

## 支持的模型/功能

- **可观测性**：全链路 Trace 可视化（Prompt 解析、模型调用、工具执行、记忆读写），支持延时、Token、QPM、限流等分钟级监控指标；支持 Span 数据导出（JSONL/EXCEL）及一键添加至评测集 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **自动化评测**：支持多评估器并行打分，涵盖预置模板（通用质量、智能体、文本匹配、相似度、格式校验）与自定义类型（LLM 评估器、Code 评估器、基于评测任务生成的 LLM 评估器）；每个评测任务最多支持 10 个评估器 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **Prompt 优化**：提供双路径优化能力——**版本对比调试**（支持基准组+最多两组对照组）与**调试反馈驱动优化**（结合多轮调试对话+人工反馈生成新 Prompt），采纳后需手动发布才生效 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。
- **标签体系**：支持分类、布尔值、数字、文本四类标签，用于人工标注评测数据与线上 Span，支撑多维分析与筛选 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，而其他文档未提及 API 支持；因此当前 `agenteval` 的观测能力仅限控制台交互，不可编程调用。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | 评分范围、通过阈值 | 决定打分尺度与 Pass/Fail 判定逻辑；建议精细评估用 0–100，快速分类用 0–1 或 1–5；阈值通常设为范围中点 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md) |
| **评测集字段** | `query` / `response` / `reference_response` 等映射字段 | 所有评估器变量必须完成字段映射才能创建评测任务；预置评估器对字段有明确要求（如「问答相关性」必含 `query` 和 `response`） [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md) |
| **告警规则** | 持续时间、检查周期、统计周期、阈值比较符 | 告警触发依赖复合条件（如“错误率 ≥ 1% 持续 5 分钟”）；预置模板覆盖 QPM、错误次数/率、TTFT 等核心指标 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md) |

## 使用方式

1. **前置准备**：使用阿里云主账号开通可观测链路 OpenTelemetry 服务并初始化 LogStore；确保应用已发布且属于当前业务空间 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
2. **观测启用**：在控制台开启应用观测 → 自动生成 Trace → 支持按 Request ID/Trace ID 搜索、导出数据、添加 Span 至评测集。
3. **评测构建**：
   - 创建评测集（选择智能体/工作流类型 → 编辑表结构 → 导入数据 → **必须发布**）；
   - 创建评估器（选预置模板或自定义 LLM/Code → 配置评分范围与阈值 → **试运行验证**）；
   - 创建评测任务（关联已发布评测集 + 应用 + 评估器 → 完成参数映射 → 发起）。
4. **优化执行**：
   - 多版本对比：设置基准组与对照组 Prompt → 输入问题调试 → 对比输出 → 采纳最优配置；
   - 调试反馈：输入代表性问题 → 选择调试结果 → 描述具体问题与期望行为 → 生成并采纳优化 Prompt → **必须重新调试验证原场景、正常场景、边界场景后发布**。

## 限制和注意事项

- **权限与开通**：应用观测首次使用需主账号操作开通 OpenTelemetry 服务，子账号需被授予对应权限；高峰期开通可能延迟 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测集状态**：草稿状态的评测集不可用于评测任务，必须点击“发布”后方可选用 [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)。
- **评估器依赖**：被评测任务引用的评估器无法删除；基于评测任务创建的评估器**不支持试运行**，需实际运行评测任务验证效果 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **模型与成本**：LLM 评估器调用产生 Token 费用，Code 评估器无额外费用；建议 LLM 评估器选用 32B 以上模型并优化 Prompt 提升准确性 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **功能边界**：应用观测不支持 Assistant API 创建的智能体；评测任务创建后配置不可修改（仅可新增人工标签）；优化采纳仅更新编辑区 Prompt，**不会自动发布** [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)


