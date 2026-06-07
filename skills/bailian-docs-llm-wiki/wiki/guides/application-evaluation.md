# application evaluation

阿里云百炼的应用评测体系用于系统化评估智能体应用与工作流应用的输出质量，覆盖从评测数据准备、自动/人工评分到结果分析的全流程。当前平台同时提供旧版（自动评测 + 手动评测）和新版（评测集 + 评测任务 + 评估器 + 标签）两套形态，新版基于评估器与标签解耦评分逻辑与任务执行，更适合长期沉淀业务评测体系。

## 评测形态总览

百炼共有两种相关但相互独立的评测入口：

- **旧版自动评测**：基于知识库自动生成评测集，使用大模型对智能体回答打分（1-5），输出 BadCase 与归因分析，仅面向**已发布**、**已配置知识库**、**已开通应用观测**的智能体应用。详见 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **旧版手动评测**：人工构建评测集，对应用回答做"较差/一般/较好"的人工打标，产出评测报告。详见 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测任务**：以"评测集 + 应用 + 评估器 + 标签"为单位组装评测任务，支持自动评分与人工标注混用，覆盖智能体应用、工作流应用以及纯人工标注场景。详见 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

> **注意**：新版评测任务页面左上角的"返回旧版"按钮可切换回旧版应用评测；同名功能（如"评测集"）在新旧版下数据结构与可选类型不同，互不通用，建议团队内统一一种版本。

## 评测集

评测集是所有评测流程的数据基础，存在两类型号的实现：

### 旧版评测集

旧版仅支持两种类型，详见 [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)：

- **对话分析**（`.xls`/`.xlsx`）：字段为 `Prompt`、`Completion`、`SessionId`，相同 `SessionId` 的多行视为同一多轮对话，主要供手动评测使用。
- **知识问答**（`.jsonl`）：字段为 `query`、`queryType`、`referenceAnswer`、`fineKeywords`（嵌套数组，每个子数组为一个独立信息点）、`coarseKeywords`（1-3 个核心主题词），主要供自动评测使用。

两种类型单次最多上传 10 个文件、单文件不超过 20 MB。

### 新版评测集

新版评测集支持三种类型，详见 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)：

| 类型 | 适用场景 | 表结构 |
| --- | --- | --- |
| 智能体 | 评测智能体应用 | 根据所选应用的出入参自动生成 |
| 工作流 | 评测工作流应用 | 根据所选工作流的出入参自动生成 |
| 自定义 | 自定义评测/纯人工标注 | 自由添加列与字段类型 |

关键约束：

- **类型一旦创建不可修改**。
- 评测集需经过**发布**才能被评测任务引用；已被引用的评测集无法删除。
- 每次发布生成一个新版本，评测任务创建时可指定具体版本。
- 数据导入除手动上传外，还可从**应用观测**直接拉真实数据。

## 评测任务

新版评测任务把"评测集 + 应用关联 + 评估器 + 标签"四件事组合成一次评测，配置完成后**不可修改**（标签除外，可随时追加），详见 [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)。

核心字段：

- **选择评测集**：从已发布列表选择评测集与版本。
- **选择应用**：三选一
  - `不关联应用`：纯人工标注。
  - `工作流`：使用评测集数据调用工作流。
  - `智能体`：使用评测集数据调用智能体。
- **评估器**：单任务最多 10 个，所有变量必须完成参数映射后才能保存。官方建议添加 3-5 个评估器从多维度评估，例如"相关性（LLM）+ 格式校验（Code）"、"正确性（LLM）+ 字符串匹配（Code）"。
- **标签**：可选，用于人工标注，创建后仍可在详情页通过"标签配置"追加。

任务详情页提供：

- **数据明细**：展示每条评测数据、评估器自动评分（0-1 或自定义范围）、人工标签结果，支持普通模式与快速标注两种交互。
- **指标统计**：展示综合得分、评测进度，以及基于标签的统计分析。

> **注意**：评测任务一旦发起即扣 Token，调用模型按 [模型列表](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md) 中的价格计费；旧版自动评测在评测过程中产生的中间步骤即便最终任务失败，已消耗的 Token 仍计入用量。

## 评估器（新版）

评估器定义"如何评分"的规则，独立于评测任务存在，可被多个任务引用，详见 [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)。

三种创建方式：

1. **基于预置模板**：覆盖"通用质量、智能体、文本匹配、文本相似度、格式校验"五大分类。
2. **自定义 LLM 评估器**：用大模型按 Prompt 打分，适合相关性、幻觉、有害性等需要语义理解的场景；评估模型限时免费。
3. **自定义 Code 评估器**：Python 3.10 函数实现，函数签名需包含全部入参并返回数值评分，适合格式校验、数值计算、精确匹配等需要确定性的场景。
4. **基于评测任务**：用已完成标注的历史评测任务自动抽象出 LLM 评估器，将标注经验固化为自动化规则；该方式**不支持试运行**，且只能选择"已完成评估"的任务。

通用配置：

- **评分范围**：作为提示词写入系统提示词，与 Prompt 内的评分尺度必须一致。精细评估建议 0-100；快速分类建议 0-1 或 1-5。
- **通过阈值**：`评分 ≥ 阈值` 判定为 Pass，通常取评分范围中位数。
- **参数映射**：在评测任务中使用评估器时，需将评估器形参（如 `query`、`response`、`reference`、`label_score`）映射到评测集字段或应用输出，**所有变量必须完成映射**才能保存任务。

LLM 评估器与 Code 评估器对比：

| 对比项 | LLM 评估器 | Code 评估器 |
| --- | --- | --- |
| 评估方式 | 大模型语义理解 | 代码规则判断 |
| 优势 | 灵活，适应复杂场景 | 精确、可重复 |
| 典型场景 | 相关性、有害性、幻觉检测 | 格式校验、数值计算、精确匹配 |
| 成本 | 产生 Token 费用 | 无额外费用 |

## 标签管理（新版）

标签是评测任务与应用观测共用的人工标注组件，支持四种类型，详见 [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)：

| 类型 | 取值 | 标注方式 | 筛选条件 | 适用场景 |
| --- | --- | --- | --- | --- |
| 分类标签 | 最多 20 个自定义选项 | 下拉多选 | 属于 / 不属于 | 回答质量、错误类型、情感倾向 |
| 布尔值标签 | 固定 True/False | 二选一 | 属于 / 不属于 | 是否正确、是否有幻觉、是否符合规范 |
| 数字标签 | Double（整数或小数） | 输入框 | =、≠、>、≥、<、≤ | 评分（1-5）、相关性得分（0-1）、完整度（0-100） |
| 文本标签 | 任意 String | 输入框 | 包含 / 不包含 | 错误原因说明、改进建议、备注 |

使用要点：

- 标签先在"标签管理"创建，然后在评测任务详情页通过"标签配置"挂载。
- **快速标注**模式下分类与布尔值标签显示为下拉，数字与文本标签显示为输入框，编辑后立即保存。
- 在**应用观测**侧，可对 Span 直接打标签，标注内容自动保存，过滤器中会自动列出已使用的标签作为筛选项。

## 旧版自动评测流程

旧版自动评测全程分四步（详见 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)）：

1. **创建评测任务**：可选 1 个应用做深度评测，或最多 8 个应用做横向对比。横向评测要求所有所选应用至少共享一个相同知识库。
2. **设置评测集**：可由大模型按知识库自动生成（默认任务类型：事实型、分析型、比较型、教程型，可自定义新增；需选 2-8 种类型），也可选已有评测集，但必须确保参考答案能在当前知识库中找到。
3. **配置评测规则**：按任务类型设置分类采样数，得到本次评测样本总数。评测/生成模型仅支持 `qwen-max` 与 `qwen-plus`；可先**试运行**抽 1 题预览结果，仅支持单应用预览。
4. **执行评测**：发起后任务在后台排队，进度长时间停在 0% 是正常的；任务完成后可"追加评测"加入新应用对比（总数不超过 8）。

> **注意**：自动评测期间**不得关闭应用观测**，否则可能导致任务失败、数据丢失或报告不准确；评测报告只显示成功完成的用例，失败用例不计入正确率。

### 评分与归因

- 评分 1-5：5 分优秀、4 分良好，**低于 4 分被视为错误并触发归因分析**。
- 总正确率 = 得分 ≥ 4 的回答数 / 总回答数。
- BadCase 列表默认按分数升序展示 Top-5，可下载全部结果。
- 归因类型与建议：
  - **模型理解有误**：补充更清晰的回答要求或换更强的模型。
  - **重排不佳**：调整重排配置或增加传给模型的切片数。
  - **检索无效**：调整检索策略，避免召回过多或过少。
  - **切片不完整**：增大切片长度或启用语义切分。
  - **未获取知识**：向知识库补充相关内容。

### 持续评测建议

下列场景应触发新一轮评测：知识库变更、Prompt 调整、模型更换/升级、检索/重排策略调整、定期回归（周/月）。建议按"识别 BadCase → 归因 → 针对性优化 → 发布新版本 → 再评测对比"形成闭环。

## 旧版手动评测流程

旧版手动评测面向"已发布的智能体应用 + 上传发布过的对话分析评测集"，由人工对应用输出做"较差/一般/较好"的打标，详见 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)：

1. 下载模板填写 `Prompt`/`Completion`/`SessionId`，上传到评测集页面，等待"导入成功"后发布（草稿状态不可用）。
2. 在"手动评测"页面创建任务，选择已发布应用、已发布评测集，再选择评测维度（无自定义时可用内置模板）。
3. 系统按评测集调用应用推理生成结果，进入"标注中"状态后逐条人工打标，全部完成后提交。
4. 评测费用 = 评测产生的 Tokens × 模型调用单价，使用独占资源部署的模型不收费。

## 计费与限制

- 旧版自动评测：评测集生成与评测均产生 Token 消耗，仅 `qwen-max` 与 `qwen-plus` 可用；预估"平均消耗"为参考值、"最大消耗"为成本硬上限。
- 旧版手动评测：按推理实际产生的 Tokens 计费，独占资源部署不收费。
- 新版评测任务：评估器调用大模型的 Token 按 [模型列表](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md) 计费，可在评测任务列表查看消耗明细。
- 权限：旧版自动评测需要 RAM 子账号具备"管理员"或"应用评测-操作"权限。
- 横向对比：旧版自动评测单任务最多 8 个应用；新版评测任务单任务最多 10 个评估器。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)



