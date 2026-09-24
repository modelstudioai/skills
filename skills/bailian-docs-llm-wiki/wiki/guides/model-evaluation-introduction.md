# model evaluation introduction

模型评测是百炼平台提供的核心模型能力评估功能，支持通过标准化或自定义方式对文本生成类模型进行量化打分与横向对比。它覆盖模型选型、调优验证、能力归因和持续监控等关键研发场景，提供从数据准备、维度定义、任务执行到结果分析的端到端闭环。当前功能仅面向文本生成类模型，不支持多模态或语音类模型。

## 支持的模型/功能

- **支持的模型类型**：预置模型（如千问系列商业及开源模型）和已部署的调优模型（Fine-tuned Text Generation Model），详见[预置模型列表](raw/model-user-guide/model-deployment-index/model-deployment-introduction.md)。  
- **评测方式**：  
  - **自定义评测**：使用用户上传的评测数据集（EvaluationSet 类型）或已有推理结果集，配合自定义评测维度（含大模型评估、规则评估、人工评估三类共五种类型）完成评分；  
  - **基线评测**：直接调用平台内置的 5 大类、13 个公开标准 Benchmark（如 MMLU-Pro、GSM8K、HumanEval、LongBench-v2、FinanceQA），无需准备数据或配置维度，但**仅在北京地域可用**（其他地域控制台不显示该选项）[模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **核心功能模块**：评测维度模板（可复用）、评测任务（支持推理调用与纯评分两种模式）、排行榜（同维度下多模型横向对比）、人工标注工作台（仅限人工评估维度）。

> **注意**：文档 1 中称“基线评测仅北京地域可用”，而文档 2 未提及地域限制，但其引用的上游文档 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md) 明确说明该限制，因此以文档 1 为准。

## 关键参数

| 参数类别 | 参数名 | 说明 | 必填性 | 约束条件 |
|----------|--------|------|--------|----------|
| **通用** | 维度名称 | 评测维度模板标识符 | 是 | ≤20 字符 |
| | 描述 | 补充说明评判目标 | 否 | ≤100 字符 |
| **大模型评估** | 裁判模型 | 执行自动评分的 LLM（如千问-Max） | 是（仅该类） | 从下拉列表选择 |
| | 评分器 Prompt | 指导裁判模型打分的提示词 | 是（仅该类） | 必须含 `${prompt}` / `${output}` / `${completion}` 至少一个变量；≤50000 字符 |
| | 评分范围（数值型） | 整数区间，如 `0–5` | 是（仅数值型） | 最小值 ≥ 0，最大值 ≥ 1 |
| | 通过阈值（数值型/相似度型） | 判定 Pass 的最低分或相似度 | 是 | 步长 0.1（数值型）或 0.01（相似度型） |
| | Pass/Fail 标签（分类型） | 分类输出标签 | 是（仅分类型） | Pass 与 Fail 标签互斥且不可重复 |
| **规则评估** | 比较操作符（字符串匹配） | 相等 / 不相等 / 包含 | 是（仅该子类） | — |
| | 评估指标（文本相似度） | ROUGE-1/2/L、BLEU、Cosine、Fuzzy Match、Accuracy | 是（仅该子类） | — |
| **任务级** | System Prompt | 为被评测模型设定角色（非评分器 Prompt） | 否 | 多数场景可留空 |

所有评测维度创建后，**类型不可修改**，选错需删除重建；已关联的评测任务不受影响，但排行榜绑定维度为空时将阻止新任务提交 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 使用方式

1. **准备数据**：在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 两列），或准备已含 `Output` 的推理结果集文件。  
2. **创建维度**：进入「评测维度」页签 → 「创建评测维度」→ 选择类型 → 配置参数（如裁判模型、Prompt、标签、阈值等）。推荐先用预置模板（如“综合评测”“标准匹配”）快速启动，再基于小样本（50–100 条）验证效果并迭代 Prompt [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。  
3. **创建任务**：  
   - **自定义评测**：选择「评测数据集」（触发模型推理，产生费用）或「推理结果集」（跳过推理，仅评分）→ 关联已建维度 → 设置 `System Prompt`（可选）→ 开启/关闭排行榜参与 → 「开始评测」；  
   - **基线评测**：选择「基线评测」→ 选模型 → 勾选 Benchmark（支持多选及子维度筛选）→ 可选开启「数据采样百分比」→ 「开始评测」。  
4. **查看结果**：任务状态为「评测完成」后，进入详情页：  
   - 自定义评测：查看「数据明细」（逐条 Prompt/Output/Completion/评分）和「指标统计」（综合得分、通过率、分数分布）；  
   - 基线评测：查看「任务总览」（雷达图）、「基线评分明细」（按 Benchmark 下钻）、「Case 分析」（含裁判依据）、「多任务对比」（最多 5 模型并行分析）。

## 限制和注意事项

- **模型限制**：仅支持文本生成类模型（Text Generation），不支持图像、语音、多模态等其他模态模型。  
- **地域限制**：基线评测功能**仅在北京地域（华北2）可用**，其他地域控制台不展示该选项，属正常现象 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **维度不可变性**：评测维度类型创建后不可修改，误选需删除重建；删除维度前须确认无排行榜绑定，否则将导致排行榜无法新建任务。  
- **费用说明**：  
  - 使用「评测数据集」时，产生被评测模型的推理费用（按 [Token](../concepts/token.md) 计费）；  
  - 使用「大模型评估」维度时，额外产生裁判模型评分费用（按 [Token](../concepts/token.md) 计费）；  
  - 「规则评估」与「人工评估」维度无裁判模型费用；「推理结果集」来源无推理费用。  
- **结果解读建议**：避免仅依赖综合得分做决策——1–3% 的分数差异通常属于评测噪声；应结合分数分布、Bad Case 分析和维度明细定位真实短板 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **人工评估特殊流程**：使用人工评估维度的任务，必须完成全部数据的人工标注后，状态才变为「评测完成」；未标注完时始终为「进行中」。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


