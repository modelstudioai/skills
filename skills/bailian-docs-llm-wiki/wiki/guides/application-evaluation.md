# application evaluation

百炼平台的应用评测能力提供自动与手动两种评测路径，支持对智能体、工作流等应用的输出质量进行系统化评估。核心目标是通过结构化评测集、可配置评估器和多维度标签体系，实现从问题发现、归因分析到优化验证的完整闭环。评测结果既可用于单应用深度调优，也支持多应用横向对比选型。

## 支持的模型/功能

- **自动评测**：基于知识库自动生成评测集，利用大模型（当前仅支持 `qwen-max` 和 `qwen-plus`）对智能体回答进行语义评分，并输出 BadCase 归因（如“检索无效”“切片不完整”）与调优建议 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建 `.xls`/`.xlsx` 格式的对话分析评测集，通过人工打标（较差/一般/较好）完成效果验证 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：引入模块化设计，包含**评测集**（支持智能体/工作流/自定义三类）、**评估器**（预置模板、LLM、Code、基于历史任务生成四类）、**标签管理**（分类/布尔/数字/文本四类标注维度）和**评测任务**四大组件，支持灵活组合与复用 [新版应用评测](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation.md)。

> **注意**：文档 1（自动评测）明确限定仅支持已发布的 Agent 1.0 应用；而文档 4（新版评测集）和文档 8（评测任务）均指出新版体系支持“智能体”和“工作流”两类应用。二者存在适用范围差异——旧版自动评测功能仅覆盖智能体，新版评测任务则扩展至工作流。开发者应根据实际应用类型选择对应评测路径。

## 关键参数

- **评测集字段**：知识问答类需包含 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords` 和 `queryType`；对话分析类需包含 `Prompt`、`Completion` 和可选 `SessionId` [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。
- **评估器配置**：
  - LLM评估器：需指定模型、编写 Prompt、设置评分范围（如 0–5 或 0–100）及通过阈值；
  - Code评估器：需定义入参（如 `query`, `response`）、编写 Python 函数并返回数值评分；
  - 所有评估器均需完成**参数映射**（如将评估器变量 `response` 映射至评测集字段 `Completion`），否则无法运行 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签类型**：分类（多选枚举）、布尔（True/False）、数字（Double）、文本（String），每类对应不同筛选条件与标注方式 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备数据**：创建并发布评测集（支持自动生成或手动上传 `.jsonl`/`.xls`/`.xlsx` 文件）；
2. **配置评估逻辑**：创建评估器（推荐组合使用 LLM + Code 类型，例如“相关性（LLM）+ JSON格式校验（Code）”）；
3. **构建评测任务**：在[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task)页面选择评测集、关联应用（智能体/工作流/不关联）、添加评估器并完成参数映射、可选添加标签；
4. **执行与分析**：发起任务后，在详情页查看自动评分结果、人工标注数据、指标统计（综合得分、各评估器通过率）及 BadCase 分析。

## 限制和注意事项

- **数量限制**：单次多应用横向评测最多支持 8 个应用；单个评测任务最多添加 10 个评估器；单次上传评测集文件最多 10 个，单文件 ≤20MB。
- **权限要求**：子账号需具备 `管理员` 或 `应用评测-操作` 权限方可使用自动评测功能 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **依赖前提**：自动评测要求应用已发布、已配置知识库、且已开通并启用“应用观测”功能；未满足任一条件将导致任务失败或结果不准。
- **版本约束**：评测集发布后类型不可修改；评测任务创建后配置不可更改（如需调整，须新建任务）；基于评测任务创建的评估器不支持试运行 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **计费说明**：LLM评估器调用产生 Token 费用；Code评估器无额外费用；所有评测任务产生的 Token 消耗可在控制台查看，最终以账单为准。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [新版应用评测](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)


