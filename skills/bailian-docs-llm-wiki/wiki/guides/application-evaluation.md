# application evaluation

阿里云百炼提供了完整的应用评测体系，支持自动评测和手动评测两种模式，用于系统化评估智能体应用和工作流应用的输出质量。评测体系包含评测集管理、评测任务执行、评估器配置和标签标注等核心功能，帮助开发者在应用上线前验证效果、持续迭代优化。

## 评测模式

百炼支持两种主要的评测模式，适用于不同的评测场景：

- **自动评测**：利用大模型基于知识库自动生成评测集，自动评估智能体回答并生成评测报告与调优建议。支持单应用深度评测和最多 8 个应用的横向对比评测。详见[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：通过人工构建评测集，对应用的回答进行人工分析与评分，适用于需要领域专家判断的场景。详见[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。

自动评测仅面向已发布且配置了知识库的智能体应用，且需要开通"应用观测"功能。手动评测同样仅支持已发布的智能体应用。

## 评测集

评测集是评测任务的数据基础，用于存储和管理评测数据。百炼提供两套评测集体系：

### 旧版评测集

旧版评测集支持两种类型：

| 类型 | 文件格式 | 适用场景 |
|------|----------|----------|
| 对话分析 | `.xls`、`.xlsx` | 手动评测，支持单轮/多轮对话 |
| 知识问答 | `.jsonl` | 自动评测，包含 query、参考答案、关键词等字段 |

评测集可通过大模型基于知识库自动生成（仅知识问答类型），也支持手动上传。单次上传最多 10 个文件，单个文件不超过 20MB。详见[评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。

### 新版评测集

新版评测集支持三种类型：**智能体**、**工作流**和**自定义**。智能体和工作流类型会根据应用的出入参形式自动生成数据模板，自定义类型可任意定义表结构。创建后类型不可修改。

新版评测集还支持从应用观测页面导入真实线上数据，并提供版本管理功能，每次发布会生成新版本。详见[新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。

> **注意**：旧版评测集和新版评测集是两套独立的体系。新版评测集增加了工作流类型支持和从应用观测导入数据的能力，建议优先使用新版。

## 评测任务

### 自动评测流程

完成一次自动评测需要四个阶段：

1. **创建评测任务**：选择 1-8 个已发布且配置了知识库的智能体应用，选择用于生成评测集的知识库。多应用横向评测时，所有应用必须关联至少一个相同的知识库。
2. **设置评测集**：可自动生成（基于知识库，由 `qwen-max` 或 `qwen-plus` 模型生成）或选择已有评测集。生成时需选择 2-8 种任务类型（事实型、分析型、比较型、教程型等）。
3. **配置评测规则**：设置每种任务类型的采样数量，选择评测模型。支持试运行预览评测效果。
4. **执行评测**：确认配置后发起评测。评测完成后可追加应用进行对比（总数不超过 8 个）。

### 新版评测任务

新版评测任务支持智能体和工作流两种应用类型，可结合评估器（自动评分）和标签（人工标注）进行多维度评价。创建时需配置：

- **评测集**：从已发布的评测集中选择
- **应用关联**：可选择不关联应用（纯人工标注）、关联智能体或关联工作流
- **评估器**：建议添加 3-5 个，每个任务最多 10 个，需完成参数映射
- **标签**：用于人工标注维度

评测任务创建后配置不可修改。详见[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

## 评估器

评估器是新版评测体系的核心组件，用于自动评估应用输出质量。支持以下创建方式：

### LLM 评估器

使用大模型对输出进行语义评分，适用于相关性、有害性、幻觉检测等需要语义理解的场景。需配置评估 Prompt、评分范围和通过阈值。建议使用 32B 以上参数量的模型。

### Code 评估器

使用 Python 3.10 脚本实现评估逻辑，适用于格式校验、数值计算、精确匹配等需要确定性结果的场景。无额外 Token 费用。

### 基于评测任务创建

通过历史评测任务的标注结果，自动抽象生成新的 LLM 评估器，适用于将人工标注经验固化为自动化规则。

百炼还提供通用质量、智能体、文本匹配、文本相似度、格式校验等预置评估器模板，可直接使用或基于模板自定义。详见[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

## 标签管理

标签用于人工标注评测数据，支持四种类型：

| 标签类型 | 说明 | 适用场景 |
|----------|------|----------|
| 分类 | 从预定义选项中多选 | 回答质量、错误类型分类 |
| 布尔值 | True/False 二选一 | 是否正确、是否存在幻觉 |
| 数字 | Double 类型数值输入 | 评分（1-5）、相关性得分 |
| 文本 | 自由文本输入 | 错误原因说明、改进建议 |

标签可在评测任务和应用观测中使用，支持普通标注和快速标注两种模式。详见[标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 评测报告与归因分析

自动评测完成后，系统生成包含以下内容的评测报告：

- **总正确率**：得分 >= 4 分的回答占比（评分范围 1-5 分）
- **BadCase 分析**：按分数从低到高展示错误条目，自动进行归因分析
- **调优建议**：针对 Prompt、检索配置或知识库切片的具体优化建议
- **RAG 智能体评价**：按问题类型（事实型、分析型等）展示单项得分

归因分析可定位问题环节：模型理解有误、重排不佳、检索无效、切片不完整、未获取知识。每种归因类型都有对应的优化方向。

## 限制与注意事项

- 自动评测仅支持已发布且配置知识库的智能体应用
- 自动评测需开通应用观测功能，评测期间不可关闭
- 多应用横向评测最多支持 8 个应用
- 评测集生成和评测任务为离线任务，需后台排队执行
- 评测任务分步计费，即使后续步骤失败，已消耗的 Token 仍会计入用量
- 新版评测任务创建后配置不可修改
- 子账号需要 `管理员` 或 `应用评测-操作` 权限

## 最佳实践

建议在以下场景触发评测：知识库更新后、调整 Prompt 后、更换/升级模型后、调整检索/重排策略后，以及定期回归（每周或每月）。

推荐的优化闭环：识别 BadCase → 归因分析定位问题 → 针对性优化配置 → 发布新版本并再次评测 → 对比结果确认改进。通过多应用横向评测，可以对比不同版本的效果，验证迭代的有效性。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)


