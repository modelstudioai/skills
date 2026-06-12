# application evaluation

阿里云百炼提供应用评测功能，用于系统化评估智能体应用和工作流应用的输出质量。平台支持自动评测（基于大模型自动打分与归因分析）和手动评测（人工构建评测集并标注打分）两种模式，帮助开发者在应用上线前后持续监控和优化应用效果。

## 评测模式

### 自动评测

自动评测利用大模型基于应用关联的知识库自动生成评测集，对智能体的回答进行评分并生成评测报告与调优建议。支持两种子模式：

- **单应用评测**：深度评估单个智能体应用，生成评分、错误分析和优化建议的详细报告。
- **多应用横向评测**：在同一评测基准下对比最多 8 个应用（或同一应用的不同版本），用于选型决策或版本迭代验证。

前提条件：应用必须已发布、已配置知识库、已开通应用观测。详细流程参见[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。

### 手动评测

手动评测通过人工构建评测集（对话分析类型），对应用的回答进行人工分析与评分，产出评测报告。适用于需要领域专家主观判断的场景。操作流程为：准备评测集 → 上传并发布 → 创建评测任务 → 人工标注打分 → 查看评测报告。详见[手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。

### 新版评测任务

新版评测系统支持智能体和工作流两种应用类型，引入了评估器（自动评分）和标签（人工标注）的组合机制，实现更灵活的多维度评测。详见[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

## 评测集

评测集是评测任务的数据基础，用于存储和管理评测数据。

### 旧版评测集类型

| 类型 | 文件格式 | 适用场景 |
|------|----------|----------|
| 对话分析 | `.xls`/`.xlsx` | 手动评测，支持单轮和多轮对话 |
| 知识问答 | `.jsonl` | 自动评测，包含 query、referenceAnswer、关键词等字段 |

### 新版评测集类型

| 类型 | 说明 |
|------|------|
| 智能体 | 根据智能体应用的出入参形式定义，适用于智能体评测 |
| 工作流 | 根据工作流应用的出入参形式定义，适用于工作流评测 |
| 自定义 | 任意定义表结构，适用于特殊评测场景 |

创建方式包括手动上传、自动生成（仅知识问答类型）和从应用观测导入。评测集支持版本管理，每次发布生成新版本。详见[新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。

> **注意**：旧版评测集（对话分析/知识问答）与新版评测集（智能体/工作流/自定义）是两套独立体系。旧版评测集可在新版页面左上角点击"返回旧版"使用。

## 评估器

评估器是新版评测系统的核心组件，用于自动评估应用输出质量。

### 评估器类型

| 类型 | 评估方式 | 适用场景 | 成本 |
|------|----------|----------|------|
| LLM 评估器 | 大模型语义理解 | 相关性、有害性、幻觉检测 | 产生 Token 费用 |
| Code 评估器 | Python 代码规则判断 | 格式校验、数值计算、精确匹配 | 无额外费用 |
| 基于评测任务 | 从历史标注数据学习规则 | 将人工标注经验固化为自动评估 | 产生 Token 费用 |

### 预置模板分类

- **通用质量**：评估回答的基本质量指标
- **智能体**：评测智能体应用的各项能力
- **文本匹配**：精确规则文本匹配
- **文本相似度**：计算文本相似度得分
- **格式校验**：验证输出格式规范性

每个评测任务最多添加 10 个评估器。建议组合使用 3-5 个评估器从不同维度评估，如：相关性（LLM）+ 格式校验（Code）。详见[评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

## 标签管理

标签用于人工标注，支持四种类型：

| 类型 | 说明 | 典型场景 |
|------|------|----------|
| 分类 | 从预定义选项中多选 | 回答质量（较差/一般/较好） |
| 布尔值 | True/False 二选一 | 是否存在幻觉 |
| 数字 | Double 数值输入 | 评分 1-5 分 |
| 文本 | 自由文本输入 | 错误原因说明 |

标签可同时在评测任务和应用观测中使用，实现线上真实数据的质量评估。详见[标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 自动评测归因分析

对得分低于 4 分的 BadCase，系统自动进行归因分析，定位 RAG 流程中的问题环节：

| 归因类型 | 含义 | 优化方向 |
|----------|------|----------|
| 模型理解有误 | 已获取正确知识但推理错误 | 优化 Prompt 或切换更强模型 |
| 重排不佳 | 正确切片被召回但排序靠后 | 调整重排配置或增加切片数量 |
| 检索无效 | 检索策略不当，召回过多或过少 | 调整检索方式 |
| 切片不完整 | 切分粒度过细，语义单元被分割 | 增大切片长度或启用语义切分 |
| 未获取知识 | 知识库缺失相关内容 | 补充知识库 |

## 最佳实践

### 触发评测的时机

- 知识库更新后
- 调整 Prompt 后
- 更换或升级模型后
- 调整检索/重排策略后
- 定期回归（每周或每月）

### 优化闭环

1. 识别 BadCase（得分 < 4 分）
2. 分析归因，定位问题环节
3. 实施针对性优化
4. 发布新版本，用同一评测集再次评测
5. 对比新旧版本报告，验证效果

## 计费与限制

- 自动评测仅支持使用 `qwen-max` 和 `qwen-plus` 模型生成评测集和执行评测。
- 评测费用 = 评测产生的 Tokens x 模型调用单价，以实际账单为准。
- 多应用横向评测中所有被选应用必须关联至少一个相同的知识库。
- 评测任务运行期间不可关闭应用观测，否则可能导致任务失败或数据丢失。
- 评测任务创建后配置不可修改，如需变更请创建新任务。
- 单次上传评测集文件最多 10 个，单文件不超过 20MB。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)





