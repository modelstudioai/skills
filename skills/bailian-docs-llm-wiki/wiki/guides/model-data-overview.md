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
| 训练场景 | 限定模型输入输出模态 | 是 | 文本生成 / 视觉理解 / 图生视频（首帧）/ 图生视频（首尾帧）；评测集仅允许文本生成 |
| 训练方法 | 仅训练集可见 | 是 | `SFT`（全站点）、`DPO`（北京）、`CPT`（北京） |
| 存储位置 | 影响计费与操作权限 | 是 | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 授权，仅训练集可用，评测集禁用） |
| 导入方式 | 决定前置条件与适用规模 | 是 | `本地上传`（无依赖）、`从 OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`）、`日志回流`（需 SLS 授权）、`API 上传` |

- **日志回流特有参数**：时间范围（最近 30 天）、API Key 过滤（全部/其他/指定）、模型选择（最多 10 个）、OSS 数据路径（仅挂载模式）；修改时间范围会联动重置 API Key 和模型选择 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理特有约束**：仅支持 ChatML 格式的 SFT-文本生成训练集；不提供 API 接口，仅控制台可用 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 使用方式

- **创建数据集**：通过控制台 **[数据管理 > 数据集 > 创建数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 完成，需依次填写名称、类型、场景、方法、格式、存储位置及导入方式。提交即发布，**不再生成草稿版本**（历史草稿仍可编辑） [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流**：入口包括模型监控列表页、模型监控详情页、数据管理新建页；需先完成 SLS 审计日志与推理日志的授权开通（顺序不可逆），再配置筛选条件 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** 页面创建数据流（含清洗/增强节点），再基于该数据流启动任务，目标训练集将自动生成新版本（如 V1 → V2），原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本管理**：所有数据集支持多版本，新增版本需重新导入全部数据（非增量）；仅历史草稿版本可在线编辑，已发布版本不可编辑 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流（除新加坡外）均仅限华北2（北京）可用；OSS 挂载存储也仅限北京 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据量限制**：
  - 日志回流单次上限 10 万条（可多次追加至不同版本）；
  - 数据增强-通用节点单次最多生成 2000 条样本；
  - 评测集不支持 OSS 导入，且仅支持文本生成场景。
- **不可逆操作**：
  - 发布后的数据集版本不可编辑、不可删除；
  - 删除整个数据集将移除其下所有版本，**不可恢复**；
  - 日志回流任务执行中不可手动终止 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式与兼容性**：
  - 数据处理仅接受 ChatML 格式 SFT 训练集，不支持 Excel 或其他 JSONL 变体；
  - 视觉/图生视频训练集暂无官方推荐数据量，需根据场景自行评估；
  - 所有导入数据默认启用 OSS 服务端加密（SSE-OSS）。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志读写等下游资源按各自产品计费，使用前请查阅最新计费文档 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


