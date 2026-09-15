# model data overview

百炼平台的模型数据管理功能为大模型调优与评测提供统一、可控的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT/视觉/图生视频）和评测集两类核心资源。所有数据集均支持版本管理、多方式导入及结构化存储，是模型训练、评估与数据增强的基础载体。数据集创建即发布，不支持草稿暂存，需在创建前明确用途与配置。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧）、图生视频（首尾帧）四类训练场景；对应训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 与 CPT 仅限北京地域使用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，用于模型泛化能力客观评估，不可用于训练 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：仅支持 SFT-文本生成训练集（ChatML 格式），提供数据清洗（如敏感信息打码、特殊内容移除）与数据增强（通用/分类/抽取/创作等场景）能力，当前仅在北京地域可用 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流**：支持将 SLS 推理日志自动转化为结构化 JSONL 数据集，可用于训练集（SFT/DPO/CPT）或评测集，当前在华北2（北京）和新加坡 Region 可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

> **注意**：文档 2 明确指出“数据处理暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，但文档 1 中“训练方法与场景”表格未排除 DPO 训练集用于数据处理。实际以文档 2 为准——DPO 训练集**不可用于数据清洗或增强**。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值范围/约束 |
|------|------|----------|----------------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3）；创建后不可修改 |
| 数据集类型 | 决定下游用途 | 是 | `训练集` 或 `评测集`，创建后不可变更 |
| 训练场景 | 数据适用的模态与任务类型 | 是 | `文本生成` / `视觉理解` / `图生视频（首帧）` / `图生视频（首尾帧）`；评测集仅允许 `文本生成` |
| 训练方法 | 仅训练集必选 | 是 | `SFT`（全站点）、`DPO`（北京）、`CPT`（北京） |
| 数据格式 | 文件组织形式 | 是 | `Jsonl 格式` 或 `Excel 格式` |
| 存储位置 | 数据物理存放方式 | 是 | `平台 OSS 存储`（免费，自动发布）或 `云存储挂载`（需 OSS 授权，仅训练集可用，不支持评测集） |
| 导入方式 | 数据来源路径 | 是 | `本地上传` / `从 OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`） / `日志回流` / `API 上传` |

- **日志回流特有参数**：时间范围（仅最近 30 天）、API Key 过滤（全部/其他/指定）、模型选择（最多 10 个）、OSS 数据路径（仅挂载模式）；修改时间范围或训练方式会联动重置其他字段 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 使用方式

- **创建数据集**：通过控制台 **[数据管理](https://bailian.console.aliyun.com/cn-beijing/model/data)** > **数据集** > **创建数据集** 完成全流程配置。SFT/DPO 文本生成支持多文件本地上传；OSS 导入需提前为 Bucket 添加标签 `bailian-datahub-access=read`；日志回流需先完成 SLS 审计日志与推理日志的开通及角色授权 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **数据处理**：仅对已发布的 SFT-文本生成训练集生效。在 **数据管理** > **数据流** 页签中创建数据流（含清洗/增强节点），再通过 **任务列表** 启动数据流任务。处理结果将自动生成新版本（如 V1 → V2），原版本不受影响 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **日志回流追加**：支持两种增量方式：① 进入已有数据集的 **导入数据** 页面，选择日志回流；② 在数据集详情页点击 **新增版本**（仅平台存储数据集可用）。OSS 挂载数据集必须使用方式① [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、数据清洗与增强、日志回流功能均**仅在北京地域可用**；日志回流额外支持新加坡 Region [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **不可变性**：数据集类型、训练场景、训练方法、存储位置、数据格式一经创建即锁定，不可编辑 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **容量与数量**：单次日志回流上限 10 万条（可多次追加）；数据集创建数量无限制，导入数据量无上限；但 OSS 导入不支持评测集 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **版本管理**：新增版本采用**全量新建模式**，不支持基于上一版本的增量修改；历史草稿版本可在线编辑，但已发布版本不可编辑 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **安全与合规**：所有导入数据默认启用 OSS 服务端加密（SSE-OSS）；敏感信息打码等清洗操作需人工校验输出完整性，避免误删关键语义 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
- **发布与删除**：发布操作不可逆，已发布版本不可再编辑；删除操作不可恢复，且会移除该数据集下所有版本，请谨慎执行 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


