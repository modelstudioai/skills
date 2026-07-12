# application evaluation

阿里云百炼提供完整的应用评测体系，支持对智能体应用和工作流应用的输出质量进行系统化评估。平台同时提供自动评测与手动评测两种模式，并通过评测集、评估器和标签三大组件构建多维度的评测闭环。当前平台存在新旧两套评测系统，新版在评测任务管理、评估器和标签体系上做了较大升级。

## 评测模式

百炼支持两种评测模式，分别适用于不同场景：

### 自动评测

[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)利用大模型基于应用关联的知识库自动生成评测集，并对智能体的回答进行自动评分，生成评测报告与调优建议。支持两种子模式：

- **单应用评测**：深度评估单个智能体应用的表现，生成包含评分、错误分析和优化建议的详细报告。
- **多应用横向评测**：在同一评测基准下对比最多 8 个应用（或同一应用的不同版本），用于选型决策或版本迭代效果验证。

前提条件：

1. 仅面向**已发布**的智能体应用，且应用须已配置知识库。
2. 须开通**应用观测**功能，并将待评测应用添加到观测列表。
3. 子账号需获取`管理员`或`应用评测-操作`权限。
4. 多应用横向评测时，所有被选应用必须关联至少一个相同的知识库。

自动评测流程分四步：创建评测任务 → 设置评测集 → 配置评测规则 → 执行评测。评测集生成和评估模型当前仅支持 `qwen-max` 和 `qwen-plus`。

### 手动评测

[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)通过人工构建评测集，对应用回答进行人工分析与评分。流程为：准备评测集（下载模板填充数据）→ 上传评测集 → 创建评测任务 → 人工标注打分 → 查看评测报告。

手动评测适用于需要领域专家主观判断的场景，评测维度支持使用内置模板或自定义评测维度模板。

> **注意**：手动评测属于旧版评测系统的功能。新版评测系统通过「评测任务 + 标签」的组合同样支持人工标注场景，且功能更灵活。

## 评测集

评测集是评测任务的数据基础，用于存储和管理评测数据。

### 旧版评测集

[旧版评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)支持两种类型：

| 类型 | 文件格式 | 适用场景 |
|------|----------|----------|
| 对话分析 | `.xls` / `.xlsx` | 人工评测，包含 Prompt、Completion、SessionId 字段，支持多轮对话 |
| 知识问答 | `.jsonl` | 自动评测，包含 query、queryType、referenceAnswer、fineKeywords、coarseKeywords 字段 |

创建方式：自动生成（基于知识库，仅知识问答类型）或手动上传。单次上传最多 10 个文件，单个文件不超过 20MB。

### 新版评测集

[新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)支持三种类型：

| 类型 | 说明 |
|------|------|
| 智能体 | 根据选中智能体应用的出入参形式定义评测集 |
| 工作流 | 根据选中工作流应用的出入参形式定义评测集 |
| 自定义 | 任意定义评测集表结构，适用于特殊评测场景 |

新版评测集支持手动上传和从应用观测导入两种创建方式，并具备版本管理能力，每次发布生成新版本。创建后类型不可修改。

## 评估器

[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)是新版评测体系的核心组件，用于自动评估应用输出质量。支持三种创建方式：

### 基于预置模板

百炼提供多种预置评估器模板，覆盖以下分类：

- **通用质量**：评估回答的基本质量指标
- **智能体**：专门用于评测智能体应用
- **文本匹配**：精确规则文本匹配
- **文本相似度**：计算文本相似度得分
- **格式校验**：验证输出格式规范性

### 自定义评估器

| 类型 | 评估方式 | 适用场景 | 成本 |
|------|----------|----------|------|
| LLM 评估器 | 大模型语义理解 | 相关性、有害性、幻觉检测 | 产生 [Token](../concepts/token.md) 费用 |
| Code 评估器 | Python 代码规则判断 | 格式校验、数值计算、精确匹配 | 无额外费用 |

### 基于评测任务创建

通过历史评测任务的标注结果自动抽象为新的 LLM 评估器，适用于将人工标注经验固化为自动化评估规则的场景。需选择已完成评估的评测任务，并配置 query、response、label_score 的字段映射。

每个评测任务最多支持添加 10 个评估器。建议组合 3-5 个评估器从不同维度评估应用质量，例如：相关性评估器（LLM）+ 格式校验评估器（Code）。

## 标签管理

[标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)用于对评测数据和应用观测数据进行自定义标注，支持四种标签类型：

| 标签类型 | 数据类型 | 适用场景 |
|----------|----------|----------|
| 分类 | 预定义选项（最多 20 个） | 回答质量分级、错误类型分类 |
| 布尔值 | True / False | 是否正确、是否存在幻觉 |
| 数字 | Double 数值 | 评分（1-5）、相关性得分（0-1） |
| 文本 | 自由文本 | 错误原因说明、改进建议 |

标签可同时用于评测任务的人工标注和应用观测的数据标注，支持基于标签的数据筛选和指标统计。

## 评测任务（新版）

[新版评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)支持智能体和工作流应用的评测，核心配置包括：

- **选择评测集**：从已发布的评测集列表中选择评测集和版本
- **关联应用**：支持不关联应用（纯人工标注）、关联工作流或关联智能体三种方式
- **添加评估器**：配置自动评分规则及参数映射
- **添加标签**：配置人工标注维度

任务详情页提供数据明细和指标统计两个视图，支持普通模式和快速标注两种标注方式。

## 评测报告与归因分析

自动评测完成后生成评测报告，包含以下维度：

- **总正确率**：得分 >= 4 分的回答占比（评分范围 1-5 分）
- **BadCase 分析**：按分数从低到高展示错误评测条目
- **调优建议**：基于归因分析提供 Prompt、检索配置或知识库切片的具体优化建议
- **RAG 智能体评价**：按问题类型展示单项得分

归因分析将 BadCase 定位到 RAG 流程的具体环节：

| 归因类型 | 含义 | 优化方向 |
|----------|------|----------|
| 模型理解有误 | 已获取正确知识但推理错误 | 优化提示词或切换更强模型 |
| 重排不佳 | 正确切片排序靠后 | 调整重排配置或增加切片数量 |
| 检索无效 | 召回切片过多或过少 | 调整检索策略 |
| 切片不完整 | 语义单元被分割到多个切片 | 增大切片长度或启用语义切分 |
| 未获取知识 | 知识库缺少相关内容 | 补充知识库内容 |

## 最佳实践

### 建立持续评测机制

以下场景建议触发评测：知识库更新后、调整 Prompt 后、更换或升级模型后、调整检索/重排策略后、定期回归（每周或每月）。

### 优化闭环

识别 BadCase → 分析归因定位问题 → 实施针对性优化 → 发布新版本再次评测 → 对比结果确认改进。若效果未达预期则继续迭代。

## 计费说明

评测任务调用大模型产生的 [Token](../concepts/token.md) 费用正常计费。自动评测的评测集生成和评估均会消耗 [Token](../concepts/token.md)，预估平均消耗仅为参考值，最终以实际账单为准。评估器模型当前限时免费。

## 常见问题

- **评测集生成进度长时间保持 0%**：评测集生成和应用评测为离线任务，需后台排队执行，排队期间进度保持 0%，任务开始后自动更新。
- **评测期间能否关闭应用观测**：不可以，否则可能导致评测任务失败或数据丢失。
- **评测报告中用例数量与设置不符**：自动评测可能部分失败，报告仅展示成功完成的用例。
- **评测任务创建后可否修改**：任务配置（应用、评测集）不可修改，但可随时添加人工标签。如需不同配置请创建新任务。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)






