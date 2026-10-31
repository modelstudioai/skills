# model data overview

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可扩展的数据集基础设施。它支持训练集（SFT/DPO/CPT）和评测集的全生命周期管理，涵盖创建、导入、版本控制、清洗增强及日志回流等核心能力。所有数据集均默认启用 OSS 服务端加密（SSE-OSS），存储与下游使用遵循地域与权限约束。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧/首尾帧）四类训练场景；训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 和 CPT 仅限北京地域可用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，可用于模型泛化能力评估 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：支持对已发布的 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），暂不支持 SFT-视觉理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持将 SLS 推理日志自动转化为结构化 JSONL 数据集，适用于训练集（SFT/DPO/CPT）和评测集（文本生成），当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 1 称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档 3 明确日志回流在**北京和新加坡**均支持 DPO/CPT 训练集创建。此处以文档 3 的最新地域支持范围为准，即 DPO/CPT 训练集的日志回流能力已扩展至新加坡。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值范围/约束 |
|------|------|----------|----------------|
| 数据集名称 | 全局唯一标识符 | 是 | ≤50 字符；支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3）；创建后不可修改 |
| 数据集类型 | 决定用途与后续操作权限 | 是 | `训练集` 或 `评测集`；创建后不可变更 |
| 训练场景 | 限定模型输入输出模态 | 是 | 文本生成 / 视觉理解 / 图生视频（首帧）/ 图生视频（首尾帧）；评测集仅允许文本生成 |
| 训练方法 | 仅训练集需指定 | 是 | `SFT`（全站点）、`DPO`（北京/新加坡）、`CPT`（北京/新加坡） |
| 数据格式 | 文件解析标准 | 是 | `Jsonl 格式` 或 `Excel 格式`；数据处理仅接受 ChatML 格式的 Jsonl [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) |
| 存储位置 | 数据物理存放方式 | 是 | `平台 OSS 存储`（免费，默认）或 `云存储挂载`（需 OSS 标签授权，仅训练集可用）；评测集不支持挂载 |
| 导入方式 | 数据来源通道 | 是 | `本地上传`（通用）、`从 OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`，训练集专用）、`日志回流`（需 SLS 授权，支持训练集/评测集）、`API 上传`（编程集成） |

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)，点击「创建数据集」，按向导填写上述关键参数并选择导入方式。
2. **导入数据**：
   - 本地上传：直接拖拽或选择文件（SFT/DPO 支持多文件）；
   - OSS 导入：目标 Bucket 需预先添加标签 `bailian-datahub-access=read`；
   - 日志回流：需先完成 SLS 审计日志与推理日志的开通及角色授权 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
   - API 上传：通过 `training_file_ids` 引用已发布数据集 ID，详见[模型调优 API 指南](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
3. **版本管理**：数据集发布后，可通过「新增版本」创建全新数据快照；历史草稿版本支持在线编辑，但已发布版本不可编辑。
4. **数据处理（可选）**：仅对 SFT-文本生成训练集有效，在 [数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow) 中搭建清洗/增强工作流，任务完成后自动生成新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练方法、云存储挂载、数据处理功能均仅限华北2（北京）；日志回流额外支持新加坡 Region。
- **格式与兼容性**：
  - 数据处理仅支持 ChatML 格式的 SFT-文本生成训练集，不支持 DPO、CPT、视觉理解等类型 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - 评测集不支持 OSS 导入和 OSS 挂载 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **容量与配额**：
  - 单次日志回流上限为 10 万条，但可通过多次回流至不同版本突破总量限制 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
  - 数据集创建数量无限制，导入数据量无上限（平台 OSS 存储）。
- **操作不可逆**：
  - 发布后的数据集版本不可编辑、不可删除；
  - 删除整个数据集将永久移除其所有版本，无法恢复；
  - 日志回流任务执行中不可手动终止。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


