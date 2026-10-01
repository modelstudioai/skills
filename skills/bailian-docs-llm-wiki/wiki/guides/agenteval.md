# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心评估与优化模块，提供可观测性、自动化评测和 Prompt 智能优化三位一体的能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路数据采集，并支持从线上 Trace 快速构建评测集、多维度评估器配置及基于反馈的 Prompt 迭代闭环，专为开发者设计用于量化质量、定位瓶颈、驱动持续优化。

## 支持的模型/功能

- **可观测性**：支持智能体应用（Agent 1.0 / 2.0）和工作流应用的全链路追踪，覆盖 Prompt 解析、大模型调用（含 TTFT、耗时、Token）、工具执行（MCP）、向量检索、记忆读写等环节；但**暂不支持通过 Assistant API 创建的智能体应用** [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置评估器（通用质量、智能体、文本匹配、文本相似度、格式校验）和自定义能力（LLM 评估器、Code 评估器、基于评测任务生成的 LLM 评估器）；支持 LLM 评估器调用百炼平台内限时免费的大模型（建议选用 32B+ 参数量模型以提升准确性）[评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持多版本 Prompt 对比调试、基于单条或多条调试对话 + 人工反馈的智能 Prompt 生成，以及从优质评测集或线上 Trace 数据反哺优化 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。
- **标签体系**：支持分类、布尔值、数字、文本四类标签，可用于评测任务的人工标注，也可直接应用于应用观测中的 Span 数据标注，实现跨模块统一质量维度管理 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，而其他模块（如评测任务、评估器）未提及 API 支持状态；当前所有功能均需通过控制台操作，无公开 SDK 或 RESTful API 接口。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | 评分范围、通过阈值 | 决定打分尺度（如 `0-100` 用于精细评估，`0-1` 用于快速分类）和 Pass/Fail 判定基准；必须与系统提示词逻辑一致 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。 |
| **评测任务** | 字段映射 | 所有评估器变量（如 `query`, `response`, `reference`）必须显式映射到评测集字段或模型输出，映射错误将导致评估失败；每个任务最多支持 10 个评估器 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。 |
| **告警规则** | 持续时间、检查周期、统计周期 | 告警触发需满足“指标在持续时间内持续越界”，检查周期默认 60 秒，统计周期单位为分钟（1–10080）；预置模板覆盖 QPM、错误率、TTFT 等核心指标 [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)。 |
| **评测集** | 类型（智能体/工作流/自定义）、发布状态 | 评测集必须**发布后**才能用于评测任务；草稿状态不可用；类型选择影响字段自动解析逻辑 [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)。 |

## 使用方式

1. **接入与观测**：  
   - 主账号完成可观测链路 OpenTelemetry 服务授权、开通与 LogStore 初始化；  
   - 在应用列表中开启观测，Trace 数据按分钟级同步；  
   - 可直接将 Span 数据批量导入评测集，构建真实业务场景评测样本 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。

2. **构建评测闭环**：  
   - 创建评测集（上传 Excel/XLSX，≤20 MB），发布后生效；  
   - 创建评估器（选预置模板或自定义 LLM/Code），注意字段要求与评测集对齐；  
   - 创建评测任务，绑定评测集、应用、评估器（配置字段映射）及可选标签；  
   - 查看数据明细（支持普通/快速标注模式）与指标统计（综合得分、进度、得分分布）。

3. **Prompt 优化**：  
   - 在应用优化页发起任务，支持两种路径：  
     - *版本对比*：设置基准组与最多两组对照组，输入问题并对比输出差异，一键采纳最优 Prompt；  
     - *调试反馈*：选择调试对话（单条或多条），输入具体人工反馈（如“遗漏家电类目例外”），系统生成优化 Prompt 并支持对比采纳；  
   - **采纳仅更新草稿 Prompt，不自动发布**，需手动验证后点击“发布”才生效 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

## 限制和注意事项

- **权限与开通**：应用观测依赖主账号开通 OpenTelemetry 服务，子账号需被授予对应权限；高峰期开通可能延迟 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
- **数据时效与范围**：Trace 数据最长保留 30 天，监控/限流统计聚合粒度支持分钟/小时/天，但告警历史未明确时限；导出数据格式仅支持 JSONL 和 Excel。  
- **评估器约束**：基于评测任务创建的 LLM 评估器**不支持试运行**，需在实际评测任务中验证效果；Code 评估器必须返回数值且符合评分范围，函数签名须严格匹配入参 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。  
- **评测任务不可变性**：任务创建后，其关联的评测集、应用、评估器配置均不可修改；如需调整，必须新建任务 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。  
- **成本提示**：LLM 评估器调用及评测任务执行产生的 Token 消耗按百炼计费规则正常计费，需关注用量 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)


