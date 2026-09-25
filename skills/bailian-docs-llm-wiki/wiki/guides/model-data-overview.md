# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型调优与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT）、评测集的创建、导入、版本管理及后处理。所有数据集均需在业务空间内显式创建并发布，支持多地域（部分能力限北京）和多种数据源接入，是模型迭代闭环的关键基础设施。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧/首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 与 CPT 仅在北京地域可用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，可用于模型效果客观评估 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：支持对已发布的 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），暂不支持 DPO、CPT 或视觉类训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：将 SLS 推理日志自动转化为结构化 JSONL 数据集，支持训练集（SFT/DPO/CPT）与评测集两类用途，当前仅在北京和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出数据处理“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，而文档 1 中“数据准备”章节提及“视觉理解和图生视频训练集暂无官方推荐数据量”，二者一致；但文档 1 表格中“训练方法与场景”未明确限制 DPO/CPT 的数据处理兼容性，实际以文档 2 的功能边界为准。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值约束 |
|------|------|----------|----------|
| 数据集名称 | 全局唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） |
| 数据集类型 | 创建后不可变更 | 是 | `训练集` / `评测集` |
| 训练场景 | 仅训练集需选 | 是 | `文本生成` / `视觉理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集固定为文本生成 |
| 训练方法 | 仅训练集需选 | 是 | `SFT`（全站）、`DPO` / `CPT`（仅北京） |
| 数据格式 | 导入文件格式 | 是 | `Jsonl 格式` 或 `Excel 格式` |
| 存储位置 | 影响计费与操作权限 | 是 | `平台 OSS 存储`（免费，支持新增版本）或 `云存储挂载`（OSS 挂载，需额外授权，评测集不支持，且不支持新增版本） |
| 导入方式 | 决定前置条件与流程 | 是 | `本地上传`（无依赖）、`从 OSS 导入`（Bucket 需标签 `bailian-datahub-access=read`）、`日志回流`（需完成 SLS 审计+推理日志授权）、`API 上传` |

## 使用方式

1. **创建数据集**：进入 [数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data) > **数据集** > **创建数据集**，按向导填写上述关键参数，并选择导入方式上传数据。提交即发布，不再保留草稿状态（历史草稿仍可编辑）。
2. **日志回流专用流程**：需先在 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) 完成审计日志与推理日志的**分步开通与角色授权**（顺序不可逆），再通过任一入口（监控页、详情页、数据管理页）配置时间范围、API Key、模型等筛选条件创建任务 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
3. **数据处理**：仅适用于已发布的 SFT-文本生成训练集（ChatML 格式）。在数据管理 > **数据流** 页签，通过画布搭建含“数据清洗”和/或“数据增强”节点的工作流，再基于该数据流创建任务，指定目标训练集触发处理。处理结果自动生成新版本，原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
4. **版本管理**：所有数据集支持多版本。新增版本需重新导入全部数据（非增量），平台存储数据集支持“新增版本”按钮；OSS 挂载数据集仅能通过“导入数据”页追加 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理功能、日志回流（除新加坡外）均仅在北京（华北2）地域可用；OSS 挂载存储要求 Bucket 与百炼服务同 Region。
- **数据量限制**：
  - 日志回流单次上限 10 万条（可多次回流累积）；
  - 数据增强-通用节点单次最多生成 2000 条样本；
  - 评测集不支持从 OSS 导入；
  - 不支持创建或发布空数据集。
- **格式与兼容性**：
  - 数据处理严格限定输入为 SFT-文本生成训练集的 ChatML 格式（`.jsonl`），其他类型（如 DPO、视觉类）无法使用 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - 所有导入数据自动启用 OSS 服务端加密（SSE-OSS）；
  - 训练集/评测集创建后，类型、场景、训练方法、存储位置均不可变更。
- **操作风险**：
  - 发布与删除操作**不可逆**，已发布版本不可编辑，仅历史草稿版本可删除；
  - OSS 挂载数据集不支持“新增版本”，误删需重建；
  - 日志回流任务执行中不可手动终止，失败需提工单排查。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志读写等下游资源按各自产品计费。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


