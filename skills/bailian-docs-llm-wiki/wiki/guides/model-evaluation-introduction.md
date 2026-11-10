# model evaluation introduction

模型评测是百炼平台提供的核心能力评估功能，用于量化文本生成类模型在业务场景中的实际表现。它支持自定义评测（基于用户数据集和自定义评分标准）与基线评测（基于公开标准数据集的通用能力评估）两种范式，通过结构化维度对模型输出进行打分、聚合与对比，最终生成可解释的评测报告与排行榜。该功能贯穿模型选型、调优验证、质量监控与难例挖掘等关键研发环节。

## 支持的模型/功能

- **支持的模型类型**：当前仅支持文本生成类模型（包括预置模型与调优后的 SFT/DPO 模型），不支持视觉、语音或多模态模型。
- **评测方式**：
  - **自定义评测**：使用用户上传的评测集（`prompt&completion` 单轮或 `ChatML-messages` 多轮格式），关联自定义或预置评测维度，支持 AI 自动评测、规则评估与人工标注三种评分方式 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
  - **基线评测**：内置 5 大类 13 个公开 Benchmark（如 MMLU-Pro、GSM8K、HumanEval），无需准备数据或配置维度，仅北京地域可用 [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)。
- **核心功能**：Pass@K 稳定性分析、结果分桶（定位难例）、数据回流至训练集、多模型排行榜横向对比。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否必填 | 取值示例 |
|----------|--------|------|-----------|-----------|
| **评测维度** | 类型 | 决定评分机制，创建后不可更改 | 是 | `大模型评估-数值型`、`规则评估-字符串匹配`、`人工评估-分类型` |
| | 裁判模型 | 仅大模型评估类型需指定 | 是（大模型评估） | `qwen-max`（推荐，当前限时免费） |
| | 评分范围 | 数值型维度的整数区间 | 是（数值型） | `0~5`（默认），最大值 ≤ 10 |
| | 通过阈值 | 判定 Pass/Fail 的分界线（支持小数） | 是（数值型/相似度型） | `3.0`（数值型）、`0.75`（相似度型） |
| **评测任务** | 数据来源 | 影响费用与执行逻辑 | 是 | `评测数据集`（产生推理费）、`推理结果集`（仅评分费） |
| | 单样本推理次数 | 控制 Pass@K 计算粒度 | 否（默认 1） | `3`（生成 3 次 Output 并统计通过率） |
| | 并发数 | 影响评测耗时，不影响结果 | 否（默认 8） | `1~20` |

> **注意**：文档 2 与文档 5 均指出“基线评测仅北京地域可用”，但文档 2 在“自定义评测与基线评测”表格中将“可用范围”列为“全地域”（对应基线评测行），而文档 5 明确强调“基线评测仅北京地域可用。其他地域不显示此选项，属正常现象”。此处以文档 5 的明确声明为准，文档 2 表格存在表述矛盾。

## 使用方式

1. **准备数据**：在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)中创建并发布**评测集**（类型必须为“评测集”，格式为 `prompt&completion` 或 `ChatML-messages`）[训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
2. **创建评测维度**：在“模型评测 > 评测维度”页创建模板。优先选用预置模板（共 47 个：19 个大模型评估 + 28 个规则评估），或自定义 Prompt/算法参数。人工评估维度需设计互斥穷尽的 Pass/Fail 标签 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction.md)。
3. **创建评测任务**：
   - *自定义评测*：选择模型、数据来源（评测集或推理结果集）、关联一个或多个维度，设置推理次数与并发数，提交 [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md)。
   - *基线评测*：选择模型与 Benchmark（如 `GSM8K`），可选采样百分比，提交。
4. **查看与分析结果**：任务完成后，在“Case 分析”页切换“逐次采样”或“按题聚合”视图；使用“分桶”功能按得分区间筛选难例；导出结果或回流至数据集 [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)。

## 限制和注意事项

- **地域限制**：基线评测功能仅在北京地域可用，其他地域控制台不显示该选项。
- **类型不可变**：评测维度的“类型”字段创建后不可修改，选错需删除重建；若该维度已被排行榜绑定，则需先从排行榜移除才能删除 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。
- **费用敏感点**：
  - 大模型评估维度会产生裁判模型 [Token](../concepts/token.md) 费用；规则评估与人工评估无此费用。
  - 使用“评测数据集”会触发被评测模型推理，产生额外 [Token](../concepts/token.md) 费用；“推理结果集”方式可规避此成本。
  - 建议先用 50–100 条数据小规模验证配置，再扩大评测规模。
- **数据格式强约束**：评测集必须为“评测集”类型且已发布；`prompt&completion` 格式需包含 `Prompt` 和 `Completion` 两列；`ChatML-messages` 格式需为合法 JSONL，`messages` 字段为数组 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **人工评估流程**：使用人工评估维度的任务，必须完成全部样本的人工标注，任务状态才变为“评测完成” [人工标注评测](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)。

## 来源文档

- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)
- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction.md)
- [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md)
- [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)
- [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)
- [人工标注评测](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)
- [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)
- [排行榜](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-leaderboard.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction.md)
- [大模型评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-llm.md)
- [规则评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-rule.md)
- [人工评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-manual.md)


