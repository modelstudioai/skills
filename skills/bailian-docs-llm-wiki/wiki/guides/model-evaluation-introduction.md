# model evaluation introduction

模型评测是百炼平台提供的核心模型能力评估功能，支持通过标准化流程对文本生成类模型进行量化打分与横向对比。它提供自定义评测（基于用户数据与业务标准）和基线评测（基于公开标准数据集）两种范式，覆盖从快速选型到调优验证、持续监控的全周期需求。该功能面向开发者设计，强调可复用性、可解释性与成本可控性。

## 支持的模型/功能

- **支持模型类型**：当前仅支持**文本生成类模型**（Text Generation），包括预置模型（如千问系列）及用户调优后的模型；不支持多模态、语音、向量等非文本生成模型 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **核心评测方式**：
  - **自定义评测**：支持用户上传评测数据集（EvaluationSet 类型，含 `Prompt` 和 `Completion` 字段）或复用已有推理结果集；支持五种评测维度类型（见下文），可灵活组合。
  - **基线评测**：内置 5 大类、13 个公开 Benchmark（如 MMLU-Pro、GSM8K、HumanEval、LongBench-v2、FinanceQA），自动执行、无需准备数据或配置维度；**仅在北京地域（华北2）可用** [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **关键辅助功能**：排行榜（同维度下多模型横向对比）、人工标注（适用于主观判断场景）、Case 分析（Bad Case 定位与依据回溯）。

> **注意**：文档 1 中称“基线评测仅北京地域可用”，而文档 2 未提及地域限制，但其引用的控制台路径（`cn-beijing`）与文档 1 一致，且文档 1 明确说明“其他地域不显示此选项，属正常现象”。因此以文档 1 的地域限制为准，该信息无矛盾。

## 关键参数

评测效果高度依赖参数配置，核心参数按维度类型划分：

| 维度类型 | 必填参数 | 说明 | 费用影响 |
|----------|----------|------|-----------|
| **大模型评估-数值型** | 裁判模型、评分器模板、评分范围（整数区间，如 `0-5`）、通过阈值（如 `3.0`） | 评分器 Prompt 需含 `${prompt}`/`${output}`/`${completion}` 至少一个变量 | 产生被评测模型推理费 + 裁判模型评分费 |
| **大模型评估-分类型** | 裁判模型、评分器模板、Pass/Fail 标签（互斥且不可重复） | 同上，Prompt 需明确定义分类逻辑 | 同上 |
| **规则评估-字符串匹配** | 比较操作符（相等/不相等/包含）、评测输入（参考文本）、模型输出（待匹配文本） | 至少一侧需含变量（如 `${completion}`） | 仅被评测模型推理费（若使用评测数据集） |
| **规则评估-文本相似度** | 评估指标（ROUGE-1/BLEU/Cosine 等）、通过阈值（0–1 区间）、评测输入与模型输出 | 同上 | 同上 |
| **人工评估-分类型** | Pass/Fail 标签 | 无裁判模型，纯人工标注 | 仅被评测模型推理费（若使用评测数据集） |

所有维度均需配置**维度名称**（≤20 字符）和**描述**（≤100 字符）。维度类型创建后**不可修改**，选错需删除重建 [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

## 使用方式

标准流程为四步闭环：**准备数据 → 创建维度 → 创建任务 → 查看结果**。

1. **准备数据**  
   在数据管理模块上传 `EvaluationSet` 类型数据集（含 `Prompt` 和 `Completion` 列），或准备已含 `Output` 的推理结果集文件。

2. **创建评测维度**  
   进入「评测维度」页签 → 「创建评测维度」→ 选择类型 → 填写对应参数（如裁判模型、标签、算法等）。推荐优先使用预置模板（如“综合评测”“标准匹配”）快速启动，再根据小样本验证结果迭代优化 Prompt [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)。

3. **创建评测任务**  
   - **自定义评测**：选择「评测数据集」（触发模型推理）或「推理结果集」（跳过推理）→ 关联已创建维度 → 设置 System Prompt（通常留空）→ 提交。  
   - **基线评测**：仅北京地域可见 → 选择 Benchmark（支持多选及子维度勾选）→ 可选开启「数据采样百分比」加速 → 提交。  
   > **注意**：文档 1 与文档 2 均明确要求维度必须**提前创建**，且基线评测**不支持关联自定义维度**或使用推理结果集 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

4. **查看结果**  
   - **自定义评测**：在任务详情页查看「指标统计」（综合得分、通过率、分数分布）和「数据明细」（逐条 Prompt/Output/Completion/评分）。  
   - **基线评测**：查看「任务总览」（雷达图）、「基线评分明细」（按 Benchmark 下钻）、「Case 分析」（含 LLM 判官依据）、「多任务对比」（最多 5 个任务）。

## 限制和注意事项

- **地域限制**：基线评测功能**仅在北京地域（华北2）可用**，其他地域控制台不显示该选项，属正常设计 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **模型限制**：仅支持文本生成类模型；多模态、语音、Embedding 等模型暂不支持评测。
- **维度限制**：维度类型创建后不可更改；被排行榜绑定的维度删除后，该排行榜将无法创建新任务（绑定维度为空）。
- **数据要求**：  
  - 评测数据集必须为 `EvaluationSet` 类型且已发布版本；  
  - 推理结果集需严格按模板格式上传（含 `Prompt`, `Output`, 可选 `Completion`）；  
  - 小规模验证建议 50–100 条，正式评测建议 200–500 条。
- **费用提示**：  
  - 使用「评测数据集」会产生被评测模型推理费用；  
  - 仅大模型评估维度（数值型/分类型）产生裁判模型评分费用；  
  - 规则评估与人工评估无裁判模型费用；  
  - 成本优化建议：先小规模验证配置，再保存推理结果集复用 [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。
- **结果解读**：综合得分是各维度平均分，可能掩盖维度间差异；建议结合分数分布图与 Bad Case 分析定位短板；1–3% 的分差通常属评测噪声，不宜作为决策依据。

## 来源文档

- [模型评测](../../raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)
- [评测维度](../../raw/model-user-guide/model-evaluation-introduction/evaluation-metrics.md)


