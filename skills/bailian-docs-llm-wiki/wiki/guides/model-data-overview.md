# model data overview

百炼平台的模型数据体系围绕训练集与评测集构建，提供从数据采集（如日志回流）、质量治理（清洗与增强）到版本管理的全链路能力。所有数据操作均基于结构化 JSONL 格式，支持 SFT、DPO、CPT 等主流训练范式，并严格遵循地域与格式约束。开发者需根据下游任务目标选择合适的数据类型、场景和处理路径。

## 支持的模型/功能

- **数据来源功能**：  
  - **日志回流**：将 SLS 推理日志自动转化为结构化训练集或评测集，支持 SFT/DPO/CPT 训练方式及文本生成评测场景，目前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
  - **数据处理**：提供可视化数据流编排能力，支持对 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）和增强（如 Few-Shot 生成），暂不支持 SFT-图片理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **数据集类型与场景**：  
  - 训练集支持 4 种训练场景：文本生成、视觉理解、图生视频（首帧）、图生视频（首尾帧）；评测集仅支持文本生成场景 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
  > **注意**：文档 1 明确声明“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，而文档 3 和文档 2 均指出日志回流支持 DPO 训练集。该矛盾表明文档 1 的描述已过时，实际 DPO 训练集可通过日志回流创建，但不可用于数据处理节点。

## 关键参数

| 参数类别 | 参数名 | 说明 | 约束 |
|----------|--------|------|------|
| **通用** | 数据集名称 | 最长 50 字符，支持中文/英文/数字/下划线/连字符/点 | 创建后不可修改 |
| | 数据集描述 | 最长 200 字符 | 可选 |
| **日志回流专用** | 时间范围 | 最近 30 天（含当天），精确到秒 | 修改后重置 API Key 与模型选择 |
| | 单次回流上限 | 10 万条日志 | 超出部分不回流，但可多次追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| | API Key 过滤 | 支持「全部」「其他」或指定 Key（多选） | 「其他」包含已删除 Key 或跨工作空间日志 |
| **数据处理专用** | `dataSetCount` | 数据清洗/增强节点输出的 messages 数量，系统自动生成且不可更改 | 用于条件判断节点分支逻辑 |
| | 生成样本数（增强） | 每次数据增强任务最多生成 2000 条新样本 | 增强后数据自动附加 `foreignKey` 字段，不影响训练 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) |

## 使用方式

- **控制台操作为主**：  
  - 所有数据集创建、日志回流配置、数据流搭建均通过 [数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data) 控制台完成。  
  - 日志回流需先在[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)页面完成审计日志与推理日志的授权和开启（必须按序：先审计、再推理）[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **数据流编排流程**（数据清洗/增强）：  
  1. 在数据流画布中拖入「开始」→「数据清洗」→「数据增强」→「结束」节点；  
  2. 为清洗节点启用所需算子（如敏感信息打码），为增强节点选择场景（如「数据增强-通用」）并配置 `生成样本数`；  
  3. 发布数据流后，在「任务列表」中创建任务，选择目标训练集（SFT-文本生成，ChatML 格式）启动处理 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **版本管理**：  
  - 每次数据处理、日志回流或导入均生成独立新版本（如 V1 → V2），不覆盖原数据；  
  - 仅历史创建的草稿版本支持在线编辑；已发布版本仅可通过「新增版本」重新导入全部数据 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：  
  - 数据处理功能仅适用于华北2（北京）地域 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；  
  - 日志回流仅在华北2（北京）和新加坡可用，DPO/CPT 训练方法及云存储挂载也仅限北京地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **格式与兼容性**：  
  - 数据处理仅接受 SFT-文本生成训练集（ChatML 格式），不支持 Excel、JSONL 非 ChatML 结构或其他训练方式输入；  
  - 日志回流产出为标准 JSONL，可直接用于训练或后续数据处理，但评测集不支持 OSS 挂载 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **API 与自动化**：  
  - 数据处理暂不提供可用 API，仅支持控制台操作 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；  
  - 数据集可通过 API 引用（`training_file_ids`），但 CRUD 操作当前仅限控制台 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **费用与安全**：  
  - 数据管理功能免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务分别计费；  
  - 所有导入数据默认启用 OSS 服务端加密（SSE-OSS，AES256）。

## 来源文档

- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)


