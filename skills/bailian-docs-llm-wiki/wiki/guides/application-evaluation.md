# application evaluation

应用评测是阿里云百炼平台用于系统化验证智能体与工作流输出质量的核心功能。平台提供人工标注与大模型自动打分双模评测体系，结合自定义评估器、多维标签与归因分析模块，输出结构化评测报告与调优建议，支撑开发者完成应用上线前的端到端验证与持续迭代优化。

## 支持的模型与功能
- **评测模式**：支持[[自动评测]]（单应用深度诊断、最多8个应用横向对比）与[[手动评测]]（基于对话历史或标准答案逐条打标）。
- **应用类型**：兼容已发布的智能体应用与工作流应用。
- **评估模型**：评测集自动生成与内置自动评估默认使用 `qwen-max` 或 `qwen-plus`。自定义 LLM 评估器建议选用 32B 及以上参数量模型以提升语义判断稳定性。

## 关键参数
| 组件 | 关键配置项与约束 |
|:---|:---|
| **[[评测集]]** | 新版支持智能体、工作流、自定义表结构；旧版区分对话分析（`.xls/.xlsx`）与知识问答（`.jsonl`）。单文件上限 20MB，单次最多上传 10 个文件。字段需包含 `query`/`response` 等评估器必参映射源。 |
| **[[评估器]]** | 支持 `LLM`（语义理解，需配置 Prompt、评分范围、通过阈值）与 `Code`（Python 规则脚本，无额外 Token 成本）。变量必须完成映射，单任务最多绑定 10 个评估器。 |
| **[[评测任务]]** | 需绑定已发布的[[评测集]]版本与应用（或选择“不关联应用”用于纯人工场景）。配置提交后锁定，不可中途修改应用或数据集映射。 |
| **[[标签管理]]** | 支持分类（最多20个枚举选项）、布尔值、数字（Double）、文本四种类型。用于主观维度标注与数据过滤统计。 |

## 使用方式
1. **准备数据与组件**：下载模板填充标准答案或使用知识库自动生成数据。按需创建评估器与业务标签。
2. **发起任务**：创建[[评测任务]]，完成数据集版本、目标应用、评估器参数映射及人工标签绑定。
3. **执行与标注**：
   - 自动模式：后台按采样策略调度大模型批量打分，生成 BadCase 列表、正确率统计及 RAG 归因分析。完整流程参考 [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
   - 人工模式：在任务详情页使用“普通模式”或“快速标注”界面对照原始输出进行打分。交互指南参考 [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
4. **结果分析与迭代**：基于评分分布与标签统计定位薄弱环节，调整 Prompt、知识库切片策略或检索重排参数后发布新版本，复用原数据集进行回归对比。数据结构管理规范详见 [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)

## 限制和注意事项
> **注意**：文档体系存在新旧版本差异。旧版架构仅支持智能体应用且评测集格式固定；当前平台已升级为支持工作流、自定义表结构与独立评估器/标签体系的新架构。旧版入口保留用于过渡，新接入项目请直接使用新版控制台。

- **任务不可变性**：评测任务发起后，关联的数据集版本、应用及评估器映射配置均锁定。若需调整参数或更换数据集，必须新建任务。
- **计费逻辑**：评测产生的 Token 按实际调用量计费。界面“预估最大消耗”为防异常输出的硬性成本上限，“预估平均消耗”仅供参考，最终结算以账单为准。Code 评估器不产生额外费用。
- **环境与状态依赖**：执行自动评测前必须开通[[应用观测]]且应用处于已发布状态。评测期间关闭观测可能导致任务中断或报告失真。
- **离线队列机制**：自动评测集生成与批量任务执行属异步离线流程。后台排队期间控制台进度可能显示 0%，属正常调度状态，请勿重复点击或中途删除数据。
- **结果偏差防范**：复用已有知识问答评测集时，若参考答案内容未覆盖在当前知识库切片中，自动评估器的相关性打分将产生系统性偏差。

## 来源文档

- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)

