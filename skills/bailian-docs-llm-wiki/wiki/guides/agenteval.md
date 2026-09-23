# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 智能优化（Optimization）三位一体的能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路接入，支持从线上 Trace 沉淀到评测集、多维自动评分、人工反馈驱动的 Prompt 迭代闭环，助力开发者量化质量、定位瓶颈、持续提效。

## 支持的模型/功能

- **观测能力**：支持智能体应用（Agent 1.0 / 2.0）和工作流应用的全链路追踪，覆盖 Prompt 解析、模型调用（含 TTFT、总延时）、工具执行（MCP）、向量检索、记忆读写等环节；支持分钟级监控指标（QPM、[Token](../concepts/token.md) 消耗、错误率）与限流统计 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置评估器（通用质量、智能体、文本匹配、相似度、格式校验）与自定义评估器（LLM 评估器、Code 评估器、基于评测任务生成的 LLM 评估器），支持多评估器组合使用（单任务最多 10 个）[评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持多版本 Prompt 对比调试、基于单条/多条调试结果 + 人工反馈的 Prompt 智能生成与采纳，覆盖角色设定、规则强化、格式约束、安全合规等优化维度 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

> **注意**：应用观测目前暂不支持通过 Assistant API 创建的智能体应用 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)，且当前无开放 API 接口。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | 评分范围、通过阈值 | 决定打分尺度（如 0–100 或 1–5）与 Pass/Fail 判定基准；需与 Prompt 中的评分指令严格一致 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md) |
| **评测集结构** | 字段映射 | 评估器变量（如 `query`, `response`, `reference`）必须精确映射到评测集字段或模型输出；预置评估器对必选字段有明确要求（如「问答相关性」需 `query`+`response`） |
| **标签类型** | 分类 / 布尔 / 数字 / 文本 | 影响标注方式与筛选逻辑；分类标签最多 20 个选项，数字标签支持 Double 类型，文本标签用于自由备注 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md) |
| **告警规则** | 持续时间、检查周期、阈值、统计周期 | 告警触发需满足“持续时间 × 检查周期”内指标持续越界；预置模板覆盖 QPM、错误率、TTFT 等核心指标 |

## 使用方式

1. **观测接入**：在应用观测页面完成 OpenTelemetry 角色授权、服务开通与 LogStore 初始化（主账号操作）→ 开启目标应用观测 → 自动同步 Trace 数据（分钟级延迟）→ 支持按 Trace ID/Request ID 搜索、导出 JSONL/Excel、添加 Span 至评测集。
2. **评测构建**：
   - 创建评测集（选择智能体/工作流类型 → 编辑表结构 → 上传 XLS/XLSX 文件 → 发布）；
   - 创建评估器（基于预置模板或自定义 LLM/Code）；
   - 创建评测任务（关联已发布评测集 + 应用 + 评估器 + 字段映射）。
3. **优化迭代**：
   - 在应用优化页发起调试对话，复现问题场景；
   - 选择调试结果并输入具体人工反馈（建议按「问题现象 + 缺失内容 + 期望行为」描述）；
   - 生成优化 Prompt 后，**必须重新调试验证**原问题、正常流程与边界输入，确认无回归后再发布。

> **注意**：评测任务创建后不可修改配置（应用、评测集、评估器映射），仅支持新增人工标签；若需变更，须新建任务 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

## 限制和注意事项

- **权限与开通**：应用观测首次使用需主账号完成 OpenTelemetry 服务开通与存储初始化，子账号需被授予对应权限；告警通知依赖云监控联系人组配置。
- **数据时效性**：Trace 数据同步延迟为分钟级；监控/限流统计聚合粒度支持分钟/小时/天，历史数据最长保留 30 天。
- **评估器依赖**：基于评测任务创建的评估器**不支持试运行**，需在实际评测任务中验证效果；LLM 评估器调用产生 [Token](../concepts/token.md) 费用，Code 评估器无额外成本。
- **评测集状态**：草稿状态的评测集不可用于评测任务，必须点击「发布」后方可选用。
- **优化生效逻辑**：Prompt 采纳操作仅更新编辑区内容，**不会自动发布应用**；必须手动点击「发布」才使新版本生效 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)


