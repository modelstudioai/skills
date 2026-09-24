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
| 训练方法 | 仅训练集需选 | 是 | `SFT`（全站点）、`DPO` / `CPT`（仅北京） |
| 数据格式 | 导入文件格式 | 是 | `Jsonl 格式` / `Excel 格式` |
| 存储位置 | 影响计费与权限 | 是 | `平台 OSS 存储`（免费，自动发布） / `云存储挂载`（需 OSS 标签 `bailian-datahub-access=read`，仅训练集可用） |
| 导入方式 | 决定前置条件 | 是 | `本地上传`（无依赖）、`从 OSS 导入`（需 Bucket 标签）、`日志回流`（需 SLS 授权）、`API 上传` |

- **日志回流特有参数**：时间范围（最近 30 天）、API Key 过滤（全部/其他/指定）、模型选择（最多 10 个）、OSS 数据路径（仅挂载模式）——修改时间范围会联动重置 API Key 和模型选择 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)，点击**创建数据集**，按向导填写参数并选择导入方式。
2. **导入数据**：
   - *本地上传*：直接拖拽或选择文件，SFT/DPO 文本生成支持多文件；
   - *OSS 导入*：目标 Bucket 需添加标签 `bailian-datahub-access=read`，评测集不支持；
   - *日志回流*：需先完成 SLS 审计日志+推理日志授权（顺序不可逆），再配置时间、API Key、模型等筛选条件 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
   - *API 上传*：通过 `training_file_ids` 引用已发布数据集 ID，详见[模型调优 API 指南](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)。
3. **数据处理（可选）**：仅适用于已发布的 SFT-文本生成训练集（ChatML 格式），在 [数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow) 中创建清洗/增强任务，输出为新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
4. **下游使用**：发布后的训练集用于[模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/model-training-overview.md)，评测集用于[模型评测](raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理、日志回流（除新加坡外）均仅在北京地域可用；OSS 挂载存储也仅限北京 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **不可变性**：数据集类型、训练场景、训练方法、存储位置、数据格式创建后均不可修改；发布操作不可逆，已发布版本不可编辑 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **容量与配额**：
  - 单次日志回流上限 10 万条（可多次追加至不同版本）；
  - 数据集数量无上限，但单次导入数据量无硬性上限（平台 OSS 存储）；
  - 数据处理节点中，“数据增强-通用”每次最多生成 2000 条样本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **格式强约束**：SFT/DPO/CPT/评测集均有严格数据格式要求（如 ChatML），建议下载模板校验；非标准格式导入将失败 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **安全与合规**：所有导入数据默认启用 OSS 服务端加密（SSE-OSS）；敏感信息打码等清洗操作需人工验证结果完整性，避免误删关键字段 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


