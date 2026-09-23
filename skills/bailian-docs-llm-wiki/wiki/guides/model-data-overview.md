# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可复用的数据集基础设施。它支持训练集（SFT/DPO/CPT/视觉/图生视频）和评测集的全生命周期管理，涵盖创建、导入、版本控制、清洗增强及日志回流等能力。所有数据集均默认启用 OSS 服务端加密（SSE-OSS），并严格遵循地域与场景约束。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧）、图生视频（首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练）。  
- **评测集**：仅支持文本生成场景，用于模型泛化能力评估。  
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式）的数据清洗与增强，不支持 SFT-视觉理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流**：支持将 SLS 推理日志转化为结构化训练集（SFT/DPO/CPT）或评测集（文本生成），目前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
> **注意**：文档 2 明确声明“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，而文档 1 表述为“数据集分为训练集（支持 SFT/DPO/CPT）和评测集”，未限定处理能力。此处以文档 2 的明确限制为准。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | `训练集` 或 `评测集` | 创建后不可变更 |
| **训练场景** | 文本生成 / 视觉理解 / 图生视频（首帧）/ 图生视频（首尾帧） | 评测集仅允许文本生成 |
| **训练方法** | SFT / DPO / CPT | DPO/CPT 仅限北京地域；评测集不适用 |
| **存储位置** | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 授权，仅训练集可用） | 评测集不支持云存储挂载；创建后不可更改 |
| **导入方式** | 本地上传 / 从 OSS 导入 / 日志回流 / API 上传 | 评测集不支持 OSS 导入；日志回流单次上限 10 万条 |

## 使用方式

- **创建数据集**：在 [数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data) > 数据集列表页点击「创建数据集」，按向导填写名称、类型、场景、方法、格式、存储位置及导入方式。提交即发布，无草稿模式（历史草稿仍可编辑）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **日志回流**：需先在[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)完成审计日志与推理日志的授权及开通，再通过模型监控页、数据管理页或详情页入口配置时间范围、API Key、模型等参数。OSS 挂载需额外授权两个服务角色 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **数据处理**：仅支持已发布的 SFT-文本生成训练集。在数据管理 > 数据流页签创建数据流（含清洗/增强节点），再通过任务列表选择目标训练集启动任务。处理结果自动生成新版本，不覆盖原数据 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理、日志回流（除新加坡外）均仅限华北2（北京）地域。  
- **格式与兼容性**：SFT 文本训练集必须为 ChatML 格式 JSONL；视觉/图生视频训练集暂无官方推荐数据量；评测集导出为 XLSX，训练集导出为 JSONL 或 ZIP（依场景而定）。  
- **版本管理**：新增版本采用「新建模式」，需重新导入全部数据；不支持基于上一版本的增量修改。OSS 挂载数据集不支持「新增版本」操作，须通过「导入数据」页追加 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。  
- **不可逆操作**：发布与删除操作均不可逆；已发布版本不可编辑；仅历史草稿版本可删除。  
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费。  
> **注意**：文档 1 称“数据集创建数量无限制，导入数据量无上限”，但文档 3 明确“日志回流单次上限 10 万条”，且文档 2 注明“数据增强-通用任务每次最多生成 2000 条样本”。此处“无上限”指平台侧无硬性配额，实际受单次操作限制、地域可用性及下游服务容量约束。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


