# model data [overview](../api/overview.md)

百炼平台的模型数据管理功能为大模型调优与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/视觉/图生视频）和评测集（文本生成）的创建、导入、版本管理与处理。所有数据集均以结构化格式存储并加密，支持多方式接入与自动化增强，是模型效果提升的关键基础设施。

## 支持的模型/功能

- **训练集**：支持四类训练场景：**文本生成**（SFT/DPO/CPT）、**视觉理解**（图/视频→文本）、**图生视频（首帧）**、**图生视频（首尾帧）**；其中 DPO 和 CPT 仅限北京地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：**仅支持文本生成场景**，不可用于视觉或视频类任务；不支持 OSS 导入和 OSS 挂载存储 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：仅支持 **SFT-文本生成训练集（ChatML 格式）** 的清洗与增强，暂不支持 SFT-视觉理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持生成训练集（SFT/DPO/CPT）和评测集（文本生成），覆盖北京与新加坡 Region；单次上限 10 万条，可多次追加至不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确限定数据处理“仅适用于华北2（北京）地域”，但文档 3 表明日志回流在新加坡也可用；而文档 1 中“DPO/CPT 仅支持北京地域”与文档 3 中“日志回流支持北京和新加坡的 DPO/CPT 训练集”存在潜在矛盾。实际使用时，请以控制台可用选项为准，北京地域功能最全。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | 必选：`训练集` 或 `评测集` | 创建后不可变更 |
| **训练场景** | 文本生成 / 视觉理解 / 图生视频（首帧）/ 图生视频（首尾帧） | 评测集仅允许“文本生成” |
| **训练方法** | SFT（全部站点）、DPO（北京/新加坡）、CPT（北京/新加坡） | 创建后锁定；DPO/CPT 不支持非北京/新加坡地域的其他训练方式 |
| **数据格式** | `Jsonl 格式` 或 `Excel 格式` | 推荐下载模板校验结构 |
| **存储位置** | `平台 OSS 存储`（免费，默认）或 `云存储挂载`（OSS 挂载） | 评测集不支持 OSS 挂载；OSS 挂载需额外授权角色 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| **导入方式** | 本地上传 / 从 OSS 导入 / 日志回流 / API 上传 | 评测集不支持 OSS 导入；日志回流需先完成 SLS 审计日志+推理日志双授权 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |

## 使用方式

- **创建数据集**：在 [数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data) 页面点击「创建数据集」，按向导填写参数并选择导入方式；提交即发布，无草稿模式（历史草稿仍可编辑）。
- **日志回流**：需先在[模型监控](https://bailian.console.aliyun.com/model/telemetry)完成审计日志与推理日志的**分步授权与开启**（顺序不可逆），再通过任一入口（监控页、数据管理页）配置时间范围、API Key、模型等参数 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：仅支持已发布的 SFT-文本生成训练集（ChatML 格式）。在数据管理 > 数据流页签中，创建含「数据清洗」+「数据增强」节点的数据流任务，系统将自动生成新版本（如 V1 → V2），原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本管理**：所有数据集支持多版本，新增版本需重新导入全部数据（非增量）；仅历史草稿版本可在线编辑，已发布版本不可编辑。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据处理、日志回流均**仅在北京地域完全可用**；日志回流扩展支持新加坡，但部分能力（如数据处理）未明确支持该地域，建议优先使用北京。
- **格式与兼容性**：
  - 数据处理严格要求 SFT-文本生成训练集为 **ChatML 格式**（`.jsonl`），不支持 Excel 或其他格式 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - 视觉/图生视频训练集无官方推荐数据量，需根据场景自行评估；
  - 评测集必须与训练集**数据不重叠**，确保评估客观性 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **容量与配额**：
  - 单次日志回流上限 **10 万条**（非总量限制），可多次追加；
  - 数据集创建数量无限制，导入数据量无上限（平台 OSS 存储）；
  - 数据增强-通用节点单次最多生成 **2000 条样本** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **操作风险**：
  - **发布与删除均不可逆**：已发布版本不可编辑，删除即永久移除所有版本；
  - OSS 挂载数据集**不支持「新增版本」**，追加数据须通过「导入数据」页操作 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
  - 日志回流预估数据量为近似值，实际回流条数可能略有差异，超 10 万时需主动缩小筛选范围。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


