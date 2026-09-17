# application evaluation

应用评测是百炼平台用于系统化评估智能体/工作流应用输出质量的核心能力，支持自动与人工双路径评测机制。通过结构化评测集、可配置评估器和多维度标签体系，开发者可量化分析回答准确性、相关性、完整性等关键指标，并基于归因分析快速定位 RAG 流程中的瓶颈环节（如检索无效、切片不完整、模型理解有误等），形成“评测→分析→优化→再评测”的闭环迭代。

## 支持的模型/功能

- **自动评测**：面向已发布的[智能体应用（Agent 1.0）](../../raw/application-user-guide/llm-application/single-agent-application.md)，基于知识库自动生成评测集，支持单应用深度评测与最多 8 个应用的横向对比；仅支持 `qwen-max` 和 `qwen-plus` 模型用于评测集生成与最终评分 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **手动评测**：支持人工构建评测集并进行人工打标，适用于需主观判断或无标准答案的业务场景 [原文标题](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)。
- **新版评测体系**（推荐）：提供统一的评测任务入口，支持智能体、工作流、自定义三类应用评测；引入**评估器**（LLM/Code）、**标签管理**与**版本化评测集**，实现自动评分与人工标注协同 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation.md)。

> **注意**：文档 1（自动评测）与文档 6（新版评测任务）存在功能覆盖关系。文档 1 描述的是旧版单点自动评测流程，而文档 6 定义的新版评测任务已整合自动与人工能力，并明确支持“不关联应用”（纯人工标注）、工作流及智能体三类评测模式。新版为当前主推架构，旧版功能仍可通过页面右上角“返回旧版”访问，但新项目应优先采用新版。

## 关键参数

| 参数类别 | 名称 | 说明 | 约束 |
|----------|------|------|------|
| **评测集** | 类型 | `智能体` / `工作流` / `自定义`（新版）；`对话分析`（.xls/.xlsx）或`知识问答`（.jsonl）（旧版） | 创建后不可修改类型；知识问答型仅用于自动评测 [原文标题](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md) |
| **评估器** | 模型选择 | LLM评估器支持 `qwen-max` 等模型；Code评估器无模型依赖 | LLM评估器调用产生[Token](../concepts/token.md)费用；Code评估器免费 |
| **评估器** | 评分范围 & 通过阈值 | 如 `0-1`、`1-5`、`0-100`；阈值决定 Pass/Fail 判定 | 需与Prompt中描述一致；建议精细评估用大范围，快速分类用小范围 |
| **评测任务** | 应用关联 | 可选 `智能体`、`工作流` 或 `不关联应用` | “不关联应用”适用于纯人工标注场景，不触发模型调用 |

## 使用方式

1. **准备评测数据**  
   - 新版：在[评测集](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=evalSet)页面创建评测集，支持手动上传（.xls/.xlsx/.jsonl）或从应用观测导入；选择类型（智能体/工作流/自定义）后，系统自动生成字段模板 [原文标题](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)。  
   - 旧版：按格式要求准备文件（对话分析用 .xlsx，知识问答用 .jsonl），上传至评测集管理页并**发布**（草稿不可用）。

2. **配置评估能力**  
   - 创建[评估器](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=grader)：使用预置模板（如“问答相关性”）或自定义 LLM/Code 评估器；务必完成参数映射（如将 `query` 映射到评测集的 `Prompt` 字段）。  
   - 创建[标签](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=annotation)：定义分类、布尔值、数字或文本标签，用于人工标注维度（如“回答质量：较差/一般/较好”）。

3. **发起评测任务**  
   - 在[评测任务](https://bailian.console.aliyun.com/cn-beijing/?tab=app#/efm/app_evaluate/tabs?activeKey=task)页面创建任务，关联已发布的评测集与应用（或选择“不关联应用”），添加评估器与标签。  
   - 任务启动后，系统自动调用应用获取响应，并运行评估器打分；人工标注可在任务详情页的“数据明细”中通过“快速标注”模式完成。

## 限制和注意事项

- **权限与前提**：自动评测要求子账号具备 `管理员` 或 `应用评测-操作` 权限；且目标智能体应用必须已**发布**、**配置知识库**、并加入**应用观测**列表 [原文标题](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)。
- **数量限制**：单次多应用横向评测最多支持 8 个应用；单个评测任务最多添加 10 个评估器；单个评测集单次上传最多 10 个文件（≤20MB/个）。
- **评测集兼容性**：旧版“知识问答”型评测集（.jsonl）仅适配自动评测；新版评测集类型（智能体/工作流/自定义）与旧版格式不直接兼容，迁移需重新创建。
- **计费说明**：LLM评估器调用、自动评测中的模型推理均按实际[Token](../concepts/token.md)消耗计费；Code评估器与人工标注不产生额外费用。预估[Token](../concepts/token.md)消耗为参考值，以实际账单为准。
- **状态与修改**：评测任务创建后，其关联的评测集、应用、评估器配置**不可修改**；如需调整，须新建任务。已发布的评测集支持版本管理，但类型不可变更。

## 来源文档

- [自动评测](../../raw/application-user-guide/application-evaluation/application-auto-evaluation.md)
- [手动评测](../../raw/application-user-guide/application-evaluation/evaluate-manual-application.md)
- [评测集](../../raw/application-user-guide/application-evaluation/application-evaluation-dataset.md)
- [新版应用评测](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation.md)
- [新版评测集](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/new-version-of-evaluation-set.md)
- [评测任务](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/evaluation-task.md)
- [标签管理](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/label-management.md)
- [评估器](../../raw/application-user-guide/application-evaluation/new-version-of-application-evaluation/grader.md)


