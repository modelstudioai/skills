# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 智能优化（Optimization）三位一体的闭环能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路接入，支持智能体（Agent 1.0/2.0）和工作流应用，旨在帮助开发者量化输出质量、定位性能瓶颈、构建可信评测集并持续提升线上效果。

## 支持的模型/功能

- **观测能力**：支持端到端 Trace 可视化，完整捕获 Prompt 解析、大模型调用（含 TTFT、总延时、[Token](../concepts/token.md) 消耗）、工具执行（MCP）、向量检索、记忆读写等环节；支持分钟级监控统计（QPM、错误率、各模型/工具调用趋势）与限流分析 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：覆盖多维自动评估，包括准确性、相关性、合规性、简洁性、幻觉检测等；支持预置评估器（通用质量、智能体、文本匹配、相似度、格式校验）与自定义评估器（LLM 评估器、Code 评估器、基于历史评测任务生成的 LLM 评估器）[评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：提供 Prompt 多版本对比调试、基于调试对话+人工反馈的智能优化、以及基于优质评测集/线上 Trace 的迭代优化；支持一键采纳最优配置，但需手动发布生效 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。
- **标签体系**：支持分类、布尔值、数字、文本四类标签，用于人工标注评测数据与观测 Span，支撑多维度质量归因与筛选分析 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，而其他模块（如评测任务、评估器）均未提及开放 API 接口能力。当前所有功能均通过控制台 Web 界面操作，无 SDK 或 RESTful API 文档支撑。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评测集** | 字段映射、发布状态 | 评测集必须**发布**后才能用于评测任务；字段需与所选评估器的必选参数（如 `query`, `response`, `reference`）严格对齐，否则评估失败 [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)。 |
| **评估器** | 评分范围、通过阈值、参数映射 | LLM/Code 评估器均需配置 `评分范围`（如 0–100）和 `通过阈值`（默认建议设为中位数）；所有评估器变量必须完成字段映射，否则无法创建评测任务 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。 |
| **评测任务** | 应用关联方式、评估器数量上限 | “不关联应用”仅用于纯人工标注；每个评测任务最多支持 **10 个评估器**，建议组合使用 LLM（语义）与 Code（规则）评估器以覆盖多维度 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。 |
| **告警规则** | 持续时间、检查周期、重复策略 | 告警触发需满足“指标连续 N 分钟超标”，`持续时间` 单位为分钟；`告警检查周期` 默认 60 秒，最小值为 0（即实时检查）；重复策略决定告警恢复前是否重发 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)。 |

## 使用方式

1. **前置准备**：使用阿里云主账号登录 Evolution 控制台，完成可观测链路 OpenTelemetry 服务授权、开通与 LogStore 初始化（子账号需主账号授予权限）。
2. **开启观测**：在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)页面为已发布应用开启观测，Trace 数据分钟级同步，支持按 Request ID/Trace ID 搜索及 30 天内导出（JSONL/Excel）。
3. **构建评测资产**：
   - 创建并**发布**评测集（支持智能体/工作流类型，字段需匹配评估器）；
   - 创建评估器（选用预置模板或自定义 LLM/Code），确保参数映射正确；
   - （可选）创建标签，用于人工标注补充自动评估盲区。
4. **执行评测**：创建评测任务，关联已发布评测集与应用，添加 ≤10 个评估器并完成参数映射，启动后查看自动评分与人工标签结果。
5. **优化 Prompt**：通过“多版本对比”或“调试&反馈”模式发起优化，系统生成建议后需**手动采纳至编辑区 → 调试验证 → 发布应用**三步完成生效。

## 限制和注意事项

- **模型与框架限制**：应用观测**不支持通过 Assistant API 创建的智能体应用**；所有功能均要求应用已发布且属于当前业务空间 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **数据时效性**：观测数据、监控统计、限流指标更新频率为**分钟级**，不支持实时毫秒级追踪；告警检查周期最小为 0 秒（即实时），但实际触发受持续时间约束。
- **评测集与评估器强耦合**：预置评估器对评测集字段有明确要求（如「问答相关性」必需 `query` 和 `response`），字段缺失或名称不匹配将导致评估失败；自定义 Code 评估器需严格遵循 Python 3.10 函数签名与返回类型规范。
- **权限与配额**：告警规则最多关联 50 个应用；评测集字段映射上限 50 个；标签选项最多 20 个；所有操作需主账号初始化权限，子账号需显式授权。
- **成本提示**：LLM 评估器调用产生 [Token](../concepts/token.md) 费用，Code 评估器无额外费用；评测任务消耗的 [Token](../concepts/token.md) 量可在任务列表页查看。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)


