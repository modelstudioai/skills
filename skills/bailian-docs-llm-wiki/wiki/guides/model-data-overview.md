# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可扩展的数据集基础设施。它支持训练集（SFT/DPO/CPT/视觉/图生视频）和评测集的全生命周期管理，涵盖创建、导入、版本控制、清洗增强及回流等核心能力。所有数据集均默认启用 OSS 服务端加密（SSE-OSS），存储与下游使用遵循地域与权限约束。

## 支持的模型/功能

- **训练集类型**：支持文本生成、视觉理解、图生视频（首帧）、图生视频（首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 与 CPT 仅限北京地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：仅支持文本生成场景，不可用于视觉或图生视频任务。
- **数据处理功能**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），但明确不支持 SFT-图片理解训练集和 DPO 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流功能**：支持将 SLS 推理日志转化为结构化 JSONL 数据集，可用于训练集（SFT/DPO/CPT）或评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 声称“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，而文档 1 中“训练方法与场景”表格未排除 DPO 的数据处理可能性；但文档 2 是唯一明确限定支持范围的权威说明，应以文档 2 为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | “训练集”或“评测集”，创建后不可变更 | 评测集仅支持文本生成场景 |
| **训练场景 & 方法** | 文本生成/SFT、文本生成/DPO、文本生成/CPT 等组合；DPO/CPT 仅北京可用 | 创建后锁定，不可更改 |
| **存储位置** | “平台 OSS 存储”（免费，默认）或“云存储挂载”（需额外授权） | 评测集不支持云存储挂载；OSS 挂载需 Bucket 标签 `bailian-datahub-access=read` [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| **导入方式** | 本地上传、OSS 导入、日志回流、API 上传 | 评测集不支持 OSS 导入；日志回流单次上限 10 万条，仅支持最近 30 天日志 |

## 使用方式

- **创建数据集**：通过控制台 **[数据管理 > 数据集 > 创建数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 完成。需依次填写名称/描述、选择类型/场景/方法/格式/存储位置/导入方式，并按所选方式上传或配置数据源。
- **日志回流专用流程**：需先在 **[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)** 页面完成审计日志与推理日志的**分步开通与角色授权**（顺序不可颠倒），再进入日志回流表单配置时间范围、API Key、模型等筛选条件 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理（清洗/增强）**：仅支持已发布的 SFT-文本生成训练集（ChatML 格式）。需在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** 中创建数据流（含清洗/增强节点），再基于该数据流启动任务，系统将自动生成新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本管理**：所有数据集支持多版本，新增版本需重新导入全部数据（非增量）；历史草稿版本可在线编辑，但新建数据集提交即发布，不再产生草稿。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理功能、日志回流（除新加坡外）均**仅限华北2（北京）地域**；OSS 导入要求 Bucket 与百炼实例同地域。
- **格式强约束**：SFT/DPO/CPT/评测集均有严格数据格式要求（如 ChatML、JSONL），建议下载模板校验；数据处理仅接受 ChatML 格式 SFT 训练集，其他格式将失败。
- **不可逆操作**：数据集发布后不可编辑；删除操作不可恢复；OSS 挂载数据集不支持“新增版本”，仅能通过“导入数据”页追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **用量限制**：日志回流单次上限 10 万条（可多次执行）；数据增强-通用节点单次最多生成 2000 条样本；所有数据集禁止为空。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费，详见百炼计费页面。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


