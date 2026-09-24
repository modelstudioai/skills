# agenteval

`agenteval` 是百炼平台 Evolution 体系中面向 AI Agent 全生命周期管理的核心模块，提供可观测性（Observability）、自动化评测（Evaluation）与 Prompt 智能优化（Optimization）三位一体的能力。它不依赖特定开发框架，基于 OpenTelemetry GenAI 标准接入，支持对智能体（Agent 1.0/2.0）和工作流应用进行端到端质量量化、问题归因与持续迭代。

## 支持的模型/功能

- **观测能力**：完整追踪 Prompt 解析、大模型调用（含 TTFT、总延时、[Token](../concepts/token.md) 消耗）、工具执行（MCP）、向量检索、[记忆](../concepts/memory.md)读写等全链路 Span；支持 Trace 数据导出（JSONL/EXCEL）及一键添加至评测集 [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)。
- **评测能力**：支持多维自动化评估，包括准确性、相关性、合规性、格式规范性、工具调用正确性等。提供两类核心组件：
  - **预置评估器**：覆盖通用质量、智能体专项、文本匹配、相似度、格式校验等场景；
  - **自定义评估器**：支持 LLM 评估器（需指定模型并编写评估 Prompt）和 Code 评估器（Python 3.10 脚本，要求返回数值评分）[评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)。
- **优化能力**：支持基于调试对话、人工反馈、优质评测集或线上 Trace 的 Prompt 多版本对比与智能生成；优化结果需人工审查后采纳，不自动发布 [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)。

> **注意**：文档 4 明确指出“应用观测目前暂无 API”，而文档 2 和文档 1 均未提及 API 支持，因此当前观测能力仅限控制台使用，不可编程调用。

## 关键参数

| 参数类别 | 关键项 | 说明 |
|----------|--------|------|
| **评估器配置** | 评分范围 | 决定打分尺度（如 `0-100` 或 `1-5`），影响评估粒度与阈值设定；必须与系统提示词中的范围声明一致。 |
| | 通过阈值 | 用于判定 Pass/Fail（评分 ≥ 阈值为 Pass）；建议设为评分范围中位数。 |
| | 字段映射 | 所有评估器变量（如 `query`, `response`, `reference`）必须映射到评测集字段或模型输出，否则任务创建失败。 |
| **评测任务** | 应用关联方式 | 可选“不关联应用”（纯人工标注）、“智能体”或“工作流”；选择后不可修改。 |
| | 评估器数量上限 | 单个评测任务最多添加 10 个评估器，建议组合 LLM（语义）与 Code（规则）评估器以覆盖多维度。 |
| **标签** | 类型 | 分类、布尔值、数字、文本四类；数字标签支持 `>`, `>=` 等筛选，文本标签支持 `包含`/`不包含`。 |

## 使用方式

1. **观测启用**：在[应用观测](https://bailian.console.aliyun.com/loop/app-observe)页面开启目标应用观测，授权 OpenTelemetry 服务角色并初始化 LogStore（主账号操作）；开启后数据分钟级同步。
2. **评测构建**：
   - 创建**评测集**（需发布后才可用），规划字段以匹配目标评估器的必填参数（如「问答相关性」需 `query`+`response`）；
   - 创建或选用**评估器**，完成试运行验证（LLM/Code 类型支持，但「基于评测任务创建」类型不支持试运行）；
   - 创建**评测任务**，绑定评测集、应用及评估器，并完成全部字段映射。
3. **优化实施**：
   - 在「应用优化」页面发起调试对话，或选取线上 Trace/评测失败样本；
   - 提交具体人工反馈（推荐格式：“问题现象 + 具体缺失 + 期望行为”）；
   - 查看优化结果对比，**手动采纳**至编辑区，**必须重新调试验证**后点击「发布」才生效。

## 限制和注意事项

- **观测限制**：不支持通过 Assistant API 创建的智能体应用；Trace 数据最长保留 30 天；限流指标（QPM）更新频率为分钟级。
- **评测限制**：评测集文件仅支持 `.xls`/`.xlsx`（≤20 MB）；草稿状态评测集不可用于评测任务；「基于评测任务创建」的评估器无法试运行，需在真实任务中验证效果。
- **优化限制**：采纳操作仅更新当前 Prompt 编辑区，**不会自动发布**；优化后必须覆盖原问题、正常流程、边界输入三类场景验证，避免退化。
- **权限要求**：开通应用观测需主账号授权；子账号需被授予对应 OpenTelemetry 权限。
- **计费说明**：评测任务中 LLM 评估器调用产生的 [Token](../concepts/token.md) 按标准计费；Code 评估器无额外费用 [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)。

## 来源文档

- [快速开始](../../raw/application-user-guide/agenteval/agenteval-quick-start.md)
- [概览](../../raw/application-user-guide/agenteval/agenteval-introduction.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability.md)
- [应用观测](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-observation.md)
- [告警管理](../../raw/application-user-guide/agenteval/agenteval-observability/agenteval-alert-management.md)
- [应用评测](../../raw/application-user-guide/agenteval/agenteval-evaluation.md)
- [评测集](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-set.md)
- [评估器](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-grader.md)
- [评测任务](../../raw/application-user-guide/agenteval/agenteval-evaluation/agenteval-evaluation-task.md)
- [应用优化](../../raw/application-user-guide/agenteval/agenteval-optimization.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags.md)
- [标签管理](../../raw/application-user-guide/agenteval/agenteval-tags/agenteval-tag-management.md)
- [更新日志](../../raw/application-user-guide/agenteval/agenteval-changelog.md)


