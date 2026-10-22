# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/视觉理解/图生视频）和评测集的创建、导入、版本管理及后处理。所有数据集均默认启用 OSS 服务端加密（SSE-OSS），存储与下游调用遵循地域与权限约束。核心能力聚焦于结构化数据准备与质量增强，而非原始日志或非结构化文件托管。

## 支持的模型/功能

- **训练集类型**：支持文本生成、视觉理解、图生视频（首帧）、图生视频（首尾帧）四类训练场景；其中 SFT、DPO、CPT 仅限文本生成场景（DPO/CPT 还需北京地域支持）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **评测集类型**：仅支持文本生成场景，不可用于视觉或视频任务。  
- **数据处理功能**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），暂不支持 SFT-视觉理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流**：可将 SLS 推理日志转化为结构化 JSONL 数据集，支持训练集（SFT/DPO/CPT）和评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  

> **注意**：文档 2 明确声明“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，但文档 1 表格中“支持的训练方法与场景”未排除 DPO 文本生成用于数据处理。此处以文档 2 的明确限制为准——DPO 训练集**不可用于数据清洗或增强**。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | `训练集` 或 `评测集` | 创建后不可变更；评测集仅支持文本生成场景 |
| **训练场景** | 文本生成 / 视觉理解 / 图生视频（首帧） / 图生视频（首尾帧） | 仅训练集需选择；视觉/视频类无官方推荐数据量 |
| **训练方法** | SFT（全部站点）、DPO（仅北京）、CPT（仅北京） | 创建后锁定；CPT 要求 ≥5000 万 [Token](../concepts/token.md) |
| **存储位置** | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 授权，仅训练集可用） | 评测集不支持云存储挂载；OSS 挂载需额外授权角色 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| **导入方式** | 本地上传 / 从 OSS 导入 / 日志回流 / API 上传 | 评测集不支持 OSS 导入；日志回流单次上限 10 万条，可多次追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |

## 使用方式

- **创建数据集**：在控制台 **[数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 页面点击“创建数据集”，按向导填写名称、类型、场景、方法、格式、存储位置及导入方式。提交即发布，不再保留草稿（历史草稿仍可编辑）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **日志回流**：需先在 **[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)** 完成审计日志 + 推理日志双授权，并开通 SLS；再通过模型监控页、详情页或数据管理页入口配置时间范围、API Key、模型等参数创建任务 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **数据处理（清洗/增强）**：仅支持已发布的 SFT-文本生成训练集（ChatML 格式）。在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** 中创建数据流（含清洗/增强节点），再启动数据流任务，系统自动生成新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **版本管理**：所有数据集支持多版本，新增版本需重新导入全部数据（无增量继承模式）；日志回流支持通过“导入数据”页或“新增版本”弹窗追加（OSS 挂载数据集仅支持前者）[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流（除新加坡外）均**仅限华北2（北京）**；OSS 挂载存储要求 Bucket 与百炼 Region 一致。  
- **格式强约束**：SFT/DPO/CPT/评测集均有严格 JSONL 或 Excel 模板要求，建议下载模板填写；数据处理**仅接受 ChatML 格式 SFT 文本训练集**，其他格式（如纯 Prompt-Completion）或非文本训练集均不支持 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **不可逆操作**：数据集发布后不可编辑；删除操作不可恢复；OSS 挂载数据集不支持“新增版本”，仅能通过“导入数据”页追加 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务分别产生独立费用，需查阅百炼计费页面确认 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **数据量边界**：SFT 建议 ≥1000 条，DPO ≥100 条，CPT ≥5000 万 [Token](../concepts/token.md)；日志回流单次 ≤10 万条，但可通过多批次累积；数据增强-通用节点单次最多生成 2000 条样本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


