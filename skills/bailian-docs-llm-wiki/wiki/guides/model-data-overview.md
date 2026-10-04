# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT）、评测集的创建、导入、版本管理及后处理。所有数据集均需明确类型与场景，创建后不可变更，且下游任务（如模型调优、评测）严格依赖已发布版本。数据质量直接影响模型效果，建议结合数据清洗与增强提升训练集质量。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧/首尾帧）四类训练场景；训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 与 CPT 仅限北京地域可用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，用于模型泛化能力评估，不支持 OSS 导入或 OSS 挂载存储 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流**：支持将 SLS 推理日志自动转化为结构化训练集或评测集（JSONL 格式），适用于文本生成场景，当前在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式）的数据清洗与增强，不支持 DPO、CPT 或视觉类训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 2 明确指出“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，但文档 1 中“训练方法与场景”表格未排除 DPO 训练集用于数据处理——该处为过时或错误信息，应以文档 2 的限定为准。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值范围/约束 |
|------|------|----------|----------------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3）；建议按 `功能_模型_时间` 命名 |
| 数据集类型 | 决定用途与后续能力 | 是 | `训练集` 或 `评测集`，**创建后不可变更** |
| 训练场景 | 限定模型输入输出模态 | 是 | `文本生成` / `视觉理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集仅允许 `文本生成` |
| 训练方法 | 仅训练集可见 | 是 | `SFT`（全地域）、`DPO` / `CPT`（仅北京） |
| 数据格式 | 文件组织方式 | 是 | `Jsonl 格式` 或 `Excel 格式`；数据处理仅接受 ChatML 格式的 Jsonl [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) |
| 存储位置 | 影响计费与操作权限 | 是 | `平台 OSS 存储`（免费、支持新增版本、自动发布）或 `云存储挂载`（需 OSS 授权、不支持评测集、不支持新增版本） |
| 导入方式 | 决定前置条件与适用规模 | 是 | `本地上传`（无依赖）、`从 OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`）、`日志回流`（需 SLS 授权与日志开通）、`API 上传`（需编程集成） |

## 使用方式

- **创建数据集**：通过控制台 **[数据管理 > 数据集 > 创建数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 完成，需依次填写名称、类型、场景、方法、格式、存储位置及导入方式。提交即发布，**不再生成草稿版本**（历史草稿仍可编辑）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流**：需先在 **[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)** 完成审计日志与推理日志的授权及开通（顺序不可逆），再通过任一入口（监控页、详情页、数据管理页）配置时间范围、API Key、模型等参数创建任务；单次上限 10 万条，支持多次追加至不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：仅限北京地域，在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** 搭建数据流（如清洗→增强），选择 SFT-文本生成训练集启动任务；处理完成后自动生成新版本，**不覆盖原数据集** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本管理**：所有数据集支持多版本，通过 **新增版本**（平台存储）或 **导入数据**（OSS 挂载）追加；每个版本独立存储、独立发布，**不支持增量修改**。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理、日志回流（除新加坡外）均仅限华北2（北京）；OSS 挂载存储也仅限北京 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **不可变性**：数据集类型、训练场景、训练方法、存储位置、数据格式创建后**不可变更**；发布后的版本**不可编辑、不可删除**；仅历史草稿版本可删除 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **容量与数量**：数据集创建数量无限制，单次日志回流上限 10 万条（可多次追加），但单次数据增强任务最多生成 2000 条样本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **格式强约束**：SFT/DPO/CPT/评测集均有严格数据格式要求，推荐下载对应模板并校验；数据处理仅接受 ChatML 格式 Jsonl，非该格式将失败 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **安全与合规**：所有导入数据默认启用 OSS 服务端加密（SSE-OSS）；敏感信息打码等清洗操作需人工确认效果，避免误删关键字段 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志读写等产生实际费用，详见百炼计费页面。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


