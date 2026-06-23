# application evaluation

阿里云百炼提供完整的应用评测体系，支持对智能体应用和工作流应用的输出质量进行系统化评估。平台同时提供自动评测和手动评测两种模式，结合评测集、评估器和标签等核心组件，帮助开发者持续监控和优化应用效果。

## 评测模式

### 自动评测

自动评测利用大模型基于应用的知识库自动生成评测集，并对智能体的回答进行评分和归因分析，生成包含调优建议的评测报告。支持两种模式：

- **单应用评测**：深度评估单个智能体应用，生成评分、错误分析和优化建议的详细报告。
- **多应用横向评测**：在同一基准下对比多个应用（最多 8 个），用于选型决策或版本迭代验证。

自动评测的完整操作流程包括四个阶段：创建评测任务、设置评测集、配置评测规则和执行评测。详见[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

**前提条件**：

1. 仅面向已发布且配置了知识库的智能体应用。
2. 需开通"应用观测"功能，并将评测应用添加到观测列表。
3. 子账号需获取`管理员`或`应用评测-操作`权限。

### 手动评测

手动评测通过人工构建评测集，针对特定业务场景对应用回答进行人工分析与评分。操作流程为：准备评测集（下载模板填写 Prompt/Completion/SessionId）、上传并发布评测集、创建评测任务、人工打标、查看评测报告。详见[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。

## 评测集

评测集是评测任务的数据基础，支持自动生成和手动上传两种创建方式。

### 旧版评测集类型

| 类型 | 文件格式 | 适用场景 |
|------|----------|----------|
| 对话分析 | `.xls` / `.xlsx` | 手动评测，包含 Prompt、Completion、SessionId 字段，支持多轮对话 |
| 知识问答 | `.jsonl` | 自动评测，包含 query、queryType、referenceAnswer、fineKeywords、coarseKeywords 字段 |

### 新版评测集类型

新版评测集支持三种类型，详见[新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)：

| 类型 | 说明 |
|------|------|
| 智能体 | 根据智能体应用的出入参形式定义评测集 |
| 工作流 | 根据工作流应用的出入参形式定义评测集 |
| 自定义 | 任意定义表结构，适用于特殊评测场景 |

创建方式包括手动上传（xls/xlsx，单文件 20MB 以内）和从应用观测导入真实数据。评测集创建后需要发布才能用于评测任务，支持版本管理。

> **注意**：创建评测集时，类型一旦确定不可修改。

## 评测任务

新版评测任务支持智能体和工作流应用的评测，可结合评估器（自动评分）和标签（人工标注）进行多维度评价。创建评测任务时需配置：

- **任务名称和描述**
- **评测集**：从已发布的评测集中选择
- **应用关联**：可选不关联应用（纯人工标注）、关联工作流或关联智能体
- **评估器**：最多添加 10 个评估器，需完成参数映射
- **标签**：用于人工标注的自定义维度

评测任务创建后配置不可修改。任务详情页提供数据明细（含评估器评分和人工标注）和指标统计（含综合得分和通过率）两个视图。详见[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

## 评估器

评估器是自动评估应用输出质量的核心组件，分为三种创建方式：

### 预置评估器模板

百炼提供多个预置模板，覆盖通用质量、智能体能力、文本匹配、文本相似度和格式校验等场景。使用前需确认评测集字段满足评估器的必选参数要求。

### LLM 评估器

使用大模型对应用输出进行语义评分，适用于相关性、有害性、幻觉检测等需要语义理解的场景。需配置评估 Prompt、评分范围和通过阈值。

### Code 评估器

使用 Python 3.10 脚本实现评估逻辑，适用于格式校验、数值计算、精确匹配等需要确定性结果的场景。无额外 Token 费用。

此外还支持**基于评测任务创建评估器**，将历史标注经验固化为自动化评估规则。详见[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

## 标签管理

标签用于对评测数据和应用观测数据进行自定义标注，支持四种类型：

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| 分类 | 从预定义选项中选择（最多 20 个选项） | 回答质量、错误类型分类 |
| 布尔值 | True/False 二选一 | 是否正确、是否存在幻觉 |
| 数字 | Double 类型数值输入 | 评分（1-5）、相关性得分 |
| 文本 | 自由文本输入 | 错误原因说明、改进建议 |

标签可在评测任务中用于人工标注，也可在应用观测中对线上数据进行标注。支持普通模式（逐条标注）和快速标注（批量编辑）两种模式。详见[标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 评测报告与归因分析

自动评测完成后，系统生成评测报告，包含以下内容：

- **评分机制**：大模型对每个回答打 1-5 分，4 分及以上视为正确。
- **总正确率**：得分不低于 4 分的回答占比。
- **BadCase 分析**：按分数从低到高展示错误条目，包含打分和问题分类。
- **归因分析**：对 BadCase 自动定位问题环节，包括模型理解有误、重排不佳、检索无效、切片不完整、未获取知识五种归因类型。
- **调优建议**：针对 Prompt、检索配置或知识库切片的具体优化建议。

## 最佳实践

### 建立持续评测机制

以下场景建议触发评测：知识库更新后、调整 Prompt 后、更换或升级模型后、调整检索/重排策略后、定期回归（每周或每月）。

### 优化闭环

1. 识别 BadCase（得分低于 4 分的回答）
2. 分析归因，定位问题环节
3. 实施针对性优化
4. 发布新版本，使用同一评测集再次评测
5. 对比新旧版本报告，验证优化效果

## 计费说明

- 自动评测和评测任务调用大模型均会产生 Token 费用，按实际消耗计费。
- 生成评测集和执行评测均仅支持 `qwen-max` 和 `qwen-plus` 模型。
- 控制台会显示预估平均消耗（参考值）和预估最大消耗（理论上限），最终以实际账单为准。
- Code 评估器不产生额外 Token 费用。

## 常见问题

- **评测集生成进度长时间保持 0%**：评测集生成为离线任务，需在后台排队执行，排队期间进度为 0%。
- **评测期间勿关闭应用观测**：否则可能导致评测任务失败或报告不准确。
- **评测报告用例数量与设置不符**：失败的评测用例不计入最终正确率。
- **评测任务失败仍消耗 Token**：每个成功完成的步骤都会计费，后续步骤失败不影响已消耗部分。
- **评测任务创建后不可修改**：如需不同配置，请创建新的评测任务。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)




