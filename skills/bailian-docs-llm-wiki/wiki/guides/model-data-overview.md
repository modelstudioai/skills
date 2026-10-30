# model data overview

百炼平台的模型数据管理功能为大模型训练与评测提供统一的数据集生命周期支持，涵盖训练集（SFT/DPO/CPT）、评测集的创建、导入、版本管理及后处理。所有数据集均需在业务空间内显式创建并发布，支持多地域部署但部分能力存在地域限制。数据质量直接影响调优与评测效果，建议结合数据清洗与增强等工具提升数据可用性。

## 支持的模型/功能

- **训练集**：支持文本生成、视觉理解、图生视频（首帧/首尾帧）四类训练场景；训练方法包括 SFT（监督微调）、DPO（直接偏好优化）和 CPT（持续预训练）。其中 DPO 与 CPT 仅限北京地域使用 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **评测集**：仅支持文本生成场景，可用于模型泛化能力评估 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **日志回流**：将 SLS 推理日志自动转化为结构化 JSONL 数据集，支持训练集（SFT/DPO/CPT）和评测集两类用途，当前仅在北京和新加坡地域可用 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据处理**：支持对已发布的 SFT-文本生成训练集（ChatML 格式）进行清洗（如敏感信息打码、特殊内容移除）与增强（如 Few-Shot 生成），暂不支持 DPO、CPT 或视觉类训练集 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。

> **注意**：文档 2 明确指出“数据处理支持 SFT-文本生成训练集，暂不支持 SFT-图片理解训练集和 DPO-文本生成训练集”，而文档 1 中“训练方法与场景”表格未标注此限制，实际以文档 2 的明确声明为准。

## 关键参数

| 参数 | 说明 | 是否必填 | 取值范围/约束 |
|------|------|----------|----------------|
| 数据集名称 | 唯一标识符 | 是 | ≤50 字符，支持中文、英文、数字、下划线、连字符、点（文档 1）或斜杠（文档 3）；创建后不可修改 |
| 数据集类型 | 决定下游用途 | 是 | `训练集` 或 `评测集`，创建后不可变更 |
| 训练场景 | 数据适用的模态与任务类型 | 是 | 文本生成 / 视觉理解 / 图生视频（首帧）/ 图生视频（首尾帧）；评测集仅允许文本生成 |
| 训练方法 | 仅训练集必填 | 是 | `SFT`（全地域）、`DPO`（仅北京）、`CPT`（仅北京） |
| 数据格式 | 文件组织方式 | 是 | `Jsonl 格式` 或 `Excel 格式`，推荐按模板准备 |
| 存储位置 | 数据物理存放方式 | 是 | `平台 OSS 存储`（免费，自动加密）或 `云存储挂载`（需 OSS 标签授权，仅训练集支持） |
| 导入方式 | 数据来源路径 | 是 | `本地上传` / `从 OSS 导入`（需 Bucket 标签 `bailian-datahub-access=read`） / `日志回流` / `API 上传` |

> **注意**：文档 1 和文档 3 对“数据集名称”支持字符的描述存在差异（文档 1 允许点 `.`，文档 3 允许斜杠 `/`），实际控制台校验以最新控制台行为为准，建议避免使用非常规符号以防兼容问题。

## 使用方式

1. **创建数据集**：进入 [数据管理 > 数据集](https://bailian.console.aliyun.com/cn-beijing/model/data) 页面，点击“创建数据集”，依次填写名称、类型、场景、方法、格式、存储位置及导入方式。提交即发布，无草稿保存机制（历史草稿版本除外）[训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
2. **日志回流**：需先在 [模型监控](https://bailian.console.aliyun.com/cn-beijing/model/telemetry) 完成审计日志与推理日志的开通及角色授权（`AliyunServiceRoleForSFMAccessSLS` 等），再通过任一入口（监控页、详情页、数据管理页）配置时间范围、API Key、模型等参数发起回流 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
3. **数据处理**：仅支持已发布的 SFT-文本生成训练集（ChatML 格式）。在 [数据管理 > 数据流](https://bailian.console.aliyun.com/cn-beijing/model/data?tab=data_flow) 创建数据流，编排“数据清洗”与“数据增强”节点，再通过“任务列表”选择目标训练集启动处理任务，结果自动生成新版本 [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)。
4. **版本管理**：所有数据集支持多版本，新增版本需重新导入全部数据（非增量更新）。仅历史草稿版本可在线编辑；已发布版本不可编辑，仅可导出（SFT 导出为 jsonl，视觉类导出为 zip，评测集导出为 xlsx）。

## 限制和注意事项

- **地域限制**：DPO/CPT 训练、云存储挂载、数据处理功能均仅限华北2（北京）地域；日志回流额外支持新加坡地域 [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)。
- **数据量限制**：
  - 日志回流单次上限 10 万条，但可通过多次回流至不同版本突破总量限制；
  - 数据增强-通用节点单次最多生成 2000 条样本；
  - 不支持创建或发布空数据集。
- **不可逆操作**：发布、删除（含整个数据集及其所有版本）均不可恢复；已发布版本不可编辑 [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)。
- **格式与兼容性**：
  - 数据处理仅接受 ChatML 格式的 SFT-文本生成训练集，其他格式（如纯文本、JSONL 非 ChatML 结构）将失败；
  - 评测集不支持从 OSS 导入，也不支持 OSS 挂载存储；
  - 所有导入数据默认启用 OSS 服务端加密（SSE-OSS）。
- **计费提示**：数据管理功能本身免费，但平台 OSS 存储、OSS 挂载、SLS 日志服务等下游资源按各自产品计费规则收费，使用前请查阅百炼计费文档。

## 来源文档

- [训练集与评测集](../../raw/model-user-guide/model-data-overview/training-set-and-evaluation-set.md)
- [数据清洗或增强](../../raw/model-user-guide/model-data-overview/data-processing.md)
- [日志回流](../../raw/model-user-guide/model-data-overview/model-log-backflow.md)


