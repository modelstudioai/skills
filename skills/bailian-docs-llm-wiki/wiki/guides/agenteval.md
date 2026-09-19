# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 智能优化（Optimization）三位一体的闭环能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路数据采集，并支持从线上 Trace 沉淀评测样本、多维评估器自动打分、以及基于调试反馈的 Prompt 迭代优化，助力开发者量化质量、定位瓶颈、持续提升 Agent 生产效果。

## 支持的模型/功能

- **可观测性**：完整追踪智能体应用（Agent 1.0 / Agent 2.0）和工作流应用的端到端执行链路，包括 Prompt 解析、大模型调用（含 TTFT、耗时、[Token](../concepts/token.md) 消耗）、MCP 工具执行、向量检索、记忆读写等节点；支持 Trace 列表搜索、原始数据查看、标注记录与 JSONL/EXCEL 导出 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **自动化评测**：支持预置与自定义评估器组合使用。预置评估器覆盖通用质量、智能体专项（如工具调用合规性）、文本匹配、相似度、格式校验等场景；自定义评估器支持 LLM（基于大模型语义评分）与 Code（Python 3.10 脚本规则判断）两种实现方式，可配置评分范围、通过阈值及参数映射 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **Prompt 优化**：提供双路径优化能力：① 多版本对比调试（基准组 vs 对照组），支持人工调整 Prompt 后并行验证输出差异；② 基于调试对话 + 人工反馈（问题现象+期望行为）的智能 Prompt 生成，支持单条或多条调试结果输入，生成结果需人工采纳后写入编辑区 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。
- **标签体系**：支持分类、布尔值、数字、文本四类标签，用于人工标注评测数据与观测 Span，支撑多维度质量分析与筛选；标签可直接应用于评测任务和应用观测模块 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)。

> **注意**：应用观测目前暂不支持通过 Assistant API 创建的智能体应用，且无开放 API 接口 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)；而评测任务创建后，其核心配置（应用、评测集、评估器映射）不可修改，仅支持追加人工标签 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | 评分范围 | 决定打分尺度（如 `0-100` 或 `1-5`），影响评估器提示词与结果粒度；LLM 和 Code 评估器均需显式配置 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。 |
| | 通过阈值 | 定义 Pass/Fail 判定标准（如 `≥80` 为 Pass），需与评分范围逻辑一致。 |
| | 参数映射 | 必须为评估器所有引用变量（如 `query`, `response`, `reference`）完成字段映射，否则无法保存评测任务；映射源可为评测集字段或应用输出 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。 |
| **评测集** | 类型与版本 | 创建时需指定智能体/工作流类型及具体版本，系统据此解析输入输出字段；草稿状态不可用于评测，必须发布 [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)。 |
| **优化任务** | 调试结果选择 | 单条适用于明确单一问题；多条需聚焦同一优化目标，避免冲突反馈降低优化有效性 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。 |
| | 人工反馈 | 应按「问题现象 + 具体缺失/错误 + 期望行为」结构化描述，例如：“遗漏家电类目退款例外；请完整列出一般规则、适用条件和特殊品类例外” [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。 |

## 使用方式

1. **接入与准备**  
   - 主账号完成可观测链路 OpenTelemetry 服务授权、开通与 LogStore 初始化（子账号需主账号赋权）[应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
   - 发布待评测/优化的智能体或工作流应用。

2. **构建评测资产**  
   - 创建并发布评测集（支持 xls/xlsx 模板导入，字段需匹配目标评估器要求）[评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)。  
   - 创建评估器（选用预置模板或自定义 LLM/Code），并在评测任务中完成参数映射 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。  
   - 创建标签（如“回答完整性”分类标签、“是否存在幻觉”布尔标签），用于人工标注 [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)。

3. **执行核心流程**  
   - **观测**：开启应用观测 → 查看 Trace 列表与监控统计（QPM、[Token](../concepts/token.md)、模型耗时等）→ 将典型 Span 批量添加至评测集 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
   - **评测**：创建评测任务 → 绑定评测集与应用 → 添加评估器并映射参数 → 运行后在详情页查看自动评分与人工标签结果 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。  
   - **优化**：进入应用优化 → 选择调试问题 → 发起版本对比或基于调试结果+人工反馈生成新 Prompt → 采纳后手动验证并发布 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

## 限制和注意事项

- **功能限制**：应用观测暂无 API 接口；Assistant API 创建的智能体应用不被支持；评测任务创建后配置不可修改，需新建任务变更 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
- **数据时效性**：观测数据同步频率为分钟级，Trace 最长保留 30 天；监控与限流指标聚合粒度支持分钟/小时/天 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。  
- **成本与配额**：LLM 评估器调用产生 [Token](../concepts/token.md) 费用，计入用户账单；Code 评估器无额外费用；每个评测任务最多支持 10 个评估器，每个评测集最多支持 50 个字段映射 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。  
- **安全与合规**：优化过程生成的 Prompt 需人工复核知识口径、权限边界、安全与合规要求，智能优化无法理解隐含业务规则 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。  
- **版本兼容性**：基于评测任务创建的评估器不支持试运行，需在实际评测中验证效果；且仅支持已完成评估的评测任务作为训练源 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)


