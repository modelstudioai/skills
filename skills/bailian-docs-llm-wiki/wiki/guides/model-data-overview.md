# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/视觉/图生视频）和评测集（文本生成）的创建、导入、版本管理、清洗增强及日志回流等核心能力。所有数据集均默认启用 OSS 服务端加密（SSE-OSS），存储与下游调用遵循地域与权限约束。开发者需根据训练目标谨慎选择数据集类型、场景与方法，因关键属性（如类型、训练场景、训练方式）创建后不可变更。

## 支持的模型/功能

- **训练集**：支持四类训练场景：**文本生成**（SFT/DPO/CPT）、**视觉理解**（图/视频→文本）、**图生视频（首帧）**、**图生视频（首尾帧）**；其中 SFT、DPO、CPT 仅在**华北2（北京）地域**可用（DPO/CPT 及云存储挂载不支持其他地域）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：**仅支持文本生成场景**，不支持视觉或图生视频；不支持 OSS 导入与 OSS 挂载存储 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：当前**仅支持 SFT-文本生成训练集（ChatML 格式）**，不支持 SFT-视觉理解、DPO 或 CPT 训练集的数据清洗与增强 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持生成**训练集（SFT/DPO/CPT）和评测集（文本生成）**，但仅在**华北2（北京）和新加坡 Region** 可用；单次回流上限 10 万条，可多次追加至不同版本 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 1 称“DPO/CPT 训练方法、云存储挂载仅支持北京地域”，而文档 3 明确日志回流在**北京和新加坡**均支持 DPO/CPT 训练集创建。此处以文档 3 的最新地域支持范围为准，文档 1 中“仅北京”表述已过时。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值与限制 |
|------|------|----------|------------|
| **数据集名称** | 数据集唯一标识 | 是 | ≤50 字符；支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3）；创建后不可修改 |
| **数据集类型** | 训练集 or 评测集 | 是 | 创建后不可变更；评测集仅支持文本生成场景 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| **训练场景** | 数据适用的建模任务 | 是 | 文本生成 / 视觉理解 / 图生视频（首帧）/ 图生视频（首尾帧）；评测集此项隐藏 |
| **训练方法** | 仅训练集必填 | 是 | SFT（全部站点）、DPO（北京/新加坡）、CPT（北京/新加坡）；创建后锁定 |
| **数据格式** | 文件结构规范 | 是 | Jsonl 格式 或 Excel 格式；SFT/DPO/CPT/评测集均有对应模板，须严格遵循 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md) |
| **存储位置** | 数据物理存放方式 | 是 | 平台 OSS 存储（免费，自动发布）或云存储挂载（需额外授权，仅训练集支持）；评测集禁用挂载 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| **导入方式** | 数据来源路径 | 是 | 本地上传 / 从 OSS 导入 / 日志回流 / API 上传；评测集不支持 OSS 导入 |

## 使用方式

- **创建数据集**：通过控制台 **[数据管理 > 数据集 > 创建数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 进入向导页，按顺序填写上述参数并上传数据；提交即**立即发布**，不再产生草稿版本（历史草稿仍可编辑）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流**：需先在 **[模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry)** 完成审计日志与推理日志的**分步开通与角色授权**（顺序不可逆），再通过任一入口（监控页、详情页、数据管理页）配置时间范围、API Key、模型等参数创建 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理（清洗/增强）**：仅限已发布的 SFT-文本生成训练集，在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** 中搭建数据流（含开始/清洗/增强/结束节点），再创建数据流任务；处理完成后自动生成新版本，**不覆盖原数据集** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **版本管理**：所有数据集支持多版本，通过 **“新增版本”**（平台存储）或 **“导入数据”**（OSS 挂载）追加；新增版本需**重新导入全部数据**，不支持增量修改 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 限制和注意事项

- **不可逆操作**：发布、删除（含整个数据集及其所有版本）均不可恢复；仅历史草稿版本可删除 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **地域强约束**：
  - DPO/CPT 训练、云存储挂载、数据处理功能**仅限华北2（北京）**；
  - 日志回流**支持北京与新加坡**，其他 Region 不显示入口；
  - 文档 2 声明“本文档仅适用于华北2（北京）地域”，但文档 3 已扩展至新加坡，开发者需按实际 Region 选择能力。
- **格式与兼容性**：
  - 数据处理**仅接受 ChatML 格式的 SFT-文本生成训练集**，不支持 Excel、JSONL 其他变体或非 SFT 类型 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - 评测集导出固定为 `.xlsx`，SFT 训练集导出为 `.jsonl`，视觉训练集导出为 `.zip`；
  - 日志回流产出数据为 JSONL 格式，可直接用于调优或评测。
- **用量限制**：
  - 日志回流单次上限 10 万条（可多次追加）；
  - 数据增强-通用节点单次最多生成 2000 条样本；
  - 不支持创建或发布空数据集。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费，使用前请查阅[百炼计费文档](https://help.aliyun.com/zh/bailian/pricing)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


