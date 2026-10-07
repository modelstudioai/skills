# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT）、评测集的创建、导入、版本管理及后处理。所有数据集均支持结构化存储与安全加密，是模型调优和效果评估的基础依赖。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧/首尾帧）四类训练场景；训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 与 CPT 仅限北京地域可用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，用于模型泛化能力客观评估，不支持 OSS 导入或 OSS 挂载存储 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：支持对已发布的 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），暂不支持 DPO、CPT 或视觉类训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持将 SLS 推理日志自动转化为结构化 JSONL 数据集，可用于训练集（SFT/DPO/CPT）或评测集，当前仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出数据处理“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，但文档 1 中“数据准备”章节提及“视觉理解和图生视频训练集暂无官方推荐数据量”，二者未冲突；而文档 3 声明日志回流支持训练集的 DPO/CPT 场景，与文档 1 中“DPO/CPT 训练方法……仅支持北京地域”的表述一致，但文档 1 未限定日志回流渠道——因此文档 3 补充了关键适用性信息，属合理扩展，非矛盾。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值示例/约束 |
|------|------|----------|----------------|
| 数据集名称 | 全局唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） |
| 数据集类型 | 创建后不可变更 | 是 | `训练集` / `评测集` |
| 训练场景 | 仅训练集需选 | 是 | `文本生成` / `视觉理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集固定为文本生成 |
| 训练方法 | 仅训练集需选 | 是 | `SFT`（全站点）、`DPO` / `CPT`（仅北京） |
| 数据格式 | 文件解析依据 | 是 | `Jsonl 格式`（推荐）或 `Excel 格式` |
| 存储位置 | 影响计费与权限 | 是 | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 标签 `bailian-datahub-access=read`，仅训练集可用） |
| 导入方式 | 决定前置条件 | 是 | `本地上传`（无依赖）、`从 OSS 导入`（需 Bucket 标签）、`日志回流`（需 SLS 授权）、`API 上传`（需调用 fine-tuning API） |

## 使用方式

- **创建数据集**：通过控制台 **[数据管理 > 数据集 > 创建数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 进入向导页，按顺序填写参数并选择导入方式；提交即发布，不保留草稿（历史草稿仍可编辑）。
- **日志回流专用流程**：需先在 **[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)** 完成审计日志与推理日志的分步授权（必须先审计、后推理），再通过任一入口（监控页顶栏、详情页时间区、数据管理新建页）配置回流参数 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：仅支持已发布的 SFT-文本生成训练集（ChatML 格式），需在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** 中创建数据流任务，清洗与增强节点串联执行，结果自动生成新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **API 集成**：训练集 ID（`training_file_ids`）可通过模型调优 API 引用；日志回流与数据处理暂不提供开放 API [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理、日志回流均仅限华北2（北京）；日志回流额外支持新加坡 Region [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据量限制**：
  - 日志回流单次上限 10 万条（可多次追加至不同版本）；
  - 数据增强-通用节点单次最多生成 2000 条样本；
  - 评测集不支持 OSS 导入，且存储位置不可选 OSS 挂载。
- **格式与兼容性**：
  - 数据处理仅接受 ChatML 格式的 SFT-文本生成训练集，不支持 Excel 或其他格式 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - 所有导入数据自动启用 OSS 服务端加密（SSE-OSS，AES256）；
  - 训练集/评测集创建后，类型、场景、训练方法、存储位置均不可修改。
- **操作风险**：
  - 发布与删除操作不可逆，已发布版本不可编辑；
  - OSS 挂载数据集不支持“新增版本”，追加数据须通过“导入数据”页操作；
  - 日志回流预估数据量为近似值，实际回流条数可能略有差异，超 10 万时系统禁用提交按钮，需缩小筛选范围 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


