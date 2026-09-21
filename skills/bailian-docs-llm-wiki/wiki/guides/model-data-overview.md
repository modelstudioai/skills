# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可控的数据基础设施。它支持训练集（SFT/DPO/CPT/视觉/图生视频）和评测集（文本生成）两类数据集的全生命周期管理，涵盖创建、导入、版本控制、清洗增强及下游集成。所有数据集均默认启用 OSS 服务端加密（SSE-OSS），存储与计算分离，开发者可通过控制台或 API 灵活接入。

## 支持的模型/功能

- **训练集**：支持四类训练场景：  
  - 文本生成（SFT/DPO/CPT）  
  - 视觉理解（图/视频→文本）  
  - 图生视频（首帧）  
  - 图生视频（首尾帧）  
  其中 SFT 和 DPO 支持日志回流构建，CPT 仅限北京地域；视觉与图生视频暂无官方推荐数据量，需按场景足量准备。  
- **评测集**：仅支持文本生成场景，可用于模型评测与 A/B 对比，[详见模型评测概述](raw/model-user-guide/model-evaluation-introduction/model-evaluation-overview.md)。  
- **数据处理**：支持对 **SFT-文本生成训练集（ChatML 格式）** 进行清洗（如敏感信息打码、特殊内容移除）与增强（基于千问-Max 的 Few-Shot 生成），但不支持 DPO、CPT 或视觉类训练集 —— 此限制在 [数据清洗或增强](raw/model-user-guide/model-data-overview/data-processing.md) 文档中明确说明。  
> **注意**：文档 1 称“已发布数据集（含历史创建的草稿版本）均可用于数据处理”，但文档 3 明确限定仅支持 SFT-文本生成训练集，且强调“暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”。二者存在范围矛盾，**以文档 3 的精确限定为准**。

## 关键参数

| 参数 | 说明 | 必填 | 取值约束 |
|------|------|------|-----------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符；支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 2） |
| 数据集类型 | 训练集 / 评测集 | 是 | 创建后不可变更（[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)） |
| 训练场景 | 文本生成 / 视觉理解 / 图生视频（首帧/首尾帧） | 是 | 评测集仅允许“文本生成” |
| 训练方法 | SFT / DPO / CPT | 是（训练集） | DPO/CPT 仅北京地域可用；评测集不显示该字段 |
| 数据格式 | Jsonl / Excel | 是 | 推荐下载模板校验结构（文档 1） |
| 存储位置 | 平台 OSS 存储 / 云存储挂载 | 是 | 评测集禁用“云存储挂载”；OSS 挂载需额外授权（[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)） |
| 导入方式 | 本地上传 / OSS 导入 / 日志回流 / API 上传 | 是 | 评测集不支持 OSS 导入（文档 1）；日志回流支持训练集与评测集（文档 2） |

## 使用方式

- **创建与导入**：  
  在 [数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data) 页面点击“创建数据集”，按向导填写参数并选择导入方式。  
  - *本地上传*：适合小批量，支持多文件（SFT/DPO 文本）。  
  - *OSS 导入*：需为目标 Bucket 添加标签 `bailian-datahub-access=read`，仅训练集可用。  
  - *日志回流*：从 SLS 推理日志自动提取结构化数据，支持北京/新加坡地域，单次上限 10 万条（[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)）。  
  - *API 上传*：通过 `training_file_ids` 引用已发布数据集 ID，适用于自动化流水线（[fine-tuning-api-guide.md](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)）。  

- **版本管理**：  
  新增版本采用“新建模式”，需重新导入全部数据（非增量）；历史草稿版本可在线编辑 Prompt/Completion，已发布版本不可编辑（文档 1）。  

- **数据处理（清洗/增强）**：  
  仅限北京地域，仅支持 SFT-文本生成训练集（ChatML 格式）。通过 [数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow) 搭建数据流任务，系统自动生成新版本（V2、V3…），原版本保留（[数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)）。

## 限制和注意事项

- **地域限制**：  
  - DPO/CPT 训练、云存储挂载、数据处理功能仅在北京地域可用（文档 1 & 3）。  
  - 日志回流支持北京与新加坡，其他 Region 不显示入口（文档 2）。  

- **数据量与格式**：  
  - 训练集无总量上限，但日志回流单次上限 10 万条（可多次追加）；SFT 建议 ≥1000 条，DPO ≥100 条，CPT ≥5000 万 Token（文档 1）。  
  - 评测集必须与训练集数据不重叠，确保评估客观性（文档 1）。  
  - 所有导入数据自动启用 SSE-OSS 加密（文档 1）。  

- **操作风险**：  
  - 发布与删除操作均**不可逆**：发布后版本不可编辑；删除整个数据集将移除其所有版本（文档 1）。  
  - OSS 挂载数据集不支持“新增版本”，只能通过“导入数据页”追加（文档 2）。  
  - 日志回流时间范围严格限定为最近 30 天（含当天），且预估数据量仅为近似值，实际结果可能略有差异（文档 2）。  

- **计费提示**：  
  数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费（文档 1）。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)


