# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心能力模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 持续优化（Optimization）三位一体的能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准实现链路接入，支持智能体（Agent 1.0/2.0）和工作流应用，覆盖从调试、质量量化到线上运维的完整闭环。

## 支持的模型/功能

- **观测能力**：支持端到端 Trace 可视化，完整记录 Prompt 解析、大模型调用（含 TTFT、总耗时、Token 消耗）、工具执行（MCP）、向量检索、记忆读写等环节；支持导出 JSONL/EXCEL 格式数据用于离线分析 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：提供预置评估器模板（通用质量、智能体、文本匹配、文本相似度、格式校验）及自定义能力，支持 LLM 评估器（语义理解型）与 Code 评估器（规则确定型）双模式 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持多版本 Prompt 对比调试、基于调试对话+人工反馈的智能 Prompt 生成，以及基于优质评测集/线上 Trace 的定向优化 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。
- **标签体系**：支持分类、布尔值、数字、文本四类标签，用于人工标注评测结果与线上 Span 数据，支撑多维指标统计与筛选。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，而文档 1 中“全流程可观测”描述未限定接口形态，实际开发者需通过控制台操作或导出数据实现集成，不可依赖实时 API 接入。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | `评分范围`、`通过阈值` | 决定打分尺度与 Pass/Fail 判定逻辑；建议精细评估用 0–100，快速分类用 0–1 或 1–5；阈值通常设为范围中值 [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。 |
| **评测集** | `评测集类型`（智能体/工作流/自定义）、`字段映射` | 创建时需匹配所选应用的输入输出结构；LLM 评估器对字段名有强依赖（如 `query`/`response`），映射错误将导致评估失败。 |
| **告警规则** | `持续时间`、`告警检查周期`、`统计周期` | 告警触发需满足“指标在持续时间内连续违反阈值”，检查周期默认 60 秒，统计周期单位为分钟（1–10080）[告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)。 |
| **Prompt 优化** | `调试问题代表性`、`人工反馈明确性` | 优化效果高度依赖输入质量：单条调试应聚焦单一问题；人工反馈需按“问题现象 + 具体缺失 + 期望行为”结构化描述，避免模糊表述。 |

## 使用方式

1. **观测接入**：主账号完成 OpenTelemetry 服务授权、开通与 LogStore 初始化后，在控制台开启目标应用的观测；数据同步延迟为分钟级，支持按 Trace ID/Request ID 搜索与 30 天内数据导出。
2. **评测构建**：
   - 创建已发布的评测集（草稿不可用）；
   - 配置评估器并严格完成字段映射（如 `query` → 评测集 `question` 字段）；
   - 创建评测任务时，最多添加 10 个评估器，建议组合 LLM + Code 类型以覆盖语义与规则维度。
3. **优化执行**：
   - 在“多版本对比”中设置基准组与对照组 Prompt，发起调试验证差异；
   - 在“调试&反馈优化”中选择代表性调试结果，输入结构化人工反馈，生成 Prompt 后必须**手动采纳至编辑区**，再经调试验证后**手动发布**才生效。
4. **标签应用**：在评测任务或应用观测中直接添加已有标签，支持快速标注与基于标签的筛选/统计，无需额外配置。

## 限制和注意事项

- **观测限制**：不支持通过 Assistant API 创建的智能体应用；Trace 数据仅在开启观测后新增请求被采集，关闭期间数据不回溯。
- **评估器限制**：基于评测任务创建的评估器**不支持试运行**，需在真实评测任务中验证效果；Code 评估器要求 Python 3.10 运行时，函数必须返回数值且覆盖全部入参。
- **权限与配置**：应用观测初始化必须由主账号操作；子账号需主账号授予 `AliyunBailianFullAccess` 或最小化 OpenTelemetry 相关权限。
- **数据一致性风险**：文档 8 强调“评测集完备后需发布才能使用”，但文档 13 提到“评测任务发起后将无法修改配置”，二者叠加意味着：若评测集发布后更新字段，已创建的评测任务仍引用旧版本，需新建任务绑定新版本评测集。
- **计费提示**：LLM 评估器调用、评测任务中模型推理均产生 Token 费用，需在控制台监控消耗量 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

## 来源文档

- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)


