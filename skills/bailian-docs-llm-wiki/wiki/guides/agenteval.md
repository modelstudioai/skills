# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期评测与优化的核心模块，提供可观测性、自动化评测、智能 Prompt 优化三大能力。它支持对智能体/工作流应用的执行链路进行端到端追踪，基于评测集与多类型评估器量化输出质量，并通过版本对比与调试反馈驱动 Prompt 持续迭代。所有功能均通过控制台界面操作，暂未开放 API 接口 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。

## 支持的模型/功能

- **可观测性**：支持智能体（Agent 1.0 / 2.0）和工作流应用的全链路 Trace 追踪，覆盖 Prompt 解析、大模型调用、MCP 工具执行、向量检索、记忆读写等环节；支持延时（TTFT、总耗时）、Token 消耗、QPM、错误率等监控与限流指标 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：
  - **预置评估器**：按「通用质量」「智能体」「文本匹配」「文本相似度」「格式校验」分类，开箱即用；
  - **自定义评估器**：支持 LLM 评估器（需指定模型，限时免费）和 Code 评估器（Python 3.10 脚本），可配置评分范围（如 0–100）、通过阈值及参数映射；
  - **基于评测任务创建评估器**：从已完成标注的历史评测任务中自动抽象 LLM 评估规则 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持多版本 Prompt 对比调试、基于调试对话与人工反馈的智能优化，以及一键采纳最优配置；优化结果需手动发布才生效 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

> **注意**：文档 13 明确指出“应用观测目前暂无 API”，但文档 1 中“观测”章节未提及该限制，易引发误解；以文档 13 为准。

## 关键参数

| 参数类别 | 关键字段 | 说明 |
|----------|----------|------|
| **评估器通用** | `评分范围` | 决定打分尺度（如 0–1、1–5、0–100），需与 Prompt 中的评分指令严格一致；精细评估推荐 0–100，快速分类推荐 0–1 或 1–5 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。 |
| | `通过阈值` | 评分 ≥ 阈值为 Pass；建议设为评分范围中位数（如 0–100 时设为 50）。 |
| **LLM 评估器** | `模型选择` | 支持多种大模型，评估模型限时免费；建议选用 32B 以上参数量模型提升准确性。 |
| | `Prompt` | 必须明确评分标准、步骤、输出格式；可导入预置模板或基于历史评测任务生成。 |
| **Code 评估器** | `入参设置` | 必须包含 `query` 和 `response`（默认），可添加自定义变量；函数签名须与入参完全一致。 |
| | `执行函数` | 必须返回数值类型结果（在评分范围内），建议含异常处理逻辑。 |
| **评测任务** | `评测集字段映射` | 所有评估器参数（如 `query`, `reference`, `response`）必须显式映射到评测集字段或模型输出；映射错误将导致评估失败 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。 |

## 使用方式

1. **准备阶段**  
   - 创建并**发布**评测集（草稿不可用）[评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)；  
   - 创建评估器（预置/LLM/Code/基于评测任务），完成试运行验证（LLM/Code 类型支持，基于评测任务类型不支持）；  
   - 开启目标应用的观测（需主账号完成 OpenTelemetry 权限与服务开通）。

2. **评测执行**  
   - 创建评测任务：选择已发布评测集、关联应用（或选“不关联应用”用于纯人工标注）、添加 ≤10 个评估器并完成**全部参数映射**；  
   - 启动任务后，可在详情页查看自动评分结果、人工标签、数据明细及指标统计（综合得分、通过率、Token 消耗等）。

3. **优化迭代**  
   - 在应用优化页面发起调试，输入问题观察多版本 Prompt 输出差异；  
   - 或基于调试结果+人工反馈（描述“问题现象+缺失内容+期望行为”）生成优化 Prompt；  
   - **采纳**后仍需手动调试验证原场景、正常场景、边界场景，确认无退化再点击**发布**。

## 限制和注意事项

- **评测集**：仅支持 `.xls`/`.xlsx` 格式，单文件 ≤20 MB；草稿状态不可用于评测任务 [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)。  
- **评估器**：被评测任务引用的评估器无法删除；基于评测任务创建的评估器不支持试运行，需实际运行评测任务验证效果。  
- **观测能力**：不支持通过 Assistant API 创建的智能体应用；Trace 数据同步延迟为分钟级，关闭观测后历史数据不再更新。  
- **计费**：评测任务中 LLM 评估器调用产生的 Token 按标准计费；Code 评估器无额外费用。  
- **权限**：OpenTelemetry 服务开通需主账号操作，子账号需被授予对应权限。  
- **版本控制**：评测集最多保留最近 10 个版本；评估器编辑支持版本回溯，但采纳优化仅更新当前 Prompt 草稿，不自动发布。

## 来源文档

- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)


