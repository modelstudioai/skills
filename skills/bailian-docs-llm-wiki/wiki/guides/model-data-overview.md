# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT）、评测集的创建、导入、版本管理及后处理能力。所有数据集均需在业务空间内创建，支持多地域部署但部分功能存在地域限制。数据质量直接影响模型调优效果，建议在训练前通过清洗与增强提升数据规范性与多样性。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧/首尾帧）四类训练场景；训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）；其中 DPO 与 CPT 仅限北京地域可用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，可用于模型泛化能力评估，不支持 OSS 导入与 OSS 挂载存储 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：支持对已发布的 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），暂不支持 DPO、CPT 及视觉类训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：将 SLS 推理日志自动转化为结构化 JSONL 数据集，支持训练集（SFT/DPO/CPT）与评测集两类用途，当前仅在北京与新加坡地域可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，而文档 1 表述为“训练集支持4种训练场景”，未排除 DPO 的数据处理可能性。以文档 2 为准，DPO 训练集不可用于数据清洗或增强。

## 关键参数

| 参数 | 说明 | 必填 | 取值范围/约束 |
|------|------|------|----------------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）；文档 3 允许斜杠，但实际控制台校验以文档 1 为准 |
| 数据集类型 | 决定下游用途 | 是 | `训练集` 或 `评测集`，创建后不可变更 |
| 训练场景 | 场景适配性控制 | 是 | 文本生成 / 视觉理解 / 图生视频（首帧）/ 图生视频（首尾帧）；评测集仅允许文本生成 |
| 训练方法 | 算法路径选择 | 是（训练集） | `SFT`（全地域）、`DPO`/`CPT`（仅北京） |
| 数据格式 | 文件结构要求 | 是 | `Jsonl 格式` 或 `Excel 格式`，推荐下载模板校验格式 |
| 存储位置 | 成本与权限模型 | 是 | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 授权，仅训练集可用） |
| 导入方式 | 数据来源通道 | 是 | `本地上传`（通用）、`从 OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`，仅训练集）、`日志回流`（需 SLS 授权，北京/新加坡）、`API 上传`（编程集成） |

> **注意**：文档 3 中“回流位置”允许选择“OSS 挂载”，且明确评测集禁用该选项；而文档 1 中“存储位置”表格注明“评测集不可用”云存储挂载——二者一致，无矛盾。

## 使用方式

- **创建数据集**：在控制台 **[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)** > **数据集** 页面点击「创建数据集」，按向导完成参数配置与数据导入；提交即发布，不支持草稿保存（历史草稿版本除外）。
- **数据处理**：仅限北京地域，在 **数据管理 > 数据流** 页签中创建数据流任务，选择已发布的 SFT-文本生成训练集作为输入，系统自动生成新版本（如 V1 → V2），原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：需先在 **模型监控 > 开通日志服务** 完成审计日志与推理日志双重授权（顺序不可逆），再通过模型监控页、详情页或数据管理页入口发起回流任务；支持多次追加至同一数据集的不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **API 集成**：训练集 ID 可通过 `training_file_ids` 参数传入模型调优 API；数据集 CRUD 当前仅支持控制台操作，数据处理暂无可用 API [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理、日志回流均仅支持华北2（北京）地域；日志回流额外支持新加坡地域 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据量约束**：
  - 日志回流单次上限 10 万条（可多次追加）；
  - DPO 建议数据量“上百条”，SFT“上千条”，CPT 要求“5000 万 Token”；
  - 数据处理中“数据增强-通用”节点单次最多生成 2000 条样本。
- **格式与兼容性**：
  - 数据处理仅接受 ChatML 格式的 SFT-文本生成训练集，不支持 Excel 或其他格式；
  - 评测集导出固定为 `.xlsx`，SFT 训练集导出为 `.jsonl`，视觉类导出为 `.zip`；
  - 所有导入数据默认启用 OSS 服务端加密（SSE-OSS，AES256）。
- **不可逆操作**：
  - 发布后的数据集版本不可编辑、不可删除；
  - 删除整个数据集将清除其所有版本，不可恢复；
  - 日志回流任务执行中不可手动终止。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志读写等下游资源按各自产品计费。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


