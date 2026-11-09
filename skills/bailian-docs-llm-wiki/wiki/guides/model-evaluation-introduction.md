# model evaluation introduction

模型评测是百炼平台用于量化评估大模型能力的核心功能，支持自定义评测与基线评测两种模式。它通过将模型输出与预设标准（如参考答案、语义规则或人工判断）进行比对，生成可量化的评分与分析报告，服务于模型选型、调优效果验证和持续质量监控等关键场景。整个流程依赖于评测集、评测维度和评测任务三个核心要素的协同。

## 支持的模型/功能

- **支持的模型类型**：当前仅支持文本生成类模型（包括预置模型与调优后的 SFT/DPO 模型），视觉理解、图生视频等模态暂不支持评测 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **评测方式**：
  - **自定义评测**：基于用户上传的评测集（`prompt&completion` 单轮或 `ChatML-messages` 多轮格式）和自定义评测维度，支持大模型评估、规则评估、人工评估三类评分方式。
  - **基线评测**：内置 5 大类、13 个公开标准 Benchmark（如 MMLU-Pro、GSM8K、HumanEval），无需准备数据集或配置维度，但**仅北京地域可用** [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)。
- **核心功能**：Pass@K 统计、结果分桶、难例回流、排行榜横向对比、推理结果集复用以降本。

> **注意**：文档 3 和文档 7 均明确指出基线评测“仅北京地域可用”，但文档 3 在“自定义评测与基线评测”表格中将“可用范围”列为“全地域”（对应基线评测列），该处为明显矛盾。应以文档 7 的“重要”提示及文档 3 后文“不同地域可用的评测方式可能不同（如基线评测仅北京地域可用）”为准，此处为文档 3 表格内容过时或笔误。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否必填 | 约束 |
|----------|--------|------|----------|------|
| **评测维度** | 类型 | 5 种之一：大模型评估-分类型/数值型、规则评估-字符串匹配/文本相似度、人工评估-分类型 | 是 | 创建后不可更改 |
| | 裁判模型 | 仅大模型评估类型需指定（如千问-Max） | 大模型评估必填 | — |
| | 评分范围 | 仅数值型必填，整数区间（如 `0~5`） | 数值型必填 | 最小值 ≥ 0，最大值 ≥ 1 |
| | 通过阈值 | 数值型/相似度型必填，决定 Pass/Fail 判定线 | 是 | 数值型步长 0.1；相似度型范围 `0~1`，步长 `0.01` |
| **评测任务** | 数据来源 | “评测数据集”（触发模型推理）或“推理结果集”（仅评分） | 是 | 评测数据集须为 `EvaluationSet` 类型且已发布 [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md) |
| | 单样本推理次数 | 控制每条样本的采样次数，用于计算 Pass@K | 否 | 默认 `1`；大于 `1` 时费用与推理次数成正比 |
| | 并发数 | 影响评测执行速度 | 否 | 默认 `8`，可设 `1~20` |

## 使用方式

1. **准备数据**：在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)中创建并发布**评测集**（类型必须为 `EvaluationSet`），支持单轮（`prompt&completion`）或多轮（`ChatML-messages`）格式 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
2. **定义标准**：在**模型评测 > 评测维度**中创建评测维度模板，选择类型并配置参数（如裁判模型、Prompt、算法、阈值等）。推荐优先使用预置模板（共 47 个）快速启动 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
3. **发起评测**：在**模型评测 > 评测任务**中创建任务，选择模型、关联评测集与一个或多个维度，并设置推理参数（如 `temperature`）与并发策略。
4. **分析结果**：任务完成后，在**Case 分析**页查看逐样本评分、Pass@K 聚合、分桶结果；通过**排行榜**横向对比多模型表现 [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)。

## 限制和注意事项

- **类型不可变**：评测维度的“类型”字段创建后不可修改，选错需删除重建；若该维度已被任务或排行榜引用，则需先解除关联 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项 [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)。
- **费用构成**：费用 = 被评测模型推理费 + （仅大模型评估维度）裁判模型评分费。规则评估与人工评估无裁判模型费用，是成本最低方案 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **数据集约束**：评测集不支持从 OSS 导入；训练集与评测集类型创建后不可变更；所有数据集导入均启用 OSS 服务端加密（SSE-OSS） [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **人工标注**：使用人工评估维度的任务，必须完成全部样本的人工标注后，任务状态才变为“评测完成”，方可进行后续分析 [人工标注评测](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)。

## 来源文档

- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)
- [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)
- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction.md)
- [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md)
- [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)
- [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)
- [人工标注评测](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)
- [排行榜](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-leaderboard.md)
- [大模型评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-llm.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction.md)
- [规则评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-rule.md)
- [人工评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-manual.md)


