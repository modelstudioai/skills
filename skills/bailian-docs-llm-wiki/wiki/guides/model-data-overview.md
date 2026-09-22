# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可复用的数据集基础设施。它支持训练集（SFT/DPO/CPT）和评测集两类数据集的创建、版本管理、清洗增强及日志回流，覆盖文本生成、视觉理解、图生视频等多场景。所有数据集均默认启用 OSS 服务端加密（SSE-OSS），存储与下游使用遵循地域与权限约束。

## 支持的模型/功能

- **训练集**：支持 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）三种训练方法，对应文本生成、视觉理解、图生视频（首帧/首尾帧）四类训练场景；其中 DPO/CPT 仅限北京地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，可用于模型泛化能力评估 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），暂不支持 SFT-视觉理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持将 SLS 推理日志转化为结构化 JSONL 数据集，用于训练集（SFT/DPO/CPT）或评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，但文档 1 表格中“支持的训练场景”一栏未排除视觉理解/DPO 在数据处理中的适用性。以文档 2 的限定为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | “训练集”或“评测集”，创建后不可变更 | 评测集仅支持文本生成场景 |
| **训练场景** | 文本生成 / 视觉理解 / 图生视频（首帧）/ 图生视频（首尾帧） | 仅训练集需填写；视觉理解/图生视频暂无官方推荐数据量 |
| **训练方法** | SFT / DPO / CPT | DPO/CPT 仅北京地域可用；CPT 要求 ≥5000 万 [Token](../concepts/token.md) |
| **数据格式** | Jsonl 格式 或 Excel 格式 | 建议下载模板按规范准备，避免导入失败 |
| **存储位置** | 平台 OSS 存储（免费，无上限）或云存储挂载（需 Bucket 标签 `bailian-datahub-access=read`） | 评测集不支持云存储挂载；OSS 挂载需额外授权角色 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |

## 使用方式

- **创建数据集**：在控制台 **[数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 页面点击“创建数据集”，依次填写名称、类型、场景、方法、格式、存储位置及导入方式（本地上传/OSS 导入/日志回流/API 上传）。
- **日志回流**：需先在 **[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)** 完成审计日志与推理日志的开通及 SLS 角色授权；再通过模型监控页、详情页或数据管理页入口配置时间范围、API Key、模型等参数 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：仅支持已发布的 SFT-文本生成训练集（ChatML 格式）。在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** 中创建数据流（含清洗/增强节点），再启动数据流任务处理指定训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本管理**：同一数据集可创建多个独立版本（自动递增编号），新增版本需重新导入全部数据（非增量）；历史草稿版本支持在线编辑，已发布版本不可编辑。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理功能、日志回流（除新加坡外）均仅限华北2（北京）地域；OSS 导入要求 Bucket 与百炼实例同地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据量限制**：日志回流单次上限 10 万条（可多次追加）；数据增强-通用节点单次最多生成 2000 条样本；SFT 推荐数据量 ≥1000 条，DPO ≥100 条，CPT ≥5000 万 [Token](../concepts/token.md)。
- **不可逆操作**：数据集发布后不可编辑；删除操作不可恢复；OSS 挂载数据集不支持“新增版本”，仅能通过“导入数据”页追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **格式与兼容性**：数据处理仅接受 ChatML 格式的 SFT-文本生成训练集；评测集导出为 XLSX，SFT 训练集导出为 JSONL；视觉理解训练集导出为 ZIP。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


