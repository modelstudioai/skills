# model data overview

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可扩展的数据集基础设施。它支持训练集（SFT/DPO/CPT）和评测集的全生命周期管理，涵盖创建、导入、版本控制、清洗增强及日志回流等核心能力。所有数据集均默认启用 OSS 服务端加密（SSE-OSS），存储与下游资源费用独立计费。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧）、图生视频（首尾帧）四类训练场景；训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 和 CPT 仅限北京地域使用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，可用于模型泛化能力评估 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：支持对已发布的 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）和增强（如 Few-Shot 生成），暂不支持 SFT-视觉理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持将 SLS 推理日志自动转化为结构化 JSONL 数据集，适用于训练集（SFT/DPO/CPT）和评测集（文本生成），当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 1 称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档 3 明确日志回流在**北京和新加坡**均支持 DPO/CPT 训练集创建。此处以文档 3 的最新地域支持范围为准，即 DPO/CPT 训练集的日志回流能力已扩展至新加坡。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值约束 |
|------|------|----------|-----------|
| 数据集名称 | 全局唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3）；建议按 `功能_模型_时间` 命名 |
| 数据集类型 | 决定用途与后续操作权限 | 是 | `训练集` 或 `评测集`，**创建后不可变更** |
| 训练场景 | 限定模型输入输出模态 | 是 | `文本生成` / `视觉理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集仅允许 `文本生成` |
| 训练方法 | 仅训练集需指定 | 是 | `SFT`（全站点）、`DPO`（北京/新加坡）、`CPT`（北京/新加坡） |
| 数据格式 | 文件解析标准 | 是 | `Jsonl 格式` 或 `Excel 格式`；数据处理仅接受 ChatML 格式 Jsonl [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) |
| 存储位置 | 影响权限模型与操作能力 | 是 | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 授权，评测集禁用，不自动发布） |
| 导入方式 | 决定前置条件与适用规模 | 是 | `本地上传`（无依赖）、`从 OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`）、`日志回流`（需 SLS 授权）、`API 上传` |

## 使用方式

- **创建数据集**：通过控制台 **[数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 页面进入创建流程，严格按顺序填写参数（如修改时间范围会重置 API Key 选择）[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：仅支持对历史草稿版或已发布版的 SFT-文本生成训练集操作。需先在 **数据管理 > 数据流** 创建清洗/增强数据流，再通过 **任务列表** 启动数据流任务，处理结果将自动生成新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：入口包括模型监控页顶部按钮、模型监控详情页时间选择器旁按钮、或数据管理新建数据集时选择“日志回流”导入方式。授权需严格按序完成审计日志→推理日志→（OSS 挂载时）多角色授权 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **下游调用**：已发布数据集可通过 `training_file_ids` 参数在模型调优 API 中直接引用；评测集用于[模型评测](../concepts/model-evaluation.md)任务 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **不可逆操作**：数据集发布后不可编辑；删除操作不可恢复；数据集类型、训练场景、训练方式、存储位置、回流位置等关键字段创建后均不可更改 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **地域与功能限制**：
  - DPO/CPT 训练方法、云存储挂载、数据处理功能均仅限华北2（北京）地域（文档 1 & 2）；
  - 日志回流支持北京和新加坡（文档 3），但数据处理仍仅限北京——这意味着新加坡用户无法对日志回流生成的 DPO 训练集执行清洗增强。
- **数据量约束**：
  - 日志回流单次上限 10 万条（可多次追加至不同版本）；
  - 数据增强-通用节点单次最多生成 2000 条样本；
  - CPT 推荐数据量 ≥5000 万 [Token](../concepts/token.md)，SFT 推荐 ≥1000 条，DPO 推荐 ≥100 条 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式强约束**：SFT/DPO/CPT/评测集均有严格数据格式要求，务必下载对应模板并校验；数据处理仅接受 ChatML 格式 Jsonl，非该格式将失败 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务均产生独立费用，需提前查阅百炼计费文档。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


