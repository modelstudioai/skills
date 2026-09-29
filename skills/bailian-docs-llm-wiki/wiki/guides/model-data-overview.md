# model data [overview](overview.md)

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT）、评测集的创建、导入、版本管理及后处理。所有数据集均需在业务空间下统一管理，支持多地域部署但部分能力存在地域限制。

## 支持的模型/功能

- **训练集类型**：支持文本生成、视觉理解、图生视频（首帧/首尾帧）四类训练场景；仅文本生成场景支持全部训练方法（SFT、DPO、CPT），其余场景当前仅支持 SFT。
- **评测集类型**：仅支持文本生成场景，不可用于视觉或视频类任务。
- **核心功能**：
  - 数据集创建与多版本管理（自动递增版本号，不支持增量编辑）；
  - 四种导入方式：本地上传、OSS 导入、日志回流、API 上传；
  - 数据处理（清洗与增强）：目前**仅支持 SFT-文本生成训练集（ChatML 格式）**，不支持 DPO 训练集、视觉理解训练集或评测集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)；
  - 日志回流：将 SLS 推理日志结构化为 JSONL 数据集，支持训练集（SFT/DPO/CPT）和评测集，但仅在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出数据处理“暂不支持[SFT-图片理解训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)和[DPO-文本生成训练集](https://help.aliyun.com/zh/model-studio/model-training-overview#2f5553c6d832d)”，而文档 1 表述为“训练集支持4种训练场景”，未限定数据处理兼容性。此处以文档 2 的明确限制为准。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值范围/约束 |
|------|------|----------|----------------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3） |
| 数据集类型 | 创建后不可变更 | 是 | `训练集` 或 `评测集` |
| 训练场景 | 仅训练集需选 | 是 | `文本生成` / `视觉理解` / `图生视频（首帧）` / `图生视频（首尾帧）` |
| 训练方法 | 仅训练集需选 | 是 | `SFT`（全站点）、`DPO`（仅北京）、`CPT`（仅北京） |
| 数据格式 | 仅影响导入解析 | 是 | `Jsonl 格式` 或 `Excel 格式` |
| 存储位置 | 影响计费与权限 | 是 | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 标签 `bailian-datahub-access=read`，仅训练集可用） |
| 导入方式 | 决定前置条件 | 是 | `本地上传` / `从 OSS 导入` / `日志回流` / `API 上传` |

- **日志回流特有参数**：时间范围（最近 30 天）、API Key 过滤（全部/其他/指定）、模型选择（最多 10 个）、OSS 数据路径（仅挂载模式）——详见 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 使用方式

- **创建流程**：进入 [数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data) > **数据集** > **创建数据集**，按向导填写参数并选择导入方式。
- **导入方式选择指南**：
  - 小批量数据 → 本地上传；
  - 大批量结构化数据 → 从 OSS 导入（需 Bucket 标签授权）；
  - 从线上推理反馈构建训练数据 → 日志回流（需先开通审计日志与推理日志，并授权 SLS 角色）[日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)；
  - 自动化集成 → API 上传（参考 [使用 API 或命令行进行模型调优](raw/model-user-guide/fine-tuning/fine-tune-text-generation-model/fine-tuning-api-guide.md)）。
- **数据处理（清洗/增强）**：仅限已发布的 SFT-文本生成训练集，在 **数据管理 > 数据流** 中创建数据流任务，支持敏感信息打码、去重、毒性消除等清洗算子，以及基于千问-Max 的 Few-Shot 数据增强 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **下游调用**：训练集 ID 可通过 `training_file_ids` 参数传入模型调优 API；评测集 ID 用于模型评测任务。

## 限制和注意事项

- **地域限制**：
  - DPO/CPT 训练、数据处理、日志回流（除新加坡外）均**仅支持华北2（北京）**；
  - 评测集不支持 OSS 导入和 OSS 挂载存储；
  - 日志回流在非北京/新加坡 Region 不显示入口。
- **数据量与容量**：
  - 单次日志回流上限 10 万条（可多次追加至不同版本）；
  - CPT 推荐数据量 ≥5000 万 Token；SFT 推荐 ≥1000 条；DPO 推荐 ≥100 条；
  - 数据集创建数量无限制，平台 OSS 存储无数据量上限。
- **不可逆操作**：
  - 发布后的数据集版本不可编辑、不可删除；
  - 删除整个数据集将移除其所有版本，操作不可恢复；
  - 新增版本采用**新建模式**（全量重传），不支持基于上一版本的增量修改。
- **格式与兼容性**：
  - 数据处理仅接受 ChatML 格式的 SFT-文本生成训练集，不兼容 Excel 或其他 JSONL 变体；
  - 评测集必须与训练集数据不重叠，确保评估客观性；
  - 所有导入数据默认启用 OSS 服务端加密（SSE-OSS）。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务将产生独立费用，请查阅百炼计费文档。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


