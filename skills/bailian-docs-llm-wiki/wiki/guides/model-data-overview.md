# model data overview

百炼平台提供两类核心数据构建能力：一是面向训练集的**数据清洗与增强**，用于提升 SFT 训练数据质量与规模；二是面向推理日志的**日志回流**，将 SLS 中的原始日志结构化为可直接用于微调或评测的 JSONL 数据集。二者均聚焦于模型调优前的数据准备阶段，支持华北2（北京）和新加坡 Region，且均采用版本化管理，不覆盖原始数据。

## 支持的模型/功能

- **数据清洗与增强**：仅支持 [SFT-文本生成训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)，格式严格限定为 ChatML（`.jsonl`），暂不支持 SFT-图片理解、DPO 或 CPT 训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流**：支持生成**训练集**（SFT/DPO/CPT）和**评测集**（仅文本生成场景），输出为结构化 JSONL；支持平台存储（默认）与 OSS 挂载两种模式，但评测集仅支持平台存储 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- > **注意**：文档 1 明确声明“暂不支持 DPO-文本生成训练集”，而文档 2 明确列出日志回流支持 DPO 训练集。该矛盾表明：**DPO 训练集仅可通过日志回流生成，不可通过数据清洗/增强节点处理**。实际使用中，DPO 数据必须经由日志回流产出，再导入后可选做清洗（见下文“限制和注意事项”）。

## 关键参数

| 功能 | 参数 | 说明 |
|------|------|------|
| **数据清洗节点** | `dataSetCount`（只读） | 表示当前节点输出的 messages 数量，用于条件判断等下游逻辑 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md) |
| **数据增强节点** | `生成样本数` | 单次任务最多生成 2000 条；若输入 10 条，设为 10，则输出共 20 条（含原始） |
| **日志回流** | 时间范围 | 仅支持最近 30 天（含当天），精确到秒；修改后联动重置 API Key 和模型选择 |
| | 单次回流上限 | 10 万条（硬限制），超出部分静默丢弃；总量无上限，支持多版本追加 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md) |
| | 训练方式 | 创建后锁定，不可更改（SFT/DPO/CPT）；评测集不显示此字段 |

## 使用方式

- **数据清洗与增强**：通过控制台「数据管理 → 数据流」搭建可视化工作流。必须包含开始节点（输入 `对话文本`）、至少一个清洗/增强节点、结束节点（自动发布新版本）。目前**不提供公开 API**，仅支持控制台操作 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **日志回流**：在「模型监控」或「数据管理」页面入口创建，需先完成 SLS 审计日志 + 推理日志的**分步开通与授权**（审计日志为前置依赖），再配置时间范围、API Key、模型等参数。OSS 挂载模式需额外授权两个服务角色。  
- **组合使用**：日志回流产出的数据集（如 SFT 或 DPO 训练集）可作为数据清洗/增强节点的输入源，实现“日志→结构化→清洗→增强”全链路 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

## 限制和注意事项

- **地域限制**：两项功能均仅在**华北2（北京）和新加坡**可用；文档 1 提及“仅适用于华北2（北京）地域”，但文档 2 明确新增新加坡支持，故以文档 2 为准，新加坡亦可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。  
- **格式强约束**：数据清洗/增强仅接受 ChatML 格式 `.jsonl`；日志回流输出为标准 JSONL，但输入日志需经 SLS 正确采集并满足百炼解析协议。  
- **版本与覆盖**：所有处理（清洗、增强、回流）均生成**独立新版本**，绝不覆盖原数据集；用户需主动切换版本用于后续训练。  
- **敏感数据提示**：文档 1 明确建议，对法律文件、医学记录、文学作品、方言、用户评论等高敏或高价值文本，**不应使用自动化清洗/增强**，应人工审核或跳过 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。  
- **资源与费用**：开启推理日志将产生 SLS 存储与读写费用；OSS 挂载模式需额外承担 OSS 费用及 DataHub 导入成本。

## 来源文档

- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


