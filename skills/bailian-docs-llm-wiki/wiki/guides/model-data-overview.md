# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/视觉理解/图生视频）和评测集的创建、导入、版本管理及后处理。所有数据集均支持结构化存储、OSS 加密保护，并可直接对接下游调优与评测任务。数据质量直接影响模型效果，建议在调优前通过清洗与增强提升数据集质量。

## 支持的模型/功能

- **训练集类型**：支持文本生成、视觉理解、图生视频（首帧）、图生视频（首尾帧）四类训练场景；其中 SFT、DPO、CPT 仅适用于文本生成场景，视觉与图生视频暂不支持 DPO/CPT [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集类型**：仅支持文本生成场景，不可用于视觉或视频类任务。
- **数据处理能力**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行数据清洗（如敏感信息打码、特殊内容移除）和数据增强（通用/分类/抽取/创作等场景），但**暂不支持 SFT-视觉理解训练集和 DPO 训练集** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流能力**：支持将 SLS 推理日志转化为结构化 JSONL 数据集，可用于训练集（SFT/DPO/CPT）或评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，而文档 1 表述为“训练集支持4种训练场景”且未排除 DPO 的数据处理能力。以文档 2 的限定为准，DPO 训练集不可用于数据清洗或增强。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值范围/约束 |
|------|------|----------|----------------|
| 数据集名称 | 全局唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） |
| 数据集类型 | 决定用途与后续操作权限 | 是 | `训练集` 或 `评测集`，**创建后不可变更** |
| 训练场景 | 指定模型输入输出模态 | 是 | `文本生成` / `视觉理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集仅允许 `文本生成` |
| 训练方法 | 仅训练集需指定 | 是 | `SFT`（全地域）、`DPO`（仅北京）、`CPT`（仅北京） |
| 数据格式 | 文件解析标准 | 是 | `Jsonl 格式` 或 `Excel 格式`；数据处理仅接受 ChatML 格式的 Jsonl [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) |
| 存储位置 | 影响计费与管理方式 | 是 | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 标签授权，仅训练集可用，评测集禁用） |
| 导入方式 | 决定数据来源与前置条件 | 是 | `本地上传`（无依赖）、`从 OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`）、`日志回流`（需 SLS 授权）、`API 上传` |

## 使用方式

- **创建数据集**：在控制台 **[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)** > **数据集** 页面点击「创建数据集」，按向导完成参数配置与数据导入。提交即发布，**不再生成草稿版本**（历史草稿仍可编辑）。
- **数据处理（清洗/增强）**：仅限已发布的 SFT-文本生成训练集。访问 **[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** > **数据流** 页签，创建数据流并启动任务。处理结果将自动生成新版本（如 V1 → V2），**不覆盖原版本** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：需先在 **[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)** 完成审计日志与推理日志的开通及角色授权（文档 3）。授权后可通过模型监控页、模型详情页或数据管理页入口创建回流任务，支持按时间范围、API Key、模型等多维筛选。
- **追加数据**：已有数据集可通过「新增版本」（平台存储）或「导入数据」页（所有存储类型）追加日志回流数据；**OSS 挂载数据集不支持「新增版本」**，必须使用「导入数据」页 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理功能、日志回流（除新加坡外）均**仅限华北2（北京）地域**；OSS 导入、云存储挂载也仅支持北京地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **不可逆操作**：数据集发布后不可编辑；删除操作不可恢复；删除整个数据集将移除其所有版本，请谨慎执行。
- **数据量约束**：
  - 日志回流单次上限 10 万条（可多次回流累积）；
  - 数据增强-通用节点单次最多生成 2000 条样本；
  - CPT 推荐数据量 ≥5000 万 [Token](../concepts/token.md)，SFT 建议 ≥1000 条，DPO 建议 ≥100 条。
- **格式强约束**：数据处理仅接受 ChatML 格式的 SFT 文本训练集；视觉/图生视频训练集暂无官方推荐数据量，需自行保障样本充分性。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费，详见百炼计费文档。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


