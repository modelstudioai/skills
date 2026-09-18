# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可追溯的数据基础设施。它支持训练集（SFT/DPO/CPT）和评测集的创建、版本化管理、清洗增强及自动化回流，覆盖从数据准备到下游任务的全链路。所有数据集均默认启用 OSS 服务端加密（SSE-OSS），存储与处理行为受地域、训练方法和场景约束。

## 支持的模型/功能

- **训练集类型**：支持文本生成、视觉理解、图生视频（首帧）、图生视频（首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：仅支持文本生成场景，不可用于视觉或视频类任务。
- **数据处理能力**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），但暂不支持 SFT-视觉理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持将 SLS 推理日志转化为结构化 JSONL 数据集，可用于训练集（SFT/DPO/CPT）或评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档2明确指出数据处理“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，而文档1称训练集支持“视觉理解、图生视频”等场景——二者存在功能覆盖矛盾。实际可用性以控制台能力为准：**数据清洗/增强仅适用于 SFT-文本生成（ChatML 格式）训练集**，其他类型暂不支持。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长50字符，支持中文、英文、数字、下划线、连字符、点（文档1）或斜杠（文档3） | 创建后不可修改 |
| **数据集类型** | “训练集”或“评测集”，创建后不可变更 | 评测集仅支持文本生成场景 |
| **训练场景 & 方法** | 文本生成/SFT、DPO、CPT 等组合需严格匹配；DPO/CPT 仅限北京地域（文档1） | 日志回流中训练方式由系统动态展示并锁定（文档3） |
| **存储位置** | “平台 OSS 存储”（免费，自动发布）或“云存储挂载”（需额外授权，仅训练集可用） | 评测集不支持 OSS 挂载（文档1、文档3） |
| **导入方式** | 本地上传、OSS 导入、日志回流、API 上传；日志回流单次上限 10 万条（文档1、文档3） | 日志回流时间范围限定为最近 30 天（文档1、文档3） |

## 使用方式

- **创建数据集**：通过控制台 **[数据管理 > 数据集 > 创建数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 进入向导，依次填写名称/描述、选择类型/场景/方法/格式/存储位置/导入方式，并上传数据。提交即发布，无草稿保存机制（历史草稿除外）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：仅支持已发布的 SFT-文本生成训练集。在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** 中创建数据流（含清洗+增强节点），再启动数据流任务。处理完成后自动生成新版本，原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：需先在 **[模型监控](https://bailian.console.aliyun.com/model/telemetry)** 完成审计日志与推理日志的开通及角色授权（文档3）。之后可通过模型监控页、数据管理页等入口配置时间范围、API Key、模型等参数创建回流任务。平台存储模式下导入完成即自动发布 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流（除新加坡外）均仅支持华北2（北京）地域。
- **格式与兼容性**：SFT 文本训练集必须为 ChatML 格式（`messages` 数组）；数据处理不接受非 ChatML 格式输入；评测集导出为 XLSX，训练集导出为 JSONL（文档1）。
- **不可逆操作**：数据集发布后不可编辑；删除操作不可恢复；OSS 挂载数据集不支持“新增版本”，仅能通过“导入数据”页追加（文档1、文档3）。
- **容量与配额**：单次日志回流上限 10 万条（可多次追加）；数据集数量无上限，但单次导入数据量无硬性上限（文档1）；数据增强-通用节点每次最多生成 2000 条样本（文档2）。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费（文档1、文档3）。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


