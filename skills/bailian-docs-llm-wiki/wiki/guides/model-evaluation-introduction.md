# model evaluation introduction

模型评测是百炼平台提供的核心模型能力评估功能，支持通过自定义评测和基线评测两种方式，对文本生成与多模态模型进行量化打分与横向对比。它覆盖从数据准备、维度定义、任务执行到结果分析与回流的完整闭环，帮助开发者科学选型、验证调优效果并持续监控模型质量。评测结果可生成结构化报告、排行榜及难例分桶，支撑数据驱动的模型迭代决策。

## 支持的模型与功能

- **支持的模型类型**：文本生成类模型（含 Function Calling、结构化输出能力）、视觉理解模型（如 Qwen4-Max）、文生图/图生图/图生视频（首帧/首尾帧）模型。图片生成与视频生成模型暂不支持基线评测，需使用[创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md)。
- **评测方式**：
  - **自定义评测**：基于用户自有评测集与自定义维度，支持大模型评估（AI 自动评分）、规则评估（算法计算）和人工评估（人工标注）三种评分范式；
  - **基线评测**：内置覆盖通用知识、数学、代码、上下文推理、领域专项 5 大类共 13 个文本基线，以及 CMMMU、MMMU-Pro 等 4 个多模态视觉理解基线，开箱即用，仅北京地域可用 [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)。
- **多模态支持**：视觉理解、文生图、图生图、图生视频（首帧/首尾帧）等任务类型均支持，但当前仅限人工评估维度；大模型评估与规则评估维度在多模态任务中不可选，属预期限制 [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md)。

## 关键参数

| 参数类别 | 参数名 | 说明 | 是否必填 | 注意事项 |
|----------|--------|------|-----------|-----------|
| **通用配置** | 维度名称 / 任务名称 | 标识符，长度 ≤50 字符 | 是 | 命名建议采用“评估方面+评估方式”，如“回答准确性-LLM评分” |
| **评分器类型** | 类型（5 种） | 大模型评估-数值型/分类型、规则评估-字符串匹配/文本相似度、人工评估-分类型 | 是 | 创建后不可更改，选错需删除重建 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md) |
| **大模型评估** | 裁判模型 | 如千问-Max，用于自动评分 | 数值型/分类型必填 | 当前限时免费调用；评分范围建议 0–5，避免过大区间降低一致性 |
| | 评分器 Prompt | 含 `${messages}` / `${completion}` / `${output}` 变量，指导裁判模型评判 | 是 | 至少含一个变量；切换预置模板会覆盖当前内容，需提前备份 |
| | 通过阈值 | 数值型：最低 Pass 分数；相似度型：最低相似度（0–1） | 数值型/相似度型必填 | 默认 3（0–5 区间），业务敏感场景需按容忍度调整 |
| **规则评估** | 比较操作符 / 评估指标 | 如“相等”“包含”“BLEU”“ROUGE-L”等 | 是 | 翻译推荐 BLEU，摘要推荐 ROUGE-L，语义相关性推荐余弦相似度 |
| **任务执行** | 单样本推理次数 | ≥1，用于计算 Pass@K 稳定性指标 | 否（默认 1） | 设置 >1 时推理与评分费用同比增加；Pass@K 为 - 表示存在失败采样 [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md) |
| | 并发数 | 1–20，影响执行速度，不影响结果 | 否（默认 8） | — |

> **注意**：文档 1 与文档 4 对“多模态任务支持的评估类型”描述一致（仅人工评估），但文档 1 中“大模型评估与规则评估即将上线”的表述与文档 4 中“属预期行为”“相关能力即将上线”的措辞存在时效性差异。当前生产环境以文档 4 的明确限制为准：**多模态任务仅支持人工评估维度，且无时间表承诺上线其他类型**。

## 使用方式

1. **准备数据**：在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)上传评测集（EvaluationSet 类型），格式依任务类型而定：
   - 文本生成：`prompt&completion`（单轮）或 `ChatML-messages`（多轮）；
   - 多模态：Zip 压缩包（含 `data.jsonl` + 图片/视频文件），字段结构详见[调优数据上传规则-评测集格式](../../raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/text-generation-tuning-data-upload-rules.md#sec-eval-set)。

2. **创建维度**：在**评测维度**页签，选择预置模板（47 个）或自定义创建。例如快速启动可选“回答准确性-LLM评分”（数值型）或“安全风险分类”（分类型）。

3. **创建任务**：
   - 自定义评测：选择模型 → 任务类型（自动灰显不支持项）→ 数据来源（评测集或推理结果集）→ 关联维度 → 配置推理参数（System Prompt、temperature 等）→ 提交；
   - 基线评测：选择模型 → 任务类型 → 勾选 Benchmark（如 GSM8K、CMMMU）→ 提交。

4. **查看与分析**：任务完成后，在详情页使用：
   - **任务总览**：综合得分、Bad Case 数、消耗明细；
   - **Case 分析**：逐样本查看输入/输出/评分；支持“逐次采样”与“按题聚合（Pass@K）”视图；
   - **分桶与导出**：按得分/Pass@K 区间分类难例，支持下载或回流为新数据集。

## 限制和注意事项

- **地域限制**：基线评测仅在北京地域可用；DPO/CPT 训练、OSS 导入等部分数据功能也受限于北京地域 [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)。
- **多模态限制**：
  - 任务类型为视觉理解、文生图等时，**仅支持人工评估维度**，大模型评估与规则评估维度不可选；
  - 数据来源**仅支持评测数据集**，不支持推理结果集；
  - 所有评测维度必须为“人工评估-分类型”，预置模板亦禁用。
- **费用相关**：
  - 费用 = 被评测模型推理费 + 裁判模型评分费（仅大模型评估产生）；
  - 规则评估与人工评估**无裁判模型费用**，成本最低；
  - 单样本推理次数 >1 时，费用线性增加；建议先用 50–100 条小规模验证配置 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **操作约束**：
  - 评测维度类型创建后不可更改；
  - 已被排行榜绑定的维度无法删除；
  - 任务提交后不可更换被评测模型，需删除重建；
  - 人工评估任务须全部标注完成才变为“评测完成”状态。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)
- [评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction.md)
- [创建自定义评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-custom-evaluation-task.md)
- [创建基线评测任务](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/create-baseline-evaluation-task.md)
- [查看评测结果](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/view-evaluation-results.md)
- [人工标注评测](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-manual-annotation.md)
- [排行榜](../../raw/model-user-guide/model-evaluation-introduction/evaluation-task-introduction/evaluation-leaderboard.md)
- [训练集与评测集](../../raw/model-user-guide/model-evaluation-introduction/training-set-and-evaluation-set.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction.md)
- [大模型评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-llm.md)
- [人工评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-manual.md)
- [规则评估](../../raw/model-user-guide/model-evaluation-introduction/evaluation-dimension-introduction/evaluation-dimension-rule.md)


