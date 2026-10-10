# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 智能优化（Optimization）三位一体的能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路数据采集，并支持从线上 Trace 沉淀评测样本、多维评估器量化输出质量、以及基于调试反馈闭环优化 Prompt，适用于智能体（Agent 1.0/2.0）和工作流应用的持续迭代。

## 支持的模型/功能

- **观测能力**：支持端到端追踪智能体/工作流应用的全链路执行过程（Prompt 解析、大模型调用、MCP 工具执行、向量检索、记忆读写等），自动捕获延时、[Token](../concepts/token.md) 消耗、错误信息及上下文 Span 数据；支持将 Span 直接导入评测集 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置评估器（通用质量、智能体专项、文本匹配、相似度、格式校验）与自定义评估器（LLM 评估器、Code 评估器、基于评测任务生成的 LLM 评估器）；支持多评估器组合（单任务最多 10 个），覆盖语义理解与精确规则双场景 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持两种 Prompt 优化路径：① 多版本对比调试（基准组 vs 对照组）；② 基于调试对话 + 人工反馈的智能生成优化；采纳后仅更新草稿 Prompt，需手动发布生效 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，而其他模块（如评测任务、评估器）均未提及 API 支持状态。当前所有功能均通过控制台 Web 界面操作，无公开 SDK 或 RESTful 接口文档支撑程序化调用。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | `评分范围`、`通过阈值` | 决定打分尺度与 Pass/Fail 判定逻辑；建议精细评估用 0–100，快速分类用 0–1 或 1–5；阈值通常设为范围中位数 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md) |
| **评测集字段** | `query`、`response`、`reference_response`、`context` 等 | 不同评估器对必填字段有强依赖（如「问答相关性」要求 `query`+`response`），需在创建评测集前按评估器模板规划表结构 |
| **告警规则** | `持续时间`、`告警检查周期`、`指标`、`告警阈值` | 告警触发需满足“指标连续 N 分钟超阈值”，检查周期最小为 60 秒；预置模板覆盖 QPM、错误率、TTFT 等核心指标 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md) |
| **标签类型** | 分类 / 布尔值 / 数字 / 文本 | 影响标注方式与筛选条件（如分类标签支持「属于」筛选，数字标签支持「大于」筛选），需按评测维度语义选择 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md) |

## 使用方式

1. **前置准备**：使用主账号完成可观测链路 OpenTelemetry 服务授权、开通与 LogStore 初始化（分钟级生效）；确保应用已发布且归属当前业务空间 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
2. **观测启用**：在 [应用观测](https://bailian.console.aliyun.com/loop/app-observe) 页面开启目标应用观测，Trace 数据自动同步（分钟级延迟），支持按 Request ID/Trace ID 搜索、30 天内数据导出（JSONL/Excel）。
3. **评测构建**：
   - 创建评测集（需发布后才可用），选择类型（智能体/工作流/自定义）并映射输入输出字段；
   - 创建评估器（预置或自定义），完成试运行验证；
   - 创建评测任务，绑定评测集、应用、评估器（含字段映射），支持“不关联应用”用于纯人工标注场景 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。
4. **优化执行**：
   - 进入应用优化页，选择待优化应用；
   - 可选「对比模式」调试多版本 Prompt，或「调试窗口」输入问题 → 选择调试结果 → 输入人工反馈 → 生成并采纳优化 Prompt；
   - **必须重新调试验证原问题、正常流程、边界场景后，再点击发布**。

## 限制和注意事项

- **观测限制**：不支持通过 Assistant API 创建的智能体应用；Trace 数据仅保留 30 天；监控统计聚合粒度最小为分钟级；限流统计仅展示 QPM 相关指标。
- **评测限制**：评测集文件最大 20 MB（xls/xlsx）；每个评测任务最多添加 10 个评估器；基于评测任务创建的评估器**不支持试运行**，需实际运行评测任务验证效果 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **权限与部署**：应用观测配置需主账号操作；子账号需被授予 `AliyunBaiLianFullAccess` 或等效可观测权限；所有功能均部署在百炼控制台，无独立服务实例。
- **成本提示**：LLM 评估器调用产生 [Token](../concepts/token.md) 费用，计入百炼账单；Code 评估器无额外费用；评测任务产生的 [Token](../concepts/token.md) 消耗可在任务列表查看。
- **版本与兼容性**：仅支持 Agent 1.0 和 Agent 2.0 架构的应用；工作流应用同样受支持；不兼容非百炼托管的外部 Agent 服务。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)


