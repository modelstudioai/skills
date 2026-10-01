# model data [overview](overview.md)

百炼平台的模型数据管理功能为开发者提供从数据集创建、版本管理到清洗增强的全链路支持，覆盖训练集与评测集的生命周期。核心能力包括多格式数据导入、地域受限的数据处理（如清洗/增强）、以及基于日志回流的自动化数据生产。所有操作均通过控制台完成，当前暂不提供数据处理专用 API。

## 支持的模型/功能

- **训练集支持场景**：文本生成、视觉理解、图生视频（首帧/首尾帧）；**评测集仅支持文本生成** [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)  
- **训练方法支持**：SFT（监督微调）、DPO（直接偏好优化）、CPT（持续预训练），其中 DPO/CPT 仅限华北2（北京）地域 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)  
- **数据处理功能**：仅支持 SFT-文本生成训练集（ChatML 格式），**不支持 SFT-图片理解、DPO-文本生成等其他类型** [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)  
- **日志回流支持**：可生成训练集（SFT/DPO/CPT）或评测集（文本生成），但仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)  

> **注意**：文档1称数据处理“仅适用于华北2（北京）地域”，而文档3明确日志回流在“华北2（北京）和新加坡”均可用。此处存在地域支持范围不一致，实际使用请以控制台可用 Region 为准。

## 关键参数

- **数据集元信息**：名称（≤50字符，支持中文/英文/数字/下划线/连字符/点）、描述（≤200字符）、类型（训练集/评测集，创建后不可变更）  
- **训练配置**：训练场景、训练方法（SFT/DPO/CPT）、数据格式（Jsonl/Excel）、存储位置（平台 OSS 存储/OSS 挂载）  
- **数据处理节点参数**：
  - `dataSetCount`：系统自动生成，表示当前节点输出的 messages 数量，不可修改  
  - `对话文本`：开始节点唯一输入参数，表示待处理的 ChatML 格式训练集  
- **日志回流关键约束**：单次回流上限 10 万条；时间范围限定为最近 30 天；API Key 过滤与模型选择存在联动重置规则 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)  

## 使用方式

- **创建数据集**：在[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data) > 数据集页点击「创建数据集」，按向导填写元信息、选择训练场景/方法、指定导入方式（本地上传/OSS 导入/日志回流/API 上传）并上传数据 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)  
- **数据清洗与增强**：需先创建数据流（含开始→数据清洗→数据增强→结束节点），再基于该数据流创建数据流任务，选择目标训练集执行 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)  
- **日志回流**：在模型监控页或数据管理页选择「日志回流」入口，完成审计日志+推理日志授权后，配置时间范围、API Key、模型等参数提交任务 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)  
- **版本管理**：所有数据集支持多版本，新增版本需重新导入全部数据（无增量继承模式）；历史草稿版本可用于数据处理 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)  

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗与增强功能仅限华北2（北京）；日志回流扩展支持新加坡 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)  
- **格式强约束**：数据处理仅接受 SFT-文本生成训练集的 ChatML 格式（`.jsonl`），其他格式（如 DPO、图片理解）将被拒绝 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)  
- **API 缺失**：数据处理暂无可用 API，必须通过控制台操作；模型调优 API 仅支持通过 `training_file_ids` 引用已发布训练集 ID [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)  
- **不可逆操作**：数据集发布后不可编辑；删除操作不可恢复；OSS 挂载数据集不支持「新增版本」，只能通过「导入数据」页追加 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)  
- **敏感内容警告**：法律文件、医学记录、文学作品、方言汇总、用户评论、技术手册等数据**不建议**进行自动清洗或增强，可能破坏语义完整性 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)

## 来源文档

- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


