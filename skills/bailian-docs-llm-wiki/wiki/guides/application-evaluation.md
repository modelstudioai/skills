# application evaluation

应用评测是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与人工双路径评测机制。通过评测集驱动、多维度评估器打分与人工标签标注相结合的方式，开发者可量化分析回答准确性、相关性、完整性等关键指标，并基于归因分析定位 RAG 流程中的瓶颈环节（如检索失效、切片不完整、模型理解偏差等），形成“评测→分析→优化→再验证”的闭环迭代。

## 支持的模型/功能

- **自动评测**：面向已发布的[智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)，基于知识库自动生成评测集，支持单应用深度评测与最多 8 个应用的横向对比；当前仅支持 `qwen-max` 和 `qwen-plus` 模型用于评测集生成与最终评分 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建评测集（`.xls`/`.xlsx` 格式），通过人工打标完成效果评估，适用于需强主观判断或无标准答案的场景 [原文标题](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**：包含评测集、评测任务、评估器和标签管理四大模块，支持智能体、工作流、自定义三类评测集，允许混合使用 LLM 评估器（语义理解）与 Code 评估器（规则校验），并支持人工标签多类型标注（分类/布尔/数字/文本） [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation.md)。

> **注意**：旧版自动评测（文档 1）与新版评测体系（文档 4–8）并存，但功能定位存在重叠与演进关系。新版明确支持工作流应用评测、自定义表结构评测集及组合式评估器，而旧版仅限智能体应用且依赖固定知识库生成逻辑。开发者应优先采用新版体系，旧版文档仅作兼容参考。

## 关键参数

- **评测集类型**：
  - `知识问答`（`.jsonl`）：用于自动评测，含 `query`、`referenceAnswer`、`coarseKeywords`、`fineKeywords`、`queryType` 字段；
  - `对话分析`（`.xls`/`.xlsx`）：用于手动评测，含 `Prompt`、`Completion`、`SessionId` 字段；
  - 新版还支持 `智能体`/`工作流`/`自定义` 三类结构化评测集，字段可编辑 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。
- **评估器参数**：
  - LLM 评估器：需配置 `模型`、`Prompt`、`评分范围`（如 0–1 或 1–5）、`通过阈值`；
  - Code 评估器：需定义入参（如 `query`, `response`）、Python 执行函数及评分范围；
  - 所有变量必须完成字段映射后方可保存评测任务 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。
- **标签类型**：支持分类（多选枚举）、布尔值（True/False）、数字（Double）、文本（String）四类，用于人工标注与筛选 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

## 使用方式

1. **准备评测数据**：
   - 自动生成：在[自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)中选择知识库与任务类型（事实型/分析型等），由 `qwen-max`/`qwen-plus` 生成 `.jsonl` 评测集；
   - 手动上传：按模板填写 `.xls`/`.xlsx`（对话分析）或 `.jsonl`（知识问答），发布后方可使用；
   - 新版创建：在[新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)中选择类型（智能体/工作流/自定义），下载模板、填充并上传。

2. **配置评测任务**：
   - 旧版：在自动评测流程中依次完成“创建任务→设置评测集→配置规则→执行评测”；
   - 新版：在[评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)中选择评测集与应用（智能体/工作流/不关联），添加 1–10 个评估器并完成参数映射，可选配人工标签。

3. **执行与分析**：
   - 自动评测：系统调用模型运行，生成含总正确率、BadCase 归因（如“检索无效”“切片不完整”）、RAG 分项得分的报告；
   - 新版任务：在详情页查看“数据明细”（含各评估器评分与人工标签）与“指标统计”（综合得分、通过率柱状图、数据分布）。

## 限制和注意事项

- **应用要求**：自动评测仅支持已发布的智能体应用（Agent 1.0），且必须配置知识库并开通[应用观测](../../raw/application-user-guide/application-monitoring/application-observation.md)功能；新版评测任务支持工作流应用，但旧版不支持。
- **数量限制**：单次自动评测最多选择 8 个应用；评测集单文件 ≤20 MB，单次上传 ≤10 个文件；每个评测任务最多添加 10 个评估器。
- **权限与状态**：子账号需具备 `管理员` 或 `应用评测-操作` 权限；评测集与评测任务创建后，仅草稿状态可编辑，发布/创建后不可修改配置（如需调整，须新建）。
- **[Token](../concepts/token.md) 消耗**：所有模型调用均产生 [Token](../concepts/token.md) 费用，预估消耗为参考值，实际以账单为准；`预估最大消耗` 是防超长输出的成本硬上限，实际消耗通常远低于此值。
- **评测失败处理**：部分用例执行失败时，仅成功用例计入正确率统计；失败步骤若已消耗 [Token](../concepts/token.md)，仍会计费。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版应用评测](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)


