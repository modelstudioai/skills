# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型调优与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT）、评测集的创建、导入、版本管理及后处理。所有数据集均需在业务空间内显式创建并发布，支持多地域（部分能力限北京）和多种数据源接入，是模型迭代闭环的关键基础设施。

## 支持的模型/功能

- **数据集类型**：明确区分**训练集**（用于[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)）和**评测集**（用于[模型评测](raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)），创建后类型不可变更 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **训练场景与方法**：
  - 训练集支持文本生成、视觉理解、图生视频（首帧/首尾帧）四类场景；评测集**仅支持文本生成**。
  - 训练方法包括 SFT（全地域可用）、DPO 和 CPT（二者**仅限北京地域**）。
- **高级功能**：
  - **日志回流**：将 SLS 推理日志自动转化为结构化训练/评测数据集，支持北京与新加坡 Region [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
  - **数据处理**：支持对 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码）与增强（如 Few-Shot 生成），**当前仅限北京地域**，且不支持 DPO 或视觉类训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 2 明确指出数据处理“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，而文档 1 中“训练集支持4种训练场景”未排除其数据处理适用性，此处以文档 2 的限定为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | `训练集` 或 `评测集` | 创建后不可变更 |
| **训练场景** | 文本生成 / 视觉理解 / 图生视频（首帧） / 图生视频（首尾帧） | 评测集仅允许“文本生成” |
| **训练方法** | SFT / DPO / CPT | 仅训练集显示；DPO/CPT 限北京 |
| **数据格式** | `Jsonl 格式` 或 `Excel 格式` | 模板需严格匹配对应场景 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| **存储位置** | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 授权，评测集不支持） | 创建后不可更改；OSS 挂载需添加 Bucket 标签 `bailian-datahub-access=read` |
| **导入方式** | 本地上传 / 从 OSS 导入 / 日志回流 / API 上传 | 评测集不支持 OSS 导入；日志回流单次上限 10 万条，仅支持最近 30 天日志 |

## 使用方式

- **创建流程**：在控制台 **[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)** > **数据集** 页面点击 **创建数据集**，依次填写名称、类型、场景、方法、格式、存储位置及导入方式 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流专用路径**：可通过 **模型监控列表页**、**模型监控详情页** 或 **数据管理新建页** 三个入口进入配置表单，需先完成审计日志与推理日志的授权开通 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：仅支持已发布的 SFT-文本生成训练集（ChatML 格式）。需在 **数据管理 > 数据流** 页签创建数据流任务，选择预置模板或自定义节点（如“数据清洗→数据增强”），处理结果将生成独立新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **API 集成**：支持通过 API 上传数据文件（详见[调优 API 指南](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)），但数据处理功能**暂无可用 API**（文档 2 明确声明）。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、日志回流（北京/新加坡）、数据处理功能均**仅限北京地域**（文档 1 与文档 2 均强调“重要：本文档仅适用于华北2（北京）地域”）；文档 3 补充日志回流亦支持新加坡。
- **不可逆操作**：数据集发布后不可编辑；删除操作不可恢复；版本管理采用**新建模式**（非增量继承），每次新增版本需重新导入全部数据 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式与兼容性**：
  - 数据处理仅接受 ChatML 格式的 SFT-文本生成训练集，不支持 Excel、DPO 或视觉类数据 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
  - 日志回流产出 JSONL 格式结构化数据，可直接用于调优或评测，也支持后续数据清洗 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **容量与配额**：
  - 单次日志回流上限 10 万条（可多次追加至不同版本）；OSS 导入无数据量上限；平台存储无数据量上限。
  - 数据集名称/描述长度、字符集等约束详见各参数说明。
- **计费提示**：数据管理功能本身免费，但存储（平台 OSS 或自有 OSS）、SLS 日志服务、模型调用等下游资源按各自产品计费。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


