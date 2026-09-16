# model data overview

百炼平台的数据管理功能为模型训练与评测提供统一的数据集支持，涵盖训练集（SFT/DPO/CPT/视觉理解/图生视频）和评测集（仅文本生成）两大类型。所有数据集均支持版本管理、多方式导入及安全存储，并可直接用于下游调优与评测任务。数据质量直接影响模型效果，建议结合数据清洗与增强提升训练集质量。

## 支持的模型/功能

- **训练集**：支持四类训练场景：**文本生成**（SFT/DPO/CPT）、**视觉理解**（图/视频→文本）、**图生视频（首帧）**、**图生视频（首尾帧）**；其中 SFT、DPO、CPT 仅在**华北2（北京）地域**可用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：**仅支持文本生成场景**，不支持视觉或视频类评测 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流**：支持将 SLS 推理日志转化为结构化训练集或评测集，当前在**华北2（北京）和新加坡 Region**可用，其他地域不可见 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理（清洗/增强）**：**仅支持 SFT-文本生成训练集（ChatML 格式）**，暂不支持 DPO 训练集、视觉理解训练集或评测集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 2 明确指出数据处理“暂不支持[SFT-图片理解训练集]和[DPO-文本生成训练集]”，但文档 1 表格中“数据处理”列为“已发布数据集（含历史创建的草稿版本）均可用于”，存在范围矛盾。以文档 2 的明确限定为准——数据处理功能当前**仅限 SFT 文本生成训练集**。

## 关键参数

| 参数 | 说明 | 约束 |
|------|------|------|
| **数据集名称** | 最长 50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） | 创建后不可修改 |
| **数据集类型** | 必选：`训练集` 或 `评测集` | 创建后不可变更 |
| **训练场景** | 文本生成 / 视觉理解 / 图生视频（首帧）/ 图生视频（首尾帧） | 评测集仅允许“文本生成” |
| **训练方法** | SFT / DPO / CPT（仅训练集） | DPO/CPT 仅北京地域可用；创建后锁定 |
| **数据格式** | Jsonl 格式 或 Excel 格式 | 模板需严格匹配场景要求 |
| **存储位置** | 平台 OSS 存储（免费） 或 云存储挂载（OSS 挂载） | 评测集不支持 OSS 挂载；挂载需额外授权 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| **导入方式** | 本地上传 / 从 OSS 导入 / 日志回流 / API 上传 | 评测集不支持“从 OSS 导入”；日志回流单次上限 10 万条 |

## 使用方式

- **创建数据集**：在控制台 **[数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data)** 页面点击“创建数据集”，按向导填写参数并选择导入方式。提交即发布，**不再生成草稿版本**（历史草稿仍可编辑） [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流**：需先完成审计日志与推理日志的开通及服务角色授权（AliyunServiceRoleForSFMAccessSLS 等），再通过模型监控页或数据管理页进入表单配置 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理（清洗/增强）**：仅支持已发布的 SFT-文本生成训练集。在 **[数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow)** 中创建数据流（含清洗/增强节点），再启动数据流任务。处理结果自动生成新版本，**不覆盖原数据集** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **API 集成**：模型调优 API（如 `training_file_ids`）可直接引用已发布训练集 ID；但数据处理暂无可用 API [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗/增强、日志回流（除新加坡外）均**仅限华北2（北京）**；OSS 挂载存储也仅在北京可用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据量限制**：
  - 日志回流：单次最多 10 万条，但可多次回流至不同版本，**总量无上限** [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
  - 数据增强：`数据增强-通用`节点每次最多生成 2000 条样本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - 推荐最小数据量：SFT ≥ 1000 条，DPO ≥ 百条，CPT ≥ 5000 万 Token [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **不可逆操作**：发布、删除（含整个数据集及其所有版本）均不可恢复；已发布版本不可编辑，仅历史草稿版本可删 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式强约束**：SFT/DPO/CPT/评测集均有严格 JSONL 或 Excel 模板要求，必须下载对应模板准备数据，否则导入失败 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


