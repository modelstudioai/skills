# application evaluation

阿里云百炼的应用[评测](../concepts/evaluation.md)能力用于系统化评估[智能体应用](../concepts/agent-application.md)、工作流应用的输出质量。覆盖[评测](../concepts/evaluation.md)集管理、[评测](../concepts/evaluation.md)任务编排、自动评估器评分、人工标签标注、评测报告分析等全流程，支持自动评测与手动评测两种范式，并区分"旧版"与"新版"两套界面。

## 评测范式

应用评测存在两条主线：

- **自动评测**：基于应用关联的[知识库](../concepts/knowledge-base.md)，由大模型自动生成评测集并评分（1-5 分），产出评分、BadCase 分析、归因分析和调优建议。详见 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。仅面向已发布且配置[知识库](../concepts/knowledge-base.md)的[智能体应用](../concepts/agent-application.md)，要求开通"应用观测"，单次最多 8 个应用横向评测。
- **手动评测**：人工构建评测集，对应用输出逐条打标（较差/一般/较好，或 1-5 分），适合有领域专家介入的端到端验证。详见 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。

> **注意**：当前控制台已推出"新版应用评测"，在评测任务、评估器、标签管理页面左上角单击"返回旧版"可回到旧版自动评测界面。新版与旧版在评测集类型、关联应用范围、评估器机制上有显著差异，使用前请先确认所处版本。

## 评测集

评测集是评测任务的数据基础，支持自动生成与手动上传两种创建方式，文件格式与字段要求因评测集类型而异。详见 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)。

### 旧版评测集类型

- **对话分析**：`.xls`/`.xlsx`，字段为 Prompt（用户输入）、Completion（参考答案）、SessionId（相同 SessionId 视为多轮对话）。适用于手动评测。
- **知识问答**：`.jsonl`，字段为 query、queryType、referenceAnswer、fineKeywords（嵌套数组，每个子数组为一个独立信息点）、coarseKeywords（1-3 个核心主题词）。适用于自动评测。

### 新版评测集类型

新版评测集支持 **智能体**、**工作流**、**自定义** 三种类型，按所选应用的出入参形式自动生成数据模板，自定义类型可任意定义表结构。手动上传支持 `.xls`/`.xlsx`，单文件不超过 20MB，单次最多 10 个文件；存储位置固定为平台存储；创建后类型不可修改。详见 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。

### 创建与管理

- 自动生成仅支持知识问答类型，且仅支持 `qwen-max` 和 `qwen-plus` 模型。
- 手动上传需先下载模板填写，再上传并**发布**后才能用于评测任务；草稿状态不可用。
- 修改通过"增量导入"完成：支持单条新增、批量导入、全量覆盖三种方式；每次发布生成新版本，评测任务可选特定版本。

## 评测任务

评测任务串联评测集、被测应用、评估器和标签，是新版应用评测的核心。详见 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

### 关键配置

- **任务名称**：最多 50 字符；**任务描述**：最多 200 字符。
- **选择评测集**：从已发布评测集中选择集合与版本。
- **选择应用**：支持三种关联方式——不关联应用（纯人工标注）、工作流、智能体。
- **评估器**：每个评测任务最多添加 10 个评估器，建议组合 3-5 个覆盖不同维度（如 LLM + Code 组合）。所有变量必须完成参数映射后才能保存。
- **标签**：可选，用于人工标注。

> **注意**：评测任务发起后配置不可修改，如需调整请创建新任务。任务调用大模型产生的 [Token](../concepts/token.md) 费用正常[计费](../concepts/billing.md)。

### 任务详情与结果

任务详情页提供"数据明细"与"指标统计"两个视图。数据明细展示每条评测数据的评估器评分结果，支持普通模式与快速标注两种标注模式；单条标注页分为评测集数据、应用输出、人工标注三栏，可通过上一条/下一条逐条切换。指标统计展示综合得分、评测进度、各评估器通过率及数据项分布。

## 评估器

评估器定义"如何评分"，可被多个评测任务复用。百炼提供预置模板与自定义创建两种途径，自定义又细分为 LLM 评估器、Code 评估器和基于评测任务创建。详见 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

### 预置评估器模板

按通用质量、智能体、文本匹配、文本相似度、格式校验五类组织。不同模板对评测集字段有不同必选参数要求（如"问答相关性"要求 query 和 response），建议构建评测集前先确认所需字段。

### 自定义评估器

- **LLM 评估器**：用大模型评分，适合相关性、有害性、幻觉检测等需要语义理解的场景。配置项含模型选择、Prompt、评分范围、通过阈值；建议使用 32B 以上参数量模型，并通过试运行验证。
- **Code 评估器**：用 Python 3.10 函数实现评分逻辑，适合格式校验、数值计算、精确匹配。函数签名须包含所有入参，必须返回数值类型评分，建议包含错误处理。
- **基于评测任务创建**：从已完成标注的历史评测任务中自动抽象出 LLM 评估器。必须选择已完成评估的评测任务；`label_score` 映射的是评测任务中评估器的输出分数，而非评测集原始字段；不支持试运行。

### 评分规则与使用

评分范围决定打分尺度（精细评估用 0-100，快速分类用 0-1 或 1-5），通过阈值决定 Pass/Fail。在评测任务中使用时，需将评估器参数（query、reference_response、context 等）映射到评测集字段或应用输出。映射错误会导致评估器失效，须仔细核对字段名。

### LLM 与 Code 评估器对比

| 对比项 | LLM 评估器 | Code 评估器 |
| --- | --- | --- |
| 评估方式 | 大模型语义理解 | 代码规则判断 |
| 优势 | 灵活，适应复杂场景 | 精确，可重复 |
| 适用场景 | 相关性、有害性、幻觉检测 | 格式校验、数值计算、精确匹配 |
| 成本 | 产生 [Token](../concepts/token.md) 费用 | 无额外费用 |

## 标签管理

标签是评测与应用观测共用的核心组件，用于多维度标注与筛选。详见 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)。

### 标签类型

- **分类标签**：从预定义选项多选，最多 20 个选项，筛选用属于/不属于。示例：回答质量（较差/一般/较好）。
- **布尔值标签**：True/False 二选一，适合是否正确、是否存在幻觉等二元判断。
- **数字标签**：Double 类型，支持等于/不等于/大于/大于等于/小于/小于等于筛选。示例：1-5 分评分。
- **文本标签**：String 类型自由输入，支持包含/不包含筛选。示例：错误原因说明、改进建议。

### 使用方式

标签名称必填（1-50 字），描述可选（0-200 字）。在评测任务详情页通过"标签配置"添加标签后，可在数据明细中按标签筛选；应用观测模块中可对每个 Span 标注标签，实现对线上真实数据的质量评估，标注内容自动保存。

## 自动评测报告与归因

自动评测使用大模型对每个回答评分（1-5 分），评分时对比智能体输出与参考答案，评估准确性、完整性和相关性。5 分优秀，4 分良好，4 分以下触发自动归因。

### 报告内容

- **总正确率**：得分不低于 4 分的回答数 / 总回答数 × 100%，多应用评测以图表对比。
- **BadCase 分析**：默认按分数从低到高展示 Top-5 错误条目，无 BadCase 时列表为空。
- **调优建议**：针对 Prompt、检索配置、[知识库](../concepts/knowledge-base.md)切片给出具体优化建议。
- **RAG 智能体评价**：按问题类型（事实型、分析型、比较型、教程型）展示单项得分，分优秀（≥4）、良好（2-4）、待提升（<2）三档。

### 归因类型与优化建议

- **模型理解有误**：已获取正确知识但提示词不明确或模型能力不足——补充清晰回答要求或切换更强模型。
- **重排不佳**：正确切片被召回但排序靠后——调整重排配置或增加传给模型的切片数。
- **检索无效**：检索策略不合适导致召回过多或过少——根据数据特点调整检索方式。
- **切片不完整**：切分粒度过细导致语义单元被分割——增大切片长度或启用语义切分。
- **未获取知识**：知识库无结果或缺失相关内容——补充相应知识。

## 限制与注意事项

- 自动评测仅支持 `qwen-max` 和 `qwen-plus` 模型（评测集生成与评测打分均限）。
- 自动评测仅面向已发布、配置知识库的[智能体应用](../concepts/agent-application.md)；多应用横向评测时所有应用须关联至少一个相同知识库；横向评测最多 8 个应用，追加评测后总数同样不超过 8。
- 评测期间请勿关闭应用观测，否则可能导致任务失败、数据丢失或报告不准确。
- 评测任务分步执行，每个成功步骤都会消耗 [Token](../concepts/token.md) 并[计费](../concepts/billing.md)，后续步骤失败不影响已消耗 Token 的[计费](../concepts/billing.md)。
- 评测报告只显示成功完成的用例，失败用例不计入正确率。
- 评测集生成与评测均为离线任务，需后台排队，排队期间进度保持 0%。
- 评估器删除后无法恢复；被评测任务引用的评估器不可删除。
- 新版评测集类型创建后不可修改。
- 子账号（RAM 用户）使用自动评测需具备"管理员"或"应用评测-操作"权限。

## 持续评测与优化闭环

单次评测仅反映特定时间点表现，建议在以下场景触发评测：知识库更新后、调整 Prompt 后、更换或升级模型后、调整检索/重排策略后、定期回归（每周或每月）。

优化闭环建议按"识别 BadCase → 分析归因定位问题 → 实施针对性优化 → 发布新版本再次评测 → 对比结果确认改进"五步迭代，未达预期则返回第一步开始新一轮循环。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)




